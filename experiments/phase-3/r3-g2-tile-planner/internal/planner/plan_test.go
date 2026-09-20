package planner

import (
	"errors"
	"strings"
	"testing"

	"example.invalid/mneme-r3-g2-tile-planner/internal/tlog"
)

func TestSyntheticValid14Plan(t *testing.T) {
	requireSyntheticCase(t, "SYN-VALID-14")
	responses := make([]parsedResponse, 0, requiredMaxInputs)
	for index := 0; index < requiredMaxInputs; index++ {
		responses = append(responses, syntheticParsedResponse(requiredSyntheticInputID(index), int64(index), 16, "shared-tree-size-16"))
	}
	result, err := buildPlan(responses, exactSyntheticConfig())
	if err != nil {
		t.Fatalf("build synthetic plan: %v", err)
	}
	if !result.Complete || len(result.Inputs) != 14 || len(result.Responses) != 14 || len(result.Heads) != 1 || len(result.Operations) != 14 {
		t.Fatalf("unexpected complete-plan counts: complete=%v inputs=%d responses=%d heads=%d operations=%d", result.Complete, len(result.Inputs), len(result.Responses), len(result.Heads), len(result.Operations))
	}
	if len(result.Origins) == 0 || len(result.LiteralTiles) == 0 || len(result.Conditions) != 7 {
		t.Fatalf("synthetic plan lacks tile closure or sufficiency conditions")
	}
}

func TestSingleRecordAndHeadVariants(t *testing.T) {
	t.Run("SYN-SINGLE-RECORD", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-SINGLE-RECORD")
		responses := []parsedResponse{syntheticParsedResponse("L01", 0, 1, "single")}
		heads, err := buildHeads(responses, requiredMaxHeads)
		if err != nil {
			t.Fatalf("build single head: %v", err)
		}
		operations, err := buildOperations(responses, heads, requiredMaxOperations)
		if err != nil {
			t.Fatalf("build single-record operations: %v", err)
		}
		if len(heads) != 1 || len(operations) != 1 || operations[0].Kind != "RECORD_CHECK" || operations[0].RecordInputID != "L01" {
			t.Fatalf("unexpected single-record plan")
		}
	})

	t.Run("SYN-EQUAL-SAME-ROOT", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-EQUAL-SAME-ROOT")
		responses := []parsedResponse{
			syntheticParsedResponse("L01", 0, 2, "same-root"),
			syntheticParsedResponse("L02", 1, 2, "same-root"),
		}
		heads, err := buildHeads(responses, requiredMaxHeads)
		if err != nil {
			t.Fatalf("deduplicate equal synthetic heads: %v", err)
		}
		if len(heads) != 1 || strings.Join(heads[0].SourceInputIDs, ",") != "L01,L02" || heads[0].VariantFlag != "" {
			t.Fatalf("equal synthetic heads were not deterministically deduplicated")
		}
	})

	t.Run("SYN-EQUAL-DIFFERENT-ROOT", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-EQUAL-DIFFERENT-ROOT")
		responses := []parsedResponse{
			syntheticParsedResponse("L01", 0, 2, "variant-a"),
			syntheticParsedResponse("L02", 1, 2, "variant-b"),
		}
		heads, err := buildHeads(responses, requiredMaxHeads)
		if err != nil {
			t.Fatalf("retain equal-size synthetic variants: %v", err)
		}
		if len(heads) != 2 || heads[0].VariantFlag != "POSSIBLE_FORK_OR_UNVERIFIED_VARIANT" || heads[1].VariantFlag != "POSSIBLE_FORK_OR_UNVERIFIED_VARIANT" {
			t.Fatalf("equal-size synthetic variants lack the required flag")
		}
	})
}

