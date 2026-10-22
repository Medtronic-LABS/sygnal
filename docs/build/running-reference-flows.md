---
description: Import and run the use-case Postman collections against a sandbox.
---

# Running the reference flows

Each [use case](../use-cases/README.md) ships an importable **Postman Collection v2.1** and a **self-contained environment** in the repository's [`reference-flows/`](https://github.com/Medtronic-LABS/sygnal/tree/main/reference-flows) folder.

## Quick start

1. **Import** the use case's collection (`Sygnal_UC<n>_…_Postman_Collection.json`) and its environment (`UC<n>_Dev.postman_environment.json`) into Postman.
2. **Select** that environment. Postman allows one active environment at a time, which is why each use case has its own.
3. **Set** `bpp_uri`, `bap_uri`, and any sandbox credentials. `bpp_uri` is the target base URL, and it changes by transaction: for example ComEMR for T1, the campaign platform for UC3, and CARE for UC4's T2.
4. **Check** `network_id`. The shipped value, `example.net/health`, is a placeholder (stub). Replace it with your sandbox network's id. To run against other platforms, join the [Sygnal Sandbox](sandbox.md).
5. **Run** the requests in order. Each folder walks through one transaction. Matched flows (UC3, UC4's T2) start at `discover`, and directed flows start at `select`. The sequence is: `select` → `on_select` → `init` → `on_init` → `confirm` → `on_confirm` (Referral ID issued) → `status` / `update` steps → closure, plus any deviation branch.

## What the collections contain

| Use case | Folders |
|---|---|
| UC1 | Referral coordination (DIGIT HCM → ComEMR), with a `NO_SHOW` deviation branch |
| UC2 | Emergency referral with an `OBSERVER` on the notification roster, and a `PATIENT_CANCELLED` branch |
| UC3 | Matched task-out: `discover` → `confirm` → completion |
| UC4 | `T1 · Referral Coordination`, `T2 · PHU Booking on CARE`, `Relay · CARE progress → T1 status chain` |

## Things to know

* **Envelope version.** `context.version` is `2.0.0`, the Beckn core message version. The health schema packs are v2.1; that version appears in their `@context` URLs.
* **Stubs.** Participant ids, keys and document references are stubs. Signing keys are left empty; supply your own sandbox keys, or let your adapter sign.
* **Coded values.** Every coded value's `@context` is the environment variable `codedvalue_ctx`, which points at the network's [code lists](../specification/coded-values.md). To run the flows against another network's lists, change that one variable.
* **Shared values.** Network-wide values are duplicated across the per-use-case environments. Keep them in sync when they change.
* **Scope.** The collections test the **peer-to-peer core**: Beckn transitions, with deviations carried inside the Beckn messages (in-band). Collections for the `sygnal/*` APIs are on the [roadmap](../roadmap.md). In the meantime, the [OpenAPI reference](../specification/api-reference.md) has validated example payloads for every Sygnal API.
