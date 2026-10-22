---
description: How broken promises come to light. The counter-party principle, in-band and escalated deviations, SLAs and escalation tiers.
---

# Deviations and escalation

A **deviation** is a departure from the expected course of a handoff. Examples are a referral that was never acknowledged, a patient who didn't attend, a provider cancellation, a transport failure, a stock-out, or a field task found not done. Sygnal's trust model rests on finding deviations reliably, without a central system watching every transaction.

## The counter-party principle

For every handoff, the party with the strongest incentive to report a failure is **the one waiting for a response**. Sygnal is built on that observation:

* The **expecting party** runs a service-level agreement (SLA) timer for each outstanding commitment, for example "acceptance due within 2 hours of `confirm`".
* If the expected response arrives, **nothing is reported**. Silence is the normal state.
* If it doesn't arrive in time, the expecting party raises the deviation and attaches its signed evidence.

Nobody is asked to report their own failure. Loss to follow-up becomes visible as a by-product: a handoff with no acceptance **is** a patient who fell through.

## Two ways a deviation travels

### 1. In-band, between the two parties

Within a transaction, a deviation travels on the referral itself, in its built-in `deviation` field on `update` or `status`. It uses existing Beckn verbs. The field is present only when a deviation occurs. It carries **coded** fields only: a reason code, who detected it, and when. Any human note stays in the edge platform. Free text entered in the field is the largest source of accidental disclosure. Keeping it out of the message builds privacy into the structure. (The upstream `deviation` schema has an optional `note` field; Sygnal's profile leaves it out.)

```json
"deviation": {
  "reasonCode": {
    "@context": "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld",
    "@type": "DeviationReasonCode", "code": "NO_SHOW", "display": "Patient No-Show"
  },
  "detectedBy": "clinic-np-001",
  "detectedAt": "2026-07-03T10:00:00Z"
}
```

### 2. Escalated, beyond the two parties

When a deviation needs its own tracked record, it becomes a **`sygnal/deviation/flag`**. Examples are an SLA breach, an unacknowledged referral, or a discrepancy a supervisor observed. The mode decides who receives the flag and who sets its outcome (the disposition):

| Mode | Raised by | Sent to, and disposed of by | Example |
|---|---|---|---|
| `COUNTER_PARTY` | A party to the transition, whose expectation was not met | The flagged counter-party, which replies on `on_flag`. If it stays unresolved, the reporter can escalate to the [Deviation & Escalation Platform](../components/deviation-and-escalation.md). | "I referred this patient; the receiver never confirmed receipt." |
| `THIRD_PARTY` | A `SUPERVISOR` who observed a discrepancy | The Deviation & Escalation Platform, which replies on `on_flag` | "A household recorded as covered was found missed during a spot-check." |

Each flag has a type: `NOT_RECEIVED`, `NOT_ACCEPTED`, `COVERAGE_MISMATCH`, `ATTESTATION_MISMATCH`, `SLA_BREACH` or `OTHER`. Its status is split by who sets it. The reporter sets `OPEN`, `WITHDRAWN` or `CLOSED`. The respondent sets `ACKNOWLEDGED`, `RESOLVED` or `DISPUTED`. See [deviation/flag](../specification/apis/deviation-flag.md).

{% hint style="warning" %}
**The coded-only rule.** Deviations carry **coded** information: a reason code, participant and transition references, a timestamp, and hashed evidence where needed. They never carry patient identifiers or free text about a patient. Free text is the most common route to accidental disclosure. In a `DeviationReport`, states and status reasons are [CodedValues](../specification/coded-values.md#the-codedvalue-pattern), so the schema itself rejects free text.
{% endhint %}

## SLAs: one definition, read everywhere

Coordination SLAs are defined once, as `SlaRule`s in the network's [coordination policy](policies.md). Each rule names:

* what it applies to (transition type, urgency, from-tier, to-tier);
* the **start** and **stop** messages, for example `confirm` to the `on_status` that carries `ACCEPTED`;
* the **window**, as an ISO 8601 duration such as `PT2H`;
* the **expecting role**, which is the party that raises the flag on breach;
* an advisory **escalation tier** on breach.

The same rule drives the edge's timers, the `SLA_BREACH` deviation, the network's `SLA_BREACH` and `UNACKNOWLEDGED_REFERRAL` signals, and the breach counts in network telemetry. There is one source of truth, so these uses cannot drift apart.

## Escalation tiers

When a deviation stays open, it moves up through the tiers below. The tier is **advisory**: the network recommends, and people decide.

| Tier | What happens | Who sees what |
|---|---|---|
| **1. Structured inquiry** | The responsible party is asked for status about a specific handoff | Status codes only, for example acknowledged, rejected or pending with a coded reason |
| **2. Human escalation** | A supervisor or district officer is alerted | Metadata only, for example "Facility X has 15 unacknowledged referrals in 7 days" |
| **3. Governance alert** | Persistent patterns reach programme or health-system leadership | Aggregates and trends |

## When nobody reports

Counter-party reporting works when somebody is waiting. For some population-health obligations, such as scheduled follow-ups, screenings and vaccination schedules, neither side may notice a miss. For these, Network Intelligence can watch the coordination events that edges report under policy. When an expected completion doesn't appear, it sends a `FOLLOW_UP_DUE` signal to the responsible platform, which decides what to do. A dedicated mechanism for registering such obligations is an [open question](../reference/open-questions.md). See [Reporting and signals](reporting-and-signals.md).
