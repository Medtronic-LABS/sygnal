"""Validate the Sygnal coordination API spec.

Usage:  python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml
Needs:  pip install pyyaml openapi-spec-validator jsonschema rfc3987
"""
import sys, json, copy, yaml
from openapi_spec_validator import OpenAPIV31SpecValidator
from jsonschema import Draft202012Validator, FormatChecker

path = sys.argv[1]
raw = open(path, encoding="utf-8").read()

# 1. YAML well-formedness + duplicate-key detection (safe_load silently overwrites dupes)
class DupLoader(yaml.SafeLoader): pass
dups = []
def construct_mapping(loader, node, deep=False):
    seen = set()
    for k, _ in node.value:
        key = loader.construct_object(k, deep=deep)
        if key in seen: dups.append((key, k.start_mark.line + 1))
        seen.add(key)
    return yaml.SafeLoader.construct_mapping(loader, node, deep)
DupLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, construct_mapping)
doc = yaml.load(raw, Loader=DupLoader)
print("[1] YAML parse: OK" + ("" if not dups else f"  DUPLICATE KEYS: {dups}"))

# 2. OpenAPI 3.1 structure + $ref resolution (collect ALL errors, not just first)
errs = list(OpenAPIV31SpecValidator(doc).iter_errors())
print(f"[2] OpenAPI 3.1 structure/$ref: {'OK' if not errs else f'{len(errs)} error(s)'}")
for e in errs: print("    -", e.message, "@", list(e.path))

# explicit internal $ref sweep (belt and braces)
def walk(n, p=""):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == "$ref" and isinstance(v, str): yield p, v
            else: yield from walk(v, f"{p}/{k}")
    elif isinstance(n, list):
        for i, v in enumerate(n): yield from walk(v, f"{p}/{i}")
def resolve(ref):
    node = doc
    for part in ref.lstrip("#/").split("/"): node = node[part]
    return node
bad = []
refs = list(walk(doc))
for p, r in refs:
    try: resolve(r)
    except Exception: bad.append((p, r))
print(f"    internal $refs: {len(refs)} checked, {len(bad)} unresolved {bad if bad else ''}")

# unused components
used = {r for _, r in refs}
unused = [f"#/components/{sec}/{n}" for sec in doc["components"] for n in doc["components"][sec]
          if f"#/components/{sec}/{n}" not in used]
print(f"    unused components: {unused or 'none'}")

# 3. example-vs-schema (2020-12, refs resolved against the whole doc, formats asserted)
fc = FormatChecker()
def validator_for(schema):
    root = {"components": doc["components"], **schema} if isinstance(schema, dict) else schema
    return Draft202012Validator(root, format_checker=fc)
# 2b. Deprecated Schema Object `example` (OAS 3.1: use JSON Schema `examples` array)
def find_example(n, p=""):
    if isinstance(n, dict):
        for k, v in n.items():
            if k == "example": yield p
            yield from find_example(v, f"{p}/{k}")
    elif isinstance(n, list):
        for i, v in enumerate(n): yield from find_example(v, f"{p}/{i}")
depr = list(find_example(doc["components"].get("schemas", {}), "#/components/schemas"))
print(f"    deprecated 'example' keywords: {depr or 'none'}")

# 2c. Stray keywords inside schemas (e.g. an unquoted comma in a flow-style description
#     silently creates a junk key; JSON Schema ignores unknown keywords, so [2] can't see it)
KW = set("""$ref $schema $id $anchor $defs $comment $dynamicRef $dynamicAnchor type enum const properties required
additionalProperties items prefixItems minItems maxItems uniqueItems contains allOf anyOf oneOf not if then else format
description title default examples example readOnly writeOnly deprecated minimum maximum exclusiveMinimum exclusiveMaximum
multipleOf minLength maxLength pattern patternProperties propertyNames minProperties maxProperties dependentRequired
dependentSchemas unevaluatedProperties unevaluatedItems discriminator xml externalDocs contentMediaType contentEncoding""".split())
stray = []
def chk(s, p):
    if not isinstance(s, dict): return
    stray.extend((p, k) for k in s if k not in KW and not k.startswith("x-"))
    for k in ("properties", "patternProperties", "$defs"):
        for n, sub in (s.get(k) or {}).items(): chk(sub, f"{p}/{k}/{n}")
    for k in ("items", "additionalProperties", "not", "if", "then", "else", "contains"):
        if isinstance(s.get(k), dict): chk(s[k], f"{p}/{k}")
    for k in ("allOf", "anyOf", "oneOf"):
        for i, sub in enumerate(s.get(k) or []): chk(sub, f"{p}/{k}/{i}")
