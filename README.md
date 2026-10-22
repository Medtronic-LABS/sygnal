# Sygnal

**Sygnal is an open way to build Care Coordination Networks.** In these networks, independent health platforms hand off care to one another, follow each handoff to the end, and show where care falls through the gaps. They do this without a separate integration between every pair of platforms. There is also no central system that holds patient records or makes clinical decisions.

Sygnal provides:

* **Specifications.** The Sygnal coordination protocol, built on [Beckn Protocol v2](https://github.com/beckn/protocol-specifications-v2).
* **Edge tools.** The Sygnal Edge Adapter, which lets any platform join a network.
* **Network enablement services.** Network Registry, Discovery Service, Policy Manager, Deviation & Escalation Platform and Network Intelligence.

These come in three parts:

* the **Sygnal Protocol**: the open specification, in this repository;
* the **Sygnal Platform**: software that implements it, being prepared for open-source release;
* **Sygnal Network Services**: the shared services, hosted so a network doesn't have to run them. They handle metadata only.

See [Protocol, platform and services](docs/concepts/protocol-platform-services.md).

📖 **Read the documentation:** start at [`docs/README.md`](docs/README.md). The `docs/` folder is published as the Sygnal documentation site.

> **Status:** active development. The specification is a **public draft (v0.9)** and may change before v1.0. See [Status and roadmap](docs/roadmap.md).

## What's in this repository

```
docs/              The documentation (published as the book; see SUMMARY.md)
specs/             OpenAPI 3.1 definition of the Sygnal coordination APIs, plus validator
reference-flows/   Postman collections and environments for the use cases (UC1–UC4)
schemas/           sygnal: JSON-LD vocabulary and extension packs (to come)
adapter-config/    ONIX configuration that connects an adapter to a network's telemetry and dashboards
codedvalues/       The network's code lists (every coded value in the flows resolves here)
```

The runnable components (the Edge Adapter and the network services) will each get their own repository as they are released.

## Quick links

* [Why Sygnal](docs/why-sygnal/README.md) · [Architecture](docs/concepts/architecture.md) · [Design principles](docs/concepts/design-principles.md)
* [Specification](docs/specification/README.md) · [OpenAPI file](specs/sygnal-coordination-apis.yaml)
* [Use cases](docs/use-cases/README.md) · [Reference flows](reference-flows/README.md)
* [How to give feedback](docs/reference/feedback.md) · [Contributing](docs/reference/contributing.md)

## Validate the specification

```bash
pip install pyyaml openapi-spec-validator jsonschema rfc3987
python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml
python3 specs/tools/check_codedvalues.py .
```

## Licence

The Sygnal specification and documentation are published under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You may share and adapt them, including for commercial use, if you give credit. You must share adapted versions under the same licence. The licence for reference code (such as the validator) is still to be decided.

Adapters connect to platforms that have their own licences (for example, OpenMRS uses MPL-2.0). Keeping each component in its own repository keeps these licences clearly separate.

Sygnal is an open initiative led by Medtronic LABS. See [About Sygnal](docs/reference/about.md). Contact: [hello@sygnal.network](mailto:hello@sygnal.network).
