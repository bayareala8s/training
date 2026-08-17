package chaos

import (
	"fmt"
	"strings"
	"time"
)

// FaultType identifies injection mode.
type FaultType string

const (
	FaultLatency FaultType = "latency"
	FaultError   FaultType = "error_rate"
	FaultDepDown FaultType = "dependency_down"
)

// FaultConfig describes active fault injection.
type FaultConfig struct {
	Type      FaultType
	LatencyMs int
	ErrorRate float64
	Target    string
}

// FaultInjector applies and removes faults.
type FaultInjector struct {
	active bool
	config FaultConfig
}

// Enable activates fault injection.
func (f *FaultInjector) Enable(cfg FaultConfig) {
	f.active = true
	f.config = cfg
}

// Disable removes fault injection.
func (f *FaultInjector) Disable() {
	f.active = false
}

// Apply applies fault to a request.
func (f *FaultInjector) Apply(instance string) (time.Duration, error) {
	if !f.active || f.config.Target != "" && f.config.Target != instance {
		return 0, nil
	}
	switch f.config.Type {
	case FaultLatency:
		return time.Duration(f.config.LatencyMs) * time.Millisecond, nil
	case FaultError:
		if f.config.ErrorRate >= 1.0 {
			return 0, fmt.Errorf("injected error")
		}
	case FaultDepDown:
		return 0, fmt.Errorf("dependency down")
	}
	return 0, nil
}

// Experiment describes a chaos experiment manifest.
type Experiment struct {
	Name        string
	Hypothesis  string
	DurationSec int
	Fault       FaultConfig
	SLOBreach   float64
}

// Report is experiment output.
type Report struct {
	Name       string `json:"name"`
	Hypothesis string `json:"hypothesis"`
	Passed     bool   `json:"passed"`
	Summary    string `json:"summary"`
}

// Runner executes experiments.
type Runner struct{}

// Run executes an experiment and returns report.
func (r *Runner) Run(exp Experiment) (Report, error) {
	injector := &FaultInjector{}
	injector.Enable(exp.Fault)
	delay, err := injector.Apply(exp.Fault.Target)
	report := Report{
		Name:       exp.Name,
		Hypothesis: exp.Hypothesis,
		Passed:     err == nil && exp.SLOBreach < 0.05,
		Summary:    fmt.Sprintf("delay=%v err=%v", delay, err),
	}
	if exp.Fault.Type == FaultError && exp.SLOBreach >= 0.05 {
		report.Passed = false
	}
	injector.Disable()
	return report, nil
}

// ParseManifest parses minimal YAML-like experiment manifest.
func ParseManifest(content string) (Experiment, error) {
	exp := Experiment{Name: "unnamed"}
	for _, line := range strings.Split(content, "\n") {
		line = strings.TrimSpace(line)
		if strings.HasPrefix(line, "name:") {
			exp.Name = strings.TrimSpace(strings.TrimPrefix(line, "name:"))
		}
		if strings.HasPrefix(line, "hypothesis:") {
			exp.Hypothesis = strings.TrimSpace(strings.TrimPrefix(line, "hypothesis:"))
		}
		if strings.HasPrefix(line, "target:") {
			exp.Fault.Target = strings.TrimSpace(strings.TrimPrefix(line, "target:"))
		}
		if strings.HasPrefix(line, "type:") {
			exp.Fault.Type = FaultType(strings.TrimSpace(strings.TrimPrefix(line, "type:")))
		}
	}
	return exp, nil
}

// MarkdownReport formats report as markdown.
func MarkdownReport(r Report) string {
	status := "PASS"
	if !r.Passed {
		status = "FAIL"
	}
	return fmt.Sprintf("# Chaos Report: %s\n\n**Hypothesis:** %s\n\n**Result:** %s\n\n%s\n", r.Name, r.Hypothesis, status, r.Summary)
}
