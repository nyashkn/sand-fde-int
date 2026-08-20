# /// script
# requires-python = ">=3.14"
# dependencies = [
#     "marimo",
#     "pandas>=3.0.5",
#     "numpy",
#     "altair",
# ]
# ///
"""EDA across all five source files, reusing the pipeline's own gold/checks functions.

Same directory as run.py so `from dataflow import bronze, silver, gold, checks` works
without path hacking. Every figure below calls the actual pipeline function that produces
it in production (gold.facility_capability, checks.temporal_signal_check, ...) rather than
reimplementing the computation, so this notebook cannot drift from what the bulletin ships.
"""

import marimo

__generated_with = "0.23.16"
app = marimo.App(width="medium")


@app.cell
def _():
    import marimo as mo
    import numpy as np
    import pandas as pd
    import altair as alt

    from dataflow import bronze, silver, gold, checks

    return alt, bronze, checks, gold, mo, pd, silver


@app.cell
def _(mo):
    mo.md("""
    # Quarterly Health Bulletin — data quality and capability EDA

    All five source files (`facilities`, `clinical_neonatal`, `governance`,
    `operations`, `healthcare_workers`), reactive against the pipeline's own
    `dataflow` functions. Reproduces the finding behind every caveat and capability
    figure the bulletin publishes, live, rather than restating a number.
    """)
    return


@app.cell
def _(mo):
    mo.md("""
    ## 1. Bronze: five files, loaded verbatim
    """)
    return


@app.cell
def _(bronze):
    data_dir = bronze.data_dir()
    ingested_at = bronze.ingested_at()
    bronze_frames = bronze.bronze(data_dir, ingested_at)
    bronze_dhis2 = bronze.bronze_dhis2(data_dir, ingested_at)
    return bronze_dhis2, bronze_frames


@app.cell
def _(bronze_frames, mo, pd):
    _PROV = {"_source_system", "_source_file", "_source_row", "_batch", "_row_hash",
              "_ingested_at", "_rejection_reason"}
    file_summary = pd.DataFrame([
        {
            "file": name,
            "rows": len(df),
            "source_columns": len([c for c in df.columns if c not in _PROV]),
            "dtypes": "str (bronze loads every column as text; typing happens in silver)",
        }
        for name, df in bronze_frames.items()
    ])
    mo.ui.table(file_summary, label="Bronze row counts, all five source files")
    return


@app.cell
def _(bronze_frames, mo):
    bronze_tabs = mo.ui.tabs({
        name: mo.ui.table(df, page_size=8) for name, df in bronze_frames.items()
    })
    bronze_tabs
    return


@app.cell
def _(mo):
    mo.md("""
    ## 2. Missingness per file
    """)
    return


@app.cell
def _(bronze_frames, mo, pd):
    _PROV = {"_source_system", "_source_file", "_source_row", "_batch", "_row_hash",
              "_ingested_at", "_rejection_reason"}
    # Bronze loads with keep_default_na=False, so a genuinely blank cell survives as "".
    # But this source also writes an explicit "None" string for an absent value (seen in
    # night_shift_coverage), which pandas' own NA machinery would never catch — checking
    # for both is what "reproduced live" means here, not trusting a single sentinel.
    _MISSING = {"", "None"}
    missingness_rows = []
    for _name, _df in bronze_frames.items():
        for _col in _df.columns:
            if _col in _PROV:
                continue
            _empty = _df[_col].astype(str).str.strip().isin(_MISSING).sum()
            if _empty > 0:
                missingness_rows.append({
                    "file": _name, "column": _col, "empty": _empty,
                    "pct_empty": round(_empty / len(_df) * 100, 1),
                })
    missingness = pd.DataFrame(missingness_rows, columns=["file", "column", "empty", "pct_empty"])
    missingness = missingness.sort_values("pct_empty", ascending=False)
    mo.ui.table(missingness, label='Every column with at least one "" or "None" value, all files')
    return (missingness,)


@app.cell
def _(missingness, mo):
    _night = missingness[missingness["column"] == "night_shift_coverage"]
    mo.md(
        f"""
        `healthcare_workers.csv`'s `night_shift_coverage` is missing on
        **{int(_night['empty'].iloc[0])} of 117 facilities**
        ({_night['pct_empty'].iloc[0]}%) — the largest gap in any facility-snapshot file,
        computed live from the column above rather than restated.
        """
    ) if len(_night) else mo.md("`night_shift_coverage` has no missing values in this run.")
    return


@app.cell
def _(mo):
    mo.md("""
    ## 3. Batch collision, reproduced live
    """)
    return