func TestHeadSourceAndSignedNoteHashesRemainPaired(t *testing.T) {
	responses := []parsedResponse{
		syntheticParsedResponse("L10", 1, 2, "paired-head"),
		syntheticParsedResponse("L02", 0, 2, "paired-head"),
	}
	responses[0].SignedNoteSHA256 = "0000"
	responses[1].SignedNoteSHA256 = "ffff"
	heads, err := buildHeads(responses, requiredMaxHeads)
	if err != nil {
		t.Fatalf("build paired head: %v", err)
	}
	if len(heads) != 1 {
		t.Fatalf("paired responses produced %d heads, want 1", len(heads))
	}
	if strings.Join(heads[0].SourceInputIDs, ",") != "L02,L10" || strings.Join(heads[0].SignedNoteHashes, ",") != "ffff,0000" {
		t.Fatalf("source inputs and signed-note hashes lost pairing: %#v %#v", heads[0].SourceInputIDs, heads[0].SignedNoteHashes)
	}
}

func TestOperationClosureAndOrderIndependence(t *testing.T) {
	requireSyntheticCase(t, "SYN-MULTI-SIZE-HEADS")
	base := []parsedResponse{
		syntheticParsedResponse("L01", 0, 1, "size-1"),
		syntheticParsedResponse("L02", 0, 2, "size-2"),
		syntheticParsedResponse("L03", 0, 4, "size-4"),
	}
	heads, err := buildHeads(append([]parsedResponse{}, base...), requiredMaxHeads)
	if err != nil {
		t.Fatalf("build multi-size heads: %v", err)
	}
	responses := append([]parsedResponse{}, base...)
	heads, err = buildHeads(responses, requiredMaxHeads)
	if err != nil {
		t.Fatalf("assign multi-size head identities: %v", err)
	}
	operations, err := buildOperations(responses, heads, requiredMaxOperations)
	if err != nil {
		t.Fatalf("build multi-size operation closure: %v", err)
	}
	if len(heads) != 3 || len(operations) != 9 {
		t.Fatalf("multi-size closure counts = heads %d operations %d, want 3 and 9", len(heads), len(operations))
	}

	requireSyntheticCase(t, "SYN-ORDER-PERMUTATIONS")
	permutations := [][3]int{{0, 1, 2}, {0, 2, 1}, {1, 0, 2}, {1, 2, 0}, {2, 0, 1}, {2, 1, 0}}
	baseline := strings.Join(operationKeys(operations), "\n")
	for _, permutation := range permutations {
		candidate := []parsedResponse{base[permutation[0]], base[permutation[1]], base[permutation[2]]}
		candidateHeads, buildErr := buildHeads(candidate, requiredMaxHeads)
		if buildErr != nil {
			t.Fatalf("build permuted heads: %v", buildErr)
		}
		candidateOperations, buildErr := buildOperations(candidate, candidateHeads, requiredMaxOperations)
		if buildErr != nil {
			t.Fatalf("build permuted operations: %v", buildErr)
		}
		if strings.Join(operationKeys(candidateOperations), "\n") != baseline {
			t.Fatalf("operation closure changed for permutation %v", permutation)
		}
	}
}

