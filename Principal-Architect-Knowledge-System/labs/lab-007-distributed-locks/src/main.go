// Package main — Lab 007: Distributed locks and fencing tokens HTTP service.
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"
	"time"

	"github.com/principal-architect-knowledge-system/lab-007-distributed-locks/locks"
)

func runDemo(store *locks.Store) {
	fmt.Println("==> Lab 007 Distributed Locks — CLI demo")

	h, err := store.AcquireLock("blob-1", 5000)
	if err != nil {
		fmt.Printf("acquire failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Acquired lock on %s token=%s\n", h.ResourceID, h.Token)

	fence, err := store.IssueFence("blob-1")
	if err != nil {
		fmt.Printf("fence failed: %v\n", err)
		os.Exit(1)
	}
	if err := store.WriteResource("blob-1", fence, []byte("ok")); err != nil {
		fmt.Printf("write failed: %v\n", err)
		os.Exit(1)
	}
	fmt.Printf("Write accepted with fence=%d\n", fence)

	_ = store.ReleaseLock(h.ResourceID, h.Token)
	_, _ = store.AcquireLock("blob-1", 5000)
	if err := store.WriteResource("blob-1", fence, []byte("stale")); err != nil {
		fmt.Printf("Stale fence rejected: %v\n", err)
	}

	fmt.Println("Done — run with --serve for HTTP demo on :8100")
}

func main() {
	serve := flag.Bool("serve", false, "Start HTTP API server")
	port := flag.Int("port", 8100, "HTTP port")
	demo := flag.Bool("demo", false, "Run CLI demo")
	chaos := flag.String("chaos", "", "Chaos: stale-holder")
	pauseMs := flag.Int("pause-ms", 0, "Pause for stale-holder chaos")
	flag.Parse()

	store := locks.NewStore()

	if *chaos == "stale-holder" {
		h, _ := store.AcquireLock("blob", 1)
		fence, _ := store.IssueFence("blob")
		_ = store.WriteResource("blob", fence, []byte("ok"))
		if *pauseMs > 0 {
			time.Sleep(time.Duration(*pauseMs) * time.Millisecond)
		} else {
			time.Sleep(5 * time.Millisecond)
		}
		_, _ = store.AcquireLock("blob", 5000)
		if err := store.WriteResource("blob", fence, []byte("stale")); err != nil {
			fmt.Printf("stale-holder chaos: stale write rejected: %v\n", err)
		}
		_ = h
		return
	}

	if *serve {
		addr := fmt.Sprintf(":%d", *port)
		log.Printf("Lab 007 distributed locks listening on http://localhost%s", addr)
		log.Fatal(http.ListenAndServe(addr, locks.NewHandler(store)))
	}

	if *demo {
		runDemo(store)
		return
	}

	runDemo(store)
}
