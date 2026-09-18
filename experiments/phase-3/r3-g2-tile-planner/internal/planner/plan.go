package planner

import (
	"crypto/sha256"
	"encoding/hex"
	"errors"
	"fmt"
	"sort"
	"strconv"
	"strings"

	"example.invalid/mneme-r3-g2-tile-planner/internal/tlog"
)

var errPlanCapture = errors.New(planSentinelText)

type recordingTileReader struct {
	height    int
	tiles     []tlog.Tile
	saveCalls int
}

func (reader *recordingTileReader) Height() int {
	return reader.height
}

func (reader *recordingTileReader) ReadTiles(tiles []tlog.Tile) ([][]byte, error) {
	reader.tiles = append(reader.tiles, tiles...)
	return nil, errPlanCapture
}

func (reader *recordingTileReader) SaveTiles(_ []tlog.Tile, _ [][]byte) {
	reader.saveCalls++
}

func buildPlan(responses []parsedResponse, cfg config) (planResult, error) {
	result := planResult{Inputs: make([]inputRow, 0, len(responses)), Responses: responses}
	for _, response := range responses {
		result.Inputs = append(result.Inputs, response.Input)
	}

	heads, err := buildHeads(responses, cfg.maxHeads)
	if err != nil {
		return result, err
	}
	result.Heads = heads
	headByID := make(map[string]head, len(heads))
	for _, item := range heads {
		headByID[item.ID] = item
	}
	responseByID := make(map[string]parsedResponse, len(responses))
	for _, response := range responses {
		responseByID[response.Input.InputID] = response
	}

	operations, err := buildOperations(responses, heads, cfg.maxOperations)
	if err != nil {
		return result, err
	}
	result.Operations = operations

	origins := make([]tileOrigin, 0, len(operations)*4)
	for _, operation := range operations {
		captured, captureErr := captureOperationTiles(operation, responseByID, headByID, cfg.tileHeight)
		if captureErr != nil {
			return result, fmt.Errorf("operation %s: %w", operation.ID, captureErr)
		}
		origins = append(origins, captured...)
	}
	sort.Slice(origins, func(i, j int) bool {
		left := origins[i].OperationID + "\x00" + origins[i].Path + "\x00" + origins[i].Role
		right := origins[j].OperationID + "\x00" + origins[j].Path + "\x00" + origins[j].Role
		return left < right
	})
	result.Origins = origins

	literalTiles, err := collapseLiteralTiles(origins, cfg.maxLiteralPaths)
	if err != nil {
		return result, err
	}
	result.LiteralTiles = literalTiles
	result.Conditions = successfulConditions(result)
	result.Complete = true
	return result, nil
}

func buildHeads(responses []parsedResponse, maxHeads int) ([]head, error) {
	byKey := make(map[string]*head, len(responses))
	for index := range responses {
		response := &responses[index]
		key := strconv.FormatInt(response.Tree.N, 10) + ":" + response.TreeRootBase64
		item, ok := byKey[key]
		if !ok {
			digest := sha256.Sum256([]byte(key))
			item = &head{
				ID:         "H-" + hex.EncodeToString(digest[:8]),
				Tree:       response.Tree,
				RootBase64: response.TreeRootBase64,
			}
			byKey[key] = item
		}
		response.HeadID = item.ID
		item.SourceInputIDs = append(item.SourceInputIDs, response.Input.InputID)
		item.SignedNoteHashes = append(item.SignedNoteHashes, response.SignedNoteSHA256)
	}
	if len(byKey) > maxHeads {
		return nil, fmt.Errorf("distinct head count %d exceeds cap %d", len(byKey), maxHeads)
	}
	heads := make([]head, 0, len(byKey))
	for _, item := range byKey {
		sort.Strings(item.SourceInputIDs)
		sort.Strings(item.SignedNoteHashes)
		heads = append(heads, *item)
	}
	sort.Slice(heads, func(i, j int) bool {
		if heads[i].Tree.N != heads[j].Tree.N {
			return heads[i].Tree.N < heads[j].Tree.N
		}
		return heads[i].RootBase64 < heads[j].RootBase64
	})
	for index := range heads {
		for other := range heads {
			if index != other && heads[index].Tree.N == heads[other].Tree.N && heads[index].RootBase64 != heads[other].RootBase64 {
				heads[index].VariantFlag = "POSSIBLE_FORK_OR_UNVERIFIED_VARIANT"
				break
			}
		}
	}
	seenIDs := make(map[string]struct{}, len(heads))
	for _, item := range heads {
		if _, exists := seenIDs[item.ID]; exists {
			return nil, fmt.Errorf("head identifier collision")
		}
		seenIDs[item.ID] = struct{}{}
	}
	return heads, nil
}

