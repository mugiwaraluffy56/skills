import assert from 'node:assert/strict';
import { mkdtemp, mkdir, readFile, rm, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';
import { validateRepository, validateSkill } from '../scripts/validate.mjs';

const text = (header = 'name: test-skill\ndescription: Use when testing the validator.', body = '# Instructions\nDo the task.') => `---\n${header}\n---\n${body}`;

test('accepts standard frontmatter, folded descriptions, and CRLF', () => {
  assert.equal(validateSkill(text(), 'test-skill').name, 'test-skill');
  assert.ok(validateSkill(text('name: test-skill\ndescription: >\n  Use when testing.'), 'test-skill'));
  assert.ok(validateSkill(text().replaceAll('\n', '\r\n'), 'test-skill'));
});

test('rejects missing, malformed, and duplicate-key YAML', () => {
  for (const value of ['no frontmatter', text('['), text('name: test-skill\nname: other')]) {
    assert.throws(() => validateSkill(value, 'test-skill'));
  }
});

test('rejects invalid names and mismatched directories', () => {
  for (const name of ['Bad_Name', '-bad', 'bad-', 'bad--name', 'a'.repeat(65), 'other']) {
    assert.throws(() => validateSkill(text(`name: ${name}\ndescription: Test`), 'test-skill'));
  }
});

test('rejects missing, non-string, empty, and overlong descriptions and empty body', () => {
  for (const description of ['', '42', 'null', '""', 'x'.repeat(1025)]) {
    assert.throws(() => validateSkill(text(`name: test-skill\ndescription: ${description}`), 'test-skill'));
  }
  assert.throws(() => validateSkill(text(undefined, '  '), 'test-skill'));
});

async function fixture(t) {
  const directory = await mkdtemp(join(tmpdir(), 'skills-validator-'));
  t.after(() => rm(directory, { recursive: true, force: true }));
  await mkdir(join(directory, '.claude-plugin'));
  await mkdir(join(directory, 'skills'));
  for (const file of ['package.json', '.claude-plugin/plugin.json', '.claude-plugin/marketplace.json']) {
    await writeFile(join(directory, file), await readFile(new URL(`../${file}`, import.meta.url)));
  }
  return directory;
}

test('accepts an empty scaffold and discovers a future skill', async (t) => {
  const directory = await fixture(t);
  assert.equal(await validateRepository(directory), 0);
  await mkdir(join(directory, 'skills/test-skill'));
  await writeFile(join(directory, 'skills/test-skill/SKILL.md'), text());
  assert.equal(await validateRepository(directory), 1);
});

test('rejects version drift', async (t) => {
  const directory = await fixture(t);
  await writeFile(join(directory, 'package.json'), JSON.stringify({ version: '9.9.9' }));
  await assert.rejects(validateRepository(directory), /versions differ/);
});

test('allows explicit empty placeholders without counting them as skills', async (t) => {
  const directory = await fixture(t);
  await mkdir(join(directory, 'skills/plan'));
  await writeFile(join(directory, 'skills/plan/.gitkeep'), '');
  assert.equal(await validateRepository(directory), 0);
  await writeFile(join(directory, 'skills/plan/unfinished.md'), 'Draft');
  await assert.rejects(validateRepository(directory), /regular SKILL.md/);
});

test('rejects skill directories without an entry point', async (t) => {
  const directory = await fixture(t);
  await mkdir(join(directory, 'skills/incomplete'));
  await assert.rejects(validateRepository(directory), /regular SKILL.md/);
});

test('rejects nested skills that default plugin discovery cannot expose', async (t) => {
  const directory = await fixture(t);
  await mkdir(join(directory, 'skills/test-skill/references'), { recursive: true });
  await writeFile(join(directory, 'skills/test-skill/SKILL.md'), text());
  await writeFile(join(directory, 'skills/test-skill/references/SKILL.md'), text());
  await assert.rejects(validateRepository(directory), /Nested skill/);
});
