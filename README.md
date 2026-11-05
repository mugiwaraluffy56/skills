# skills

My personal agent skills for building production-grade software, from idea to release.

I want my coding agents to help me build the whole feature—not just write code that looks right. Understand the problem, question assumptions, implement the actual user journey, test the failure paths, and review what shipped against what was asked for.

These are the workflows I'm taking from project to project. Use the skills that fit the task, with the coding agent and tools you already use.

## Skills

| Skill | When to use it | Outcome |
| --- | --- | --- |
| [`oss-reuse-atlas`](skills/oss-reuse-atlas/SKILL.md) | Starting a software project, researching alternatives, or looking for code and product references | An evidence-backed catalog of comparable open-source applications and reusable modules, with commit-pinned implementation dossiers, license checks, and reuse decisions. **Research only: no implementation plan.** |
| [`feature-discovery`](skills/feature-discovery/SKILL.md) | Before implementing a substantial feature, integration, or product workflow | A validated user journey, capability/compatibility matrix, source-backed requirements, justified constraints, and measurable acceptance criteria. |
| [`production-vertical-slice`](skills/production-vertical-slice/SKILL.md) | Building an accepted feature across frontend, API, state, workers, external services, or other relevant boundaries | A functional end-to-end user journey, tests for success and failure, and accurate verification evidence. |
| [`adversarial-acceptance`](skills/adversarial-acceptance/SKILL.md) | After feature implementation or when a feature passes tests but still feels incomplete | An independent review that challenges the scope, compatibility, behavior, recovery, security, UX, and claims of production readiness. |

The goal isn't more process for every small change. It's giving the agent the right discipline when a task needs it, while keeping me in control of scope and decisions. Each skill includes its own instructions and resources; sibling skills are optional, not requirements.

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

The installer requires Node.js 22.20+. The skills aren't tied to JavaScript: they guide the agent through your project's languages and tools. Global installation makes a skill available across projects; it doesn't automatically run it. Ask your agent to use the skill when you need it.

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

Restart your agent if newly installed skills don't appear.

## Usage

Start a new project with a **research-only** reference collection:

```text
Use oss-reuse-atlas to find a broad, evidence-backed library of open-source
applications like this project and related reusable implementations. Pin source
revisions, inspect actual code/tests and licenses, and record precise reuse
options. Do not create an implementation plan, milestones, tickets, or code.
```

Before and after implementing a feature:

```text
Use feature-discovery to investigate the full user journey, official API
capabilities, representative open-source implementations, compatibility,
edge cases, and justified constraints. Use production-vertical-slice to build
the accepted feature with real end-to-end behavior. Finally, use
adversarial-acceptance to challenge the result against my original request.
```

Bring the actual context: the problem, relevant code, constraints, and what you expect to work. Invocation details vary by agent; some also expose skills as slash commands. You can use each skill separately, not just in the sequence above.

The research skill includes a standard-library helper requiring Python 3.10+ when you run its structural validation. It checks artifact structure, not the truth of upstream claims or legal permission to reuse code.

Installing a skill doesn't connect external services, grant permissions, or prove a feature is production-ready. Those still need explicit setup, authorization, and evidence.

## Update or remove

```bash
npx skills@latest check
npx skills@latest update
npx skills@latest remove
```

Review prompts because these commands may include skills from other collections. For plugin installations, manage updates and removal through Claude Code's `/plugin` menu.

## License

[MIT](LICENSE).
