# Answer key — Week 2 quiz

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Secrets in git → disclosure; stolen creds → spoofing as partner. |
| 2 | **B** | CMK supports key policies and compliance storytelling. |
| 3 | **A** | ListBucket must be scoped with `s3:prefix` for subtree listing. |
| 4 | **B** | All four Block Public Access settings should be enabled. |
| 5 | **B** | Data events log object-level API calls. |
| 6 | **B** | Forces TLS for S3 API access. |
| 7 | **C** | Secrets Manager is the standard store for connector credentials. |
| 8 | **B** | Access logs complement CloudTrail for bucket request audit. |
| 9 | **B** | Overly tight SourceArn breaks legitimate AssumeRole (see AWS Transfer guidance). |
| 10 | **B** | Gateway endpoint keeps S3 traffic on AWS network from VPC. |
| 11 | **Sample:** CloudTrail PutObject; S3 access logs; Transfer logs; S3 version ID; structured app logs with user ID. (Any two.) | |
| 12 | **Sample:** Restricts listing/authorization to a partner subtree so roles cannot see other partners’ prefixes. | |
