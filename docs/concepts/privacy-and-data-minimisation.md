---
description: How "clinical data stays at the edge" is enforced by the protocol and its implementation, not promised in a policy document.
---

# Privacy and data minimisation

Sygnal builds its privacy guarantees into the protocol and its reference implementation. They are not a policy promise added on top. (Where a reference component is still being built, the rules below are the requirements it must meet; see each component's status.) This page explains what reaches the network services, what never does, and how that boundary is enforced.

## What reaches the network services, and what never does

| Can reach the control plane | Never does |
|---|---|
| Event type: referral placed, accepted, completed | Diagnoses, except the condition code in a governed notifiable report |
| Timestamps and participant identifiers (platforms, not people) | Clinical notes |
| Coded reasons, such as a deviation reason code | Lab results or vital-sign readings |
| Aggregate counts for a stated period and coded area | Names or identifiers that unlock the record |
| Hashed references: a pseudonymous subject reference, or a commitment to an artefact held at the edge | Free text about a patient |
| For notifiable conditions only, a limited set of fields with a legal basis | Anything that identifies an individual in a handoff both sides agree went as expected (it counts only in aggregates) |

The **peer-to-peer plane** is different. A handoff between two authorised parties carries the context the receiving side needs to act on. See [Two planes](architecture.md#two-planes).

## What may travel peer to peer

Sygnal's position on patient information, by kind of interaction:

1. **Any Sygnal interaction that is not peer to peer never carries personal or clinical data about a patient.** This covers everything sent to or from the network services: deviations, reports, signals and policies. The one governed exception is [reporting of notifiable conditions](#the-exception-for-notifiable-conditions). It carries a bounded set of fields under a stated legal basis.
2. **Where a health information exchange exists, point to it.** A handoff should carry a pointer to the record held in the exchange, not the record itself.
3. **Coordination-specific information may travel peer to peer.** The handoff between the two parties may carry what makes the referral possible, such as the referral note, coded reason and urgency. Encrypting that payload to the receiver's registered key is **recommended**, on top of TLS (the standard encryption of the connection). It also protects the content in intermediaries, logs and queues. It is not mandated.
4. **Health records beyond referral-enabling information should be shared outside the Sygnal network**, over the health system's records layer.
5. **Networks should define their own policy** for these elements: what may travel peer to peer, whether payload encryption is required, and which records layer to point to.

## How it is enforced

**1. Content is excluded at the edge, before anything leaves.** The edge adapter turns an event (a referral, a visit, a completed task) into a coordination message that carries only metadata. Clinical detail is never packaged for the control plane, so there is nothing to strip out later.

**2. Trust runs on signatures, not disclosure.** Both sides of a handoff sign what they sent and received. Matching signatures show that both agree it happened, without either side handing a record to the network.

**3. Silence is the default.** While both sides agree, nothing that identifies an individual reaches the network services. Only a mismatch, an unexplained gap, an aggregate the policy permits, or a governed notifiable report ever leaves.

**4. What may leave is set by policy, field by field.** The reporting policy's `dataMinimization` is the single source of truth. Its allow-lists are JSONPath expressions that the **edge** evaluates against its own outgoing events. The receiver **must** refuse a report that carries anything outside the allow-list (`403`).

**5. Policies can only narrow.** When several policies apply, data minimisation always merges to the most restrictive result. See [the narrowing invariant](policies.md#policies-can-only-narrow).

**6. The network never queries.** There is no search or filter API on the network services. The read APIs resolve by reference: `deviation/get` and `plan/get` return a single record, and `policy/get` returns the policies that apply to the requesting edge. Dashboards query the services' own stores, which hold only what was reported under policy.

## Aggregates

Aggregate reporting is the default and covers most needs. An aggregate `CoordinationEvent`:

* covers a stated **`period`** (an ISO 8601 interval) and a coded **`area`** (codes only, never free text or coordinates);
* carries **`metrics`** whose keys must be codes defined in the policy's `metricDefinitions`. An unknown code is refused;
* reports **counts, never rates**. Edges send numerator and denominator as two counts, so the network can add them up again across facilities and districts;
* has an `id` and a `revision`, so a late correction from an edge that was offline replaces the earlier figure instead of being double counted.

**Small cells.** No single field identifies anyone, but combinations can. "Measles, area X, week 32: 1 case" can point to one household in a small village. The policy's `minCellSize` (recommended: 5) tells the edge to suppress any value below the threshold, or roll it up to a coarser area or a longer period. The edge should also suppress a second value if someone could work out the hidden one by subtraction.

## The exception for notifiable conditions

For a named set of **notifiable conditions** (for example tuberculosis, measles or cholera), a policy can permit individual-level reporting. It is explicit and bounded:

* `appliesToConditions` names the conditions;
* `allowedFields` is a bounded allow-list of fields, set per health system as the minimum needed to triage and what notification law requires;
* `legalBasis` cites the mandate;
* a pseudonymous `subjectRef` may be included if the policy permits it.

This is the one place Sygnal may carry more than a hash. Governance draws this line on purpose, and keeps it minimal and auditable.

{% hint style="info" %}
**Direction of travel: notifiable reporting by reference.** One proposal, still open, is that a notifiable event would carry only metadata, the triage fields and a **reference**. The full record would stay at the edge. An authorised public-health participant would fetch it through a signed, role-checked read. This moves control from send time (what leaves) to access time (who reads it, and why). See [Open questions](../reference/open-questions.md).
{% endhint %}

## Two channels, both content-free

Operational telemetry (message counts, response times, ACK/NACK replies that confirm or reject receipt, and timeouts) travels separately from coordination events and **never** carries payload content. The reference setup enforces this in three places: the adapter's selective audit logging, which exports only the fields on the network's allow-list (the message header and coordination metadata such as service type, urgency, status and attendance); the network's collector, which keeps only those audit records and strips signatures; and the network's reporting service, which applies the allow-list again before storing anything. See [Reporting and signals](reporting-and-signals.md#two-channels-coordination-events-and-network-telemetry).

## Identifiers

* `transactionId` and `messageId` must be random UUIDs, never derived from a patient or household identifier.
* Pseudonymous subject references need care. A plain hash of a small-space identifier, such as a phone number or a national ID, can be reversed by hashing every candidate. Linking records across programmes therefore calls for a **keyed** hash. The key is shared among edges and never held by the network services. The hashing scheme is an [open question](../reference/open-questions.md).

## Remaining risks

* **Re-identification from metadata patterns.** Even without identifiers, sequences of visits and timings could identify someone in a small population. `minCellSize`, coarse areas and aggregate-by-default reporting reduce this risk. They do not eliminate it.
* **Open extension fields.** Typed `*Attributes` extensions on some resources (not on `CoordinationEvent`) are open by design. Networks that define them should keep them coded and free of personal information.
