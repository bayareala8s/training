# Kube events — pay-prod-east-2

**Namespace:** `baypay-prod` (synthetic teaching cluster)  
**Pod:** `payment-service-east-2-7f9c8d4b6-xk2q1`  
**Gate:** 2  
**Source:** `kubectl get events` teaching paste. Not a real cluster.

```text
LAST SEEN   TYPE      REASON      OBJECT                                         MESSAGE
109m        Normal    Scheduled   pod/payment-service-east-2-7f9c8d4b6-xk2q1    Successfully assigned baypay-prod/payment-service-east-2-7f9c8d4b6-xk2q1 to ip-10-8-2-44
109m        Normal    Pulled      pod/payment-service-east-2-7f9c8d4b6-xk2q1    Container image "baypay.example/payment-service:3.8.2" already present
109m        Normal    Created     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Created container payment
109m        Normal    Started     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Started container payment
82m         Warning   OOMKilled   pod/payment-service-east-2-7f9c8d4b6-xk2q1    Container payment exceeded its memory limit (limit 512Mi, usage 512Mi)
82m         Normal    Killing     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Stopping container payment
82m         Normal    Created     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Created container payment
82m         Normal    Started     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Started container payment
58m         Warning   OOMKilled   pod/payment-service-east-2-7f9c8d4b6-xk2q1    Container payment exceeded its memory limit (limit 512Mi, usage 512Mi)
58m         Normal    Killing     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Stopping container payment
27m         Warning   OOMKilled   pod/payment-service-east-2-7f9c8d4b6-xk2q1    Container payment exceeded its memory limit (limit 512Mi, usage 512Mi)
27m         Normal    Killing     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Stopping container payment
27m         Normal    Pulled      pod/payment-service-east-2-7f9c8d4b6-xk2q1    Container image "baypay.example/payment-service:3.8.2" already present
27m         Normal    Created     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Created container payment
27m         Normal    Started     pod/payment-service-east-2-7f9c8d4b6-xk2q1    Started container payment
```

## Pod status excerpt (16:50 Pacific)

```text
Restart Count:  3
Last State:     Terminated
  Reason:       OOMKilled
  Exit Code:    137
  Started:      Thu, 15 Oct 2026 16:12:08 -0700
  Finished:     Thu, 15 Oct 2026 16:41:02 -0700
Current State:  Running
  Started:      Thu, 15 Oct 2026 16:41:11 -0700
Limits:
  memory:  512Mi
  cpu:     1
Requests:
  memory:  512Mi
  cpu:     250m
```

No `java.lang.OutOfMemoryError` event. The kubelet killed the container at the **cgroup** limit.
