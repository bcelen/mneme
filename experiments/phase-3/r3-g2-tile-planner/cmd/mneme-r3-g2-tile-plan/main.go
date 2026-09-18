package main

import (
	"os"

	"example.invalid/mneme-r3-g2-tile-planner/internal/planner"
)

func main() {
	os.Exit(planner.Main(os.Args[1:], os.Stderr))
}
