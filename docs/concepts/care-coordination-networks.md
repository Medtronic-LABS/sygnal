---
description: What a Care Coordination Network is, who takes part, and the roles they play.
---

# Care Coordination Networks

A **Care Coordination Network** is a set of independent health platforms that have agreed to coordinate care through a shared protocol. Each platform connects **once**, through an edge adapter. After that it can coordinate with **any** other participant, not only the ones it has built a bridge to. N point-to-point integrations become N connections to one network.

Sygnal is what makes such a network possible. It supplies the specification every participant speaks, the edge tools that let a platform join, and the shared services the network needs to run.

## Who takes part

| Participant | Examples | What it does on the network |
|---|---|---|
| **Edge platforms** | Community health worker apps, primary-care EMRs, hospital management systems, campaign platforms, labs, pharmacies | Initiate and fulfil handoffs; raise deviations; report coordination metadata as policy permits; receive advisory signals |
| **Network facilitator** | The organisation that operates a network's shared services | Runs the [network enablement services](../components/README.md). It is an **ordinary registered participant**, with no privileged channel. |
| **Governance** | A ministry of health, a programme, a regional health authority, a network's governing body | Issues signed coordination policies; sets participation and certification rules |
| **Oversight parties** | Supervisors, programme managers, public-health authorities | Raise third-party deviations; receive escalations and signals |

A health worker is **not** a participant. Workers act through the platforms they use. One worker may use a campaign app in the morning and a clinical app in the afternoon; the handoff between those two platforms is what crosses the network.

## Roles on the network

Every message is sent by a registered participant acting in a **role**. The registry records each participant's roles, and every receiver checks them (see [Trust and security](trust-and-security.md)).

| Role | Meaning | Typical actions |
|---|---|---|
| `SEEKER` | Seeks an outcome on behalf of a person, for example the referrer in a referral | Beckn `discover`/`select`/`init`/`confirm`; `deviation/flag` as counter-party |
| `PROVIDER` | Provides the outcome, for example the receiving facility or the care coordinator | Beckn `on_*` callbacks; `deviation/flag` as counter-party |
| `SUPERVISOR` | Oversight party that can assert a discrepancy it observed | `deviation/flag` in third-party mode |
| `GOVERNANCE` | Issues coordination policy | `policy/update` |
| `OBSERVER` | Watches network-level coordination metadata and sends advisory signals | `signal/emit` |

Roles are **per transaction**. The same platform can be the seeker in one handoff and the provider in the next. For example, a campaign platform refers a child upward to a clinical system, and the clinical system later contracts a field task back to the campaign platform.

## Networks are plural

There is no single global Sygnal network. Each health system, whether national, regional, a programme or a private provider network, can run its **own** network on the same open specification. Each network is identified by a `networkId` and has its own registry, policies and governance. A participant can belong to more than one network.

### A network of networks

Large and diverse health systems rarely fit one network. A national health system, for example, is often a collection of many health systems: it may have networks per state or region, separate programme networks (for example maternal health or tuberculosis), and private provider networks, while patients move between all of them. Sygnal networks are meant to be able to **interact with each other**, forming a **network of networks**:

* **Cross-network handoffs.** A participant on one network can hand off to a participant on another, for example a district referral network passing a patient to a tertiary hospital network in another region.
* **Shared or bridged discovery.** One network's Discovery Service can find services published on a linked network.
* **Trust across networks.** Registries can recognise each other's participants, so signatures and roles can be verified across the link.
* **Policy at the boundary.** Each network keeps its own policies and governance. What crosses the link follows the stricter of the two, consistent with the [rule that policies can only narrow](policies.md#policies-can-only-narrow).
* **A picture of the whole.** Network Intelligence on each network can share policy-permitted aggregates upward, giving a view of the wider health system, such as a regional or national view, without centralising any records.

Payment and telecom networks follow the same pattern: they interconnect, but each one is still operated independently.

{% hint style="info" %}
**Being designed.** Today each network is self-contained, and a participant can join several networks. The mechanisms for linking networks (cross-network addressing, registry trust, policy at the boundary) are an [open question](../reference/open-questions.md#network-of-networks).
{% endhint %}

## What makes a network work

1. **A shared language:** the [Sygnal specification](../specification/README.md), built on Beckn Protocol v2.
2. **A way in for every platform:** the [Edge Adapter](../components/edge-adapter.md).
3. **A directory of who's who:** the [Network Registry](../components/network-registry.md).
4. **A way to find the right counterpart:** the [Discovery Service](../components/discovery-service.md).
5. **Rules everyone follows:** coordination policies issued through the [Policy Manager](../components/policy-manager.md).
6. **A safety net for broken promises:** the [Deviation & Escalation Platform](../components/deviation-and-escalation.md).
7. **A view of the whole:** [Network Intelligence](../components/network-intelligence.md), built from metadata only.
8. **People who set the rules:** [network governance](../governance/README.md).
