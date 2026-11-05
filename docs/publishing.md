# Publishing

## First push

The GitHub repository is `mugiwaraluffy56/skills`. For a fresh local checkout without a configured remote:

1. Verify the repository path in `README.md` matches the intended remote.
2. Review the plugin marketplace owner and names in `.claude-plugin/`.
3. Review the MIT license and copyright holder.
4. Run `npm ci` and `npm run check`.
5. Commit and push:

```bash
git add .
git commit -m "Initialize skills repository scaffold"
git remote add origin https://github.com/mugiwaraluffy56/skills.git
git push -u origin main
```

If the remote already contains commits, reconcile its history first rather than force-pushing. No npm publishing is needed; the skills CLI installs directly from GitHub. Private repositories require Git credentials with access.

Publishing the empty scaffold is fine, but skill discovery will return no skills until you add one. Do not advertise an empty catalog as an installable skill pack.

## Releases

For user-visible changes, run `npm run changeset` and commit the generated entry with the change. Select `personal-skills-tooling` even though the repository is not an npm-distributed package.

On `main`, the release workflow opens or updates a version PR. Its version command consumes changesets, updates the changelog and package version, syncs plugin metadata and the lockfile, then runs the checks. Review and merge that PR; the next run creates and pushes the version tag. No npm credentials are needed and nothing is published to npm.

### GitHub setup

In repository **Settings → Actions → General → Workflow permissions**, enable **Allow GitHub Actions to create and approve pull requests**. Organization policies may restrict this setting. The release job requests only repository contents and pull-request write permissions through `GITHUB_TOKEN`.

PRs created with the default `GITHUB_TOKEN` do not trigger other workflows. The release job runs checks itself, but repositories requiring a separate PR check may need an approved GitHub App token to trigger that check, or a maintainer-run validation workflow. Do not bypass required checks to merge a release PR.

### Manual fallback

With pending changesets committed, run `npm run version:skills`, review and commit the generated changes, then push. Run `npm run release` to create a local tag and `git push origin --tags` to publish tags you have reviewed. Changesets tags this single-package repository as `v<version>`. Avoid mixing manual and automated release operations at the same time.

For reproducible CLI installs, consumers can use a tag URL as the source:

```bash
npx skills@latest add https://github.com/mugiwaraluffy56/skills/tree/v0.1.1
```

## Smoke test after adding the first skill

From a disposable project, run `npx skills@latest add mugiwaraluffy56/skills --list`, install a named skill for the desired agent, and verify its behavior. Separately test `/plugin marketplace add mugiwaraluffy56/skills` and `/plugin install personal-skills@personal-skills` inside Claude Code. CI checks structure, not live agent compatibility.

## Design references

- [Matt Pocock's skills](https://github.com/mattpocock/skills): standard skill distribution and plugin marketplace.
- [gstack](https://github.com/garrytan/gstack): end-to-end tooling; its browser/runtime setup is unnecessary for an empty Markdown-first collection.
- [skills CLI discovery rules](https://github.com/vercel-labs/skills/blob/main/docs/creating-skills.md).
