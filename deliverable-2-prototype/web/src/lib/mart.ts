/**
 * Read the gold marts at build time.
 *
 * DuckDB runs in Node here, not in the browser: the bulletin is static output, so the
 * data is resolved once at build rather than fetched by a client that may have no
 * network. The explore surface will read the same Parquet files through DuckDB-WASM.
 * Same files, same SQL, two runtimes.
 */
import { DuckDBInstance, type DuckDBConnection } from '@duckdb/node-api';
import { resolve } from 'node:path';

// Resolved against the project root rather than import.meta.url: Astro bundles this
// module, so its own URL at build time is the bundle's location, not src/lib.
const MART = resolve(process.cwd(), '../pipeline/mart');

const MART_TABLES = [
  'silver',
  'org_units',
  'facility_quarter',
  'district_quarter',
  'nmr_district_quarter',
  'nmr_facility_quarter',
  'completeness_summary',
  'temporal_signal_check',
  'stratification_check',
  'observations_resolved',
  'cause_capability_links',
  'facility_capability',
  'capability_summary',
  'known_contradictions',
] as const;

/**
 * The four editions this mart has data for. Shared by the publish-facing `index.astro`
 * (reads `QUARTER` from the environment, one build per edition) and the dev-only
 * `[quarter].astro` route (one `astro dev` process, all four browsable live), so the two
 * routing strategies can never enumerate a different quarter list.
 */
export const ALL_QUARTERS = ['2024-Q1', '2024-Q2', '2024-Q3', '2024-Q4'] as const;

/**
 * Cache the in-flight promise, not the resolved connection.
 *
 * The page loads seven queries through Promise.all, so caching only the settled value
 * lets all seven enter setup before any assigns it, and the second one to reach
 * CREATE VIEW fails with "view already exists".
 */
let ready: Promise<DuckDBConnection> | null = null;

function db(): Promise<DuckDBConnection> {
  ready ??= (async () => {
    const instance = await DuckDBInstance.create(':memory:');
    const c = await instance.connect();
    for (const t of MART_TABLES) {
      await c.run(`CREATE VIEW ${t} AS SELECT * FROM read_parquet('${MART}/${t}.parquet')`);
    }
    return c;
  })();
  return ready;
}

export async function q<T = Record<string, unknown>>(sql: string): Promise<T[]> {
  const c = await db();
  const reader = await c.runAndReadAll(sql);
  return reader.getRowObjects() as T[];
}

/**
 * Coerce a DuckDB scalar to a JS number.
 *
 * Non-obvious and needed at every call site: BIGINT arrives as `bigint`, DECIMAL as an
 * object carrying `toDouble`, and both silently become `NaN` under plain `Number()`.
 */
export function num(v: unknown): number {
  if (v === null || v === undefined) return NaN;
  if (typeof v === 'bigint') return Number(v);
  if (typeof v === 'number') return v;
  if (typeof v === 'object' && 'toDouble' in v && typeof v.toDouble === 'function') {
    return Number(v.toDouble());
  }
  return Number(v);
}

export type QuarterState = 'complete' | 'contested' | 'absent';

export interface Completeness {
  period: string;
  facilities_received: number;
  facilities_expected: number;
  batches: number;
  state: QuarterState;
}

export async function completeness(quarter: string): Promise<Completeness[]> {
  const rows = await q(`SELECT period, facilities_received, facilities_expected, batches, state
    FROM completeness_summary WHERE quarter = '${quarter}' ORDER BY period`);
  return rows.map((r) => ({
    period: String(r.period),
    facilities_received: num(r.facilities_received),
    facilities_expected: num(r.facilities_expected),
    batches: num(r.batches),
    state: String(r.state) as QuarterState,
  }));
}

export async function headlineNmr(quarter: string) {
  const [r] = await q(`SELECT sum(numerator) AS deaths, sum(denominator) AS births,
    sum(CASE WHEN provisional THEN 1 ELSE 0 END) AS provisional_districts,
    count(*) AS districts
    FROM nmr_district_quarter WHERE quarter = '${quarter}'`);
  const deaths = num(r.deaths);
  const births = num(r.births);
  return {
    rate: (deaths / births) * 1000,
    deaths,
    births,
    provisionalDistricts: num(r.provisional_districts),
    districts: num(r.districts),
  };
}

