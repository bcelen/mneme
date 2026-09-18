package sourcebundle

import (
	"bytes"
	"encoding/hex"
	"strconv"
	"strings"
	"testing"
)

func TestEmbeddedSourceManifestIsDeterministic(t *testing.T) {
	first, err := ManifestTSV()
	if err != nil {
		t.Fatalf("render first embedded source manifest: %v", err)
	}
	second, err := ManifestTSV()
	if err != nil {
		t.Fatalf("render second embedded source manifest: %v", err)
	}
	if !bytes.Equal(first, second) {
		t.Fatalf("embedded source manifest is not byte-deterministic")
	}
	if len(first) == 0 || first[len(first)-1] != '\n' || bytes.Contains(first, []byte{'\r'}) {
		t.Fatalf("embedded source manifest is not normalized LF text")
	}
}

func TestEmbeddedSourceProvenanceClassifications(t *testing.T) {
	body, err := ManifestTSV()
	if err != nil {
		t.Fatalf("render embedded source manifest: %v", err)
	}
	lines := strings.Split(strings.TrimSuffix(string(body), "\n"), "\n")
	if len(lines) < 2 || lines[0] != "path\tbytes\tsha256\torigin\tlicense_status" {
		t.Fatalf("embedded source manifest has an unexpected schema")
	}

	expectedCopied := map[string][2]string{
		"internal/tlog/note.go": {
			"copied-go1.27.1-x-mod@v0.36.1-0.20260813213634-8569e2639ca1",
			"BSD-3-Clause-x-mod",
		},
		"internal/tlog/tile.go": {
			"copied-go1.27.1-x-mod@v0.36.1-0.20260813213634-8569e2639ca1",
			"BSD-3-Clause-x-mod",
		},
		"internal/tlog/tlog.go": {
			"copied-go1.27.1-x-mod@v0.36.1-0.20260813213634-8569e2639ca1",
			"BSD-3-Clause-x-mod",
		},
		"LICENSES/golang.org-x-mod-BSD-3-Clause.txt": {
			"copied-go1.27.1-x-mod-license",
			"BSD-3-Clause-x-mod-text",
		},
		"copied-tlog-manifest.tsv": {
			"p2-02-provenance-evidence",
			"project-internal-no-redistribution-grant",
		},
	}
	seenCopied := make(map[string]bool, len(expectedCopied))
	previousPath := ""
	seenPaths := make(map[string]struct{}, len(lines)-1)
	for index, line := range lines[1:] {
		fields := strings.Split(line, "\t")
		if len(fields) != 5 {
			t.Fatalf("manifest row %d has %d fields, want 5", index+2, len(fields))
		}
		path := fields[0]
		if previousPath != "" && previousPath >= path {
			t.Fatalf("manifest paths are not strictly ordered at %q and %q", previousPath, path)
		}
		previousPath = path
		if _, exists := seenPaths[path]; exists {
			t.Fatalf("duplicate embedded path %q", path)
		}
		seenPaths[path] = struct{}{}
		byteCount, parseErr := strconv.Atoi(fields[1])
		if parseErr != nil || byteCount < 1 {
			t.Fatalf("embedded path %q has invalid byte count %q", path, fields[1])
		}
		digest, decodeErr := hex.DecodeString(fields[2])
		if decodeErr != nil || len(digest) != 32 || strings.ToLower(fields[2]) != fields[2] {
			t.Fatalf("embedded path %q has invalid SHA-256 %q", path, fields[2])
		}
		expectedOrigin, expectedLicense := sourceProvenance(path)
		if fields[3] != expectedOrigin || fields[4] != expectedLicense {
			t.Fatalf("embedded path %q has unexpected provenance %q %q", path, fields[3], fields[4])
		}
		if expected, ok := expectedCopied[path]; ok {
			if fields[3] != expected[0] || fields[4] != expected[1] {
				t.Fatalf("copied path %q differs from accepted P2-02 classification", path)
			}
			seenCopied[path] = true
		} else if fields[3] != "planner-owned" || fields[4] != "project-internal-no-redistribution-grant" {
			t.Fatalf("planner-owned path %q has unexpected classification", path)
		}
	}
	for path := range expectedCopied {
		if !seenCopied[path] {
			t.Fatalf("accepted copied source path %q is absent", path)
		}
	}
}
