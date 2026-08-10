"""Bronze — source data exactly as received.

Two rules govern this layer and nothing else may override them:

1. Field names and values are the source's, unmodified. Bronze must stay auditable
   against the file the Ministry actually sent.
2. Nothing is dropped. A row a check rejects is evidence, not garbage, so it stays
   here with its reason attached.

The only thing bronze *adds* is batch identity — see `_assign_batch` for why that
is not a violation of rule 1.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd

SOURCE_FILES = [
    "facilities.csv",
    "clinical_neonatal.csv",
    "governance.csv",
    "healthcare_workers.csv",
    "operations.csv",
]

# Fields that identify a logical reporting unit within a source. Used only to detect
# repeated loads; never to deduplicate them.
_GRAIN_KEYS = ["facility_id", "reporting_month"]


def _assign_batch(df: pd.DataFrame, source_system: str, source_file: str) -> pd.Series:
    """Label each row with the load it belongs to.

    The sample ships two complete loads of 2024-01 and two of 2024-03 concatenated into
    one file — row-index gap is exactly 117 for all 234 pairs, so these are whole-batch
    double-loads rather than per-facility corrections.

    Batch is the Nth *occurrence* of a (facility, period) pair, not a timestamp. That
    distinction is deliberate. Nothing in the source establishes which load was
    submitted later: there is no timestamp column, both rows are always internally
    consistent, and the directional split is 113 vs 119. Naming these `occ1`/`occ2`
    records that we found two loads without asserting an order we cannot support.

    Calling them `latest` and `previous` would be the whole defect, restated as a fix.
    """
    keys = [k for k in _GRAIN_KEYS if k in df.columns]
    if not keys:
        # Dimension file — one row per facility, no period, so one batch.
        return pd.Series(f"{source_system}:{source_file}:occ1", index=df.index)
    occurrence = df.groupby(keys).cumcount() + 1
    return source_system + ":" + source_file + ":occ" + occurrence.astype(str)


def _row_hash(df: pd.DataFrame) -> pd.Series:
    """Stable content hash per row, so a re-ingest is recognisable as the same bytes."""
    joined = df.astype(str).agg("\x1f".join, axis=1)
    return joined.map(lambda s: hashlib.sha256(s.encode()).hexdigest()[:16])


def data_dir() -> Path:
    """Location of the provided sample data. Overridable at execution time."""
    return Path(__file__).resolve().parents[3] / "assignment" / "data"


def ingested_at() -> str:
    """Single ingest timestamp for the whole run, so one run is one provenance event."""
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def bronze(data_dir: Path, ingested_at: str) -> dict[str, pd.DataFrame]:
    """Load every source file verbatim, adding only provenance.

    Returns a frame per source file. Original column names survive untouched; the six
    added columns are all prefixed `_` so they cannot collide with a source field.
    """
    out: dict[str, pd.DataFrame] = {}
    for name in SOURCE_FILES:
        # dtype=str throughout: parsing is silver's job. Bronze must not coerce
        # '35' into an int, or a leading zero disappears and the audit trail with it.
        df = pd.read_csv(data_dir / name, dtype=str, keep_default_na=False)
        df["_source_system"] = "assignment_csv"
        df["_source_file"] = name
        df["_source_row"] = range(len(df))
        df["_batch"] = _assign_batch(df, "assignment_csv", name)
        df["_row_hash"] = _row_hash(df.drop(columns=["_batch"], errors="ignore"))
        df["_ingested_at"] = ingested_at
        df["_rejection_reason"] = ""  # populated by data-validation; never removes a row
        out[name] = df
    return out


def bronze_dhis2(data_dir: Path, ingested_at: str) -> pd.DataFrame:
    """Second source: a small DHIS2-shaped export.

    Exists to test a claim the crosswalk makes but one source cannot prove — that a new
    source is onboarded by adding mapping rows, not pipeline code. Its field names are
    DHIS2's real ones (`orgUnit`, `period`, `dataElement`, `value`), which share nothing
    with the CSV column names, so convergence in silver is a real result rather than a
    coincidence of naming.
    """
    path = data_dir.parent.parent / "deliverable-2-prototype" / "pipeline" / "mart" / "dhis2_sample.csv"
    df = pd.read_csv(path, dtype=str, keep_default_na=False)
    df["_source_system"] = "dhis2"
    df["_source_file"] = "dhis2_sample.csv"
    df["_source_row"] = range(len(df))
    df["_batch"] = "dhis2:dhis2_sample.csv:occ1"
    df["_row_hash"] = _row_hash(df)
    df["_ingested_at"] = ingested_at
    df["_rejection_reason"] = ""
    return df
