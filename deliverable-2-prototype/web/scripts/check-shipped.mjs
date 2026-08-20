#!/usr/bin/env node
/**
 * Every declared input the pipeline reads by name must actually ship.
 *
 * This check exists because of a defect it would have caught: `gold.py` reads
 * `known_contradictions.csv` and `cause_capability_links.csv` with a bare
 * `pd.read_csv(mart_dir / ...)`, and neither file had ever been `git add`ed. Nothing
 * in the suite noticed, because every other check runs against the working tree, where
 * the files are present. `uv run python run.py` succeeded, `bun run verify` passed, and
 * all four quarters rendered. A reviewer cloning the repo got a FileNotFoundError on the
 * first pipeline command.
 *
 * The general shape of that failure is worth stating: the verification story tested what
 * the author has, not what a third party receives. Those differ exactly when a file is
 * untracked, which is the one state the working tree cannot show you. So this check asks
 * git, not the filesystem.
 *
 * ponytail: parses the read calls out of the dataflow source rather than keeping a
 * hand-maintained manifest. A manifest is a second list to forget to update, which is
 * the same class of bug this check is here to prevent.
 */
import { readFileSync, readdirSync } from 'node:fs';
import { execFileSync } from 'node:child_process';
import { join, resolve, relative } from 'node:path';

const ROOT = resolve(process.cwd(), '..');            // deliverable-2-prototype/
const DATAFLOW = join(ROOT, 'pipeline', 'dataflow');
const MART = join(ROOT, 'pipeline', 'mart');

// `mart_dir / "name.csv"` and `mart_dir / ("name" + ".csv")`, plus plain "name.csv"
// string literals passed to a read_csv call. One pattern per line keeps this readable.
const PATTERNS = [
  /mart_dir\s*\/\s*["']([\w.-]+\.csv)["']/g,
  /read_csv\w*\(\s*[^)]*?["']([\w.-]+\.csv)["']/g,
];

const referenced = new Set();
for (const f of readdirSync(DATAFLOW).filter((n) => n.endsWith('.py'))) {
  const src = readFileSync(join(DATAFLOW, f), 'utf8');
  for (const re of PATTERNS) {
    for (const m of src.matchAll(re)) referenced.add(m[1]);
  }
}

if (referenced.size === 0) {
  console.error('check-shipped: parsed no CSV reads out of pipeline/dataflow/*.py.');
  console.error('  The patterns above no longer match the source. Fix them rather than');
  console.error('  deleting this check: a check that cannot fail is not a control.');
  process.exit(1);
}

// git ls-files is the authority. The filesystem cannot distinguish "present" from
// "present and tracked", and that distinction is the entire point of this check.
const tracked = new Set(
  execFileSync('git', ['ls-files', '--', relative(process.cwd(), MART)], {
    cwd: process.cwd(), encoding: 'utf8',
  })
    .split('\n')
    .filter(Boolean)
    .map((p) => p.split('/').pop()),
);

const missing = [...referenced].filter((n) => !tracked.has(n)).sort();

if (missing.length) {
  console.error(`check-shipped: ${missing.length} declared input(s) read by the pipeline are not tracked by git:`);
  for (const n of missing) console.error(`  pipeline/mart/${n}`);
  console.error('');
  console.error('  A clone of this repository cannot run the pipeline. Fix with:');
  console.error(`    git add ${missing.map((n) => `deliverable-2-prototype/pipeline/mart/${n}`).join(' ')}`);
  process.exit(1);
}

console.log(`check-shipped: ${referenced.size} declared input(s) read by the pipeline, all tracked.`);
