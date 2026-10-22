---
description: The ideas you need to read the rest of the documentation.
---

# Concepts at a glance

| Concept | In one line | Read |
|---|---|---|
| **Care Coordination Network** | Independent health platforms joined by a shared protocol, a registry and a few shared services, so that any participant can coordinate with any other. | [Care Coordination Networks](care-coordination-networks.md) |
| **Two planes** | Handoffs travel peer to peer between participants. The shared services see coordination metadata only. | [Architecture](architecture.md) |
| **Transition** | A handoff of responsibility (referral, task, follow-up), carried as a Beckn contract between two participants. | [Coordination model](coordination-model.md) |
| **Counter-party principle** | The party that is waiting for something reports when it doesn't happen. Reporting is silent by default. | [Deviations and escalation](deviations-and-escalation.md) |
| **Report in, signal out** | Edges report coordination metadata as the policy permits; the network replies only with advisory signals. | [Reporting and signals](reporting-and-signals.md) |
| **Coordination policy** | Signed, versioned configuration (reporting, service-level agreements or SLAs, instrumentation, precedence) that governance publishes and edges enforce. | [Coordination policies](policies.md) |
| **Data minimisation** | Policy sets, field by field, what may leave an edge. When policies combine, the most restrictive result always wins. The edge enforces it. | [Privacy and data minimisation](privacy-and-data-minimisation.md) |
| **Trust** | A registered participant signs every message. The network services have no privileged channel. | [Trust and security](trust-and-security.md) |
| **Consent** | Consent travels with the referral, with three classes: explicit-mediated, treatment-relationship and deemed. | [Consent](consent.md) |
| **Protocol, platform and services** | An open protocol; open-source software that implements it (being prepared for release); and hosted, metadata-only services that run it for a network. | [Protocol, platform and services](protocol-platform-services.md) |
| **Complementary DPI** | Sygnal sits above the digital public infrastructure (DPI) for identity, records and discovery, and below clinical systems. | [Sygnal and other health DPI](relationship-to-other-dpi.md) |

**The guiding rule:** the centre observes and signals; it never decides. Clinical decisions stay at the edge, with the health worker and the clinician.
