#!/usr/bin/env python3
"""Check that every CodedValue in the reference flows and spec examples resolves
against the network code lists in codedvalues/attributes.yaml.

A CodedValue is any JSON object carrying "@type" and "code". Objects whose
"@context" is a Beckn schema pack (schema.beckn.io) are pack resources, not coded
values, and are skipped.

Usage: python3 specs/tools/check_codedvalues.py [repo-root]
"""
import json, pathlib, re, sys, collections
import yaml

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
attrs = yaml.safe_load((root / "codedvalues/attributes.yaml").read_text())
lists = {name: set(map(str, cls["properties"]["code"]["enum"]))
         for name, cls in attrs["components"]["schemas"].items()}

OUR_CTX = "https://raw.githubusercontent.com/Medtronic-LABS/sygnal/main/codedvalues/context.jsonld"
errors, seen = [], collections.Counter()

def walk(node, where, env):
    if isinstance(node, dict):
        if isinstance(node.get("@type"), str) and isinstance(node.get("code"), (str, int)):
            ctx = str(node.get("@context", ""))
            ctx = env.get(ctx.strip("{}"), ctx) if ctx.startswith("{{") else ctx
            if "schema.beckn.io" not in ctx:
                t, c = node["@type"], str(node["code"])
                seen[t] += 1
                if ctx != OUR_CTX:
                    errors.append(f"{where}: {t}/{c} uses @context {ctx or '(none)'}, not the network context")
                elif t not in lists:
                    errors.append(f"{where}: unknown @type {t}")
                elif c not in lists[t]:
                    errors.append(f"{where}: {t} has no member {c}")
        for v in node.values():
            walk(v, where, env)
    elif isinstance(node, list):
        for v in node:
            walk(v, where, env)

# Reference flows: resolve {{codedvalue_ctx}} from each folder's environment file.
for coll in sorted(root.glob("reference-flows/*/*Postman_Collection.json")):
    env = {}
    for e in coll.parent.glob("*environment.json"):
        env.update({v["key"]: v["value"] for v in json.loads(e.read_text())["values"]})
    def items(n):
        for it in n.get("item", []):
            yield from items(it) if "item" in it else [it]
    for it in items(json.loads(coll.read_text())):
        raw = it.get("request", {}).get("body", {}).get("raw")
        if not raw:
            continue
        try:
            body = json.loads(re.sub(r'(?<!")\{\{[^}]+\}\}(?!")', "0", raw))
        except json.JSONDecodeError:
            continue
        walk(body, f"{coll.parent.name} / {it['name']}", env)

# Spec examples.
spec = yaml.safe_load((root / "specs/sygnal-coordination-apis.yaml").read_text())
walk(spec, "spec", {})

for t, n in sorted(seen.items()):
    print(f"  {t:32} {n:4} values")
if errors:
    print(f"\nFAIL: {len(errors)} unresolved coded value(s)")
    for e in errors:
        print("  " + e)
    sys.exit(1)
print("\nOK: every coded value resolves against codedvalues/attributes.yaml")
