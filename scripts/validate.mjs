import { readdir, readFile } from 'node:fs/promises';
import { basename, join, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';
import { parse } from 'yaml';

const root = fileURLToPath(new URL('../', import.meta.url));
const slug = /^[a-z0-9]+(?:-[a-z0-9]+)*$/;

export function validateSkill(text, directoryName) {
  const match = text.replace(/\r\n/g, '\n').match(/^---\n([\s\S]*?)\n---\n([\s\S]*)$/);
  if (!match) throw new Error('SKILL.md must start with YAML frontmatter and a closing --- line');
  const metadata = parse(match[1]);
  if (!metadata || typeof metadata !== 'object' || Array.isArray(metadata)) {
    throw new Error('Frontmatter must be a YAML mapping');
  }
  const { name, description } = metadata;
  if (typeof name !== 'string' || name.length > 64 || !slug.test(name)) {
    throw new Error('name must be a lowercase slug of 1–64 characters');
  }
  if (name !== directoryName) throw new Error('name must match the skill directory');
  if (typeof description !== 'string' || !description.trim() || description.length > 1024) {
    throw new Error('description must be a nonempty string of at most 1,024 characters');
  }
  if (!match[2].trim()) throw new Error('Skill instructions must not be empty');
  return metadata;
}

export async function validateRepository(directory) {
  const json = async (path) => JSON.parse(await readFile(join(directory, path), 'utf8'));
  const pkg = await json('package.json');
  const plugin = await json('.claude-plugin/plugin.json');
  const marketplace = await json('.claude-plugin/marketplace.json');
  if (plugin.version !== pkg.version) throw new Error('Package and plugin versions differ');
  if (!/^\d+\.\d+\.\d+$/.test(plugin.version)) throw new Error('Use a major.minor.patch version');
  if (!slug.test(plugin.name) || !slug.test(marketplace.name)) throw new Error('Invalid plugin or marketplace name');
  if (!marketplace.owner?.name) throw new Error('Marketplace owner is required');
  if (marketplace.plugins?.length !== 1 || marketplace.plugins[0].name !== plugin.name || marketplace.plugins[0].source !== './') {
    throw new Error('Marketplace must point to this repository’s root plugin');
  }
  // Default Claude plugin discovery uses skills/<name>/SKILL.md.
  if ('skills' in plugin) throw new Error('Use default skills discovery, not a second manifest catalog');
  if ((await readdir(directory)).includes('SKILL.md')) throw new Error('Do not make the repository root a skill');

  const names = new Set();
  async function rejectSymlinks(path) {
    for (const entry of await readdir(path, { withFileTypes: true })) {
      if (entry.isSymbolicLink()) throw new Error(`Symlinks are not supported: ${join(path, entry.name)}`);
      if (entry.isDirectory()) await rejectSymlinks(join(path, entry.name));
      else if (entry.name === 'SKILL.md') throw new Error(`Nested skill entry point: ${join(path, entry.name)}`);
    }
  }
  for (const entry of await readdir(join(directory, 'skills'), { withFileTypes: true })) {
    if (entry.name === '.gitkeep' && entry.isFile()) continue;
    if (!entry.isDirectory()) throw new Error(`Unexpected skills/ entry: ${entry.name}`);
    const skillDirectory = join(directory, 'skills', entry.name);
    const entries = await readdir(skillDirectory, { withFileTypes: true });
    const skillFile = entries.find((item) => item.name === 'SKILL.md');
    if (!skillFile?.isFile()) throw new Error(`${entry.name} must contain a regular SKILL.md file`);
    const metadata = validateSkill(await readFile(join(skillDirectory, 'SKILL.md'), 'utf8'), basename(skillDirectory));
    if (names.has(metadata.name)) throw new Error(`Duplicate skill name: ${metadata.name}`);
    names.add(metadata.name);
    for (const item of entries) {
      if (item.isSymbolicLink()) throw new Error(`Symlinks are not supported: ${item.name}`);
      if (item.isDirectory()) await rejectSymlinks(join(skillDirectory, item.name));
    }
  }
  return names.size;
}

if (process.argv[1] && resolve(process.argv[1]) === fileURLToPath(import.meta.url)) {
  try {
    const count = await validateRepository(root);
    console.log(`Validated repository metadata and ${count} skill(s).${count === 0 ? ' Empty scaffold is valid; nothing is installable yet.' : ''}`);
  } catch (error) {
    console.error(`Validation failed: ${error.message}`);
    process.exitCode = 1;
  }
}