export async function districtNmr(quarter: string) {
  const rows = await q(`SELECT district, value, numerator, denominator, provisional
    FROM nmr_district_quarter WHERE quarter = '${quarter}' ORDER BY value DESC`);
  return rows.map((r) => ({
    district: String(r.district),
    value: num(r.value),
    numerator: num(r.numerator),
    denominator: num(r.denominator),
    provisional: Boolean(r.provisional),
  }));
}

export async function topFacilities(quarter: string, limit = 10) {
  const rows = await q(`SELECT name, district, tier, value, provisional
    FROM facility_quarter
    WHERE quarter = '${quarter}' AND data_element = 'deliveries_total'
    ORDER BY value DESC LIMIT ${limit}`);
  return rows.map((r) => ({
    name: String(r.name),
    district: String(r.district),
    tier: String(r.tier),
    value: num(r.value),
    provisional: Boolean(r.provisional),
  }));
}

export async function causeBreakdown(quarter: string) {
  const rows = await q(`SELECT data_element, sum(value) AS value,
      sum(provisional_inputs) AS prov
    FROM district_quarter
    WHERE quarter = '${quarter}' AND data_element LIKE 'neonatal_deaths_%'
      AND data_element NOT IN ('neonatal_deaths_early','neonatal_deaths_late')
    GROUP BY 1 ORDER BY 2 DESC`);
  return rows.map((r) => ({
    cause: String(r.data_element).replace('neonatal_deaths_', ''),
    value: num(r.value),
    provisional: num(r.prov) > 0,
  }));
}

export interface StillbirthFigure {
  stillbirths: number;
  deliveries: number;
  rate: number;
  provisional: boolean;
}

/**
 * Stillbirths, own figure, own denominator.
 *
 * `stillbirths` is resolved into the mart (ICD-10 P95, identity-verified against
 * `live_births = total_deliveries - stillbirths` in 1,404 of 1,404 source rows) but is
 * NOT a neonatal death: a stillbirth never had a live birth, so it cannot enter a
 * live-birth-denominated rate, and `causeBreakdown` above is correct to exclude it (its
 * canonical element is `stillbirths`, not `neonatal_deaths_*`). Reads `district_quarter`
 * directly rather than `neonatal_deaths_%`, the same resolved, batch-deduplicated table
 * every other figure on this page reads, so this figure is provisional on the same terms.
 */
export async function stillbirthRate(quarter: string): Promise<StillbirthFigure> {
  const [r] = await q(`SELECT
      sum(CASE WHEN data_element = 'stillbirths' THEN value ELSE 0 END) AS stillbirths,
      sum(CASE WHEN data_element = 'deliveries_total' THEN value ELSE 0 END) AS deliveries,
      sum(CASE WHEN data_element = 'stillbirths' THEN provisional_inputs ELSE 0 END) AS prov
    FROM district_quarter WHERE quarter = '${quarter}'`);
  const stillbirths = num(r.stillbirths);
  const deliveries = num(r.deliveries);
  return {
    stillbirths,
    deliveries,
    rate: (stillbirths / deliveries) * 1000,
    provisional: num(r.prov) > 0,
  };
}

export interface DistrictTrendPoint {
  district: string;
  quarter: string;
  value: number;
  provisional: boolean;
}

/** Every district, every quarter: the mart already carries the full grid, section 5 only ever read one national row off it. */
export async function districtTrend(): Promise<DistrictTrendPoint[]> {
  const rows = await q(
    `SELECT district, quarter, value, provisional FROM nmr_district_quarter ORDER BY district, quarter`,
  );
  return rows.map((r) => ({
    district: String(r.district),
    quarter: String(r.quarter),
    value: num(r.value),
    provisional: Boolean(r.provisional),
  }));
}

export async function checks() {
  const temporal = await q(`SELECT data_element, observed_lag1, null_mean, null_sd, seed,
    trials, caveat FROM temporal_signal_check`);
  const strat = await q(`SELECT covariate, pooled_r, within_strata, stratified_by,
    caveat FROM stratification_check`);
  const temporalRows = temporal.map((r) => ({
    element: String(r.data_element),
    observed: num(r.observed_lag1),
    nullMean: num(r.null_mean),
    nullSd: num(r.null_sd),
    seed: num(r.seed),
    trials: num(r.trials),
    caveat: String(r.caveat),
  }));
  const stratRows = strat.map((r) => ({
    covariate: String(r.covariate),
    pooled: num(r.pooled_r),
    within: String(r.within_strata),
    by: String(r.stratified_by),
    caveat: String(r.caveat),
  }));
  return { temporal: temporalRows, strat: stratRows };
}

