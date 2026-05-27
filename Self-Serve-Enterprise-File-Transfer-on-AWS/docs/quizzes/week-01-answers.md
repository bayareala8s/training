# Answer key — Week 1 quiz

| Q | Answer | Explanation |
|---|--------|-------------|
| 1 | **B** | Transfer Family is a managed protocol edge; EC2 SFTP leaves patching, HA, and scaling to you. |
| 2 | **B** | Push inbound: partner connects and uploads to your server. |
| 3 | **B** | Home directory maps to S3 prefixes; not POSIX disk on Transfer for S3 domain. |
| 4 | **C** | Transfer service assumes the access role to read/write S3 on behalf of users. |
| 5 | **B** | Versioning aids audit and recovery for overwrites/deletes. |
| 6 | **B** | Per-partner prefixes enable IAM `s3:prefix` scoping (Module 2). |
| 7 | **B** | Connectors reach remote partner hosts; servers accept inbound to you. |
| 8 | **B** | Trust policy must allow `transfer.amazonaws.com` with correct account/ARN conditions. |
| 9 | **B** | Edge lands files; Lambda/Step Functions process asynchronously. |
| 10 | **C** | Lab 1 deploys SFTP → S3. |
| 11 | **Sample:** Who sent it; when; original filename; size/hash; partner ID; processing status. (Any two valid audit questions.) | |
| 12 | **Sample:** A **server** accepts partner connections to your endpoint; a **connector** initiates SFTP/FTPS sessions to remote partner systems. | |

**Grading short answers:** Award full credit for two distinct valid audit items (Q11) and a correct direction distinction (Q12).
