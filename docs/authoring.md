# Authoring

The collection contains `oss-reuse-atlas`, `feature-discovery`, `production-vertical-slice`, and `adversarial-acceptance`. Each has its own `SKILL.md` and self-contained supporting resources. The earlier empty placeholders have been removed. Additional skills use the same `skills/<name>/` layout.

## Format

`SKILL.md` begins with YAML frontmatter containing:

- `name`: 1–64 lowercase letters, digits, and single hyphens; must match the directory name. No leading, trailing, or consecutive hyphens.
- `description`: a nonempty string of at most 1,024 characters describing what the skill does **and when to use it**.

After the closing frontmatter delimiter, write the actual instructions. Keep instructions focused. Link to supporting material rather than embedding everything in the entry point.

Optional directories inside a skill:

| Directory | Purpose |
| --- | --- |
| `references/` | Supporting documentation loaded only when needed |
| `scripts/` | Helpers the skill explicitly invokes |
| `assets/` | Templates and other resources |

Create those folders only when needed. Keep all dependencies inside the skill directory: installing one skill must not depend on sibling skills or repository-level tooling. Document required tools, network access, permissions, and potentially destructive operations. Never include credentials.

## Layout decision

Use a flat `skills/<name>/SKILL.md` layout. Both the skills CLI and Claude Code's default plugin discovery support it without maintaining a second list of skills. Do not add a root `SKILL.md`, which would turn the entire repository into a skill.

## Check

Run `npm ci` once, then `npm run check` with Python 3.10+ installed. Validation checks repository metadata, flat layout, frontmatter, unique names, and nonempty instructions; tests cover both the Node tooling and atlas Python helper. Directories containing only `.gitkeep` are allowed as placeholders and excluded from the skill count. Other incomplete skill directories fail validation. Symlinks are rejected for predictable distribution. This is a repository-specific structural check, not a full security audit or proof that an agent follows the instructions.

Before publishing a skill, test it in a disposable consumer project using the installation commands in the README. Verify discovery, invocation, linked resources, and any helpers on the agents you claim to support.

Specification: <https://agentskills.io/specification>
