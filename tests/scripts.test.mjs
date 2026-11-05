import assert from 'node:assert/strict';
import { execFileSync } from 'node:child_process';
import { copyFile, mkdir, mkdtemp, readFile, readlink, realpath, rm, symlink, writeFile } from 'node:fs/promises';
import { tmpdir } from 'node:os';
import { join } from 'node:path';
import test from 'node:test';

async function fixture(t) {
  const temporary = await realpath(await mkdtemp(join(tmpdir(), 'skills-scripts-')));
  t.after(() => rm(temporary, { recursive: true, force: true }));
  const repo = join(temporary, 'repo');
  const home = join(temporary, 'home');
  await mkdir(join(repo, 'scripts'), { recursive: true });
  await mkdir(join(repo, 'skills'));
  await mkdir(home);
  for (const name of ['link-skills.sh', 'list-skills.sh', 'sync-plugin-version.mjs']) {
    await copyFile(new URL(`../scripts/${name}`, import.meta.url), join(repo, 'scripts', name));
  }
  const run = (name) => execFileSync('bash', [join(repo, 'scripts', name)], { env: { ...process.env, HOME: home }, encoding: 'utf8', stdio: 'pipe' });
  const addSkill = async () => {
    await mkdir(join(repo, 'skills/example'));
    await writeFile(join(repo, 'skills/example/SKILL.md'), 'test fixture');
  };
  return { repo, home, run, addSkill };
}

const shellOptions = { skip: process.platform === 'win32' ? 'Local symlink tests require Unix; use Git Bash or WSL manually on Windows.' : false };

test('shell helpers handle the empty collection', shellOptions, async (t) => {
  const { run } = await fixture(t);
  assert.equal(run('list-skills.sh'), '');
  assert.match(run('link-skills.sh'), /nothing to link/);
});

test('local linker creates links and can run again', shellOptions, async (t) => {
  const { repo, home, run, addSkill } = await fixture(t);
  await addSkill();
  assert.equal(run('list-skills.sh'), 'skills/example/SKILL.md\n');
  run('link-skills.sh');
  run('link-skills.sh');
  for (const agent of ['.claude', '.agents']) {
    assert.equal(await readlink(join(home, agent, 'skills/example')), join(repo, 'skills/example'));
  }
});

test('local linker preserves conflicting installations', shellOptions, async (t) => {
  const { home, run, addSkill } = await fixture(t);
  await addSkill();
  await mkdir(join(home, '.agents/skills/example'), { recursive: true });
  const existing = join(home, '.agents/skills/example/keep.txt');
  await writeFile(existing, 'keep me');
  assert.throws(() => run('link-skills.sh'), /refusing to replace/);
  assert.equal(await readFile(existing, 'utf8'), 'keep me');
  await assert.rejects(readlink(join(home, '.claude/skills/example')), { code: 'ENOENT' });
});

test('local linker rejects destinations redirected into the repository', shellOptions, async (t) => {
  const { repo, home, run, addSkill } = await fixture(t);
  await addSkill();
  await symlink(repo, join(home, '.claude'));
  assert.throws(() => run('link-skills.sh'), /resolves into this repository/);
});

test('version sync supports check-only and write modes', async (t) => {
  const { repo } = await fixture(t);
  await mkdir(join(repo, '.claude-plugin'));
  await writeFile(join(repo, 'package.json'), '{"version":"0.2.0"}');
  const plugin = join(repo, '.claude-plugin/plugin.json');
  await writeFile(plugin, '{"name":"personal-skills","version":"0.1.0"}\n');
  const script = join(repo, 'scripts/sync-plugin-version.mjs');
  assert.throws(() => execFileSync(process.execPath, [script, '--check'], { stdio: 'pipe' }));
  assert.equal(JSON.parse(await readFile(plugin, 'utf8')).version, '0.1.0');
  execFileSync(process.execPath, [script]);
  assert.equal(JSON.parse(await readFile(plugin, 'utf8')).version, '0.2.0');
  execFileSync(process.execPath, [script, '--check']);
});
