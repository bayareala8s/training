// Package main — Lab 013: Chaos engineering HTTP service and CLI demo.
package main

import (
	"flag"
	"fmt"
	"log"
	"net/http"
	"os"

	"github.com/principal-architect-knowledge-system/lab-013-chaos-testing/chaos"
)

func runDemo(store *chaos.Store) {
	fmt.Println("==> Lab 013 Chaos Testing — CLI demo")

	report, _ := store.RunExperiment(chaos.RunExperimentRequest{
		Name:       "latency-demo",
		FaultType:  "latency",
		LatencyMs:  50,
		Target:     "api-1",
		Hypothesis: "p99 stable under latency",
	})
	fmt.Printf("Latency experiment: passed=%v summary=%s\n", report.Passed, report.Summary)

	report2, _ := store.RunExperiment(chaos.RunExperimentRequest{
		Name:       "slo-breach",
		FaultType:  "error_rate",
		ErrorRate:  1.0,
		Target:     "api-1",
		SLOBreach:  0.10,
		Hypothesis: "errors breach SLO",
	})
	fmt.Printf("SLO breach experiment: passed=%v summary=%s\n", report2.Passed, report2.Summary)

	fmt.Println("Done — run with --serve for HTTP demo on :8103")
}

func main() {
	serve := flag.Bool("serve", false, "Start HTTP API server")
	port := flag.Int("port", 8103, "HTTP port")
	demo := flag.Bool("demo", false, "Run CLI demo")
	experiment := flag.String("experiment", "", "Path to experiment YAML manifest")
	flag.Parse()

	store := chaos.NewStore()

	if *experiment != "" {
		content, err := os.ReadFile(*experiment)
		if err != nil {
			log.Fatal(err)
		}
		exp, err := chaos.ParseManifest(string(content))
		if err != nil {
			log.Fatal(err)
		}
		report, _ := store.RunExperiment(chaos.RunExperimentRequest{
			Name:       exp.Name,
			FaultType:  string(exp.Fault.Type),
			LatencyMs:  exp.Fault.LatencyMs,
			ErrorRate:  exp.Fault.ErrorRate,
			Target:     exp.Fault.Target,
			Hypothesis: exp.Hypothesis,
		})
		fmt.Println(chaos.MarkdownReport(report))
		return
	}

	if *serve {
		addr := fmt.Sprintf(":%d", *port)
		log.Printf("Lab 013 chaos testing listening on http://localhost%s", addr)
		log.Fatal(http.ListenAndServe(addr, chaos.NewHandler(store)))
	}

	if *demo {
		runDemo(store)
		return
	}

	runDemo(store)
}
