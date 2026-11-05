# Contributing

1. Use Node.js 22.20+ and npm 10.9.4 (matching CI), then run `npm ci`. Use `npm install --global npm@10.9.4` to select that npm version; the `packageManager` field documents it but npm does not enforce it automatically.
2. Read [authoring](docs/authoring.md) before adding skills.
3. Keep every skill self-contained and use the standard flat layout.
4. Run `npm run check` before opening a pull request.
5. Describe the intended trigger, behavior, and agent testing for skill changes.
6. For user-visible changes, run `npm run changeset` and commit the generated release note with the change.

Do not add generated agent installations, secrets, copied third-party skills without license attribution, or unnecessary runtime dependencies. Do not add sample skills just to make an empty catalog installable.
