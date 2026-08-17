package saga

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestHappyPath(t *testing.T) {
	o := &Orchestrator{}
	s := &Saga{ID: "s1", IdempotencyKey: "k1"}
	p := &Participants{}
	if err := o.Run(s, p); err != nil {
		t.Fatal(err)
	}
	if s.State != StateCompleted {
		t.Fatalf("expected completed, got %s", s.State)
	}
	if p.PaymentCalls != 1 || p.InventoryCalls != 1 || p.ShippingCalls != 1 {
		t.Fatalf("expected one call each, got pay=%d inv=%d ship=%d", p.PaymentCalls, p.InventoryCalls, p.ShippingCalls)
	}
}

func TestInventoryFailureCompensates(t *testing.T) {
	o := &Orchestrator{}
	s := &Saga{ID: "s2", IdempotencyKey: "k2"}
	p := &Participants{InventoryFail: true}
	if err := o.Run(s, p); err == nil {
		t.Fatal("expected inventory failure")
	}
	if s.State != StateCompensated || p.CompensateCalls != 1 {
		t.Fatal("expected compensation")
	}
}

func TestOrchestratorCrashRecovery(t *testing.T) {
	store := NewStore()
	s, err := store.StartSaga("PROD-1", "k3")
	if err != nil {
		t.Fatal(err)
	}
	if _, err := store.SimulateCrash(s.ID, StatePaymentReserved); err != nil {
		t.Fatal(err)
	}
	recovered, err := store.RecoverSaga(s.ID)
	if err != nil {
		t.Fatal(err)
	}
	if recovered.State != StateCompleted {
		t.Fatalf("expected completed after recovery, got %s", recovered.State)
	}
}

func TestIdempotentParticipant(t *testing.T) {
	p := &Participants{}
	_ = p.ReservePayment("dup")
	_ = p.ReservePayment("dup")
	if p.PaymentCalls != 1 {
		t.Fatal("duplicate calls should be idempotent")
	}
}

func TestTimeoutRetry(t *testing.T) {
	o := &Orchestrator{}
	s := &Saga{ID: "s4", IdempotencyKey: "k4"}
	p := &Participants{InventoryFail: true}
	if err := o.RunWithRetry(s, p); err != nil {
		t.Fatal(err)
	}
	if s.State != StateCompleted {
		t.Fatal("retry should succeed")
	}
}

func TestStartSagaIdempotencyKey(t *testing.T) {
	store := NewStore()
	s1, err := store.StartSaga("SKU-1", "same-key")
	if err != nil {
		t.Fatal(err)
	}
	s2, err := store.StartSaga("SKU-1", "same-key")
	if err != nil {
		t.Fatal(err)
	}
	if s1.ID != s2.ID {
		t.Fatal("duplicate idempotency key should return same saga")
	}
}

func TestHTTPSagaHappyPath(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	body := []byte(`{"product_id":"PROD-42","idempotency_key":"http-1"}`)
	resp, err := http.Post(srv.URL+"/v1/sagas", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusCreated {
		t.Fatalf("expected 201, got %d", resp.StatusCode)
	}
	var payload map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		t.Fatal(err)
	}
	sagaObj := payload["saga"].(map[string]interface{})
	if sagaObj["state"] != string(StateCompleted) {
		t.Fatalf("expected completed, got %v", sagaObj["state"])
	}
}

func TestHTTPInventoryChaosCompensates(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	resp, err := http.Post(srv.URL+"/v1/chaos/inventory-fail", "application/json", nil)
	if err != nil {
		t.Fatal(err)
	}
	resp.Body.Close()

	body := []byte(`{"product_id":"PROD-99","idempotency_key":"http-fail"}`)
	resp, err = http.Post(srv.URL+"/v1/sagas", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusConflict {
		t.Fatalf("expected 409 conflict, got %d", resp.StatusCode)
	}
	var payload map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		t.Fatal(err)
	}
	sagaObj := payload["saga"].(map[string]interface{})
	if sagaObj["state"] != string(StateCompensated) {
		t.Fatalf("expected compensated, got %v", sagaObj["state"])
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
		t.Fatalf("expected 200 for openapi.json, got %d", resp.StatusCode)
	}
	if ct := resp.Header.Get("Content-Type"); ct != "application/json" {
		t.Fatalf("expected application/json, got %s", ct)
	}

	resp2, err := http.Get(srv.URL + "/docs")
	if err != nil {
		t.Fatal(err)
	}
	defer resp2.Body.Close()
	if resp2.StatusCode != http.StatusOK {
		t.Fatalf("expected 200 for /docs, got %d", resp2.StatusCode)
	}
}
