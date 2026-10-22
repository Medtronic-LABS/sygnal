---
description: Raise a discrepancy in a coordination event. Silent by default; only a mismatch produces this call.
---

# deviation/flag

| | |
|---|---|
| **Endpoint** | `POST /sygnal/deviation/flag` |
| **Callback** | `POST /sygnal/deviation/on_flag` |
| **Direction** | Participant → counter-party, or → the Deviation & Escalation Platform |
| **Sender** | `COUNTER_PARTY` mode: a party to the referenced transition. `THIRD_PARTY` mode: a participant with the `SUPERVISOR` role. |
| **Payload** | `sygnal:DeviationReport` |
| **Responses** | `200` (callback follows), `202`, `400`, `401`, `403`, `429`, `500` |

## When to use it

Use `deviation/flag` when a coordination expectation was not met and you need to record or escalate the deviation **beyond the in-band field** on the referral (the `deviation` field carried inside the referral itself). Examples:

* a service-level agreement (SLA) expired with no acceptance (`SLA_BREACH`, `NOT_ACCEPTED`);
* a handoff was never received (`NOT_RECEIVED`);
* a supervisor's spot-check contradicts the record (`COVERAGE_MISMATCH`);
* two parties' signed accounts of an event disagree (`ATTESTATION_MISMATCH`).

In the normal case **no deviation is ever sent**. Agreement is silent. See [Deviations and escalation](../../concepts/deviations-and-escalation.md).

## Rules

* `reportedBy.id` **MUST** equal `context.senderId`.
* `THIRD_PARTY` mode **requires** the `SUPERVISOR` role. Otherwise the receiver returns `401 AUT_UNAUTHORIZED_ACTION`.
* `transitionRef` identifies the transition: the Beckn contract id or Referral ID.
* Where the transition has a Beckn transaction id, use it as `context.transactionId`.
* The report is **coded**. `deviationType`, `mode`, `severity` and the two statuses are enums. `expectedState`, `observedState`, `reporterStatusReason` and `respondentStatusReason` are [CodedValues](../coded-values.md#the-codedvalue-pattern) (`{@context, @type, code, display}`), so there is no free text. An optional `evidenceHash` is a hash commitment to evidence held at the edge. Any human note stays in the edge platform.
* Status is split by who sets it. The reporter sets `reporterStatus` (`OPEN`, `WITHDRAWN`, `CLOSED`); the respondent sets `respondentStatus` (`ACKNOWLEDGED`, `RESOLVED`, `DISPUTED`) on `on_flag`.

## Example request

```json
{
  "context": {
    "version": "2.0.0",
    "action": "sygnal/deviation/flag",
    "domain": "healthcare:care-coordination",
    "networkId": "sygnal.moh.example.org/care-net",
    "senderId": "supervisor.d01-district.example.org",
    "receiverId": "deviations.sygnal.moh.example.org",
    "transactionId": "7f1c2a4e-3b5d-4e6f-8a9b-0c1d2e3f4a5b",
    "messageId": "0b8e9c1d-2a3f-4b5c-8d6e-7f8091a2b3c4",
    "timestamp": "2026-07-01T09:15:00Z"
  },
  "message": {
    "@context": "https://spec.sygnal.network/contexts/v0.9.jsonld",
    "@type": "sygnal:DeviationReport",
    "mode": "THIRD_PARTY",
    "deviationType": "COVERAGE_MISMATCH",
    "transitionRef": "contract:campaign-d01-2026:hh-4821",
    "reportedBy": { "id": "supervisor.d01-district.example.org", "role": "SUPERVISOR" },
    "against": { "id": "chw.d01-12.example.org", "role": "PROVIDER" },
    "expectedState": { "@context": "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld", "@type": "sygnal:CoverageState", "code": "COVERED" },
    "observedState": { "@context": "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld", "@type": "sygnal:CoverageState", "code": "MISSED" },
    "severity": "MEDIUM",
    "reporterStatus": "OPEN",
    "reportedAt": "2026-07-01T09:15:00Z"
  }
}
```

## Callback: `deviation/on_flag`

The receiver returns the `DeviationReport` with `respondentStatus` set. The callback carries the request's `messageId` and is signed with a `CallbackSignature`. If the disposition changes later (for example from `ACKNOWLEDGED` to `RESOLVED`), the receiver sends an **unsolicited** `on_flag` with a fresh `messageId`, signed with a standard `Signature`. A party that missed a callback can fetch the current state with [`deviation/get`](reads.md).

## Relationship to the in-band `deviation` field

Between the two transacting parties, a deviation such as `NO_SHOW` can travel in-band, inside the referral's `update`/`status` messages, using the referral's built-in `deviation` field. `deviation/flag` is for deviations that must be raised as their own tracked object, or that must reach the network or an oversight party.
