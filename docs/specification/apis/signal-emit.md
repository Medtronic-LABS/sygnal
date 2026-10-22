---
description: Send an advisory coordination signal from the network to an edge. The edge decides.
---

# signal/emit

| | |
|---|---|
| **Endpoint** | `POST /sygnal/signal/emit` |
| **Callback** | None. The edge returns only an `Ack`. |
| **Direction** | Network Intelligence → edge |
| **Sender** | A participant with the `OBSERVER` role |
| **Payload** | `sygnal:Signal` |
| **Responses** | `200`, `400`, `401`, `500` |

## When to use it

`signal/emit` completes the observation loop. Edges report in with `event/report` and raise deviations with `deviation/flag`; the network signals out with `signal/emit`.

| `signalType` | Typical basis |
|---|---|
| `FOLLOW_UP_DUE` | An expected follow-up or completion hasn't been reported |
| `UNACKNOWLEDGED_REFERRAL` | A referral was placed and not accepted within its service-level agreement (SLA) |
| `SLA_BREACH` | A coordination SLA was missed |
| `COVERAGE_GAP` | Coverage metadata shows unreached households or areas |
| `OUTBREAK_SUSPECTED` | Syndromic or notifiable signals crossed a threshold in an area |

## Rules

* The edge **MUST** verify that the sender holds the `OBSERVER` role (`401 AUT_UNAUTHORIZED_ACTION` otherwise).
* `recommendedAction` is **advisory only**. It is never a clinical or operational directive. The edge, and the people using it, decide.
* Every signal states its `basis`: what observation triggered it.
* `signal/emit` is network-initiated, with no preceding request. It is therefore signed with a standard `Signature`, not a callback signature.
* Signals carry coordination references (`relatesTo`: a transition, plan or area), never clinical content.

## Example

```json
{
  "@context": "https://spec.sygnal.network/contexts/v0.9.jsonld",
  "@type": "sygnal:Signal",
  "signalType": "FOLLOW_UP_DUE",
  "relatesTo": "contract:campaign-d01-2026:hh-4821",
  "target": { "id": "chw.d01-12.example.org", "role": "PROVIDER" },
  "severity": "WARNING",
  "basis": "no on_confirm acceptance within 72h SLA",
  "recommendedAction": "Visit household to complete routine-care enrolment.",
  "issuedAt": "2026-07-04T08:00:00Z"
}
```
