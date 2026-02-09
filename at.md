The architecture intentionally separates orchestration and management responsibilities from transfer execution responsibilities.

Orchestration services are responsible for validating requests, managing job lifecycle, enforcing idempotency, coordinating retries, tracking state, and applying policy controls.

Transfer execution services are responsible solely for streaming file data between source and target endpoints in a secure, reliable, and efficient manner.

This separation simplifies scaling, limits blast radius during failures, and ensures that orchestration logic is not impacted by long-running or network-bound file transfers.
