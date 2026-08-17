package raftsim

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
  <title>Lab 003 — Raft Simulation</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #0d6efd; font-size: 1.5rem; }
    .ok { display: inline-block; background: #e7f1ff; color: #084298; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #0d6efd; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 003 — Raft Consensus Simulation</h1>
  <p><span class="ok">running</span> 5-node in-memory cluster — leader election and log replication</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/cluster/elect-leader</code> — elect leader for new term</li>
    <li><code>GET /v1/peers</code> — inspect peer states and commit indices</li>
    <li><code>POST /v1/log/append</code> — replicate command through leader</li>
    <li>Elect again — verify committed entries survive leader change</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_raft.sh</pre>
</body>
</html>`

type appendRequest struct {
	Command string `json:"command"`
}

// NewHandler returns the HTTP handler for the Raft simulation API.
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
			"service": "Lab 003 — Raft Simulation",
			"status":  "running",
			"endpoints": map[string]string{
				"docs":         "GET /docs",
				"openapi":      "GET /openapi.json",
				"health":       "GET /health",
				"elect_leader": "POST /v1/cluster/elect-leader",
				"append":       "POST /v1/log/append",
				"peers":        "GET /v1/peers",
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

	mux.HandleFunc("/v1/cluster/elect-leader", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		leaderID, term, err := store.ElectLeader()
		if err != nil {
			writeError(w, http.StatusInternalServerError, err.Error())
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"leader_id": leaderID,
			"term":      term,
			"peers":     store.Peers(),
		})
	})

	mux.HandleFunc("/v1/log/append", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body appendRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		leaderID, logLen, err := store.AppendLog(body.Command)
		if err != nil {
			writeJSON(w, http.StatusConflict, map[string]interface{}{
				"error": err.Error(),
			})
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"leader_id": leaderID,
			"log_len":   logLen,
			"peers":     store.Peers(),
		})
	})

	mux.HandleFunc("/v1/peers", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodGet {
			methodNotAllowed(w)
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"peers": store.Peers(),
			"stats": store.Stats(),
		})
	})

	return mux
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
