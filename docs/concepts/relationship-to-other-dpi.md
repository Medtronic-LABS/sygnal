---
description: Sygnal sits above identity, records and discovery, and below clinical systems. Complementary, not competing.
---

# Sygnal and other health DPI

Health systems have built shared digital layers, often called digital public infrastructure (DPI), for **identity** (who is this person?), **records** (what happened to them?) and **discovery** (who can provide this service?). The missing layer is **coordination**: making sure the next step happens, across providers, over time. Sygnal fills that gap. It sits **above** identity, records and discovery, and **below** the clinical platforms.

| Layer | Answers | Examples | Relationship to Sygnal |
|---|---|---|---|
| Clinical platforms | What care to give | EMRs, hospital systems, community health worker apps | The **edges** Sygnal connects. They keep clinical logic and data. |
| **Coordination** | **Did the next step happen?** | **Sygnal** | — |
| Discovery and booking | Who can provide this, and when? | Beckn-based networks, such as India's Unified Health Interface (UHI) | Sygnal **uses** discovery for matched handoffs: "find and book", then "coordinate, follow through and observe". |
| Records and exchange | What happened to this person? | Health information exchanges, OpenHIE-based mediators, FHIR servers | Clinical records move here, never through Sygnal's shared services. |
| Identity | Who is this person? | National and health IDs | Reconciliation happens here at the point of care. Identity travels peer to peer where a handoff needs it; the shared services carry pseudonymous references at most. |

## Beckn Protocol

Sygnal is built **on** [Beckn Protocol v2](https://github.com/beckn/protocol-specifications-v2), an open protocol for decentralised networks of seekers and providers.

* **Reused:**
  * unchanged: the Beckn transaction verbs (`discover` to `cancel`), the generalised contract model and the async-ACK transport (an immediate "received" reply, with the result sent later);
  * as the base, which Sygnal may extend: the signing and trust model;
  * the DeDi-based directory and decentralised discovery;
  * the ONIX adapter, as the foundation of the Sygnal Edge Adapter.
* **Profiled:** a health handoff is a *profile* of the Beckn contract, carried with existing Beckn health and service schema packs.
* **Extended:** Sygnal adds APIs built for coordination where Beckn has no equivalent: escalating deviations, policy-governed reporting, governance policy distribution, shared plans and advisory signals. These live in their own `sygnal/` namespace, so nothing collides with core Beckn.

Any Beckn-capable platform is most of the way to joining a Sygnal network. See [Transitions on Beckn](../specification/transitions-on-beckn.md), and [Related specifications](../reference/related-specifications.md) for every upstream specification, schema pack and version Sygnal uses.

## FHIR

Sygnal doesn't replace FHIR. The two work at different layers. Clinical exchange between providers stays in FHIR, over the records layer. Each Sygnal resource states how it aligns with FHIR, so platforms built on FHIR can map to it consistently:

| Sygnal resource | FHIR alignment |
|---|---|
| Transition (the handoff contract) | ServiceRequest + Task |
| `CoordinationEvent` | AuditEvent |
| `DeviationReport` | DetectedIssue *(provisional)* |
| `SharedPlan` | CarePlan, as a hashed reference only |
| `Signal` | Communication |
| `CoordinationPolicy` | Sygnal-native configuration; no FHIR clinical resource fits |

## OpenHIE and central interoperability layers

Some architectures route every exchange through a mandatory central interoperability layer. That is a successful pattern for record exchange. Sygnal deliberately does **not** do this for coordination. A central layer in every workflow becomes a single point of failure, a concentration of sensitive data, and a gatekeeper on participation. Instead, Sygnal limits the centre to a directory and a set of metadata-only services, and lets coordination run peer to peer. The two coexist: a health information mediator can be the records layer beneath a Sygnal network.

## Analogous infrastructure

The pattern is familiar from other domains:

* payment networks such as India's Unified Payments Interface (UPI), where the switch doesn't see what was bought;
* government data exchanges such as Estonia's X-Road, which connect systems without centralising data;
* open commerce networks built on Beckn.

Sygnal applies the same design to health coordination.
