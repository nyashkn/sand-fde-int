# 0004 — Borrow decision/hypothesis patterns; don't install PM skill marketplaces

- **Date:** 2026-08-09
- **Status:** Accepted

## Context

Considered adopting [phuryn/pm-skills](https://github.com/phuryn/pm-skills) (68 skills, 42
slash commands, 9 plugins, ~25k stars) and [phuryn/pm-brain](https://github.com/phuryn/pm-brain)
(file-based decision/hypothesis tracking, ~515 stars, self-described research preview,
last commit ~3 months stale) to make the scoping process visibly systematic.

Both were evaluated by reading actual repo contents, not just READMEs.

## Decision

Install neither. Borrow the two patterns that earn their place:

- pm-brain's **decision-record schema** → this folder.
- Its **hypothesis-tracking** idea → folded into the scoping doc's "assumptions to validate
  in Week 2" section, which the brief explicitly asks for anyway.

## Alternatives

- **Install pm-skills.** Roughly 3 of 68 skills are relevant here (`create-prd`,
  `pre-mortem`, `opportunity-solution-tree`). Nine plugins of overhead for three frameworks
  I can apply directly is a bad trade on a one-week deliverable.
- **Install pm-brain and run its bootstrap interview.** Its stakeholder/ingestion/maintenance
  layers are built for multi-week PM cadences. On a one-week assignment they'd generate
  scaffolding with nothing in it — the exact "process theatre" that makes a repo look
  busier rather than better.

## Reasoning

A reviewer can tell the difference between a decision log with five real decisions in it and
a bootstrapped template with five empty folders. Adopting someone else's marketplace to
demonstrate systematic thinking also inverts the thing being demonstrated: the brief asks to
see *my* process, and a generated scaffold shows a tool's.

The discipline is the artifact. The tooling is incidental.

## Reverses if

This engagement extends past the assignment into real multi-week delivery, where pm-brain's
weekly `/review` sweep and stakeholder tracking would start paying for their setup cost.
