# Authoring

No skills are included in the scaffold. When you choose to add one, create a directory at `skills/<name>/` with a `SKILL.md` entry point.

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

Run `npm ci` once, then `npm run check`. Validation checks repository metadata, flat layout, frontmatter, unique names, and nonempty instructions. Empty repositories are valid. Symlinks are rejected for predictable distribution. This is a repository-specific structural check, not a full security audit or proof that an agent follows the instructions.

Before publishing a skill, test it in a disposable consumer project using the installation commands in the README. Verify discovery, invocation, linked resources, and any helpers on the agents you claim to support.

Specification: <https://agentskills.io/specification>
