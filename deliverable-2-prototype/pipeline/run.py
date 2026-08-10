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
from dataflow import silver as silver_mod

OUT = Path(__file__).resolve().parent / "mart"


def main() -> int:
    dr = driver.Builder().with_modules(bronze_mod, silver_mod).build()

    result = dr.execute(["bronze", "bronze_dhis2", "silver", "org_units",
                        "crosswalk", "org_unit_map"])

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

    # Parquet, not the DuckDB file, is the published artifact: it supports HTTP range
    # requests, so a browser pulls only the row groups it needs and the batch job reads
    # the same bytes. No service between the pipeline and the surface.
    con.execute(f"COPY silver TO '{OUT / 'silver.parquet'}' (FORMAT PARQUET)")
    con.execute(f"COPY org_units TO '{OUT / 'org_units.parquet'}' (FORMAT PARQUET)")

    print(f"bronze     {sum(len(d) for d in result['bronze'].values()):>7,} rows "
          f"across {len(result['bronze'])} files")
    print(f"bronze2    {len(result['bronze_dhis2']):>7,} rows  (dhis2)")
    print(f"silver     {len(silver):>7,} observations")
    print(f"org_units  {len(org_units):>7,} "
          f"({', '.join(f'{k}:{v}' for k, v in org_units['level'].value_counts().items())})")
    print(f"\nwrote {OUT/'silver.parquet'}")
    con.close()
    return 0


if __name__ == "__main__":
    sys.exit(main())
