package planner

import (
	"bytes"
	"encoding/json"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func syntheticCompletePlan(t *testing.T) planResult {
	t.Helper()
	responses := []parsedResponse{syntheticParsedResponse("L01", 0, 1, "output-plan")}
	result, err := buildPlan(responses, exactSyntheticConfig())
	if err != nil {
		t.Fatalf("build synthetic output plan: %v", err)
	}
	return result
}

func TestOutputNamesSchemasAndLiteralPathUniqueness(t *testing.T) {
	expectedNames := []string{
		"planner-inputs.tsv",
		"response-structure.jsonl",
		"tree-heads.tsv",
		"operation-matrix.tsv",
		"tile-origins.tsv",
		"literal-tile-manifest.tsv",
		"structural-sufficiency.json",
		"planner-source-manifest.tsv",
		"negative-inventory.json",
		"stop-register.md",
	}
	if strings.Join(outputNames, "\n") != strings.Join(expectedNames, "\n") {
		t.Fatalf("output name contract changed")
	}

	result := syntheticCompletePlan(t)
	schemaChecks := []struct {
		name   string
		body   []byte
		header string
	}{
		{"planner-inputs.tsv", renderInputs(result.Inputs), "input_id\tsource_relative_path\tdestination_relative_path\tbytes\tsha256\treconciliation\n"},
		{"tree-heads.tsv", renderHeads(result.Heads), "head_id\tunverified_tree_size\tunverified_root_base64\tsource_input_ids\tsigned_note_hashes\tvariant_flag\ttrust\n"},
		{"operation-matrix.tsv", renderOperations(result.Operations), "operation_id\tkind\trationale\trecord_input_id\trecord_id\tolder_head_id\tnewer_head_id\tevaluation_head_id\texpected_result\n"},
		{"tile-origins.tsv", renderOrigins(result.Origins), "operation_id\tpath\trole\ttile_height\ttile_level\ttile_number\ttile_width\texpected_bytes\tprimary_path\n"},
		{"literal-tile-manifest.tsv", renderLiteralTiles(result.LiteralTiles), "manifest_id\tpath\trole\ttile_height\ttile_level\ttile_number\ttile_width\texpected_bytes\tprimary_path\torigin_count\torigin_ids_sha256\n"},
	}
	for _, check := range schemaChecks {
		if !bytes.HasPrefix(check.body, []byte(check.header)) {
			t.Fatalf("%s header differs from the accepted schema", check.name)
		}
		if bytes.Contains(check.body, []byte{'\r'}) || len(check.body) == 0 || check.body[len(check.body)-1] != '\n' {
			t.Fatalf("%s is not normalized LF text", check.name)
		}
	}

	seen := make(map[string]struct{}, len(result.LiteralTiles))
	for _, item := range result.LiteralTiles {
		if _, exists := seen[item.Path]; exists {
			t.Fatalf("duplicate literal tile path %q", item.Path)
		}
		seen[item.Path] = struct{}{}
		if item.ManifestID == "" || item.OriginCount < 1 || item.OriginIDsSHA256 == "" {
			t.Fatalf("literal tile %q lacks deterministic provenance", item.Path)
		}
	}
}

func TestSyntheticOutputsAreByteDeterministic(t *testing.T) {
	requireSyntheticCase(t, "SYN-OUTPUT-DETERMINISM")
	result := syntheticCompletePlan(t)
	rootA := t.TempDir()
	rootB := t.TempDir()
	if err := writeOutputs(rootA, result); err != nil {
		t.Fatalf("write first synthetic output set: %v", err)
	}
	if err := writeOutputs(rootB, result); err != nil {
		t.Fatalf("write second synthetic output set: %v", err)
	}
	for _, name := range outputNames {
		left, err := os.ReadFile(filepath.Join(rootA, name))
		if err != nil {
			t.Fatalf("read first %s: %v", name, err)
		}
		right, err := os.ReadFile(filepath.Join(rootB, name))
		if err != nil {
			t.Fatalf("read second %s: %v", name, err)
		}
		if !bytes.Equal(left, right) {
			t.Fatalf("synthetic output %s differs across fresh roots", name)
		}
	}
}

func TestIncompleteMarkerFailsClosed(t *testing.T) {
	requireSyntheticCase(t, "SYN-INCOMPLETE-MARKER")
	root := t.TempDir()
	marker := []byte("# Planner Stop Register\n\nUNVERIFIED AND INCOMPLETE: output promotion did not finish.\n")
	markerPath := filepath.Join(root, "stop-register.md")
	if err := writeExclusive(markerPath, marker); err != nil {
		t.Fatalf("write synthetic incomplete marker: %v", err)
	}
	conflict := filepath.Join(root, "planner-inputs.tsv")
	if err := os.Mkdir(conflict, 0o700); err != nil {
		t.Fatalf("create synthetic exclusive-write conflict: %v", err)
	}
	if err := writeExclusive(conflict, []byte("must-not-write\n")); err == nil {
		t.Fatalf("exclusive output conflict unexpectedly succeeded")
	}
	retained, err := os.ReadFile(markerPath)
	if err != nil {
		t.Fatalf("read retained incomplete marker: %v", err)
	}
	if !bytes.Equal(retained, marker) {
		t.Fatalf("incomplete marker changed after output failure")
	}
	if _, err := os.Stat(filepath.Join(root, "structural-sufficiency.json")); !os.IsNotExist(err) {
		t.Fatalf("a PASS-bearing output was promoted after failure")
	}
}

func TestNormalizedSufficiencyAndNegativeInventory(t *testing.T) {
	result := syntheticCompletePlan(t)
	sufficiency, err := renderSufficiency(result)
	if err != nil {
		t.Fatalf("render synthetic sufficiency: %v", err)
	}
	var sufficiencyDocument sufficiencyJSON
	if err := json.Unmarshal(sufficiency, &sufficiencyDocument); err != nil {
		t.Fatalf("decode synthetic sufficiency: %v", err)
	}
	if sufficiencyDocument.Status != "PASS" || sufficiencyDocument.TrustBoundary != structuralTrustLabel || sufficiencyDocument.ChecksumIntegrityProven {
		t.Fatalf("sufficiency document crossed the structural trust boundary")
	}

	requireSyntheticCase(t, "SYN-NEGATIVE-INVENTORY")
	negative, err := renderNegativeInventory()
	if err != nil {
		t.Fatalf("render synthetic negative inventory: %v", err)
	}
	var inventory negativeInventoryJSON
	if err := json.Unmarshal(negative, &inventory); err != nil {
		t.Fatalf("decode synthetic negative inventory: %v", err)
	}
	if inventory.TrustBoundary != structuralTrustLabel ||
		inventory.VerifierKeys != 0 ||
		inventory.SignatureVerifications != 0 ||
		inventory.MerkleVerifications != 0 ||
		inventory.TileBodiesRead != 0 ||
		inventory.SaveTilesCalls != 0 ||
		inventory.NetworkActions != 0 ||
		inventory.Listeners != 0 ||
		inventory.ChildProcesses != 0 ||
		inventory.GoCacheReads != 0 ||
		inventory.GoSumWrites != 0 ||
		inventory.GraphCommands != 0 ||
		inventory.AuthenticationResults != 0 {
		t.Fatalf("negative inventory contains a nonzero forbidden capability")
	}
	if bytes.Contains(negative, []byte{'\r'}) || negative[len(negative)-1] != '\n' {
		t.Fatalf("negative inventory is not normalized LF JSON")
	}
}

func TestIncompletePlanCannotBePromoted(t *testing.T) {
	root := t.TempDir()
	err := writeOutputs(root, planResult{Complete: false})
	assertErrorContains(t, err, "refuse to promote outputs")
	entries, readErr := os.ReadDir(root)
	if readErr != nil {
		t.Fatalf("read incomplete-plan output root: %v", readErr)
	}
	if len(entries) != 0 {
		t.Fatalf("incomplete plan created %d outputs", len(entries))
	}
}
