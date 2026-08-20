#!/usr/bin/env node
/**
 * Hold the email edition to what email can actually do.
 *
 * Each rule here is a measured failure, not a precaution. The full bulletin inlined
 * measured 99.0 KB against Gmail's ~102 KB clip threshold, and 33.8 KB of that was SVG
 * that Gmail, Outlook and Yahoo do not render at all.
 *
 * The byte ceiling is the one that will actually fire: it passes today at 16 KB and gets
 * closer every quarter that adds a row.
 */
import { readFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';

// Gmail clips a message body past ~102 KB and hides the remainder behind
// "[Message clipped] View entire message". The disclosure sections are at the bottom.
const CEILING = 102 * 1024;
const WARN_AT = 0.7;

const file = join(process.cwd(), 'dist', 'email.inlined.html');
if (!existsSync(file)) {
  console.error('  dist/email.inlined.html missing. Run: bun run build && bun run email');
  process.exit(1);
}

const html = readFileSync(file, 'utf8');
const bytes = Buffer.byteLength(html, 'utf8');

const RULES = [
  {
    id: 'byte-ceiling',
    why: `Gmail clips past ~${(CEILING / 1024).toFixed(0)} KB, and the disclosures are at the bottom.`,
    hits: bytes > CEILING ? [`${(bytes / 1024).toFixed(1)} KB`] : [],
  },
  {
    id: 'no-embedded-svg',
    why: 'Embedded <svg> is unsupported in Gmail, Outlook and Yahoo (~38% support), and Outlook began retiring it in Aug 2025.',
    hits: [...html.matchAll(/<svg\b/gi)].map((m) => m[0]),
  },
  {
    id: 'no-script',
    why: 'Every email client strips script.',
    hits: [...html.matchAll(/<script\b/gi)].map((m) => m[0]),
  },
  {
    id: 'no-flex-or-grid',
    why: "Outlook's Word rendering engine supports neither. Use table layout.",
    hits: [...html.matchAll(/display\s*:\s*(?:flex|grid)/gi)].map((m) => m[0]),
  },
  {
    id: 'state-not-colour-only',
    why: 'Provisional and caveat must appear as words, since a client that drops CSS still has to carry the state.',
    hits: /provisional/i.test(html) && /caveat/i.test(html) ? [] : ['state words absent'],
  },
];

let failures = 0;
for (const r of RULES) {
  if (r.hits.length > 0) {
    failures += r.hits.length;
    console.error(`\n  FAIL  ${r.id}  (${r.hits.length})`);
    console.error(`        ${r.why}`);
    for (const h of [...new Set(r.hits)].slice(0, 3)) console.error(`        > ${String(h).slice(0, 80)}`);
  }
}

const pct = ((bytes / CEILING) * 100).toFixed(0);
if (failures > 0) {
  console.error(`\n  ${failures} violation(s). ${(bytes / 1024).toFixed(1)} KB, ${pct}% of ceiling.\n`);
  process.exit(1);
}
if (bytes > CEILING * WARN_AT) {
  console.log(`  WARN  ${(bytes / 1024).toFixed(1)} KB is ${pct}% of the clip ceiling. Budget is nearly spent.`);
} else {
  console.log(`  email check passed: ${(bytes / 1024).toFixed(1)} KB, ${pct}% of ceiling, ${RULES.length} rules`);
}
