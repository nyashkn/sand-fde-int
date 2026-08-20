# PRODUCT.md

**register:** product

## What this is

A quarterly health bulletin for Rwanda's Ministry of Health, generated from DHIS2-shaped
facility data. It replaces roughly 40 hours a month of manual Excel compilation.

The generation is not the hard part. An adversarial review of the engagement found that the
Director's stated complaint, *"our data is a mess, we cannot make good decisions"*, is not
about throughput. It is about trust: *"I cannot trust any number I am shown."* Producing
distrusted numbers faster is not an improvement.

So the product is not a report generator. It is **a document whose every number can be
interrogated**, and which states plainly, as a caveat, when the data cannot support a claim.

## Users

**The Director, MoH.** Primary. Quotes figures publicly and must defend them when
challenged. Arrives asking *can I trust this document*, not *what is the number*, he can
already get numbers, he cannot currently defend them. Needs the headline figure, its state,
and what backs it, in the first screen. Reads on a laptop, often forwarded by email.

**A District Health Officer.** Secondary. Arrives asking *what is happening in my district
and what do I do about it*. Needs to find their district without reading anything addressed
to the Director. Works with 4 to 6 hours of power a day and intermittent 3G, so the document
must work offline once opened.

**An MoH analyst.** Tertiary. Currently does the manual compilation. Arrives asking *where
did this number come from and what did the pipeline do to it*. Needs lineage, the conflict
queue, and enough detail to answer a challenge from either of the above.

**The MoH IT team.** At handover. Arrives asking *can we run this without them*. One named
Digital Health Officer must restart the pipeline unassisted before exit; that act is the
difference between the engagement succeeding and not.

## Tone

Plain, exact, unhedged. Numbers carry their denominators. Uncertainty is stated in the same
breath as the claim it qualifies, never in a footnote.

The document says what it does not know as readily as what it does. A caveat says why a
claim does not clear its statistical bar, in the position the claim would have occupied. A
partial quarter names the months it is missing, next to the figure rather than in an
appendix. Known defects in the source data are published rather than quietly corrected.

Never reassuring. Never promotional. A reader should finish a section knowing exactly how
much weight it will bear.

## Anti-references

- **A dashboard.** Not a wall of KPI tiles with sparklines. There is no live operational
  decision being made here; this is a document that gets read, quoted, and filed.
- **The hero-metric template.** Big number, small label, gradient accent, three supporting
  stats. It implies confidence the data does not have.
- **Healthcare white-and-teal.** The first-order category reflex. The engagement already has
  a warm earth palette; use it.
- **A trend arrow.** The single most expected element in a quarterly bulletin, and this data
  cannot support one. Its absence is a feature and is stated as such.
- **Clean numbers.** A bulletin that renders tidy figures over data with two duplicated
  months and two absent ones is exactly the object the Director already refuses.

## Strategic principles

**Disclosure is a feature.** Where the data does not clear its statistical bar, the document
says so, as a caveat, in the position the claim would have occupied. Demoting that caveat to
a footnote would make it look like an omission.

**Every figure is interrogable.** State and lineage travel with the number, as data, through
every surface including ones that cannot execute code.

**The reader should not need us.** The document is self-contained, works offline, and
explains its own provenance. If it needs a person to interpret it, it has failed the handover
test that defines the engagement's success.

**Inherit, do not reinvent.** Tokens, vocabulary, and standards come from what already
exists: the engagement's own design system, DHIS2's data model, ICD-10, WHO GHO.
