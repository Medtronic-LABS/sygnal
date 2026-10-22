---
description: The Sygnal resources, their key fields and enumerations. The OpenAPI document is authoritative.
---

# Data model

This page summarises the resources the Sygnal APIs carry. The [OpenAPI reference](api-reference.md) is authoritative. Where this page and the OpenAPI document differ, the OpenAPI document wins.

All resources are JSON-LD, with `@context` and `@type` (`sygnal:<Noun>`). The `sygnal:` vocabulary context will be published at `https://spec.sygnal.network/contexts/v0.9.jsonld`. Until then, the URL is a placeholder.

## Shared building blocks

| Schema | Purpose | Key fields |
|---|---|---|
| `SygnalContext` | Message header (closed) | See [Conventions](conventions.md#header-sygnalcontext) |
| `Participant` | A participant reference: its registry identifier and role. No personal information. | `id`, `role` (`SEEKER`, `PROVIDER`, `OBSERVER`, `GOVERNANCE`, `SUPERVISOR`) |
| `CodedValue` | A typed code from a code list resolved through `@context` ([pattern](coded-values.md#the-codedvalue-pattern)) | `@context`, `@type`, `code`, `display` |
| `HashRef` | A hashed reference to something that stays at the edge | `algorithm` (`BLAKE2b-512` default, `SHA-256`), `value` |
| `Area` | A coded geographic unit; codes only, never free text or coordinates | `code`, `level`, `system` |
| `Attributes` | A typed JSON-LD extension bag | `@context`, `@type`, then open |
| `Query` | Single-record selector for reads | `ref` or `scope`, optional `version` |
| `Ack`, `Nack`, `Error`, signatures | Exact copies of the Beckn v2 core definitions | — |

## DeviationReport

A discrepancy between counter-parties, or one asserted by a third party.

| Field | Notes |
|---|---|
| `mode` | `COUNTER_PARTY` or `THIRD_PARTY` |
| `deviationType` | `NOT_RECEIVED`, `NOT_ACCEPTED`, `COVERAGE_MISMATCH`, `ATTESTATION_MISMATCH`, `SLA_BREACH`, `OTHER` |
| `transitionRef` | The transition (Beckn contract) concerned |
| `reportedBy`, `against` | `Participant`s |
| `expectedState`, `observedState` | `CodedValue`s, for example `sygnal:CoverageState` or `sygnal:TransitionState` |
| `evidenceHash` | `HashRef` commitment to evidence held at the edge |
| `severity` | `LOW`, `MEDIUM`, `HIGH` |
| `reporterStatus` | Set by the reporter: `OPEN`, `WITHDRAWN`, `CLOSED` |
| `respondentStatus` | Set by the respondent: `ACKNOWLEDGED`, `RESOLVED`, `DISPUTED` |
| `reporterStatusReason`, `respondentStatusReason` | `CodedValue`s, for example `sygnal:DeviationStatusReason`. No free text. |
| `deviationAttributes` | Typed extension |

## CoordinationEvent

One item of coordination metadata that an edge reports to the network.

| Field | Notes |
|---|---|
| `eventType` | `TRANSITION_PLACED`, `TRANSITION_ACCEPTED`, `TRANSITION_DECLINED`, `TRANSITION_COMPLETED`, `DELIVERY_RECORDED`, `DEVIATION_RAISED`, `COVERAGE_REPORTED`, `SYNDROMIC_SIGNAL`, `NOTIFIABLE_CASE` |
| `granularity` | `AGGREGATE` or `INDIVIDUAL` (the latter only where the policy allows) |
| `id`, `revision` | `id` is required for aggregates; `revision` (default 1) lets a higher revision replace an earlier one |
| `period`, `area` | The interval and coded area the figures cover (aggregates) |
| `metrics` | Aggregates only; keys **must** be codes the policy defines |
| `subjectRef`, `subjectType` | Individual only, together, and only if the policy permits; `subjectType` is `PATIENT` or `HOUSEHOLD` |
| `caseDetail` | Individual notifiable only: `condition`, `onsetDate`, `area`, as the policy's allow-list permits |
| `from`, `to`, `occurredAt` | Participants and time |

There is no extension bag on this resource, by design.

## CoordinationPolicy

Signed configuration, issued by governance, made up of typed sections. See [Coordination policies](../concepts/policies.md).

| Field | Notes |
|---|---|
| `id`, `version`, `effectiveFrom`, `supersedes` | Identity and ordering |
| `scope` | `jurisdiction`, `program`, `facility`; omitted for network-wide policies |
| `issuerStatus` | `DRAFT`, `ACTIVE`, `RETIRED` (set by governance) |
| `edgeStatus`, `edgeStatusReason` | `APPLIED` or `REJECTED` (set by the edge on `on_update`) |
| `sections[]` | `ReportingSection`, `SlaSection`, `InstrumentationSection`, `PrecedenceSection`, or a network-defined extension section, each with an optional `critical` flag |

**ReportingSection:** `eventTypes`, `cadence`, `areaCodeSystem`, `metricDefinitions[]` (`code`, `kind`: `COUNT`/`SUM`/`MIN`/`MAX`, `unit`, `description`), `reportingMode` (a summary that must agree with `dataMinimization`), and `dataMinimization`:

* `aggregate`: `allowedFields` (JSONPath; default `$.metrics`), `subjectRefPermitted` (default false), `minCellSize`;
* `individual`: `appliesToConditions`, `allowedFields`, `subjectRefPermitted`, `legalBasis`.

**SlaSection:** `rules[]` of `SlaRule`: `id`; `appliesTo` (`transitionType`, `urgency`, `fromTier`, `toTier`); `start` and `stop` (`action`, optional `state`); `window` (ISO 8601 duration); `expectingRole`; and `onBreach.escalationTier` (1, 2 or 3; advisory).

**InstrumentationSection:** `level` (`OFF`, `AGGREGATE`, `EXCEPTIONS`, `PER_TRANSACTION`), plus `until`, which is required for `PER_TRANSACTION`.

**PrecedenceSection** (network-wide only): `levels`, `resolution` per section type (`MOST_SPECIFIC` or `HIGHEST_AUTHORITY`), `locked` (JSONPath), `environment` (`PRODUCTION` or `NON_PRODUCTION`).

## SharedPlan

| Field | Notes |
|---|---|
| `planId`, `version` | Identity; monotonic version or version vector |
| `planHash` | `HashRef` to the full plan held at the owning edge |
| `owner`, `participants[]` | `Participant`s; may be more than two |
| `changeType` | `CREATED`, `UPDATED`, `CLOSED` (set by the owner) |
| `participantStatus` | `SYNCED` or `CONFLICT` (set by a participant on `on_sync`) |
| `goalRefs`, `lastUpdated`, `planAttributes` | — |

## Signal

| Field | Notes |
|---|---|
| `signalType` | `FOLLOW_UP_DUE`, `SLA_BREACH`, `UNACKNOWLEDGED_REFERRAL`, `COVERAGE_GAP`, `OUTBREAK_SUSPECTED` |
| `relatesTo` | Transition, plan or area reference |
| `target` | `Participant` |
| `severity` | `INFO`, `WARNING`, `CRITICAL` |
| `basis` | What observation triggered it |
| `recommendedAction` | **Advisory only** |
| `issuedAt`, `expiresAt`, `signalAttributes` | — |

## FHIR alignment

Each resource carries an `x-fhir-resource` annotation in the OpenAPI document: `DeviationReport` → DetectedIssue *(provisional)*, `CoordinationEvent` → AuditEvent, `SharedPlan` → CarePlan (hashed reference only), `Signal` → Communication. `CoordinationPolicy` is Sygnal-native.
