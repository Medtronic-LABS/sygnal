---
description: The thin layer that lets any platform join a Sygnal network without rebuilding itself.
---

# Edge Adapter

The **Sygnal Edge Adapter** is what lets an existing platform join a Care Coordination Network. It sits beside the platform and speaks the protocol on its behalf. The platform keeps doing its own job. It calls the adapter to send a handoff, and the adapter sends callbacks back to it.

Without an adapter, every EMR vendor, community-health app and hospital system would have to build the same things on its own: signing, registry lookups, asynchronous callbacks, SLA (service-level agreement) timers, policy enforcement and offline queuing. That is unrealistic, and the results would always be inconsistent. **The adapter does more than any other component to make adoption possible.**

## What it does

| Function | Description |
|---|---|
| **Signing and verification** | Signs every outbound message with the platform's registered key; verifies inbound signatures against the registry; signs every acknowledgement |
| **Routing** | Resolves counterparts' addresses from the registry and delivers requests and callbacks point to point |
| **Schema validation** | Validates Beckn and Sygnal payloads against the published schemas |
| **Transitions** | Carries Beckn `discover` → `confirm` → `status`/`update`/`cancel` flows between the platform and its counterparts |
| **SLA timers** | Tracks outstanding commitments against the policy's SLA rules and tells the platform when one is breached, so the platform can decide whether to raise `deviation/flag`. The adapter never escalates on its own. |
| **Policy enforcement** | Applies the active coordination policy, so that only allow-listed fields leave in `event/report` and telemetry stays at the policy's instrumentation level |
| **Network telemetry** | Exports operational metrics with no message content (counts, ACK/NACK "received"/"rejected" replies, latencies, timeouts, SLA breaches) to the network's telemetry endpoint |
| **Resilience** | Queues messages locally when connectivity or the network services are unavailable, and sends them later. It never makes the platform wait or slow down. |

## Built on Beckn ONIX, and beyond it

Sygnal **uses [Beckn ONIX](https://github.com/beckn/beckn-onix)**, Beckn's open-source network adapter, as the foundation of its Edge Adapter. The Sygnal Edge Adapter builds on top of ONIX. It inherits ONIX's signing, registry integration, schema validation, routing and OpenTelemetry support, and it tracks the latest ONIX release. It adds:

* the Beckn health schema packs and the Sygnal API specification;
* routing rules for the `sygnal/*` actions;
* header-only, selective audit logging, so payload content never leaves the edge in logs;
* telemetry export through a local collector that applies the allow-list again before anything is sent;
* plugins for callback latency, callback timeouts, SLA breaches and live policy updates;
* onboarding tooling: key generation, registry record generation, and a health-check ("doctor") script.

A platform that already runs ONIX, for example from the Beckn starter kit's generic devkit, can move to the Sygnal Edge Adapter mostly by configuration.

**Built to outlast any one foundation.** The Sygnal Edge Adapter is defined by what it must do (the functions above and the Sygnal specification), not by ONIX. Sygnal's additions are kept as separable plugins and configuration, so the adapter can follow ONIX as it evolves, or move to another foundation if ONIX's direction or support changes.

## Deployment modes

| Mode | How it works | Best for | Available |
|---|---|---|---|
| **Sidecar** | A separate service beside the platform; the platform calls it over local HTTP | Most existing platforms that can make HTTP calls | **Today**, with Beckn ONIX |
| **Shared (proxy)** | One adapter at facility or district level, serving several basic systems or human operators | Low-maturity settings; a first step for facilities without a capable system | Planned |
| **Embedded** | Protocol handling built into the platform as a library | Platforms that want the tightest integration | Being explored |

## What leaves the edge through the adapter

Every message a platform sends to the network goes through its adapter.

| Going to | What goes through the adapter | Content |
|---|---|---|
| **Another participant** (peer to peer) | Beckn handoffs, status updates, in-band deviations, `deviation/flag` between the parties | What the handoff needs, signed |
| **Discovery Service** | `discover` | Search terms and filters, never patient details |
| **Network services** | Escalated `deviation/flag`, `event/report`, `policy/get` | Coded coordination metadata, filtered by policy |
| **Network telemetry** | Operational counts and timings | No message content at any level |

## Protocol, platform and network services

| Protocol | Platform | Network Services |
|---|---|---|
| Beckn transport and trust; Sygnal APIs and conventions | Built on open-source Beckn ONIX; Sygnal edition being prepared for release | Not hosted: runs beside each platform, or with a hosting partner |

See [Protocol, platform and services](../concepts/protocol-platform-services.md).

## Status

{% hint style="info" %}
**Design complete; configuration in use on the [Sygnal Sandbox](../build/sandbox.md).** Participants on the sandbox run ONIX with Sygnal configuration (health schema packs, selective audit logging, OpenTelemetry export). That configuration is published in the repository's [`adapter-config/`](https://github.com/Medtronic-LABS/sygnal/tree/main/adapter-config) folder. The packaged Sygnal edition and its plugins are planned. Known gaps being addressed:

* falling back to the registry address when a message carries no callback URI;
* role authorization checks, which can be configured through ONIX's policy-checker plugin;
* validation of `sygnal/*` actions alongside the Beckn core schema.
{% endhint %}

Step-by-step onboarding guidance will be published with the packaged Sygnal Edge Adapter.
