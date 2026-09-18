package planner

import (
	"bufio"
	"bytes"
	"crypto/sha256"
	"encoding/base64"
	"encoding/hex"
	"fmt"
	"io"
	"os"
	"path/filepath"
	"strconv"
	"strings"
	"unicode/utf8"

	"example.invalid/mneme-r3-g2-tile-planner/internal/tlog"
)

func readInputManifest(path string, maxInputs int) ([]inputRow, error) {
	body, err := readBoundedRegularFile(path, 64*1024)
	if err != nil {
		return nil, fmt.Errorf("input manifest: %w", err)
	}
	if bytes.Contains(body, []byte{'\r'}) || len(body) == 0 || body[len(body)-1] != '\n' {
		return nil, fmt.Errorf("input manifest must use LF endings and end with LF")
	}

	scanner := bufio.NewScanner(bytes.NewReader(body))
	scanner.Buffer(make([]byte, 4096), 64*1024)
	if !scanner.Scan() {
		return nil, fmt.Errorf("input manifest is empty")
	}
	const header = "input_id\tsource_relative_path\tdestination_relative_path\tbytes\tsha256"
	if scanner.Text() != header {
		return nil, fmt.Errorf("input manifest header differs from the accepted schema")
	}

	rows := make([]inputRow, 0, requiredMaxInputs)
	for scanner.Scan() {
		if len(rows) >= maxInputs {
			return nil, fmt.Errorf("input count exceeds cap %d", maxInputs)
		}
		fields := strings.Split(scanner.Text(), "\t")
		if len(fields) != 5 {
			return nil, fmt.Errorf("manifest row %d has %d fields, want 5", len(rows)+2, len(fields))
		}
		expectedID := fmt.Sprintf("L%02d", len(rows)+1)
		if fields[0] != expectedID {
			return nil, fmt.Errorf("manifest row %d has input ID %q, want %q", len(rows)+2, fields[0], expectedID)
		}
		expectedDestination := "lookups/" + expectedID + ".lookup"
		if fields[2] != expectedDestination {
			return nil, fmt.Errorf("manifest row %d has destination %q, want %q", len(rows)+2, fields[2], expectedDestination)
		}
		if !validRelativePath(fields[1]) {
			return nil, fmt.Errorf("manifest row %d has invalid source-relative path", len(rows)+2)
		}
		module, version, splitErr := moduleVersionFromLookupPath(fields[1])
		if splitErr != nil {
			return nil, fmt.Errorf("manifest row %d: %w", len(rows)+2, splitErr)
		}
		byteCount, parseErr := strconv.ParseInt(fields[3], 10, 64)
		if parseErr != nil || strconv.FormatInt(byteCount, 10) != fields[3] || byteCount < 1 || byteCount > maxLookupBytes {
			return nil, fmt.Errorf("manifest row %d has invalid canonical byte count", len(rows)+2)
		}
		if !validSHA256(fields[4]) {
			return nil, fmt.Errorf("manifest row %d has invalid lowercase SHA-256", len(rows)+2)
		}
		rows = append(rows, inputRow{
			InputID:                 fields[0],
			SourceRelativePath:      fields[1],
			DestinationRelativePath: fields[2],
			Bytes:                   byteCount,
			SHA256:                  fields[4],
			Module:                  module,
			Version:                 version,
		})
	}
	if err := scanner.Err(); err != nil {
		return nil, fmt.Errorf("scan input manifest: %w", err)
	}
	if len(rows) != requiredMaxInputs {
		return nil, fmt.Errorf("input manifest has %d rows, want exactly %d", len(rows), requiredMaxInputs)
	}
	return rows, nil
}

