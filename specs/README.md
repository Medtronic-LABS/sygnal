# specs: the Sygnal coordination API specification

| File | What |
|---|---|
| [`sygnal-coordination-apis.yaml`](sygnal-coordination-apis.yaml) | OpenAPI 3.1 definition of the Sygnal coordination APIs. **v0.9.0, public draft.** |
| [`tools/validate.py`](tools/validate.py) | Validator. Run it after every change. |

```bash
pip install pyyaml openapi-spec-validator jsonschema rfc3987
python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml
```

The human-readable specification is in the documentation under [`docs/specification/`](../docs/specification/README.md).

## Upstream

The Beckn core components (signatures, request digest, `Ack`, `Error`) are mirrored verbatim from the canonical Beckn v2 `beckn.yaml` (marked `x-mirrors`), so that this file validates standalone. Production implementations should reference the canonical file. When extensions need offline `$ref` resolution, pin the Beckn protocol specification and the Beckn health schema packs as release-pinned git submodules under `upstream/`, never `main`.

## Changing the specification

1. Edit the YAML.
2. Run the validator. All checks must pass.
3. Update the affected pages under `docs/specification/` and add an entry to [`docs/specification/changelog.md`](../docs/specification/changelog.md).
4. Record any non-obvious design choice as a decision record, with its context and consequences.
