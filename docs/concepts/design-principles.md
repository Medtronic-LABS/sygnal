---
description: The constraints every Sygnal component and every extension must respect.
---

# Design principles

These principles are **constraints**, not aspirations. The specification and the components follow each one. If a proposed feature breaks a principle, the feature is redesigned or rejected.

## Data sovereignty: where data lives

**1. Clinical data stays at the edge.** Clinical records remain with the platform that created them. Where a record must move between providers, it moves peer to peer over the health system's records layer, with consent. The network services never hold or aggregate clinical data.

**2. Only coordination metadata reaches the centre, and only as policy permits.** The control plane carries event types, timestamps, participant identifiers, coded reasons and hashed references. The only exception is a notifiable report that is limited in scope and has a legal basis. Even then, the reporting policy controls it field by field, and the edge enforces it.

**3. Counter-party reporting, not self-reporting.** The party that is waiting for something has the strongest incentive to report that it didn't happen. So the expecting party raises deviations. Nobody is asked to report their own failure. Signed messages provide the evidence.

## Resilience: what happens when things break

**4. Treatment is never blocked by coordination.** No coordination step, policy check or dispute process may delay urgent care. Coordination is an accountability layer, not a gate.

**5. Graceful degradation by design.** Every component defines how it behaves when the services it depends on are unavailable. If the network services are down, peer-to-peer coordination continues. If connectivity drops, events queue and sync later.

**6. Progressive enhancement, not big bang.** The network delivers value at every level of digital maturity and can be adopted one use case at a time.

## Governance: who controls what

**7. The centre observes and signals; it never decides.** The network services can flag a gap or a breach and recommend an action. They cannot dictate a clinical or operational response. The `recommendedAction` on every signal is advisory.

**8. Intelligence lives at the edge.** Clinical logic, care plans and decision support run on the edge platforms. Only structured, minimal outputs leave them.

## Protocol design

**9. Reuse before you build.** Where Beckn Protocol v2 already has a function (finding a counterpart, agreeing terms, placing and tracking a handoff), Sygnal uses it through a profile (a set of rules for how to use it) and does not reinvent it. Sygnal adds new APIs only for the real gaps: deviations, policy-governed reporting, governance policy, shared plans and advisory signals. See [Transitions on Beckn](../specification/transitions-on-beckn.md).

**10. Domain-neutral grammar, health-specific bindings.** Sygnal's verbs and resource names are domain-neutral (`deviation/flag`, `CoordinationEvent`). The message's `domain` and the payload's type carry the health binding. This means the same grammar could coordinate other sectors without changing the protocol.

**11. Open and replaceable.** The specification is open. Every reference component can be replaced by another implementation that honours the specification.

## The guardrail

{% hint style="danger" %}
**Any capability that requires the centre to see clinical content, or to make a clinical decision, is rejected or redesigned to run at the edge.**
{% endhint %}

For example, deciding whether a patient's care follows the clinical protocol, as clinical decision support does, needs diagnoses and results. So that logic runs in the edge platform, where the data already is. When it finds the patient needs care elsewhere, the platform makes a referral through Sygnal. When an agreed step is overdue, it raises a coded deviation. Either way, the network sees only coordination details, never the clinical reasoning behind them.