for n, s in doc["components"]["schemas"].items(): chk(s, f"#/components/schemas/{n}")
for pth, it in doc["paths"].items():
    for op in it.values():
        rb = (op.get("requestBody") or {}).get("content", {}).get("application/json", {}).get("schema")
        if rb: chk(rb, pth)
print(f"    stray schema keywords: {stray or 'none'}")

print("[3] Schema examples vs schemas (Draft 2020-12, format-asserting):")
fails = len(depr) + len(stray)
for name, sch in doc["components"]["schemas"].items():
    for i, ex in enumerate(sch.get("examples") or []):
        es = list(validator_for({"$ref": f"#/components/schemas/{name}"}).iter_errors(ex))
        fails += bool(es)
        print(f"    {name}[{i}]: {'OK' if not es else [e.message + ' @ ' + '/'.join(map(str,e.path)) for e in es]}")
    for pn, ps in (sch.get("properties") or {}).items():
        if isinstance(ps, dict):
            for i, ex in enumerate(ps.get("examples") or []):
                es = list(validator_for(ps).iter_errors(ex))
                fails += bool(es)
                print(f"    {name}.{pn}[{i}]: {'OK' if not es else [e.message for e in es]}")
# 4. Envelope check: build each request body from the component examples and validate
ctx = {"version":"2.0.0","networkId":"sygnal.example/care-net",
       "senderId":"sender.example","receiverId":"receiver.example",
       "transactionId":"7f1c2a4e-3b5d-4e6f-8a9b-0c1d2e3f4a5b","messageId":"1a2b3c4d-5e6f-4a7b-8c9d-0e1f2a3b4c5d",
       "timestamp":"2026-07-01T09:15:00Z"}
ex = {n: (s.get("examples") or [None])[0] for n, s in doc["components"]["schemas"].items()}
ex["Query"] = {"ref": "policy:moh:coverage"}
print("[4] Assembled request envelopes vs each path's requestBody schema:")
for pth, item in doc["paths"].items():
    body_schema = item["post"]["requestBody"]["content"]["application/json"]["schema"]
    msg_s = body_schema["properties"]["message"]
    if "$ref" in msg_s: msg = ex[msg_s["$ref"].split("/")[-1]]
    elif "policies" in (msg_s.get("properties") or {}): msg = {"policies": [ex["CoordinationPolicy"]]}
    else: msg = {"policyId": "policy:moh:coverage", "events": [ex["CoordinationEvent"]]}
    env = {"context": {**ctx, "action": pth.lstrip("/")}, "message": msg}
    es = list(validator_for(body_schema).iter_errors(env))
    wrong = {"context": {**ctx, "action": "sygnal/wrong/verb"}, "message": msg}
    neg = list(validator_for(body_schema).iter_errors(wrong))
    nonet = {"context": {k: v for k, v in env["context"].items() if k != "networkId"}, "message": msg}
    neg2 = list(validator_for(body_schema).iter_errors(nonet))
    legacy = {"context": {**env["context"], "bapId": "sender.example"}, "message": msg}
    neg3 = list(validator_for(body_schema).iter_errors(legacy))
    fails += bool(es) + (not neg) + (not neg2) + (not neg3)
    print(f"    {pth}: {'OK' if not es else [e.message for e in es]}; rejects wrong-action/no-networkId/bapId: "
          f"{bool(neg)}/{bool(neg2)}/{bool(neg3)}")

