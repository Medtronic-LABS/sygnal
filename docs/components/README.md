---
description: The edge tool and network enablement services that Sygnal provides, what each does, and how mature it is.
---

# Components overview

The specification is what makes a network interoperable. The components are what make it **easy to run**. Where Sygnal provides software for a component, it will be an open-source **reference implementation** in the Sygnal Platform, released as it becomes ready. Any implementation that follows the specification can replace any component.

| Component | Layer | What it does | Status |
|---|---|---|---|
| [Edge Adapter](edge-adapter.md) | Edge | Lets a platform join the network: signs, verifies and routes messages; runs SLA (service-level agreement) timers; enforces reporting policy; exports operational telemetry with no message content | Design complete; configuration in use on the Sygnal Sandbox |
| [Network Registry](network-registry.md) | Coordination protocol | Directory of participants: identifiers, keys, addresses, roles | Aligned with the DeDi protocol; uses the hosted dedi.global service today; role recording is an open item |
| [Discovery Service](discovery-service.md) | Coordination protocol | Finds services and providers to hand off to (matched transitions) | Sygnal runs its own instance of Beckn's decentralised discovery service, in use on the Sygnal Sandbox |
| [Policy Manager](policy-manager.md) | Observation, intelligence and policy | Holds, signs and distributes coordination policies; answers `policy/get` | Specified; reference service planned |
| [Deviation & Escalation Platform](deviation-and-escalation.md) | Observation, intelligence and policy | Receives deviation flags, tracks their outcomes (dispositions), runs escalation ladders | Specified; a basic receiver is in use on the Sygnal Sandbox |
| [Network Intelligence](network-intelligence.md) | Observation, intelligence and policy | Observes coordination metadata and telemetry; dashboards; advisory signals | Reporting service and dashboards in use on the Sygnal Sandbox |

See [Status and roadmap](../roadmap.md) for what comes next.

## Principles that apply to every component

* **Metadata only to the network services.** The network services are designed never to receive clinical content (apart from a governed notifiable report). The Edge Adapter enforces this: only fields allowed by the policy's allow-list leave a platform for the network services.
* **Ordinary participants.** The operator of the network services registers and signs like any other participant. There is no privileged channel.
* **Observe and signal, never decide.** Services can flag, escalate and recommend. They cannot block, reroute or override care.
* **Graceful degradation.** If a network service is down, peer-to-peer coordination continues, and edges queue what they would have sent.
* **Replaceable.** A deployment may swap any reference component for its own implementation.

## Who runs what

| Component | Run by |
|---|---|
| Edge Adapter | Each participating platform, or a hosting partner on its behalf |
| Network Registry, Discovery Service | The network facilitator, or reused from shared infrastructure such as a hosted DeDi registry |
| Policy Manager | The network facilitator, on behalf of governance |
| Deviation & Escalation Platform, Network Intelligence | The network facilitator |

One organisation can operate all the shared services for a network. They are separate components, so they can also be operated, scaled or replaced independently.

## Run it yourself, or use the hosted services

A network can run every shared component itself, using any implementation of the specification. This includes the **Sygnal Platform** once it is released. Or a network can use **Sygnal Network Services**, where the shared components are hosted and operated for it, currently by Medtronic LABS. The hosted services sit on the control plane, so they handle coordination metadata only, never patient records. A network can replace them at any time, and participants do not need to change their integration. See [Protocol, platform and services](../concepts/protocol-platform-services.md).
