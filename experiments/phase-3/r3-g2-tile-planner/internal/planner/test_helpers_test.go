package planner

import (
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"encoding/json"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"sort"
	"strconv"
	"strings"
	"testing"

	"example.invalid/mneme-r3-g2-tile-planner/internal/tlog"
)

const syntheticTrustLabel = "SYNTHETIC_NON_AUTHENTICATED_TEST_DATA"

type syntheticCase struct {
	CaseID         string   `json:"case_id"`
	Category       string   `json:"category"`
	Construction   string   `json:"construction"`
	Mutation       string   `json:"mutation"`
	ExpectedResult string   `json:"expected_result"`
	ExpectedStop   string   `json:"expected_stop"`
	Requirements   []string `json:"requirements"`
}

type syntheticCaseDocument struct {
	SchemaVersion int             `json:"schema_version"`
	TrustLabel    string          `json:"trust_label"`
	Cases         []syntheticCase `json:"cases"`
}

type syntheticCorpus struct {
	Base     string
	Manifest string
	Root     string
	Rows     []inputRow
	Bodies   map[string][]byte
}

var requiredSyntheticCaseIDs = []string{
	"ERR-BLANK-RECORD-LINE",
	"ERR-DUPLICATE-ID",
	"ERR-HEAD-CAP",
	"ERR-INPUT-CAP",
	"ERR-MALFORMED-ROOT-BASE64",
	"ERR-MALFORMED-SIGNATURE",
	"ERR-MISSING-INPUT",
	"ERR-MISSING-TERMINATOR",
	"ERR-OPERATION-CAP",
	"ERR-OVERSIZED-INPUT",
	"ERR-PATH-CAP",
	"ERR-PATH-TRAVERSAL",
	"ERR-RECORD-NEGATIVE",
	"ERR-RECORD-NONCANONICAL",
	"ERR-SAVE-TILES",
	"ERR-SYMLINK-INPUT",
	"ERR-TREE-NONCANONICAL",
	"ERR-UNEXPECTED-INPUT",
	"ERR-UTF8",
	"ERR-WRONG-ROOT-LENGTH",
	"SYN-EQUAL-DIFFERENT-ROOT",
	"SYN-EQUAL-SAME-ROOT",
	"SYN-INCOMPLETE-MARKER",
	"SYN-LARGE-TILE-NUMBER",
	"SYN-MULTI-SIZE-HEADS",
	"SYN-NEGATIVE-INVENTORY",
	"SYN-ORDER-PERMUTATIONS",
	"SYN-OUTPUT-DETERMINISM",
	"SYN-PARTIAL-FALLBACK",
	"SYN-POWER-OF-TWO",
	"SYN-SENTINEL-REQUIRED",
	"SYN-SHARED-TILES",
	"SYN-SINGLE-RECORD",
	"SYN-SOURCE-PROVENANCE",
	"SYN-VALID-14",
}

