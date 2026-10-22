---
description: Who sets the rules on a Sygnal network, and who stewards the specification.
---

# Network governance

Governance on a Sygnal network works at two levels. **Each network** governs how it runs. **The specification** is stewarded for everyone who uses it.

{% hint style="info" %}
**Setting up a new network?** You don't have to run the shared services yourself. Sygnal Network Services can host the registry, discovery, deviation tracking and reporting for you, so you can start with the [Sygnal Sandbox](../build/sandbox.md) and focus on the rules. You can bring any service in house later. See [Protocol, platform and services](../concepts/protocol-platform-services.md).
{% endhint %}

## Governing a network

Each network (serving a national, regional, programme or private provider health system) has its own governance. Governance **configures the network. It never decides care**.

| Governance decides | Expressed through |
|---|---|
| What coordination metadata may be reported, at what granularity, and which notifiable conditions allow individual reporting, with what legal basis | The `ReportingSection` of coordination policies |
| Coordination service-level agreements (SLAs, the agreed time limits) and escalation tiers | The `SlaSection` |
| How much operational telemetry adapters send | The `InstrumentationSection` |
| How overlapping policies at network, jurisdiction, programme and facility level resolve, and which fields are locked | The `PrecedenceSection` |
| Who may join, in which roles, and what they must demonstrate first | Participation rules; registry roles; certification |
| Who operates the network services | Appointment of the network facilitator |

A `GOVERNANCE`-role participant signs each policy, and the [Policy Manager](../components/policy-manager.md) distributes it. Each network decides how it drafts, consults on and approves its policies.

## Safeguards built into the protocol

The protocol itself answers some governance questions, so that no single actor can override them:

* **The reporting dial can't be turned up from below.** Data minimisation always merges to the most restrictive result. A lower level can narrow what leaves the edge, never widen it.
* **Everything is attributable.** Policies and signals are signed by registered identities, so every rule and every alert has an author.
* **Individual reporting needs a stated legal basis**, and is limited to a named set of conditions and fields.
* **Per-transaction telemetry is allowed only on non-production networks**, and it has an expiry.
* **The centre has no privileged channel.** Edges verify the network services exactly as they verify each other.

## Questions each network must answer

These are not settled by the protocol, and each network should decide them explicitly:

* **Who sets the dial, at which level?** National, regional, district or programme; how to resolve disagreements; and how to make settings public.
* **Preventing misuse of accountability data.** Observation data could be used to punish rather than support facilities or regions. Networks should state how dashboards and escalations are used.
* **Power asymmetry.** A small facility may be reluctant to flag a large hospital. Options include supervisor-raised flags, aggregate-only views at higher tiers, and protection for reporters.
* **Consent.** How Sygnal's coordination consent relates to the health system's existing consent framework.
* **Peer-to-peer content.** What referral-enabling information may travel in handoffs, whether payload encryption is required, and which records layer handoffs should point to (see [What may travel peer to peer](../concepts/privacy-and-data-minimisation.md#what-may-travel-peer-to-peer)).
* **Keys and trust anchor.** Who provisions, rotates and revokes participant keys, and on what root of trust.
* **Sustainability.** Who funds the network services and adapter maintenance.

## Stewarding the specification

Today, **Medtronic LABS** leads the development of the Sygnal specification, in the open and with partners, and develops the reference components. The intent is that **no single vendor owns the standard**. Stewardship is meant to move to a neutral governance body as adoption grows. That body would hold the specification, run certification of adapters and services, and manage protocol evolution, including how changes are proposed, ratified and versioned.

Until then:

* changes are proposed and discussed in the open (see [Contributing](../reference/contributing.md));
* significant design choices are recorded with their context and reasons;
* versions follow [semantic versioning](../specification/changelog.md), and implementations pin released versions.

## Certification

A **conformance suite**, built from the specification's requirements, will let platforms and service implementations demonstrate conformance. Certification of independent adapters is part of the [roadmap](../roadmap.md).
