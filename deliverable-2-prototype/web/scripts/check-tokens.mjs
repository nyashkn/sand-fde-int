#!/usr/bin/env node
/**
 * The chart palette and the stylesheet must be the same palette.
 *
 * Charts are rendered in Node, where there is no document and no cascade, so Observable
 * Plot cannot read `var(--clay)`. `charts.ts` therefore holds literal hex values that
 * duplicate `tokens.css`. They agree today because they were typed to agree, which is
 * exactly the arrangement that drifts the first time someone adjusts a colour in one file.
 *
 * This is also the answer to whether a future explore surface can inherit the token set:
 * it can, because the tokens are plain custom properties, but any surface that renders
 * outside the browser inherits this duplication too and must be added below.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const S = join(process.cwd(), 'src');
const css = readFileSync(join(S, 'styles', 'tokens.css'), 'utf8');
const ts = readFileSync(join(S, 'lib', 'charts.ts'), 'utf8');

const cssVars = Object.fromEntries(
  [...css.matchAll(/--([a-z0-9-]+)\s*:\s*([^;]+);/gi)].map((m) => [m[1], m[2].trim().toLowerCase()]),
);

const block = ts.match(/const TOKENS = \{([\s\S]*?)\n\} as const;/)?.[1] ?? '';
const tsTokens = Object.fromEntries(
  [...block.matchAll(/^\s*([a-zA-Z0-9_]+):\s*'([^']+)'/gm)].map((m) => [m[1], m[2].trim().toLowerCase()]),
);

/** camelCase token in charts.ts -> kebab custom property in tokens.css. */
const PAIRS = {
  ink: 'ink', inkSoft: 'ink-soft', muted: 'muted', clay: 'clay', clayD: 'clay-d',
  olive: 'olive', rule: 'rule', rule2: 'rule-2', cream: 'cream', oat: 'oat', paper: 'paper',
};

// Not a colour, so it has no custom property to compare against. Named here so that an
// unpaired token is a deliberate exemption rather than a silent gap.
const EXEMPT = new Set(['mono']);

const problems = [];
for (const [tsKey, value] of Object.entries(tsTokens)) {
  if (EXEMPT.has(tsKey)) continue;
  const cssKey = PAIRS[tsKey];
  if (!cssKey) {
    problems.push(`${tsKey}: in charts.ts with no tokens.css counterpart and no exemption`);
    continue;
  }
  if (!(cssKey in cssVars)) {
    problems.push(`${tsKey}: expects --${cssKey}, absent from tokens.css`);
    continue;
  }
  if (cssVars[cssKey] !== value) {
    problems.push(`${tsKey}: charts.ts ${value}, tokens.css --${cssKey} ${cssVars[cssKey]}`);
  }
}

if (problems.length > 0) {
  console.error('\n  FAIL  chart palette has drifted from the stylesheet');
  for (const p of problems) console.error(`        ${p}`);
  console.error('');
  process.exit(1);
}
const n = Object.keys(tsTokens).length - EXEMPT.size;
console.log(`  token check passed: ${n} chart colours identical to tokens.css`);
