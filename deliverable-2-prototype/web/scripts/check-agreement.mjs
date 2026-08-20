#!/usr/bin/env node
/**
 * The two surfaces must publish the same figure.
 *
 * They are separate templates reading one mart, so nothing structural stops them
 * formatting a shared number differently. That already happened once: the email counted
 * withheld guard rows and reported 6 where the bulletin counted panels and reported 2.
 * Same data, same build, two published answers.
 *
 * This reads the rendered output rather than the source, because agreement in the mart
 * is not the claim. The claim is that a Director reading the email and a DHO reading the
 * bulletin see the same number.
 *
 * Reads `dist/2024-Q1.html`, not `dist/index.html`: the site root is a landing page
 * (`src/pages/index.astro`) that links to editions rather than rendering one, so it is no
 * longer a bulletin surface. `2024-Q1.html` is `src/pages/[quarter].astro`'s static output
 * for the same default quarter `email.astro` falls back to when `QUARTER` is unset, which
 * is what an unqualified `astro build` (this check's own build step) produces for both.
 */
import { readFileSync } from 'node:fs';
import { join } from 'node:path';

const DIST = join(process.cwd(), 'dist');
const text = (f) =>
  readFileSync(join(DIST, f), 'utf8')
    .replace(/<(script|style)\b[\s\S]*?<\/\1>/gi, ' ')
    .replace(/<svg[\s\S]*?<\/svg>/gi, ' ')
    .replace(/<[^>]+>/g, ' ')
    .replace(/&[a-z]+;|&#\d+;/gi, ' ')
    .replace(/\s+/g, ' ');

const bulletin = text('2024-Q1.html');
const email = text('email.inlined.html');

/** Each claim must appear in both surfaces, spelled identically. */
const SHARED = [
  { id: 'headline-rate', re: /([\d.]+) per 1,000 live births/ },
  { id: 'deaths', re: /([\d,]+) deaths across/ },
  { id: 'live-births', re: /deaths across ([\d,]+) live births/ },
  { id: 'months-held', re: /(\d+) of (\d+) expected months/ },
  { id: 'provisional-districts', re: /(\d+) of (\d+) district figures/ },
  // Both surfaces read the same temporal_signal_check / stratification_check row and
  // must state the same caveat, not a retyped paraphrase: the checks always render now,
  // never gate, so this is the one place a caveat could silently drift between surfaces
  // the way the withheld-panel count once did. Anchored on the checks.py-authored prefix
  // rather than the whole sentence, since the surrounding lead-in prose legitimately
  // differs between the full bulletin and the abbreviated email.
  { id: 'temporal-caveat', re: /observed lag-1 [-\d.]+/ },
  { id: 'correlation-caveat', re: /pooled r=[-+\d.]+/ },
];

let failures = 0;
for (const c of SHARED) {
  const b = bulletin.match(c.re);
  const e = email.match(c.re);
  if (!b || !e) {
    failures++;
    console.error(`  FAIL  ${c.id}: absent from ${!b ? 'bulletin' : 'email'}`);
    continue;
  }
  if (b[0] !== e[0]) {
    failures++;
    console.error(`  FAIL  ${c.id}\n        bulletin: ${b[0]}\n        email:    ${e[0]}`);
  }
}

if (failures > 0) {
  console.error(`\n  ${failures} disagreement(s) between the two surfaces.\n`);
  process.exit(1);
}
console.log(`  agreement check passed: ${SHARED.length} shared figures identical across 2 surfaces`);
