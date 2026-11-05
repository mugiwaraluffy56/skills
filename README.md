# Agent Skills

Reusable engineering workflows for coding agents, from researching existing software to validating complete features. Each skill is independent, project-agnostic, and installable into Codex, Claude Code, OpenCode, Cursor, and other compatible agents.

## Skills

| Skill | When to use it | Outcome |
| --- | --- | --- |
| [`oss-reuse-atlas`](skills/oss-reuse-atlas/SKILL.md) | Starting a software project, researching alternatives, or looking for code and product references | An evidence-backed catalog of comparable open-source applications and reusable modules, with commit-pinned implementation dossiers, license checks, and reuse decisions. **Research only: no implementation plan.** |
| [`feature-discovery`](skills/feature-discovery/SKILL.md) | Before implementing a substantial feature, integration, or product workflow | A validated user journey, capability/compatibility matrix, source-backed requirements, justified constraints, and measurable acceptance criteria. |
| [`production-vertical-slice`](skills/production-vertical-slice/SKILL.md) | Building an accepted feature across frontend, API, state, workers, external services, or other relevant boundaries | A functional end-to-end user journey, tests for success and failure, and accurate verification evidence. |
| [`adversarial-acceptance`](skills/adversarial-acceptance/SKILL.md) | After feature implementation or when a feature passes tests but still feels incomplete | An independent review that challenges the scope, compatibility, behavior, recovery, security, UX, and claims of production readiness. |

The skills complement existing project instructions, acceptance gates, testing tools, and implementation skills (including Matt Pocock's `implement`). They do not impose Klyna-specific architecture or dependencies on other projects.

## Install

Install with the [skills CLI](https://skills.sh):

```bash
npx skills@latest add mugiwaraluffy56/skills
```

Choose which skills and coding agents to install. For **global availability across projects** for the selected agent(s):

```bash
npx skills@latest add mugiwaraluffy56/skills -g
```

List available skills without installing:

```bash
npx skills@latest add mugiwaraluffy56/skills --list
```

Install an individual skill for a specific agent (example: OpenCode):

```bash
npx skills@latest add mugiwaraluffy56/skills --skill oss-reuse-atlas -a opencode -g
```

The CLI requires Node.js 22.20+. Global installation **makes a skill available**, but does not automatically invoke it when you open a project. Invoke it explicitly using your agent's skill mechanism.

### Claude Code plugin

Inside Claude Code:

```text
/plugin marketplace add mugiwaraluffy56/skills
/plugin install personal-skills@personal-skills
```

Avoid installing the same collection through both plugin and skills CLI for Claude Code unless you intentionally want duplicated discovery.

### From a local checkout

```bash
npx skills@latest add /absolute/path/to/skills
```

To test the plugin locally, run `claude --plugin-dir .` in the repository. Restart agents if newly installed skills do not appear.

## Usage

Start a new project with a **research-only** reference collection:

```text
Use $oss-reuse-atlas to find a broad, evidence-backed library of open-source
applications like this project and related reusable implementations. Pin source
revisions, inspect actual code/tests and licenses, and record precise reuse
options. Do not create an implementation plan, milestones, tickets, or code.
```

Before and after implementing a feature:

```text
Use $feature-discovery to investigate the full user journey, official API
capabilities, representative open-source implementations, compatibility,
edge cases, and justified constraints. Use $production-vertical-slice to build
the accepted feature with real end-to-end behavior. Finally, use
$adversarial-acceptance to challenge the result against my original request.
```

Use only the skills relevant to the task. All have their own `SKILL.md` and supporting references or scripts. The research skill's validator is optional and uses Python's standard library; it validates the **artifact structure**, not the truth of upstream claims.

## Update or remove

```bash
npx skills@latest check
npx skills@latest update
npx skills@latest remove
```

Review prompts because these commands may include skills from other repositories.

## Contributing and validation

Skill entrypoints live at `skills/<name>/SKILL.md`, with optional local `references/`, `scripts/`, and `assets/` directories. Installed skills must not depend on this repository's build tooling or on sibling skills. The Claude plugin uses default discovery, not a separately maintained skill list.

```bash
npm ci
npm run check
```

Development tooling requires Node.js 22.20+. See [authoring](docs/authoring.md), [publishing](docs/publishing.md), and [contributing](CONTRIBUTING.md).

## License

[MIT](LICENSE).
