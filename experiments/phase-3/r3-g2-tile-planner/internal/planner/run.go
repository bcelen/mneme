package planner

import (
	"flag"
	"fmt"
	"io"
	"os"
)

// Main parses the frozen command surface and returns a process exit code. It
// does not read environment variables, user configuration, a home directory,
// a key, a cache, a service, or a network resource.
func Main(arguments []string, stderr io.Writer) int {
	cfg, err := parseFlags(arguments, stderr)
	if err != nil {
		fmt.Fprintf(stderr, "planner configuration stop: %v\n", err)
		return 2
	}
	rows, err := readInputManifest(cfg.inputManifest, cfg.maxInputs)
	if err != nil {
		fmt.Fprintf(stderr, "planner input-manifest stop: %v\n", err)
		return 1
	}
	responses, err := readDeclaredInputs(cfg.inputRoot, rows)
	if err != nil {
		fmt.Fprintf(stderr, "planner input stop: %v\n", err)
		return 1
	}
	result, err := buildPlan(responses, cfg)
	if err != nil {
		fmt.Fprintf(stderr, "planner derivation stop: %v\n", err)
		return 1
	}
	if err := writeOutputs(cfg.outputRoot, result); err != nil {
		fmt.Fprintf(stderr, "planner output stop: %v\n", err)
		return 1
	}
	return 0
}

func parseFlags(arguments []string, stderr io.Writer) (config, error) {
	var cfg config
	set := flag.NewFlagSet("mneme-r3-g2-tile-plan", flag.ContinueOnError)
	set.SetOutput(stderr)
	set.StringVar(&cfg.mode, "mode", "", "required literal mode: plan")
	set.StringVar(&cfg.inputManifest, "input-manifest", "", "literal input-manifest path")
	set.StringVar(&cfg.inputRoot, "input-root", "", "literal input root")
	set.IntVar(&cfg.tileHeight, "tile-height", 0, "required tile height: 8")
	set.IntVar(&cfg.maxInputs, "max-inputs", 0, "required input cap: 14")
	set.IntVar(&cfg.maxHeads, "max-heads", 0, "required head cap: 14")
	set.IntVar(&cfg.maxOperations, "max-operations", 0, "required operation cap: 400")
	set.IntVar(&cfg.maxLiteralPaths, "max-literal-paths", 0, "required literal-path cap: 4096")
	set.StringVar(&cfg.outputRoot, "output-root", "", "literal empty output root")
	if err := set.Parse(arguments); err != nil {
		return config{}, err
	}
	if set.NArg() != 0 {
		return config{}, fmt.Errorf("positional arguments are forbidden")
	}
	if cfg.mode != requiredMode {
		return config{}, fmt.Errorf("mode is %q, want %q", cfg.mode, requiredMode)
	}
	if cfg.inputManifest == "" || cfg.inputRoot == "" || cfg.outputRoot == "" {
		return config{}, fmt.Errorf("input-manifest, input-root, and output-root are required")
	}
	if cfg.tileHeight != requiredTileHeight || cfg.maxInputs != requiredMaxInputs || cfg.maxHeads != requiredMaxHeads || cfg.maxOperations != requiredMaxOperations || cfg.maxLiteralPaths != requiredMaxLiteralPaths {
		return config{}, fmt.Errorf("safety caps must be exactly tile-height=%d max-inputs=%d max-heads=%d max-operations=%d max-literal-paths=%d", requiredTileHeight, requiredMaxInputs, requiredMaxHeads, requiredMaxOperations, requiredMaxLiteralPaths)
	}
	if cfg.inputManifest == cfg.outputRoot || cfg.inputRoot == cfg.outputRoot {
		return config{}, fmt.Errorf("output root must be distinct from all input paths")
	}
	if _, err := os.Stat(cfg.inputManifest); err != nil {
		return config{}, fmt.Errorf("stat input manifest: %w", err)
	}
	return cfg, nil
}
