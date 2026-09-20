package planner

import "example.invalid/mneme-r3-g2-tile-planner/internal/tlog"

const (
	requiredMode             = "plan"
	requiredTileHeight       = 8
	requiredMaxInputs        = 14
	requiredMaxHeads         = 14
	requiredMaxOperations    = 400
	requiredMaxLiteralPaths  = 4096
	maxLookupBytes           = 1024
	maxTreeSize              = int64(1<<62 - 1)
	planSentinelText         = "MNEME_PLAN_ONLY_TILE_CAPTURE"
	structuralTrustLabel     = "UNVERIFIED_STRUCTURAL_INPUT"
	structuralPassConclusion = "Structurally sufficient for literal tile planning"
)

var outputNames = []string{
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

type config struct {
	mode            string
	inputManifest   string
	inputRoot       string
	outputRoot      string
	tileHeight      int
	maxInputs       int
	maxHeads        int
	maxOperations   int
	maxLiteralPaths int
}

type inputRow struct {
	InputID                string
	SourceRelativePath     string
	DestinationRelativePath string
	Bytes                  int64
	SHA256                 string
	Module                 string
	Version                string
}

type parsedResponse struct {
	Input              inputRow
	RecordID           int64
	RecordSpanStart    int
	RecordSpanEnd      int
	RecordTextSHA256   string
	SignedNoteSpanStart int
	SignedNoteSpanEnd  int
	SignedNoteSHA256   string
	ExpectedGoModLine  string
	Tree               tlog.Tree
	TreeRootBase64     string
	Signatures         []signatureStructure
	HeadID             string
}

type signatureStructure struct {
	Name          string `json:"name"`
	KeyHashPrefix string `json:"key_hash_prefix"`
	Encoded       string `json:"encoded"`
	DecodedBytes  int    `json:"decoded_bytes"`
}

type head struct {
	ID               string
	Tree             tlog.Tree
	RootBase64       string
	SourceInputIDs   []string
	SignedNoteHashes []string
	VariantFlag      string
}

type operation struct {
	ID               string
	Kind             string
	Rationale        string
	RecordInputID    string
	RecordID         int64
	OlderHeadID      string
	NewerHeadID      string
	EvaluationHeadID string
	ExpectedResult   string
}

type tileOrigin struct {
	OperationID string
	Tile        tlog.Tile
	Path        string
	Role        string
	PrimaryPath string
}

type literalTile struct {
	ManifestID     string
	Path           string
	Role           string
	TileHeight     int
	TileLevel      int
	TileNumber     int64
	TileWidth      int
	ExpectedBytes  int
	PrimaryPath    string
	OriginCount    int
	OriginIDsSHA256 string
	OriginIDs      []string
}

type planResult struct {
	Inputs       []inputRow
	Responses    []parsedResponse
	Heads        []head
	Operations   []operation
	Origins      []tileOrigin
	LiteralTiles []literalTile
	Conditions   []conditionResult
	Stops        []string
	Complete     bool
}

type conditionResult struct {
	ID     string `json:"id"`
	Status string `json:"status"`
	Detail string `json:"detail"`
}
