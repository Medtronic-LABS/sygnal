---
description: Three small reads, modelled on Beckn status, for catching up on current state. Not search.
---

# Reads: policy, deviation, plan

Sygnal has three **current-state pulls**. A participant uses them to catch up after missing a pushed message. They are modelled on Beckn `status` (query by id, answer by callback) and **never** on search.

| Endpoint | Callback | Selector | Returns | Purpose |
|---|---|---|---|---|
| `sygnal/policy/get` | `policy/on_get` | `ref` (policy id) **or** `scope` | `{ "policies": [...] }`: one policy for a `ref`; for a `scope`, every policy in its precedence chain, network-wide included | Start-up; recover from a missed `policy/update`; compute the effective policy |
| `sygnal/deviation/get` | `deviation/on_get` | `ref` = deviation id, or the `transitionRef` for the open deviation | One `DeviationReport` | Recover from a missed `on_flag` |
| `sygnal/plan/get` | `plan/on_get` | `ref` = plan id, optional `version` | One `SharedPlan` | Recover from a missed `plan/sync` |

## The shared `Query` selector

All three take the same `Query` as their `message`:

```json
{ "ref": "plan:patient-9f2:integrated", "version": "7" }
```

* At least one of `ref` or `scope` **MUST** be present; `version` alone is not a valid selector.
* `scope` (jurisdiction, program, facility) is meaningful only for `policy/get`.
* A selector that matches nothing returns `404`.
* The sender must be entitled to the record: an edge in the policy's scope, a party to the deviation, or a participant in the plan.

## Why there is no list or search API

The network services deliberately offer **no** list, filter or search API. Dashboards and analytics query the services' **own stores**, which hold only what was reported under policy. A general query API would turn the centre into a large data store that others can query. That is the job of the records layer, which sits *below* Sygnal, not inside it.

This is also why reporting allow-lists use JSONPath while reads do not. Allow-list expressions travel from governance to the edge and **restrict** what leaves the edge. They never let the network **query** what it holds.
