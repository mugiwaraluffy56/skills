# skills

My personal agent skills for building production-grade software, from idea to release.

I'm putting together the workflows I want my coding agents to follow: planning features, writing code, testing it, reviewing changes, and shipping. Small, focused skills I can use across projects and agents without repeating the same instructions every time.

This is where I'll maintain them. **No skills added yet—just the foundation.**

## Install

Once I've added skills, you can install them with the [skills CLI](https://skills.sh):

```bash
npx skills@latest add mugiwaraluffy56/skills
```

Pick the skills and coding agents you want during setup. It supports Claude Code, Codex, OpenCode, Cursor, and other agents.

```bash
# Make them available across your projects for the agents you select
npx skills@latest add mugiwaraluffy56/skills -g

# See what's available without installing
npx skills@latest add mugiwaraluffy56/skills --list

# Install one skill for OpenCode
npx skills@latest add mugiwaraluffy56/skills --skill SKILL-NAME -a opencode
```

The CLI needs Node.js 22.20+. The catalog is empty right now, so there's nothing to install yet.

### Claude Code plugin

If you prefer plugins, run these inside Claude Code:

```text
/plugin marketplace add mugiwaraluffy56/skills
/plugin install personal-skills@personal-skills
```

Use either the plugin or the skills CLI for Claude Code, not both, so you don't end up with duplicates. The plugin name is `personal-skills`; the GitHub repository is `skills`.

### From a local checkout

After adding a skill, run this from the project where you want to use it:

```bash
npx skills@latest add /absolute/path/to/skills
```

For local Claude Code plugin development, run `claude --plugin-dir .` from this repository. Restart your agent if new skills don't show up.

## Update or remove

For skills installed through the CLI:

```bash
npx skills@latest check
npx skills@latest update
npx skills@latest remove
```

Check the prompts—these commands can include skills from other repositories too. For the Claude Code plugin, use `/plugin` to manage updates or uninstall it.

## How I'm organizing this

Each skill will live in `skills/<name>/SKILL.md`, with its own supporting resources when needed. I'm using the standard [Agent Skills](https://agentskills.io) format rather than building a custom installer or runtime.

```text
skills/             The skills themselves (empty for now)
.claude-plugin/     Claude Code plugin and marketplace metadata
.github/workflows/  CI checks
docs/               Authoring and publishing notes
scripts/            Repository validation
tests/              Tests for the validator
AGENTS.md           Shared instructions for agents working in this repo
CLAUDE.md           Loads the shared instructions for Claude Code
GLOSSARY.md         Shared terminology
```

## Working on the repo

```bash
npm ci
npm run check
```

The tooling needs Node.js 22.20+. You don't need to install this repository's npm dependencies just to use its skills.

More details: [authoring](docs/authoring.md), [publishing](docs/publishing.md), and [contributing](CONTRIBUTING.md).

## License

[MIT](LICENSE).
