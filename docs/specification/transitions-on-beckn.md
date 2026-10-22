---
description: How a handoff is expressed with unchanged Beckn v2 verbs and contracts. Profile, don't alias.
---

# Transitions on Beckn

Handoffs (referrals, transfers, enrolments, field tasks, escalations) are carried by **standard Beckn Protocol v2 transactions**. Sygnal adds no transition verbs. This page sets out the profile.

## Profile, don't alias

Sygnal does not introduce wire-level aliases such as a `transition` verb that means `init` + `confirm`. No Beckn gateway, registry, validator or SDK would recognise a new wire verb. Sygnal would lose the existing Beckn tooling, which is the reason to reuse Beckn in the first place.

* **Wire layer:** Beckn verbs, unchanged.
* **Semantic layer:** a **CareTransition** is a *profile*: a named use of the Beckn contract, bound to health and limited to a set lifecycle. The specification describes it as a workflow ("these verbs, in this order, with these schemas"), never as one name that stands for several verbs.
* **SDK layer (optional):** a convenience such as `createTransition()` may wrap the Beckn calls. It helps developers but is not part of the protocol.

## The lifecycle

| Beckn action | Use in a transition | Required? |
|---|---|---|
| `discover` / `on_discover` | Find a receiver | Matched transitions only |
| `select` / `on_select` | Choose an offer | When there is a real choice |
| `init` / `on_init` | Agree terms: consent, service-level agreement (SLA), responsible party | Negotiated transitions |
| `confirm` / `on_confirm` | Place the handoff; the contract is created | **Always** |
| `status` / `on_status` | Observe state; unsolicited `on_status` pushes are allowed | As needed |
| `update` / `on_update` | Change and notify: attended, outcome, reassignment | As needed |
| `cancel` / `on_cancel` | Withdraw or decline after acceptance | As needed |

Acceptance, decline, attendance, no-show and completion are **states**, reported as `{status, statusReason}` on the callback. They are not verbs.

Two practical notes:

* Negotiation before the handoff is placed runs through `select` and `init` only. Beckn's `context.try` (preview mode) applies only to `update` and `cancel`, not `confirm`.
* Unsolicited `on_status` is Beckn's built-in way for one party to push a state change to the other without being asked.

## The contract

The Beckn v2 `Contract` is domain-neutral and supports non-economic value. Its only required field is `commitments`; consideration, settlement and payment are optional, and `confirm` is not tied to payment. So a transition fits the contract simply:

```json
{
  "commitments": [ { "status": "...", "resources": [ { "id": "...", "quantity": 1 } ], "offer": { "id": "...", "resourceIds": ["..."] } } ],
  "status": "...",
  "participants": [ "..." ],
  "contractAttributes": { "@type": "HealthReferral", "...": "..." }
}
```

`contractAttributes` is Beckn's built-in extension point for domain attributes.

## Schema packs used

Each pack fills one of Beckn's extension points (`contractAttributes`, `offerAttributes`, `resourceAttributes`, `participantAttributes`). Health packs carry clinical handoffs; the generic service packs carry non-clinical coordination and are the base the health packs extend.

| Pack | Extension point | Used for | Reference flows |
|---|---|---|---|
| `HealthReferral` | `contractAttributes` | Clinical referrals (T1): specialty, urgency tier, `lifecycleState`, `notificationRoster`, in-band `deviation`, `referralNote` pointer, `consent`, `targetBookingRef` | UC1, UC2, UC4 |
| `HealthContract` | `contractAttributes` | Downstream bookings (T2), with `coordinationRef` back to the referral | UC4 |
| `HealthOffer` | `offerAttributes` | What a health service offers: service type, outcome commitments | UC1, UC2, UC4 |
| `HealthResource` | `resourceAttributes` | A health resource being booked, for example a physical consultation | UC4 |
| `HealthParticipant` | `participantAttributes` | Participants in a health handoff and their roles, for example a community health worker and their health identifiers | UC1, UC2, UC4 |
| `ServiceCoordination` | `contractAttributes` | Generic, non-clinical coordination, for example a field task | UC3 |
| `ServiceCoordinationOffer` | `offerAttributes` | A coordination engagement, such as a campaign's coverage window | UC3 |
| `ServiceCoordinationResource` | `resourceAttributes` | A standing coordination capability: a coordination desk and its scope (categories, service types, geography) | UC1, UC2, UC3 |
| `ServiceParticipant` | `participantAttributes` | Participants in a generic coordination and their roles, for example the requester | UC3 |

Each pack is referenced at runtime by its `@context` URL, `https://schema.beckn.io/<Pack>/v2.1/context.jsonld`. Sygnal doesn't copy them. The packs belong to a larger catalogue (consideration, entitlement, performance and settlement packs, for example) that Sygnal networks can use as needs arise; see [Related specifications](../reference/related-specifications.md). Coded values inside these payloads (specialty, consent class and so on) resolve against the network's [code lists](coded-values.md).

## Envelope version

The Beckn **core message** version, `context.version`, is `2.0.0`, a constant in the core specification. The domain schema packs are version 2.1; that version appears in their `@context` URLs, not in the envelope.

## Transition types

A deployment should define the set of transition types it uses (for example referral, transfer, enrolment handoff, escalation, programme handoff, field task). SLA rules match on them through `appliesTo.transitionType`.
