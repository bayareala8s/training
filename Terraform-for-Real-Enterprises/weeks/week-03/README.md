# Week 3 – Terraform Modules (Enterprise Design)

## Learning Objectives

- Design modules with clear inputs, outputs, and contracts
- Version and publish modules for internal consumption
- Manage dependencies and backward compatibility

## Topics

- Reusable module architecture
- Inputs and outputs
- Module versioning
- Dependency management
- Backward compatibility

## Labs

| Lab | Description |
|-----|-------------|
| **3.1** | Build production-style VPC module (subnets, IGW, NAT, tags) |
| **3.2** | Compose networking modules (security groups, route tables) |
| **3.3** | Publish module via registry, Git tag, or internal source |

## Deliverables

1. **Production-grade Terraform modules** — At least one networking module with examples/
2. **Module documentation** — README per module: inputs, outputs, examples, upgrade notes

## Suggested Time

8–10 hours

## Submission

PR: `week-03: vpc module v1.0.0` with semantic version tag and CHANGELOG entry.
