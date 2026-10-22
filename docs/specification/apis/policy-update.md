---
description: Distribute a signed coordination policy from governance to an edge; the edge confirms adoption.
---

# policy/update

| | |
|---|---|
| **Endpoint** | `POST /sygnal/policy/update` |
| **Callback** | `POST /sygnal/policy/on_update` |
| **Direction** | Governance (via the Policy Manager) → edge. It is the only verb that sends configuration down to the edge. |
| **Sender** | A participant with the `GOVERNANCE` role |
| **Payload** | `sygnal:CoordinationPolicy` |
| **Responses** | `200` (callback follows), `202`, `400`, `401`, `403`, `500` |

## When to use it

Push a new or revised [coordination policy](../../concepts/policies.md) to the edges in its scope. Edges that were offline, or that are starting up, fetch their applicable policies with [`policy/get`](reads.md) instead.

A network can start without policies; see [Starting without encoded policies](../../concepts/policies.md#starting-without-encoded-policies).

## Rules

* The edge **MUST** verify that the sender holds the `GOVERNANCE` role before applying the policy (`401 AUT_UNAUTHORIZED_ACTION` otherwise). A forged policy could widen what leaves the edge.
* The edge ignores sections whose `@type` it doesn't recognise, **unless** a section is `critical: true`. Then it rejects the whole policy.
* A `PrecedenceSection` is valid only in a network-wide policy (one with no `scope`).
* When several policies apply, the edge computes its effective policy using the network's declared precedence, and **always** merges `dataMinimization` to the most restrictive result.
* `InstrumentationSection.level: PER_TRANSACTION` is valid only when the network's `PrecedenceSection` declares `environment: NON_PRODUCTION`, and it requires `until`.

## Callback: `policy/on_update`

The edge returns the policy with `edgeStatus` set to:

* `APPLIED`, or
* `REJECTED`, with an `edgeStatusReason`, for example naming an unrecognised critical section type.

## Example

See the example in [Coordination policies](../../concepts/policies.md#example), and the full examples (a scoped policy and a network-wide precedence policy) in the [OpenAPI reference](../api-reference.md).
