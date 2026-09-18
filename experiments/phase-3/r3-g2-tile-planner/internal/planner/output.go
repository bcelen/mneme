package planner

import (
	"bytes"
	"encoding/json"
	"fmt"
	"os"
	"path/filepath"
	"strconv"
	"strings"

	"example.invalid/mneme-r3-g2-tile-planner"
)

type responseStructureJSON struct {
	InputID               string               `json:"input_id"`
	Trust                  string               `json:"trust"`
	RecordID               int64                `json:"record_id"`
	RecordSpanStart        int                  `json:"record_span_start"`
	RecordSpanEnd          int                  `json:"record_span_end"`
	RecordTextSHA256       string               `json:"record_text_sha256"`
	SignedNoteSpanStart    int                  `json:"signed_note_span_start"`
	SignedNoteSpanEnd      int                  `json:"signed_note_span_end"`
	SignedNoteSHA256       string               `json:"signed_note_sha256"`
	ExpectedGoModLine      string               `json:"expected_go_mod_line"`
	UnverifiedTreeSize     int64                `json:"unverified_tree_size"`
	UnverifiedTreeRootBase64 string             `json:"unverified_tree_root_base64"`
	Signatures             []signatureStructure `json:"unverified_signature_envelope"`
	ParseResult            string               `json:"parse_result"`
}

type sufficiencyJSON struct {
	Status                  string            `json:"status"`
	Conclusion              string            `json:"conclusion"`
	TrustBoundary           string            `json:"trust_boundary"`
	ChecksumIntegrityProven bool              `json:"checksum_integrity_proven"`
	Counts                  sufficiencyCounts `json:"counts"`
	Conditions              []conditionResult `json:"conditions"`
}

type sufficiencyCounts struct {
	Inputs       int `json:"inputs"`
	Responses    int `json:"responses"`
	Heads        int `json:"heads"`
	Operations   int `json:"operations"`
	TileOrigins  int `json:"tile_origins"`
	LiteralPaths int `json:"literal_paths"`
}

type negativeInventoryJSON struct {
	TrustBoundary          string `json:"trust_boundary"`
	VerifierKeys           int    `json:"verifier_keys"`
	SignatureVerifications int    `json:"signature_verifications"`
	MerkleVerifications    int    `json:"merkle_verifications"`
	TileBodiesRead         int    `json:"tile_bodies_read"`
	SaveTilesCalls         int    `json:"save_tiles_calls"`
	NetworkActions         int    `json:"network_actions"`
	Listeners              int    `json:"listeners"`
	ChildProcesses         int    `json:"child_processes"`
	GoCacheReads           int    `json:"go_cache_reads"`
	GoSumWrites            int    `json:"go_sum_writes"`
	GraphCommands          int    `json:"graph_commands"`
	AuthenticationResults  int    `json:"authentication_results"`
}

