package locks

import (
	"fmt"
	"sync"
	"sync/atomic"
	"time"
)

// LockHandle represents an acquired distributed lock.
type LockHandle struct {
	ResourceID string
	Token      string
	TTLMs      int
	expiresAt  time.Time
}

// MemoryLockService is an in-memory lock service.
type MemoryLockService struct {
	mu    sync.Mutex
	locks map[string]*LockHandle
}

// NewMemoryLockService creates a lock service.
func NewMemoryLockService() *MemoryLockService {
	return &MemoryLockService{locks: make(map[string]*LockHandle)}
}

// Acquire obtains a lock with TTL.
func (s *MemoryLockService) Acquire(resourceID string, ttlMs int) (*LockHandle, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	if existing, ok := s.locks[resourceID]; ok && time.Now().Before(existing.expiresAt) {
		return nil, fmt.Errorf("lock held")
	}
	handle := &LockHandle{
		ResourceID: resourceID,
		Token:      fmt.Sprintf("%s-%d", resourceID, time.Now().UnixNano()),
		TTLMs:      ttlMs,
		expiresAt:  time.Now().Add(time.Duration(ttlMs) * time.Millisecond),
	}
	s.locks[resourceID] = handle
	return handle, nil
}

// Release releases a lock.
func (s *MemoryLockService) Release(handle *LockHandle) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if cur, ok := s.locks[handle.ResourceID]; ok && cur.Token == handle.Token {
		delete(s.locks, handle.ResourceID)
	}
	return nil
}

// Renew extends lock TTL.
func (s *MemoryLockService) Renew(handle *LockHandle) error {
	s.mu.Lock()
	defer s.mu.Unlock()
	if cur, ok := s.locks[handle.ResourceID]; ok && cur.Token == handle.Token {
		cur.expiresAt = time.Now().Add(time.Duration(handle.TTLMs) * time.Millisecond)
		return nil
	}
	return fmt.Errorf("lock not held")
}

// MemoryFencingService issues monotonic tokens.
type MemoryFencingService struct {
	counters map[string]*int64
	mu       sync.Mutex
}

// NewMemoryFencingService creates fencing service.
func NewMemoryFencingService() *MemoryFencingService {
	return &MemoryFencingService{counters: make(map[string]*int64)}
}

// Issue returns next fencing token.
func (f *MemoryFencingService) Issue(resourceID string) (int64, error) {
	f.mu.Lock()
	defer f.mu.Unlock()
	if _, ok := f.counters[resourceID]; !ok {
		var zero int64
		f.counters[resourceID] = &zero
	}
	return atomic.AddInt64(f.counters[resourceID], 1), nil
}

// GatedResource rejects writes with stale fencing tokens.
type GatedResource struct {
	mu        sync.Mutex
	lastFence map[string]int64
}

// Write applies data if fenceID is strictly greater than last committed.
func (g *GatedResource) Write(resourceID string, fenceID int64, data []byte) error {
	g.mu.Lock()
	defer g.mu.Unlock()
	if g.lastFence == nil {
		g.lastFence = make(map[string]int64)
	}
	if fenceID <= g.lastFence[resourceID] {
		return fmt.Errorf("stale fence %d for %s (last=%d)", fenceID, resourceID, g.lastFence[resourceID])
	}
	g.lastFence[resourceID] = fenceID
	return nil
}
