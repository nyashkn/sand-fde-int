#!/usr/bin/env node
/**
 * Build one edition per quarter and publish it under a quarter-stamped name.
 *
 * The assertion is the point. Building with `QUARTER=2024-Q3` and copying the result to
 * `bulletin-2024-Q3.html` already produced two byte-identical files both holding Q1
 * figures, because the page read `import.meta.env.QUARTER`, which Astro only populates
 * for PUBLIC_-prefixed variables. Nothing failed; the wrong quarter simply shipped under
 * the right name.
 *
 * So the requested quarter is checked against what the document actually says before
 * anything is written.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, copyFileSync, mkdirSync } from 'node:fs';
import { join } from 'node:path';

const QUARTERS = process.argv.slice(2);
if (QUARTERS.length === 0) {
  console.error('usage: node scripts/publish.mjs 2024-Q1 2024-Q3');
  process.exit(1);
}

const DIST = join(process.cwd(), 'dist');
const OUT = join(process.cwd(), '..', 'output');
mkdirSync(OUT, { recursive: true });

for (const quarter of QUARTERS) {
  execFileSync('bun', ['x', 'astro', 'build'], {
    env: { ...process.env, QUARTER: quarter },
    stdio: 'pipe',
  });
  execFileSync('node', ['scripts/email.mjs'], {
    env: { ...process.env, QUARTER: quarter },
    stdio: 'pipe',
  });

  const html = readFileSync(join(DIST, 'index.html'), 'utf8');
  const title = html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '';
  if (!title.includes(quarter)) {
    console.error(`  FAIL  requested ${quarter}, document says "${title}".`);
    console.error('        Refusing to publish a file whose name and contents disagree.');
    process.exit(1);
  }

  copyFileSync(join(DIST, 'index.html'), join(OUT, `bulletin-${quarter}.html`));
  copyFileSync(join(DIST, 'email.inlined.html'), join(OUT, `bulletin-${quarter}.email.html`));
  const kb = (Buffer.byteLength(html, 'utf8') / 1024).toFixed(1);
  console.log(`  published bulletin-${quarter}.html  ${kb} KB  (+ email edition)`);
}
