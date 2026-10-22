---
description: The network's code lists. Every coded value names its own list, so each network can publish the value sets it uses.
---

# Coded values

Coded values are **additive vocabulary, not schema changes**. A payload says which value set it uses, so a network can publish its own lists without touching any schema. The reference network publishes its lists in the repository's [`codedvalues/`](https://github.com/Medtronic-LABS/sygnal/tree/main/codedvalues) folder, and every coded value in the reference flows resolves there.

## The CodedValue pattern

Sygnal uses the same coded-value pattern as the Beckn health (DHP) packs. A coded value names its own code list:

```json
{ "@context": "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld",
  "@type": "sygnal:CoverageState", "code": "MISSED", "display": "Missed" }
```

* `@context` resolves to a JSON-LD context. Its sibling `attributes.yaml` defines one class per `@type`, with the allowed `code` values, so a receiver can validate the code.
* `@type` names the list; `code` is the value; `display` is an optional label taken from the list.
* Beckn health and service pack payloads use the same pattern (for example a referral's `targetCriteria.specialty`), and so do Sygnal API payloads.

In the Sygnal APIs, `DeviationReport.expectedState`, `observedState`, `reporterStatusReason` and `respondentStatusReason` are CodedValues (schema `CodedValue`).

**Close to FHIR's `Coding`.** A coded value carries the same information as a FHIR `Coding`: the code list it comes from (`@context` and `@type`, like `system`), the `code`, and a `display` label. Platforms that use FHIR can map between the two directly. Where a network's list matches a standard terminology, the network can say so in its code lists.

{% hint style="info" %}
**Why network-owned lists.** Value sets vary by health system: specialties, programmes, districts, operational reasons. Pointing `@context` at a network's own lists lets each network say exactly which values its participants accept, and lets a receiver check them, while the schemas stay shared.
{% endhint %}

## Sygnal lists (draft)

Used by the Sygnal coordination APIs.

| `@type` | Members | Used by |
|---|---|---|
| `sygnal:CoverageState` | `COVERED`, `PARTIAL`, `MISSED`, `REFUSED` | `DeviationReport` expected/observed state |
| `sygnal:TransitionState` | `PLACED`, `ACCEPTED`, `DECLINED`, `ATTENDED`, `NO_SHOW`, `COMPLETED`, `CANCELLED`, `NO_RESPONSE` | `DeviationReport` expected/observed state |
| `sygnal:DeviationStatusReason` | Reporter: `RESOLUTION_ACCEPTED`, `RAISED_IN_ERROR`, `DUPLICATE`, `SUPERSEDED`. Respondent: `ACTION_TAKEN`, `ALREADY_COMPLETED`, `RECORD_CORRECTED`, `NOT_RESPONSIBLE`, `EVIDENCE_DISPUTED`. Either: `OTHER` | `DeviationReport` status reasons |

## Shared lists (draft)

Used inside Beckn health and service pack payloads. They keep the pack's `@type` names. They started from the [DHP devkit code lists](https://github.com/beckn/DHP-Specs/tree/main/devkit/stub), and the network has added the members shown below.

| `@type` | Added by this network | Used in |
|---|---|---|
| `ConsentClass` | — | UC1–UC4 |
| `DeviationReasonCode` | — | UC1, UC2 |
| `LGDDistrict` | `DEMO-01` (example district) | UC1–UC3 |
| `ReferralCategory` | `OPERATIONAL` | UC1–UC3 |
| `ServiceCategory` | `FIELD_DATA_COLLECTION` | UC3 |
| `Specialty` | `PAEDIATRICS`, `OBSTETRICS` | UC1, UC2, UC4 |
| `SubSpecialty` | `ICCM`, `MNCH` | UC1, UC2, UC4 |
| `TargetServiceType` | `FIELD_VISIT` | UC1–UC3 |

The full member list of each is in [`attributes.yaml`](https://github.com/Medtronic-LABS/sygnal/blob/main/codedvalues/attributes.yaml).

## Candidate additions

| Type | Candidate members | Status |
|---|---|---|
| Operational `DeviationReasonCode` | `TRANSPORT_UNAVAILABLE`, `FACILITY_CLOSED`, `STOCK_OUT`, `UNREACHABLE` | Candidate. Current reference flows use only existing codes. |

## Rules for code lists

* **Add, don't change.** Within a minor version, members are only added. Removing or renaming a member is a breaking change.
* **Everything resolves.** Every coded value in the reference flows and specification examples must resolve against the network's lists. The repository's `specs/tools/check_codedvalues.py` checks this.
* **Pin a release.** The `@context` URL currently follows the repository's main branch. It will move to a stable address with a tagged release. Production networks should pin a released version.

## Health reason codes and generic reason codes

The deviation reason codes used for referrals are a sub-class of the generic coordination deviation codes. Each referral code maps to one generic code (`skos:exactMatch`). Health participants send the native referral codes. Matching codes across code systems is a task for analytics.

## Sygnal enumerations

Enumerations defined by the Sygnal APIs themselves (deviation types, event types, signal types, roles, statuses) are listed in the [Data model](data-model.md).
