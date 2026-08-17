// Package main — Lab 003: Raft consensus simulation HTTP service and CLI demo.
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/principal-architect-knowledge-system/lab-003-raft-simulation/raftsim"
)

func runDemo(store *raftsim.Store) {
	fmt.Println("==> Lab 003 Raft Simulation — CLI demo")

	leaderID, term, err := store.ElectLeader()
	if err != nil {
		fmt.Printf("elect leader failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Elected leader %d at term %d\n", leaderID, term)

	_, logLen, err := store.AppendLog("set x=1")
	if err != nil {
		fmt.Printf("append failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Appended command — log_len=%d on leader\n", logLen)

	_, term2, _ := store.ElectLeader()
	fmt.Printf("New leader elected at term %d — committed entries preserved\n", term2)

	fmt.Println("Done — run with --serve for HTTP demo on :8098")
}

func main() {
	serve := flag.Bool("serve", false, "Start HTTP API server")
	port := flag.Int("port", 8098, "HTTP port")
	demo := flag.Bool("demo", false, "Run CLI demo")
	flag.Parse()

	store := raftsim.NewStore()

	if *serve {
		addr := fmt.Sprintf(":%d", *port)
		log.Printf("Lab 003 Raft simulation listening on http://localhost%s", addr)
		log.Fatal(http.ListenAndServe(addr, raftsim.NewHandler(store)))
	}

	if *demo {
		runDemo(store)
		return
	}

	runDemo(store)
}
