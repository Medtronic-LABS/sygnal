---
description: The steps a platform takes to join a Sygnal network, from identity and keys to the first test handoff.
---

# Joining a network

This page describes how a platform joins a Sygnal network. The steps are the same for every network; the values (network id, registry, addresses) come from the network you join. To try Sygnal first with test data, start with the [Sygnal Sandbox](sandbox.md).

## Before you start

From the network you are joining, you need:

* the **network id** and the **registry** it uses;
* the **Discovery Service** address, if you will make or receive matched handoffs;
* the **network telemetry** address, and the credential for it if the network uses one;
* the **roles** you will hold. Most platforms are `SEEKER`, `PROVIDER` or both. Supervisors, governance and observers hold their own roles.

## Steps

### 1. Choose your identity

Pick a stable **identifier** for your platform on this network, typically a domain you control, such as `emr.example.org`. It becomes your `senderId` / `receiverId`.

### 2. Generate keys

1. Generate an **Ed25519** signing key pair.
2. Keep the private key in your secret store.

Never use shared test keys on a real network.

### 3. Publish your record in the directory

Sygnal networks use directories that follow the open [DeDi protocol](https://github.com/LF-Decentralized-Trust-labs/decentralized-directory-protocol). You publish a signed record with your identifier, public key and address (`url`). The operator of each network you join then adds a reference to your record in its registry, and records your Sygnal roles in that network. On the Sygnal Sandbox, the sandbox team does this.

You can publish your record in one of two ways:

* **Hosted:** on [dedi.global](https://dedi.global). You host nothing yourself, but you need access to your domain's DNS to verify it.
* **On your own domain:** as DeDi files that you publish and keep up to date.

Use one way for each record, not both. Networks for Humanity's [onboarding guide](https://docs.nfh.global/build/onboarding) walks through both, step by step. See also [Network Registry](../components/network-registry.md).

### 4. Deploy the Edge Adapter

Deploy the [Edge Adapter](../components/edge-adapter.md) beside your platform as a separate service (sidecar). Today that means [Beckn ONIX](https://github.com/beckn/beckn-onix), for example from the Beckn starter kit's [generic devkit](https://github.com/beckn/starter-kit/tree/main/generic-devkit). Configure:

* your identity, keys and network id;
* the registry and Discovery Service addresses;
* the Beckn health schema packs and the Sygnal specification;
* routing for Beckn actions and `sygnal/*` actions to your platform's endpoints;
* **selective, header-only audit logging**, so no payload content is logged off the platform;
* telemetry export to the network's address. The repository's [`adapter-config/`](https://github.com/Medtronic-LABS/sygnal/tree/main/adapter-config) folder has a ready-made ONIX allow-list and telemetry block.

### 5. Connect your platform to the adapter

Your platform calls the adapter to send requests (for example `confirm`), and receives incoming requests and callbacks from it. Implement:

* the Beckn actions for the handoffs you take part in, as seeker, provider or both;
* the `sygnal/*` endpoints for your role: at minimum `deviation/flag` (as a counter-party) and `deviation/on_flag` (for flags you raise), and, where the network uses them, `policy/update`, `policy/on_get` and `signal/emit`;
* a mapping between your internal workflow states and the referral `lifecycleState`.

### 6. Publish your catalogue (providers)

If others will find you through discovery:

1. Publish your catalogue: services, coverage and capacity.
2. Add its location to your directory record.

### 7. Fetch your policies (if the network has them)

A network can start without encoded policies; see [Starting without encoded policies](../concepts/policies.md#starting-without-encoded-policies). Where it has them:

1. On start-up, call `policy/get` with your scope to fetch the policies that apply to you.
2. Work out your effective policy and apply it.
3. When a later policy is pushed to you, confirm adoption with `policy/on_update`.

### 8. Test

1. Run the [reference flows](running-reference-flows.md) for your role.
2. Check that no payload content reaches the telemetry address: send a payload with a tag in it, and check that the tag never arrives.

## Moving from an existing Beckn kit

Platforms already running ONIX can usually join by changing configuration:

1. Pin the adapter version.
2. Add the health schema packs and the `sygnal/*` routes.
3. Switch on selective audit logging and telemetry export.
4. Point discovery at the network's Discovery Service.
5. **Replace any shared test keys with your own.**

## Setting up a network instead?

The network operator creates the network's registry and adds a reference to each participant's record, on dedi.global or on its own domain. The NFH [onboarding guide](https://docs.nfh.global/build/onboarding) covers this too. For the governance side (who may join, roles, policies), see [Network governance](../governance/README.md).
