package chaos

import (
	"fmt"
	"sync"
)

// RunExperimentRequest is the HTTP body for POST /v1/experiments/run.
type RunExperimentRequest struct {
	Name       string  `json:"name"`
	FaultType  string  `json:"fault_type"`
	LatencyMs  int     `json:"latency_ms"`
	ErrorRate  float64 `json:"error_rate"`
	Target     string  `json:"target"`
	Hypothesis string  `json:"hypothesis"`
	SLOBreach  float64 `json:"slo_breach"`
}

// EnableFaultRequest is the HTTP body for POST /v1/faults/enable.
type EnableFaultRequest struct {
	FaultType  string  `json:"fault_type"`
	LatencyMs  int     `json:"latency_ms"`
	ErrorRate  float64 `json:"error_rate"`
	Target     string  `json:"target"`
}

// Store coordinates fault injection and experiment execution.
type Store struct {
	mu         sync.RWMutex
	injector   *FaultInjector
	runner     *Runner
	enabled    bool
	config     FaultConfig
	experiments int
	passed      int
	failed      int
}

// NewStore creates a chaos engineering demo store.
func NewStore() *Store {
	return &Store{
		injector: &FaultInjector{},
		runner:   &Runner{},
	}
}

// EnableFault activates fault injection.
func (s *Store) EnableFault(req EnableFaultRequest) FaultConfig {
	s.mu.Lock()
	defer s.mu.Unlock()

	cfg := FaultConfig{
		Type:      FaultType(req.FaultType),
		LatencyMs: req.LatencyMs,
		ErrorRate: req.ErrorRate,
		Target:    req.Target,
	}
	if cfg.Type == "" {
		cfg.Type = FaultLatency
	}
	if cfg.Target == "" {
		cfg.Target = "api-1"
	}
	s.injector.Enable(cfg)
	s.enabled = true
	s.config = cfg
	return cfg
}

// DisableFault removes active fault injection.
func (s *Store) DisableFault() {
	s.mu.Lock()
	defer s.mu.Unlock()
	s.injector.Disable()
	s.enabled = false
}

// FaultActive reports whether faults are enabled.
func (s *Store) FaultActive() bool {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.enabled
}

// CurrentFault returns the active fault config.
func (s *Store) CurrentFault() FaultConfig {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return s.config
}

// ApplyFault applies the active fault to an instance (demo probe).
func (s *Store) ApplyFault(instance string) (Report, error) {
	s.mu.RLock()
	injector := s.injector
	s.mu.RUnlock()

	delay, err := injector.Apply(instance)
	return Report{
		Name:    "probe",
		Summary: fmt.Sprintf("delay=%v err=%v", delay, err),
		Passed:  err == nil,
	}, err
}

// RunExperiment executes a chaos experiment.
func (s *Store) RunExperiment(req RunExperimentRequest) (Report, error) {
	if req.Name == "" {
		req.Name = "unnamed"
	}
	faultType := FaultType(req.FaultType)
	if faultType == "" {
		faultType = FaultLatency
	}
	target := req.Target
	if target == "" {
		target = "api-1"
	}
	exp := Experiment{
		Name:        req.Name,
		Hypothesis:  req.Hypothesis,
		Fault: FaultConfig{
			Type:      faultType,
			LatencyMs: req.LatencyMs,
			ErrorRate: req.ErrorRate,
			Target:    target,
		},
		SLOBreach: req.SLOBreach,
	}
	if exp.Hypothesis == "" {
		exp.Hypothesis = "steady state maintained under fault"
	}

	s.mu.Lock()
	defer s.mu.Unlock()
	report, err := s.runner.Run(exp)
	s.experiments++
	if report.Passed {
		s.passed++
	} else {
		s.failed++
	}
	return report, err
}

// Stats returns observability counters for /health.
func (s *Store) Stats() map[string]interface{} {
	s.mu.RLock()
	defer s.mu.RUnlock()
	return map[string]interface{}{
		"fault_enabled":    s.enabled,
		"fault_type":       string(s.config.Type),
		"fault_target":     s.config.Target,
		"experiments_run":  s.experiments,
		"experiments_pass": s.passed,
		"experiments_fail": s.failed,
	}
}
