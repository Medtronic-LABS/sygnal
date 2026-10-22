---
description: The upstream specifications, schema packs and software Sygnal builds on, with the versions it pins.
---

# Related specifications

Sygnal builds on open specifications and software maintained by others. This page lists each one, what Sygnal uses it for, and the version Sygnal is reviewed against.

{% hint style="info" %}
**Pin a release.** Where an upstream project tags releases, Sygnal pins one. Where it doesn't yet, the link goes to the main branch. The page then notes the commit that Sygnal was last reviewed against.
{% endhint %}

## Protocol

| Specification | What Sygnal uses it for | Version |
|---|---|---|
| [Beckn Protocol v2 core API](https://github.com/beckn/protocol-specifications-v2/blob/core-v2.0.0-lts/api/v2.0.0/beckn.yaml) | Transaction verbs (`discover` to `cancel`), the contract model, the envelope and `Context`, the async-ACK pattern, error codes | `core-v2.0.0-lts` |
| [Beckn authentication and trust (NFH-007)](https://github.com/beckn/protocol-specifications-v2/blob/core-v2.0.0-lts/docs/Authentication_and_Trust.md) | Message signing, callback and response signatures, key resolution. Adopted without changes in Sygnal 0.9. | `core-v2.0.0-lts` (draft) |
| [DeDi (Decentralized Directory) protocol](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol) | The participant directory behind the [Network Registry](../components/network-registry.md) | Main branch |
| [RFC 9535: JSONPath](https://www.rfc-editor.org/rfc/rfc9535) | Path expressions in reporting allow-lists, locked policy fields and discovery filters | RFC |

## Schema packs

The Beckn health and service schema packs live in [DHP-Specs](https://github.com/beckn/DHP-Specs). Messages refer to each pack by its `@context` URL at `schema.beckn.io`.

| Pack | `@context` | Source |
|---|---|---|
| `HealthReferral` | `https://schema.beckn.io/HealthReferral/v2.1/context.jsonld` | [schema/HealthReferral](https://github.com/beckn/DHP-Specs/tree/main/schema/HealthReferral) |
| `HealthContract` | `https://schema.beckn.io/HealthContract/v2.1/context.jsonld` | [schema/HealthContract](https://github.com/beckn/DHP-Specs/tree/main/schema/HealthContract) |
| `HealthOffer` | `https://schema.beckn.io/HealthOffer/v2.1/context.jsonld` | [schema/HealthOffer](https://github.com/beckn/DHP-Specs/tree/main/schema/HealthOffer) |
| `HealthResource` | `https://schema.beckn.io/HealthResource/v2.1/context.jsonld` | [schema/HealthResource](https://github.com/beckn/DHP-Specs/tree/main/schema/HealthResource) |
| `HealthParticipant` | `https://schema.beckn.io/HealthParticipant/v2.1/context.jsonld` | [schema/HealthParticipant](https://github.com/beckn/DHP-Specs/tree/main/schema/HealthParticipant) |
| `ServiceCoordination` | `https://schema.beckn.io/ServiceCoordination/v2.1/context.jsonld` | [devkit/config/schema/ServiceCoordination](https://github.com/beckn/DHP-Specs/tree/main/devkit/config/schema/ServiceCoordination) |
| `ServiceCoordinationOffer` | `https://schema.beckn.io/ServiceCoordinationOffer/v2.1/context.jsonld` | [devkit/config/schema/ServiceCoordinationOffer](https://github.com/beckn/DHP-Specs/tree/main/devkit/config/schema/ServiceCoordinationOffer) |
| `ServiceCoordinationResource` | `https://schema.beckn.io/ServiceCoordinationResource/v2.1/context.jsonld` | [devkit/config/schema/ServiceCoordinationResource](https://github.com/beckn/DHP-Specs/tree/main/devkit/config/schema/ServiceCoordinationResource) |
| `ServiceParticipant` | `https://schema.beckn.io/ServiceParticipant/v2.1/context.jsonld` | [devkit/config/schema/ServiceParticipant](https://github.com/beckn/DHP-Specs/tree/main/devkit/config/schema/ServiceParticipant) |

These are the packs the [reference flows](../use-cases/README.md) use today. [Transitions on Beckn](../specification/transitions-on-beckn.md#schema-packs-used) explains what each one is for. The full catalogue has more packs for both health and generic services, such as consideration, entitlement, performance and settlement:

* health packs: [`schema/`](https://github.com/beckn/DHP-Specs/tree/main/schema);
* health and generic service packs together: [`devkit/config/schema/`](https://github.com/beckn/DHP-Specs/tree/main/devkit/config/schema).

DHP-Specs has no tagged release for the v2.1 packs yet. Sygnal 0.9 was reviewed against commit `7a117e4`.

**Code lists.** Coded values in these messages are looked up in the network's own [code lists](../specification/coded-values.md), not in an upstream file. The shared lists started from the [DHP devkit code lists](https://github.com/beckn/DHP-Specs/tree/main/devkit/stub).

## Software

| Project | What Sygnal uses it for | Version |
|---|---|---|
| [Beckn ONIX](https://github.com/beckn/beckn-onix) | The foundation of the [Edge Adapter](../components/edge-adapter.md) | Latest release ([v1.9.2](https://github.com/beckn/beckn-onix/releases/tag/v1.9.2) at review) |
| [Beckn starter kit: generic devkit](https://github.com/beckn/starter-kit/tree/main/generic-devkit) | A quick way to set up ONIX participants; the starting point for moving to the Edge Adapter | Main branch (reviewed at `4a7ad5d`) |
| [Beckn Discovr](https://github.com/beckn/beckn-discovr) | The open-source discovery service behind the [Discovery Service](../components/discovery-service.md) | [v1.7.1](https://github.com/beckn/beckn-discovr/tree/v1.7.1) at review |
| [dedi.global](https://dedi.global) ([documentation](https://dedi-global.gitbook.io/docs)) | The hosted DeDi registry that Sygnal Network Services use by default | Hosted service |

## Health data standards

| Standard | Relationship |
|---|---|
| [HL7 FHIR](https://hl7.org/fhir/) | Clinical records are still exchanged in FHIR, over the records layer. Each Sygnal resource states which FHIR resource it aligns with; see [Sygnal and other health DPI](../concepts/relationship-to-other-dpi.md#fhir). |
