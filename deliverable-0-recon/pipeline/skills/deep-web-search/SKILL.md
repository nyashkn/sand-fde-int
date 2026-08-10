---
name: deep-web-search
description: How a fabro agent node runs KN's web-research stack (Perplexity, Parallel.ai, Exa) plus native web tools, with a two-pass "discover then double-click" method and a strict citation format. Load this before any research lane.
---

# deep-web-search

You are a research lane in a fabro workflow. Produce **grounded, sourced** findings — never rely on parametric memory for facts about specific systems, vendors, laws, or deployments. Every non-obvious claim carries a source URL.

## Engines (in priority order)

All KN engines authenticate through the Infisical wrapper `infisical-kn-personal-dev`, which
injects the keys freshly from Infisical at call time. **Always prefix these commands with the
wrapper** — the sandbox strips `*_api_key` env vars, so the wrapper is the only reliable path.

1. **Perplexity** (grounded, cited synthesis) — best first pass per sub-question.
   MUST run under `uv run --with litellm` (the script needs litellm; bare python3 lacks it):
   ```bash
   infisical-kn-personal-dev uv run --with litellm \
     python3 ~/.claude/skills/perplexity-search/scripts/perplexity_search.py \
     "<specific question with time frame + domain>" --model sonar-pro --output out/.raw/pplx_<slug>.json
   ```
   Use `--model sonar-pro-search` ONLY for a hard multi-step sub-question (it is 10x the cost).

2. **Parallel.ai** — two modes:
   - **search** (fast, ~$0.01-0.03) — DEFAULT for lane discovery + corpus building:
     ```bash
     infisical-kn-personal-dev uv run --with parallel-web \
       python3 ~/.claude/skills/parallel-search/scripts/parallel_search.py search \
       --objective "<lane goal>" --max-chars 30000 --json > out/.raw/parallel_<slug>.json
     ```
   - **deep** (agentic synthesized report, SLOW: several minutes; $0.10-0.50) — it BLOCKS the lane,
     so use at most once per lane and only when `search`+Perplexity left a real gap:
     ```bash
     infisical-kn-personal-dev uv run --with parallel-web \
       python3 ~/.claude/skills/parallel-search/scripts/parallel_search.py deep \
       --query "<multi-paragraph question>" --processor pro-fast --json > out/.raw/parallel_deep_<slug>.json
     ```
   Never run `--processor ultra` unless explicitly told; never fire more than one `deep` at a time.

3. **Exa / native** — for discovery, company/vendor lookup, and known-URL extraction, use the
   fabro-native `web_search`, `web_fetch`, and (if available) `exa` tools you already have. Prefer
   these for cheap breadth; escalate to Perplexity/Parallel for depth + citations.

Write raw engine dumps under `out/.raw/` (create it); keep your lane `.md` clean and human-readable.

## Method: two passes ("discover, then double-click")

1. **Discover (breadth):** enumerate everything in scope for your lane — systems, vendors, laws,
   integration points. Cheap engines (native `web_search`, one Perplexity `sonar-pro` per
   sub-question).
2. **Double-click (depth):** pick the 3-5 most central items and research each in depth — one
   focused query per item (architecture, owner, data handled, integration points). This recursion
   is what turns a list into understanding. Note when a discovered item deserves its own deeper pass.

Stop when a second pass adds no new named systems/facts (diminishing returns), not on a fixed count.

## Output contract

Write your lane file `out/NN-<lane>.md` (the exact path is in your node prompt) with:

- A short **overview** (3-6 sentences).
- The **discovered inventory** (bulleted; each item = name + one line + source URL).
- **Double-click** subsections for the central items.
- A **gaps + confidence** note: what you could not verify, and how confident (high/med/low) each
  section is. Public docs on MoH-internal systems are thin — say so rather than inventing.
- **Citations inline** as `[claim](url)` or a trailing `Source: <url>` per bullet. No uncited facts.

## Guardrails

- Rwanda-specific: prefer primary sources — MoH Rwanda, RBC, NCSA, MINICT, HISP/DHIS2, OpenHIE,
  WHO/Global Fund country pages, published tenders, peer-reviewed digital-health papers.
- Never echo any API key. Never `cat` a secret. The wrapper handles auth.
- If an engine call fails (network/quota), fall back to the next engine; note the degradation in
  your gaps section. Do not silently drop a sub-question.
