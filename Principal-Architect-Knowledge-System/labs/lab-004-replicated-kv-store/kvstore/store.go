package kvstore

import (
	"fmt"
	"sync"
)

// Store manages multiple replicated shards.
type Store struct {
	mu          sync.RWMutex
	Shards      []*Cluster
	ReplicaDown map[int]map[int]bool
	ReadRepairs int
}

// NewStore creates a 3-shard cluster with N=3, R=2, W=2.
func NewStore(shardCount, replicas, r, w int) *Store {
	shards := make([]*Cluster, shardCount)
	down := make(map[int]map[int]bool)
	for i := 0; i < shardCount; i++ {
		shards[i] = NewCluster(i, replicas, r, w)
		down[i] = make(map[int]bool)
	}
	return &Store{Shards: shards, ReplicaDown: down}
}

func (s *Store) shardFor(key string) int {
	return ShardForKey(key, len(s.Shards))
}

func (s *Store) downFor(shard int) map[int]bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.ReplicaDown[shard]
}

// Put routes a write to the correct shard quorum.
func (s *Store) Put(key, value string) (VersionedValue, int, error) {
	shardID := s.shardFor(key)
	s.mu.RLock()
	down := s.ReplicaDown[shardID]
	cluster := s.Shards[shardID]
	s.mu.RUnlock()
	v, err := cluster.Put(key, value, down)
	return v, shardID, err
}

// Get performs quorum read and optional read repair.
func (s *Store) Get(key string, repair bool) (VersionedValue, int, bool, int) {
	shardID := s.shardFor(key)
	s.mu.RLock()
	down := s.ReplicaDown[shardID]
	cluster := s.Shards[shardID]
	s.mu.RUnlock()
	v, ok := cluster.QuorumRead(key, down)
	if !ok {
		return VersionedValue{}, shardID, false, 0
	}
	repairs := 0
	if repair {
		repairs = cluster.ReadRepair(key, v, down)
		s.mu.Lock()
		s.ReadRepairs += repairs
		s.mu.Unlock()
	}
	return v, shardID, true, repairs
}

// SetReplicaDown marks a replica unavailable for chaos demos.
func (s *Store) SetReplicaDown(shard, replica int, down bool) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if shard < 0 || shard >= len(s.Shards) {
		return fmt.Errorf("invalid shard %d", shard)
	}
	if replica < 0 || replica >= len(s.Shards[shard].Replicas) {
		return fmt.Errorf("invalid replica %d", replica)
	}
	if down {
		s.ReplicaDown[shard][replica] = true
	} else {
		delete(s.ReplicaDown[shard], replica)
	}
	return nil
}

// ResetChaos clears all replica-down flags.
func (s *Store) ResetChaos() {
	s.mu.Lock()
	defer s.mu.Unlock()
	for shard := range s.ReplicaDown {
		s.ReplicaDown[shard] = make(map[int]bool)
	}
}

// Stats returns observability counters.
func (s *Store) Stats() map[string]interface{} {
	s.mu.RLock()
	defer s.mu.RUnlock()
	downCount := 0
	for _, replicas := range s.ReplicaDown {
		downCount += len(replicas)
	}
	return map[string]interface{}{
		"shards":            len(s.Shards),
		"replicas_per_shard": len(s.Shards[0].Replicas),
		"quorum_r":          s.Shards[0].R,
		"quorum_w":          s.Shards[0].W,
		"replicas_down":     downCount,
		"read_repairs":      s.ReadRepairs,
	}
}

// ClusterView returns per-shard replica versions for a key (debug/demo).
func (s *Store) ClusterView(key string) map[string]interface{} {
	shardID := s.shardFor(key)
	s.mu.RLock()
	defer s.mu.RUnlock()
	replicas := make([]map[string]interface{}, 0, len(s.Shards[shardID].Replicas))
	for i, r := range s.Shards[shardID].Replicas {
		v, ok := r.Shard.Get(key)
		replicas = append(replicas, map[string]interface{}{
			"replica": i,
			"leader":  r.Shard.Leader,
			"down":    s.ReplicaDown[shardID][i],
			"present": ok,
			"version": v.Version,
			"value":   v.Value,
		})
	}
	return map[string]interface{}{
		"key":    key,
		"shard":  shardID,
		"replicas": replicas,
	}
}