export interface CauseCapabilityLink {
  causeElement: string;
  capabilityElement: string;
  note: string;
}

export async function causeCapabilityLinks(): Promise<CauseCapabilityLink[]> {
  const rows = await q(`SELECT cause_element, capability_element, relationship_note
    FROM cause_capability_links`);
  return rows.map((r) => ({
    causeElement: String(r.cause_element),
    capabilityElement: String(r.capability_element),
    note: String(r.relationship_note),
  }));
}

export interface CapabilityMetric {
  metric: string;
  category: string | null;
  kind: 'numeric' | 'categorical';
  nFacilities: number;
  nWith: number | null;
  pctWith: number | null;
  median: number | null;
  min: number | null;
  max: number | null;
  mean: number | null;
}

/**
 * Not quarter-scoped, unlike `headlineNmr`: capability data is stamped `period="ALL"`
 * (one snapshot per facility, not one per month), so there is no quarter to parameterise.
 */
export async function capabilitySummary(): Promise<CapabilityMetric[]> {
  const rows = await q(`SELECT metric, category, kind, n_facilities, n_with, pct_with,
    median, min, max, mean FROM capability_summary`);
  return rows.map((r) => ({
    metric: String(r.metric),
    category: r.category === null ? null : String(r.category),
    kind: String(r.kind) as 'numeric' | 'categorical',
    nFacilities: num(r.n_facilities),
    nWith: r.n_with === null ? null : num(r.n_with),
    pctWith: r.pct_with === null ? null : num(r.pct_with),
    median: r.median === null ? null : num(r.median),
    min: r.min === null ? null : num(r.min),
    max: r.max === null ? null : num(r.max),
    mean: r.mean === null ? null : num(r.mean),
  }));
}

export interface Contradiction {
  finding: string;
  kind: string;
  elements: string;
  statement: string;
}

export async function contradictions(): Promise<Contradiction[]> {
  const rows = await q(`SELECT finding, kind, elements, statement FROM known_contradictions`);
  return rows.map((r) => ({
    finding: String(r.finding),
    kind: String(r.kind),
    elements: String(r.elements),
    statement: String(r.statement),
  }));
}

const CROSSWALK = resolve(process.cwd(), '../pipeline/mart/crosswalk.csv');

/**
 * Canonical elements the crosswalk maps (role <> 'unmapped') that reach a gold table but
 * that no query in this file or `email.astro` ever looks up. Not derivable from the
 * crosswalk itself, which has no "rendered" column: `governance_protocol_updated`
 * (`protocol_last_updated`) reaches `capability_summary` like every other observation-role
 * column, but `newborn_protocol_exists` (rendered in section 3's gap bars as "No or outdated
 * protocol") is a pure function of the same staleness this column measures, so the raw
 * date stops at gold. Named explicitly, the same way `EQUIPMENT_INDEX_FIELDS` above names
 * its columns: a fact about this template's own field usage, not one crosswalk.csv encodes.
 */
const CARRIED_UNUSED_ELEMENTS = ['governance_protocol_updated'] as const;

export interface CrosswalkCoverage {
  totalSourceColumns: number;
  reachingFigure: number;
  excluded: number;
  carriedUnused: number;
}

/**
 * Column-coverage counts for the aggregate line near section 8, read live off `crosswalk.csv`
 * rather than hand-counted: a hand-typed 66/9 already drifted once on this page (the
 * lineage table's own row counts, before `rulesApplied` moved off a literal), and
 * `check-agreement.mjs`'s culture is that a stated figure must match a computed one.
 * `dhis2`'s 5 rows are a second source proving the same canonical elements `assignment_csv`
 * already declares, not additional distinct source columns, so only `assignment_csv` rows
 * count toward the 66.
 */
export async function crosswalkCoverage(): Promise<CrosswalkCoverage> {
  const [r] = await q(`
    SELECT
      count(*) FILTER (WHERE source_system = 'assignment_csv') AS total,
      count(*) FILTER (WHERE source_system = 'assignment_csv' AND role = 'unmapped') AS excluded
    FROM read_csv_auto('${CROSSWALK}')
  `);
  const totalSourceColumns = num(r.total);
  const excluded = num(r.excluded);
  const carriedUnused = CARRIED_UNUSED_ELEMENTS.length;
  return {
    totalSourceColumns,
    excluded,
    carriedUnused,
    reachingFigure: totalSourceColumns - excluded - carriedUnused,
  };
}