func buildOperations(responses []parsedResponse, heads []head, maxOperations int) ([]operation, error) {
	operations := make([]operation, 0, len(heads)*len(heads)+len(responses)*len(heads))
	for i := 0; i < len(heads); i++ {
		for j := i + 1; j < len(heads); j++ {
			older, newer := heads[i], heads[j]
			kind := "TREE_CONSISTENCY"
			if older.Tree.N == newer.Tree.N {
				kind = "EQUAL_SIZE_VARIANT_CONSISTENCY"
			}
			operations = append(operations, operation{
				Kind:             kind,
				Rationale:        "pairwise retained-head consistency closure",
				OlderHeadID:      older.ID,
				NewerHeadID:      newer.ID,
				EvaluationHeadID: newer.ID,
				ExpectedResult:   planSentinelText,
			})
		}
	}
	for _, response := range responses {
		for _, candidate := range heads {
			if candidate.Tree.N < response.Tree.N {
				continue
			}
			rationale := "record under every retained head not smaller than its own head"
			if candidate.ID == response.HeadID {
				rationale = "record under its own retained head"
			}
			operations = append(operations, operation{
				Kind:             "RECORD_CHECK",
				Rationale:        rationale,
				RecordInputID:    response.Input.InputID,
				RecordID:         response.RecordID,
				EvaluationHeadID: candidate.ID,
				ExpectedResult:   planSentinelText,
			})
		}
	}
	sort.Slice(operations, func(i, j int) bool {
		left := operationSortKey(operations[i])
		right := operationSortKey(operations[j])
		return left < right
	})
	if len(operations) > maxOperations {
		return nil, fmt.Errorf("operation count %d exceeds cap %d", len(operations), maxOperations)
	}
	for index := range operations {
		operations[index].ID = fmt.Sprintf("O-%03d", index+1)
	}
	return operations, nil
}

func operationSortKey(item operation) string {
	return strings.Join([]string{
		item.Kind,
		item.OlderHeadID,
		item.NewerHeadID,
		item.RecordInputID,
		fmt.Sprintf("%020d", item.RecordID),
		item.EvaluationHeadID,
	}, "\x00")
}

func captureOperationTiles(item operation, responses map[string]parsedResponse, heads map[string]head, tileHeight int) ([]tileOrigin, error) {
	recorder := &recordingTileReader{height: tileHeight}
	var err error
	switch item.Kind {
	case "RECORD_CHECK":
		response, ok := responses[item.RecordInputID]
		if !ok {
			return nil, fmt.Errorf("missing response %q", item.RecordInputID)
		}
		evaluationHead, ok := heads[item.EvaluationHeadID]
		if !ok {
			return nil, fmt.Errorf("missing evaluation head %q", item.EvaluationHeadID)
		}
		reader := tlog.TileHashReader(evaluationHead.Tree, recorder)
		_, err = reader.ReadHashes([]int64{tlog.StoredHashIndex(0, response.RecordID)})
	case "TREE_CONSISTENCY", "EQUAL_SIZE_VARIANT_CONSISTENCY":
		older, ok := heads[item.OlderHeadID]
		if !ok {
			return nil, fmt.Errorf("missing older head %q", item.OlderHeadID)
		}
		newer, ok := heads[item.NewerHeadID]
		if !ok {
			return nil, fmt.Errorf("missing newer head %q", item.NewerHeadID)
		}
		_, err = tlog.TreeHash(older.Tree.N, tlog.TileHashReader(newer.Tree, recorder))
	default:
		return nil, fmt.Errorf("unknown operation kind %q", item.Kind)
	}
	if !errors.Is(err, errPlanCapture) {
		return nil, fmt.Errorf("tile derivation returned %v, want %s", err, planSentinelText)
	}
	if recorder.saveCalls != 0 {
		return nil, fmt.Errorf("tile derivation attempted SaveTiles %d times", recorder.saveCalls)
	}
	if len(recorder.tiles) == 0 {
		return nil, fmt.Errorf("tile derivation captured no tile")
	}

	origins := make([]tileOrigin, 0, len(recorder.tiles)*2)
	seen := make(map[string]struct{}, len(recorder.tiles)*2)
	for _, tile := range recorder.tiles {
		primaryPath, err := canonicalTilePath(tile, tileHeight)
		if err != nil {
			return nil, err
		}
		primaryKey := primaryPath + "\x00PRIMARY"
		if _, exists := seen[primaryKey]; !exists {
			origins = append(origins, tileOrigin{OperationID: item.ID, Tile: tile, Path: primaryPath, Role: "PRIMARY", PrimaryPath: primaryPath})
			seen[primaryKey] = struct{}{}
		}
		if tile.W < 1<<tileHeight {
			full := tile
			full.W = 1 << tileHeight
			fullPath, pathErr := canonicalTilePath(full, tileHeight)
			if pathErr != nil {
				return nil, pathErr
			}
			fallbackKey := fullPath + "\x00FULL_FALLBACK_CANDIDATE\x00" + primaryPath
			if _, exists := seen[fallbackKey]; !exists {
				origins = append(origins, tileOrigin{OperationID: item.ID, Tile: full, Path: fullPath, Role: "FULL_FALLBACK_CANDIDATE", PrimaryPath: primaryPath})
				seen[fallbackKey] = struct{}{}
			}
		}
	}
	return origins, nil
}

