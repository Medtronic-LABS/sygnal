---
description: The network's directory of who's who. Identifiers, keys, addresses and roles. A directory, not a router.
---

# Network Registry

The **Network Registry** is the network's address and key directory. Every participant registers:

* its **namespace identifier**, used as `senderId` / `receiverId`;
* its **public signing key**, which others use to verify its messages;
* its **address** (`url`), where it receives requests and default callbacks;
* the **networks** it belongs to;
* its **Sygnal roles**, such as `GOVERNANCE`, `OBSERVER` or `SUPERVISOR`, which receivers check before acting on a message.

## How it is used

* **Verification.** A receiver looks up `senderId` in the registry for the message's `networkId`, retrieves the sender's key, verifies the signature, and checks the sender's role.
* **Addressing.** A sender looks up the receiver's address. Established peers cache each other's details, so they do not need the registry for every message.
* **Membership.** Discovery results can be checked against the registry to confirm that a provider is a network participant.

**A directory, not a router.** No coordination message passes through the registry. This keeps the network's centre small. It also means a registry outage does not stop peers that already know each other.

## Implementation

Sygnal's registry is **aligned with, and adapts, the [DeDi (Decentralized Directory) protocol](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol)**. DeDi is the open protocol Beckn v2 networks use for participant directories. In DeDi, each participant publishes its record as a signed, machine-readable file on a domain it controls, and anyone can verify it without contacting a central source. The same records can advertise where a participant's catalogues are published, for the [Discovery Service](discovery-service.md) to crawl.

* **Today:** Sygnal Network Services use [dedi.global](https://dedi.global), a hosted DeDi service, as the default registry service. To publish your record, see [Joining a network](../build/joining-a-network.md).
* **Adaptations:** Sygnal adds what coordination needs on top of DeDi records, such as each participant's Sygnal roles and network membership.
* **Other registries:** dedi.global's own software is not open source. A network that needs its own directory, for example to host it in its own jurisdiction, can run a DeDi-compliant registry built to the open protocol. Sygnal may provide an open-source registry if networks need one. Because DeDi is decentralised, a network, or a network of networks, can also spread its directory across operators.

| Protocol | Platform | Network Services |
|---|---|---|
| DeDi, plus Sygnal roles and membership | No Sygnal registry software | dedi.global (default) |

See [Protocol, platform and services](../concepts/protocol-platform-services.md).

## Status

{% hint style="info" %}
**Aligned with DeDi; dedi.global in use today.** Open item: **how Sygnal roles are recorded**. Each network's operator records the roles of its participants; how they are recorded is still open. Options include a registry-record attribute and a credential issued by the network facilitator. The Beckn trust specification does not define this, so each network needs to agree on it. See [Open questions](../reference/open-questions.md).
{% endhint %}
