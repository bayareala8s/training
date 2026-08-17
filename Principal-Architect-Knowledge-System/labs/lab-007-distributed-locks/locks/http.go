package locks

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
  <title>Lab 007 — Distributed Locks</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #198754; font-size: 1.5rem; }
    .ok { display: inline-block; background: #d1e7dd; color: #0f5132; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #198754; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 007 — Distributed Locks &amp; Fencing</h1>
  <p><span class="ok">running</span> TTL locks with monotonic fencing tokens protecting a shared resource</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/locks/acquire</code> — obtain lock with TTL</li>
    <li><code>POST /v1/fencing/issue</code> — get monotonic fence token</li>
    <li><code>POST /v1/resource/write</code> — write with valid fence</li>
    <li>Release lock, re-acquire, reject stale fence write</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_locks.sh</pre>
</body>
</html>`

type acquireRequest struct {
	ResourceID string `json:"resource_id"`
	TTLMs      int    `json:"ttl_ms"`
}

type releaseRequest struct {
	ResourceID string `json:"resource_id"`
	Token      string `json:"token"`
}

type issueFenceRequest struct {
	ResourceID string `json:"resource_id"`
}

type writeRequest struct {
	ResourceID string `json:"resource_id"`
	FenceID    int64  `json:"fence_id"`
	Data       string `json:"data"`
}

// NewHandler returns the HTTP handler for the locks API.
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
			"service": "Lab 007 — Distributed Locks",
			"status":  "running",
			"endpoints": map[string]string{
				"docs":    "GET /docs",
				"openapi": "GET /openapi.json",
				"health":  "GET /health",
				"acquire": "POST /v1/locks/acquire",
				"release": "POST /v1/locks/release",
				"fence":   "POST /v1/fencing/issue",
				"write":   "POST /v1/resource/write",
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

	mux.HandleFunc("/v1/locks/acquire", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body acquireRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		handle, err := store.AcquireLock(body.ResourceID, body.TTLMs)
		if err != nil {
			writeJSON(w, http.StatusConflict, map[string]interface{}{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{"lock": handle})
	})

	mux.HandleFunc("/v1/locks/release", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body releaseRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		if err := store.ReleaseLock(body.ResourceID, body.Token); err != nil {
			writeJSON(w, http.StatusConflict, map[string]interface{}{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{"released": true})
	})

	mux.HandleFunc("/v1/fencing/issue", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body issueFenceRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		fenceID, err := store.IssueFence(body.ResourceID)
		if err != nil {
			writeJSON(w, http.StatusBadRequest, map[string]interface{}{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"resource_id": body.ResourceID,
			"fence_id":    fenceID,
		})
	})

	mux.HandleFunc("/v1/resource/write", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body writeRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		if err := store.WriteResource(body.ResourceID, body.FenceID, []byte(body.Data)); err != nil {
			writeJSON(w, http.StatusConflict, map[string]interface{}{"error": err.Error()})
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"resource_id": body.ResourceID,
			"fence_id":    body.FenceID,
			"written":     true,
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
