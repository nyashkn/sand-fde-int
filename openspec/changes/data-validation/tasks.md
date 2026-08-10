## 1. Registry and record shapes

- [ ] 1.1 Define the check registry record: id, version, scope enum (row/column/batch/cross-file/file), severity enum (blocker/material/cosmetic), disposition enum (auto-resolvable/needs-human/informational), description, and the object it attaches to
- [ ] 1.2 Define the finding record: check id, check version, scope key, examined population, measured values, outcome, run id, seed where stochastic
- [ ] 1.3 Define the resolution record: finding key, decider, decided at, option chosen, stated reason, supersedes
- [ ] 1.4 Define the provisional columns carried on silver and gold rows, including the provisional-input count that survives aggregation
- [ ] 1.5 Confirm every record shape references objects by the identity rules from `conceptual-model`, not by source keys

## 2. Port the 17 audited findings into registered checks

- [ ] 2.1 Row-scope checks: protocol-training contradiction (14/14), training-date vs trained-count (36/48), impossible stockout days (11/117), missing backup power with powered equipment (33/117)
- [ ] 2.2 Column-scope checks: unreconciled derived column, quantised-uniform column, future-dated column, near-constant column, broken clinical reconciliation
- [ ] 2.3 Batch-scope check: whole-period collision detection, raising exactly one conflict per affected period
- [ ] 2.4 Cross-file checks: kangaroo-care space vs practice (19/32), tier-capability collapse, tier-inappropriate specialist staffing, night-coverage gap at tier
- [ ] 2.5 File-scope checks: referral network imbalance, absent expected periods
- [ ] 2.6 Verify each ported check reproduces the exact number recorded in `artifacts/04-data-quality-audit.html`, including its denominator

## 3. Structural guards

- [ ] 3.1 Temporal-signal guard: compute observed lag-1 autocorrelation and the within-entity permutation null over a fixed seed, record both, and mark the series as carrying no temporal signal when the null is not exceeded
- [ ] 3.2 Wire the guard so a period-over-period presentation on a no-signal series is refused, and the refusal reason is emitted in its place
- [ ] 3.3 Stratification guard: require any association presented as explanatory to declare its stratification variable, and refuse it when the association does not survive within strata
- [ ] 3.4 Verify the guard refuses the capability/NMR pooled correlation (pooled -0.844, within-tier +0.042/+0.111/+0.144) and permits an association that does survive
- [ ] 3.5 Verify the derived-column guard refuses `staff_per_delivery_2024` (best formula 58.1% versus mode baseline 65.8%)

## 4. Disposition behaviour

- [ ] 4.1 Confirm no check path mutates, drops, or defaults a value anywhere in the pipeline
- [ ] 4.2 Confirm rejected rows remain retrievable in original form with their rejection reason
- [ ] 4.3 Confirm a run with unresolved conflicts completes and emits output
- [ ] 4.4 Confirm a recorded resolution is reapplied on the next run without human involvement, and clears provisional state on exactly the affected figures
- [ ] 4.5 Confirm provisional state survives aggregation and that the provisional-input count is retrievable
- [ ] 4.6 Confirm a renderer that cannot express provisional state omits the figure rather than presenting it as settled

## 5. Clean-result recording

- [ ] 5.1 Record pass results with the population examined, so a pass is distinguishable from silence
- [ ] 5.2 Record non-execution distinctly from a pass
- [ ] 5.3 Reproduce the 31 clean checks from the audit as registered checks that record positive evidence

## 6. Edition summary

- [ ] 6.1 Emit expected-versus-received inputs per source, per period, per entity
- [ ] 6.2 Emit unresolved conflicts grouped by scope
- [ ] 6.3 Emit any presentation withheld under the refusal rules, with its reason
- [ ] 6.4 Verify the summary correctly reports 2024-02 and 2024-12 as absent and Q1/Q4 as incomplete

## 7. Record and hand off

- [ ] 7.1 Record the DUP-01 withdrawal and its replacement as an ADR, citing the measurements that made ordering undefendable
- [ ] 7.2 Answer or explicitly defer the two open questions in `design.md`
- [ ] 7.3 Confirm `ingest-mart` has the bronze-retention and silver-column requirements it inherits
- [ ] 7.4 Confirm `bulletin-render` has the provisional-rendering and refusal-disclosure requirements it inherits
