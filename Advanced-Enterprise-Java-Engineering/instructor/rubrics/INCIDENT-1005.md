# Rubric — INCIDENT-1005

**Type:** INCIDENT  
**Weights:** Technical accuracy 25% · Diagnostic method 20% · Production awareness 15% · Trade-off analysis 15% · Security / reliability 10% · Communication 10% · Efficiency 5%

A lucky “expired cert” with no `notAfter` or CN-versus-host quote must **not** max Diagnostic method (20%).

| Dimension | 5 | 3 | 1 |
|---|---|---|---|
| Technical accuracy | `payment-tls` expired (notAfter 15 Oct 2026); CN=`*.baypay.internal`; host `payments.apps.baypay.example`; pods Ready; curl 60 | Expired named; host or CN missing | “Ingress 503” or “CrashLoop” as RCA |
| Diagnostic method | Gate 1→2→3; curl opened to confirm handshake; openssl quoted | Used all files; skipped a hypothesis | Opened solutions or curl first |
| Production awareness | Rotate cert or fix host; TLS stays on; no pod/DB bounce | Restart Ingress only | Disable TLS to restore HTTP |
| Trade-off analysis | cert-manager vs calendar; SAN vs internal wildcard; Route shares host | Mentions renewal | HTTP-only as strategy |
| Security / reliability | No `tls.key` in notes; handshake is the customer failure; expiry alert | Mentions HTTPS | Pastes a private key |
| Communication | Ready pods named; no invented Spring 5xx | Usable, slightly over-confident | Blames “TLS” with no date or host |
| Efficiency | 45–75 minutes | Complete but slow | Incomplete worksheet |

Stabilization that only says “restart the pods” while they are already Ready loses Production awareness.
