---
description: How the Sygnal specification is versioned, and what changed in each published version.
---

# Versioning and changelog

## Versioning

* The specification uses [semantic versioning](https://semver.org/). Before 1.0, a minor version (0.**x**) may contain breaking changes; each one is called out below.
* Edges and network services declare which specification version they support. They pin a **released** version, never the main branch.
* The Beckn core message version (`context.version`, currently `2.0.0`) is independent of the Sygnal specification version.
* Once there is more than one released version, this page will keep a compatibility matrix (specification version × component version).

## 0.9.0: first public draft (October 2026)

Published by Medtronic LABS on behalf of the Sygnal project.

The first published version of the Sygnal coordination APIs.

**Scope**

* Five write APIs: `deviation/flag`, `event/report`, `policy/update`, `plan/sync`, `signal/emit`, with their callbacks.
* Three reads modelled on Beckn `status`: `policy/get`, `deviation/get`, `plan/get`, sharing one `Query` selector.
* `SygnalContext`: a closed header, a profile of Beckn v2 `Context` using `senderId`/`receiverId`, with optional `senderUri`/`receiverUri`.
* Beckn v2 authentication and trust (NFH-007) adopted without changes in this version, plus per-action role authorization.
* `CoordinationPolicy` with typed sections (Reporting, SLA, Instrumentation, Precedence, extensions), a `critical` flag, declared precedence, and the fixed rule that data minimisation always merges to the most restrictive result.
* Aggregate reporting with `period`, coded `Area`, `id`/`revision` corrections, a metric catalogue and `minCellSize`. A limited exception for individual reporting of notifiable conditions.
* Separation of coordination events from network telemetry.
* Fully coded deviations: `DeviationReport` states and status reasons are `CodedValue`s (the Beckn DHP `{@context, @type, code, display}` pattern), with draft Sygnal code lists in `codedvalues/`.
* Network-owned code lists: every coded value in the reference flows, including those in Beckn health and service pack payloads, resolves against the network's lists in `codedvalues/`.

**Not yet included:** attestation (`attestation/attest`); notifiable reporting by reference; a published `sygnal:` JSON-LD vocabulary (the `@context` URL is a placeholder).

**Note for early implementers:** this version combines several internal drafts. It is the baseline for public review; earlier internal drafts are not supported.
