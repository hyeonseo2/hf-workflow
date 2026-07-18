import { cp, mkdir, rm } from 'node:fs/promises';
import { dirname, resolve } from 'node:path';
import { fileURLToPath } from 'node:url';

const root = resolve(dirname(fileURLToPath(import.meta.url)), '../..');
const source = resolve(root, 'dashboard');
const output = resolve(root, 'dist');

await rm(output, { force: true, recursive: true });
await mkdir(output, { recursive: true });

for (const entry of ['assets', 'data', 'js', 'index.html', 'styles.css']) {
  await cp(resolve(source, entry), resolve(output, entry), { recursive: true });
}
