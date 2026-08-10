/**
 * Chart registry: figure kind determines chart type.
 *
 * The mapping is a lookup, not a per-panel decision. A kind absent from `RENDERERS`
 * throws rather than improvising, which is what stops one document encoding the same
 * thing five different ways.
 *
 * Observable Plot renders to SVG here in Node at build time. Mosaic's vgplot is built
 * on Observable Plot, so the interactive surface will share this grammar rather than
 * needing a second, drifting registry.
 */
import * as Plot from '@observablehq/plot';
import { parseHTML } from 'linkedom';

const TOKENS = {
  ink: '#1a1917',
  muted: '#5a5248',
  rule: '#ded9cc',
  clay: '#c36a47',
  clayD: '#a9532f',
  olive: '#6f855a',
  oat: '#efebe0',
  paper: '#ffffff',
  // No quoted family names: Plot writes this into an SVG style attribute, and the
  // HTML-escaped quotes it emits there are not parseable CSS for the email inliner.
  mono: 'ui-monospace, Menlo, Monaco, monospace',
} as const;

/** Diagonal hatch marking provisional values, so state survives greyscale. */
const HATCH_DEF = `<defs><pattern id="hatch" width="5" height="5" patternTransform="rotate(45)" patternUnits="userSpaceOnUse"><rect width="5" height="5" fill="${TOKENS.oat}"/><line x1="0" y1="0" x2="0" y2="5" stroke="${TOKENS.clay}" stroke-width="2"/></pattern></defs>`;

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

export interface CompositionDatum {
  category: string;
  value: number;
}

export type FigureKind = 'ranking' | 'distribution-across-units' | 'composition';

interface RenderOptions {
  width?: number;
  xLabel?: string;
  benchmark?: { value: number; label: string };
}

/**
 * Plot needs a DOM. linkedom supplies one in Node without a browser, which is what keeps
 * this a build-time step rather than a headless-browser dependency.
 */
function plotToSvg(mark: (document: Document) => SVGSVGElement | HTMLElement): string {
  const { document } = parseHTML('<!DOCTYPE html><html><body></body></html>');
  const node = mark(document as unknown as Document);
  const svg = 'outerHTML' in node ? node.outerHTML : String(node);
  return svg.replace(/<svg /, `<svg role="img" `).replace(/(<svg[^>]*>)/, `$1${HATCH_DEF}`);
}

const baseStyle = {
  fontFamily: TOKENS.mono,
  fontSize: 11,
  background: 'transparent',
  color: TOKENS.ink,
} as const;

function ranking(data: RankingDatum[], o: RenderOptions): string {
  return plotToSvg((document) =>
    Plot.plot({
      document,
      width: o.width ?? 760,
      height: Math.max(160, data.length * 26 + 40),
      marginLeft: 210,
      marginRight: 56,
      style: baseStyle,
      x: { label: o.xLabel ?? null, grid: true, tickFormat: 's', nice: true },
      y: { label: null, domain: data.map((d) => d.label) },
      marks: [
        Plot.barX(data, {
          x: 'value',
          y: 'label',
          fill: (d: RankingDatum) => (d.provisional ? 'url(#hatch)' : TOKENS.clay),
          stroke: (d: RankingDatum) => (d.provisional ? TOKENS.clay : 'none'),
          strokeDasharray: '2,2',
          insetTop: 3,
          insetBottom: 3,
        }),
        Plot.text(data, {
          x: 'value',
          y: 'label',
          text: (d: RankingDatum) => d.value.toLocaleString(),
          textAnchor: 'start',
          dx: 6,
          fill: TOKENS.muted,
          fontSize: 10.5,
        }),
        Plot.ruleX([0], { stroke: TOKENS.ink }),
      ],
    }),
  );
}

function distribution(data: DistributionDatum[], o: RenderOptions): string {
  const sorted = [...data].sort((a, b) => b.value - a.value);
  return plotToSvg((document) =>
    Plot.plot({
      document,
      width: o.width ?? 760,
      height: Math.max(200, sorted.length * 19 + 48),
      marginLeft: 128,
      marginRight: 40,
      style: baseStyle,
      x: { label: o.xLabel ?? null, grid: true, nice: true },
      y: { label: null, domain: sorted.map((d) => d.label) },
      marks: [
        Plot.ruleY(sorted, { y: 'label', x1: 0, x2: 'value', stroke: TOKENS.rule }),
        ...(o.benchmark
          ? [
              Plot.ruleX([o.benchmark.value], { stroke: TOKENS.olive, strokeWidth: 1.5 }),
              Plot.text([o.benchmark], {
                x: 'value',
                frameAnchor: 'top',
                text: 'label',
                dy: -6,
                dx: 4,
                textAnchor: 'start',
                fill: TOKENS.olive,
                fontSize: 10,
              }),
            ]
          : []),
        Plot.dot(sorted, {
          x: 'value',
          y: 'label',
          r: 4,
          fill: (d: DistributionDatum) => (d.provisional ? TOKENS.paper : TOKENS.clay),
          stroke: TOKENS.clay,
          strokeWidth: (d: DistributionDatum) => (d.provisional ? 1.5 : 0),
          strokeDasharray: (d: DistributionDatum) => (d.provisional ? '2,1.5' : 'none'),
        }),
      ],
    }),
  );
}

function composition(data: CompositionDatum[], o: RenderOptions): string {
  const palette = ['#c36a47', '#3e857c', '#8a6b9e', '#b58a34', '#5e7fa6'];
  const total = data.reduce((s, d) => s + d.value, 0);
  return plotToSvg((document) =>
    Plot.plot({
      document,
      width: o.width ?? 760,
      height: 132,
      marginLeft: 8,
      marginRight: 8,
      marginTop: 28,
      style: baseStyle,
      x: { label: null, percent: false, axis: null },
      color: { domain: data.map((d) => d.category), range: palette, legend: true },
      marks: [
        Plot.barX(data, { x: 'value', fill: 'category', insetLeft: 0.5, insetRight: 0.5 }),
        Plot.text(data, {
          x: 'value',
          fill: TOKENS.paper,
          text: (d: CompositionDatum) => (d.value / total > 0.08 ? `${Math.round((d.value / total) * 100)}%` : ''),
          fontSize: 11,
        }),
      ],
    }),
  );
}

const RENDERERS = { ranking, 'distribution-across-units': distribution, composition } as const;

export function chart(kind: FigureKind, data: unknown[], options: RenderOptions = {}): string {
  const render = RENDERERS[kind];
  if (!render) {
    throw new Error(
      `No chart type registered for figure kind "${kind}". ` +
        `Register it in src/lib/charts.ts rather than improvising one at the call site.`,
    );
  }
  // Each renderer validates its own datum shape through its typed signature; the cast is
  // the one place the registry's heterogeneous table meets a concrete renderer.
  const typed = data as RankingDatum[] & DistributionDatum[] & CompositionDatum[];
  return render(typed, options);
}
