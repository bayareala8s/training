package saga

import (
	"fmt"
	"sync"
	"time"
)

// SagaState represents orchestrator workflow state.
type SagaState string

const (
	StateStarted           SagaState = "started"
	StatePaymentReserved   SagaState = "payment_reserved"
	StateInventoryReserved SagaState = "inventory_reserved"
	StateShipped           SagaState = "shipped"
	StateCompleted         SagaState = "completed"
	StateCompensating      SagaState = "compensating"
	StateCompensated       SagaState = "compensated"
	StateFailed            SagaState = "failed"
)

// StepLog is one append-only transition in the saga log.
type StepLog struct {
	Step      string    `json:"step"`
	State     SagaState `json:"state"`
	Timestamp time.Time `json:"timestamp"`
}

// Saga holds workflow instance data.
type Saga struct {
	ID             string    `json:"id"`
	ProductID      string    `json:"product_id"`
	State          SagaState `json:"state"`
	IdempotencyKey string    `json:"idempotency_key"`
	Log            []StepLog `json:"log"`
	Error          string    `json:"error,omitempty"`
}

// Participants simulate payment, inventory, and shipping services.
type Participants struct {
	PaymentCalls    int
	InventoryCalls  int
	ShippingCalls   int
	CompensateCalls int
	InventoryFail   bool
	mu              sync.Mutex
	processed       map[string]bool
}

// ReservePayment simulates payment reservation (idempotent by key).
func (p *Participants) ReservePayment(key string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	if p.processed == nil {
		p.processed = make(map[string]bool)
	}
	if p.processed["pay:"+key] {
		return nil
	}
	p.PaymentCalls++
	p.processed["pay:"+key] = true
	return nil
}

// ReserveInventory simulates inventory reservation (idempotent by key).
func (p *Participants) ReserveInventory(key string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	if p.processed == nil {
		p.processed = make(map[string]bool)
	}
	if p.processed["inv:"+key] {
		return nil
	}
	if p.InventoryFail {
		return fmt.Errorf("inventory unavailable")
	}
	p.InventoryCalls++
	p.processed["inv:"+key] = true
	return nil
}

// CreateShipment simulates shipping (idempotent by key).
func (p *Participants) CreateShipment(key string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	if p.processed == nil {
		p.processed = make(map[string]bool)
	}
	if p.processed["ship:"+key] {
		return nil
	}
	p.ShippingCalls++
	p.processed["ship:"+key] = true
	return nil
}

// CompensatePayment reverses payment reservation.
func (p *Participants) CompensatePayment(key string) error {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.CompensateCalls++
	return nil
}

// Stats returns participant call counters for observability.
func (p *Participants) Stats() map[string]int {
	p.mu.Lock()
	defer p.mu.Unlock()
	return map[string]int{
		"payment_calls":    p.PaymentCalls,
		"inventory_calls":  p.InventoryCalls,
		"shipping_calls":   p.ShippingCalls,
		"compensate_calls": p.CompensateCalls,
	}
}

// Orchestrator drives saga steps with an in-memory transition log.
type Orchestrator struct {
	mu sync.Mutex
}

func (o *Orchestrator) appendLog(saga *Saga, step string, state SagaState) {
	saga.State = state
	saga.Log = append(saga.Log, StepLog{
		Step:      step,
		State:     state,
		Timestamp: time.Now().UTC(),
	})
}

// Run executes the happy path or compensation chain.
func (o *Orchestrator) Run(saga *Saga, p *Participants) error {
	o.mu.Lock()
	defer o.mu.Unlock()

	o.appendLog(saga, "start", StateStarted)

	if err := p.ReservePayment(saga.IdempotencyKey); err != nil {
		saga.Error = err.Error()
		o.appendLog(saga, "reserve_payment", StateFailed)
		return err
	}
	o.appendLog(saga, "reserve_payment", StatePaymentReserved)

	if err := p.ReserveInventory(saga.IdempotencyKey); err != nil {
		o.appendLog(saga, "reserve_inventory", StateCompensating)
		_ = p.CompensatePayment(saga.IdempotencyKey)
		saga.Error = err.Error()
		o.appendLog(saga, "compensate_payment", StateCompensated)
		return err
	}
	o.appendLog(saga, "reserve_inventory", StateInventoryReserved)

	if err := p.CreateShipment(saga.IdempotencyKey); err != nil {
		o.appendLog(saga, "create_shipment", StateCompensating)
		_ = p.CompensatePayment(saga.IdempotencyKey)
		saga.Error = err.Error()
		o.appendLog(saga, "compensate_payment", StateCompensated)
		return err
	}
	o.appendLog(saga, "create_shipment", StateShipped)
	o.appendLog(saga, "complete", StateCompleted)
	return nil
}

// Recover resumes an incomplete saga from the last committed step.
func (o *Orchestrator) Recover(saga *Saga, p *Participants) error {
	switch saga.State {
	case StatePaymentReserved:
		return o.resumeAfterPayment(saga, p)
	case StateInventoryReserved:
		return o.resumeAfterInventory(saga, p)
	case StateStarted:
		return o.Run(saga, p)
	default:
		return nil
	}
}

func (o *Orchestrator) resumeAfterPayment(saga *Saga, p *Participants) error {
	o.mu.Lock()
	defer o.mu.Unlock()

	if err := p.ReserveInventory(saga.IdempotencyKey); err != nil {
		o.appendLog(saga, "reserve_inventory", StateCompensating)
		_ = p.CompensatePayment(saga.IdempotencyKey)
		saga.Error = err.Error()
		o.appendLog(saga, "compensate_payment", StateCompensated)
		return err
	}
	o.appendLog(saga, "reserve_inventory", StateInventoryReserved)

	if err := p.CreateShipment(saga.IdempotencyKey); err != nil {
		o.appendLog(saga, "create_shipment", StateCompensating)
		_ = p.CompensatePayment(saga.IdempotencyKey)
		saga.Error = err.Error()
		o.appendLog(saga, "compensate_payment", StateCompensated)
		return err
	}
	o.appendLog(saga, "create_shipment", StateShipped)
	o.appendLog(saga, "complete", StateCompleted)
	return nil
}

func (o *Orchestrator) resumeAfterInventory(saga *Saga, p *Participants) error {
	o.mu.Lock()
	defer o.mu.Unlock()

	if err := p.CreateShipment(saga.IdempotencyKey); err != nil {
		o.appendLog(saga, "create_shipment", StateCompensating)
		_ = p.CompensatePayment(saga.IdempotencyKey)
		saga.Error = err.Error()
		o.appendLog(saga, "compensate_payment", StateCompensated)
		return err
	}
	o.appendLog(saga, "create_shipment", StateShipped)
	o.appendLog(saga, "complete", StateCompleted)
	return nil
}

// RunWithRetry retries once when inventory fails transiently.
func (o *Orchestrator) RunWithRetry(saga *Saga, p *Participants) error {
	err := o.Run(saga, p)
	if err != nil && p.InventoryFail {
		p.SetInventoryFail(false)
		saga.State = StateStarted
		saga.Log = nil
		saga.Error = ""
		return o.Run(saga, p)
	}
	return err
}

// SetInventoryFail toggles inventory failure injection (thread-safe).
func (p *Participants) SetInventoryFail(fail bool) {
	p.mu.Lock()
	defer p.mu.Unlock()
	p.InventoryFail = fail
}

// InventoryFailEnabled reports chaos flag.
func (p *Participants) InventoryFailEnabled() bool {
	p.mu.Lock()
	defer p.mu.Unlock()
	return p.InventoryFail
}
