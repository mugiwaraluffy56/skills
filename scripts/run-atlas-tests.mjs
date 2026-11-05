import { spawnSync } from 'node:child_process';
import { fileURLToPath } from 'node:url';

const python = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
const result = spawnSync(python, [fileURLToPath(new URL('../tests/test_validate_atlas.py', import.meta.url))], { stdio: 'inherit' });
if (result.error) console.error(`Atlas tests require Python 3.10+. Set PYTHON to its executable path. ${result.error.message}`);
process.exitCode = result.status ?? 1;