func writeOutputs(root string, result planResult) error {
	if !result.Complete {
		return fmt.Errorf("refuse to promote outputs for an incomplete plan")
	}
	if err := validateEmptyOutputRoot(root); err != nil {
		return err
	}

	files := make(map[string][]byte, len(outputNames))
	files["planner-inputs.tsv"] = renderInputs(result.Inputs)
	responseJSON, err := renderResponses(result.Responses)
	if err != nil {
		return err
	}
	files["response-structure.jsonl"] = responseJSON
	files["tree-heads.tsv"] = renderHeads(result.Heads)
	files["operation-matrix.tsv"] = renderOperations(result.Operations)
	files["tile-origins.tsv"] = renderOrigins(result.Origins)
	files["literal-tile-manifest.tsv"] = renderLiteralTiles(result.LiteralTiles)
	sufficiency, err := renderSufficiency(result)
	if err != nil {
		return err
	}
	files["structural-sufficiency.json"] = sufficiency
	sourceManifest, err := sourcebundle.ManifestTSV()
	if err != nil {
		return fmt.Errorf("render planner source manifest: %w", err)
	}
	files["planner-source-manifest.tsv"] = sourceManifest
	negative, err := renderNegativeInventory()
	if err != nil {
		return err
	}
	files["negative-inventory.json"] = negative
	files["stop-register.md"] = []byte("# Planner Stop Register\n\nNo stop condition was observed.\n")

	if len(files) != len(outputNames) {
		return fmt.Errorf("internal output count %d differs from required %d", len(files), len(outputNames))
	}
	for _, name := range outputNames {
		body, ok := files[name]
		if !ok {
			return fmt.Errorf("required output %q is absent", name)
		}
		if len(body) == 0 || body[len(body)-1] != '\n' || bytes.Contains(body, []byte{'\r'}) {
			return fmt.Errorf("required output %q is empty or not normalized LF text", name)
		}
	}

	// The deterministic incomplete marker is written first. If any later write
	// fails, the output set cannot be mistaken for a promoted PASS result.
	incompleteStop := []byte("# Planner Stop Register\n\nUNVERIFIED AND INCOMPLETE: output promotion did not finish.\n")
	if err := writeExclusive(filepath.Join(root, "stop-register.md"), incompleteStop); err != nil {
		return fmt.Errorf("create incomplete stop register: %w", err)
	}
	for _, name := range outputNames {
		if name == "stop-register.md" {
			continue
		}
		if err := writeExclusive(filepath.Join(root, name), files[name]); err != nil {
			return fmt.Errorf("create output %q: %w", name, err)
		}
	}
	completeStopPath := filepath.Join(root, ".stop-register.md.complete")
	if err := writeExclusive(completeStopPath, files["stop-register.md"]); err != nil {
		return fmt.Errorf("create complete stop register replacement: %w", err)
	}
	if err := os.Rename(completeStopPath, filepath.Join(root, "stop-register.md")); err != nil {
		return fmt.Errorf("promote complete stop register: %w", err)
	}
	return nil
}

func writeExclusive(path string, body []byte) error {
	file, err := os.OpenFile(path, os.O_WRONLY|os.O_CREATE|os.O_EXCL, 0o600)
	if err != nil {
		return err
	}
	written, writeErr := file.Write(body)
	syncErr := file.Sync()
	closeErr := file.Close()
	if writeErr != nil {
		return writeErr
	}
	if syncErr != nil {
		return syncErr
	}
	if closeErr != nil {
		return closeErr
	}
	if written != len(body) {
		return fmt.Errorf("short write: wrote %d of %d bytes", written, len(body))
	}
	return nil
}

func validateEmptyOutputRoot(root string) error {
	info, err := os.Lstat(root)
	if err != nil {
		return fmt.Errorf("lstat output root: %w", err)
	}
	if info.Mode()&os.ModeSymlink != 0 || !info.IsDir() {
		return fmt.Errorf("output root must be a non-symlink directory")
	}
	entries, err := os.ReadDir(root)
	if err != nil {
		return fmt.Errorf("read output root: %w", err)
	}
	if len(entries) != 0 {
		return fmt.Errorf("output root must be empty, found %d entries", len(entries))
	}
	return nil
}

func renderInputs(inputs []inputRow) []byte {
	var out strings.Builder
	out.WriteString("input_id\tsource_relative_path\tdestination_relative_path\tbytes\tsha256\treconciliation\n")
	for _, input := range inputs {
		fmt.Fprintf(&out, "%s\t%s\t%s\t%d\t%s\tMATCH\n", input.InputID, input.SourceRelativePath, input.DestinationRelativePath, input.Bytes, input.SHA256)
	}
	return []byte(out.String())
}

func renderResponses(responses []parsedResponse) ([]byte, error) {
	var out bytes.Buffer
	encoder := json.NewEncoder(&out)
	encoder.SetEscapeHTML(false)
	for _, response := range responses {
		row := responseStructureJSON{
			InputID:                  response.Input.InputID,
			Trust:                    structuralTrustLabel,
			RecordID:                 response.RecordID,
			RecordSpanStart:           response.RecordSpanStart,
			RecordSpanEnd:             response.RecordSpanEnd,
			RecordTextSHA256:          response.RecordTextSHA256,
			SignedNoteSpanStart:       response.SignedNoteSpanStart,
			SignedNoteSpanEnd:         response.SignedNoteSpanEnd,
			SignedNoteSHA256:          response.SignedNoteSHA256,
			ExpectedGoModLine:         response.ExpectedGoModLine,
			UnverifiedTreeSize:        response.Tree.N,
			UnverifiedTreeRootBase64: response.TreeRootBase64,
			Signatures:                response.Signatures,
			ParseResult:               "STRUCTURALLY_PARSED_NOT_AUTHENTICATED",
		}
		if err := encoder.Encode(row); err != nil {
			return nil, fmt.Errorf("encode response structure: %w", err)
		}
	}
	return out.Bytes(), nil
}

