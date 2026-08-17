# Platform Modules CHANGELOG

## v1.0.0 — Initial release

### Added

- `network-baseline` — VPC with public/private subnets, NAT instance default, course tags
- `app-host` — private EC2 host with IMDSv2, egress-only SG

### Versioning policy

- **PATCH** — bug fixes, docs
- **MINOR** — new optional inputs
- **MAJOR** — removed/renamed required inputs

Consumers must pin `ref=` to a tag; never track `main` for production.
