/**
 * Chart registry: figure kind determines chart type.
 *
 * The mapping is a lookup, not a per-panel decision. A kind absent from `RENDERERS`
 * throws rather than improvising, which is what stops one document encoding the same
 * thing five different ways.
 *
 * Flint compiles a semantic spec (chart type + channel/field mapping + semantic types)
 * to a Vega-Lite spec, themed via the `swiss` preset. `vega-lite` compiles that to a
 * Vega spec, and `vega` renders it to static SVG in Node at build time, headless (the
 * `renderer: 'none'` view never touches Canvas). No `linkedom`/DOM shim is needed for
 * this backend, unlike Observable Plot's browser-shaped API.
 *
 * Two things Flint's semantic layer does not expose (colors/fonts/ticks are derived,
 * not authored) are handled as the documented escape hatch: author the Flint spec,
 * then edit the compiled Vega-Lite spec for the one presentation detail Flint has no
 * knob for. `HATCH_DEF` (provisional overlay) and the district benchmark rule are both
 * this: a `fill`/`stroke` condition and an extra `rule` layer added after `assembleVegaLite`,
 * never before it.
 */
import { assembleVegaLite } from 'flint-chart';
import * as vegaLite from 'vega-lite';
import * as vega from 'vega';

/**
 * Exact palette match to `tokens.css`, not Flint's own `swiss` defaults (which are close
 * but not identical: `#1a1a1a`/`#f4f1ea`/`#e2231a`). `check-tokens.mjs` verifies this
 * object's values against the stylesheet directly, the same duplication-drift guard the
 * old literal `TOKENS` object served, now against a theme override instead of hand-copied
 * hex per mark.
 */
const THEME_SPEC = {
  extends: 'swiss',
  ink: {
    surface: { canvas: '#f6f4ef', plot: '#f6f4ef' },
    text: { primary: '#161513', secondary: '#6b6659' },
    structure: { grid: '#c9c4b4', axis: '#161513', rule: '#161513' },
    series: { single: '#c22029' },
    accent: '#c22029',
  },
} as const;

const INK = THEME_SPEC.ink.text.primary;
const PAPER = THEME_SPEC.ink.surface.canvas;
const RED = THEME_SPEC.ink.series.single;
const BLUE = '#0067a5'; // swiss preset's status.positive, used only for the benchmark rule

/** Diagonal hatch marking provisional values, so state survives greyscale. */
const HATCH_DEF = `<defs><pattern id="hatch" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="${PAPER}"/><line x1="0" y1="0" x2="0" y2="5" stroke="${RED}" stroke-width="2"/></pattern></defs>`;

export interface RankingDatum {
  label: string;
  value: number;
  provisional: boolean;
}

export interface DistributionDatum {
  label: string;
  value: number;
  provisional: boolean;
}

export interface GroupedDatum {
  group: string;
  label: string;
  value: number;
}

export interface TrendPoint {
  quarter: string;
  value: number;
  provisional: boolean;
}

export interface DistrictTrendDatum {
  quarter: string;
  district: string;
  value: number;
  provisional: boolean;
}

export type FigureKind =
  | 'ranking'
  | 'distribution-across-units'
  | 'grouped-by-category'
  | 'district-trend';

interface RenderOptions {
  width?: number;
  xLabel?: string;
  benchmark?: { value: number; label: string };
  /** `district-trend` only: the national series, drawn as a second, bolder layer. */
  nationalTrend?: TrendPoint[];
}

/** Compile a layered Vega-Lite spec to static SVG, headless. */
async function toSvg(spec: Record<string, unknown>): Promise<string> {
  const compiled = vegaLite.compile(spec as vegaLite.TopLevelSpec).spec;
  const view = new vega.View(vega.parse(compiled), { renderer: 'none' });
  const svg = await view.toSVG();
  return svg.replace(/<svg /, `<svg role="img" `).replace(/(<svg[^>]*>)/, `$1${HATCH_DEF}`);
}

