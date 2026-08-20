"""Structural checks — annotate, never gate, an analysis the data may not fully support.

Ordinary validation rejects a *row*. These annotate a *claim*: no amount of cleaning makes
a trend line's persistence provably real on a series with no measured temporal signal, or
makes a pooled correlation causal when it vanishes inside every stratum. The statistics
are unchanged from when they gated content; only the consumer contract changed. Every
check's finding now always renders, carrying the same information a hidden state used
to withdraw, stated as a caveat instead.

They are code rather than a documented rule for the reason recorded in the original
design: during this engagement the ecological fallacy was explicitly warned against and
then committed three messages later, by the person who raised it. A rule a human has to
remember is not a control.

Seeds are fixed and recorded so a caveat is reproducible.
"""

from __future__ import annotations

import numpy as np
import pandas as pd

PERMUTATION_SEED = 20260810
PERMUTATION_TRIALS = 200


def _lag1(series: np.ndarray) -> float:
    if len(series) < 3:
        return np.nan
    a, b = series[:-1], series[1:]
    if a.std() == 0 or b.std() == 0:
        return np.nan
    return float(np.corrcoef(a, b)[0, 1])


def temporal_signal_check(observations_resolved: pd.DataFrame) -> pd.DataFrame:
    """Is month-to-month movement real, or a stable per-entity baseline plus noise?

    Test: compute lag-1 autocorrelation over the pooled series, then rebuild the null by
    shuffling each facility's own months among themselves. Shuffling destroys any real
    temporal ordering while preserving each facility's level, so if the shuffled null
    matches or exceeds the observed value, every bit of apparent persistence is the
    facility's baseline and none of it is a trend.

    This is a narrow claim (real momentum beyond a facility's stable baseline), not
    "no trend data exists" — a caller reporting a raw quarter-over-quarter series has
    real numbers regardless of what this test finds; the caveat qualifies whether that
    movement is statistically distinguishable from noise, nothing more.
    """
    rows = []
    for element in ["live_births", "deliveries_total", "neonatal_deaths_early"]:
        df = observations_resolved[
            (observations_resolved["data_element"] == element)
            & (observations_resolved["period"] != "ALL")
        ][["org_unit", "period", "value_num"]].dropna()
        if df.empty:
            continue

        wide = df.pivot_table(index="org_unit", columns="period", values="value_num")
        wide = wide.sort_index(axis=1)
        observed = float(np.nanmean([_lag1(r) for r in wide.to_numpy() if not np.isnan(r).any()]))

        rng = np.random.default_rng(PERMUTATION_SEED)
        arr = wide.to_numpy()
        arr = arr[~np.isnan(arr).any(axis=1)]
        null = []
        for _ in range(PERMUTATION_TRIALS):
            shuffled = np.apply_along_axis(rng.permutation, 1, arr)
            null.append(np.mean([_lag1(r) for r in shuffled]))
        null_mean, null_sd = float(np.mean(null)), float(np.std(null))

        # Local only: decides which caveat sentence to state, never whether the row
        # renders. Everything below always renders.
        has_signal = bool(observed > null_mean + 3 * null_sd)
        rows.append({
            "data_element": element,
            "observed_lag1": round(observed, 4),
            "null_mean": round(null_mean, 4),
            "null_sd": round(null_sd, 4),
            "seed": PERMUTATION_SEED,
            "trials": PERMUTATION_TRIALS,
            "caveat": (
                f"observed lag-1 {observed:.3f} clears the within-facility permutation "
                f"null of {null_mean:.3f}\u00b1{null_sd:.3f}; treat as a real signal"
                if has_signal else
                f"observed lag-1 {observed:.3f} does not exceed a within-facility "
                f"permutation null of {null_mean:.3f}\u00b1{null_sd:.3f}; treat as "
                f"directional, not conclusive"
            ),
        })
    return pd.DataFrame(rows)


def stratification_check(
    observations_resolved: pd.DataFrame, org_units: pd.DataFrame
) -> pd.DataFrame:
    """Does a pooled association survive inside the strata of a shared driver?

    An association presented as explanatory must declare what it was stratified against.
    If the pooled sign does not hold within strata, it describes the stratum and not the
    thing being explained, and the caveat says exactly that.
    """
    facilities = org_units[org_units["level"] == "facility"][["org_unit", "tier"]]

    def facility_totals(elements: list[str]) -> pd.Series:
        d = observations_resolved[observations_resolved["data_element"].isin(elements)]
        return d.groupby("org_unit")["value_num"].sum()

    deaths = facility_totals(["neonatal_deaths_early", "neonatal_deaths_late"])
    births = facility_totals(["live_births"])
    nmr = (deaths / births * 1000).rename("nmr")

    rows = []
    for element in ["governance_staff_trained_rate", "capability_cpap_machines",
                    "ops_referral_time_hrs"]:
        cov = (
            observations_resolved[observations_resolved["data_element"] == element]
            .groupby("org_unit")["value_num"].mean().rename("covariate")
        )
        df = pd.concat([nmr, cov], axis=1).join(facilities.set_index("org_unit")).dropna()
        if len(df) < 10:
            continue

        pooled = float(df["nmr"].corr(df["covariate"]))
        within = {}
        for tier, g in df.groupby("tier"):
            if len(g) >= 10 and g["covariate"].std() > 0:
                within[tier] = round(float(g["nmr"].corr(g["covariate"])), 3)

        # Local only: decides which caveat sentence to state, never whether the row
        # renders. Survives only if every sufficiently-populated stratum keeps the
        # pooled sign and at least half the pooled magnitude.
        survives = bool(within) and all(
            np.sign(v) == np.sign(pooled) and abs(v) >= abs(pooled) / 2
            for v in within.values()
        )
        rows.append({
            "covariate": element,
            "outcome": "nmr",
            "stratified_by": "tier",
            "pooled_r": round(pooled, 3),
            "within_strata": "; ".join(f"{k} {v:+.3f}" for k, v in sorted(within.items())),
            "caveat": (
                f"pooled r={pooled:+.3f} is consistent within tier "
                f"({'; '.join(f'{k} {v:+.3f}' for k, v in sorted(within.items()))})"
                if survives else
                f"pooled r={pooled:+.3f} does not survive stratification by tier "
                f"({'; '.join(f'{k} {v:+.3f}' for k, v in sorted(within.items()))}); "
                f"the association describes tier, not the covariate"
            ),
        })
    return pd.DataFrame(rows)
