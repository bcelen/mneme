package planner

import (
	"bytes"
	"os"
	"path/filepath"
	"strings"
	"testing"
)

func syntheticArguments(corpus syntheticCorpus, outputRoot string) []string {
	return []string{
		"-mode", "plan",
		"-input-manifest", corpus.Manifest,
		"-input-root", corpus.Root,
		"-tile-height", "8",
		"-max-inputs", "14",
		"-max-heads", "14",
		"-max-operations", "400",
		"-max-literal-paths", "4096",
		"-output-root", outputRoot,
	}
}

func replaceArgumentValue(arguments []string, name, value string) []string {
	result := append([]string{}, arguments...)
	for index := 0; index+1 < len(result); index++ {
		if result[index] == name {
			result[index+1] = value
			return result
		}
	}
	return result
}

func TestParseFlagsAcceptsOnlyFrozenCommandSurface(t *testing.T) {
	corpus := writeSyntheticCorpus(t)
	outputRoot := t.TempDir()
	arguments := syntheticArguments(corpus, outputRoot)
	var stderr bytes.Buffer
	cfg, err := parseFlags(arguments, &stderr)
	if err != nil {
		t.Fatalf("parse exact synthetic flags: %v", err)
	}
	if cfg.mode != requiredMode || cfg.inputManifest != corpus.Manifest || cfg.inputRoot != corpus.Root || cfg.outputRoot != outputRoot ||
		cfg.tileHeight != requiredTileHeight || cfg.maxInputs != requiredMaxInputs || cfg.maxHeads != requiredMaxHeads ||
		cfg.maxOperations != requiredMaxOperations || cfg.maxLiteralPaths != requiredMaxLiteralPaths {
		t.Fatalf("parsed configuration differs from the frozen command surface")
	}

	tests := []struct {
		name      string
		flag      string
		value     string
		fragment  string
	}{
		{"mode", "-mode", "inspect", "mode is"},
		{"tile-height", "-tile-height", "7", "safety caps must be exactly"},
		{"max-inputs", "-max-inputs", "13", "safety caps must be exactly"},
		{"max-heads", "-max-heads", "13", "safety caps must be exactly"},
		{"max-operations", "-max-operations", "399", "safety caps must be exactly"},
		{"max-literal-paths", "-max-literal-paths", "4095", "safety caps must be exactly"},
	}
	for _, test := range tests {
		t.Run(test.name, func(t *testing.T) {
			_, err := parseFlags(replaceArgumentValue(arguments, test.flag, test.value), &bytes.Buffer{})
			assertErrorContains(t, err, test.fragment)
		})
	}

	t.Run("positional-argument", func(t *testing.T) {
		_, err := parseFlags(append(append([]string{}, arguments...), "synthetic-positional"), &bytes.Buffer{})
		assertErrorContains(t, err, "positional arguments are forbidden")
	})

	t.Run("missing-required-path", func(t *testing.T) {
		_, err := parseFlags(replaceArgumentValue(arguments, "-input-root", ""), &bytes.Buffer{})
		assertErrorContains(t, err, "are required")
	})

	t.Run("output-equals-input", func(t *testing.T) {
		_, err := parseFlags(replaceArgumentValue(arguments, "-output-root", corpus.Root), &bytes.Buffer{})
		assertErrorContains(t, err, "output root must be distinct")
	})
}

func TestParseFlagsIsIndependentOfSyntheticEnvironment(t *testing.T) {
	corpus := writeSyntheticCorpus(t)
	arguments := syntheticArguments(corpus, t.TempDir())
	first, err := parseFlags(arguments, &bytes.Buffer{})
	if err != nil {
		t.Fatalf("parse flags before synthetic environment change: %v", err)
	}
	t.Setenv("HOME", "/synthetic-forbidden-home")
	t.Setenv("GOPROXY", "https://synthetic.example.invalid/forbidden")
	t.Setenv("GOSUMDB", "synthetic.example.invalid")
	second, err := parseFlags(arguments, &bytes.Buffer{})
	if err != nil {
		t.Fatalf("parse flags after synthetic environment change: %v", err)
	}
	if first != second {
		t.Fatalf("configuration changed with unrelated synthetic environment values")
	}
}

func TestMainExitClassesFailClosed(t *testing.T) {
	t.Run("configuration-stop", func(t *testing.T) {
		var stderr bytes.Buffer
		if code := Main(nil, &stderr); code != 2 {
			t.Fatalf("configuration stop code = %d, want 2", code)
		}
		if !strings.Contains(stderr.String(), "planner configuration stop:") {
			t.Fatalf("configuration stop lacks normalized diagnostic")
		}
	})

	t.Run("input-stop", func(t *testing.T) {
		corpus := writeSyntheticCorpus(t)
		if err := os.Remove(filepath.Join(corpus.Root, "L14.lookup")); err != nil {
			t.Fatalf("remove synthetic input: %v", err)
		}
		var stderr bytes.Buffer
		if code := Main(syntheticArguments(corpus, t.TempDir()), &stderr); code != 1 {
			t.Fatalf("input stop code = %d, want 1", code)
		}
		if !strings.Contains(stderr.String(), "planner input stop:") {
			t.Fatalf("input stop lacks normalized diagnostic")
		}
	})

	t.Run("output-stop", func(t *testing.T) {
		corpus := writeSyntheticCorpus(t)
		outputRoot := t.TempDir()
		if err := os.WriteFile(filepath.Join(outputRoot, "synthetic-blocker"), []byte("SYNTHETIC\n"), 0o600); err != nil {
			t.Fatalf("write synthetic output blocker: %v", err)
		}
		var stderr bytes.Buffer
		if code := Main(syntheticArguments(corpus, outputRoot), &stderr); code != 1 {
			t.Fatalf("output stop code = %d, want 1", code)
		}
		if !strings.Contains(stderr.String(), "planner output stop:") {
			t.Fatalf("output stop lacks normalized diagnostic")
		}
	})
}
