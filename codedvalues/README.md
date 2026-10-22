# codedvalues: Sygnal network vocabularies

This folder holds the code lists that a Sygnal network uses. They follow the Beckn DHP CodedValue pattern. A message carries a coded value like this:

```json
{ "@context": "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld",
  "@type": "sygnal:CoverageState", "code": "MISSED", "display": "Missed" }
```

`@context` points to [`context.jsonld`](context.jsonld). The file next to it, [`attributes.yaml`](attributes.yaml), defines one class per `@type` and lists the allowed `code` values. A validator uses it to check each code.

The pattern lets a message name the list of values it uses, so each network can publish its own lists. The reference flows point every coded value to this folder (Postman variable `codedvalue_ctx`).

## Sygnal lists (draft, v0.9)

| `@type` | Members | Used by |
|---|---|---|
| `sygnal:CoverageState` | `COVERED`, `PARTIAL`, `MISSED`, `REFUSED` | `DeviationReport.expectedState` / `observedState` |
| `sygnal:TransitionState` | `PLACED`, `ACCEPTED`, `DECLINED`, `ATTENDED`, `NO_SHOW`, `COMPLETED`, `CANCELLED`, `NO_RESPONSE` | `DeviationReport.expectedState` / `observedState` |
| `sygnal:DeviationStatusReason` | Reporter: `RESOLUTION_ACCEPTED`, `RAISED_IN_ERROR`, `DUPLICATE`, `SUPERSEDED`. Respondent: `ACTION_TAKEN`, `ALREADY_COMPLETED`, `RECORD_CORRECTED`, `NOT_RESPONSIBLE`, `EVIDENCE_DISPUTED`. Either: `OTHER` | `DeviationReport.reporterStatusReason` / `respondentStatusReason` |

## Shared lists (draft, v0.9)

These keep the `@type` names that the Beckn health and service schema packs use. They started from the [DHP devkit stub](https://github.com/beckn/DHP-Specs/tree/main/devkit/stub). In `attributes.yaml`, members that this network added are marked `x-sygnal-additions`.

| `@type` | Sygnal additions | Used in |
|---|---|---|
| `ConsentClass` | — | UC1–UC4 |
| `DeviationReasonCode` | — | UC1, UC2 |
| `LGDDistrict` | `DEMO-01` (example district) | UC1–UC3 |
| `ReferralCategory` | `OPERATIONAL` | UC1–UC3 (`OPERATIONAL` in UC3) |
| `ServiceCategory` | `FIELD_DATA_COLLECTION` | UC3 |
| `Specialty` | `PAEDIATRICS`, `OBSTETRICS` | UC1, UC2, UC4 |
| `SubSpecialty` | `ICCM`, `MNCH` | UC1, UC2, UC4 |
| `TargetServiceType` | `FIELD_VISIT` | UC1–UC3 (`FIELD_VISIT` in UC3) |

## Candidates

| `@type` | Candidate members | Status |
|---|---|---|
| `DeviationReasonCode` (operational) | `TRANSPORT_UNAVAILABLE`, `FACILITY_CLOSED`, `STOCK_OUT`, `UNREACHABLE` | Not yet used; flows use existing codes |

## Rules

* Within a minor version, members can only be added. Removing or renaming a member is a breaking change.
* Every coded value in the reference flows must be defined here. `python3 specs/tools/check_codedvalues.py .` checks this (run from the repository root).
* The `@context` URL currently points into the repository. It will move to a stable address with a tagged release.

See [Coded values](../docs/specification/coded-values.md) in the documentation.
