---
description: How to give feedback on and contribute to the Sygnal specification, documentation and reference flows.
---

# Contributing

Sygnal is developed in the open, and the specification is a public draft. Review and contributions are welcome.

## Ways to contribute

* **Review the specification.** Read the [Specification](../specification/README.md) and [Open questions](open-questions.md), and tell us what is unclear, wrong or missing.
* **Propose a use case.** Describe a coordination scenario from your health system, with its actors, trigger and expected flow.
* **Improve the documentation.** Fix errors and unclear passages.
* **Implement.** Build an adapter or a service against the specification, and tell us what you learn.

## How

Open an issue or a pull request on the [GitHub repository](https://github.com/Medtronic-LABS/sygnal).

For questions and ideas, see [How to give feedback](feedback.md). To discuss a pilot or partnership, email [hello@sygnal.network](mailto:hello@sygnal.network).

## Repository layout

```
docs/              this documentation (published as the book)
  specification/   human-readable specification
specs/             OpenAPI definition of the Sygnal APIs + validator
reference-flows/   Postman collections and environments, one folder per use case
schemas/           sygnal: JSON-LD vocabulary and extension packs (to come)
codedvalues/       the network's code lists
adapter-config/    ONIX configuration for network telemetry
```

## Conventions

* **Specification changes:**
  1. Edit `specs/sygnal-coordination-apis.yaml`.
  2. Run `python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml` and `python3 specs/tools/check_codedvalues.py .`. All checks must pass.
  3. Update the affected pages under `docs/specification/`.
  4. Add a changelog entry.
* **Design decisions:** record any important or non-obvious choice as a decision record, with its context and consequences.
* **Documentation changes:** run `python3 specs/tools/check_links.py .` before you push. Every internal link must resolve.
* **Reference flows:** keep each use case's environment in sync with its collection. Never commit real keys, tokens or personal data.
* **Commits:** follow [Conventional Commits](https://www.conventionalcommits.org/). Work on short-lived branches that merge back into the main branch quickly (trunk-based development).
* **Consumers** of the specification pin a **released** version, never `main`.

## Writing guidelines for the documentation

* **Write in plain language.** Readers include health-system leaders, programme managers and policy makers as well as engineers, and many read English as a second language. Keep it professional, simple and easy to follow:
  * one idea per sentence, ideally under 25 words; active voice; lead with the point;
  * everyday words: "use", not "leverage" or "utilise"; "before", not "prior to"; "show", not "surface";
  * no jargon or metaphor-jargon ("first-class", "hot path", "load-bearing"); explain an unavoidable technical term the first time it appears on a page, and spell out acronyms;
  * "for example" and "that is", not "e.g." and "i.e.";
  * no hype or marketing superlatives;
  * British spelling (organisation, programme, catalogue).
* **Say "health system", not "country" or "national"**, in generic statements. A national health system is one kind of health system, alongside regional, programme-level and private ones, and is often itself a collection of many health systems. Use "national" only as an example of a health system, or for a specific national deployment.
* **Say "platform" or "edge platform"** for software, and keep "health system" for the system of care.
* **Credit Medtronic LABS by role.** Spell it "Medtronic LABS". Say what it does in context: it **leads** the protocol, which is developed with partners and the community (always present the protocol as a shared effort, never as Medtronic LABS' alone); it **develops** the Sygnal Platform; it **operates** Sygnal Network Services today; and it **looks after** the specification until a neutral body takes over. In headline credits, say "an open initiative led by Medtronic LABS". Sygnal is the name; use a text credit, not a logo.
* **Name the right tier.** Say **Sygnal Protocol** for the specification, **Sygnal Platform** for the reference software, and **Sygnal Network Services** for the hosted services. "Sygnal" alone means all three.
* **Scope privacy claims precisely.** The **network services** never receive clinical content. Peer-to-peer handoffs carry what the two authorised parties need. Avoid blanket "Sygnal sees nothing" claims.
* **Sygnal flags systems and roles, not people.** The platform resolves a role to a person.
* **Source every statistic** with a published reference.

## Licence

The Sygnal specification and documentation are published under [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/). You may share and adapt them, including for commercial use, if you give credit. You must share adapted versions under the same licence. The licence for reference code (such as the validator) is still to be decided.
