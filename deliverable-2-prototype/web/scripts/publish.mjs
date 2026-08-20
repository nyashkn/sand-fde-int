#!/usr/bin/env node
/**
 * Build one edition per quarter and publish it under a quarter-stamped name.
 *
 * The bulletin content comes from `dist/<quarter>.html`, the static file
 * `src/pages/[quarter].astro` emits per quarter via `getStaticPaths`: path-driven, not
 * env-driven, so which edition is which cannot depend on a build-time environment
 * variable. (`dist/index.html` is the site's landing page, `src/pages/index.astro`, not a
 * bulletin edition; it links to all four but renders none of them.) `astro build` still
 * runs once per requested quarter here because the email edition
 * (`src/pages/email.astro`) is `QUARTER`-env-scoped by design, one send per quarter.
 *
 * The assertion is the point. Building with `QUARTER=2024-Q3` and copying a document that
 * actually says 2024-Q1 already shipped once, back when the root page itself read
 * `import.meta.env.QUARTER`, which Astro only populates for PUBLIC_-prefixed variables.
 * Nothing failed; the wrong quarter simply shipped under the right name. So the requested
 * quarter is checked against what the document actually says before anything is written.
 */
import { execFileSync } from 'node:child_process';
import { readFileSync, writeFileSync, copyFileSync, mkdirSync } from 'node:fs';
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

  const html = readFileSync(join(DIST, `${quarter}.html`), 'utf8');
  const title = html.match(/<title>([^<]*)<\/title>/)?.[1] ?? '';
  if (!title.includes(quarter)) {
    console.error(`  FAIL  requested ${quarter}, document says "${title}".`);
    console.error('        Refusing to publish a file whose name and contents disagree.');
    process.exit(1);
  }

  // `[quarter].astro` links sibling quarters as site-absolute paths ("/2024-Q2"), correct
  // for the deployed root. A published edition is a flat sibling file, not a site route,
  // so its cross-quarter nav is rewritten to the filename it actually ships as.
  const flat = html.replace(/href="\/(\d{4}-Q\d)"/g, 'href="bulletin-$1.html"');

  writeFileSync(join(OUT, `bulletin-${quarter}.html`), flat);
  copyFileSync(join(DIST, 'email.inlined.html'), join(OUT, `bulletin-${quarter}.email.html`));
  const kb = (Buffer.byteLength(flat, 'utf8') / 1024).toFixed(1);
  console.log(`  published bulletin-${quarter}.html  ${kb} KB  (+ email edition)`);
}
