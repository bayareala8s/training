package saga

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
  <title>Lab 010 — Saga Orchestration</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #6b3fa0; font-size: 1.5rem; }
    .ok { display: inline-block; background: #f3e8ff; color: #6b21a8; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #6b3fa0; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 010 — Saga Orchestration</h1>
  <p><span class="ok">running</span> Orchestrator drives payment → inventory → shipping with compensating transactions</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/sagas</code> — happy path completes all steps</li>
    <li><code>POST /v1/chaos/inventory-fail</code> — next saga fails inventory and compensates payment</li>
    <li><code>POST /v1/sagas</code> again — observe <code>compensated</code> state</li>
    <li><code>POST /v1/chaos/reset</code> — clear chaos flag</li>
    <li><code>POST /v1/sagas/{id}/recover</code> — resume after simulated crash</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_saga.sh</pre>
</body>
</html>`

type startSagaRequest struct {
	ProductID      string `json:"product_id"`
	IdempotencyKey string `json:"idempotency_key"`
}

type crashRequest struct {
	State SagaState `json:"state"`
}

// NewHandler returns the HTTP handler for the saga API.
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
			"service": "Lab 010 — Saga Orchestration",
			"status":  "running",
			"endpoints": map[string]string{
				"docs":         "GET /docs",
				"openapi":      "GET /openapi.json",
				"health":       "GET /health",
				"start_saga":   "POST /v1/sagas",
				"list_sagas":   "GET /v1/sagas",
				"get_saga":     "GET /v1/sagas/{id}",
				"recover":      "POST /v1/sagas/{id}/recover",
				"crash":        "POST /v1/sagas/{id}/crash",
				"chaos_fail":   "POST /v1/chaos/inventory-fail",
				"chaos_reset":  "POST /v1/chaos/reset",
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

	mux.HandleFunc("/v1/sagas", func(w http.ResponseWriter, r *http.Request) {
		switch r.Method {
		case http.MethodPost:
			var body startSagaRequest
			if err := json.NewDecoder(r.Body).Decode(&body); err != nil {
				writeError(w, http.StatusBadRequest, "invalid JSON body")
				return
			}
			saga, err := store.StartSaga(body.ProductID, body.IdempotencyKey)
			if err != nil {
				writeJSON(w, http.StatusConflict, map[string]interface{}{
					"saga":  saga,
					"error": err.Error(),
				})
				return
			}
			writeJSON(w, http.StatusCreated, map[string]interface{}{"saga": saga})
		case http.MethodGet:
			writeJSON(w, http.StatusOK, map[string]interface{}{"sagas": store.ListSagas()})
		default:
			methodNotAllowed(w)
		}
	})

	mux.HandleFunc("/v1/sagas/", func(w http.ResponseWriter, r *http.Request) {
		path := strings.TrimPrefix(r.URL.Path, "/v1/sagas/")
		parts := strings.Split(path, "/")
		if len(parts) == 0 || parts[0] == "" {
			http.NotFound(w, r)
			return
		}
		id := parts[0]

		if len(parts) == 1 && r.Method == http.MethodGet {
			saga, ok := store.GetSaga(id)
			if !ok {
				writeError(w, http.StatusNotFound, "saga not found")
				return
			}
			writeJSON(w, http.StatusOK, map[string]interface{}{"saga": saga})
			return
		}

		if len(parts) == 2 && parts[1] == "recover" && r.Method == http.MethodPost {
			saga, err := store.RecoverSaga(id)
			if err != nil {
				if strings.Contains(err.Error(), "not found") {
					writeError(w, http.StatusNotFound, err.Error())
					return
				}
				writeJSON(w, http.StatusConflict, map[string]interface{}{
					"saga":  saga,
					"error": err.Error(),
				})
				return
			}
			writeJSON(w, http.StatusOK, map[string]interface{}{"saga": saga})
			return
		}

		if len(parts) == 2 && parts[1] == "crash" && r.Method == http.MethodPost {
			var body crashRequest
			if err := json.NewDecoder(r.Body).Decode(&body); err != nil || body.State == "" {
				body.State = StatePaymentReserved
			}
			saga, err := store.SimulateCrash(id, body.State)
			if err != nil {
				writeError(w, http.StatusNotFound, err.Error())
				return
			}
			writeJSON(w, http.StatusOK, map[string]interface{}{"saga": saga})
			return
		}

		http.NotFound(w, r)
	})

	mux.HandleFunc("/v1/chaos/inventory-fail", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		store.SetInventoryFail(true)
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"inventory_fail": true,
			"message":        "next saga will fail inventory and compensate payment",
		})
	})

	mux.HandleFunc("/v1/chaos/reset", func(w http.ResponseWriter, r *http.Request) {
		if r.Method != http.MethodPost {
			methodNotAllowed(w)
			return
		}
		store.SetInventoryFail(false)
		writeJSON(w, http.StatusOK, map[string]interface{}{
			"inventory_fail": false,
			"message":        "chaos disabled",
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