func TestTilePathFallbackSentinelAndDeduplication(t *testing.T) {
	t.Run("SYN-POWER-OF-TWO", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-POWER-OF-TWO")
		path, err := canonicalTilePath(tlog.Tile{H: 8, L: 0, N: 0, W: 256}, 8)
		if err != nil {
			t.Fatalf("canonical full tile path: %v", err)
		}
		if path != "/tile/8/0/000" || strings.Contains(path, ".p/") {
			t.Fatalf("full tile path = %q", path)
		}
	})

	t.Run("SYN-LARGE-TILE-NUMBER", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-LARGE-TILE-NUMBER")
		path, err := canonicalTilePath(tlog.Tile{H: 8, L: 4, N: 1234567, W: 256}, 8)
		if err != nil {
			t.Fatalf("canonical large tile path: %v", err)
		}
		if path != "/tile/8/4/x001/x234/567" {
			t.Fatalf("large tile path = %q", path)
		}
	})

	t.Run("SYN-SENTINEL-REQUIRED", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-SENTINEL-REQUIRED")
		reader := &recordingTileReader{height: requiredTileHeight}
		_, err := reader.ReadTiles([]tlog.Tile{{H: 8, L: 0, N: 0, W: 1}})
		if !errors.Is(err, errPlanCapture) || err.Error() != planSentinelText || len(reader.tiles) != 1 {
			t.Fatalf("recording reader did not stop at the required sentinel")
		}
	})

	t.Run("ERR-SAVE-TILES", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-SAVE-TILES")
		reader := &recordingTileReader{height: requiredTileHeight}
		reader.SaveTiles([]tlog.Tile{{H: 8, L: 0, N: 0, W: 1}}, [][]byte{{0}})
		if reader.saveCalls != 1 {
			t.Fatalf("SaveTiles attempt was not recorded")
		}
	})

	t.Run("SYN-PARTIAL-FALLBACK", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-PARTIAL-FALLBACK")
		responses := []parsedResponse{syntheticParsedResponse("L01", 0, 1, "partial")}
		heads, err := buildHeads(responses, requiredMaxHeads)
		if err != nil {
			t.Fatalf("build partial-fallback head: %v", err)
		}
		operation := operation{ID: "O-001", Kind: "RECORD_CHECK", RecordInputID: "L01", RecordID: 0, EvaluationHeadID: heads[0].ID}
		origins, err := captureOperationTiles(operation, map[string]parsedResponse{"L01": responses[0]}, map[string]head{heads[0].ID: heads[0]}, requiredTileHeight)
		if err != nil {
			t.Fatalf("capture partial synthetic tile: %v", err)
		}
		roles := make(map[string]bool)
		for _, origin := range origins {
			roles[origin.Role] = true
		}
		if !roles["PRIMARY"] || !roles["FULL_FALLBACK_CANDIDATE"] {
			t.Fatalf("partial tile closure lacks primary or full fallback: %v", roles)
		}
	})

	t.Run("SYN-SHARED-TILES", func(t *testing.T) {
		requireSyntheticCase(t, "SYN-SHARED-TILES")
		tile := tlog.Tile{H: 8, L: 0, N: 0, W: 1}
		path, err := canonicalTilePath(tile, requiredTileHeight)
		if err != nil {
			t.Fatalf("canonical shared tile: %v", err)
		}
		items, err := collapseLiteralTiles([]tileOrigin{
			{OperationID: "O-001", Tile: tile, Path: path, Role: "PRIMARY", PrimaryPath: path},
			{OperationID: "O-002", Tile: tile, Path: path, Role: "PRIMARY", PrimaryPath: path},
		}, requiredMaxLiteralPaths)
		if err != nil {
			t.Fatalf("collapse shared synthetic tile: %v", err)
		}
		if len(items) != 1 || items[0].OriginCount != 2 || strings.Join(items[0].OriginIDs, ",") != "O-001,O-002" {
			t.Fatalf("shared tile origins were not preserved")
		}
	})
}

func TestPlannerCapsFailClosed(t *testing.T) {
	t.Run("ERR-HEAD-CAP", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-HEAD-CAP")
		responses := []parsedResponse{
			syntheticParsedResponse("L01", 0, 1, "head-a"),
			syntheticParsedResponse("L02", 0, 2, "head-b"),
		}
		_, err := buildHeads(responses, 1)
		assertErrorContains(t, err, "exceeds cap 1")
	})

	t.Run("ERR-OPERATION-CAP", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-OPERATION-CAP")
		responses := []parsedResponse{syntheticParsedResponse("L01", 0, 1, "operation-cap")}
		heads, err := buildHeads(responses, requiredMaxHeads)
		if err != nil {
			t.Fatalf("build operation-cap head: %v", err)
		}
		_, err = buildOperations(responses, heads, 0)
		assertErrorContains(t, err, "exceeds cap 0")
	})

	t.Run("ERR-PATH-CAP", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-PATH-CAP")
		tileA := tlog.Tile{H: 8, L: 0, N: 0, W: 1}
		tileB := tlog.Tile{H: 8, L: 0, N: 1, W: 1}
		pathA, _ := canonicalTilePath(tileA, requiredTileHeight)
		pathB, _ := canonicalTilePath(tileB, requiredTileHeight)
		_, err := collapseLiteralTiles([]tileOrigin{
			{OperationID: "O-001", Tile: tileA, Path: pathA, Role: "PRIMARY", PrimaryPath: pathA},
			{OperationID: "O-002", Tile: tileB, Path: pathB, Role: "PRIMARY", PrimaryPath: pathB},
		}, 1)
		assertErrorContains(t, err, "exceeds cap 1")
	})
}
