---
description: Where implementers start, depending on what you are building.
---

# Getting started

## Pick your path

| You are… | Start with |
|---|---|
| **A platform vendor or implementer** connecting an EMR, community health app or hospital system | The [Sygnal Sandbox](sandbox.md), the [Edge Adapter](../components/edge-adapter.md) and [Running the reference flows](running-reference-flows.md). Step-by-step onboarding guidance and an implementer checklist will be published with the first Sygnal Platform components. |
| **A developer** who wants to see the actual messages sent between platforms | [Running the reference flows](running-reference-flows.md) and the [Use cases](../use-cases/README.md) |
| **A network operator** setting up the shared services | [Protocol, platform and services](../concepts/protocol-platform-services.md), the [Components overview](../components/README.md) and [Network governance](../governance/README.md) |
| **Someone reviewing or extending the specification** | [Specification overview](../specification/README.md) and [Contributing](../reference/contributing.md) |

## What you need to know first

1. **Handoffs are Beckn.** If your platform can already act as a Beckn seeker or provider, you are most of the way there. See [Transitions on Beckn](../specification/transitions-on-beckn.md).
2. **Everything is signed and asynchronous.** Expect an immediate signed ACK (a "received" reply), then a signed callback. See [Conventions](../specification/conventions.md).
3. **Clinical content stays with you.** The network services get coordination metadata only, as policy permits. Your adapter enforces this. See [Privacy and data minimisation](../concepts/privacy-and-data-minimisation.md).
4. **You raise deviations when you are the one waiting.** Run SLA (service-level agreement) timers for the commitments you depend on. See [Deviations and escalation](../concepts/deviations-and-escalation.md).

## Incremental adoption

You don't need to implement everything at once. A sensible order is:

1. **Join** the network: keys, registry record, adapter.
2. **Handoffs:** directed referrals, with status and deviations carried inside the handoff messages (in-band), as in UC1 and UC2.
3. **Deviations:** raise `deviation/flag` when a step you are waiting for is overdue, and handle `on_flag` outcomes (dispositions).
4. **Policies (when the network has them, at any point from here):** accept `policy/update`, fetch with `policy/get`, and apply the shared SLA rules and data rules. See [Starting without encoded policies](../concepts/policies.md#starting-without-encoded-policies).
5. **Reporting:** send aggregate `event/report` and export network telemetry. Reporting needs a reporting policy.
6. **Signals:** receive `signal/emit` and turn signals into worklist items for the accountable role.
7. **Matched handoffs** through discovery (as in UC3 and UC4), and **shared plans** where relevant.
