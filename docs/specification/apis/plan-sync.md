---
description: Publish or update a shared, versioned, multi-party plan by hashed reference. The plan itself stays at the edge.
---

# plan/sync

| | |
|---|---|
| **Endpoint** | `POST /sygnal/plan/sync` |
| **Callback** | `POST /sygnal/plan/on_sync` (one per participant) |
| **Direction** | Plan owner → each subscribed participant |
| **Sender** | The plan's owner (`owner.id` = `senderId`) |
| **Payload** | `sygnal:SharedPlan` |
| **Responses** | `200` (callback follows), `202`, `400`, `401`, `403`, `409`, `500` |

## When to use it

Use it when several providers share responsibility for one person's plan, for example concurrent HIV, tuberculosis and antenatal care. A shared plan is one-to-many: one plan with many subscribers. Two-party contracts would produce N copies and no single source of truth. So Sygnal models it as **publish to a shared reference**:

* the full plan (a FHIR CarePlan) stays at the owning edge;
* `plan/sync` carries the plan's id, `version`, a hash commitment (`planHash`), the owner, the participants and the `changeType` (`CREATED`, `UPDATED`, `CLOSED`);
* participants fetch the plan content itself through the records layer, with consent.

One publish becomes N separate deliveries, one per participant. Each delivery is addressed through the registry.

## Rules

* `owner.id` **MUST** equal `context.senderId`.
* `version` only ever increases (monotonic), or is a version vector, so that conflicts can be detected.
* `planHash` commits the owner to a specific plan version, so a later dispute can check the plan held at the edge against it.

## Callback: `plan/on_sync`

Each participant returns the `SharedPlan` with `participantStatus`:

* `SYNCED`: the participant holds this version;
* `CONFLICT`: the participant returns its own `version` so the owner can reconcile.

A participant that missed a sync catches up with [`plan/get`](reads.md).

## Example

```json
{
  "@context": "https://spec.sygnal.network/contexts/v0.9.jsonld",
  "@type": "sygnal:SharedPlan",
  "planId": "plan:patient-9f2:integrated",
  "version": "7",
  "planHash": { "algorithm": "BLAKE2b-512", "value": "b2:9af1...c3" },
  "owner": { "id": "phc.d01-central.example.org", "role": "PROVIDER" },
  "participants": [
    { "id": "chw2.d01-12.example.org", "role": "PROVIDER" },
    { "id": "art-centre.d01.example.org", "role": "PROVIDER" },
    { "id": "anc-clinic.d01.example.org", "role": "PROVIDER" }
  ],
  "changeType": "UPDATED",
  "lastUpdated": "2026-07-01T12:00:00Z"
}
```

{% hint style="info" %}
The edge governs care-plan ownership, conflict detection between concurrent plans, and emergency versus elective changes. See [Open questions](../../reference/open-questions.md) for what is still being designed.
{% endhint %}