function ranking(data: RankingDatum[], o: RenderOptions): Promise<string> {
  const spec = assembleVegaLite({
    data: { values: data },
    semantic_types: { label: 'Name', value: 'Count' },
    chart_spec: {
      chartType: 'Bar Chart',
      encodings: {
        x: { field: 'value' },
        y: { field: 'label', sortBy: 'x', sortOrder: 'descending' },
      },
      // Flint's own value-label layers union the y domain across all layers and drop a
      // custom aggregate sort in the process (`sortBy`/`sortOrder` above silently becomes
      // alphabetical). One hand-authored label layer below avoids the multi-layer union
      // entirely and keeps the descending-by-volume order the ranking exists to show.
      chartProperties: { showValueLabels: false },
      baseSize: { width: o.width ?? 760, height: Math.max(160, data.length * 26 + 40) },
    },
    field_display_names: o.xLabel ? { value: o.xLabel } : undefined,
    theme_spec: THEME_SPEC,
  }) as Record<string, unknown> & {
    mark: Record<string, unknown>;
    encoding: Record<string, unknown>;
    config: Record<string, unknown>;
    background: string;
    height: unknown;
    padding: unknown;
    data: unknown;
  };

  const bar = spec;
  const baseColor = bar.mark.color as string;
  const barLayer = {
    mark: { ...bar.mark, color: undefined },
    encoding: {
      ...bar.encoding,
      fill: { condition: { test: 'datum.provisional', value: 'url(#hatch)' }, value: baseColor },
    },
  };
  delete barLayer.mark.color;

  const labelLayer = {
    mark: { type: 'text', align: 'left', baseline: 'middle', dx: 6, color: THEME_SPEC.ink.text.secondary,
            font: spec.config.font, fontSize: 10.5 },
    encoding: {
      x: bar.encoding.x,
      y: bar.encoding.y,
      text: { field: 'value', type: 'quantitative', format: ',d' },
    },
  };

  return toSvg({
    config: spec.config, background: spec.background, height: spec.height,
    padding: spec.padding, data: spec.data,
    layer: [barLayer, labelLayer],
  });
}

