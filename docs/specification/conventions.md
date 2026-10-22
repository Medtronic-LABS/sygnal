---
description: Naming, envelope, header, signing, responses and errors shared by every Sygnal API.
---

# Conventions

## Naming: `sygnal/{noun}/{verb}`

Every Sygnal endpoint is `sygnal/{noun}/{verb}`, and its callback is `sygnal/{noun}/on_{verb}`.

* **`sygnal/` is the namespace.** It keeps the extension apart from core Beckn's flat (single-word) verbs, so no names collide. For example, Beckn has its own `update`.
* **The noun qualifies the verb.** Beckn can use flat verbs because it has essentially one noun: the contract. Sygnal has several nouns (deviation, event, policy, plan, signal), so each verb is qualified by its noun.
* **`context.action` mirrors the path** as a single token, for example `sygnal/deviation/flag`. A Beckn router still routes each message on one action string.
* **The domain is not in the path.** The health binding is carried in `context.domain` (`healthcare:care-coordination`) and the payload's `@type` (`sygnal:<Noun>`). There are no `care/...` aliases.
* **Schemas are named by resource noun**, such as `DeviationReport`, `CoordinationEvent`, `CoordinationPolicy`, `SharedPlan` and `Signal`. The verb lives only in the path.

## Envelope

Every request body is a Beckn envelope:

```json
{
  "context": { "...": "SygnalContext header" },
  "message": { "...": "the resource itself" }
}
```

`message` carries the resource **directly**, with no per-endpoint wrapper. There are two narrow exceptions that carry a set: `event/report` carries `{ "policyId": "...", "events": [ ... ] }`, and `policy/on_get` carries `{ "policies": [ ... ] }`.

Every payload is JSON-LD, with `@context` and `@type`. Extension points (`deviationAttributes`, `planAttributes`, `policyAttributes`, `signalAttributes`) are typed JSON-LD bags with their own `@context` and `@type`. `CoordinationEvent` deliberately has **no** extension bag, because an open bag would bypass the reporting allow-list.

## Header: `SygnalContext`

The header is a **closed** profile of the Beckn v2 `Context`: a strict subset of its fields, plus three Sygnal fields that core v2 doesn't define (`domain`, `senderUri`, `receiverUri`). The two address fields are proposed to Beckn as replacements for `bapUri`/`bppUri` that work in either direction.

| Field | Required | Meaning |
|---|---|---|
| `version` | yes | Beckn core message version, `2.0.0` |
| `action` | yes | Mirrors the path, for example `sygnal/event/report` |
| `networkId` | yes | The network whose registry resolves the participants |
| `senderId` | yes | The participant that signed **this** message |
| `receiverId` | yes | The participant it is addressed to |
| `transactionId` | yes | The Beckn transaction id of the transition this message concerns; if there is none, a new UUID created by whoever starts the thread |
| `messageId` | yes | Unique per request; a solicited callback carries its request's `messageId` |
| `timestamp` | yes | Creation time |
| `domain` | no | Domain binding, for example `healthcare:care-coordination` |
| `ttl` | no | ISO 8601 duration for which the message is valid |
| `requestDigest` | no | On a solicited callback, the digest of the triggering request body |
| `senderUri` | no | On a request, where the sender wants its callback delivered |
| `receiverUri` | no | On a solicited callback, copied from the request's `senderUri` |

Any other field, including Beckn's legacy `bapId` / `bppId` / `bapUri` / `bppUri`, is **rejected**. On a callback, sender and receiver swap relative to the request.

**Addresses.** A request's destination always comes from the registry. A callback goes to `receiverUri` if present, otherwise to the receiver's registry `url`.

**Identifiers.** `transactionId` and `messageId` **MUST** be random UUIDs, never derived from a patient or household identifier. Receivers **MUST NOT** apply Beckn's "active confirmed transaction" check to Sygnal actions.

## Asynchronous acknowledgement

1. The receiver verifies the request and responds immediately:
   * `200 Ack`: accepted; the business result follows on the paired `on_*` callback;
   * `202 AckNoCallback`: accepted; no callback follows (normal for `event/report`);
   * a `Nack` with an error, as listed below.
2. Where there is a result, the receiver sends the signed `on_*` callback to the sender.

## Signing

Sygnal builds on Beckn v2 authentication and trust ([NFH-007](https://github.com/beckn/protocol-specifications-v2/blob/core-v2.0.0-lts/docs/Authentication_and_Trust.md)). Version 0.9 adopts it without changes; later versions may extend it.

| Message | `Authorization` header | Signs over |
|---|---|---|
| Any `sygnal/{noun}/{verb}` request, including `signal/emit` | `Signature` | `(created) (expires) digest` |
| A solicited `on_*` callback | `CallbackSignature` | the above plus the request's signature |
| A later, unsolicited `on_*` (for example a deviation's disposition changes) | `Signature` | `(created) (expires) digest` |
| Every synchronous response, of any status | `Signature` response header (`AckSignature`) | the above plus the request's signature |

Keys are Ed25519 and are resolved from the registry named by `networkId`. The receiver **MUST** check that the signing key belongs to `senderId`. The signature, digest, `Ack` and `Error` schemas in the Sygnal specification are exact copies of Beckn v2 core (marked `x-mirrors`). Production implementations should reference the canonical Beckn definitions.

## Role authorization

On top of signature verification, the receiver checks that the sender holds the Sygnal role the action requires, and that payload identities match the signer. See [Trust and security](../concepts/trust-and-security.md#role-authorization-sygnals-addition).

## Responses and errors

| Status | Body | When |
|---|---|---|
| `200` | `Ack` | Accepted; a callback follows where the action defines one |
| `202` | `Ack` (no callback) | Accepted; no callback follows |
| `400` | `Nack` | Schema or precondition failure (`SCH_*`, `CTX_*`) |
| `401` | `Nack` | Signature absent, expired or invalid (`AUT_SIGNATURE_*`, `AUT_KEY_*`), **or** the sender lacks the required role (`AUT_UNAUTHORIZED_ACTION`) |
| `403` | `Nack` | Declined for policy reasons (`POL_*`), for example a field not permitted by `dataMinimization` or an unknown metric code. No callback follows. |
| `404` | `Nack` | A read selector matched nothing |
| `409` | `Nack` | Conflict, for example a stale shared-plan version |
| `429` | `Nack` | Rate limited |
| `500` | `Nack` | Server error |

Error bodies use the Beckn v2 `Error` shape. The top-level `code` comes from the canonical Beckn error-code list. Domain-specific detail may appear under `details.cause`.

## Expressions

Where the specification uses path expressions (reporting allow-lists, locked policy fields), they are **JSONPath, as defined in [RFC 9535](https://www.rfc-editor.org/rfc/rfc9535)**. That is the same grammar Beckn discovery filters use. The edge evaluates them to **restrict** what leaves it. The network never evaluates them to query what it holds.
