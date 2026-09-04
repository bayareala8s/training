# INC-SEC-1402 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** HTTPS handshake failures while payment tasks stay RUNNING  
**Region:** `us-west-2`  
**Cluster / service:** `baypay-prod-west` / `payment-service`  
**Host:** `payments.apps.baypay.example`  
**Your name / cohort:**  
**Time started:**  
**Time submitted:**

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1:  

Gate 2:  

Gate 3:  

## Supporting evidence

(File, timestamp, quote. Handshake result, leaf dates if present, ACM status and domain, Route 53 names that exist or do not resolve. Task lastStatus only if the timeline or a file states it.)

## Next investigation

(What would you open or measure next, and why? If you wanted an omitted evidence kind, say what it would show.)

## Stabilization action

(What restores merchant HTTPS *now*? Certificate object versus listener versus DNS versus app? What do you explicitly not do — TLS off, DB bounce, `dmgr-east`, security-group “fix”?)

## Remediation

(What remains after the page is quiet? Alerts, change-control, records as code?)

## Communication update

(Five lines max. Audience: merchant success + platform lead. No unsupported cause.)
