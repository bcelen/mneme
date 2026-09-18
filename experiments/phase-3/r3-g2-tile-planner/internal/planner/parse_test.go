package planner

import (
	"bytes"
	"encoding/base64"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func TestSyntheticCaseInventory(t *testing.T) {
	cases := loadSyntheticCases(t)
	if len(cases) != 35 {
		t.Fatalf("synthetic case count = %d, want 35", len(cases))
	}
	for index := 1; index < len(cases); index++ {
		if cases[index-1].CaseID >= cases[index].CaseID {
			t.Fatalf("case inventory is not strictly ordered at %q and %q", cases[index-1].CaseID, cases[index].CaseID)
		}
	}
}

func TestParseValidSyntheticResponses(t *testing.T) {
	requireSyntheticCase(t, "SYN-VALID-14")
	corpus := writeSyntheticCorpus(t)
	rows, err := readInputManifest(corpus.Manifest, requiredMaxInputs)
	if err != nil {
		t.Fatalf("read synthetic manifest: %v", err)
	}
	responses, err := readDeclaredInputs(corpus.Root, rows)
	if err != nil {
		t.Fatalf("read synthetic responses: %v", err)
	}
	if len(responses) != requiredMaxInputs {
		t.Fatalf("parsed response count = %d, want %d", len(responses), requiredMaxInputs)
	}
	for index, response := range responses {
		if response.Input.InputID != requiredSyntheticInputID(index) {
			t.Fatalf("response %d input ID = %q", index, response.Input.InputID)
		}
		if !strings.HasPrefix(response.Input.Module, "example.invalid/") {
			t.Fatalf("response %s has non-synthetic module %q", response.Input.InputID, response.Input.Module)
		}
		if response.Tree.N != 16 || len(response.Signatures) != 1 || response.Signatures[0].DecodedBytes != 68 {
			t.Fatalf("response %s has unexpected structural result", response.Input.InputID)
		}
	}
}

func TestParseResponseRejectsHostileSyntheticStructure(t *testing.T) {
	rows, bodies := syntheticRowsAndBodies(t)
	row := rows[0]
	valid := bodies[row.InputID]
	root := syntheticHash("shared-tree-size-16")
	rootBase64 := base64.StdEncoding.EncodeToString(root[:])
	shortRootBase64 := base64.StdEncoding.EncodeToString(make([]byte, 31))

	tests := []struct {
		caseID   string
		mutate   func([]byte) []byte
		fragment string
	}{
		{
			caseID: "ERR-RECORD-NEGATIVE",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte("0\n"), []byte("-1\n"), 1)
			},
			fragment: "record ID is negative",
		},
		{
			caseID: "ERR-RECORD-NONCANONICAL",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte("0\n"), []byte("00\n"), 1)
			},
			fragment: "record ID is not canonical",
		},
		{
			caseID: "ERR-TREE-NONCANONICAL",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte("go.sum database tree\n16\n"), []byte("go.sum database tree\n016\n"), 1)
			},
			fragment: "parse unverified tree text",
		},
		{
			caseID: "ERR-UTF8",
			mutate: func(body []byte) []byte {
				return append([]byte{0xff}, body...)
			},
			fragment: "not valid UTF-8",
		},
		{
			caseID: "ERR-BLANK-RECORD-LINE",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte("\n\ngo.sum database tree"), []byte("\n\nsynthetic-extra-line\n\ngo.sum database tree"), 1)
			},
			fragment: "unambiguous envelope separator",
		},
		{
			caseID: "ERR-MISSING-TERMINATOR",
			mutate: func(body []byte) []byte {
				return append([]byte{}, body[:len(body)-1]...)
			},
			fragment: "not LF-terminated",
		},
		{
			caseID: "ERR-MALFORMED-ROOT-BASE64",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte(rootBase64+"\n"), []byte("not-base64***\n"), 1)
			},
			fragment: "parse unverified tree text",
		},
		{
			caseID: "ERR-WRONG-ROOT-LENGTH",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte(rootBase64+"\n"), []byte(shortRootBase64+"\n"), 1)
			},
			fragment: "parse unverified tree text",
		},
		{
			caseID: "ERR-MALFORMED-SIGNATURE",
			mutate: func(body []byte) []byte {
				return bytes.Replace(body, []byte("— synthetic.example.invalid "), []byte("-- synthetic.example.invalid "), 1)
			},
			fragment: "exact note prefix",
		},
	}

	for _, test := range tests {
		t.Run(test.caseID, func(t *testing.T) {
			requireSyntheticCase(t, test.caseID)
			_, err := parseResponse(row, test.mutate(append([]byte{}, valid...)))
			assertErrorContains(t, err, test.fragment)
		})
	}
}

