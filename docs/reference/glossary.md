---
description: Terms used across the Sygnal documentation.
---

# Glossary

**Adapter (Edge Adapter).** The layer that sits beside a platform and speaks the protocol for it. It signs and routes messages, runs service-level agreement (SLA) timers and enforces policy. See [Edge Adapter](../components/edge-adapter.md).

**Aggregate reporting.** Reporting counts for a period and area, with no identifiers. This is the default reporting mode.

**Async ACK.** A message pattern with two replies. The receiver first sends back a signed acknowledgement (ACK), the immediate "received" reply. The actual result follows later as a separate signed callback.

**Beckn Protocol.** An open protocol for decentralised networks of seekers and providers. Sygnal builds on Beckn v2 for handoffs, trust and the registry.

**Care coordinator.** The participant that holds a referral (T1) and arranges its fulfilment, including any downstream booking (T2).

**Care Coordination Network.** A network of independent health platforms that coordinate care through a shared protocol, registry and services. Sygnal helps make such networks possible.

**CareTransition.** The health profile of a Beckn contract. It represents a handoff of responsibility from one party to another.

**Control plane.** The shared network services, and the messages sent to and from them. These messages carry metadata only. Compare *peer-to-peer plane*.

**Coordination event.** A metadata record of coordination activity (`CoordinationEvent`). Edges report it through `event/report`, as policy allows.

**Coordination policy.** Signed, versioned settings (`CoordinationPolicy`) that governance issues. It has typed sections for reporting, SLAs, instrumentation and precedence.

**Counter-party principle.** The party that is waiting for something reports when it doesn't happen. If nothing goes wrong, nothing is reported.

**Critical section.** A policy section marked `critical: true`. An edge that doesn't recognise it must reject the whole policy.

**Data minimisation.** The policy's rules, field by field (`dataMinimization`), for what may leave an edge. When rules combine, the strictest rule always wins.

**Deviation.** A handoff that does not go as expected. The two parties either record it in their own messages to each other, or raise it with `deviation/flag`.

**Directed transition.** A handoff where the receiver is known in advance, so there is no discovery step. Compare *matched transition*.

**Edge platform.** An existing system where care happens, such as an EMR, a hospital system or a community health worker app.

**Escalation tier.** An advisory step on the escalation ladder: 1 is a structured inquiry, 2 is human escalation and 3 is a governance alert.

**HashRef.** A hashed reference to something that stays at the edge. It can stand for a plan or a piece of evidence without revealing it, or refer to a person under a pseudonym.

**Health system.** The system of care a Sygnal network serves. It can be national, regional, programme-level or a private provider network. A national health system is often itself a collection of many health systems.

**In-band deviation.** A deviation that the two parties to a transaction record in the referral's own `deviation` field.

**Matched transition.** A handoff where the receiver must first be found through discovery.

**Network facilitator.** The organisation that operates a network's shared services. It is an ordinary registered participant.

**Network telemetry.** Operational metrics about exchanges: counts, response times, ACK/NACK replies and timeouts. They travel on a separate channel from coordination events and never include message content.

**Notifiable-condition exception.** A narrow exception, with a legal basis, that allows reporting about individuals for named notifiable conditions.

**Peer-to-peer plane.** Handoff messages that travel directly between two participants. Compare *control plane*.

**Records layer.** The systems a health system uses to exchange clinical records, such as a health information exchange or FHIR services. It sits beneath Sygnal.

**Referral ID.** The coordination ID given to a referral (T1) at `on_confirm`. It stays the same for the whole episode, including any escalation.

**Role.** A participant's function in a given exchange: `SEEKER`, `PROVIDER`, `SUPERVISOR`, `GOVERNANCE` or `OBSERVER`.

**Seeker / provider.** Beckn's general roles: the party that wants an outcome and the party that provides it.

**Signal.** An advisory message (`Signal`) from Network Intelligence to an edge, sent with `signal/emit`.

**SLA rule.** A coordination service-level rule (`SlaRule`). It names a start message, a stop message, a time window and the role that is waiting.

**Sygnal Network Services.** The shared network components (registry, discovery, deviation tracking, reporting and intelligence), hosted and run for a network to make adoption cheaper. They handle metadata only. See [Protocol, platform and services](../concepts/protocol-platform-services.md).

**Sygnal Platform.** The reference software that implements the Sygnal Protocol: the Edge Adapter and the components that run a network. It is being prepared for open-source release.

**Sygnal Protocol.** The open Sygnal specification: coordination APIs, schemas, code lists, conventions and trust profile.

**T1 / T2.** The two transactions in a referral: the coordination contract (T1) and an optional downstream booking (T2).