function distribution(data: DistributionDatum[], o: RenderOptions): Promise<string> {
  const sorted = [...data].sort((a, b) => a.value - b.value);
  const spec = assembleVegaLite({
    data: { values: sorted },
    semantic_types: { label: 'Region', value: 'Amount' },
    chart_spec: {
      chartType: 'Scatter Plot',
      encodings: {
        x: { field: 'value' },
        y: { field: 'label', sortBy: 'x', sortOrder: 'ascending' },
      },
      baseSize: { width: o.width ?? 760, height: Math.max(200, sorted.length * 19 + 48) },
    },
    field_display_names: o.xLabel ? { value: o.xLabel } : undefined,
    theme_spec: THEME_SPEC,
  }) as Record<string, unknown> & {
    mark: Record<string, unknown>;
    encoding: Record<string, unknown>;
    config: Record<string, unknown>;
    background: string;
    height: unknown;
    padding: unknown;
    data: unknown;
  };

  const baseColor = spec.mark.color as string;
  // A benchmark below the data's own minimum (here: national ~19 against a district
  // range starting near 28) sits outside Vega-Lite's auto-computed domain otherwise, and
  // the rule renders clamped to the plot's left edge, on top of the y-axis labels rather
  // than inside the plot. Extending the x domain to include the benchmark (with a little
  // padding either side) is what actually puts the rule and its "national ~N" label in
  // open space.
  const xEncoding = spec.encoding.x as Record<string, unknown>;
  if (o.benchmark) {
    const values = sorted.map((d) => d.value);
    const lo = Math.min(...values, o.benchmark.value);
    const hi = Math.max(...values, o.benchmark.value);
    const pad = (hi - lo) * 0.06;
    xEncoding.scale = { domain: [Math.max(0, lo - pad), hi + pad] };
  }
  // Hollow vs. filled is the whole provisional encoding: fill matches the canvas so the
  // marker reads as an open circle, stroke stays the series colour so it stays legible.
  const pointLayer = {
    mark: { ...spec.mark, stroke: baseColor, strokeWidth: 1.5 },
    encoding: {
      ...spec.encoding,
      fill: { condition: { test: 'datum.provisional', value: spec.background }, value: baseColor },
    },
  };
  delete pointLayer.mark.color;

  const layers = [pointLayer];
  if (o.benchmark) {
    layers.push({
      data: { values: [{ v: o.benchmark.value, label: o.benchmark.label }] },
      mark: { type: 'rule', color: BLUE, strokeWidth: 1.5, strokeDash: [4, 3] },
      encoding: { x: { field: 'v', type: 'quantitative' } },
    } as typeof pointLayer);
    layers.push({
      data: { values: [{ v: o.benchmark.value, label: o.benchmark.label }] },
      mark: { type: 'text', align: 'left', baseline: 'bottom', dx: 4, dy: -4,
              color: BLUE, font: spec.config.font, fontSize: 10 },
      // y: {value: 0} pins the label to the top edge of the plot area, independent of
      // the category axis, matching the original Observable Plot `frameAnchor: 'top'`
      // behaviour. Without it the label has no y encoding and Vega-Lite centres it,
      // which collides with whichever district happens to sit in the middle of the list.
      encoding: { x: { field: 'v', type: 'quantitative' }, y: { value: 0 },
                  text: { field: 'label', type: 'nominal' } },
    } as typeof pointLayer);
  }

  return toSvg({
    config: spec.config, background: spec.background, height: spec.height,
    padding: spec.padding, data: spec.data,
    layer: layers,
  });
}

/**
 * Grouped bar: one band per `label` (here, facility tier), one bar per `group` (here, a
 * capability metric) inside the band. Built for section 3's tier comparison, where the finding
 * is that adjacent tiers read as near-identical on every field: a grouped bar makes that
 * a shape (flat bars sitting beside flat bars), which four separate single-series bars
 * would not.
 */
function groupedByCategory(data: GroupedDatum[], o: RenderOptions): Promise<string> {
  const spec = assembleVegaLite({
    data: { values: data },
    semantic_types: { label: 'Category', value: 'Amount', group: 'Category' },
    chart_spec: {
      chartType: 'Grouped Bar Chart',
      encodings: { x: { field: 'label' }, y: { field: 'value' }, group: { field: 'group' } },
      baseSize: { width: o.width ?? 760, height: 320 },
    },
    field_display_names: o.xLabel ? { value: o.xLabel } : undefined,
    theme_spec: THEME_SPEC,
  }) as Record<string, unknown>;

  return toSvg(spec);
}

/**
 * District-level trend: every district's own line (`detail`, not `color`: 30 hues in a
 * one-accent palette reads as noise, not information), overlaid with the national series
 * as a second, bolder, hand-authored layer, the same escape hatch the district benchmark
 * rule in `distribution()` uses. Provisional (batch-conflict) district-quarter points are
 * hatched, matching section 4's convention on the same data; the national line's own hatched
 * points mark the two partial quarters (a missing month), the convention already in use
 * in section 5's superseded bar grid.
 */
