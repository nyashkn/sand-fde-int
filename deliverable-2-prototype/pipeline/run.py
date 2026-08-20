"""Build the mart.

    uv run python run.py

Hamilton derives the DAG from function parameter names, so the lineage of every
output is the call graph itself rather than a diagram maintained alongside it.
"""

from __future__ import annotations

import sys
from pathlib import Path

import duckdb
from hamilton import driver

from dataflow import bronze as bronze_mod
from dataflow import checks as checks_mod
from dataflow import gold as gold_mod
from dataflow import silver as silver_mod

OUT = Path(__file__).resolve().parent / "mart"


def main() -> int:
    dr = driver.Builder().with_modules(bronze_mod, silver_mod, gold_mod, checks_mod).build()

    GOLD = ["facility_quarter", "district_quarter", "nmr_district_quarter",
            "nmr_facility_quarter", "completeness_summary",
            "temporal_signal_check", "stratification_check",
            "cause_capability_links", "facility_capability", "capability_summary",
            "known_contradictions"]
    result = dr.execute(["bronze", "bronze_dhis2", "silver", "org_units",
                         "crosswalk", "org_unit_map", "observations_resolved"] + GOLD)

    silver = result["silver"]
    org_units = result["org_units"]

    con = duckdb.connect(str(OUT / "mart.duckdb"))

    def publish(table: str, df) -> None:
        """Register explicitly under a distinct name.

        `CREATE OR REPLACE TABLE x AS SELECT * FROM x` silently reads the existing
        *table* rather than the DataFrame once x exists, so a second run re-copies
        stale rows and every change appears to have no effect.
        """
        con.register("_src", df)
        con.execute(f"CREATE OR REPLACE TABLE {table} AS SELECT * FROM _src")
        con.unregister("_src")

    publish("silver", silver)
    publish("org_units", org_units)
    for name, df in result["bronze"].items():
        publish("bronze_" + name.replace(".csv", ""), df)
    publish("bronze_dhis2", result["bronze_dhis2"])
    publish("crosswalk", result["crosswalk"])
    publish("org_unit_map", result["org_unit_map"])
    publish("observations_resolved", result["observations_resolved"])
    for name in GOLD:
        publish(name, result[name])

    # Parquet, not the DuckDB file, is the published artifact: it supports HTTP range
    # requests, so a browser pulls only the row groups it needs and the batch job reads
    # the same bytes. No service between the pipeline and the surface.
    #
    # observations_resolved is published because it is the only table carrying
    # rules_applied, and the bulletin's lineage section must read the rule name rather
    # than restate it. A hand-typed rule name in a provenance record is a fabrication
    # waiting to happen, and it happened once already.
    PUBLISHED = ["silver", "org_units", "observations_resolved"] + GOLD
    for name in PUBLISHED:
        con.execute(f"COPY {name} TO '{OUT / (name + '.parquet')}' (FORMAT PARQUET)")

    # Parquet stays the contract (ADR 0010): Python stops there, and Astro reads it
    # through DuckDB-WASM, never CSV. These five are a human-readable export on top,
    # not a replacement, for the small tables SOLUTION-DESIGN.md asks a reader to
    # verify directly. Kept small on purpose: a CSV sibling for silver or
    # observations_resolved would bloat the repo for no reader benefit.
    CSV_EXPORT = ["stratification_check", "temporal_signal_check",
                  "completeness_summary", "nmr_district_quarter", "capability_summary"]
    for name in CSV_EXPORT:
        con.execute(f"COPY {name} TO '{OUT / (name + '.csv')}' (FORMAT CSV, HEADER)")

    print(f"bronze     {sum(len(d) for d in result['bronze'].values()):>7,} rows "
          f"across {len(result['bronze'])} files")
    print(f"bronze2    {len(result['bronze_dhis2']):>7,} rows  (dhis2)")
    print(f"silver     {len(silver):>7,} observations")
    print(f"org_units  {len(org_units):>7,} "
          f"({', '.join(f'{k}:{v}' for k, v in org_units['level'].value_counts().items())})")
    for name in GOLD:
        print(f"gold       {len(result[name]):>7,}  {name}")
    print(f"\nwrote {len(PUBLISHED)} parquet files to {OUT}")
    print(f"wrote {len(CSV_EXPORT)} csv siblings to {OUT}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
