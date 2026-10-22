---
description: Worked coordination scenarios, each with a narrative, a sequence diagram and a runnable Postman reference flow.
---

# Use cases overview

Each use case is a concrete coordination scenario between real kinds of platforms. Each page sets out the actors, trigger, consent basis and scope, and gives a sequence diagram. Each use case also has an **importable Postman collection and environment** that you can run against a sandbox.

The four core use cases are set in **community health**. A health campaign platform and a primary-care clinical platform coordinate care for the households a campaign reaches:

* **DIGIT HCM**, an open-source health campaign management platform, operated by community health workers in *campaign mode* (registration, distribution, field observation);
* **ComEMR**, a community and primary-care EMR built on Medtronic LABS' SPICE platform, operated in *clinical mode*. It plays the **care coordinator** role: it receives referrals, routes them to clinical workers, and escalates to peripheral health units;
* **CARE**, an open-source hospital information system, appears in UC4 as a facility on a *separate* platform.

The same community health worker may use both DIGIT HCM and ComEMR. The worker switches between roles but is not a participant. What crosses the network is the handoff between the two platforms.

## Registry

| UC | Title | Direction | Transactions | Contract | Consent | Status |
|---|---|---|---|---|---|---|
| [UC1](uc1-upward-fever-referral.md) | Upward fever referral (child, malaria RDT positive) | Upward, directed | T1 only | `HealthReferral` | A | Draft |
| [UC2](uc2-upward-mnch-danger-sign.md) | Upward MNCH danger-sign referral (pregnant mother) | Upward, directed | T1 only | `HealthReferral` | A | Draft |
| [UC3](uc3-downward-task-out.md) | Downward task-out (field data collection) | Downward, matched | One matched transaction | `ServiceCoordination` (generic) | A | Draft |
| [UC4](uc4-separate-system-escalation.md) | Escalation to a facility on a separate platform | Upward + downstream hop | T1 + T2 | `HealthReferral` + `HealthContract` | A | Draft |

Beyond these, [Coordination patterns](coordination-patterns.md) describes six wider patterns (campaign-to-routine conversion, cross-programme coordination, supervisor deviations, delivery attestation, outbreak signalling and coverage observation), and shows which Sygnal APIs each uses.

## Reference flows

Each use case ships a **Postman Collection (v2.1)** and a **self-contained environment** in the repository's [`reference-flows/`](https://github.com/Medtronic-LABS/sygnal/tree/main/reference-flows) folder. See [Running the reference flows](../build/running-reference-flows.md).

## Known gaps carried across use cases

| Gap | Where | How it is handled |
|---|---|---|
| Community-health and field codes (`PAEDIATRICS`, `ICCM`, `OBSTETRICS`, `MNCH`, `FIELD_DATA_COLLECTION`, `OPERATIONAL`, `FIELD_VISIT`) are not in the DHP devkit code lists | UC1–UC4 | Added to the network's own [code lists](../specification/coded-values.md), which every flow's coded values point at (permitted by design) |
| No consent field on the generic `ServiceCoordination` pack | UC3 | Carried as a self-authored extension; see [Consent](../concepts/consent.md#known-gap-consent-on-the-generic-contract) |
| Operational deviation codes (transport unavailable, stock-out, …) | All | Optional additive vocabulary; flows use standard upstream codes only |

## What the reference flows cover

The reference flows test the **peer-to-peer core**: the Beckn transition lifecycle, with deviations carried inside the transaction messages themselves (in-band). The Sygnal coordination APIs add to the same scenarios without changing them. These are `deviation/flag` for service-level agreement (SLA) breaches, policy-governed `event/report`, `signal/emit` and `policy/update`. Each use-case page notes where they come in.

## Adding a use case

1. Copy an existing use-case page and its reference-flow folder.
2. Edit the narrative, the sequence diagram, and the collection and environment JSON. Keep the environment's variables in sync with the collection.
3. Add a row to the registry above and an entry in the table of contents.
4. Record any modelling choice that is not obvious as a design decision, with its context and consequences.
