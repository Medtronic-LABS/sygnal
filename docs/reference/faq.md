---
description: Common questions about Sygnal.
---

# FAQ

### Is Sygnal a platform that health workers log into?

No. Sygnal runs **across** the platforms a health system already uses. Health workers keep using their own apps and EMRs. Sygnal connects those platforms to each other. The dashboards in Network Intelligence are for programme managers and network operators. They show coordination metadata only.

### Does patient data go through Sygnal?

Handoffs between two providers travel directly between them. They carry what the receiving side needs to act. The **shared** network services receive only coordination metadata, as the reporting policy permits. The edge enforces this. The only exception is a narrow notifiable report with a stated legal basis. Clinical records move over the health system's records layer. See [Privacy and data minimisation](../concepts/privacy-and-data-minimisation.md).

### Does Sygnal make clinical decisions or route patients?

No. The centre observes and signals; it never decides. Discovery can suggest possible providers, but the platform or a person makes the choice. Signals are advisory.

Decision support belongs at the edge, with the platform and the health worker. Extensions to the Edge Adapter that help with this are being explored with the Sygnal community, for example checking local data against a care protocol and suggesting when a referral is due. They would run under the platform's control, and the decision would stay with the health worker.

### Why build on Beckn rather than define a new protocol?

Beckn v2 already handles finding a counterpart, agreeing terms, placing a commitment and tracking it. It also handles signing and trust through a registry. It has open-source tools and live networks. Because Sygnal reuses Beckn, a platform that already supports Beckn is most of the way to joining. Sygnal adds APIs only where Beckn has no equivalent. See [Sygnal and other health DPI](../concepts/relationship-to-other-dpi.md).

### How is this different from a health information exchange?

An exchange moves **records**: what happened. Sygnal coordinates **handoffs**: what should happen next, and whether it did. The two work together. An exchange can be the records layer beneath a Sygnal network.

### How is this different from an EMR's own referral module?

A referral module works inside one platform. When a patient moves to a different platform, the module can no longer see what happens. Sygnal follows the handoff across platforms, including SPICE and any other platform that joins.

### What happens if the network services go down?

Peer-to-peer coordination continues. The edge holds deviations and reports in a queue and sends them later. Clinical work never waits on Sygnal.

### Who decides what gets reported?

Each network's governance, through signed coordination policies. A lower level can never allow more data to leave the edge than a higher level permits. See [Coordination policies](../concepts/policies.md).

### Is Sygnal tied to one health system?

No. Any health system (national, regional, programme or private) can run its own network on the same open specification. A national health system is often a collection of many health systems, each of which can run its own network, and those networks are meant to be able to link up. See [Care Coordination Networks](../concepts/care-coordination-networks.md#a-network-of-networks).

### Is Sygnal only for health?

The protocol's core terms are not specific to health. This covers verbs such as `deviation/flag` and `event/report`, and nouns such as `CoordinationEvent`. The health-specific parts sit in the message domain and payload types. Health is the first and current focus.

### Do we have to adopt everything at once?

No. Start with one use case, such as referral tracking between two platforms, and add components as value is proven. See [Getting started](../build/README.md#incremental-adoption).

### Do we have to use the hosted services?

No. Sygnal Network Services exist to make starting easier. The network can run any of them itself, using any implementation of the specification. This includes the Sygnal Platform once it is released. The network can also swap a service later, and participants don't need to change their integration. The hosted services are on the control plane, so they handle coordination metadata only, never patient records. See [Protocol, platform and services](../concepts/protocol-platform-services.md).

### Who owns Sygnal?

The protocol is developed in the open, with partners, and Medtronic LABS leads that work today. Medtronic LABS also develops the Sygnal Platform and operates the hosted services. The intent is for stewardship to move to a neutral governance body, so that no single vendor owns the standard. See [About Sygnal](about.md) and [Network governance](../governance/README.md).