/**
 * Capability metrics never rendered past national rollup, broken out by tier.
 *
 * `capabilitySummary` above is deliberately national-only (period = ALL, one snapshot).
 * This reads the same `facility_capability` pivot the mart already carries and groups by
 * tier instead, because tier is the covariate that actually explains outcome variation in
 * this dataset (section 6): a national median hides that District and Health Center read as
 * near-identical on every field below, despite very different mortality.
 */
const TIER_CAPABILITY_METRICS = [
  'capability_nicu_beds', 'capability_incubators_functional', 'capability_incubators_total',
  'capability_radiant_warmers', 'capability_phototherapy_units', 'capability_cpap_machines',
  'capability_resuscitation_tables', 'ops_oxygen_cylinders', 'ops_oxygen_concentrators',
  'ops_stockout_days', 'governance_death_audit_rate', 'governance_supervision_visits',
  'governance_thermal_compliance', 'governance_ipc_score', 'staff_nurses_total',
  'staff_nurses_neonatal', 'staff_midwives', 'staff_obstetricians', 'staff_pediatricians',
  'staff_anesthetists',
] as const;
export type TierCapabilityMetric = (typeof TIER_CAPABILITY_METRICS)[number];

export interface TierCapabilityRow {
  tier: string;
  n: number;
  metric: TierCapabilityMetric;
  median: number;
}

export async function capabilityByTier(): Promise<TierCapabilityRow[]> {
  const cols = TIER_CAPABILITY_METRICS.map((m) => `median(${m}) AS ${m}`).join(', ');
  const rows = await q(
    `SELECT tier, count(*) AS n, ${cols} FROM facility_capability GROUP BY tier ORDER BY tier`,
  );
  const out: TierCapabilityRow[] = [];
  for (const r of rows) {
    for (const metric of TIER_CAPABILITY_METRICS) {
      out.push({ tier: String(r.tier), n: num(r.n), metric, median: num(r[metric]) });
    }
  }
  return out;
}

export interface StratRow {
  covariate: string;
  pooled: number;
  within: string;
  by: string;
  caveat: string;
}

/**
 * Same stratified-correlation logic `pipeline/dataflow/checks.py::stratification_check`
 * applies to its three covariates (sign and half-magnitude must hold in every
 * sufficiently-populated stratum), reproduced here for two covariates that file never
 * tested. Not a duplicate of that module: this reads already-resolved mart tables through
 * DuckDB's own `corr()`, computed at build time in this layer because the pipeline itself
 * is out of scope for this change. A stratum needs at least 10 facilities to report,
 * matching the Python check's own floor; `Referral` (n=2) is pooled-only for that reason.
 */
function survivesStratification(pooled: number, within: number[]): boolean {
  return (
    within.length > 0 &&
    within.every((v) => Math.sign(v) === Math.sign(pooled) && Math.abs(v) >= Math.abs(pooled) / 2)
  );
}

function stratRow(covariate: string, pooled: number, within: [string, number][]): StratRow {
  const fmt = (v: number) => `${v >= 0 ? '+' : ''}${v.toFixed(3)}`;
  const withinStr = within.map(([tier, v]) => `${tier} ${fmt(v)}`).join('; ');
  const caveat = survivesStratification(pooled, within.map(([, v]) => v))
    ? `pooled r=${fmt(pooled)} is consistent within tier (${withinStr})`
    : `pooled r=${fmt(pooled)} does not survive stratification by tier (${withinStr}); the association describes tier, not the covariate`;
  return { covariate, pooled, within: withinStr, by: 'tier', caveat };
}

async function corrByTier(covariateExpr: string): Promise<{ tier: string | null; r: number; n: number }[]> {
  const rows = await q(`
    WITH nmr AS (
      SELECT org_unit, sum(numerator) * 1000.0 / sum(denominator) AS nmr
      FROM nmr_facility_quarter GROUP BY org_unit
    )
    SELECT fc.tier AS tier, corr(${covariateExpr}, nmr.nmr) AS r, count(*) AS n
    FROM facility_capability fc JOIN nmr ON fc.org_unit = nmr.org_unit
    GROUP BY GROUPING SETS ((fc.tier), ())
  `);
  return rows.map((r) => ({ tier: r.tier === null ? null : String(r.tier), r: num(r.r), n: num(r.n) }));
}

function toStratRow(label: string, rows: { tier: string | null; r: number; n: number }[]): StratRow {
  const pooled = rows.find((r) => r.tier === null)!.r;
  const within = rows
    .filter((r) => r.tier !== null && r.n >= 10)
    .map((r) => [r.tier as string, r.r] as [string, number])
    .sort((a, b) => a[0].localeCompare(b[0]));
  return stratRow(label, pooled, within);
}