function districtTrend(data: DistrictTrendDatum[], o: RenderOptions): Promise<string> {
  const spec = assembleVegaLite({
    data: { values: data },
    semantic_types: { quarter: 'Quarter', value: 'Amount', district: 'Category' },
    chart_spec: {
      chartType: 'Line Chart',
      encodings: { x: { field: 'quarter' }, y: { field: 'value' }, detail: { field: 'district' } },
      baseSize: { width: o.width ?? 760, height: 340 },
    },
    field_display_names: o.xLabel ? { value: o.xLabel } : undefined,
    theme_spec: THEME_SPEC,
  }) as Record<string, unknown> & {
    mark: Record<string, unknown>;
    encoding: Record<string, unknown>;
    config: Record<string, unknown>;
    background: string;
    height: unknown;
    padding: unknown;
    data: unknown;
  };

  const secondary = THEME_SPEC.ink.text.secondary;
  const districtLayer = {
    mark: { type: 'line', color: secondary, strokeWidth: 1, opacity: 0.55, interpolate: 'monotone' },
    encoding: {
      ...spec.encoding,
      strokeDash: { condition: { test: 'datum.provisional', value: [2, 2] }, value: [0, 0] },
    },
  };

  const layers = [districtLayer] as Array<Record<string, unknown>>;
  const national = o.nationalTrend ?? [];
  if (national.length > 0) {
    const xEnc = (spec.encoding as Record<string, unknown>).x;
    const yEnc = (spec.encoding as Record<string, unknown>).y;
    layers.push({
      data: { values: national },
      mark: { type: 'line', color: RED, strokeWidth: 2.5 },
      encoding: { x: xEnc, y: yEnc },
    });
    layers.push({
      data: { values: national },
      mark: { type: 'point', size: 64, filled: true, stroke: RED, strokeWidth: 1.5 },
      encoding: {
        x: xEnc,
        y: yEnc,
        fill: { condition: { test: 'datum.provisional', value: 'url(#hatch)' }, value: RED },
      },
    });
  }

  // Explicit, hardcoded width AND height, not `spec.width`/`spec.height`: Flint's layout
  // phase for a `Line Chart` with a `detail` channel derives view size from a
  // cross-section density formula tuned for a handful of continuous series, not 30
  // detail-split lines against 4 ordinal ticks, and computed a 178x458 view here instead
  // of the requested 760x340 (confirmed by inspecting the built SVG's own `width`/
  // `height` attributes). `ranking`/`distribution` above never hit this because Bar
  // Chart and Scatter Plot size differently; this is the one renderer where trusting
  // Flint's own dimensions produced the wrong chart.
  return toSvg({
    config: spec.config, background: spec.background,
    width: o.width ?? 760, height: 340,
    padding: spec.padding, data: spec.data,
    layer: layers,
  });
}

/**
 * Four kinds, deliberately.
 *
 * A `composition` renderer existed and was removed: five causes as a stacked bar needed
 * five hues in a palette with one accent, collided its own percentage labels, and sat
 * directly above a table carrying the same five numbers plus their ICD-10 codes. It
 * showed proportion, which a Share column shows exactly and a reader can subtract.
 *
 * A chart earns a place here by doing something a table cannot: `ranking` compares
 * magnitude across ten bars at a glance, `distribution-across-units` shows spread and
 * distance from a benchmark across thirty, `grouped-by-category` compares several
 * measures across a handful of categories at once, `district-trend` shows thirty
 * simultaneous series against one benchmark line. Reinstating a kind means clearing that
 * bar.
 */
const RENDERERS = {
  ranking,
  'distribution-across-units': distribution,
  'grouped-by-category': groupedByCategory,
  'district-trend': districtTrend,
} as const;

export async function chart(kind: FigureKind, data: unknown[], options: RenderOptions = {}): Promise<string> {
  const render = RENDERERS[kind as keyof typeof RENDERERS];
  if (!render) {
    throw new Error(
      `No chart type registered for figure kind "${kind}". ` +
        `Register it in src/lib/charts.ts rather than improvising one at the call site.`,
    );
  }
  // Each renderer validates its own datum shape through its typed signature; the cast is
  // the one place the registry's heterogeneous table meets a concrete renderer.
  const typed = data as RankingDatum[] & DistributionDatum[] & GroupedDatum[] & DistrictTrendDatum[];
  return render(typed, options);
}