func readDeclaredInputs(root string, rows []inputRow) ([]parsedResponse, error) {
	rootInfo, err := os.Lstat(root)
	if err != nil {
		return nil, fmt.Errorf("lstat input root: %w", err)
	}
	if rootInfo.Mode()&os.ModeSymlink != 0 || !rootInfo.IsDir() {
		return nil, fmt.Errorf("input root must be a non-symlink directory")
	}
	realRoot, err := filepath.EvalSymlinks(root)
	if err != nil {
		return nil, fmt.Errorf("evaluate input root: %w", err)
	}
	realRoot, err = filepath.Abs(realRoot)
	if err != nil {
		return nil, fmt.Errorf("absolute input root: %w", err)
	}

	entries, err := os.ReadDir(realRoot)
	if err != nil {
		return nil, fmt.Errorf("read input root: %w", err)
	}
	if len(entries) != len(rows) {
		return nil, fmt.Errorf("input root has %d entries, want exactly %d", len(entries), len(rows))
	}
	expectedNames := make(map[string]struct{}, len(rows))
	for _, row := range rows {
		expectedNames[row.InputID+".lookup"] = struct{}{}
	}
	for _, entry := range entries {
		if _, ok := expectedNames[entry.Name()]; !ok {
			return nil, fmt.Errorf("undeclared input-root entry %q", entry.Name())
		}
		if entry.Type()&os.ModeSymlink != 0 || !entry.Type().IsRegular() {
			return nil, fmt.Errorf("input-root entry %q is not a regular non-symlink file", entry.Name())
		}
	}

	responses := make([]parsedResponse, 0, len(rows))
	for _, row := range rows {
		name := row.InputID + ".lookup"
		path := filepath.Join(realRoot, name)
		if filepath.Dir(path) != realRoot {
			return nil, fmt.Errorf("input %s escapes input root", row.InputID)
		}
		body, readErr := readBoundedRegularFile(path, maxLookupBytes)
		if readErr != nil {
			return nil, fmt.Errorf("input %s: %w", row.InputID, readErr)
		}
		if int64(len(body)) != row.Bytes {
			return nil, fmt.Errorf("input %s byte count %d differs from manifest %d", row.InputID, len(body), row.Bytes)
		}
		digest := sha256.Sum256(body)
		if hex.EncodeToString(digest[:]) != row.SHA256 {
			return nil, fmt.Errorf("input %s SHA-256 differs from manifest", row.InputID)
		}
		response, parseErr := parseResponse(row, body)
		if parseErr != nil {
			return nil, fmt.Errorf("input %s: %w", row.InputID, parseErr)
		}
		responses = append(responses, response)
	}
	return responses, nil
}

func parseResponse(row inputRow, body []byte) (parsedResponse, error) {
	if !utf8.Valid(body) {
		return parsedResponse{}, fmt.Errorf("response is not valid UTF-8")
	}
	recordID, recordText, signedNote, err := tlog.ParseRecord(body)
	if err != nil {
		return parsedResponse{}, fmt.Errorf("parse record structure: %w", err)
	}
	if recordID < 0 {
		return parsedResponse{}, fmt.Errorf("record ID is negative")
	}
	canonicalPrefix := strconv.FormatInt(recordID, 10) + "\n"
	if !bytes.HasPrefix(body, []byte(canonicalPrefix)) {
		return parsedResponse{}, fmt.Errorf("record ID is not canonical base 10")
	}
	if len(recordText) == 0 || recordText[len(recordText)-1] != '\n' || bytes.Contains(recordText, []byte("\n\n")) {
		return parsedResponse{}, fmt.Errorf("record text is empty, unterminated, or contains a blank line")
	}
	if len(signedNote) == 0 || !bytes.HasSuffix(signedNote, []byte("\n")) {
		return parsedResponse{}, fmt.Errorf("signed-note envelope is empty or not LF-terminated")
	}

	expectedLine := row.Module + " " + row.Version + "/go.mod h1:"
	matchedLine := ""
	for _, line := range strings.Split(strings.TrimSuffix(string(recordText), "\n"), "\n") {
		if strings.HasPrefix(line, expectedLine) {
			if matchedLine != "" {
				return parsedResponse{}, fmt.Errorf("multiple expected /go.mod lines")
			}
			encodedHash := strings.TrimPrefix(line, expectedLine)
			if encodedHash == "" || strings.ContainsAny(encodedHash, " \t") {
				return parsedResponse{}, fmt.Errorf("expected /go.mod line has malformed h1 value")
			}
			decodedHash, decodeErr := base64.StdEncoding.DecodeString(encodedHash)
			if decodeErr != nil || len(decodedHash) != sha256.Size || base64.StdEncoding.EncodeToString(decodedHash) != encodedHash {
				return parsedResponse{}, fmt.Errorf("expected /go.mod line has noncanonical SHA-256 base64")
			}
			matchedLine = line
		}
	}
	if matchedLine == "" {
		return parsedResponse{}, fmt.Errorf("expected /go.mod line is missing")
	}

	noteText, signatures, err := splitSignedNote(signedNote)
	if err != nil {
		return parsedResponse{}, err
	}
	tree, err := tlog.ParseTree(noteText)
	if err != nil {
		return parsedResponse{}, fmt.Errorf("parse unverified tree text: %w", err)
	}
	if tree.N < 1 || recordID >= tree.N {
		return parsedResponse{}, fmt.Errorf("record ID %d is outside own unverified tree size %d", recordID, tree.N)
	}
	recordDigest := sha256.Sum256(recordText)
	noteDigest := sha256.Sum256(signedNote)
	recordEnd := len(body) - len(signedNote)
	return parsedResponse{
		Input:               row,
		RecordID:            recordID,
		RecordSpanStart:     len(canonicalPrefix),
		RecordSpanEnd:       recordEnd,
		RecordTextSHA256:    hex.EncodeToString(recordDigest[:]),
		SignedNoteSpanStart: recordEnd,
		SignedNoteSpanEnd:   len(body),
		SignedNoteSHA256:    hex.EncodeToString(noteDigest[:]),
		ExpectedGoModLine:   matchedLine,
		Tree:                tree,
		TreeRootBase64:      base64.StdEncoding.EncodeToString(tree.Hash[:]),
		Signatures:          signatures,
	}, nil
}

