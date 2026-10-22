---
description: The Sygnal coordination protocol. Beckn v2 for handoffs, plus five coordination-native APIs and three reads.
---

# Specification overview

{% hint style="warning" %}
**Public draft, version 0.9.** This specification is complete enough to implement against. Automated checks have validated it (OpenAPI 3.1 structure, schema examples, envelopes, trust alignment, policy rules). It may still change in breaking ways before v1.0. Feedback is welcome; see [Contributing](../reference/contributing.md).
{% endhint %}

## Two layers, one wire

A Sygnal network speaks one protocol on the wire, made of two layers:

1. **Beckn Protocol v2 for handoffs.** Every transition (referral, task, booking) uses the standard Beckn actions `discover`, `select`, `init`, `confirm`, `status`, `update` and `cancel`, with their `on_*` callbacks. They carry existing Beckn health and service schema packs. Sygnal does **not** redefine them. It profiles them: it sets out how a transition uses them. See [Transitions on Beckn](transitions-on-beckn.md).
2. **Sygnal coordination APIs for everything Beckn lacks.** Sygnal defines five write APIs and three reads under the `sygnal/` namespace:

| API | Direction | Purpose |
|---|---|---|
| [`sygnal/deviation/flag`](apis/deviation-flag.md) | participant → counter-party or network | Raise a discrepancy; disposition returned on `on_flag` |
| [`sygnal/event/report`](apis/event-report.md) | edge → network | Report coordination metadata under policy (no callback) |
| [`sygnal/policy/update`](apis/policy-update.md) | governance → edge | Distribute a signed coordination policy; adoption confirmed on `on_update` |
| [`sygnal/plan/sync`](apis/plan-sync.md) | plan owner → participants | Publish or update a shared plan by hashed reference |
| [`sygnal/signal/emit`](apis/signal-emit.md) | network → edge | Send an advisory coordination signal |
| [`sygnal/policy/get`, `deviation/get`, `plan/get`](apis/reads.md) | requester → record holder | Fetch current state after missing a pushed message |

In short: **Beckn carries the handoffs. Sygnal carries trust, observation, governance and shared planning.**

## What is in the specification

| Artefact | Where |
|---|---|
| OpenAPI 3.1 definition of the Sygnal APIs | [`specs/sygnal-coordination-apis.yaml`](https://github.com/Medtronic-LABS/sygnal/blob/main/specs/sygnal-coordination-apis.yaml) |
| Validator (structure, examples, envelopes, trust and policy rules) | [`specs/tools/validate.py`](https://github.com/Medtronic-LABS/sygnal/blob/main/specs/tools/validate.py) |
| Conventions: naming, envelope, header, signing, errors | [Conventions](conventions.md) |
| How handoffs use Beckn | [Transitions on Beckn](transitions-on-beckn.md) |
| Resources and their fields | [Data model](data-model.md) |
| Network vocabulary | [Coded values](coded-values.md) |
| Rendered API reference | [OpenAPI reference](api-reference.md) |
| Version history | [Versioning and changelog](changelog.md) |

## Key words

The key words **MUST**, **MUST NOT**, **SHOULD**, **SHOULD NOT** and **MAY** in the specification are to be interpreted as described in [RFC 2119](https://www.rfc-editor.org/rfc/rfc2119) and [RFC 8174](https://www.rfc-editor.org/rfc/rfc8174) when, and only when, they appear in all capitals.

## What comes next

For what is planned next, see [Status and roadmap](../roadmap.md) and [Open questions](../reference/open-questions.md).
