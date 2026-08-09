# Decision records

One file per non-obvious decision. Numbered, append-only — superseded decisions get a
`Superseded by` line rather than an edit, so the reasoning trail stays intact.

The point is not ceremony. It's that six weeks into an engagement, "why is it built this
way?" has a cheap answer, and a handover has something to hand over.

## Format

```
# NNNN — <decision, stated as the thing chosen>

- **Date:**
- **Status:** Accepted | Superseded by NNNN | Reversed
- **Context:** what forced a choice
- **Decision:** what was chosen
- **Alternatives:** what else was on the table, and why not
- **Reverses if:** the observation that would make this wrong
```

`Reverses if` is the field that earns its keep — a decision you can't imagine reversing
usually wasn't a decision.

## Index

| # | Decision | Status |
|---|---|---|
| [0001](0001-research-before-scoping.md) | Research Sand's real products before writing any scoping | Accepted |
| [0002](0002-video-analysis-for-product-grounding.md) | Use native video-input LLM analysis, not audio transcription alone | Accepted |
| [0003](0003-adopt-bluelake-ui-language.md) | Build the prototype in the Bluelake Admin UI language | Accepted |
| [0004](0004-no-pm-tooling-install.md) | Borrow decision/hypothesis patterns; don't install PM skill marketplaces | Accepted |
| [0005](0005-git-lfs-for-videos.md) | Track source videos with Git LFS rather than excluding them | Accepted |
| [0006](0006-problem-a-plus-handover-act.md) | Commit to Problem A plus one bounded handover act *(council)* | Accepted |
| [0007](0007-cross-provider-redteam-amendments.md) | Red-team D1 across three model families, and amend *(cross-provider)* | Accepted |

---

*Schema adapted from the decision-record pattern in
[phuryn/pm-brain](https://github.com/phuryn/pm-brain) — pattern borrowed, tooling not
installed (see 0004).*
