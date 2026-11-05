# Agent Skills Collection

Shared language for authoring and distributing this repository's skills.

## Language

**Skill**:
A self-contained set of instructions and optional supporting resources that teaches a coding agent a specific workflow.
_Avoid_: Plugin (when referring to an individual skill).

**Collection**:
The set of skills maintained together in this repository. A collection can be empty.
_Avoid_: Agent, marketplace.

**Catalog**:
The discoverable inventory of skills in the collection, rather than a separately maintained list.
_Avoid_: Marketplace (when referring only to available skills).

**Coding agent**:
The tool that discovers and follows installed skills, such as Claude Code, Codex, OpenCode, or Cursor.
_Avoid_: Skill (when referring to the tool consuming instructions).

**Plugin**:
A distribution package that lets a compatible coding agent install the collection as a unit.
_Avoid_: Skill (when referring to the whole package).

**Marketplace**:
A registry of plugin offerings and their sources. It is distinct from the skills catalog inside a plugin.
_Avoid_: Collection, catalog.

**Consumer project**:
A project where someone installs and uses skills, distinct from this repository where skills are authored.
_Avoid_: Source repository (when referring to an installation destination).

**Project-local installation**:
An installation available to a coding agent within a particular consumer project.
_Avoid_: Global installation.

**Global installation**:
An installation available to a supported coding agent across the user's projects, not automatically to every agent on the machine.
_Avoid_: Universal installation, system-wide installation.

**Scaffold**:
The repository structure, documentation, metadata, and development tooling that support a collection without providing skills themselves.
_Avoid_: Installed skill pack (when the collection is empty).
