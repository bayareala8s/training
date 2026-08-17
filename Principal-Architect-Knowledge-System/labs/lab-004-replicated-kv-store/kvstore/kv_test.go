package kvstore

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func newTestStore() *Store {
	return NewStore(3, 3, 2, 2)
}

func TestHealthEndpoint(t *testing.T) {
	srv := httptest.NewServer(NewHandler(newTestStore()))
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

func TestPutGetSingleShard(t *testing.T) {
	srv := httptest.NewServer(NewHandler(newTestStore()))
	defer srv.Close()
	body := []byte(`{"value":"bar"}`)
	req, _ := http.NewRequest(http.MethodPut, srv.URL+"/v1/keys/foo", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	resp, err := http.DefaultClient.Do(req)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusCreated {
		t.Fatalf("expected 201, got %d", resp.StatusCode)
	}
	get, err := http.Get(srv.URL + "/v1/keys/foo")
	if err != nil {
		t.Fatal(err)
	}
	defer get.Body.Close()
	var payload map[string]interface{}
	if err := json.NewDecoder(get.Body).Decode(&payload); err != nil {
		t.Fatal(err)
	}
	if payload["value"] != "bar" {
		t.Fatalf("got %v", payload["value"])
	}
}

func TestQuorumRead(t *testing.T) {
	c := NewCluster(0, 3, 2, 2)
	c.Put("k", "v1", nil)
	c.Replicas[2].Shard.Put("k", "stale")
	v, ok := c.QuorumRead("k", nil)
	if !ok || v.Value != "v1" {
		t.Fatal("quorum read failed")
	}
}

func TestReadRepair(t *testing.T) {
	c := NewCluster(0, 3, 1, 1)
	c.Replicas[0].Shard.Put("k", "latest")
	latest, _ := c.Replicas[0].Shard.Get("k")
	if c.ReadRepair("k", latest, nil) < 1 {
		t.Fatal("expected read repair")
	}
}

func TestShardFailover(t *testing.T) {
	store := newTestStore()
	store.SetReplicaDown(0, 0, true)
	if _, _, err := store.Put("k", "v"); err != nil {
		t.Fatal(err)
	}
}

func TestCrossShard(t *testing.T) {
	store := newTestStore()
	_, s1, _ := store.Put("shard-a-key", "1")
	_, s2, _ := store.Put("other-shard-key", "2")
	if s1 == s2 {
		t.Fatal("expected different shards for different keys")
	}
}

func TestReplicaDownBlocksQuorum(t *testing.T) {
	store := newTestStore()
	key := "quorum-fail-key"
	shard := store.shardFor(key)
	_ = store.SetReplicaDown(shard, 0, true)
	_ = store.SetReplicaDown(shard, 1, true)
	if _, _, err := store.Put(key, "x"); err == nil {
		t.Fatal("expected quorum failure with 2 replicas down on same shard")
	}
}

func TestHTTPReadRepair(t *testing.T) {
	store := newTestStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()
	body := []byte(`{"value":"v1"}`)
	req, _ := http.NewRequest(http.MethodPut, srv.URL+"/v1/keys/repair-key", bytes.NewReader(body))
	req.Header.Set("Content-Type", "application/json")
	_, _ = http.DefaultClient.Do(req)
	store.Shards[store.shardFor("repair-key")].Replicas[2].Shard.Set("repair-key", VersionedValue{Value: "stale", Version: 0})
	resp, err := http.Get(srv.URL + "/v1/keys/repair-key?repair=true")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	var payload map[string]interface{}
	_ = json.NewDecoder(resp.Body).Decode(&payload)
	if int(payload["read_repairs"].(float64)) < 1 {
		t.Fatal("expected read repair")
	}
}

func TestSwaggerEndpoints(t *testing.T) {
	srv := httptest.NewServer(NewHandler(newTestStore()))
	defer srv.Close()
	if resp, _ := http.Get(srv.URL + "/docs"); resp.StatusCode != http.StatusOK {
		t.Fatal("expected /docs 200")
	}
	if resp, _ := http.Get(srv.URL + "/openapi.json"); resp.StatusCode != http.StatusOK {
		t.Fatal("expected /openapi.json 200")
	}
}
