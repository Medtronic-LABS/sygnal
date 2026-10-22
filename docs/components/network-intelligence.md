---
description: The whole-network picture, built from metadata only, and advisory signals back to the edge.
---

# Network Intelligence

**Network Intelligence** gives a health system the view it has never had: where coordination is working and where it is breaking. It is built entirely from coordination metadata and operational telemetry. It never holds a patient's record.

## What it does

| Function | Inputs | Outputs |
|---|---|---|
| **Coordination observation** | `event/report` (aggregates; notifiable cases where policy allows); deviation metadata | Referral completion, time to acceptance, follow-up gaps and coverage, by period, area, programme and participant |
| **Network operations** | Network telemetry from adapters | Message volume, ACK/NACK ("received"/"rejected" reply) rates, latency, timeouts and SLA (service-level agreement) breaches by action and participant; sender × receiver heatmaps; version drift |
| **Detection** | Both of the above, plus SLA definitions from policy | Patterns such as unacknowledged referrals at a facility, a breach rate rising in a district, coverage gaps, or a suspected outbreak cluster |
| **Signalling** | Detections | Advisory `sygnal/signal/emit` to the affected edge: `FOLLOW_UP_DUE`, `UNACKNOWLEDGED_REFERRAL`, `SLA_BREACH`, `COVERAGE_GAP`, `OUTBREAK_SUSPECTED` |

## Who it serves

* **Programme managers and health authorities:** where the cascade breaks, and which facilities or districts need support.
* **Network operators:** whether participants are connected, healthy and on current versions.
* **Edge platforms:** advisory signals that turn into worklist items for the accountable role.

## Design notes

* **Observe and signal, never decide.** Alerts become signals with a stated basis and an advisory recommendation. Nothing at the centre blocks, reroutes or retries traffic.
* **Only what policy permits.** Network Intelligence holds only what edges reported under the active policy. It cannot ask for more; the [reads](../specification/apis/reads.md) are lookups by reference, not queries.
* **Telemetry is authenticated and re-filtered (target design).** The network's telemetry gateway is designed to do three things. It authenticates each participant. It replaces the reported participant identity with the authenticated one, so nobody can report as someone else. It also applies the field allow-list again. Participant authentication is not yet in the sandbox service.
* **Re-aggregation.** Edges report counts, not rates, so figures can be combined across facilities and districts correctly.
* **Small-cell protection.** Edges suppress small counts before sending; dashboards must not reverse that by combining views.

## Protocol, platform and network services

| Protocol | Platform | Network Services |
|---|---|---|
| `event/report`, network telemetry, `signal/emit` | Reporting service and dashboards, being prepared for release | Reporting service and dashboards on the Sygnal Sandbox |

See [Protocol, platform and services](../concepts/protocol-platform-services.md).

## Status

{% hint style="info" %}
**Reporting service and dashboards in use on the [Sygnal Sandbox](../build/sandbox.md).** The sandbox service receives adapter telemetry over OpenTelemetry (OTLP), through a collector that applies the allow-list. The adapter and collector configuration is in [`adapter-config/`](https://github.com/Medtronic-LABS/sygnal/tree/main/adapter-config). It also records `deviation/flag` and `event/report` messages. It provides a care-coordination dashboard (referrals by type, urgency and status; time to acceptance; referral issues) and a network-operations dashboard. Production work planned: participant authentication on the telemetry channel, long-term storage, alert rules, and the signed `signal/emit` sender.
{% endhint %}