func splitSignedNote(signed []byte) ([]byte, []signatureStructure, error) {
	separator := bytes.Index(signed, []byte("\n\n"))
	if separator < 0 || bytes.Index(signed[separator+2:], []byte("\n\n")) >= 0 {
		return nil, nil, fmt.Errorf("signed note does not contain one unambiguous envelope separator")
	}
	noteText := signed[:separator+1]
	signatureBlock := signed[separator+2:]
	if len(signatureBlock) == 0 || signatureBlock[len(signatureBlock)-1] != '\n' {
		return nil, nil, fmt.Errorf("signature block is empty or unterminated")
	}
	lines := strings.Split(strings.TrimSuffix(string(signatureBlock), "\n"), "\n")
	structures := make([]signatureStructure, 0, len(lines))
	for _, line := range lines {
		if !strings.HasPrefix(line, "— ") {
			return nil, nil, fmt.Errorf("signature line lacks the exact note prefix")
		}
		fields := strings.Split(strings.TrimPrefix(line, "— "), " ")
		if len(fields) != 2 || !validSignatureName(fields[0]) {
			return nil, nil, fmt.Errorf("signature line has malformed signer structure")
		}
		decoded, err := base64.StdEncoding.DecodeString(fields[1])
		if err != nil || len(decoded) != 68 || base64.StdEncoding.EncodeToString(decoded) != fields[1] {
			return nil, nil, fmt.Errorf("signature line has noncanonical or unexpected structural byte length")
		}
		structures = append(structures, signatureStructure{
			Name:          fields[0],
			KeyHashPrefix: hex.EncodeToString(decoded[:4]),
			Encoded:       fields[1],
			DecodedBytes:  len(decoded),
		})
	}
	if len(structures) == 0 {
		return nil, nil, fmt.Errorf("signed note contains no signature structure")
	}
	return noteText, structures, nil
}

func readBoundedRegularFile(path string, limit int64) ([]byte, error) {
	info, err := os.Lstat(path)
	if err != nil {
		return nil, err
	}
	if info.Mode()&os.ModeSymlink != 0 || !info.Mode().IsRegular() {
		return nil, fmt.Errorf("%q is not a regular non-symlink file", path)
	}
	if info.Size() < 1 || info.Size() > limit {
		return nil, fmt.Errorf("%q size %d is outside 1..%d", path, info.Size(), limit)
	}
	file, err := os.Open(path)
	if err != nil {
		return nil, err
	}
	defer file.Close()
	openedInfo, err := file.Stat()
	if err != nil {
		return nil, err
	}
	if !os.SameFile(info, openedInfo) || !openedInfo.Mode().IsRegular() {
		return nil, fmt.Errorf("%q identity changed while opening", path)
	}
	body, err := io.ReadAll(io.LimitReader(file, limit+1))
	if err != nil {
		return nil, err
	}
	if int64(len(body)) != openedInfo.Size() {
		return nil, fmt.Errorf("%q size changed while reading", path)
	}
	return body, nil
}

func moduleVersionFromLookupPath(path string) (string, string, error) {
	const marker = "/lookup/"
	index := strings.Index(path, marker)
	if index < 0 || strings.Index(path[index+len(marker):], marker) >= 0 {
		return "", "", fmt.Errorf("source path has no unique /lookup/ marker")
	}
	identity := path[index+len(marker):]
	at := strings.LastIndex(identity, "@")
	if at <= 0 || at == len(identity)-1 {
		return "", "", fmt.Errorf("lookup identity lacks module@version")
	}
	module, version := identity[:at], identity[at+1:]
	if strings.ContainsAny(module+version, "\t\r\n ") {
		return "", "", fmt.Errorf("module or version contains whitespace")
	}
	return module, version, nil
}

func validRelativePath(path string) bool {
	return path != "" && !filepath.IsAbs(path) && filepath.Clean(path) == path && path != "." && path != ".." && !strings.HasPrefix(path, "../") && !strings.ContainsAny(path, "\t\r\n")
}

func validSHA256(value string) bool {
	if len(value) != sha256.Size*2 || strings.ToLower(value) != value {
		return false
	}
	decoded, err := hex.DecodeString(value)
	return err == nil && len(decoded) == sha256.Size
}

func validSignatureName(value string) bool {
	if value == "" {
		return false
	}
	for _, r := range value {
		if r < 0x21 || r > 0x7e {
			return false
		}
	}
	return true
}
