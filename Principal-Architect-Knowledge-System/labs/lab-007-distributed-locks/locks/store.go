package locks

import (
	"fmt"
	"sync"
)

// Store coordinates lock, fencing, and gated resource services.
type Store struct {
	mu       sync.RWMutex
	locks    *MemoryLockService
	fencing  *MemoryFencingService
	resource *GatedResource
	acquires int
	releases int
	writes   int
	rejects  int
}

// NewStore creates an in-memory lock and fencing demo store.
func NewStore() *Store {
	return &Store{
		locks:    NewMemoryLockService(),
		fencing:  NewMemoryFencingService(),
		resource: &GatedResource{},
	}
}

// AcquireLock obtains a distributed lock on a resource.
func (s *Store) AcquireLock(resourceID string, ttlMs int) (*LockHandle, error) {
	if resourceID == "" {
		return nil, fmt.Errorf("resource_id is required")
	}
	if ttlMs <= 0 {
		ttlMs = 5000
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	h, err := s.locks.Acquire(resourceID, ttlMs)
	if err != nil {
		return nil, err
	}
	s.acquires++
	return h, nil
}

// ReleaseLock releases a lock by resource ID and token.
func (s *Store) ReleaseLock(resourceID, token string) error {
	if resourceID == "" || token == "" {
		return fmt.Errorf("resource_id and token are required")
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	err := s.locks.Release(&LockHandle{ResourceID: resourceID, Token: token})
	if err == nil {
		s.releases++
	}
	return err
}

// IssueFence returns the next monotonic fencing token for a resource.
func (s *Store) IssueFence(resourceID string) (int64, error) {
	if resourceID == "" {
		return 0, fmt.Errorf("resource_id is required")
	}
	return s.fencing.Issue(resourceID)
}

// WriteResource applies data if the fencing token is valid.
func (s *Store) WriteResource(resourceID string, fenceID int64, data []byte) error {
	if resourceID == "" {
		return fmt.Errorf("resource_id is required")
	}
	s.mu.Lock()
	defer s.mu.Unlock()
	err := s.resource.Write(resourceID, fenceID, data)
	if err != nil {
		s.rejects++
		return err
	}
	s.writes++
	return nil
}

// Stats returns observability counters for /health.
func (s *Store) Stats() map[string]interface{} {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return map[string]interface{}{
		"lock_acquires":  s.acquires,
		"lock_releases":  s.releases,
		"resource_writes": s.writes,
		"fencing_rejects": s.rejects,
	}
}
