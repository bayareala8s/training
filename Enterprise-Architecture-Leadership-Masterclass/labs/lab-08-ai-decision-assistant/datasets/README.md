# Evaluation Dataset — Lab 08

**File:** `incident-eval-set.csv`  
**Rows:** 20 synthetic operational incidents  
**Organization:** NorthStar Financial Services (fictional)

> Fiction notice: All incident texts are invented for instruction. Do not treat as real events.

## Columns

| Column | Meaning |
| ------ | ------- |
| incident_id | Synthetic ID |
| incident_text | Input narrative for the assistant |
| expected_category | Label for evaluation |
| expected_severity | low/medium/high/critical |
| expected_routing_team | Team label |
| expected_hitl | true/false |
| expected_business_impact | Short impact statement |

## Suggested quality measure

Primary: **routing_team exact match rate** ≥ 70% on this set for mock or live mode.  
Secondary: **severity within ±1 level** ≥ 80%.  
Safety: **HITL recall on expected_hitl=true** ≥ 90%.
