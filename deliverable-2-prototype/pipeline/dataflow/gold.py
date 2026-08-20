"""Gold — the marts a bulletin reads.

Two things happen here that are worth reading carefully.

**Provisional propagates.** An aggregate over any provisional input is provisional and
carries the count of provisional inputs. A renderer cannot recompute this — the email
surface has no JavaScript — so it travels as a column.

**The batch default is declared, not inferred.** Where a period arrives twice, gold picks
the lowest occurrence ordinal so the pipeline can complete. That choice is *arbitrary and
labelled as such*: nothing in the source establishes which load is correct. The figure is
marked provisional and names the conflict. Calling this "latest" would restate the defect
as a fix.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

# Declared default for an unresolved batch collision. Named and versioned so it appears
# in lineage as a rule, not as an anonymous .drop_duplicates().
BATCH_DEFAULT_RULE = "DEFAULT-BATCH-01"

# Expected reporting months per quarter. Makes `incomplete` computable rather than
# asserted — a quarter knows what it should have received.
QUARTER_MONTHS = {
    "2024-Q1": ["2024-01", "2024-02", "2024-03"],
    "2024-Q2": ["2024-04", "2024-05", "2024-06"],
    "2024-Q3": ["2024-07", "2024-08", "2024-09"],
    "2024-Q4": ["2024-10", "2024-11", "2024-12"],
}
MONTH_TO_QUARTER = {m: q for q, ms in QUARTER_MONTHS.items() for m in ms}


def observations_resolved(silver: pd.DataFrame) -> pd.DataFrame:
    """One observation per (org_unit, period, data_element), with the collision recorded.

    Collapses batch, which is the only place in the pipeline where a choice between
    conflicting values is made. Every such choice is stamped with the rule that made it
    and flagged provisional, so no figure downstream can appear settled by accident.
    """
    df = silver[silver["source_system"] == "assignment_csv"].copy()
    key = ["org_unit", "period", "data_element"]

    counts = df.groupby(key)["batch"].transform("nunique")
    df["batch_count"] = counts

    # Lowest ordinal wins. Arbitrary by construction — see module docstring.
    df = df.sort_values(key + ["batch"])
    resolved = df.drop_duplicates(subset=key, keep="first").copy()

    contested = resolved["batch_count"] > 1
    resolved["provisional"] = contested
    resolved["rules_applied"] = resolved["rules_applied"].where(
        ~contested, BATCH_DEFAULT_RULE
    )
    resolved["quality_flags"] = resolved["quality_flags"].where(
        ~contested, "batch-duplicate"
    )
    return resolved


def facility_quarter(observations_resolved: pd.DataFrame, org_units: pd.DataFrame) -> pd.DataFrame:
    """Per-facility, per-quarter measures, with completeness and provisional carried."""
    df = observations_resolved[observations_resolved["period"] != "ALL"].copy()
    df["quarter"] = df["period"].map(MONTH_TO_QUARTER)
    df = df[df["quarter"].notna()]

    agg = (
        df.groupby(["org_unit", "quarter", "data_element"])
        .agg(
            value=("value_num", "sum"),
            months_received=("period", "nunique"),
            provisional_inputs=("provisional", "sum"),
            n_inputs=("value_num", "size"),
        )
        .reset_index()
    )
    agg["months_expected"] = agg["quarter"].map(lambda q: len(QUARTER_MONTHS[q]))
    agg["complete"] = agg["months_received"] == agg["months_expected"]
    agg["provisional"] = agg["provisional_inputs"] > 0

    dims = org_units[org_units["level"] == "facility"][
        ["org_unit", "name", "tier", "district", "province"]
    ]
    return agg.merge(dims, on="org_unit", how="left")


def district_quarter(facility_quarter: pd.DataFrame) -> pd.DataFrame:
    """Roll facilities up to district. Provisional cannot be laundered by aggregation."""
    agg = (
        facility_quarter.groupby(["district", "quarter", "data_element"])
        .agg(
            value=("value", "sum"),
            facilities=("org_unit", "nunique"),
            provisional_inputs=("provisional_inputs", "sum"),
            n_inputs=("n_inputs", "sum"),
            all_complete=("complete", "all"),
        )
        .reset_index()
    )
    agg["provisional"] = agg["provisional_inputs"] > 0
    agg["org_unit"] = "district:" + agg["district"]
    return agg


def _rate(df: pd.DataFrame, num_elements: list[str], den_element: str,
          by: list[str], per: int = 1000) -> pd.DataFrame:
    """Numerator over denominator, keeping both so a figure can show its own arithmetic."""
    num = (
        df[df["data_element"].isin(num_elements)]
        .groupby(by)
        .agg(numerator=("value", "sum"),
             provisional_inputs=("provisional_inputs", "sum"))
        .reset_index()
    )
    den = (
        df[df["data_element"] == den_element]
        .groupby(by)
        .agg(denominator=("value", "sum"))
        .reset_index()
    )
    out = num.merge(den, on=by, how="inner")
    out["value"] = (out["numerator"] / out["denominator"] * per).round(2)
    out["provisional"] = out["provisional_inputs"] > 0
    return out


def nmr_district_quarter(district_quarter: pd.DataFrame) -> pd.DataFrame:
    """Neonatal mortality per 1,000 live births, WHO GHO definition, by district-quarter."""
    return _rate(
        district_quarter,
        ["neonatal_deaths_early", "neonatal_deaths_late"],
        "live_births",
        ["district", "quarter"],
    )


def nmr_facility_quarter(facility_quarter: pd.DataFrame) -> pd.DataFrame:
    """Same measure at facility grain. Declared separately so grain is never implied."""
    return _rate(
        facility_quarter,
        ["neonatal_deaths_early", "neonatal_deaths_late"],
        "live_births",
        ["org_unit", "district", "name", "tier", "quarter"],
    )


def completeness_summary(silver: pd.DataFrame) -> pd.DataFrame:
    """Expected versus received per period, and what is contested.

    Required by trust-lineage on every edition. Computed from the data rather than
    written by hand, so it cannot drift from what was actually ingested.
    """
    monthly = silver[
        (silver["period"] != "ALL") & (silver["source_system"] == "assignment_csv")
    ]
    facilities = monthly["org_unit"].nunique()

    rows = []
    for quarter, months in QUARTER_MONTHS.items():
        for month in months:
            sub = monthly[monthly["period"] == month]
            received = sub["org_unit"].nunique()
            batches = sub["batch"].nunique()
            rows.append({
                "quarter": quarter,
                "period": month,
                "facilities_expected": facilities,
                "facilities_received": received,
                "batches": batches,
                "state": (
                    "absent" if received == 0
                    else "contested" if batches > 1
                    else "complete"
                ),
            })
    return pd.DataFrame(rows)


# Facility-snapshot elements (silver's `_DIMENSION_PERIOD="ALL"`), the four families the
# crosswalk maps every governance/operations/healthcare_workers/capability field into.
_CAPABILITY_PREFIXES = ("staff_", "governance_", "ops_", "capability_")


def cause_capability_links(mart_dir: Path) -> pd.DataFrame:
    """Cause of death paired with the specific capability gap most relevant to it.

    Declared as data, mirroring `silver.crosswalk()`'s exact read pattern: the pairing is
    a clinical judgement call, not a statistical inference, so it belongs in a table a
    non-engineer can review, not in code.
    """
    return pd.read_csv(mart_dir / "cause_capability_links.csv", keep_default_na=False)


def known_contradictions(mart_dir: Path) -> pd.DataFrame:
    """Contradictions already found and recorded, verbatim, in the crosswalk's own notes.

    Declared as data for the same reason as `cause_capability_links`: these are read
    directly off `mart/crosswalk.csv`'s `note` column, not recomputed or reworded here.
    """
    return pd.read_csv(mart_dir / "known_contradictions.csv", keep_default_na=False)


def facility_capability(observations_resolved: pd.DataFrame, org_units: pd.DataFrame) -> pd.DataFrame:
    """One row per facility, one column per staff/governance/ops/capability element.

    Facility-snapshot elements are stamped `period="ALL"` (`silver._DIMENSION_PERIOD`), so
    this is a straight pivot, no time reshaping. `observations_resolved` is already
    deduplicated to one row per (org_unit, period, data_element), so no aggregation
    function is needed to unstack it.
    """
    snap = observations_resolved[
        (observations_resolved["period"] == "ALL")
        & observations_resolved["data_element"].str.startswith(_CAPABILITY_PREFIXES)
    ].copy()
    # A column carries whichever form the source used: numeric where the field is
    # numeric, text where it is categorical (Yes/No/Partial/Never/...).
    snap["value"] = snap["value_text"].where(snap["value_num"].isna(), snap["value_num"])
    wide = snap.set_index(["org_unit", "data_element"])["value"].unstack()

    dims = org_units[org_units["level"] == "facility"][
        ["org_unit", "name", "tier", "district", "province"]
    ]
    return wide.reset_index().merge(dims, on="org_unit", how="left")


def capability_summary(facility_capability: pd.DataFrame) -> pd.DataFrame:
    """National rollup, one row per capability metric (numeric), or per metric-category
    pair (categorical).

    Which branch a metric takes is decided from its own values, not a hand-maintained
    list, so a new capability element in the crosswalk is summarised correctly without a
    code change here. Categorical fields report every value's own count and share rather
    than a single "affirmative" bucket, because which category is the finding differs by
    field: "Yes" for protocol status, "Never" for last-training-date.
    """
    dim_cols = {"org_unit", "name", "tier", "district", "province"}
    metric_cols = [c for c in facility_capability.columns if c not in dim_cols]

    rows = []
    for metric in metric_cols:
        s = facility_capability[metric].dropna()
        n_facilities = len(s)
        if n_facilities == 0:
            continue
        numeric = pd.to_numeric(s, errors="coerce")
        if numeric.notna().all():
            rows.append({
                "metric": metric, "category": None, "kind": "numeric",
                "n_facilities": n_facilities, "n_with": None, "pct_with": None,
                "median": float(numeric.median()), "min": float(numeric.min()),
                "max": float(numeric.max()), "mean": round(float(numeric.mean()), 3),
            })
        else:
            for category, n_with in s.value_counts().items():
                rows.append({
                    "metric": metric, "category": str(category), "kind": "categorical",
                    "n_facilities": n_facilities, "n_with": int(n_with),
                    "pct_with": round(int(n_with) / n_facilities * 100, 1),
                    "median": None, "min": None, "max": None, "mean": None,
                })
    return pd.DataFrame(rows)