func loadSyntheticCases(t *testing.T) []syntheticCase {
	t.Helper()
	path := filepath.Join("..", "..", "testdata", "synthetic", "cases.json")
	body, err := os.ReadFile(path)
	if err != nil {
		t.Fatalf("read synthetic case inventory: %v", err)
	}
	if len(body) == 0 || len(body) > 64*1024 || body[len(body)-1] != '\n' || bytes.Contains(body, []byte{'\r'}) {
		t.Fatalf("synthetic case inventory is empty, oversized, or not normalized LF text")
	}
	decoder := json.NewDecoder(bytes.NewReader(body))
	decoder.DisallowUnknownFields()
	var document syntheticCaseDocument
	if err := decoder.Decode(&document); err != nil {
		t.Fatalf("decode synthetic case inventory: %v", err)
	}
	if err := decoder.Decode(&struct{}{}); err != io.EOF {
		t.Fatalf("synthetic case inventory has trailing JSON data")
	}
	if document.SchemaVersion != 1 || document.TrustLabel != syntheticTrustLabel {
		t.Fatalf("synthetic case inventory has unexpected schema or trust label")
	}
	if len(document.Cases) != len(requiredSyntheticCaseIDs) {
		t.Fatalf("synthetic case inventory has %d cases, want %d", len(document.Cases), len(requiredSyntheticCaseIDs))
	}
	seen := make(map[string]struct{}, len(document.Cases))
	for index, item := range document.Cases {
		if item.CaseID != requiredSyntheticCaseIDs[index] {
			t.Fatalf("synthetic case %d is %q, want %q", index, item.CaseID, requiredSyntheticCaseIDs[index])
		}
		if _, exists := seen[item.CaseID]; exists {
			t.Fatalf("duplicate synthetic case %q", item.CaseID)
		}
		seen[item.CaseID] = struct{}{}
		if item.Category == "" || item.Construction == "" || item.Mutation == "" || len(item.Requirements) == 0 {
			t.Fatalf("synthetic case %q is incomplete", item.CaseID)
		}
		if item.ExpectedResult != "PASS" && item.ExpectedResult != "STOP" {
			t.Fatalf("synthetic case %q has unexpected result %q", item.CaseID, item.ExpectedResult)
		}
		if item.ExpectedResult == "STOP" && item.ExpectedStop == "" {
			t.Fatalf("synthetic stop case %q lacks a stop expectation", item.CaseID)
		}
	}
	return document.Cases
}

func requireSyntheticCase(t *testing.T, caseID string) syntheticCase {
	t.Helper()
	for _, item := range loadSyntheticCases(t) {
		if item.CaseID == caseID {
			return item
		}
	}
	t.Fatalf("required synthetic case %q is absent", caseID)
	return syntheticCase{}
}

func syntheticHash(label string) tlog.Hash {
	digest := sha256.Sum256([]byte("MNEME_SYNTHETIC_HASH_V1:" + label))
	return tlog.Hash(digest)
}

func syntheticLookupBody(t *testing.T, row inputRow, recordID, treeSize int64, rootLabel string) []byte {
	t.Helper()
	h1 := sha256.Sum256([]byte("MNEME_SYNTHETIC_H1_V1:" + row.Module + "@" + row.Version))
	recordText := []byte(fmt.Sprintf("%s %s/go.mod h1:%s\n", row.Module, row.Version, base64.StdEncoding.EncodeToString(h1[:])))
	record, err := tlog.FormatRecord(recordID, recordText)
	if err != nil {
		t.Fatalf("format synthetic record: %v", err)
	}
	treeText := tlog.FormatTree(tlog.Tree{N: treeSize, Hash: syntheticHash(rootLabel)})
	seed := sha256.Sum256([]byte("MNEME_SYNTHETIC_SIGNATURE_SHAPE_V1:" + row.InputID + ":" + rootLabel))
	signatureShape := make([]byte, 68)
	for index := range signatureShape {
		signatureShape[index] = seed[index%len(seed)] ^ byte(index)
	}
	signedNote := append([]byte{}, treeText...)
	signedNote = append(signedNote, '\n')
	signedNote = append(signedNote, []byte("— synthetic.example.invalid "+base64.StdEncoding.EncodeToString(signatureShape)+"\n")...)
	return append(record, signedNote...)
}

func syntheticRowsAndBodies(t *testing.T) ([]inputRow, map[string][]byte) {
	t.Helper()
	rows := make([]inputRow, 0, requiredMaxInputs)
	bodies := make(map[string][]byte, requiredMaxInputs)
	for index := 1; index <= requiredMaxInputs; index++ {
		inputID := fmt.Sprintf("L%02d", index)
		module := fmt.Sprintf("example.invalid/module-%02d", index)
		version := fmt.Sprintf("v0.0.%d", index)
		row := inputRow{
			InputID:                 inputID,
			SourceRelativePath:      "synthetic/lookup/" + module + "@" + version,
			DestinationRelativePath: "lookups/" + inputID + ".lookup",
			Module:                  module,
			Version:                 version,
		}
		body := syntheticLookupBody(t, row, int64(index-1), 16, "shared-tree-size-16")
		digest := sha256.Sum256(body)
		row.Bytes = int64(len(body))
		row.SHA256 = hex.EncodeToString(digest[:])
		rows = append(rows, row)
		bodies[inputID] = body
	}
	return rows, bodies
}

