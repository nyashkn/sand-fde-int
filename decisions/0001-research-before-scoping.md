# 0001, Research Sand's real products before writing any scoping

- **Date:** 2026-08-09
- **Status:** Accepted

## Context

The brief instructs candidates to "reference actual Sand products" and lists five by name:
Health Atlas, Health Outcome Tracker, Health Insight Engine, Analytics Template Toolkit,
HealthOS Data Models. None of the five appear anywhere in Sand's public materials under
those names. Writing a scoping document that name-drops them without knowing what they are
would produce confident nonsense, the exact failure mode an FDE brings to a Ministry.

## Decision

Spend the first working block on evidence gathering before writing a line of scoping:
six parallel research agents against sandtech.com, AWS Marketplace, Rwanda MoH press,
and Sand's own job postings, with every finding graded confirmed / inferred / unevidenced.

Research is a prerequisite here, not a parallel track, the scoping decisions depend on
knowing which capabilities already exist and which would be a greenfield build.

## Alternatives

- **Take the five product names at face value and scope against them.** Faster, and the
  document would read fluently. But it would assert an architecture that doesn't exist, and
  any Sand engineer reading it would know immediately.
- **Ask the recruiter what the products are.** Legitimate, but the brief explicitly says
  working with uncertainty and partial information is part of the assignment.

## Reverses if

Sand publishes a technical product sheet, or an interviewer confirms the five names are real
internal SKUs. Neither changes the architecture conclusions, only how they'd be labelled.
