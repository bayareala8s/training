# Diagram Taxonomy

Every module must include diagrams across these categories.

| Code | Category | Purpose |
| ---- | -------- | ------- |
| `concept` | Concept | Explain architecture ideas and frameworks |
| `process` | Process flow | How work / decisions progress |
| `aws` | AWS reference architecture | Service-level reference designs |
| `sequence` | Sequence | Time-ordered interactions |
| `infrastructure` | Infrastructure | Accounts, network, shared services, CI/CD |
| `dataflow` | Data flow | Movement of business/technical data |
| `security` | Security | Trust, IAM, encryption, threat, DR |
| `executive` | Executive | CIO-ready simplified views |

## Lab diagram set (required per AWS / architecture lab)

1. Business context  
2. Current architecture  
3. Target architecture  
4. Step-by-step deployment  
5. AWS resources  
6. Data flow  
7. Security  
8. Monitoring  
9. Failure scenario  
10. Recovery  
11. Cleanup flow  
12. Expected final architecture  

## Naming convention

```text
{module|lab|cap}-{NN}-{category}-{slug}
```

Examples:

- `m01-concept-ea-domains`
- `m05-aws-landing-zone`
- `lab06-dataflow-payment-events`
- `cap-executive-transformation-overview`

## Manifest fields

Each diagram entry must declare: `id`, `title`, `category`, `module`, `lesson`, `lab`, `slides`, `workbook`, `learningObjective`, `formats`, `awsIcons[]`, `tags[]`.
