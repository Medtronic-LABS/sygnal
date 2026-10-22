# schemas: Sygnal JSON-LD vocabulary and extension packs

This folder will hold the files, written by Sygnal, that define the **shape of the data**. They sit beside the API specification in [`../specs/`](../specs/README.md). They will include:

* the `sygnal:` JSON-LD **context and vocabulary**, to be published at `https://spec.sygnal.network/contexts/v0.9.jsonld`. The specification currently uses this as a placeholder URL;
* any **composable extension packs**, for example policy section types or `contractAttributes` extensions that a network defines. These follow the Beckn v2.1 pack layout (`attributes.yaml`, `context.jsonld`, `vocab.jsonld`, `examples/`).

The Beckn health and service packs (`HealthReferral`, `ServiceCoordination`, `HealthContract` and others) are written and kept in Beckn. Sygnal refers to them by `@context` URL and does not copy them.

**Status:** empty. Authoring the `sygnal:` vocabulary is tracked in the [roadmap](../docs/roadmap.md).
