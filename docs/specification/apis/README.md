---
description: The five Sygnal write APIs and three reads, at a glance.
---

# Sygnal APIs

| Endpoint | Callback | Direction | Sender role | Payload `@type` | FHIR alignment | Pattern |
|---|---|---|---|---|---|---|
| [`sygnal/deviation/flag`](deviation-flag.md) | `deviation/on_flag` | participant → counter-party or network | party to the transition, or `SUPERVISOR` | `sygnal:DeviationReport` | DetectedIssue *(provisional)* | request + callback |
| [`sygnal/event/report`](event-report.md) | — | edge → network | registered edge in the policy's scope | `sygnal:CoordinationEvent` (batched) | AuditEvent | one-way, no callback (`202`) |
| [`sygnal/policy/update`](policy-update.md) | `policy/on_update` | governance → edge | `GOVERNANCE` | `sygnal:CoordinationPolicy` | — (Sygnal-native) | request + callback |
| [`sygnal/plan/sync`](plan-sync.md) | `plan/on_sync` | plan owner → each participant | the plan's owner | `sygnal:SharedPlan` | CarePlan (hashed reference) | publish + per-party callback |
| [`sygnal/signal/emit`](signal-emit.md) | — (edge returns `Ack`) | network → edge | `OBSERVER` | `sygnal:Signal` | Communication | network-initiated push |
| [`sygnal/policy/get`](reads.md) | `policy/on_get` | edge → policy holder | edge in scope | `Query` → `{policies[]}` | — | pull, shaped like Beckn `status` |
| [`sygnal/deviation/get`](reads.md) | `deviation/on_get` | party → deviation holder | party to the deviation | `Query` → `DeviationReport` | — | pull, shaped like Beckn `status` |
| [`sygnal/plan/get`](reads.md) | `plan/on_get` | participant → plan owner | plan participant | `Query` → `SharedPlan` | — | pull, shaped like Beckn `status` |

All Sygnal APIs share the [conventions](../conventions.md): `{context, message}` envelope, `SygnalContext` header, signed requests, callbacks and responses, and asynchronous acknowledgement.

## Who implements what

| Component | Sends | Receives |
|---|---|---|
| [Edge Adapter](../../components/edge-adapter.md) / edge platform | `deviation/flag`, `event/report`, `plan/sync`, `*/get`, `policy/on_update`, `plan/on_sync`, `deviation/on_flag` (as respondent) | `policy/update`, `signal/emit`, `plan/sync`, `deviation/flag` (as counter-party), all `on_*` replies to its requests |
| [Policy Manager](../../components/policy-manager.md) | `policy/update`, `policy/on_get` | `policy/get`, `policy/on_update` |
| [Deviation & Escalation Platform](../../components/deviation-and-escalation.md) | `deviation/on_flag`, `deviation/on_get` | `deviation/flag`, `deviation/get` |
| [Network Intelligence](../../components/network-intelligence.md) | `signal/emit` | `event/report` |
