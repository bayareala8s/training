## Architecture Review

**Reviewer:** <!-- name -->  
**Author:** <!-- name -->  
**Week:** <!-- e.g. 2, 5, capstone -->

### Scope

<!-- What system or change is under review? -->

### Diagram

<!-- Link to diagram in repo or attach image -->

### Review checklist

- [ ] Account / environment boundaries are clear
- [ ] State file boundaries match blast radius
- [ ] IAM follows least privilege for Terraform and workloads
- [ ] Network ingress/egress is intentional (no accidental `0.0.0.0/0` on admin ports)
- [ ] Tagging and cost allocation are defined
- [ ] CI/CD includes plan before apply and approval where needed
- [ ] DR / rollback path is documented for critical components

### Findings

| Severity | Finding | Recommendation |
|----------|---------|----------------|
| | | |

### Decision

- [ ] Approved
- [ ] Approved with follow-ups
- [ ] Changes requested
