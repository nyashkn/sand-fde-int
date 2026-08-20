#!/usr/bin/env node
/**
 * The chart palette and the stylesheet must be the same palette.
 *
 * Charts render in Node via Flint's Vega-Lite backend, themed by a narrow override of
 * the `swiss` preset (`THEME_SPEC` in `charts.ts`) rather than a hand-typed literal per
 * mark: Flint's own `swiss` defaults are close to but not identical to this project's
 * tokens, so the override exists specifically to pin them exact. That override still
 * duplicates hex values that also live in `tokens.css`, so the drift risk this check
 * exists for is unchanged, only its source shape moved from a flat `TOKENS` object to a
 * few nested `ink.*` keys.
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

const block = ts.match(/const THEME_SPEC = \{([\s\S]*?)\n\} as const;/)?.[1] ?? '';
const themeInk = Object.fromEntries(
  [...block.matchAll(/\b([a-zA-Z0-9_]+):\s*'(#[0-9a-fA-F]+)'/g)].map((m) => [m[1], m[2].trim().toLowerCase()]),
);

/** THEME_SPEC.ink.* key -> kebab custom property in tokens.css. Two keys legitimately
 * point at the same custom property (canvas/plot are both --paper; axis/rule are both
 * --ink), which is fine: both must still agree with that one property. */
const PAIRS = {
  canvas: 'paper', plot: 'paper', primary: 'ink', secondary: 'gray-mid',
  grid: 'gray-line', axis: 'ink', rule: 'ink', single: 'red', accent: 'red',
};

const problems = [];
for (const [tsKey, value] of Object.entries(themeInk)) {
  const cssKey = PAIRS[tsKey];
  if (!cssKey) {
    problems.push(`${tsKey}: in charts.ts THEME_SPEC with no tokens.css counterpart declared here`);
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

/** The scalar walk above matches `key: '#hex'`, which an array literal is not, so a
 * palette declared as `categorical: [...]` used to pass this check without being read
 * at all. It was unset, and Flint's own swiss ramp reached the published chart. Walk
 * the array explicitly: every entry must be some colour tokens.css declares. */
const categorical = [...(block.match(/categorical:\s*\[([^\]]*)\]/)?.[1] ?? '')
  .matchAll(/'(#[0-9a-fA-F]+)'/g)].map((m) => m[1].toLowerCase());

if (categorical.length === 0) {
  problems.push('THEME_SPEC.ink.series.categorical is unset — Flint falls back to its own ramp');
} else {
  const known = new Set(Object.values(cssVars));
  for (const hex of categorical) {
    if (!known.has(hex)) problems.push(`categorical ${hex}: no matching custom property in tokens.css`);
  }
  if (new Set(categorical).size !== categorical.length) {
    problems.push('categorical: repeated colour, two series would be indistinguishable');
  }
}

if (Object.keys(themeInk).length === 0) {
  problems.push('THEME_SPEC.ink not found in charts.ts (regex or export shape changed)');
}

if (problems.length > 0) {
  console.error('\n  FAIL  chart palette has drifted from the stylesheet');
  for (const p of problems) console.error(`        ${p}`);
  console.error('');
  process.exit(1);
}
console.log(
  `  token check passed: ${Object.keys(themeInk).length} chart theme colours`
  + ` + ${categorical.length} categorical series inks identical to tokens.css`,
);
