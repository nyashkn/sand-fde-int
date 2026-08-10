#!/usr/bin/env node
/**
 * Enforce the rules that were knowingly violated last time.
 *
 * These are all mechanically checkable, which is precisely why leaving them to review
 * failed: the previous renderer shipped em dashes and side-stripe borders after the rule
 * was written down. A rule a human has to remember is not a control.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { join } from 'node:path';

const DIST = join(process.cwd(), 'dist');

/** Visible copy only. CSS custom properties legitimately start with `--`. */
const copyOf = (html) =>
  html
    .replace(/<style\b[^>]*>[\s\S]*?<\/style>/gi, ' ')
    .replace(/<script\b[^>]*>[\s\S]*?<\/script>/gi, ' ')
    .replace(/style="[^"]*"/gi, ' ');

const RULES = [
  {
    id: 'no-em-dash',
    why: 'House style bans the em dash. Use commas, colons, semicolons or parentheses.',
    test: (html) => [...copyOf(html).matchAll(/\u2014|&mdash;|\s--\s/g)].map((m) => m[0]),
  },
  {
    id: 'no-side-stripe',
    why: 'A coloured left or right border above a hairline is a banned accent pattern. Use a tinted background with a rule above.',
    test: (html) =>
      [...html.matchAll(/border-(?:left|right)\s*:\s*([^;"}]*)/gi)]
        .map((m) => m[1].trim())
        .filter((decl) => {
          const width = Number.parseFloat(decl);
          const hasColour = /#|rgb|var\(--/i.test(decl);
          return Number.isFinite(width) && width > 1 && hasColour;
        }),
  },
  {
    id: 'no-script',
    why: 'The email surface strips script. Any script tag means the document behaves differently where it matters most.',
    test: (html) => [...html.matchAll(/<script\b/gi)].map((m) => m[0]),
  },
  {
    id: 'no-external-assets',
    why: 'The document must render offline and survive forwarding. Every asset is inline.',
    test: (html) => [...html.matchAll(/(?:src|href)="https?:\/\/[^"]+"/gi)].map((m) => m[0]),
  },
];

const files = readdirSync(DIST, { recursive: true }).filter((f) => String(f).endsWith('.html'));
if (files.length === 0) {
  console.error('No HTML in dist/. Run the build first.');
  process.exit(1);
}

let failures = 0;
for (const file of files) {
  const html = readFileSync(join(DIST, String(file)), 'utf8');
  for (const rule of RULES) {
    const hits = rule.test(html);
    if (hits.length > 0) {
      failures += hits.length;
      console.error(`\n  FAIL  ${file}  ${rule.id}  (${hits.length})`);
      console.error(`        ${rule.why}`);
      for (const h of [...new Set(hits)].slice(0, 5)) {
        console.error(`        > ${String(h).slice(0, 90)}`);
      }
    }
  }
}

const label = `${files.length} file(s), ${RULES.length} rules`;
if (failures > 0) {
  console.error(`\n  ${failures} violation(s) across ${label}\n`);
  process.exit(1);
}
console.log(`  style check passed: ${label}`);
