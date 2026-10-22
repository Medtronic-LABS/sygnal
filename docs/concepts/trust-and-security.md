---
description: Every message signed by a registered participant; role authorization on top; no privileged channel for the network services.
---

# Trust and security

Sygnal has no central party that sees every transaction and can vouch for it. Instead, trust is **explicit and cryptographic**. Every message is signed, and every signature can be checked against a registry. Accountability rests on the evidence those signatures produce.

## Built on Beckn authentication and trust

Sygnal builds on the Beckn Protocol v2 authentication and trust model ([NFH-007](https://github.com/beckn/protocol-specifications-v2/blob/core-v2.0.0-lts/docs/Authentication_and_Trust.md)). Version 0.9 adopts it without changes. In future, Sygnal may extend it where coordination needs more, for example role authorization recorded in the registry, or payload-level attestation. The base model:

* Every participant registers a namespace identifier and an **Ed25519** signing key in the network's registry.
* Every request is signed. The signature covers the creation time, the expiry time and a digest of the body.
* Every **solicited callback** (`on_*`, the later reply to a request) carries a signature linked to the signature of the request that triggered it. This means no one can replay it against a different request.
* Every **synchronous response** (the immediate reply), whether ACK (accepted) or NACK (rejected), carries a signed `Signature` header. That is the receiver's signed receipt.
* Receivers resolve the sender's key from the registry named by the message's `networkId`, and check that the signing key belongs to the stated `senderId`.

Sygnal uses the direction-neutral header fields `senderId` / `receiverId`, plus optional `senderUri` / `receiverUri` for callback addresses. The header is a closed profile of the Beckn v2 context: a subset of its fields plus three Sygnal fields. This means a generic Beckn stack can parse it. See [Conventions](../specification/conventions.md).

## The network facilitator is an ordinary participant

The organisation that runs the network services registers its identity and keys **like any edge**. Edges verify its `policy/update` and `signal/emit` messages exactly as they verify each other. There is no privileged channel and no special trust in the centre.

This matters for two reasons:

* **"Observe and signal, never decide" becomes auditable.** Every signal is attributable to a registered identity.
* **Data minimisation becomes enforceable.** A forged policy, or one signed by a participant without the `GOVERNANCE` role, fails signature or role verification at the edge.

## Role authorization: Sygnal's addition

A valid signature proves **who** sent a message. It doesn't prove they are **allowed** to send it. So every receiver makes two more checks. It checks the sender's Sygnal **role**, as recorded against the sender's registry entry. It also checks that identities in the payload match the signer:

| Action | Sender must be | Payload binding |
|---|---|---|
| `deviation/flag` (counter-party) | A party to the referenced transition | `reportedBy.id` = `senderId` |
| `deviation/flag` (third-party) | `SUPERVISOR` | `reportedBy.id` = `senderId` |
| `event/report` | A registered edge within the active policy's scope | `from.id` (if present) = `senderId` |
| `policy/update` | `GOVERNANCE` | — |
| `plan/sync` | The plan's owner | `owner.id` = `senderId` |
| `signal/emit` | `OBSERVER` | — |
| `*/get` | A party entitled to the record | — |

If the role check fails, the receiver rejects the message with `401` and the Beckn error code `AUT_UNAUTHORIZED_ACTION`. A policy refusal, such as a field outside the allow-list, is a `403`.

## Evidence for disputes

Both legs of every exchange are signed. So the signed request and the signed acknowledgement can settle a dispute about **transmission** ("we sent it" / "we never received it"). The network does not judge disputes about **clinical appropriateness**. They go to the designated clinical arbiter.

## Callback addresses

A request's destination always comes from the registry. A sender can only choose where its own callbacks land, using `senderUri`. Responders should accept only HTTPS callback addresses. They should never accept private, loopback or link-local addresses. Optionally, they may also limit callbacks to hosts within the sender's own namespace domain. A valid signature proves who chose the address, not that the address belongs to them.

## Not the same as attestation

Transport signing authenticates **platforms**. A health worker signing that a delivery happened is a different layer: a payload-level attestation. A dedicated attestation API is planned (see [Status and roadmap](../roadmap.md)).

## Open questions

Several questions are still open:

* how to issue, rotate and revoke keys at scale;
* how roles are recorded in the registry;
* the trust anchor (the root of trust) for a large health system's network, such as a national one.

See [Open questions](../reference/open-questions.md).