# 5. Trust alignment with Beckn core / NFH-007
print("[5] Trust alignment (NFH-007):")
t = []
if doc.get("security") != []: t.append("root `security: []` missing")
C = doc["components"]
for pth, item in doc["paths"].items():
    op = item["post"]; refs = [p.get("$ref", "") for p in op.get("parameters", [])]
    want = "CallbackAuthorizationHeader" if pth.rsplit("/", 1)[-1].startswith("on_") else "AuthorizationHeader"
    if refs != [f"#/components/parameters/{want}"]: t.append(f"{pth}: signs with {refs}, expected {want}")
for rn, r in C["responses"].items():
    if (r.get("headers") or {}).get("Signature", {}).get("$ref") != "#/components/headers/AckSignatureHeader":
        t.append(f"response {rn}: no AckSignatureHeader")
sc = C["schemas"].get("SygnalContext", {})
if sc.get("additionalProperties") is not False: t.append("SygnalContext is not closed")
if any(k in (sc.get("properties") or {}) for k in ("bapId", "bppId", "bapUri", "bppUri")): t.append("SygnalContext declares bap*/bpp*")
if not {"senderId", "receiverId", "networkId"} <= set(sc.get("required") or []): t.append("SygnalContext must require senderId, receiverId, networkId")
for u in ("senderUri", "receiverUri"):
    if (sc.get("properties") or {}).get(u, {}).get("format") != "uri": t.append(f"SygnalContext.{u} must be declared with format uri")
    if u in (sc.get("required") or []): t.append(f"SygnalContext.{u} must be optional")
if "counterSignature" in raw: t.append("body-level counterSignature present (NFH-007 puts receipt in the Signature header)")
for n in ("AuthorizationHeader", "CallbackAuthorizationHeader"):
    if C["parameters"][n]["schema"].get("$ref") not in ("#/components/schemas/Signature", "#/components/schemas/CallbackSignature"):
        t.append(f"{n} not typed by a core signature schema")
print("    " + ("OK — security:[], per-path signing, signed responses, no body counter-signature, closed sender/receiver context" if not t else "\n    ".join(t)))
fails += len(t)
# 6. Policy & reporting rules (v0.9 public draft) — positive and negative cases
print("[6] Policy & reporting rules:")
S = lambda n: validator_for({"$ref": f"#/components/schemas/{n}"})
ok = lambda n, inst: not list(S(n).iter_errors(inst))
def body_ok(pth, msg, ctx_extra=None):
    bs = doc["paths"][pth]["post"]["requestBody"]["content"]["application/json"]["schema"]
    return not list(validator_for(bs).iter_errors({"context": {**ctx, "action": pth.lstrip("/"), **(ctx_extra or {})}, "message": msg}))
cev, pol = ex["CoordinationEvent"], ex["CoordinationPolicy"]
strip = lambda d, *ks: {k: v for k, v in d.items() if k not in ks}
indiv = {"@type": "sygnal:CoordinationEvent", "eventType": "NOTIFIABLE_CASE", "granularity": "INDIVIDUAL",
         "occurredAt": "2026-07-02T10:00:00Z", "subjectRef": {"algorithm": "BLAKE2b-512", "value": "b2:ab12"},
         "subjectType": "PATIENT", "caseDetail": {"condition": "measles", "onsetDate": "2026-06-29",
         "area": {"code": "XX-D01-12", "level": "subdistrict"}}}