func renderSyntheticManifest(rows []inputRow) []byte {
	var out strings.Builder
	out.WriteString("input_id\tsource_relative_path\tdestination_relative_path\tbytes\tsha256\n")
	for _, row := range rows {
		fmt.Fprintf(&out, "%s\t%s\t%s\t%d\t%s\n", row.InputID, row.SourceRelativePath, row.DestinationRelativePath, row.Bytes, row.SHA256)
	}
	return []byte(out.String())
}

func writeSyntheticManifest(t *testing.T, base string, rows []inputRow) string {
	t.Helper()
	path := filepath.Join(base, "synthetic-input-manifest.tsv")
	if err := os.WriteFile(path, renderSyntheticManifest(rows), 0o600); err != nil {
		t.Fatalf("write synthetic manifest: %v", err)
	}
	return path
}

func writeSyntheticCorpus(t *testing.T) syntheticCorpus {
	t.Helper()
	rows, bodies := syntheticRowsAndBodies(t)
	base := t.TempDir()
	root := filepath.Join(base, "lookups")
	if err := os.Mkdir(root, 0o700); err != nil {
		t.Fatalf("create synthetic input root: %v", err)
	}
	for _, row := range rows {
		path := filepath.Join(root, row.InputID+".lookup")
		if err := os.WriteFile(path, bodies[row.InputID], 0o600); err != nil {
			t.Fatalf("write synthetic input %s: %v", row.InputID, err)
		}
	}
	return syntheticCorpus{
		Base:     base,
		Manifest: writeSyntheticManifest(t, base, rows),
		Root:     root,
		Rows:     rows,
		Bodies:   bodies,
	}
}

func syntheticParsedResponse(inputID string, recordID, treeSize int64, rootLabel string) parsedResponse {
	root := syntheticHash(rootLabel)
	noteDigest := sha256.Sum256([]byte("MNEME_SYNTHETIC_NOTE_V1:" + inputID + ":" + rootLabel))
	recordDigest := sha256.Sum256([]byte("MNEME_SYNTHETIC_RECORD_V1:" + inputID + ":" + strconv.FormatInt(recordID, 10)))
	return parsedResponse{
		Input: inputRow{
			InputID:                 inputID,
			SourceRelativePath:      "synthetic/lookup/example.invalid/" + strings.ToLower(inputID) + "@v0.0.1",
			DestinationRelativePath: "lookups/" + inputID + ".lookup",
			Bytes:                   1,
			SHA256:                  strings.Repeat("0", 64),
			Module:                  "example.invalid/" + strings.ToLower(inputID),
			Version:                 "v0.0.1",
		},
		RecordID:         recordID,
		RecordTextSHA256: hex.EncodeToString(recordDigest[:]),
		SignedNoteSHA256: hex.EncodeToString(noteDigest[:]),
		Tree:             tlog.Tree{N: treeSize, Hash: root},
		TreeRootBase64:   base64.StdEncoding.EncodeToString(root[:]),
		Signatures: []signatureStructure{{
			Name:          "synthetic.example.invalid",
			KeyHashPrefix: "00000000",
			Encoded:       base64.StdEncoding.EncodeToString(make([]byte, 68)),
			DecodedBytes:  68,
		}},
	}
}

func exactSyntheticConfig() config {
	return config{
		mode:            requiredMode,
		tileHeight:      requiredTileHeight,
		maxInputs:       requiredMaxInputs,
		maxHeads:        requiredMaxHeads,
		maxOperations:   requiredMaxOperations,
		maxLiteralPaths: requiredMaxLiteralPaths,
	}
}

func operationKeys(items []operation) []string {
	keys := make([]string, len(items))
	for index, item := range items {
		keys[index] = operationSortKey(item)
	}
	sort.Strings(keys)
	return keys
}

func assertErrorContains(t *testing.T, err error, fragment string) {
	t.Helper()
	if err == nil || !strings.Contains(err.Error(), fragment) {
		t.Fatalf("error = %v, want fragment %q", err, fragment)
	}
}
