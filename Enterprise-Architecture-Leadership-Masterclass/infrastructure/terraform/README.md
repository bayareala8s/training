# BayLearn Terraform — EA Leadership Masterclass

| Lab | Module | Environment | Reusable module |
| --- | ------ | ----------- | --------------- |
| 05 | Cloud and Platform Strategy | `environments/lab05` | `modules/platform-foundation` |
| 06 | Integration / Data | `environments/lab06` | `modules/integration-platform` |

## Rules

- Tag: `Project=BayLearn`, `Course=EnterpriseArchitectureLeadership`, `Module`, `Environment=Lab`
- Cost target: ~<$5 per lab when destroyed promptly
- Avoid NAT Gateway, always-on EC2, EKS, OpenSearch
- Transfer Family and AWS Config are optional/conceptual with cost warnings

## Cleanup

```bash
scripts/cleanup-lab05.sh
scripts/cleanup-lab06.sh
```

Case study: NorthStar Financial Services (fictional).
