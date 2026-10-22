---
description: Report coordination metadata to the network, as the active policy permits. No callback.
---

# event/report

| | |
|---|---|
| **Endpoint** | `POST /sygnal/event/report` |
| **Callback** | None. Report in, signal out. |
| **Direction** | Edge → Network Intelligence |
| **Sender** | A registered edge within the active policy's scope |
| **Payload** | `{ "policyId": "...", "events": [ CoordinationEvent, ... ] }` |
| **Responses** | `202` (normal), `200`, `400`, `401`, `403`, `429`, `500` |

## When to use it

Send coordination events as the active [reporting policy](../../concepts/policies.md) requires: periodic aggregates (handoffs placed, accepted or completed; coverage) and, where the policy permits, individual notifiable cases. Batch several events in one message.

## Rules

* The receiver **MUST** refuse (`403`) any event carrying a field outside its mode's allow-list, or a metric code not defined in the policy's `metricDefinitions`.
* These fields are always permitted, and allow-lists do not list them: `@context`, `@type`, `id`, `revision`, `eventType`, `granularity`, `period`, `area`, `occurredAt`, `from`, `to`.
* **Aggregate events** (`granularity: AGGREGATE`) **MUST** carry `id` and `period`, **SHOULD** carry a coded `area`, and carry `metrics` only:
  * metric keys **MUST** be codes defined in the policy;
  * report counts, never rates: send numerator and denominator as two counts;
  * suppress or roll up any value below `minCellSize`;
  * a report with the same `id` and a higher `revision` **replaces** the earlier one.
* **Individual events** (`granularity: INDIVIDUAL`) are permitted only for conditions in the policy's `individual.appliesToConditions`. `caseDetail` may carry only the fields selected by `individual.allowedFields`. `subjectRef` and `subjectType` appear together, and only if the policy permits.
* `from.id`, if present, **MUST** equal `context.senderId`.
* There is no extension bag on `CoordinationEvent`.

## Example request

```json
{
  "context": {
    "version": "2.0.0",
    "action": "sygnal/event/report",
    "domain": "healthcare:care-coordination",
    "networkId": "sygnal.moh.example.org/care-net",
    "senderId": "hcm.moh.example.org",
    "receiverId": "observer.sygnal.moh.example.org",
    "transactionId": "5c0f3d2e-9a8b-4c7d-8e6f-5a4b3c2d1e0f",
    "messageId": "2c3d4e5f-6a7b-4c8d-9e0f-1a2b3c4d5e6f",
    "timestamp": "2026-07-01T00:05:00Z"
  },
  "message": {
    "policyId": "policy:moh:d01-coverage",
    "events": [
      {
        "@context": "https://spec.sygnal.network/contexts/v0.9.jsonld",
        "@type": "sygnal:CoordinationEvent",
        "id": "3e9b7c1a-5d2f-4a8e-9b6c-1f0e2d3c4b5a",
        "revision": 1,
        "eventType": "COVERAGE_REPORTED",
        "granularity": "AGGREGATE",
        "period": "2026-06-24T00:00:00Z/2026-07-01T00:00:00Z",
        "area": { "code": "XX-D01-12", "level": "subdistrict" },
        "from": { "id": "hcm.moh.example.org", "role": "PROVIDER" },
        "occurredAt": "2026-07-01T00:00:00Z",
        "metrics": { "householdsReached": 1840, "householdsTargeted": 2000 }
      }
    ]
  }
}
```

## Why there is no `on_report`

Reporting is the edge-to-network observation stream. When the network has something to say, it says it with a [`signal/emit`](signal-emit.md). An `on_report` would bring back synchronous coupling, where the edge waits on a business reply from the network. The signed transport acknowledgement already proves receipt. For an individual notifiable report that needs proof of durable receipt, the `Signature` header on the `200 Ack` **is** the signed receipt.

## Not on this channel

Operational telemetry about the exchanges themselves (counts, latencies, ACK/NACK, timeouts) does not travel on `event/report`. It uses the separate network telemetry channel, which the policy's `InstrumentationSection` governs. See [Reporting and signals](../../concepts/reporting-and-signals.md#two-channels-coordination-events-and-network-telemetry).
