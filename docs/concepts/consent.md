---
description: Consent travels with the referral. Three classes, lifecycle hooks, and a known gap on the generic contract.
---

# Consent

Consent for a health referral is carried **with the referral**, in `HealthReferral.consent`. It reuses the health-contract consent fields and adds a `consentClass` plus class-specific fields.

## Three classes

| Class | Basis | Key fields | Typical use |
|---|---|---|---|
| **A** | Explicit, **mediated** | `mediatorCredentialRef`: the mediator's credential or decentralised identifier (DID) | A community health worker captures consent at the doorstep |
| **B** | **Treatment relationship** | `originatingConsentRef`: the prior relationship | A general practitioner refers to a specialist |
| **C** | **Deemed**, ratified after the fact | `deemedBasisCode`, `clinicalJustification`, `ratifiedAt` | Emergency or compressed flows |

## Class A in community-health flows

All current [use cases](../use-cases/README.md) use **class A**. Consent is explicit. The community health worker captures it at the point of field observation, and the referral carries it:

* the mediator is identified by `mediatorCredentialRef`;
* `consentedBy` records who gave consent; `patientParticipantId` binds it to the subject;
* the consent artefact itself is a credential-scoped document in the contract's documents, referenced by `consentDocRef`.

## Lifecycle hooks

The referral lifecycle state `POST_FACTO_CONSENT_PENDING` marks a referral that is waiting for deemed (class C) consent to be ratified, that is, confirmed after the fact. A referral in that state must carry `consent`.

## Where identity may appear

Every exchange except discovery is point to point between two participants who are already coordinating a person's care. Identity-bearing consent is appropriate there.

Extra scrutiny applies to:

* **discovery**, which is a broadcast and must carry no personal information;
* **anything that reaches a third party** outside the two-party exchange. There, identity needs both a policy or consent basis and data minimisation. This is why escalated deviations and reports are [coded-only](deviations-and-escalation.md).

## Relationship to existing consent frameworks

A health system may already have a consent framework for record exchange, such as a consent manager in its health information exchange. If so, Sygnal's coordination consent should **align with it rather than duplicate it**. Sygnal carries the consent needed for the coordination handoff. The records layer governs consent for moving the clinical record. How the two artefacts relate in a given health system is decided at deployment.

## Known gap: consent on the generic contract

The generic `ServiceContract` / `ServiceCoordination` pack has **no consent field**; consent exists only in the health pack. So a generic task-out ([UC3](../use-cases/uc3-downward-task-out.md)) carries class-A consent as a self-authored extension on the generic contract attributes. The extension copies the shape of health consent. There are two ways to standardise it: add a generic `consent` field to `ServiceContract` upstream, or bind consent through `ServiceConsideration`. This is tracked in [Open questions](../reference/open-questions.md).
