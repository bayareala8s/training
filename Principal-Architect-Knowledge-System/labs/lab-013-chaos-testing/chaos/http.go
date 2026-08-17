package chaos

import (
	"encoding/json"
	"net/http"
	"strings"
)

const landingHTML = `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 013 — Chaos Testing</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #dc3545; font-size: 1.5rem; }
    .ok { display: inline-block; background: #f8d7da; color: #842029; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #dc3545; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 013 — Chaos Engineering</h1>
  <p><span class="ok">running</span> Fault injection and experiment runner with SLO abort gates</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/faults/enable</code> — inject latency or errors</li>
    <li><code>POST /v1/experiments/run</code> — run experiment with hypothesis</li>
    <li><code>POST /v1/faults/disable</code> — clear faults</li>
    <li>Run SLO-breach experiment — observe fail result</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_chaos.sh</pre>
</body>
</html>`

// NewHandler returns the HTTP handler for the chaos API.
func NewHandler(store *Store) http.Handler {
	mux := http.NewServeMux()
	registerSwaggerRoutes(mux)

	mux.HandleFunc("/", func(w http.ResponseWriter, r *http.Request) {
		if r.URL.Path != "/" {
			http.NotFound(w, r)
			return
		}
		if strings.Contains(r.Header.Get("Accept"), "text/html") {
			w.Header().Set("Content-Type", "text/html; charset=utf-8")
			_, _ = w.Write([]byte(landingHTML))
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"service": "Lab 013 — Chaos Testing",
			"status":  "running",
			"endpoints": map[string]string{
				"docs":       "GET /docs",
				"openapi":    "GET /openapi.json",
				"health":     "GET /health",
				"run_exp":    "POST /v1/experiments/run",
				"enable":     "POST /v1/faults/enable",
				"disable":    "POST /v1/faults/disable",
			},
		})
	})

	mux.HandleFunc("/health", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			methodNotAllowed(w)
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"status": "ok",
			"stats":  store.Stats(),
		})
	})

	mux.HandleFunc("/v1/experiments/run", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body RunExperimentRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		report, err := store.RunExperiment(body)
		status := http.StatusOK
		if !report.Passed {
			status = http.StatusConflict
		}
		writeJSON(w, status, map[string]interface{}{
			"report": report,
			"error":  errString(err),
		})
	})

	mux.HandleFunc("/v1/faults/enable", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body EnableFaultRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		cfg := store.EnableFault(body)
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"enabled": true,
			"fault":   cfg,
		})
	})

	mux.HandleFunc("/v1/faults/disable", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		store.DisableFault()
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"enabled": false,
			"message": "faults disabled",
		})
	})

	return mux
}

func errString(err error) string {
	if err == nil {
		return ""
	}
	return err.Error()
}

func writeJSON(w http.ResponseWriter, status int, v interface{}) {
	w.Header().Set("Content-Type", "application/json")
	w.WriteHeader(status)
	_ = json.NewEncoder(w).Encode(v)
}

func writeError(w http.ResponseWriter, status int, msg string) {
	writeJSON(w, status, map[string]string{"error": msg})
}

func methodNotAllowed(w http.ResponseWriter) {
	writeError(w, http.StatusMethodNotAllowed, "method not allowed")
}
