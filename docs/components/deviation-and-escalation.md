---
description: Receives deviation flags, tracks them to a disposition, and climbs the escalation ladder when they stay open.
---

# Deviation & Escalation Platform

The **Deviation & Escalation Platform** is the network's safety net for broken promises. A participant may raise a deviation that needs attention beyond the two parties to a handoff. The platform records it, tracks it until it has a recorded outcome (a disposition), and escalates it if it stays open.

## Responsibilities

| Responsibility | Through |
|---|---|
| Receive third-party deviations from supervisors, and counter-party deviations that a reporter escalates beyond its counter-party | `sygnal/deviation/flag` |
| Verify that the reporter is entitled to raise the flag (a party to the transition, or a `SUPERVISOR`) | Role authorization |
| Return and update the disposition | `sygnal/deviation/on_flag`, including later unsolicited updates |
| Run the escalation ladder: structured inquiry, then human escalation, then governance alert | Escalation rules from policy (`onBreach.escalationTier`) |
| Provide worklists to the accountable role: a supervisor, a district officer, a programme manager | Role-based views (metadata only) |
| Keep the signed evidence needed to settle transmission disputes | Signed requests and acknowledgements; `evidenceHash` |
| Answer reconciliation requests | `sygnal/deviation/get` → `on_get` |
| Share deviation metadata with Network Intelligence | Internal interface |

## Design notes

* **Deviations come from the edge.** The platform records what participants raise. It does not infer deviations about individual handoffs, because it can't see them. Network-level patterns, such as many unacknowledged referrals at one facility, are Network Intelligence's job.
* **Coded only.** Escalated deviations carry coded reasons, participant identifiers, timestamps and hashes. No free text about patients.
* **Advisory.** Escalation tiers and recommended actions are advisory. People decide what to do.
* **Clinical disputes are out of scope.** Disputes about whether a message was sent and received can be settled from signed evidence. Disputes about clinical appropriateness go to the designated clinical arbiter, who accesses clinical details through the records layer, not through this platform.
* **Power asymmetry.** A small facility may hesitate to flag a large hospital. Networks can reduce this risk, for example with supervisor-raised flags and aggregate-only views at higher tiers. This is an open governance question.

## Protocol, platform and network services

| Protocol | Platform | Network Services |
|---|---|---|
| `deviation/flag`, `deviation/get` | Reference service (planned) | Basic receiver on the Sygnal Sandbox |

See [Protocol, platform and services](../concepts/protocol-platform-services.md).

## Status

{% hint style="info" %}
**Specified; a basic receiver is in use on the [Sygnal Sandbox](../build/sandbox.md).** On the sandbox, a reporting service records `deviation/flag` messages. A stand-in SLA (service-level agreement) agent raises time-based flags on behalf of waiting participants. In the target design, each adapter runs its own SLA timers instead. The reference platform, with dispositions, escalation ladders and worklists, is planned.
{% endhint %}
