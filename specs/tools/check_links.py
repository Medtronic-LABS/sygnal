#!/usr/bin/env python3
"""Check that every internal link in the repository's Markdown resolves,
and that each docs page's front matter is valid YAML, its description fits
GitBook's limit, and it uses no footnotes (GitBook does not display them).

Checks relative links between Markdown files (and to other files in the repo),
heading anchors (#section), and that every page in docs/SUMMARY.md exists.
A page that has been held back from publishing won't exist here, so any link
to it fails this check.

Usage: python3 specs/tools/check_links.py [repo-root]
"""
import re, sys, pathlib

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
LINK = re.compile(r'\]\(([^)\s]+)\)')

def anchors(path):
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return {re.sub(r"[^\w\- ]", "", h.strip().lower()).replace(" ", "-")
            for h in re.findall(r"^#{1,6} (.+)$", text, re.M)}

errors = []
for md in sorted(root.rglob("*.md")):
    if ".git" in md.parts or "node_modules" in md.parts:
        continue
    text = re.sub(r"```.*?```", "", md.read_text(encoding="utf-8"), flags=re.S)
    for target in LINK.findall(text):
        if re.match(r"^[a-z]+:", target):          # http:, https:, mailto:
            continue
        path, _, anchor = target.partition("#")
        dest = (md.parent / path).resolve() if path else md
        rel = md.relative_to(root)
        if not dest.exists():
            errors.append(f"{rel}: broken link -> {target}")
        elif anchor and dest.suffix == ".md" and anchor not in anchors(dest):
            errors.append(f"{rel}: missing anchor -> {target}")

# Front matter must be valid YAML (GitBook refuses to sync otherwise).
try:
    import yaml
    for md in sorted((root / "docs").rglob("*.md")):
        text = md.read_text(encoding="utf-8")
        if text.startswith("---\n"):
            try:
                yaml.safe_load(text.split("---\n", 2)[1])
            except yaml.YAMLError as e:
                errors.append(f"{md.relative_to(root)}: front matter is not valid YAML ({str(e).splitlines()[0]})")
            else:
                desc = (yaml.safe_load(text.split("---\n", 2)[1]) or {}).get("description", "")
                if len(str(desc)) > 200:
                    errors.append(f"{md.relative_to(root)}: description is {len(str(desc))} characters; GitBook cuts it at about 200")
        if "[^" in re.sub(r"```.*?```", "", text, flags=re.S):
            errors.append(f"{md.relative_to(root)}: uses Markdown footnotes ([^n]), which GitBook does not display")
except ImportError:
    print("note: PyYAML not installed; front matter not checked")

summary = root / "docs" / "SUMMARY.md"
if summary.exists():
    for target in LINK.findall(summary.read_text(encoding="utf-8")):
        if not (summary.parent / target).exists():
            errors.append(f"docs/SUMMARY.md: page not found -> {target}")

if errors:
    print(f"FAIL: {len(errors)} problem(s)")
    print("\n".join("  " + e for e in errors))
    sys.exit(1)
print("OK: all internal links resolve; front matter is valid")
