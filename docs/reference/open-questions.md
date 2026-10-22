---
description: Design questions that are still open. A short index; views are welcome.
---

# Open questions

Sygnal is a draft, and some parts are still being designed. This page lists those questions, so you can see at a glance what is settled and what isn't. Have a view, evidence or experience on any of them? See [How to give feedback](feedback.md).

## Specification

* **Attestation:** how a party signs that something happened when there is no counter-party to confirm it, for example a delivery to a household.
* **Notifiable reporting by reference:** whether a notifiable event should carry only a reference, with an authorised public-health participant fetching the record from the edge.
* **Hashing scheme:** when pseudonymous references to a person are needed, and how the shared key is managed.
* **`DeviationReport` FHIR alignment:** confirming the provisional mapping to FHIR DetectedIssue.
* **Commitments register:** whether to define how scheduled obligations, such as follow-ups, are registered, so the network can check them when no counter-party reports.
* **Generic consent:** how consent is carried on the generic `ServiceCoordination` pack, which has no consent field.
* **Domain-neutral naming:** renaming the `CareTransition` profile to a neutral `Transition`.
* **JSON-LD vocabulary:** publishing the `sygnal:` vocabulary, whose address is a placeholder today.
* **Peer-to-peer content policy:** whether policies should say what may travel in handoffs and when it must be encrypted, and how a referral note is structured.

## Trust

* **Role recording:** whether a participant's Sygnal roles are a field in its registry record or a credential issued by the network facilitator.
* **Key management at scale:** issuing, rotating and revoking keys for thousands of facilities, and what the root of trust should be.
* **Offline signing:** how to trust the timestamps of events signed offline and sent later.

## Observation and governance

* **Who sets the reporting dial,** at which level, and how settings are made public.
* **Two reports, one event:** matching a counter-party deviation and a policy-based report about the same event.
* **Re-identification:** whether hiding small counts is enough, or more techniques are needed.
* **Capture and misuse:** safeguards so observation data supports facilities and regions rather than punishing them.
* **Power differences:** how less powerful participants can report deviations against more powerful ones without fear.

## Shared care plans

* Ownership of a plan for a patient with several conditions; the patient's own role; and accountability during handoffs.

## Network of networks

* How separately governed Sygnal networks link up: addressing across networks, recognising each other's participants, sharing discovery, combining policies at the boundary, and passing up aggregates.

## Deployment and sustainability

* How network services are deployed: one instance, regional instances or a federation.
* Whether Sygnal should provide an open-source registry that follows the DeDi (Decentralized Directory) protocol.
* Coordination across jurisdictions, moving from existing centralised platforms, and who pays for network services and adapter upkeep.
