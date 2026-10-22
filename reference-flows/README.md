# reference-flows: runnable use-case flows

One folder per use case. Each holds a **Postman Collection v2.1** and a **self-contained Postman environment**:

| Folder | Use case |
|---|---|
| [`UC1-upward-fever-referral/`](UC1-upward-fever-referral/) | [UC1: Upward fever referral](../docs/use-cases/uc1-upward-fever-referral.md) |
| [`UC2-upward-mnch-danger-sign/`](UC2-upward-mnch-danger-sign/) | [UC2: Upward MNCH danger-sign referral](../docs/use-cases/uc2-upward-mnch-danger-sign.md) |
| [`UC3-downward-task-out/`](UC3-downward-task-out/) | [UC3: Downward task-out](../docs/use-cases/uc3-downward-task-out.md) |
| [`UC4-separate-system-escalation/`](UC4-separate-system-escalation/) | [UC4: Escalation to a separate system](../docs/use-cases/uc4-separate-system-escalation.md) |

How to run them: [Running the reference flows](../docs/build/running-reference-flows.md).

## Conventions

* Collection: `Sygnal_UC<n>_<Title>_Postman_Collection.json`. Environment: `UC<n>_Dev.postman_environment.json`.
* The JSON files are the source of truth. They are maintained by hand.
* All identifiers, keys and the network ID are **stubs**: placeholder values, not real ones. Never commit real keys or tokens.
