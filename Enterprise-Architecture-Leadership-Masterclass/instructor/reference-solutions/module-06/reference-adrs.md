# ADR-M06-01 — Emit AccountCreated on API create

**Decision:** Synchronous create via API; also emit `AccountCreated` for downstream consumers.  
**Alternatives:** Sync-only; event-only create.  
**Consequences:** Dual path complexity; better decoupling for onboarding analytics.

# ADR-M06-02 — Partner file landing without Transfer Family in lab/MVP teaching slice

**Decision:** Use S3 landing + eventing for lab and as a valid internal pattern; treat Transfer Family/MFT as production option when protocol mandates exist.  
**Consequences:** Lower lab cost; document protocol gap; production may still need managed SFTP.
