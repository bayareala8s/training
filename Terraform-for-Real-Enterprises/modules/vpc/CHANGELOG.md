# Changelog — VPC Module

## [1.0.0] - 2026-05-27

### Added
- VPC with DNS support
- Public and private subnets across 2+ AZs
- Internet gateway and route tables
- Optional NAT Gateway (production pattern)
- NAT instance mode for stoppable labs (`Role=nat-instance`)
- VPC flow logs to CloudWatch (7-day retention)

### Notes
- Default lab config: NAT instance, not NAT Gateway, for cost control with `scripts/aws/stop-lab.sh`
