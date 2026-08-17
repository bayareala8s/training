// Package main — Lab 004: Replicated KV store HTTP service.
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"

	"github.com/principal-architect-knowledge-system/lab-004-replicated-kv-store/kvstore"
)

func runDemo(store *kvstore.Store) {
	fmt.Println("==> Lab 004 Replicated KV — CLI demo")
	v, shard, err := store.Put("user:42", "alice")
	if err != nil {
		fmt.Println("put failed:", err)
		return
	}
	fmt.Printf("PUT user:42 → shard=%d version=%d\n", shard, v.Version)
	got, shard, ok, _ := store.Get("user:42", true)
	if ok {
		fmt.Printf("GET user:42 → %s (shard=%d v=%d)\n", got.Value, shard, got.Version)
	}
	fmt.Println("Done — run with --serve for HTTP demo on :8095")
}

func main() {
	serve := flag.Bool("serve", false, "Start HTTP API server")
	port := flag.Int("port", 8095, "HTTP port")
	demo := flag.Bool("demo", false, "Run CLI demo")
	chaos := flag.String("chaos", "", "Chaos: replica-down")
	flag.Parse()

	store := kvstore.NewStore(3, 3, 2, 2)

	if *chaos != "" {
		fmt.Printf("chaos %q — use POST /v1/chaos/replica-down via HTTP\n", *chaos)
		return
	}

	if *serve {
		addr := fmt.Sprintf(":%d", *port)
		log.Printf("Lab 004 KV gateway listening on http://localhost%s", addr)
		log.Fatal(http.ListenAndServe(addr, kvstore.NewHandler(store)))
	}

	if *demo {
		runDemo(store)
		return
	}

	runDemo(store)
}
