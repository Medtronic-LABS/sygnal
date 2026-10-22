---
description: Holds, signs and distributes coordination policies on behalf of governance.
---

# Policy Manager

The **Policy Manager** is how governance's rules reach the edge. It holds the network's [coordination policies](../concepts/policies.md) and signs them with a `GOVERNANCE`-role identity. It sends them to the edges in scope, and answers edges that ask which policies apply to them.

## Responsibilities

| Responsibility | Through |
|---|---|
| Store versioned policies: network-wide and scoped to jurisdiction, programme or facility | Internal store |
| Sign and push new or revised policies to the edges in scope | `sygnal/policy/update` |
| Record each edge's adoption (`APPLIED` or `REJECTED`, with a reason) | `sygnal/policy/on_update` |
| Serve the applicable policy set to an edge on bootstrap or after a missed push | `sygnal/policy/get` → `on_get` |
| Expose policy state to Network Intelligence, for example SLA windows and metric definitions | Internal interface |

## What a policy carries

* **Reporting:** which coordination events the edge emits, the metric catalogue, the area code system, how often to report (cadence), and the data-minimisation allow-lists.
* **SLAs (service-level agreements):** for example "emergency referrals must be acknowledged within 2 hours, by the receiving party".
* **Instrumentation:** how much operational telemetry adapters send.
* **Precedence:** how overlapping policies resolve on this network.
* **Network extensions:** extra section types defined by the network.

## Design notes

* **Policies are data, not code.** Policies are signed JSON-LD documents. Any edge can enforce them without a policy engine, and officials can compare two versions line by line (review a diff).
* **Every edge enforces the rule that policies can only narrow.** No policy can widen what a higher level allows to leave the edge.
* **Edges cache policies** and keep applying the last known good policy when offline.
* **The protocol does not cover authoring and approval.** A network may put any drafting, consultation and sign-off workflow in front of the Policy Manager.
* Coordination policy is **not** clinical guidance. Clinical protocols and decision support stay in the edge platforms.

## Protocol, platform and network services

| Protocol | Platform | Network Services |
|---|---|---|
| `policy/update`, `policy/get`, `CoordinationPolicy` | Reference service (planned) | Planned |

See [Protocol, platform and services](../concepts/protocol-platform-services.md).

## Status

{% hint style="info" %}
**Specified; reference service planned.** The policy format, precedence and distribution APIs are defined in the v0.9 specification. On the [Sygnal Sandbox](../build/sandbox.md), SLA rules are loaded from configuration in the policy format.
{% endhint %}
