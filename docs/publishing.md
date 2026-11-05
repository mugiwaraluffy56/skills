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

After testing newly added or changed skills:

1. Update `CHANGELOG.md`.
2. Bump the version in both `package.json` and `.claude-plugin/plugin.json`.
3. Run `npm install --package-lock-only` to sync the lockfile.
4. Run `npm run check`, commit, and tag the version (for example `v0.1.1`).
5. Push the commit and tag; optionally create a GitHub release.

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