func renderHeads(heads []head) []byte {
	var out strings.Builder
	out.WriteString("head_id\tunverified_tree_size\tunverified_root_base64\tsource_input_ids\tsigned_note_hashes\tvariant_flag\ttrust\n")
	for _, item := range heads {
		fmt.Fprintf(&out, "%s\t%d\t%s\t%s\t%s\t%s\t%s\n", item.ID, item.Tree.N, item.RootBase64, strings.Join(item.SourceInputIDs, ","), strings.Join(item.SignedNoteHashes, ","), item.VariantFlag, structuralTrustLabel)
	}
	return []byte(out.String())
}

func renderOperations(operations []operation) []byte {
	var out strings.Builder
	out.WriteString("operation_id\tkind\trationale\trecord_input_id\trecord_id\tolder_head_id\tnewer_head_id\tevaluation_head_id\texpected_result\n")
	for _, item := range operations {
		recordID := ""
		if item.Kind == "RECORD_CHECK" {
			recordID = strconv.FormatInt(item.RecordID, 10)
		}
		fmt.Fprintf(&out, "%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\n", item.ID, item.Kind, item.Rationale, item.RecordInputID, recordID, item.OlderHeadID, item.NewerHeadID, item.EvaluationHeadID, item.ExpectedResult)
	}
	return []byte(out.String())
}

func renderOrigins(origins []tileOrigin) []byte {
	var out strings.Builder
	out.WriteString("operation_id\tpath\trole\ttile_height\ttile_level\ttile_number\ttile_width\texpected_bytes\tprimary_path\n")
	for _, item := range origins {
		fmt.Fprintf(&out, "%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%s\n", item.OperationID, item.Path, item.Role, item.Tile.H, item.Tile.L, item.Tile.N, item.Tile.W, item.Tile.W*32, item.PrimaryPath)
	}
	return []byte(out.String())
}

func renderLiteralTiles(items []literalTile) []byte {
	var out strings.Builder
	out.WriteString("manifest_id\tpath\trole\ttile_height\ttile_level\ttile_number\ttile_width\texpected_bytes\tprimary_path\torigin_count\torigin_ids_sha256\n")
	for _, item := range items {
		fmt.Fprintf(&out, "%s\t%s\t%s\t%d\t%d\t%d\t%d\t%d\t%s\t%d\t%s\n", item.ManifestID, item.Path, item.Role, item.TileHeight, item.TileLevel, item.TileNumber, item.TileWidth, item.ExpectedBytes, item.PrimaryPath, item.OriginCount, item.OriginIDsSHA256)
	}
	return []byte(out.String())
}

func renderSufficiency(result planResult) ([]byte, error) {
	document := sufficiencyJSON{
		Status:                  "PASS",
		Conclusion:              structuralPassConclusion,
		TrustBoundary:           structuralTrustLabel,
		ChecksumIntegrityProven: false,
		Counts: sufficiencyCounts{
			Inputs:       len(result.Inputs),
			Responses:    len(result.Responses),
			Heads:        len(result.Heads),
			Operations:   len(result.Operations),
			TileOrigins:  len(result.Origins),
			LiteralPaths: len(result.LiteralTiles),
		},
		Conditions: result.Conditions,
	}
	return marshalNormalizedJSON(document)
}

func renderNegativeInventory() ([]byte, error) {
	return marshalNormalizedJSON(negativeInventoryJSON{TrustBoundary: structuralTrustLabel})
}

func marshalNormalizedJSON(value any) ([]byte, error) {
	body, err := json.MarshalIndent(value, "", "  ")
	if err != nil {
		return nil, fmt.Errorf("encode normalized JSON: %w", err)
	}
	return append(body, '\n'), nil
}