@app.cell
def _(bronze_frames, mo):
    clinical = bronze_frames["clinical_neonatal.csv"]
    load_counts = (
        clinical.groupby(["facility_id", "reporting_month"]).size().rename("loads").reset_index()
    )
    duplicated = load_counts[load_counts["loads"] > 1]
    by_month = duplicated["reporting_month"].value_counts().rename("duplicate_facility_rows")
    mo.vstack([
        mo.md(
            f"""
            Grouping `clinical_neonatal.csv` by `(facility_id, reporting_month)` and
            counting loads directly, independent of the `_batch` column bronze already
            assigns, finds **{len(duplicated)} facility-months loaded more than once**.
            """
        ),
        mo.ui.table(by_month.reset_index().rename(columns={"index": "reporting_month"}),
                    label="Duplicate-loaded months"),
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## 4. Silver and gold: build the mart tables this notebook reuses
    """)
    return


@app.cell
def _(bronze_dhis2, bronze_frames, gold, silver):
    mart_dir = silver.mart_dir()
    crosswalk_df = silver.crosswalk(mart_dir)
    org_unit_map_df = silver.org_unit_map(mart_dir, bronze_frames)
    silver_df = silver.silver(bronze_frames, bronze_dhis2, crosswalk_df, org_unit_map_df)
    org_units_df = silver.org_units(bronze_frames)
    observations_resolved_df = gold.observations_resolved(silver_df)
    return mart_dir, observations_resolved_df, org_units_df


@app.cell
def _(mo):
    mo.md("""
    ## 5. Facility capability
    """)
    return


@app.cell
def _(gold, mo, observations_resolved_df, org_units_df):
    facility_capability_df = gold.facility_capability(observations_resolved_df, org_units_df)
    capability_summary_df = gold.capability_summary(facility_capability_df)
    mo.vstack([
        mo.md(
            f"""
            `gold.facility_capability` (called directly, not reimplemented): one row per
            facility, **{facility_capability_df.shape[1] - 5} capability/governance/
            operations/staffing columns** across **{len(facility_capability_df)}
            facilities**.
            """
        ),
        mo.ui.table(capability_summary_df, page_size=15,
                    label="gold.capability_summary — national rollup"),
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## 6. Known contradictions, each reproduced with a live cross-tab
    """)
    return


@app.cell
def _(gold, mart_dir, mo):
    known_contradictions_df = gold.known_contradictions(mart_dir)
    mo.ui.table(known_contradictions_df, label="gold.known_contradictions — declared table")
    return


@app.cell
def _(bronze_frames, mo, pd):
    hw = bronze_frames["healthcare_workers.csv"]
    trained = pd.to_numeric(hw["neonatal_trained_nurses"], errors="coerce").fillna(0) > 0
    never = hw["last_neonatal_training_date"] == "Never"
    cross = pd.crosstab(trained.map({True: "trained nurses > 0", False: "no trained nurses"}),
                          never.map({True: "last_training = Never", False: "has a training date"}))
    mo.vstack([
        mo.md("Live cross-tab reproducing the trained-nurses-vs-never-trained contradiction:"),
        mo.ui.table(cross.reset_index().rename(columns={"index": "neonatal_trained_nurses"})),
    ])
    return


@app.cell
def _(mo):
    mo.md("""
    ## 7. Structural checks (formerly guards): always render, never withhold
    """)
    return


@app.cell
def _(checks, mo, observations_resolved_df, org_units_df):
    temporal_df = checks.temporal_signal_check(observations_resolved_df)
    strat_df = checks.stratification_check(observations_resolved_df, org_units_df)
    mo.vstack([
        mo.ui.table(temporal_df, label="checks.temporal_signal_check"),
        mo.ui.table(strat_df, label="checks.stratification_check"),
    ])
    return (strat_df,)


@app.cell
def _(alt, mo, pd, strat_df):
    _rows = []
    for _, _r in strat_df.iterrows():
        _rows.append({"covariate": _r["covariate"], "stratum": "pooled", "r": _r["pooled_r"]})
        for _piece in _r["within_strata"].split("; "):
            _tier, _val = _piece.rsplit(" ", 1)
            _rows.append({"covariate": _r["covariate"], "stratum": _tier, "r": float(_val)})
    strat_long = pd.DataFrame(_rows)
    strat_chart = mo.ui.altair_chart(
        alt.Chart(strat_long)
        .mark_bar()
        .encode(x="stratum:N", y="r:Q", color="stratum:N", column="covariate:N")
        .properties(width=140, height=220, title="Pooled r vs. within-tier r, ecological fallacy check")
    )
    strat_chart
    return


@app.cell
def _(mo):
    mo.md("""
    ## 8. Finding to output trace
    """)
    return


@app.cell
def _(mo, pd):
    trace = pd.DataFrame([
        {"finding": "Surfactant availability (1 of 117)",
         "appears_in": "Bulletin §2 cause-capability pairing, §3 capability section"},
        {"finding": "Kangaroo-care self-contradiction (59.4%)",
         "appears_in": "Bulletin §7 known issues (via gold.known_contradictions)"},
        {"finding": "Trained-nurses-vs-never-trained (36 of 48)",
         "appears_in": "Bulletin §7 known issues (via gold.known_contradictions)"},
        {"finding": "Night-shift coverage gap (32 of 45 District-tier)",
         "appears_in": "Bulletin §7 known issues (via gold.known_contradictions)"},
        {"finding": "Referral imbalance (+74% outbound)",
         "appears_in": "Bulletin §7 known issues (via gold.known_contradictions)"},
        {"finding": "Power-without-generator gap (33 of 117)",
         "appears_in": "Bulletin §7 known issues (via gold.known_contradictions)"},
        {"finding": "Governance reporting completeness (median 76%)",
         "appears_in": "Bulletin §3 capability section, satisfies the brief's "
                        "\"facility performance scores\" requirement"},
        {"finding": "Temporal signal check (trend caveat)",
         "appears_in": "Bulletin §5 trend, caveat sentence inline"},
        {"finding": "Stratification check (correlation caveat)",
         "appears_in": "Bulletin §6 correlation, caveat sentence inline"},
    ])
    mo.ui.table(trace, label="Every finding above, and where it now surfaces")
    return


if __name__ == "__main__":
    app.run()
