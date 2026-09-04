# IHS plugin member status — PaymentCluster

**Captured:** 2026-09-08T21:23:00Z  
**Host:** `ihs-east.baypay.example`  
**File:** `/opt/IBM/HTTPServer/Plugins/config/baypay/plugin-cfg.xml` (synthetic excerpt)  
**Gate:** 3

## Cluster block (excerpt)

```xml
<ServerCluster Name="PaymentCluster" LoadBalance="RoundRobin">
  <Server Name="Pay1" CloneID="pay1">
    <Transport Hostname="was-pay-1.baypay.example" Port="9080" Protocol="http"/>
  </Server>
  <Server Name="Pay2" CloneID="pay2">
    <Transport Hostname="was-pay-2.baypay.example" Port="9080" Protocol="http"/>
  </Server>
  <Server Name="Pay3" CloneID="pay3">
    <Transport Hostname="was-pay-2.baypay.example" Port="9081" Protocol="http"/>
  </Server>
  <PrimaryServers>
    <Server Name="Pay1"/>
    <Server Name="Pay2"/>
    <Server Name="Pay3"/>
  </PrimaryServers>
</ServerCluster>
<UriGroup Name="Payment_URIs">
  <Uri Name="/payment/*"/>
</UriGroup>
```

Affinity / `JSESSIONID` routing is **off** for this URI group (matches the sessionless payment API).

## Runtime member view (plugin status page, 14:23 Pacific)

| Member | Transport | Connectable | In rotation | Last probe | Last HTTP from plugin |
|---|---|---|---|---|---|
| `Pay1` | `was-pay-1.baypay.example:9080` | yes | yes | 14:22:58 | 201 / 48 ms |
| `Pay2` | `was-pay-2.baypay.example:9080` | yes | yes | 14:22:58 | 504 gateway timeout / 120004 ms |
| `Pay3` | `was-pay-2.baypay.example:9081` | yes | yes | 14:22:59 | 504 gateway timeout / 120011 ms |

No member is marked down. Connectable stays **yes** on all three.

## Probe configuration (plugin custom properties, as generated)

| Property | Value |
|---|---|
| `ServerIOTimeout` | 120 |
| `ConnectTimeout` | 5 |
| `RetryInterval` | 60 |
| Health probe | TCP connect to the transport port |
| HTTP URI used for health | (none) |
| Application readiness path | (none) |

Priya Nair note (14:24 Pacific): “I can `nc` to 9080 and 9081 on `was-pay-2`. Plugin has not removed Pay2 or Pay3. I have not regenerated `plugin-cfg.xml` today.”

## What this file does not contain

Hung-thread stacks, PMI tables, and SystemOut lines live in the earlier gates. This page is the edge view only.
