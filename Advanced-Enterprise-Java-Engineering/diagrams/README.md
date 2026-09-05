# Diagram library — AEJE-D-001–072

Every diagram has editable source, SVG, PNG, and alt text. BayPay is fictional.

L-2.1 extra teaching pictures (not new catalog IDs): [java/l21/README.md](java/l21/README.md) — stack vs heap, stale `authorized`, happens-before APIs. **AEJE-D-005** is picture 2.

| ID | Title | Folder | Maps to |
|---|---|---|---|
| AEJE-D-001 | Modern Java, JDK and JVM stack | java | L-1.1 |
| AEJE-D-002 | SOLID and immutability | java | L-1.2 |
| AEJE-D-003 | BayPay transaction domain model | java | BUILD-101 |
| AEJE-D-004 | Payment validation flow | java | BUILD-102 |
| AEJE-D-005 | Java memory visibility | java | L-2.1 |
| AEJE-D-006 | Duplicate payment race | java | BREAKFIX-201 |
| AEJE-D-007 | Deadlocked payment workers | java | INCIDENT-202 |
| AEJE-D-008 | Safe concurrent payment processing | java | ARCHITECT-203 |
| AEJE-D-009 | Spring IoC container | spring | L-3.1 |
| AEJE-D-010 | Payment REST API request flow | spring | BUILD-301 |
| AEJE-D-011 | JPA transaction boundary | spring | L-3.4 |
| AEJE-D-012 | Actuator health and readiness | spring | BUILD-305 |
| AEJE-D-013 | Transaction rollback bug | spring | FIX-304 |
| AEJE-D-014 | Servlet and Jakarta EE model | java | L-4.1 |
| AEJE-D-015 | Spring to Jakarta mapping | java | ARCHITECT-401 |
| AEJE-D-016 | Connection pool exhaustion | java | INCIDENT-402 |
| AEJE-D-017 | Transaction boundary failure | java | INCIDENT-403 |
| AEJE-D-018 | WebSphere ND cell, DMGR, node, server | websphere | L-5.1 |
| AEJE-D-019 | BayPay WebSphere ND current state | websphere | ARCHITECT-501 |
| AEJE-D-020 | JDBC, JNDI and JMS | websphere | L-5.3 |
| AEJE-D-021 | Cluster members stop processing | websphere | INCIDENT-502 |
| AEJE-D-022 | Deployment failure | websphere | INCIDENT-504 |
| AEJE-D-023 | Traditional WebSphere vs Liberty | liberty | L-6.1 |
| AEJE-D-024 | Liberty features and server.xml | liberty | L-6.2 |
| AEJE-D-025 | BayPay Liberty adaptation | liberty | MODERNIZE-602 |
| AEJE-D-026 | Configuration externalization | liberty | MODERNIZE-603 |
| AEJE-D-027 | Migration waves and rollback | liberty | ARCHITECT-604 |
| AEJE-D-028 | Heap, stacks, metaspace and native memory | jvm | L-7.1 |
| AEJE-D-029 | Class loading and JIT | jvm | L-7.2 |
| AEJE-D-030 | Garbage collection | jvm | L-7.4 |
| AEJE-D-031 | JVM in containers | jvm | L-7.6 |
| AEJE-D-032 | Thread-dump decision tree | jvm | L-8.1 |
| AEJE-D-033 | CPU 98 percent | jvm | INCIDENT-801 |
| AEJE-D-034 | Memory leak | jvm | INCIDENT-802 |
| AEJE-D-035 | Deadlock | jvm | INCIDENT-803 |
| AEJE-D-036 | Thread-pool exhaustion | jvm | INCIDENT-804 |
| AEJE-D-037 | Container OOM | jvm | INCIDENT-806 |
| AEJE-D-038 | OCI container layers | containers | L-9.1 |
| AEJE-D-039 | BayPay container image | containers | BUILD-901 |
| AEJE-D-040 | Container trust boundary | containers | SECURITY-903 |
| AEJE-D-041 | Java resource sizing | containers | L-9.6 |
| AEJE-D-042 | Pods, Deployments and ReplicaSets | kubernetes | L-10.1 |
| AEJE-D-043 | OpenShift Routes vs Ingress | openshift | L-10.2 |
| AEJE-D-044 | CrashLoopBackOff | kubernetes | INCIDENT-1001 |
| AEJE-D-045 | OOMKilled | kubernetes | INCIDENT-1002 |
| AEJE-D-046 | Readiness failure | kubernetes | INCIDENT-1003 |
| AEJE-D-047 | Service routing failure | kubernetes | INCIDENT-1006 |
| AEJE-D-048 | ECR and ECS/Fargate BayPay | aws | BUILD-1101 |
| AEJE-D-049 | ECS vs EKS vs OpenShift | aws | ARCHITECT-1102 |
| AEJE-D-050 | IAM, Secrets Manager and KMS | aws | SECURITY-1103 |
| AEJE-D-051 | Unhealthy ALB target | aws | INCIDENT-1104 |
| AEJE-D-052 | Cost optimization levers | aws | COST-1105 |
| AEJE-D-053 | ALB, NLB and Route 53 | aws | L-11.4 |
| AEJE-D-054 | Git and CI flow | devops | L-12.1 |
| AEJE-D-055 | Reusable Terraform modules | devops | BUILD-1202 |
| AEJE-D-056 | CI/CD pipeline | devops | BUILD-1204 |
| AEJE-D-057 | Failed deployment and rollback | devops | INCIDENT-1205 |
| AEJE-D-058 | Ansible configuration automation | devops | BUILD-1203 |
| AEJE-D-059 | Logs, metrics and traces | observability | L-13.1 |
| AEJE-D-060 | RED, USE, SLI and SLO | observability | L-13.2 |
| AEJE-D-061 | BayPay operations dashboard | observability | BUILD-1300 |
| AEJE-D-062 | Throughput collapse and P99 spike | observability | INCIDENT-1301 |
| AEJE-D-063 | TLS and PKI trust boundary | security | L-14.1 |
| AEJE-D-064 | 99.99 percent HA failure domains | security | ARCHITECT-1401 |
| AEJE-D-065 | Certificate expiration | security | INCIDENT-1402 |
| AEJE-D-066 | Regional DR, RTO and RPO | security | DR-1403 |
| AEJE-D-067 | BayPay threat model | security | SECURITY-1404 |
| AEJE-D-068 | Evidence vs hypothesis | ai | L-15.2 |
| AEJE-D-069 | BayOps AI architecture | ai | AI-1501 |
| AEJE-D-070 | Human approval and hallucination detection | ai | L-15.6 |
| AEJE-D-071 | BayPay initial WebSphere topology | capstones | overview |
| AEJE-D-072 | Cloud-native BayPay target state | capstones | CAPSTONE-2 |

