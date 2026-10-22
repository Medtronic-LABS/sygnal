# Publishing the documentation to GitBook

The `docs/` folder is a GitBook book, synced from this repository with **GitBook Git Sync**.

## One-time setup

1. In GitBook, create a space (for example "Sygnal") and choose **Configure → GitHub Sync**.
2. Select this repository and the branch to publish (normally `main`).
3. Choose **GitHub → GitBook** for the initial sync, so that the repository is the source of truth.
4. GitBook reads [`.gitbook.yaml`](.gitbook.yaml) at the repository root:
   * `root: ./docs/`: only `docs/` is published;
   * `README.md` is the landing page and `SUMMARY.md` is the table of contents.
5. **OpenAPI reference.** The page `docs/specification/api-reference.md` embeds operations from the raw URL of `specs/sygnal-coordination-apis.yaml` on `main`. These blocks render once the specification is on `main` at that URL. Once the first version is tagged, consider pointing the blocks at the tag (for example `.../v0.9.0/specs/...`) so the published reference matches a released version. Optionally, also add the specification to the organisation's OpenAPI specs in GitBook (**OpenAPI → Add specification → From URL**, named `sygnal`) so it refreshes automatically.
6. Publish the space and set its visibility to public.

## Conventions for editors

* **Run the checks** before pushing: `python3 specs/tools/check_links.py .`, `python3 specs/tools/check_codedvalues.py .` and, if the specification changed, `python3 specs/tools/validate.py specs/sygnal-coordination-apis.yaml`.

* **Every page must be listed in `docs/SUMMARY.md`**, or GitBook won't show it.
* **Images** go in `docs/.gitbook/assets/` and are referenced with relative paths.
* **Diagrams:** use fenced ` ```mermaid ` blocks, which GitBook renders natively, or SVG in the assets folder.
* **Links to files outside `docs/`** (specs, reference flows) must be absolute GitHub URLs, because GitBook only publishes `docs/`.
* **GitBook blocks** such as `{% hint style="info" %}…{% endhint %}` render in GitBook but show as plain text on GitHub. Use them sparingly.
* Edits made in the GitBook editor are committed back to the synced branch. Prefer pull requests for substantive changes.

## If the repository is renamed again

GitHub redirects links to renamed repositories, but update the absolute links anyway: search for `github.com/Medtronic-LABS/` and `raw.githubusercontent.com/Medtronic-LABS/`, replace the old name, then reconnect Git Sync. (The repository was renamed from `ccn` to `sygnal` in October 2026.)

## Review before publishing

Pages are reviewed before they appear here. Full drafts live in a private staging repository synced to a private GitBook review space, where invited reviewers comment. Approved pages are then copied into this repository. Two rules keep links working:

* **Published pages never link to pages that haven't been published yet.** Unpublished pages may link to published ones.
* **Run the link check before every push:** `python3 specs/tools/check_links.py .` It fails if any link points to a page that isn't in this repository.

## Before going public: checklist

- [ ] Specification and documentation licence: CC BY-SA 4.0 (decided). Replace the short `LICENSE` notice with the official legal code text from creativecommons.org if you want GitHub to detect the licence automatically.
- [ ] Licence for reference code (for example the validator) decided; Apache-2.0 or MIT are the usual choices, as Creative Commons licences aren't meant for software.
- [ ] Custom domain `docs.sygnal.network` connected to the public GitBook site.
- [ ] The `sygnal:` JSON-LD context URL (`https://spec.sygnal.network/contexts/v0.9.jsonld`) is either published or clearly marked as a placeholder (it is marked in the docs).
- [ ] The repository is public, or the absolute GitHub links will 404 for readers.
