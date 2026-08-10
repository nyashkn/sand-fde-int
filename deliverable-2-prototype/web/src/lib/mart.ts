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
  'temporal_signal_guard',
  'stratification_guard',
] as const;

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

export async function guards() {
  const temporal = await q(`SELECT data_element, observed_lag1, null_mean, null_sd, seed,
    trials, disposition, reason FROM temporal_signal_guard`);
  const strat = await q(`SELECT covariate, pooled_r, within_strata, stratified_by,
    disposition, reason FROM stratification_guard`);
  return {
    temporal: temporal.map((r) => ({
      element: String(r.data_element),
      observed: num(r.observed_lag1),
      nullMean: num(r.null_mean),
      nullSd: num(r.null_sd),
      seed: num(r.seed),
      trials: num(r.trials),
      withheld: String(r.disposition) === 'withheld',
      reason: String(r.reason),
    })),
    strat: strat.map((r) => ({
      covariate: String(r.covariate),
      pooled: num(r.pooled_r),
      within: String(r.within_strata),
      by: String(r.stratified_by),
      withheld: String(r.disposition) === 'withheld',
      reason: String(r.reason),
    })),
  };
}

export async function icdCodes(): Promise<Record<string, string>> {
  const rows = await q(`SELECT DISTINCT data_element, code FROM silver
    WHERE code_system = 'ICD-10' AND code <> ''`);
  return Object.fromEntries(rows.map((r) => [String(r.data_element), String(r.code)]));
}
