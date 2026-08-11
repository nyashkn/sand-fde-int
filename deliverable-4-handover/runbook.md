# Runbook: the quarterly cycle

Every command below is run verbatim from a clean checkout as the last verification step
for this document. If a command here fails on your machine and this file was not updated
to explain why, that is a documentation bug: file it the same way you would a pipeline bug.

## Prerequisites, once per machine

```bash
# uv (Python) and bun (JavaScript) are the only two toolchains this project needs.
curl -LsSf https://astral.sh/uv/install.sh | sh
curl -fsSL https://bun.sh/install | bash
```

Versions this was built and verified against: `uv 0.11.6`, `bun 1.3.14`, Python `>=3.14`
(pinned in `pipeline/pyproject.toml`). Neither toolchain talks to a network service at
run time; both fetch packages once, on first `uv sync` / `bun install`.

## The quarterly cycle, four commands

Run from `deliverable-2-prototype/`.

```bash
cd pipeline && uv sync                    # once, or after a dependency change
uv run python run.py                      # rebuild the mart from the source CSVs
cd ../web && bun install                  # once, or after a dependency change
bun run publish                           # build both quarters, publish to ../output
```

`bun run publish` does not run `bun run verify` internally; the two are separate
package.json scripts. Run `verify` explicitly as the gate before treating a publish as
done:

```bash
bun run verify
```

Five checks run, in this order: `check-tokens.mjs`, the Astro build itself, `email.mjs`
(the inliner), `check-style.mjs`, `check-email.mjs`, `check-agreement.mjs`. **All five must
print `passed`.** If any fails, stop. Do not publish a bulletin whose checks failed.

## Reading the output

```
output/bulletin-2024-Q1.html        the bulletin, self-contained, open in any browser
output/bulletin-2024-Q1.email.html  the email edition, ready to paste into a send
```

`bun run publish` refuses to write a file whose stated quarter and rendered contents
disagree. If it refuses, the terminal output tells you which quarter and what the
document said instead; that is a real defect, not something to work around by renaming
the file.

## What each check failing means

| Check | If it fails |
|---|---|
| `check-tokens.mjs` | A chart colour was changed in one file (`tokens.css` or `charts.ts`) and not the other. Fix the one that was not intentionally changed. |
| Astro build | A template or data-reading error. The terminal shows a file and line. |
| `check-style.mjs` | An em dash, a side-stripe border, a `<script>` tag, an external asset reference, or template code that leaked into the rendered markup (an arrow function, `[object Object]`, or `undefined` printed literally). The terminal shows the offending snippet. |
| `check-email.mjs` | The email edition exceeds roughly 90 KB (a warning) or 102 KB (a failure, Gmail's clip threshold), contains an embedded chart, uses `flex`/`grid` layout Outlook cannot render, or is missing the words "provisional"/"withheld". |
| `check-agreement.mjs` | The bulletin and the email edition state a shared figure, deaths, live births, months held, provisional count, differently. This has happened once for real: fix the mart, not the template. |

None of these checks may be edited to make a failure pass. If a check is wrong, that is
itself a finding: fix the check, prove it still catches the defect it was written for
(inject the defect, confirm the check fires, then restore), and only then rerun.

## Recovering from a failed run

**`uv run python run.py` fails.** The most likely cause is a source CSV whose columns
changed shape. See `data-contract.md` for what "changed shape" means and how to update
`pipeline/mart/crosswalk.csv`. The pipeline does not partially write the mart on failure:
`mart/*.parquet` from the last successful run stays in place, so a failed rebuild does not
take down a currently-published bulletin.

**A check fails after a successful mart rebuild.** The mart built; the bulletin did not
publish. `output/bulletin-*.html` from the previous quarter's publish is untouched. Fix
the finding named in the failing check's output, rerun `bun run verify`, then `bun run
publish` again.

**Nothing published and it is the last week of the quarter.** Run:

```bash
cd deliverable-2-prototype/pipeline && uv run python run.py 2>&1 | tail -20
```

and read the last error. Every error in this pipeline names the file and the row or
column it choked on; there is no step that fails silently. If the error is not
self-explanatory, that is a bug in the pipeline's error message, not a sign you are
missing context, and should be reported the same way.

## Full clean rebuild, to prove this runbook is complete

```bash
cd deliverable-2-prototype
# git clean -fdX, not rm -rf: pipeline/mart mixes committed source files
# (crosswalk.csv, org_unit_map.csv, dhis2_sample.csv) with generated output
# (*.parquet, *.duckdb). -X removes only what .gitignore marks generated;
# a bare rm -rf pipeline/mart deletes the source files too, found the hard way
# while writing this runbook. Confirm nothing unexpected is listed first:
git clean -ndX pipeline/mart web/dist web/node_modules pipeline/.venv
git clean -fdX pipeline/mart web/dist web/node_modules pipeline/.venv
cd pipeline && uv sync && uv run python run.py
cd ../web && bun install && bun run publish && bun run verify
md5sum ../output/bulletin-2024-Q1.html
```

`bun run verify` prints five `passed` lines. The pipeline is byte-for-byte
reproducible: two clean runs on 2026-08-11 produced the identical hash
`05ce82f7889cc85f38ec61cdf3d4e0ab` for `output/bulletin-2024-Q1.html`, checked, not
assumed, because a batch job whose output silently drifts between identical inputs is a
worse failure mode than one that visibly errors.

This was run against this exact document on 2026-08-11 from a fully wiped state, with no
step added, removed, or reordered from what is written above. See
`deliverable-4-handover/README.md`, "Verification", for the result.
