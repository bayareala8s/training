package kvstore

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
  <title>Lab 004 — Replicated KV Store</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #0f766e; font-size: 1.5rem; }
    .ok { display: inline-block; background: #ccfbf1; color: #0f766e; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #0f766e; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 004 — Replicated Key-Value Store</h1>
  <p><span class="ok">running</span> 3 shards × 3 replicas, quorum R=2 W=2, consistent-hash routing</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>PUT /v1/keys/user:42</code> — write to W replicas on routed shard</li>
    <li><code>GET /v1/keys/user:42</code> — quorum read (highest version)</li>
    <li><code>GET /v1/keys/user:42/replicas</code> — inspect replica versions</li>
    <li><code>POST /v1/chaos/replica-down</code> — simulate replica failure</li>
    <li><code>GET /v1/keys/user:42?repair=true</code> — read + repair lagging replicas</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_kv.sh</pre>
</body>
</html>`

type putRequest struct {
	Value string `json:"value"`
}

type chaosRequest struct {
	Shard   int `json:"shard"`
	Replica int `json:"replica"`
}

// NewHandler returns the HTTP handler for the KV API.
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
			"service": "Lab 004 — Replicated KV Store",
			"status":  "running",
			"endpoints": map[string]string{
				"docs":     "GET /docs",
				"health":   "GET /health",
				"put":      "PUT /v1/keys/{key}",
				"get":      "GET /v1/keys/{key}",
				"replicas": "GET /v1/keys/{key}/replicas",
				"chaos":    "POST /v1/chaos/replica-down",
				"reset":    "POST /v1/chaos/reset",
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

	mux.HandleFunc("/v1/keys/", func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.Path, "/v1/keys/")
		parts := strings.Split(path, "/")
		if len(parts) == 0 || parts[0] == "" {
			http.NotFound(w, r)
			return
		}
		key := parts[0]

		if len(parts) == 2 && parts[1] == "replicas" && r.Method == http.MethodGet {
			writeJSON(w, http.StatusOK, store.ClusterView(key))
			return
		}

		switch r.Method {
		case http.MethodPut:
			var body putRequest
			if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.Value == "" {
				writeError(w, http.StatusBadRequest, "JSON body required: {\"value\": \"...\"}")
				return
			}
			v, shard, err := store.Put(key, body.Value)
			if err != nil {
				writeError(w, http.StatusServiceUnavailable, err.Error())
				return
			}
			writeJSON(w, http.StatusCreated, map[string]interface{}{
				"key": key, "value": v.Value, "version": v.Version, "shard": shard,
			})
		case http.MethodGet:
			repair := r.URL.Query().Get("repair") == "true"
			v, shard, ok, repairs := store.Get(key, repair)
			if !ok {
				writeError(w, http.StatusNotFound, "key not found")
				return
			}
			writeJSON(w, http.StatusOK, map[string]interface{}{
				"key": key, "value": v.Value, "version": v.Version, "shard": shard, "read_repairs": repairs,
			})
		default:
			methodNotAllowed(w)
		}
	})

	mux.HandleFunc("/v1/chaos/replica-down", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		var body chaosRequest
		if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
			writeError(w, http.StatusBadRequest, "invalid JSON body")
			return
		}
		if err := store.SetReplicaDown(body.Shard, body.Replica, true); err != nil {
			writeError(w, http.StatusBadRequest, err.Error())
			return
		}
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"shard": body.Shard, "replica": body.Replica, "down": true,
		})
	})

	mux.HandleFunc("/v1/chaos/reset", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		store.ResetChaos()
		writeJSON(w, http.StatusOK, map[string]string{"status": "chaos reset"})
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
