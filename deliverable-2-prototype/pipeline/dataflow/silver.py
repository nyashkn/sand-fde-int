"""Silver — canonical observations at DHIS2 grain.

Grain is `(org_unit, period, data_element, batch)`.

`batch` is in the key, and that is the load-bearing decision in this module. Without it
the two January loads collide on the natural key and one silently overwrites the other —
which is the defect, not a fix for it. With it, both are retained and the ambiguity is
representable, which is what lets a figure be honestly marked provisional.

Mapping happens through `mart/crosswalk.csv`, never through logic here. Onboarding a new
source should be rows in that file plus a format parser, and nothing else.
"""

from __future__ import annotations

import re
from pathlib import Path

import pandas as pd

# Columns bronze adds. Never confused with a source field because of the `_` prefix.
_PROV = ["_source_system", "_source_file", "_source_row", "_batch", "_row_hash",
         "_ingested_at", "_rejection_reason"]

# Files whose rows describe a facility rather than a facility-month. Their observations
# are stamped with a sentinel period so they share one grain with everything else.
_DIMENSION_PERIOD = "ALL"


def crosswalk(mart_dir: Path) -> pd.DataFrame:
    """The source-to-canonical mapping, read as data at runtime.

    Deliberately not compiled into a Python module at build time: it has to stay
    inspectable by a non-engineer at handover, and a generated artifact would become
    the thing people actually read.
    """
    cw = pd.read_csv(mart_dir / "crosswalk.csv", keep_default_na=False)
    return cw


def mart_dir() -> Path:
    return Path(__file__).resolve().parents[1] / "mart"


def _normalise_period(value: str, source_system: str) -> str:
    """Bring every source's period notation to ISO YYYY-MM."""
    if source_system == "dhis2":
        # DHIS2 monthly periods are YYYYMM.
        return f"{value[:4]}-{value[4:6]}" if re.fullmatch(r"\d{6}", value) else value
    return value


