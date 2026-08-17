// Package main — Lab 010: Saga orchestration HTTP service and CLI demo.
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/principal-architect-knowledge-system/lab-010-saga-orchestration/saga"
)

func runDemo(store *saga.Store) {
	fmt.Println("==> Lab 010 Saga Orchestration — CLI demo")

	s, err := store.StartSaga("PROD-100", "demo-happy")
	if err != nil {
		fmt.Printf("unexpected error: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Happy path: %s → %s (%d log entries)\n", s.ID, s.State, len(s.Log))

	store.SetInventoryFail(true)
	s2, err := store.StartSaga("PROD-200", "demo-fail")
	if err == nil {
		fmt.Println("expected inventory failure")
		os.Exit(1)
	}
	fmt.Printf("Compensation: %s → %s (%s)\n", s2.ID, s2.State, s2.Error)

	store.SetInventoryFail(false)
	fmt.Println("Done — run with --serve for HTTP demo on :8093")
}

func main() {
	serve := flag.Bool("serve", false, "Start HTTP API server")
	port := flag.Int("port", 8093, "HTTP port")
	demo := flag.Bool("demo", false, "Run CLI demo")
	chaos := flag.String("chaos", "", "Chaos: fail-inventory")
	flag.Parse()

	store := saga.NewStore()

	if *chaos == "fail-inventory" {
		store.SetInventoryFail(true)
	}

	if *serve {
		addr := fmt.Sprintf(":%d", *port)
		log.Printf("Lab 010 saga orchestrator listening on http://localhost%s", addr)
		log.Fatal(http.ListenAndServe(addr, saga.NewHandler(store)))
	}

	if *demo || *chaos != "" {
		runDemo(store)
		return
	}

	runDemo(store)
}
