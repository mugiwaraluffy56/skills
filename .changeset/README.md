# Changesets

For a user-visible change, run `npm run changeset`, select `personal-skills-tooling`, choose the version bump, and describe the change. Commit the generated Markdown file with your work.

- **patch**: corrections that preserve the existing workflow.
- **minor**: new skills or backward-compatible capabilities.
- **major**: breaking changes to existing workflows or installation.

The release workflow opens a version PR on `main`. Merging it allows the workflow to tag the release. This repository stays private to npm (`private: true`); skills are distributed through GitHub, not the npm registry.

See [publishing](../docs/publishing.md) for prerequisites and manual release instructions.
