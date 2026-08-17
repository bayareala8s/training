package raftsim

import (
	"fmt"
	"sync"
)

// RaftState is follower, candidate, or leader.
type RaftState string

const (
	Follower  RaftState = "follower"
	Candidate RaftState = "candidate"
	Leader    RaftState = "leader"
)

// LogEntry is a replicated command.
type LogEntry struct {
	Term    int
	Command string
}

// RaftPeer is an in-memory Raft node for simulation.
type RaftPeer struct {
	mu          sync.Mutex
	ID          int
	State       RaftState
	CurrentTerm int
	VotedFor    int
	Log         []LogEntry
	CommitIndex int
	peers       []*RaftPeer
}

// Cluster wires peers for simulation.
type Cluster struct {
	Peers []*RaftPeer
}

// NewCluster creates n Raft peers.
func NewCluster(n int) *Cluster {
	c := &Cluster{Peers: make([]*RaftPeer, n)}
	for i := 0; i < n; i++ {
		c.Peers[i] = &RaftPeer{ID: i + 1, State: Follower, VotedFor: -1}
	}
	for _, p := range c.Peers {
		p.peers = c.Peers
	}
	return c
}

// ElectLeader forces peer to become leader for simulation.
func (p *RaftPeer) ElectLeader(term int) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.CurrentTerm = term
	p.State = Leader
}

// AppendEntry replicates a command on the leader.
func (p *RaftPeer) AppendEntry(cmd string) error {
	p.mu.Lock()
	if p.State != Leader {
		p.mu.Unlock()
		return fmt.Errorf("not leader")
	}
	entry := LogEntry{Term: p.CurrentTerm, Command: cmd}
	p.Log = append(p.Log, entry)
	p.mu.Unlock()

	majority := len(p.peers)/2 + 1
	replicated := 1
	for _, peer := range p.peers {
		if peer.ID == p.ID {
			continue
		}
		peer.mu.Lock()
		peer.Log = append(peer.Log, entry)
		peer.mu.Unlock()
		replicated++
	}
	if replicated >= majority {
		commitIndex := len(p.Log) - 1
		for _, peer := range p.peers {
			peer.mu.Lock()
			if len(peer.Log) > 0 {
				peer.CommitIndex = commitIndex
			}
			peer.mu.Unlock()
		}
		p.mu.Lock()
		p.CommitIndex = commitIndex
		p.mu.Unlock()
	}
	return nil
}

// LeaderCount returns leaders in the current term.
func (c *Cluster) LeaderCount(term int) int {
	count := 0
	for _, p := range c.Peers {
		p.mu.Lock()
		if p.State == Leader && p.CurrentTerm == term {
			count++
		}
		p.mu.Unlock()
	}
	return count
}

// CommittedEntry returns committed entry at index if present.
func (p *RaftPeer) CommittedEntry(index int) (LogEntry, bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if index < 0 || index > p.CommitIndex || index >= len(p.Log) {
		return LogEntry{}, false
	}
	return p.Log[index], true
}

// TruncateLog removes divergent suffix and appends leader entries.
func (p *RaftPeer) TruncateLog(from int, entries []LogEntry) {
	p.mu.Lock()
	defer p.mu.Unlock()
	if from < len(p.Log) {
		p.Log = p.Log[:from]
	}
	p.Log = append(p.Log, entries...)
}
