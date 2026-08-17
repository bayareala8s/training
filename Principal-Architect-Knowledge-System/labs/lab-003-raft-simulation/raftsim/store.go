package raftsim

import (
	"fmt"
	"sync"
)

// PeerInfo is a snapshot of a Raft peer for HTTP responses.
type PeerInfo struct {
	ID          int       `json:"id"`
	State       RaftState `json:"state"`
	CurrentTerm int       `json:"current_term"`
	LogLen      int       `json:"log_len"`
	CommitIndex int       `json:"commit_index"`
}

// Store wraps a simulated Raft cluster for the HTTP API.
type Store struct {
	mu          sync.Mutex
	cluster     *Cluster
	currentTerm int
	leaderID    int
	appendCount int
}

// NewStore creates a 5-node Raft simulation cluster.
func NewStore() *Store {
	return &Store{
		cluster:     NewCluster(5),
		currentTerm: 0,
		leaderID:    0,
	}
}

// ElectLeader increments term and elects the next peer as leader.
func (s *Store) ElectLeader() (int, int, error) {
	s.mu.Lock()
	defer s.mu.Unlock()

	s.currentTerm++
	// Demote all peers, then elect next leader in rotation.
	for _, p := range s.cluster.Peers {
		p.mu.Lock()
		p.State = Follower
		p.mu.Unlock()
	}
	idx := (s.currentTerm - 1) % len(s.cluster.Peers)
	leader := s.cluster.Peers[idx]
	leader.ElectLeader(s.currentTerm)
	s.leaderID = leader.ID
	return leader.ID, s.currentTerm, nil
}

// AppendLog replicates a command through the current leader.
func (s *Store) AppendLog(command string) (int, int, error) {
	if command == "" {
		return 0, 0, fmt.Errorf("command is required")
	}
	s.mu.Lock()
	defer s.mu.Unlock()

	if s.leaderID == 0 {
		return 0, 0, fmt.Errorf("no leader elected; call elect-leader first")
	}
	leader := s.cluster.Peers[s.leaderID-1]
	if err := leader.AppendEntry(command); err != nil {
		return 0, 0, err
	}
	s.appendCount++
	return leader.ID, len(leader.Log), nil
}

// Peers returns snapshots of all cluster peers.
func (s *Store) Peers() []PeerInfo {
	s.mu.Lock()
	defer s.mu.Unlock()

	out := make([]PeerInfo, 0, len(s.cluster.Peers))
	for _, p := range s.cluster.Peers {
		p.mu.Lock()
		out = append(out, PeerInfo{
			ID:          p.ID,
			State:       p.State,
			CurrentTerm: p.CurrentTerm,
			LogLen:      len(p.Log),
			CommitIndex: p.CommitIndex,
		})
		p.mu.Unlock()
	}
	return out
}

// Stats returns observability counters for /health.
func (s *Store) Stats() map[string]interface{} {
	s.mu.Lock()
	defer s.mu.Unlock()

	leaders := s.cluster.LeaderCount(s.currentTerm)
	return map[string]interface{}{
		"peer_count":    len(s.cluster.Peers),
		"current_term":  s.currentTerm,
		"leader_id":     s.leaderID,
		"leaders_in_term": leaders,
		"append_total":  s.appendCount,
	}
}
