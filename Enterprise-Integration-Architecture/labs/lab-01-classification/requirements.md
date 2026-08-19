# Lab 1 — Fifteen requirements

For each, choose **API / Message / Event / File / ESB-Adapter / AI Agent**.

If a bullet hides multiple flows, split them.

1. Mobile must display the customer's current **account balance within 300 ms**.
2. Corporate customers submit **payment instructions** that must be processed even if the posting engine is down for 20 minutes.
3. **Twenty downstream systems** must learn whenever a customer changes their mailing address.
4. A regulator requires a **20 GB extract** delivered to 50 organizations **every night**.
5. A partner can **only speak SFTP** and will not fund an API project this year.
6. The call center asks, in natural language, **"Did customer ABC's settlement file arrive, and why did it fail?"**
7. Operators want to **reprocess a failed payment file** from the assistant.
8. A 1998 **MQ/ISO 20022** connection to the payment scheme cannot change in this budget year.
9. The website must **create an order** and show validation errors immediately.
10. After an order is created, **inventory, email, and analytics** should react independently.
11. Image packages of **10–50 GB** must be uploaded by a browser user who is authenticated.
12. Fraud scoring sometimes takes **90 seconds**; account opening cannot block on it.
13. A **canonical "Customer"** object on the ESB is blocking a mobile release; you need a path that does not wait for the committee.
14. Warehouse systems are **offline every Sunday**; checkout is not.
15. Security wants an **audit trail of who approved a replay** of a poison payment message.

Suggested (not unique) directions for self-check after you write rationales:

1 API · 2 Message · 3 Event · 4 File · 5 File/SFTP · 6 Agent+status API · 7 Agent+HITL+workflow · 8 Adapter · 9 API · 10 Event/pub-sub · 11 File/claim-check · 12 Message · 13 Domain API/event, not more ESB · 14 Message/queue buffer · 15 Audit event + HITL store
