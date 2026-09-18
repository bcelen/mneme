// Package sourcebundle exposes the exact source bytes compiled into the
// experimental planner so the planner can emit a self-contained source
// manifest without reading the repository at execution time.
package sourcebundle

import (
	"crypto/sha256"
	"embed"
	"encoding/hex"
	"fmt"
	"io/fs"
	"sort"
	"strings"
)

// P2-01 embeds planner-owned source and its review manifest. P2-02 adds only
// the exact copied tlog source, license, and provenance manifest. Later P2
// gates must separately review any expansion of this literal pattern list.
//
//go:embed README.md go.mod sourcebundle.go planner-owned-source-manifest.tsv copied-tlog-manifest.tsv LICENSES/golang.org-x-mod-BSD-3-Clause.txt cmd/mneme-r3-g2-tile-plan/main.go internal/planner/*.go internal/tlog/*.go
var sourceFiles embed.FS

// ManifestTSV returns a deterministic manifest of every embedded source file.
// It performs no filesystem, environment, user-home, process, or network read.
func ManifestTSV() ([]byte, error) {
	paths := make([]string, 0, 16)
	err := fs.WalkDir(sourceFiles, ".", func(path string, entry fs.DirEntry, walkErr error) error {
		if walkErr != nil {
			return walkErr
		}
		if entry.IsDir() {
			return nil
		}
		paths = append(paths, path)
		return nil
	})
	if err != nil {
		return nil, fmt.Errorf("walk embedded source: %w", err)
	}
	sort.Strings(paths)

	var out strings.Builder
	out.WriteString("path\tbytes\tsha256\torigin\tlicense_status\n")
	for _, path := range paths {
		body, readErr := sourceFiles.ReadFile(path)
		if readErr != nil {
			return nil, fmt.Errorf("read embedded source %q: %w", path, readErr)
		}
		digest := sha256.Sum256(body)
		origin, licenseStatus := sourceProvenance(path)
		fmt.Fprintf(
			&out,
			"%s\t%d\t%s\t%s\t%s\n",
			path,
			len(body),
			hex.EncodeToString(digest[:]),
			origin,
			licenseStatus,
		)
	}
	return []byte(out.String()), nil
}

func sourceProvenance(path string) (string, string) {
	switch {
	case strings.HasPrefix(path, "internal/tlog/") && strings.HasSuffix(path, ".go"):
		return "copied-go1.27.1-x-mod@v0.36.1-0.20260813213634-8569e2639ca1", "BSD-3-Clause-x-mod"
	case path == "LICENSES/golang.org-x-mod-BSD-3-Clause.txt":
		return "copied-go1.27.1-x-mod-license", "BSD-3-Clause-x-mod-text"
	case path == "copied-tlog-manifest.tsv":
		return "p2-02-provenance-evidence", "project-internal-no-redistribution-grant"
	default:
		return "planner-owned", "project-internal-no-redistribution-grant"
	}
}