inst = {"@type": "sygnal:InstrumentationSection", "level": "PER_TRANSACTION"}
cases = [
  ("AGGREGATE event without period is rejected", not ok("CoordinationEvent", strip(cev, "period"))),
  ("AGGREGATE event without id is rejected", not ok("CoordinationEvent", strip(cev, "id"))),
  ("INDIVIDUAL event needs no period/id", ok("CoordinationEvent", indiv)),
  ("metric code must match the code pattern", not ok("CoordinationEvent", {**cev, "metrics": {"Households Reached": 3}})),
  ("free-text area is rejected (coded Area only)", not ok("CoordinationEvent", {**cev, "area": "Bo district"})),
  ("PER_TRANSACTION without until is rejected", not ok("InstrumentationSection", inst)),
  ("PER_TRANSACTION with until is accepted", ok("InstrumentationSection", {**inst, "until": "2026-07-08T00:00:00Z"})),
  ("PrecedenceSection in a scoped policy is rejected", not ok("CoordinationPolicy", {**ex["CoordinationPolicy"], "sections": [{"@type": "sygnal:PrecedenceSection", "levels": ["network"]}]})),
  ("extension section may not use the sygnal: namespace", not ok("CoordinationPolicy", {**pol, "sections": [{"@context": "https://x.example/c.jsonld", "@type": "sygnal:Foo"}]})),
  ("critical extension section is schema-valid", ok("CoordinationPolicy", {**pol, "sections": [{"@context": "https://x.example/c.jsonld", "@type": "acme:Thing", "critical": True}]})),
  ("legacy policy `status` is rejected", not ok("CoordinationPolicy", {**pol, "status": "APPLIED"})),
  ("legacy DeviationReport `status` is rejected", not ok("DeviationReport", {**ex["DeviationReport"], "status": "OPEN"})),
  ("legacy SharedPlan `status` is rejected", not ok("SharedPlan", {**ex["SharedPlan"], "status": "PUBLISHED"})),
  ("FULL_INSTRUMENTATION is no longer a reportingMode", not ok("ReportingSection", {**pol["sections"][0], "reportingMode": "FULL_INSTRUMENTATION"})),
  ("request with senderUri is accepted", body_ok("/sygnal/deviation/flag", ex["DeviationReport"], {"senderUri": "https://edge.example.org/sygnal"})),
  ("callback with receiverUri is accepted", body_ok("/sygnal/deviation/on_flag", ex["DeviationReport"], {"receiverUri": "https://edge.example.org/sygnal"})),
  ("non-URI senderUri is rejected", not body_ok("/sygnal/deviation/flag", ex["DeviationReport"], {"senderUri": "not a uri"})),
  ("undeclared callbackUrl header field is rejected", not body_ok("/sygnal/deviation/flag", ex["DeviationReport"], {"callbackUrl": "https://x.example"})),
  ("InstrumentationSection level OFF parses as a string", ok("InstrumentationSection", {"@type": "sygnal:InstrumentationSection", "level": "OFF"})),
  ("free-text expectedState is rejected (CodedValue only)", not ok("DeviationReport", {**ex["DeviationReport"], "expectedState": "COVERED"})),
  ("free-text respondentStatusReason is rejected (CodedValue only)", not ok("DeviationReport", {**ex["DeviationReport"], "respondentStatusReason": "called the facility"})),
  ("coded respondentStatusReason is accepted", ok("DeviationReport", {**ex["DeviationReport"], "respondentStatus": "RESOLVED", "respondentStatusReason": {"@context": "https://x.example/c.jsonld", "@type": "sygnal:DeviationStatusReason", "code": "ACTION_TAKEN"}})),
  ("CodedValue without @context is rejected", not ok("CodedValue", {"@type": "sygnal:CoverageState", "code": "COVERED"})),
  ("CodedValue with an extra free-text field is rejected", not ok("CodedValue", {"@context": "https://x.example/c.jsonld", "@type": "sygnal:CoverageState", "code": "MISSED", "note": "x"})),
  ("policy/on_get with an empty set is rejected", not body_ok("/sygnal/policy/on_get", {"policies": []})),
]
for name, schema in doc["components"]["schemas"].items():
    for i, e in enumerate(schema.get("examples") or []):
        for sec in (e.get("sections") or []) if isinstance(e, dict) else []:
            if sec.get("@type") == "sygnal:ReportingSection" and "reportingMode" in sec:
                want = "INDIVIDUAL_NOTIFIABLE_PLUS_AGGREGATE" if (sec["dataMinimization"]["individual"].get("appliesToConditions")) else "AGGREGATE_ONLY"
                cases.append((f"{name}[{i}] reportingMode agrees with dataMinimization", sec["reportingMode"] == want))
for label, passed in cases:
    fails += not passed
    print(f"    {'OK  ' if passed else 'FAIL'} {label}")
print("RESULT:", "ALL CHECKS PASSED" if not (dups or errs or bad or fails) else "FINDINGS PRESENT")
sys.exit(0 if not (dups or errs or bad or fails) else 1)
