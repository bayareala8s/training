Benefit	Explanation
Stable Endpoint	NLB provides a static DNS name (and optionally Elastic IP) for Appian to target.
Supports UDP	Unlike ALB, NLB supports UDP traffic, which is used by Syslog.
High Availability	Automatically distributes syslog traffic across multiple Fargate tasks in different AZs.
Scalability	Add or remove tasks, and NLB will automatically route to healthy ones.
Health Checks	Routes traffic only to healthy Fargate tasks based on configured health checks.
Seamless Integration	Works with ECS and Fargate using Target Groups.
