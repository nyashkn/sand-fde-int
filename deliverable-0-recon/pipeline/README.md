# Recon pipeline — operator guide

Target-agnostic. Three [fabro](https://fabro.sh) workflows + two scripts + two skills. Built and
verified on **fabro 0.316**.

```
pipeline/
  workflows/
    recon.fabro   recon.toml     # 7-lane MECE deep-research → html artifact
    refine.fabro  refine.toml    # embed source links + machine-vision review loop (×2)
    polish.fabro  polish.toml    # subtractive readability pass, verdict-gated, re-runnable
  scripts/
    shoot.sh                     # headless-Chrome full-page screenshot, trimmed with ImageMagick
    vision_review.py             # base64 a PNG → OpenRouter vision model → text critique md
  skills/
    deep-web-search/SKILL.md     # how a lane runs Perplexity / Parallel.ai / Exa, two-pass method
    html-artifact/SKILL.md       # how the visual node builds the self-contained page
```

## Prerequisites

- `fabro` 0.316+, server running (`fabro server start`).
- An LLM provider. This pipeline uses **OpenRouter** (`deepseek-v4-flash` workhorse, `minimax-m3`
  heavy, `kimi-k3` visual). Enable it with `[llm.providers.openrouter] enabled = true` in
  `~/.fabro/settings.toml` and reference catalog models by short key.
- API keys injected at call time. Here they come through an Infisical wrapper
  (`infisical-kn-personal-dev <cmd>`) because the local sandbox strips `*_api_key` env vars — the
  wrapper re-injects them. Substitute your own key-injection for the search CLIs and
  `vision_review.py` (it needs `OPENROUTER_API_KEY`).
- `google-chrome`/Chrome.app + ImageMagick (`magick`) for `shoot.sh`. macOS paths are hard-coded;
  edit `shoot.sh` for Linux.

## Run

```bash
# 1. Point recon.toml at your target + workspace, then:
fabro create workflows/recon.toml && fabro start <run_id>     # daemon-owned; poll `fabro inspect`
# 2. Once the artifact exists:
fabro create workflows/refine.toml && fabro start <run_id>    # links + vision review
# 3. If the vision verdict is "weak":
fabro create workflows/polish.toml && fabro start <run_id>    # subtractive; re-run until gate passes
```

Use `create` + `start` (not `fabro run`) for anything long: the daemon owns the run, so it survives
the client/shell dying. Recover a lost run_id from the streamed `--json` events
(`grep -oE '01[0-9A-HJKMNP-TV-Z]{24}'`).

## Adapting to a new target

- `recon.toml` → `[run] goal`: name the **target org, sector, jurisdiction**. The seven lanes read
  this goal.
- `recon.fabro` → the `SEED:` lines in the lane FOCUS prompts: optionally list the target's known
  systems / roles / statute to warm-start discovery. Everything else is generic.
- Models: edit each graph's `model_stylesheet` (`*` = workhorse, `.heavy` = synth/legal,
  `.visual` = artifact) for your provider.

## The eight gotchas (why the graphs look the way they do)

1. **`halt` is a plain `exit 1` sink, NOT a `goal_gate`.** In 0.316 an *unvisited* `goal_gate=true`
   node fails the whole run — so the happy path must visit every gate. The single goal-gate lives on
   the always-visited `coverage`/`verify` node.
2. **Parallel lanes edge into the join UNCONDITIONALLY** (`lane -> join`). Gating a parallel branch
   on `outcome=succeeded` + `-> halt` makes it take `halt` and skip the join. Per-lane success is
   enforced by the coverage gate instead. (`join_policy` was removed in 0.316.)
3. **`reasoning_effort` is per-model.** A `model_stylesheet` class applies it blindly; `minimax-m3`
   rejects any value but `none` and kills every node in the class. Don't set it unless the model
   supports it. Verify a model first: `fabro model test -m <key> -p <provider> --json`.
4. **fabro agents are text-only.** `read_file` does not attach image pixels — a vision model in an
   agent node returns "NO VISION". Automated vision must run in a `script` node (`vision_review.py`)
   and hand back *text*. fabro's native UI-review path is instead a human `preview` gate.
5. **Critic vs refiner incentive mismatch.** A refiner told to *add* increases density every pass
   (verdict regressed Acceptable→Weak). Use a separate **subtractive** pass (CSS/layout only, no
   content change) with a density ceiling, gated on the vision verdict.
6. **Cheap model for editing; premium/vision for judgement only.** kimi full-rewrites ran $3–4 and
   ~17 min each; the subtractive CSS pass on `deepseek-v4-flash` was **$0.05**. Reserve the vision
   model for the ~4k-token critique.
7. **OpenRouter credit headroom is per-request = `max_output × output_price`.** kimi-k3's
   `max_output=131072` reserves ~$2 *per request*; a low balance rejects it outright
   ("can only afford N tokens"). Cap `max_output` with a custom model block or use a smaller model.
   Check balance: `curl https://openrouter.ai/api/v1/credits -H "Authorization: Bearer $OPENROUTER_API_KEY"`.
8. **`goal="{{ goal }}"` in graph attrs now errors `validate`** (`goal_self_reference`) — the goal
   comes from the toml. And full-page screenshots: Chrome `--screenshot` captures only the window
   height, so render tall (`--window-size=1440,12000`) then `magick -trim`; use absolute tool paths
   in node scripts (non-login shells have a different PATH).

A fuller write-up of these lives in the author's fabro workflow notes; the essentials are here so
this folder stands alone.
