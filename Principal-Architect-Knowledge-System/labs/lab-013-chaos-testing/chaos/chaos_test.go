package chaos

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"strings"
	"testing"
	"time"
)

func TestLatencyInjection(t *testing.T) {
	inj := &FaultInjector{}
	inj.Enable(FaultConfig{Type: FaultLatency, LatencyMs: 50, Target: "api-1"})
	delay, err := inj.Apply("api-1")
	if err != nil || delay != 50*time.Millisecond {
		t.Fatalf("expected 50ms latency, got %v err=%v", delay, err)
	}
}

func TestErrorInjection(t *testing.T) {
	inj := &FaultInjector{}
	inj.Enable(FaultConfig{Type: FaultError, ErrorRate: 1.0, Target: "api-1"})
	if _, err := inj.Apply("api-1"); err == nil {
		t.Fatal("expected injected error")
	}
}

func TestAbortOnSLO(t *testing.T) {
	runner := &Runner{}
	report, _ := runner.Run(Experiment{
		Name:       "slo-test",
		Hypothesis: "errors breach SLO",
		Fault:      FaultConfig{Type: FaultError, ErrorRate: 1.0, Target: "api"},
		SLOBreach:  0.10,
	})
	if report.Passed {
		t.Fatal("expected SLO breach to fail experiment")
	}
}

func TestBlastRadius(t *testing.T) {
	inj := &FaultInjector{}
	inj.Enable(FaultConfig{Type: FaultDepDown, Target: "api-1"})
	if _, err := inj.Apply("api-2"); err != nil {
		t.Fatal("untargeted instance should not receive fault")
	}
}

func TestReportGeneration(t *testing.T) {
	md := MarkdownReport(Report{Name: "exp1", Hypothesis: "steady state", Passed: true})
	if !strings.Contains(md, "Chaos Report") {
		t.Fatal("expected markdown report")
	}
}

func TestExperimentManifestParse(t *testing.T) {
	manifest := "name: dep-slow\nhypothesis: p99 stable\ntarget: api-1\ntype: latency\n"
	exp, err := ParseManifest(manifest)
	if err != nil || exp.Name != "dep-slow" || exp.Fault.Target != "api-1" {
		t.Fatal("manifest parse failed")
	}
}

func TestStoreRunExperiment(t *testing.T) {
	store := NewStore()
	report, err := store.RunExperiment(RunExperimentRequest{
		Name:      "latency-demo",
		FaultType: "latency",
		LatencyMs: 50,
		Target:    "api-1",
	})
	if err != nil || !report.Passed {
		t.Fatalf("expected pass, err=%v passed=%v", err, report.Passed)
	}
}

func TestHTTPRunExperiment(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	body := []byte(`{"name":"dep-slow","fault_type":"latency","latency_ms":50,"target":"api-1"}`)
	resp, err := http.Post(srv.URL+"/v1/experiments/run", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func TestHTTPFaultEnableDisable(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	enableBody := []byte(`{"fault_type":"latency","latency_ms":100,"target":"api-1"}`)
	resp, err := http.Post(srv.URL+"/v1/faults/enable", "application/json", bytes.NewReader(enableBody))
	if err != nil {
		t.Fatal(err)
	}
	resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}

	resp2, err := http.Post(srv.URL+"/v1/faults/disable", "application/json", nil)
	if err != nil {
		t.Fatal(err)
	}
	resp2.Body.Close()
	if resp2.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp2.StatusCode)
	}
}

func TestHTTPExperimentSLOBreach(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	body := []byte(`{"name":"slo-breach","fault_type":"error_rate","error_rate":1.0,"target":"api-1","slo_breach":0.10}`)
	resp, err := http.Post(srv.URL+"/v1/experiments/run", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusConflict {
		t.Fatalf("expected 409, got %d", resp.StatusCode)
	}
	var payload map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		t.Fatal(err)
	}
	report := payload["report"].(map[string]interface{})
	if report["passed"] != false {
		t.Fatal("expected experiment to fail")
	}
}

func TestHealthEndpoint(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	resp, err := http.Get(srv.URL + "/health")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func TestSwaggerEndpoints(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	resp, err := http.Get(srv.URL + "/openapi.json")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}

	resp2, err := http.Get(srv.URL + "/docs")
	if err != nil {
		t.Fatal(err)
	}
	defer resp2.Body.Close()
	if resp2.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp2.StatusCode)
	}
}
