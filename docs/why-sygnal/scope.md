---
description: The boundaries that keep Sygnal a coordination layer, not a clinical system.
---

# What Sygnal does and does not do

Sygnal's boundaries are a design choice. They keep it a coordination layer that any health system can adopt, rather than another clinical platform. The table below lists what Sygnal does on the left and what it deliberately does not do on the right.

| Sygnal **does** | Sygnal **does not** |
|---|---|
| **Facilitate coordination at the edge.** A lightweight adapter plugs into whatever a platform already runs, and carries coordination events (referrals, follow-ups, tasks) as they happen. | **Transmit or store clinical content in its shared services.** Clinical notes, lab results and diagnoses never reach the network services. The one exception is a condition code in a governed notifiable report. The adapter reads clinical content locally, and only to work out the coordination event. Where a record must move between providers, it moves over the health system's own health information exchange. |
| **Compare events against the configured rules.** Each handoff is checked against the SLAs (service-level agreements: agreed time limits) and coordination rules the health system has set, so a missed step is caught when it happens, not months later in review. | **Make clinical decisions.** Judging or recommending a treatment is out of scope by design. It stays with the provider. |
| **Stay silent by default.** When both sides of a handoff agree that it went as expected, nothing that identifies anyone is reported. At most, it counts towards an aggregate total that the policy permits. Silence is the normal state, not a pending alert. | **Report routine individual records centrally.** Only a mismatch, an unexplained gap, or an aggregate the reporting policy permits ever becomes visible to the shared services. |
| **Signal the accountable role.** When a deviation is detected, Sygnal flags the responsible platform and names the role accountable for closing it, as the policy defines. The platform resolves that role to an actual person. | **Hold anyone's identity centrally, or decide who gets referred where.** Sygnal's shared services never hold an individual's identity. Identity travels only peer to peer, between the two parties to a handoff. Discovery can suggest candidate providers, but the platform or a person always makes the choice. |
| **Support SLAs and escalation ladders.** If nobody acts within an agreed time window, the flag climbs to the next level, so nothing sits unresolved indefinitely. | **Turn coordination signals into clinical advice.** What Sygnal shows is always a signal about coordination, such as a gap or a delay. It is never a clinical recommendation dressed up as one. |
| **Degrade visibly, not silently.** When connectivity is weak or intermittent, coordination continues peer to peer, events queue locally, and connectivity gaps are flagged to operators. | **Block care if the network drops.** Clinical work never waits on Sygnal's uptime. |
| **Adopt incrementally, one use case at a time.** A health system can start with referral tracking and add shared care plans later, proving value at each step. | **Require a single go-live for everything.** Nothing has to switch over all at once. |
| **Stay open and replaceable.** At its core Sygnal is an open specification. Its components (the edge adapter and the network services) are reference implementations that you can adopt, replace or build yourself. | **Lock you in.** No single vendor is meant to own the standard. Stewardship is intended to move to a neutral governance body (see [Network governance](../governance/README.md)). |

## Two planes

Two kinds of movement happen on a Sygnal network, and the design keeps them apart:

* **The peer-to-peer plane.** A handoff between two providers travels **directly between them**. It carries what the handoff needs: that it happened, and the context the receiving side must act on, such as a coded reason for referral, an urgency tier, or a pointer to a note held in the records layer. This is a direct, signed, consented exchange between the two parties who are already coordinating this patient's care.
* **The control plane.** The shared network services (registry, discovery, policy, deviation and escalation, network intelligence) deliberately receive far less: **coordination metadata, never clinical content** (the one exception is a governed notifiable report, described in [Privacy and data minimisation](../concepts/privacy-and-data-minimisation.md#the-exception-for-notifiable-conditions)). Examples are event types, timestamps, participant identifiers, coded reasons, pseudonymous references and tamper-evident fingerprints.

See [Architecture](../concepts/architecture.md) and [Privacy and data minimisation](../concepts/privacy-and-data-minimisation.md) for how this is enforced.
