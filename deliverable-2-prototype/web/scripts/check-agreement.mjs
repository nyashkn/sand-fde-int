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

const bulletin = text('index.html');
const email = text('email.inlined.html');

/** Each claim must appear in both surfaces, spelled identically. */
const SHARED = [
  { id: 'headline-rate', re: /([\d.]+) per 1,000 live births/ },
  { id: 'deaths', re: /([\d,]+) deaths across/ },
  { id: 'live-births', re: /deaths across ([\d,]+) live births/ },
  { id: 'months-held', re: /(\d+) of (\d+) expected months/ },
  { id: 'provisional-districts', re: /All (\d+) district figures/ },
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

// Withheld panel count is stated as a bare integer in different sentences, so it is
// compared as a value rather than a phrase.
const bw = bulletin.match(/Panels withheld (\d+)/);
const ew = email.match(/Panels withheld (\d+)/);
if (bw?.[1] !== ew?.[1]) {
  failures++;
  console.error(`  FAIL  withheld-panels\n        bulletin: ${bw?.[1]}\n        email:    ${ew?.[1]}`);
}

if (failures > 0) {
  console.error(`\n  ${failures} disagreement(s) between the two surfaces.\n`);
  process.exit(1);
}
console.log(`  agreement check passed: ${SHARED.length + 1} shared figures identical across 2 surfaces`);
