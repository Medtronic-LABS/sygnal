---
description: Signed, versioned coordination policies with typed sections, declared precedence, and a fixed rule that policies can only narrow what leaves the edge.
---

# Coordination policies

A **coordination policy** is how governance tells every edge on a network how to behave. It sets:

* which coordination metadata may be reported, and in how much detail;
* which service-level agreements (SLAs, the agreed time limits for coordination steps) apply;
* how much operational telemetry adapters send;
* how overlapping policies combine.

Policies are **data, not code**. They are signed JSON-LD documents (`sygnal:CoordinationPolicy`, JSON-LD being JSON for linked data). Any edge can read and apply them without a policy engine. Officials can review the changes between versions. The network services can read thresholds and SLA windows. Edges can enforce the rules locally.

Governance publishes a policy with [`policy/update`](../specification/apis/policy-update.md), and edges fetch it with [`policy/get`](../specification/apis/reads.md). A participant holding the `GOVERNANCE` role must sign it.

{% hint style="info" %}
Coordination policy governs **how platforms interact**, for example "a high-risk pregnancy referral must be acknowledged within 2 hours." It does **not** carry clinical content, such as which drug to give. Clinical guidance stays in the edge platforms' own decision support.
{% endhint %}

## Starting without encoded policies

A network doesn't have to write down its policies before it starts. Without them, platforms can still hand off care, track each handoff and raise deviations based on their own understanding of what was agreed. Policies make those rules shared and checkable across the network, and they are needed before platforms report coordination events to the network: without a reporting policy, nothing is reported. Many networks will start with handoffs and deviations, and encode their policies as they go.

## Typed sections

A policy carries an array of **sections**, each with a `@type`:

| Section | What it governs |
|---|---|
| `sygnal:ReportingSection` | Which coordination events the edge emits, at what `cadence`, using which `metricDefinitions` and area codes, and, through `dataMinimization`, exactly which fields may leave the edge |
| `sygnal:SlaSection` | Coordination SLAs (`rules[]`), read by edge timers, deviations, signals and telemetry |
| `sygnal:InstrumentationSection` | How much operational telemetry adapters report (`OFF`, `AGGREGATE`, `EXCEPTIONS`, `PER_TRANSACTION`) |
| `sygnal:PrecedenceSection` | The network's declared precedence order (network-wide policies only) |
| Network-defined types | Extension sections introduced through an extension pack, with their own prefix |

**Unknown sections.** An edge ignores a section type it doesn't recognise, **unless** that section is marked `critical: true`. In that case the edge rejects the whole policy (`edgeStatus: REJECTED`, with a reason naming the type). This is the same idea as critical extensions in X.509 certificates. It means a network can add section types without changing the core specification. It also means the edge never silently skips a rule it must enforce.

**Status is split by who sets it.** Governance sets `issuerStatus` (`DRAFT`, `ACTIVE`, `RETIRED`). The edge reports `edgeStatus` (`APPLIED`, `REJECTED`) on `policy/on_update`.

## Scope and precedence

A policy may be **network-wide** (no `scope`) or **scoped** to a jurisdiction, programme or facility. When several apply, the network decides how they combine. It states this in a `PrecedenceSection` inside a network-wide policy:

* `levels`: the scope levels, highest authority first, for example `network`, `jurisdiction`, `program`, `facility`;
* `resolution`: per section type, either `MOST_SPECIFIC` (the default) or `HIGHEST_AUTHORITY`;
* `locked`: JSONPath expressions for fields that lower levels may not override;
* `environment`: `PRODUCTION` or `NON_PRODUCTION`.

Ties break by `version`, then `effectiveFrom`. `supersedes` names the policy a new one replaces.

## Policies can only narrow

{% hint style="success" %}
Whatever precedence a network declares, **data minimisation always merges to the most restrictive result**. Only fields on every allow-list are allowed. Subject references may be sent only if every policy permits them. The larger minimum cell size wins. A lower level can narrow what leaves the edge. It can **never** widen it.
{% endhint %}

This answers the obvious governance question: what stops someone turning the reporting dial to maximum? No single policy can widen what a higher level allows. Every policy is signed, so you can always tell who issued it. A forged policy, or one signed without the `GOVERNANCE` role, fails signature or role verification at the edge.

## Example

```json
{
  "@context": "https://spec.sygnal.network/contexts/v0.9.jsonld",
  "@type": "sygnal:CoordinationPolicy",
  "id": "policy-district-x-referrals",
  "version": "3",
  "effectiveFrom": "2026-07-01T00:00:00Z",
  "scope": { "jurisdiction": "district-x" },
  "issuerStatus": "ACTIVE",
  "sections": [
    {
      "@type": "sygnal:ReportingSection",
      "cadence": "P7D",
      "metricDefinitions": [
        { "code": "referrals_placed", "kind": "COUNT", "unit": "{referral}" },
        { "code": "referrals_accepted_within_sla", "kind": "COUNT", "unit": "{referral}" }
      ],
      "dataMinimization": {
        "aggregate": { "allowedFields": ["$.metrics"], "subjectRefPermitted": false, "minCellSize": 5 },
        "individual": { "appliesToConditions": [] }
      }
    },
    {
      "@type": "sygnal:SlaSection",
      "critical": true,
      "rules": [{
        "id": "emergency-referral-acceptance",
        "appliesTo": { "transitionType": "referral", "urgency": "EMERGENCY" },
        "start": { "action": "confirm" },
        "stop": { "action": "on_status", "state": "ACCEPTED" },
        "window": "PT2H",
        "expectingRole": "SEEKER",
        "onBreach": { "escalationTier": 2 }
      }]
    }
  ]
}
```

{% hint style="info" %}
This example is only an illustration. The [OpenAPI reference](../specification/api-reference.md) defines the authoritative shape. See `CoordinationPolicy` and its section schemas.
{% endhint %}

## Out of scope for the protocol

How a policy is **drafted and approved** (committees, consultation, sign-off) is an internal matter for governance. The protocol fixes the policy document itself, its signing by a `GOVERNANCE`-role participant, versioning, scope, precedence and distribution.
