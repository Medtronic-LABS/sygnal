---
description: What exists today, what is being built next, and where Sygnal is heading.
---

# Status and roadmap

{% hint style="info" %}
This page describes **what** is planned and in which order. It is not a schedule. Priorities are revisited as pilots report back.
{% endhint %}

## Available now

| Item | Status |
|---|---|
| **Sygnal specification v0.9**: five coordination APIs, three reads, header, trust profile, policy model | Public draft; automated validation passing |
| **Coordination model and use cases UC1–UC4**, with runnable Postman reference flows | Draft |
| **Documentation** (this site) | Draft for public review |
| **Adapter telemetry configuration** for ONIX: audit-field allow-list, telemetry block, network collector | Published; in use on the Sygnal Sandbox |
| **[Sygnal Sandbox](build/sandbox.md)**: an open test network with discovery, referral journeys, deviation flags and network dashboards | Open for testing with test data |

## Next

| Item | What it delivers |
|---|---|
| **Sygnal Platform, first open-source release** | Code for the components behind the Sygnal Sandbox, published component by component with a code licence |
| **Sygnal Edge Adapter**, a packaged edition of Beckn ONIX | One install for participants: health and Sygnal schemas, `sygnal/*` routing, selective audit, telemetry export, onboarding tooling |
| Adapter plugins | Callback latency, callback timeouts, breaches of service-level agreements (SLAs), live policy updates |
| **Policy Manager** reference service | Signed policy storage and distribution; `policy/get` |
| **Deviation & Escalation Platform** reference service | Dispositions, escalation ladders, worklists |
| **Network Intelligence** hardening | Participant-authenticated telemetry, alert rules, signed `signal/emit` |
| **Discovery Service** hardening | Signature verification, signed callbacks, verified catalogue crawling |
| **Production access** to Sygnal Network Services | Agreed network by network after sandbox testing: hosting, data handling, availability and support |
| `sygnal:` JSON-LD vocabulary | Publishes the context the specification currently references as a placeholder |
| Postman collections for `sygnal/*` APIs | Runnable examples beyond the peer-to-peer core |
| Conformance suite v0.x | Automated checks built from the implementer checklist |

## Specification work in progress

| Item | Notes |
|---|---|
| **Attestation** (`attestation/attest`) | Signed statements inside the message payload, tied to an obligation, for events that have no counter-party to co-sign them |
| **Notifiable reporting by reference** | Proposed: the record stays at the edge and authorised parties fetch it through a signed, role-checked read |
| **Hashing scheme** | Plain versus keyed hashing for pseudonymous subject references |
| **Role recording** in the registry | How Sygnal roles are bound to registry entries |
| **FHIR alignment** | Mapping FHIR resources to Sygnal at the edge, and carrying FHIR-aligned attributes inside schema packs where a network needs them |
| **Domain-neutral transition naming** | Moving from health-specific to neutral names, consistent with the rest of the grammar |

See [Open questions](reference/open-questions.md) for detail.

## Later

* Shared care plans across concurrent providers, at scale.
* A network of networks: linking Sygnal networks (regional, programme, private) so handoffs, discovery and trust work across them.
* Coordination-aware discovery: ranking providers by certification and by their record of closing the loop on handoffs, from metadata only.
* Population-level observation: where the care cascade breaks, by area and programme.
* An open-source Sygnal registry following the DeDi protocol, if networks need an alternative to a hosted DeDi service.
* Certification of independent adapters and service implementations.
* A neutral governance body to steward the specification.
* Exploring AI-assisted coordination that works on metadata patterns, never on clinical content.
* Exploring Edge Adapter extensions for decision support at the edge, such as suggesting when a referral is due, under the platform's control.

## Adoption path for a health system

1. **Start with one use case**, typically closed-loop referral between a community platform and a clinical platform, in one area.
2. **Add policy-governed reporting** and Network Intelligence, so programme managers can see completion and delay.
3. **Expand** to more platforms, more programmes and more areas, and add shared care plans where they help.
4. **Formalise governance:** reporting-policy governance, participation rules and certification.