def org_unit_map(mart_dir: Path, bronze: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """Resolve `(source_system, source_key)` to one shared org_unit identity.

    `conceptual-model` requires that the same facility arriving from two sources under
    different keys resolves to a *single* object identity, with both originating keys
    retained. A surrogate of the form `<source>:<key>` fails that — it manufactures one
    identity per source and silently doubles every facility.

    The registry from `facilities.csv` is the roster: it defines which facilities exist.
    Every other source resolves through `mart/org_unit_map.csv`, which is *declared*
    data, not inferred.

    Deliberately no exact-key auto-matching. Two systems using the string `NYA001` is
    evidence that they share a code space, not proof — and silently fusing on string
    equality is how an identity graph merges two distinct real-world entities. If a key
    is not in the map, it stays unresolved and becomes a finding rather than a new
    facility that quietly appears in the roster.
    """
    f = bronze["facilities.csv"]
    roster = pd.DataFrame({
        "source_system": "assignment_csv",
        "source_key": f["facility_id"],
        "org_unit": "facility:" + f["facility_id"],
        "basis": "Registry. facilities.csv is the facility roster for this engagement.",
    })
    declared = pd.read_csv(mart_dir / "org_unit_map.csv", keep_default_na=False)
    return pd.concat([roster, declared], ignore_index=True)


def silver(
    bronze: dict[str, pd.DataFrame],
    bronze_dhis2: pd.DataFrame,
    crosswalk: pd.DataFrame,
    org_unit_map: pd.DataFrame,
) -> pd.DataFrame:
    """Unpivot every source to `(org_unit, period, data_element, batch, value)`.

    The wide CSVs are DHIS2's own model pivoted sideways, so unpivoting recovers the
    grain the Ministry's HMIS already speaks. That is what lets HealthTrack, OpenMRS and
    paper entry land here later without reshaping anything.
    """
    obs_map = crosswalk[crosswalk["role"] == "observation"]
    frames: list[pd.DataFrame] = []

    # --- wide CSV sources -------------------------------------------------------
    csv_map = obs_map[obs_map["source_system"] == "assignment_csv"]
    lookup = dict(zip(csv_map["source_field"], csv_map["canonical_element"]))

    for name, df in bronze.items():
        measures = [c for c in df.columns if c in lookup]
        if not measures:
            continue
        id_cols = ["facility_id"] + _PROV
        if "reporting_month" in df.columns:
            id_cols.insert(1, "reporting_month")

        long = df.melt(
            id_vars=id_cols,
            value_vars=measures,
            var_name="_source_field",
            value_name="value_raw",
        )
        long["period"] = (
            long["reporting_month"] if "reporting_month" in long.columns
            else _DIMENSION_PERIOD
        )
        frames.append(long)

    # --- DHIS2 source: already long, so it only needs renaming ------------------
    d = bronze_dhis2.copy()
    d = d.rename(columns={"orgUnit": "facility_id", "dataElement": "_source_field",
                          "value": "value_raw"})
    d["period"] = [_normalise_period(p, "dhis2") for p in d["period"]]
    frames.append(d)

    s = pd.concat(frames, ignore_index=True)

    # --- canonical mapping ------------------------------------------------------
    # Join on (source_system, source_field) — the same field name can mean different
    # things in different systems, so the pair is the key, not the name alone.
    s = s.merge(
        obs_map[["source_system", "source_field", "canonical_element", "code_system", "code"]],
        left_on=["_source_system", "_source_field"],
        right_on=["source_system", "source_field"],
        how="inner",  # unmapped fields produce no observation, by design
    )

    # Resolve identity through the map, so two sources naming one facility land on one
    # org_unit. A left join, deliberately: an unresolved key must surface as a finding,
    # not vanish and not invent a facility.
    s["source_key"] = s["facility_id"]
    s = s.merge(
        org_unit_map[["source_system", "source_key", "org_unit"]],
        left_on=["_source_system", "source_key"],
        right_on=["source_system", "source_key"],
        how="left",
        suffixes=("", "_map"),
    )
    unresolved = s["org_unit"].isna()
    if unresolved.any():
        pairs = sorted(set(zip(s.loc[unresolved, "_source_system"],
                               s.loc[unresolved, "source_key"])))
        raise ValueError(
            f"{unresolved.sum()} observations have no org_unit resolution. "
            f"Add rows to mart/org_unit_map.csv for: {pairs[:10]}"
        )
    s["data_element"] = s["canonical_element"]

    # Numeric where possible; percentages stripped of their sign. Values that are
    # genuinely categorical (Yes/No/Partial) keep their text and get value_num = NaN.
    stripped = s["value_raw"].astype(str).str.rstrip("%")
    s["value_num"] = pd.to_numeric(stripped, errors="coerce")
    s["value_text"] = s["value_raw"]

    out = s[[
        "org_unit", "period", "data_element", "_batch",
        "value_num", "value_text",
        "_source_system", "source_key", "_source_file", "_source_row",
        "_ingested_at", "_row_hash", "code_system", "code",
    ]].rename(columns={
        "_batch": "batch",
        "_source_system": "source_system",
        "_source_file": "source_file",
        "_source_row": "source_row",
        "_ingested_at": "ingested_at",
        "_row_hash": "row_hash",
    })

    # Provenance columns required by trust-lineage. Populated by data-validation as
    # checks run; present from birth so "observation with no provenance" is not a
    # representable state.
    out["rules_applied"] = ""
    out["quality_flags"] = ""
    out["provisional"] = False

    return out.reset_index(drop=True)


def org_units(bronze: dict[str, pd.DataFrame]) -> pd.DataFrame:
    """The org_unit hierarchy, as one type at three levels.

    DHIS2 models country -> province -> district -> facility as `orgUnit` at different
    levels rather than as separate entity types. The sample flattens this into string
    columns on the facility row; we recover the hierarchy so a district figure and a
    facility figure are the same kind of object, addressable by one URL pattern.
    """
    f = bronze["facilities.csv"]
    facilities = pd.DataFrame({
        "org_unit": "facility:" + f["facility_id"],
        "source_key": f["facility_id"],
        "level": "facility",
        "name": f["facility_name"],   # label only — contradicts tier in 53% of rows
        "parent": "district:" + f["district"],
        "tier": f["tier_level"],
        "district": f["district"],
        "province": f["province"],
    })
    districts = (
        f[["district", "province"]].drop_duplicates()
        .assign(
            org_unit=lambda d: "district:" + d["district"],
            source_key=lambda d: d["district"],
            level="district",
            name=lambda d: d["district"],
            parent=lambda d: "province:" + d["province"],
            tier="",
        )
    )
    provinces = (
        f[["province"]].drop_duplicates()
        .assign(
            org_unit=lambda d: "province:" + d["province"],
            source_key=lambda d: d["province"],
            level="province",
            name=lambda d: d["province"],
            parent="country:Rwanda",
            tier="",
            district="",
        )
    )
    cols = ["org_unit", "source_key", "level", "name", "parent", "tier", "district", "province"]
    return pd.concat(
        [facilities[cols], districts[cols], provinces[cols]], ignore_index=True
    )
