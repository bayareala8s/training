package raftsim

import (
	"bytes"
	"encoding/json"
	"net/http"
	"net/http/httptest"
	"testing"
)

func TestSingleLeaderPerTerm(t *testing.T) {
	c := NewCluster(5)
	c.Peers[0].ElectLeader(1)
	if c.LeaderCount(1) != 1 {
		t.Fatalf("expected single leader, got %d", c.LeaderCount(1))
	}
}

func TestElectionAfterLeaderCrash(t *testing.T) {
	c := NewCluster(3)
	c.Peers[0].ElectLeader(1)
	c.Peers[0].State = Follower
	c.Peers[1].ElectLeader(2)
	if c.Peers[1].State != Leader {
		t.Fatal("expected new leader after crash")
	}
}

func TestLogReplication(t *testing.T) {
	c := NewCluster(3)
	c.Peers[0].ElectLeader(1)
	if err := c.Peers[0].AppendEntry("set x=1"); err != nil {
		t.Fatal(err)
	}
	for _, p := range c.Peers {
		if len(p.Log) != 1 {
			t.Fatalf("peer %d missing log entry", p.ID)
		}
	}
}

func TestCommitSafety(t *testing.T) {
	c := NewCluster(5)
	c.Peers[0].ElectLeader(1)
	_ = c.Peers[0].AppendEntry("txn-1")
	entry, ok := c.Peers[4].CommittedEntry(0)
	if !ok || entry.Command != "txn-1" {
		t.Fatal("committed entry not preserved on follower")
	}
	c.Peers[0].State = Follower
	c.Peers[2].ElectLeader(2)
	entry2, ok := c.Peers[2].CommittedEntry(0)
	if !ok || entry2.Command != "txn-1" {
		t.Fatal("committed entry lost after election")
	}
}

func TestConflictTruncation(t *testing.T) {
	peer := &RaftPeer{ID: 2, Log: []LogEntry{{Term: 1, Command: "a"}, {Term: 1, Command: "b"}}}
	peer.TruncateLog(1, []LogEntry{{Term: 2, Command: "c"}})
	if len(peer.Log) != 2 || peer.Log[1].Command != "c" {
		t.Fatal("log truncation failed")
	}
}

func TestStoreElectAndAppend(t *testing.T) {
	store := NewStore()
	leaderID, term, err := store.ElectLeader()
	if err != nil || leaderID == 0 || term != 1 {
		t.Fatalf("elect failed: leader=%d term=%d err=%v", leaderID, term, err)
	}
	_, logLen, err := store.AppendLog("txn-1")
	if err != nil || logLen != 1 {
		t.Fatalf("append failed: len=%d err=%v", logLen, err)
	}
}

func TestHTTPElectLeader(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	resp, err := http.Post(srv.URL+"/v1/cluster/elect-leader", "application/json", nil)
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
	var payload map[string]interface{}
	if err := json.NewDecoder(resp.Body).Decode(&payload); err != nil {
		t.Fatal(err)
	}
	if payload["leader_id"] == nil {
		t.Fatal("expected leader_id in response")
	}
}

func TestHTTPAppendLog(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	_, err := http.Post(srv.URL+"/v1/cluster/elect-leader", "application/json", nil)
	if err != nil {
		t.Fatal(err)
	}

	body := []byte(`{"command":"set x=1"}`)
	resp, err := http.Post(srv.URL+"/v1/log/append", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
	}
}

func TestHTTPAppendWithoutLeader(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	body := []byte(`{"command":"set x=1"}`)
	resp, err := http.Post(srv.URL+"/v1/log/append", "application/json", bytes.NewReader(body))
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusConflict {
		t.Fatalf("expected 409, got %d", resp.StatusCode)
	}
}

func TestHTTPPeers(t *testing.T) {
	store := NewStore()
	srv := httptest.NewServer(NewHandler(store))
	defer srv.Close()

	resp, err := http.Get(srv.URL + "/v1/peers")
	if err != nil {
		t.Fatal(err)
	}
	defer resp.Body.Close()
	if resp.StatusCode != http.StatusOK {
		t.Fatalf("expected 200, got %d", resp.StatusCode)
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

	resp2, err := http.Get(srv.URL + "/docs")
	if err != nil {
		t.Fatal(err)
	}
	defer resp2.Body.Close()
	if resp2.StatusCode != http.StatusOK {
		t.Fatalf("expected 200 for /docs, got %d", resp2.StatusCode)
	}
}
