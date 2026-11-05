# Repository instructions

This repository distributes reusable agent skills, not an application. Keep the scaffold empty until the user explicitly requests adding or importing skills; examples in documentation are not permission to create sample skills.

The user has requested empty `plan`, `implement`, `test`, `review`, and `ship` placeholders. Keep them as `.gitkeep`-only directories until their implementation is requested; they are not discoverable skills.

## Working rules

- Use `GLOSSARY.md` for domain terminology; update it when a term's meaning changes.
- Before adding or changing a skill, read `docs/authoring.md` for layout, format, portability, and testing requirements.
- Before changing installation, plugin metadata, or releases, read `docs/publishing.md` and keep the README's installation instructions consistent.
- Keep shared repository instructions here. `CLAUDE.md` imports this file rather than duplicating it.
- Keep skills self-contained. Repository tooling supports development; installed skills must not depend on it.
- Preserve default plugin discovery instead of maintaining a separate skill catalog in plugin metadata.
- Leave remote placeholders unresolved until the user supplies the repository URL. Publishing, pushing, and changing installed agent configurations require a user request.

## Verification

Use `npm ci` to install development dependencies and `npm run check` to validate metadata, skill structure, and validator tests. Run the checks after changes and report failures or checks you could not run.

An empty catalog passing validation means the scaffold is valid, not that there is anything to install. Structural checks do not establish live agent compatibility; test affected installation paths in a disposable consumer project when skills are available.