func TestInputManifestAndFilesystemBoundaries(t *testing.T) {
	t.Run("ERR-DUPLICATE-ID", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-DUPLICATE-ID")
		rows, _ := syntheticRowsAndBodies(t)
		rows[1].InputID = "L01"
		manifest := writeSyntheticManifest(t, t.TempDir(), rows)
		_, err := readInputManifest(manifest, requiredMaxInputs)
		assertErrorContains(t, err, "want \"L02\"")
	})

	t.Run("ERR-INPUT-CAP", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-INPUT-CAP")
		corpus := writeSyntheticCorpus(t)
		_, err := readInputManifest(corpus.Manifest, requiredMaxInputs-1)
		assertErrorContains(t, err, "input count exceeds cap")
	})

	t.Run("ERR-MISSING-INPUT", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-MISSING-INPUT")
		corpus := writeSyntheticCorpus(t)
		if err := os.Remove(filepath.Join(corpus.Root, "L14.lookup")); err != nil {
			t.Fatalf("remove synthetic input: %v", err)
		}
		_, err := readDeclaredInputs(corpus.Root, corpus.Rows)
		assertErrorContains(t, err, "want exactly 14")
	})

	t.Run("ERR-UNEXPECTED-INPUT", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-UNEXPECTED-INPUT")
		corpus := writeSyntheticCorpus(t)
		if err := os.WriteFile(filepath.Join(corpus.Root, "L15.lookup"), []byte("SYNTHETIC\n"), 0o600); err != nil {
			t.Fatalf("write undeclared synthetic input: %v", err)
		}
		_, err := readDeclaredInputs(corpus.Root, corpus.Rows)
		assertErrorContains(t, err, "want exactly 14")
	})

	t.Run("ERR-OVERSIZED-INPUT", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-OVERSIZED-INPUT")
		corpus := writeSyntheticCorpus(t)
		if err := os.WriteFile(filepath.Join(corpus.Root, "L01.lookup"), bytes.Repeat([]byte{'S'}, maxLookupBytes+1), 0o600); err != nil {
			t.Fatalf("write oversized synthetic input: %v", err)
		}
		_, err := readDeclaredInputs(corpus.Root, corpus.Rows)
		assertErrorContains(t, err, "outside 1..1024")
	})

	t.Run("ERR-SYMLINK-INPUT", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-SYMLINK-INPUT")
		corpus := writeSyntheticCorpus(t)
		path := filepath.Join(corpus.Root, "L01.lookup")
		if err := os.Remove(path); err != nil {
			t.Fatalf("remove synthetic input before symlink case: %v", err)
		}
		if err := os.Symlink("L02.lookup", path); err != nil {
			t.Fatalf("create temporary synthetic symlink: %v", err)
		}
		_, err := readDeclaredInputs(corpus.Root, corpus.Rows)
		assertErrorContains(t, err, "not a regular non-symlink file")
	})

	t.Run("ERR-PATH-TRAVERSAL", func(t *testing.T) {
		requireSyntheticCase(t, "ERR-PATH-TRAVERSAL")
		invalid := []string{"/absolute", "../escape", "a/../b", ".", "..", "tab\tname", "line\nname"}
		for _, path := range invalid {
			if validRelativePath(path) {
				t.Fatalf("hostile path %q was accepted", path)
			}
		}
	})
}

func requiredSyntheticInputID(index int) string {
	return "L" + []string{"01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"}[index]
}
