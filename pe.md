

---

**Subject:** Follow-Up: Terraform Code, Lambda Strategy, Data Storage & Scalability Considerations

Hi \[Architect's Name],

Hope you're doing well.

Thank you again for presenting the proposed AWS architecture. It was insightful and aligns well with our strategic vision for building a robust and scalable file transfer platform.

I wanted to follow up with a few technical considerations and proposals for your input:

---

**1. Terraform Code Availability**
Would it be possible for AWS and your team to share the proposed architecture as a Terraform codebase (e.g., on GitHub)? This would allow us to test and experiment with each component, simulate deployment scenarios, and gain deeper familiarity with the implementation.

---

**2. Handling Lambda Limitations**
We’re reviewing strategies to address Lambda’s current constraints (15-minute execution timeout, 10,240 MB memory, and 10,240 MB ephemeral storage).
Some approaches we’re considering:

* Step Functions to break long-running flows into smaller stateful tasks
* Using Fargate for heavier workloads or parallel processing
* Leveraging EFS where higher temporary storage is required
* Splitting workloads into microtasks across multiple Lambdas

Would love to hear if these align with AWS best practices, or if the current design already accommodates such needs.

---

**3. Parent-Child Lambda Architecture Proposal**
We’re proposing a **Parent-Child Lambda model** to achieve a plug-and-play architecture:

* **Parent Lambda** serves as a router/manager, determining the processing pattern based on metadata or JSON config
* **Child Lambdas** are modular workers for specific file processing types (e.g., decryption, compression, format conversion)

This offers extensibility and makes it easier to onboard new patterns in the future.

---

**4. Data Storage Strategy (DynamoDB vs RDBMS)**
We’re also evaluating the best storage approach for metadata, configuration, and logging.
Would a **hybrid model** using both:

* **DynamoDB** (for high-speed lookups and flexible JSON configs)
* and **RDBMS** like PostgreSQL/MySQL (for reporting, relational integrity, audit trail)

…be suitable for our use case, or would you recommend sticking to one flavor based on access patterns and performance?

---

**5. Performance Engineering & Scalability**
Currently, our file transfer volume is around **125K files/day**. We want to design the system to **scale toward 1 million+ files/day**, with sustained throughput and observability.
We’d appreciate input on:

* Bottleneck identification and autoscaling recommendations
* Use of SQS/Kinesis for decoupling and parallelization
* Performance tuning considerations for Lambda/Fargate
* Real-world benchmarks or guidance AWS can provide to validate throughput at scale

---

We greatly value your partnership and look forward to collaborating further as we shape this into a production-grade system.


