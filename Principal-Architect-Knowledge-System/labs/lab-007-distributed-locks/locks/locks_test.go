package locks

import (
	"bytes"
	"encoding/json"
	"fmt"
	"net/http"
	"net/http/httptest"
	"testing"
	"time"
)

func TestRedisLockAcquireRelease(t *testing.T) {
	svc := NewMemoryLockService()
	h, err := svc.Acquire("resource-1", 5000)
	if err != nil {
		t.Fatal(err)
	}
	if err := svc.Release(h); err != nil {
		t.Fatal(err)
	}
	if _, err := svc.Acquire("resource-1", 5000); err != nil {
		t.Fatal("expected re-acquire after release")
	}
}

func TestLockTTLExpiry(t *testing.T) {
	svc := NewMemoryLockService()
	_, err := svc.Acquire("r1", 1)
	if err != nil {
		t.Fatal(err)
	}
	time.Sleep(5 * time.Millisecond)
	if _, err := svc.Acquire("r1", 1000); err != nil {
		t.Fatal("expected lock expired")
	}
}

func TestFencingRejectsStale(t *testing.T) {
	res := &GatedResource{}
	if err := res.Write("blob-1", 10, []byte("a")); err != nil {
		t.Fatal(err)
	}
	if err := res.Write("blob-1", 9, []byte("b")); err == nil {
		t.Fatal("expected stale fence rejection")
	}
}

func TestMonotonicFencing(t *testing.T) {
	f := NewMemoryFencingService()
	t1, _ := f.Issue("blob")
	t2, _ := f.Issue("blob")
	if t2 <= t1 {
		t.Fatal("fencing tokens must be monotonic")
	}
}

func TestStaleHolderScenario(t *testing.T) {
	svc := NewMemoryLockService()
	fence := NewMemoryFencingService()
	res := &GatedResource{}
	h, _ := svc.Acquire("blob", 1)
	token, _ := fence.Issue("blob")
	_ = res.Write("blob", token, []byte("ok"))
	time.Sleep(5 * time.Millisecond)
	_, _ = svc.Acquire("blob", 5000)
	if err := res.Write("blob", token, []byte("stale")); err == nil {
		t.Fatal("stale holder write should be rejected")
	}
	_ = h
}

func TestStoreAcquireRelease(t *testing.T) {
	store := NewStore()
	h, err := store.AcquireLock("r1", 5000)
	if err != nil {
		t.Fatal(err)
	}
	if err := store.ReleaseLock(h.ResourceID, h.Token); err != nil {
		t.Fatal(err)
	}
}

func TestHTTPAcquireAndWrite(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	acquireBody := []byte(`{"resource_id":"blob-1","ttl_ms":5000}`)
	resp, err := http.Post(srv.URL+"/v1/locks/acquire", "application/json", bytes.NewReader(acquireBody))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}

	fenceBody := []byte(`{"resource_id":"blob-1"}`)
	resp2, err := http.Post(srv.URL+"/v1/fencing/issue", "application/json", bytes.NewReader(fenceBody))
	if err != nil {
		t.Fatal(err)
	}
	defer resp2.Body.Close()
	var fencePayload map[string]interface{}
	if err := json.NewDecoder(resp2.Body).Decode(&fencePayload); err != nil {
		t.Fatal(err)
	}
	fenceID := fencePayload["fence_id"]

	writeJSON := fmt.Sprintf(`{"resource_id":"blob-1","fence_id":%v,"data":"ok"}`, fenceID)
	resp3, err := http.Post(srv.URL+"/v1/resource/write", "application/json", bytes.NewReader([]byte(writeJSON)))
	if err != nil {
		t.Fatal(err)
	}
	defer resp3.Body.Close()
	if resp3.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp3.StatusCode)
	}
}

func TestHTTPStaleFenceRejected(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	fenceBody := []byte(`{"resource_id":"blob-1"}`)
	resp, err := http.Post(srv.URL+"/v1/fencing/issue", "application/json", bytes.NewReader(fenceBody))
	if err != nil {
		t.Fatal(err)
	}
	var fencePayload map[string]interface{}
	json.NewDecoder(resp.Body).Decode(&fencePayload)
	resp.Body.Close()
	fenceID := fencePayload["fence_id"]

	writeJSON := fmt.Sprintf(`{"resource_id":"blob-1","fence_id":%v,"data":"first"}`, fenceID)
	http.Post(srv.URL+"/v1/resource/write", "application/json", bytes.NewReader([]byte(writeJSON)))

	staleJSON := fmt.Sprintf(`{"resource_id":"blob-1","fence_id":%v,"data":"stale"}`, fenceID)
	resp2, err := http.Post(srv.URL+"/v1/resource/write", "application/json", bytes.NewReader([]byte(staleJSON)))
	if err != nil {
		t.Fatal(err)
	}
	defer resp2.Body.Close()
	if resp2.StatusCode != http.StatusConflict {
		t.Fatalf("expected 409, got %d", resp2.StatusCode)
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