/** The 8 equipment fields z-scored and averaged: one composite, equal-weighted, no field dominating by scale. */
const EQUIPMENT_INDEX_FIELDS = [
  'capability_nicu_beds', 'capability_incubators_functional', 'capability_radiant_warmers',
  'capability_phototherapy_units', 'capability_cpap_machines', 'capability_resuscitation_tables',
  'ops_oxygen_cylinders', 'ops_oxygen_concentrators',
] as const;

export async function equipmentTierConfound(): Promise<StratRow> {
  const zTerms = EQUIPMENT_INDEX_FIELDS.map(
    (f) => `((${f} - avg(${f}) OVER()) / stddev_samp(${f}) OVER())`,
  ).join(' + ');
  const rows = await q(`
    WITH idx AS (
      SELECT org_unit, tier, (${zTerms}) / ${EQUIPMENT_INDEX_FIELDS.length}.0 AS equip_index
      FROM facility_capability
    ), nmr AS (
      SELECT org_unit, sum(numerator) * 1000.0 / sum(denominator) AS nmr
      FROM nmr_facility_quarter GROUP BY org_unit
    )
    SELECT idx.tier AS tier, corr(idx.equip_index, nmr.nmr) AS r, count(*) AS n
    FROM idx JOIN nmr ON idx.org_unit = nmr.org_unit
    GROUP BY GROUPING SETS ((idx.tier), ())
  `);
  const parsed = rows.map((r) => ({ tier: r.tier === null ? null : String(r.tier), r: num(r.r), n: num(r.n) }));
  return toStratRow('capability_equipment_index', parsed);
}

/**
 * Only `ops_referral_feedback_rate`. `ops_referral_time_hrs` is already one of the three
 * covariates `checks.py::stratification_check` tests (`chk.strat`); recomputing it here
 * would be the same finding rendered twice under two different code paths.
 */
export async function referralFeedbackTierConfound(): Promise<StratRow> {
  const feedback = await corrByTier('fc.ops_referral_feedback_rate');
  return toStratRow('ops_referral_feedback_rate', feedback);
}

/** Facilities with zero neonatologists on staff, live-counted: the mean alone is a rounding artefact, section 7. */
export async function neonatologistCoverage(): Promise<{ zero: number; total: number }> {
  const [r] = await q(
    `SELECT sum(CASE WHEN staff_neonatologists = 0 THEN 1 ELSE 0 END) AS zero, count(*) AS total
     FROM facility_capability WHERE staff_neonatologists IS NOT NULL`,
  );
  return { zero: num(r.zero), total: num(r.total) };
}

export interface TierNmr {
  tier: string;
  meanNmr: number;
  n: number;
}

/** Mean facility NMR by tier, pooled across all four quarters: the number section 6 exists to explain. */
export async function tierNmr(): Promise<TierNmr[]> {
  const rows = await q(`
    WITH fac AS (
      SELECT org_unit, any_value(tier) AS tier,
        sum(numerator) * 1000.0 / sum(denominator) AS nmr
      FROM nmr_facility_quarter GROUP BY org_unit
    )
    SELECT tier, avg(nmr) AS mean_nmr, count(*) AS n FROM fac GROUP BY tier ORDER BY mean_nmr DESC
  `);
  return rows.map((r) => ({ tier: String(r.tier), meanNmr: num(r.mean_nmr), n: num(r.n) }));
}

export async function icdCodes(): Promise<Record<string, string>> {
  const rows = await q(`SELECT DISTINCT data_element, code FROM silver
    WHERE code_system = 'ICD-10' AND code <> ''`);
  return Object.fromEntries(rows.map((r) => [String(r.data_element), String(r.code)]));
}

/**
 * The batch-conflict rules actually applied in a quarter, read from the mart.
 *
 * Not a constant in the template. Writing the rule name by hand into the lineage table
 * already produced `DUP-01`, a rule the pipeline has never had, in a section whose entire
 * job is letting a reader check the provenance of a figure. A lineage record that names a
 * fictional rule is worse than no lineage record.
 */
export async function rulesApplied(): Promise<string[]> {
  const rows = await q(
    `SELECT DISTINCT rules_applied FROM observations_resolved WHERE rules_applied <> ''`,
  );
  return rows.map((r) => String(r.rules_applied)).sort();
}
