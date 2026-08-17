package kvstore

import (
	"fmt"
	"hash/fnv"
	"sync"
)

// VersionedValue stores a value with monotonic version.
type VersionedValue struct {
	Value   string `json:"value"`
	Version int64  `json:"version"`
}

// Shard is a single KV replica.
type Shard struct {
	mu      sync.RWMutex
	data    map[string]VersionedValue
	ShardID int
	Replica int
	Leader  bool
}

// NewShard creates an empty shard replica.
func NewShard(shardID, replica int) *Shard {
	return &Shard{
		data:    make(map[string]VersionedValue),
		ShardID: shardID,
		Replica: replica,
		Leader:  replica == 0,
	}
}

// Put stores a key with incremented version.
func (s *Shard) Put(key, value string) VersionedValue {
	s.mu.Lock()
	defer s.mu.Unlock()
	cur := s.data[key]
	cur.Version++
	cur.Value = value
	s.data[key] = cur
	return cur
}

// Set stores an exact version (read repair).
func (s *Shard) Set(key string, vv VersionedValue) {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.data[key] = vv
}

// Get returns value if present.
func (s *Shard) Get(key string) (VersionedValue, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	v, ok := s.data[key]
	return v, ok
}

// Replica wraps a shard replica.
type Replica struct {
	Shard *Shard
}

// Cluster is one shard with N replicas and quorum settings.
type Cluster struct {
	Replicas []*Replica
	R        int
	W        int
}

// NewCluster creates n replicas with quorum settings.
func NewCluster(shardID, n, r, w int) *Cluster {
	c := &Cluster{R: r, W: w, Replicas: make([]*Replica, n)}
	for i := 0; i < n; i++ {
		c.Replicas[i] = &Replica{Shard: NewShard(shardID, i)}
	}
	return c
}

func (c *Cluster) availableReplicas(down map[int]bool) []int {
	ids := make([]int, 0, len(c.Replicas))
	for i := range c.Replicas {
		if down == nil || !down[i] {
			ids = append(ids, i)
		}
	}
	return ids
}

// Put writes to W available replicas.
func (c *Cluster) Put(key, value string, down map[int]bool) (VersionedValue, error) {
	available := c.availableReplicas(down)
	if len(available) < c.W {
		return VersionedValue{}, fmt.Errorf("insufficient replicas for W=%d (available=%d)", c.W, len(available))
	}
	var latest VersionedValue
	for i := 0; i < c.W; i++ {
		latest = c.Replicas[available[i]].Shard.Put(key, value)
	}
	return latest, nil
}

// QuorumRead reads from R replicas and returns highest version.
func (c *Cluster) QuorumRead(key string, down map[int]bool) (VersionedValue, bool) {
	available := c.availableReplicas(down)
	readCount := c.R
	if readCount > len(available) {
		readCount = len(available)
	}
	var best VersionedValue
	found := false
	for i := 0; i < readCount; i++ {
		if v, ok := c.Replicas[available[i]].Shard.Get(key); ok {
			if !found || v.Version > best.Version {
				best = v
				found = true
			}
		}
	}
	return best, found
}

// ReadRepair updates lagging replicas to latest version.
func (c *Cluster) ReadRepair(key string, latest VersionedValue, down map[int]bool) int {
	repairs := 0
	for i, r := range c.Replicas {
		if down != nil && down[i] {
			continue
		}
		if v, ok := r.Shard.Get(key); !ok || v.Version < latest.Version {
			r.Shard.Set(key, latest)
			repairs++
		}
	}
	return repairs
}

// ShardForKey maps a key to shard id.
func ShardForKey(key string, shardCount int) int {
	h := fnv.New32a()
	_, _ = h.Write([]byte(key))
	return int(h.Sum32() % uint32(shardCount))
}
