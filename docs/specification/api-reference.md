---
description: The rendered OpenAPI 3.1 reference for the Sygnal coordination APIs (v0.9 public draft).
---

# OpenAPI reference

The authoritative definition of the Sygnal APIs is the OpenAPI 3.1 document [`specs/sygnal-coordination-apis.yaml`](https://github.com/Medtronic-LABS/sygnal/blob/main/specs/sygnal-coordination-apis.yaml). [Download the raw file](https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml).

## Validate it yourself

```bash
pip install pyyaml openapi-spec-validator jsonschema rfc3987
python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml
```

The validator checks:

* YAML well-formedness, including duplicate keys;
* OpenAPI 3.1 structure and `$ref` resolution;
* every schema example against its schema (JSON Schema 2020-12, with formats asserted);
* a request envelope built for each of the 14 paths;
* trust alignment with Beckn v2 core;
* positive and negative cases for the policy and reporting rules.

## Operations

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/deviation/flag" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/deviation/on_flag" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/event/report" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/policy/update" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/policy/on_update" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/plan/sync" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/plan/on_sync" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/signal/emit" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/policy/get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/policy/on_get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/deviation/get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/deviation/on_get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/plan/get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}

{% openapi src="https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml" path="/sygnal/plan/on_get" method="post" %}
https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/specs/sygnal-coordination-apis.yaml
{% endopenapi %}
