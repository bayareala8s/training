package saga

import (
	"fmt"
	"sync"
	"sync/atomic"
)

// Store holds sagas and drives orchestration (in-memory saga log).
type Store struct {
	mu              sync.RWMutex
	sagas           map[string]*Saga
	byKey           map[string]string
	orchestrator    *Orchestrator
	participants    *Participants
	nextID          atomic.Uint64
}

// NewStore creates an empty saga store.
func NewStore() *Store {
	return &Store{
		sagas:        make(map[string]*Saga),
		byKey:        make(map[string]string),
		orchestrator: &Orchestrator{},
		participants: &Participants{},
	}
}

// StartSaga runs payment → inventory → shipping for a new order saga.
func (s *Store) StartSaga(productID, idempotencyKey string) (*Saga, error) {
	if productID == "" {
		return nil, fmt.Errorf("product_id is required")
	}
	if idempotencyKey == "" {
		idempotencyKey = fmt.Sprintf("auto-%d", s.nextID.Add(1))
	}

	s.mu.Lock()
	if existingID, ok := s.byKey[idempotencyKey]; ok {
		saga := s.sagas[existingID]
		s.mu.Unlock()
		return cloneSaga(saga), nil
	}

	id := fmt.Sprintf("saga-%d", s.nextID.Add(1))
	saga := &Saga{
		ID:             id,
		ProductID:      productID,
		State:          StateStarted,
		IdempotencyKey: idempotencyKey,
	}
	s.sagas[id] = saga
	s.byKey[idempotencyKey] = id
	s.mu.Unlock()

	if err := s.orchestrator.Run(saga, s.participants); err != nil {
		return cloneSaga(saga), err
	}
	return cloneSaga(saga), nil
}

// GetSaga returns a saga by ID.
func (s *Store) GetSaga(id string) (*Saga, bool) {
	s.mu.RLock()
	defer s.mu.RUnlock()
	saga, ok := s.sagas[id]
	if !ok {
		return nil, false
	}
	return cloneSaga(saga), true
}

// ListSagas returns all sagas (newest first).
func (s *Store) ListSagas() []*Saga {
	s.mu.RLock()
	defer s.mu.RUnlock()
	out := make([]*Saga, 0, len(s.sagas))
	for _, saga := range s.sagas {
		out = append(out, cloneSaga(saga))
	}
	return out
}

// RecoverSaga resumes an incomplete saga (crash recovery demo).
func (s *Store) RecoverSaga(id string) (*Saga, error) {
	s.mu.Lock()
	saga, ok := s.sagas[id]
	if !ok {
		s.mu.Unlock()
		return nil, fmt.Errorf("saga not found: %s", id)
	}
	s.mu.Unlock()

	if err := s.orchestrator.Recover(saga, s.participants); err != nil {
		return cloneSaga(saga), err
	}
	return cloneSaga(saga), nil
}

// SimulateCrash marks a saga mid-flight for recovery demo.
func (s *Store) SimulateCrash(id string, state SagaState) (*Saga, error) {
	s.mu.Lock()
	defer s.mu.Unlock()
	saga, ok := s.sagas[id]
	if !ok {
		return nil, fmt.Errorf("saga not found: %s", id)
	}
	saga.State = state
	saga.Log = append(saga.Log, StepLog{
		Step:  "crash_simulated",
		State: state,
	})
	return cloneSaga(saga), nil
}

// SetInventoryFail enables chaos injection for the next saga run.
func (s *Store) SetInventoryFail(fail bool) {
	s.participants.SetInventoryFail(fail)
}

// InventoryFailEnabled reports chaos flag.
func (s *Store) InventoryFailEnabled() bool {
	return s.participants.InventoryFailEnabled()
}

// Stats returns observability counters.
func (s *Store) Stats() map[string]interface{} {
	s.mu.RLock()
	defer s.mu.RUnlock()
	completed, compensated, failed := 0, 0, 0
	for _, saga := range s.sagas {
		switch saga.State {
		case StateCompleted:
			completed++
		case StateCompensated:
			compensated++
		case StateFailed:
			failed++
		}
	}
	out := map[string]interface{}{
		"sagas_total":          len(s.sagas),
		"sagas_completed":      completed,
		"sagas_compensated":    compensated,
		"sagas_failed":         failed,
		"inventory_fail_chaos": s.participants.InventoryFailEnabled(),
	}
	for k, v := range s.participants.Stats() {
		out[k] = v
	}
	return out
}

func cloneSaga(s *Saga) *Saga {
	logCopy := make([]StepLog, len(s.Log))
	copy(logCopy, s.Log)
	return &Saga{
		ID:             s.ID,
		ProductID:      s.ProductID,
		State:          s.State,
		IdempotencyKey: s.IdempotencyKey,
		Log:            logCopy,
		Error:          s.Error,
	}
}
