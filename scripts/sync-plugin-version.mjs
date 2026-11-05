#!/usr/bin/env node
// Adapted from mattpocock/skills. See LICENSE.
// Copy the package version to plugin metadata; --check is read-only.
import { readFileSync, writeFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';

const pluginPath = fileURLToPath(new URL('../.claude-plugin/plugin.json', import.meta.url));
const { version } = JSON.parse(readFileSync(new URL('../package.json', import.meta.url), 'utf8'));
const source = readFileSync(pluginPath, 'utf8');
const plugin = JSON.parse(source);

if (plugin.version === version) {
  console.log(`plugin.json version is ${version} (already in sync)`);
} else if (process.argv.includes('--check')) {
  console.error(`plugin.json version is ${plugin.version}, package.json is ${version}. Run npm run sync:version.`);
  process.exitCode = 1;
} else {
  const updated = source.replace(/("version"\s*:\s*")[^"]*(")/, (_, prefix, suffix) => `${prefix}${version}${suffix}`);
  if (JSON.parse(updated).version !== version) {
    throw new Error(`Could not find a version field to replace in ${pluginPath}`);
  }
  writeFileSync(pluginPath, updated);
  console.log(`plugin.json version ${plugin.version} -> ${version}`);
}