func canonicalTilePath(tile tlog.Tile, tileHeight int) (string, error) {
	if tile.H != tileHeight || tile.L < 0 || tile.L > 63 || tile.N < 0 || tile.W < 1 || tile.W > 1<<tileHeight {
		return "", fmt.Errorf("tile coordinate is outside accepted bounds: H=%d L=%d N=%d W=%d", tile.H, tile.L, tile.N, tile.W)
	}
	native := tile.Path()
	if native == "" || strings.HasPrefix(native, "/") || !strings.HasPrefix(native, "tile/8/") || strings.Contains(native, "/data/") || strings.ContainsAny(native, "*?[]{}\\\t\r\n") {
		return "", fmt.Errorf("noncanonical or forbidden tile path %q", native)
	}
	path := "/" + native
	if strings.Contains(path, "//") || strings.Contains(path, "/../") || strings.HasSuffix(path, "/..") {
		return "", fmt.Errorf("tile path contains a noncanonical segment: %q", path)
	}
	return path, nil
}

func collapseLiteralTiles(origins []tileOrigin, maxPaths int) ([]literalTile, error) {
	type aggregate struct {
		tile       tlog.Tile
		path       string
		role       string
		primary    string
		operations map[string]struct{}
	}
	byKey := make(map[string]*aggregate, len(origins))
	for _, origin := range origins {
		item, ok := byKey[origin.Path]
		if !ok {
			item = &aggregate{tile: origin.Tile, path: origin.Path, role: origin.Role, primary: origin.PrimaryPath, operations: make(map[string]struct{})}
			byKey[origin.Path] = item
		} else {
			if item.tile.H != origin.Tile.H || item.tile.L != origin.Tile.L || item.tile.N != origin.Tile.N || item.tile.W != origin.Tile.W {
				return nil, fmt.Errorf("literal path %q maps to inconsistent tile coordinates", origin.Path)
			}
			if origin.Role == "PRIMARY" {
				item.role = "PRIMARY"
				item.primary = origin.Path
			} else if item.role != "PRIMARY" && origin.PrimaryPath < item.primary {
				// All fallback causes remain in tile-origins.tsv. The literal
				// manifest keeps one deterministic representative cause so the
				// path itself remains unique.
				item.primary = origin.PrimaryPath
			}
		}
		item.operations[origin.OperationID] = struct{}{}
	}
	if len(byKey) > maxPaths {
		return nil, fmt.Errorf("literal path row count %d exceeds cap %d", len(byKey), maxPaths)
	}
	items := make([]*aggregate, 0, len(byKey))
	for _, item := range byKey {
		items = append(items, item)
	}
	sort.Slice(items, func(i, j int) bool {
		return items[i].path < items[j].path
	})
	result := make([]literalTile, 0, len(items))
	for index, item := range items {
		operationIDs := make([]string, 0, len(item.operations))
		for operationID := range item.operations {
			operationIDs = append(operationIDs, operationID)
		}
		sort.Strings(operationIDs)
		digest := sha256.Sum256([]byte(strings.Join(operationIDs, "\n") + "\n"))
		result = append(result, literalTile{
			ManifestID:      fmt.Sprintf("T-%04d", index+1),
			Path:            item.path,
			Role:            item.role,
			TileHeight:      item.tile.H,
			TileLevel:       item.tile.L,
			TileNumber:      item.tile.N,
			TileWidth:       item.tile.W,
			ExpectedBytes:   item.tile.W * tlog.HashSize,
			PrimaryPath:     item.primary,
			OriginCount:     len(operationIDs),
			OriginIDsSHA256: hex.EncodeToString(digest[:]),
			OriginIDs:       operationIDs,
		})
	}
	return result, nil
}

func successfulConditions(result planResult) []conditionResult {
	return []conditionResult{
		{ID: "SC-01", Status: "PASS", Detail: fmt.Sprintf("exactly %d declared, identity-checked inputs", len(result.Inputs))},
		{ID: "SC-02", Status: "PASS", Detail: fmt.Sprintf("%d responses parsed as unverified structure", len(result.Responses))},
		{ID: "SC-03", Status: "PASS", Detail: fmt.Sprintf("%d distinct unverified heads retained", len(result.Heads))},
		{ID: "SC-04", Status: "PASS", Detail: fmt.Sprintf("%d order-closure operations enumerated", len(result.Operations))},
		{ID: "SC-05", Status: "PASS", Detail: fmt.Sprintf("%d operation-to-tile origins captured through the required sentinel", len(result.Origins))},
		{ID: "SC-06", Status: "PASS", Detail: fmt.Sprintf("%d literal primary/fallback manifest rows emitted", len(result.LiteralTiles))},
		{ID: "SC-07", Status: "PASS", Detail: "no cryptographic authentication claim was made"},
	}
}
