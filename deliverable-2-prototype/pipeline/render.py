"""Render the Quarterly Health Bulletin.

    uv run python render.py [--quarter 2024-Q3]

One self-contained HTML file. No JavaScript, inline CSS, table layout — it has to
survive being embedded in an email, and the surface the Director actually reads cannot
execute anything.

Every figure carries three things: its value, its state, and a link to its lineage.
Lineage sections live in the same document as `#lineage-*` anchors, so the artifact
works offline, forwards intact, and needs no server. When the explore surface exists
those anchors become canonical URLs; the contract is identical either way.

What makes this bulletin unusual is what it refuses to draw. The trend panel and the
mortality-driver panel are withheld by computed guards, not by editorial choice, and the
edition says so with the measurement that decided it.
"""

from __future__ import annotations

import argparse
import html
from datetime import datetime, timezone
from pathlib import Path

import duckdb

MART = Path(__file__).resolve().parent / "mart"
OUT = Path(__file__).resolve().parents[1] / "output"

CSS = """
:root{--ivory:#FAF9F5;--paper:#fff;--slate:#141413;--clay:#D97757;--clay-d:#B85C3E;
--oat:#E3DACC;--olive:#788C5D;--g100:#F0EEE6;--g200:#E6E3DA;--g300:#D1CFC5;
--g500:#87867F;--g700:#3D3D3A}
body{font-family:system-ui,-apple-system,'Segoe UI',Roboto,sans-serif;background:#FAF9F5;
color:#3D3D3A;line-height:1.55;margin:0;padding:40px 24px 90px;-webkit-font-smoothing:antialiased}
.page{max-width:1080px;margin:0 auto}
.head{border-bottom:2px solid #141413;padding-bottom:20px;margin-bottom:28px}
.eyebrow{font-family:ui-monospace,Menlo,monospace;font-size:11px;letter-spacing:.14em;
text-transform:uppercase;color:#D97757;margin-bottom:8px}
h1{font-family:ui-serif,Georgia,serif;font-size:34px;line-height:1.15;color:#141413;
font-weight:600;letter-spacing:-.02em;margin:0 0 10px}
.dek{font-size:15px;color:#87867F;max-width:78ch;margin:0}
h2{font-family:ui-serif,Georgia,serif;font-size:23px;color:#141413;font-weight:600;
margin:44px 0 4px;letter-spacing:-.01em}
h2 .n{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#D97757;
letter-spacing:.1em;display:block;margin-bottom:5px;font-weight:400}
h3{font-size:15px;color:#141413;font-weight:650;margin:24px 0 8px}
p{margin:10px 0;max-width:86ch;font-size:14px}
code{font-family:ui-monospace,Menlo,monospace;font-size:.87em;background:#F0EEE6;
padding:1px 5px;border-radius:3px;color:#B85C3E}
table{width:100%;border-collapse:collapse;margin:14px 0;font-size:13px}
th{text-align:left;font-family:ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.08em;
text-transform:uppercase;color:#87867F;border-bottom:1.5px solid #141413;padding:8px 10px;
vertical-align:bottom}
td{padding:8px 10px;border-bottom:1px solid #E6E3DA;vertical-align:top}
td.num{text-align:right;font-family:ui-monospace,Menlo,monospace;font-size:12.5px;white-space:nowrap}
td.mono{font-family:ui-monospace,Menlo,monospace;font-size:11.5px}
.strip{display:table;width:100%;border-collapse:collapse;border:1px solid #D1CFC5;margin:20px 0}
.strip .c{display:table-cell;background:#fff;padding:13px 15px;border-right:1px solid #D1CFC5;width:20%}
.strip .k{font-family:ui-monospace,Menlo,monospace;font-size:9.5px;letter-spacing:.1em;
text-transform:uppercase;color:#87867F;margin-bottom:6px}
.strip .v{font-family:ui-serif,Georgia,serif;font-size:26px;color:#141413;line-height:1;font-weight:600}
.strip .v.bad{color:#B85C3E}.strip .v.ok{color:#788C5D}
.strip .d{font-size:11px;color:#87867F;margin-top:5px}
.tag{font-family:ui-monospace,Menlo,monospace;font-size:9px;letter-spacing:.06em;
text-transform:uppercase;padding:2px 6px;border-radius:2px;font-weight:600;white-space:nowrap}
.tag.prov{background:#E3DACC;color:#B85C3E}
.tag.withheld{background:#D97757;color:#fff}
.tag.ok{background:#F0EEE6;color:#788C5D}
.tag.unmeas{background:#F0EEE6;color:#87867F;font-style:italic}
.box{border-left:3px solid #D97757;background:#fff;padding:15px 18px;margin:18px 0;max-width:90ch}
.box.olive{border-left-color:#788C5D}.box.slate{border-left-color:#141413}
.box .t{font-family:ui-monospace,Menlo,monospace;font-size:10px;letter-spacing:.1em;
text-transform:uppercase;color:#D97757;margin-bottom:7px;font-weight:600}
.box.olive .t{color:#788C5D}.box.slate .t{color:#141413}
.box p{margin:6px 0}.box p:first-of-type{margin-top:0}
a.lin{font-family:ui-monospace,Menlo,monospace;font-size:10px;color:#87867F;
text-decoration:none;border-bottom:1px dotted #D1CFC5;margin-left:6px}
a.lin:hover{color:#D97757;border-bottom-color:#D97757}
.lineage{background:#fff;border:1px solid #E6E3DA;padding:14px 16px;margin:10px 0;font-size:12.5px}
.lineage h4{margin:0 0 8px;font-family:ui-monospace,Menlo,monospace;font-size:11px;
letter-spacing:.06em;color:#141413;text-transform:uppercase}
.lineage dl{margin:0;display:grid;grid-template-columns:180px 1fr;gap:3px 14px}
.lineage dt{font-family:ui-monospace,Menlo,monospace;font-size:10.5px;color:#87867F}
.lineage dd{margin:0;font-size:12.5px}
.back{font-family:ui-monospace,Menlo,monospace;font-size:10px;color:#87867F;text-decoration:none}
.prov-foot{font-family:ui-monospace,Menlo,monospace;font-size:11px;color:#87867F;
border-top:1px solid #D1CFC5;margin-top:50px;padding-top:16px;line-height:1.8}
"""


def e(x) -> str:
    return html.escape(str(x))


class Bulletin:
    """Accumulates sections and the lineage records they reference."""

    def __init__(self, con: duckdb.DuckDBPyConnection, quarter: str):
        self.con = con
        self.q = quarter
        self.parts: list[str] = []
        self.lineage: list[str] = []
        self.withheld: list[tuple[str, str]] = []

    def sql(self, query: str, **p):
        return self.con.execute(query, p).fetchall()

    # -- lineage ---------------------------------------------------------------
    def link(self, anchor: str) -> str:
        return f'<a class="lin" href="#lineage-{anchor}">lineage &rarr;</a>'

    def add_lineage(self, anchor: str, title: str, facts: dict[str, str]) -> None:
        rows = "".join(f"<dt>{e(k)}</dt><dd>{v}</dd>" for k, v in facts.items())
        self.lineage.append(
            f'<div class="lineage" id="lineage-{anchor}">'
            f"<h4>{e(title)}</h4><dl>{rows}</dl>"
            f'<p style="margin-top:10px"><a class="back" href="#top">&uarr; back to bulletin</a></p></div>'
        )

    # -- sections --------------------------------------------------------------
    def completeness(self) -> None:
        rows = self.sql(
            "SELECT period, facilities_received, facilities_expected, batches, state "
            "FROM completeness_summary WHERE quarter=$q ORDER BY period", q=self.q)
        absent = [r[0] for r in rows if r[4] == "absent"]
        contested = [r[0] for r in rows if r[4] == "contested"]

        cells = "".join(
            f'<div class="c"><div class="k">{e(r[0])}</div>'
            f'<div class="v {"bad" if r[4]!="complete" else "ok"}">{r[1]}<span '
            f'style="font-size:14px;color:#87867F">/{r[2]}</span></div>'
            f'<div class="d">{e(r[4])}{"" if r[3]<2 else f" · {r[3]} batches"}</div></div>'
            for r in rows)

        note = []
        if absent:
            note.append(f"<b>{', '.join(absent)} absent entirely.</b> No facility reported "
                        f"in {'either' if len(absent)>1 else 'that'} month, so every figure "
                        f"below covers {len(rows)-len(absent)} of {len(rows)} expected months.")
        if contested:
            note.append(f"<b>{', '.join(contested)} arrived twice with differing values.</b> "
                        f"Row-index spacing shows these are whole-batch double loads, not "
                        f"per-facility corrections. No timestamp exists in the source and both "
                        f"loads are internally consistent, so nothing in the data says which is "
                        f"correct. Figures drawing on them are marked "
                        f'<span class="tag prov">provisional</span> and a decision is queued.')

        self.parts.append(
            f'<h2><span class="n">&sect;1</span>What this edition is built on</h2>'
            f'<div class="strip">{cells}</div>'
            + "".join(f'<div class="box"><div class="t">gap</div><p>{n}</p></div>' for n in note))

    def top_facilities(self) -> None:
        rows = self.sql("""
            SELECT name, district, tier, value, provisional, months_received, months_expected
            FROM facility_quarter
            WHERE quarter=$q AND data_element='deliveries_total'
            ORDER BY value DESC LIMIT 10""", q=self.q)
        body = "".join(
            f"<tr><td class='num'>{i}</td><td>{e(r[0])}</td><td>{e(r[1])}</td>"
            f"<td class='mono'>{e(r[2])}</td><td class='num'>{r[3]:,.0f}</td>"
            f"<td>{'<span class=\"tag prov\">provisional</span>' if r[4] else '<span class=\"tag ok\">settled</span>'}"
            f"{self.link('top-facilities')}</td></tr>"
            for i, r in enumerate(rows, 1))
        self.parts.append(
            f'<h2><span class="n">&sect;2 · metric 1</span>Top 10 facilities by delivery volume</h2>'
            f'<p>Ranked on total deliveries for {e(self.q)}. <b>This ranks volume, not quality.</b> '
            f'Delivery volume tracks facility tier closely, so the ordering largely reproduces the '
            f'tier hierarchy rather than telling you which facilities perform well.</p>'
            f'<table><thead><tr><th>#</th><th>Facility</th><th>District</th><th>Tier</th>'
            f'<th style="text-align:right">Deliveries</th><th>State</th></tr></thead>'
            f'<tbody>{body}</tbody></table>')

        tot = self.sql("""SELECT sum(value), count(DISTINCT org_unit), sum(provisional_inputs)
            FROM facility_quarter WHERE quarter=$q AND data_element='deliveries_total'""", q=self.q)[0]
        self.add_lineage("top-facilities", f"Top 10 facilities by volume · {self.q}", {
            "figure": f"deliveries_total, grain (facility, quarter), {e(self.q)}",
            "inputs": f"{tot[0]:,.0f} deliveries across {tot[1]} facilities",
            "provisional inputs": f"{int(tot[2]):,} of {tot[1]} facility-observations",
            "months": self._months_phrase(),
            "rule applied": "<code>DEFAULT-BATCH-01</code> — lowest occurrence ordinal on "
                            "contested batches. Arbitrary and pending resolution.",
            "definition": "Sum of <code>deliveries_total</code> over the quarter's months.",
            "source": "assignment_csv &rarr; bronze &rarr; silver &rarr; facility_quarter",
        })

    def maternal(self) -> None:
        els = [("live_births", "Live births"), ("stillbirths", "Stillbirths"),
               ("neonatal_deaths_early", "Neonatal deaths, 0&ndash;7 days"),
               ("neonatal_deaths_late", "Neonatal deaths, 8&ndash;28 days"),
               ("neonatal_deaths_asphyxia", "&mdash; of which birth asphyxia"),
               ("neonatal_deaths_prematurity", "&mdash; of which prematurity"),
               ("neonatal_deaths_sepsis", "&mdash; of which sepsis"),
               ("neonatal_deaths_congenital", "&mdash; of which congenital")]
        codes = dict(self.sql("SELECT DISTINCT canonical_element, code FROM crosswalk "
                              "WHERE code_system='ICD-10' AND canonical_element<>''"))
        body = ""
        for el, label in els:
            r = self.sql("""SELECT sum(value), sum(provisional_inputs) FROM district_quarter
                            WHERE quarter=$q AND data_element=$e""", q=self.q, e=el)[0]
            if r[0] is None:
                continue
            body += (f"<tr><td>{label}</td><td class='mono'>{e(codes.get(el,'&mdash;'))}</td>"
                     f"<td class='num'>{r[0]:,.0f}</td>"
                     f"<td>{'<span class=\"tag prov\">provisional</span>' if r[1] else '<span class=\"tag ok\">settled</span>'}</td></tr>")

        nmr = self.sql("""SELECT sum(numerator), sum(denominator) FROM nmr_district_quarter
                          WHERE quarter=$q""", q=self.q)[0]
        rate = nmr[0] / nmr[1] * 1000
        self.parts.append(
            f'<h2><span class="n">&sect;3 · metric 2</span>Maternal and neonatal indicators</h2>'
            f'<p>National totals for {e(self.q)}, bound to ICD-10 perinatal codes so they are '
            f'comparable with national reporting rather than bespoke. {self.link("maternal")}</p>'
            f'<table><thead><tr><th>Indicator</th><th>ICD-10</th>'
            f'<th style="text-align:right">Count</th><th>State</th></tr></thead>'
            f'<tbody>{body}</tbody></table>'
            f'<div class="box olive"><div class="t">headline</div>'
            f'<p><b>Neonatal mortality rate — {rate:,.1f} per 1,000 live births</b> '
            f'({nmr[0]:,.0f} deaths / {nmr[1]:,.0f} live births), WHO GHO definition. '
            f'Reported figures for Rwanda sit near 19 per 1,000, so this sample runs roughly '
            f'{rate/19:.1f}&times; the national figure — expected, since the provided data is '
            f'a synthetic sample rather than a real extract.</p></div>')

        self.add_lineage("maternal", f"Maternal and neonatal indicators · {self.q}", {
            "figure": f"8 indicators, grain (national, quarter), {e(self.q)}",
            "inputs": f"{nmr[1]:,.0f} live births, {nmr[0]:,.0f} neonatal deaths",
            "months": self._months_phrase(),
            "rule applied": "<code>DEFAULT-BATCH-01</code> on contested batches",
            "definition": "WHO GHO neonatal mortality rate: deaths within 28 days per 1,000 "
                          "live births. Cause codes bound to ICD-10 P21, P07, P36, Q00&ndash;Q99.",
            "identity check": "Cause-of-death columns sum to total neonatal deaths in "
                              "1,404 of 1,404 source rows.",
        })

    def capability(self) -> None:
        els = [("capability_nicu_beds", "NICU beds"),
               ("capability_incubators_functional", "Functional incubators"),
               ("capability_cpap_machines", "CPAP machines"),
               ("capability_radiant_warmers", "Radiant warmers"),
               ("staff_nurses_neonatal", "Neonatal-trained nurses")]
        tiers = [r[0] for r in self.sql(
            "SELECT DISTINCT tier FROM org_units WHERE level='facility' AND tier<>'' ORDER BY tier")]
        head = "".join(f"<th style='text-align:right'>{e(t)}</th>" for t in tiers)
        body = ""
        for el, label in els:
            cells = ""
            for t in tiers:
                r = self.sql("""SELECT avg(value) FROM facility_quarter
                    WHERE quarter=$q AND data_element=$e AND tier=$t""", q=self.q, e=el, t=t)[0][0]
                cells += f"<td class='num'>{r:,.1f}</td>" if r is not None else "<td class='num'>&mdash;</td>"
            body += f"<tr><td>{label}</td>{cells}</tr>"
        self.parts.append(
            f'<h2><span class="n">&sect;4 · metric 3</span>Facility capability inventory</h2>'
            f'<p>Mean holdings per facility, by tier. <b>Presented as an inventory of what '
            f'facilities have, not as a performance score.</b> The relationship between these '
            f'holdings and mortality does not survive stratification &mdash; see &sect;6. '
            f'{self.link("capability")}</p>'
            f'<table><thead><tr><th>Capability</th>{head}</tr></thead><tbody>{body}</tbody></table>'
            f'<div class="box"><div class="t">read with care</div><p>District-tier facilities are '
            f'statistically indistinguishable from Health Centers across every equipment column '
            f'above. The stated four-tier hierarchy behaves as two bands in this data.</p></div>')
        self.add_lineage("capability", f"Facility capability inventory · {self.q}", {
            "figure": "5 capability measures, grain (tier, quarter)",
            "inputs": "117 facilities, one observation per capability per facility",
            "note": "Capability measures carry period <code>ALL</code> in silver — they "
                    "describe a facility, not a facility-month.",
            "definition": "Arithmetic mean of holdings across facilities within a tier.",
        })

    def district_nmr(self) -> None:
        rows = self.sql("""SELECT district, value, numerator, denominator, provisional
            FROM nmr_district_quarter WHERE quarter=$q ORDER BY value DESC""", q=self.q)
        body = "".join(
            f"<tr><td>{e(r[0])}</td><td class='num'>{r[1]:,.1f}</td>"
            f"<td class='num'>{r[2]:,.0f}</td><td class='num'>{r[3]:,.0f}</td>"
            f"<td>{'<span class=\"tag prov\">provisional</span>' if r[4] else '<span class=\"tag ok\">settled</span>'}"
            f"{self.link('district-nmr')}</td></tr>" for r in rows)
        self.parts.append(
            f'<h2><span class="n">&sect;5</span>Neonatal mortality by district</h2>'
            f'<p>Per 1,000 live births, {e(self.q)}. Numerator and denominator are shown so the '
            f'arithmetic is checkable without leaving the page. District is the finest grain this '
            f'data supports &mdash; facility coordinates in the source are unusable, see &sect;7.</p>'
            f'<table><thead><tr><th>District</th><th style="text-align:right">NMR</th>'
            f'<th style="text-align:right">Deaths</th><th style="text-align:right">Live births</th>'
            f'<th>State</th></tr></thead><tbody>{body}</tbody></table>')
        self.add_lineage("district-nmr", f"Neonatal mortality by district · {self.q}", {
            "figure": f"nmr, grain (district, quarter), {e(self.q)}",
            "inputs": f"{len(rows)} districts, {sum(r[3] for r in rows):,.0f} live births",
            "provisional": f"{sum(1 for r in rows if r[4])} of {len(rows)} districts",
            "months": self._months_phrase(),
            "definition": "WHO GHO: (early + late neonatal deaths) / live births &times; 1,000",
            "grain note": "District, not facility. Facility-level geography is not derivable "
                          "from this source.",
        })

    def withheld_panels(self) -> None:
        t = self.sql("""SELECT data_element, observed_lag1, null_mean, null_sd, seed, trials, reason
                        FROM temporal_signal_guard WHERE disposition='withheld'""")
        s = self.sql("""SELECT covariate, pooled_r, within_strata, stratified_by, reason
                        FROM stratification_guard WHERE disposition='withheld'""")
        out = ('<h2><span class="n">&sect;6</span>Withheld &mdash; analyses this data cannot support</h2>'
               '<p>Two panels a quarterly bulletin would normally carry are not printed. They are '
               'withheld by automated guards rather than editorial judgement, and each guard '
               'records the measurement that decided it.</p>')

        if t:
            rows = "".join(
                f"<tr><td class='mono'>{e(r[0])}</td><td class='num'>{r[1]:+.3f}</td>"
                f"<td class='num'>{r[2]:+.3f} &plusmn; {r[3]:.3f}</td>"
                f"<td><span class='tag withheld'>withheld</span></td></tr>" for r in t)
            out += (f'<div class="box"><div class="t">withheld · trend vs previous quarter</div>'
                    f'<p><b>There is no genuine month-to-month signal in this data.</b> Shuffling '
                    f'each facility\'s months among themselves destroys any real ordering while '
                    f'preserving that facility\'s level. The shuffled null matches the observed '
                    f'autocorrelation, so all apparent movement is a stable per-facility baseline '
                    f'plus noise &mdash; a quarter-over-quarter arrow would be drawing noise.</p>'
                    f'<table><thead><tr><th>Series</th><th style="text-align:right">Observed lag-1</th>'
                    f'<th style="text-align:right">Permutation null</th><th>Disposition</th></tr></thead>'
                    f'<tbody>{rows}</tbody></table>'
                    f'<p style="font-size:12px;color:#87867F">Seed {t[0][4]}, {t[0][5]} trials. '
                    f'Recorded so the disposition is reproducible.</p></div>')

        if s:
            rows = "".join(
                f"<tr><td class='mono'>{e(r[0])}</td><td class='num'>{r[1]:+.3f}</td>"
                f"<td class='mono'>{e(r[2])}</td><td><span class='tag withheld'>withheld</span></td></tr>"
                for r in s)
            out += (f'<div class="box"><div class="t">withheld · what drives mortality</div>'
                    f'<p><b>Every candidate driver is confounded by tier.</b> Pooled across all 117 '
                    f'facilities, staff training correlates with mortality at &minus;0.844 &mdash; '
                    f'strong enough to look like a finding. Inside each tier it disappears. Both the '
                    f'training rate and the death count are downstream of where equipment and staff '
                    f'were placed, so the pooled figure measures tier and not training. Publishing it '
                    f'would point the Ministry at a lever that is not there.</p>'
                    f'<table><thead><tr><th>Covariate</th><th style="text-align:right">Pooled r</th>'
                    f'<th>Within tier</th><th>Disposition</th></tr></thead><tbody>{rows}</tbody></table></div>')
        self.parts.append(out)
        self.withheld = [("trend vs previous quarter", t[0][6] if t else ""),
                         ("what drives mortality", s[0][4] if s else "")]

    def defects(self) -> None:
        self.parts.append(
            '<h2><span class="n">&sect;7</span>Known defects in the source data</h2>'
            '<p>Published rather than silently corrected. Each was found by a one-line check that '
            'runs on every ingest, so the same class of problem is caught in the next quarter\'s '
            'file without anyone remembering to look.</p>'
            '<table><thead><tr><th>Field</th><th>Finding</th>'
            '<th style="text-align:right">Extent</th><th>Handling</th></tr></thead><tbody>'
            '<tr><td class="mono">gps_lat / gps_lon</td><td>Uniform random within Rwanda\'s bounding '
            'box. Every province spans the full country extent.</td><td class="num">117 / 117</td>'
            '<td><span class="tag unmeas">not used</span></td></tr>'
            '<tr><td class="mono">2024-01, 2024-03</td><td>Each loaded twice with differing values. '
            'No timestamp distinguishes them.</td><td class="num">234 rows</td>'
            '<td><span class="tag prov">queued</span></td></tr>'
            '<tr><td class="mono">2024-02, 2024-12</td><td>Absent entirely.</td>'
            '<td class="num">2 months</td><td><span class="tag unmeas">disclosed</span></td></tr>'
            '<tr><td class="mono">facility_name</td><td>Contradicts <code>tier_level</code>.</td>'
            '<td class="num">62 / 117</td><td><span class="tag unmeas">label only</span></td></tr>'
            '<tr><td class="mono">staff_per_delivery_2024</td><td>Named as derived but cannot be '
            'reconstructed &mdash; best formula matched 58.1%, worse than guessing the column\'s '
            'own mode.</td><td class="num">3 values</td><td><span class="tag unmeas">not used</span></td></tr>'
            '<tr><td class="mono">birth_weight_less_2500g</td><td>Independent of prematurity '
            '(r = 0.018) where reality gives 0.6&ndash;0.9.</td><td class="num">1,404 rows</td>'
            '<td><span class="tag unmeas">not used</span></td></tr>'
            '<tr><td class="mono">facility_id</td><td>Prefix ambiguous across districts &mdash; '
            '<code>NYA</code> maps to 7.</td><td class="num">9 prefixes</td>'
            '<td><span class="tag ok">resolved</span></td></tr>'
            '</tbody></table>'
            '<div class="box slate"><div class="t">why publish these</div>'
            '<p>A bulletin that renders clean-looking numbers over data with these problems is '
            'exactly the object the Director already refuses. Naming them, and showing what each '
            'figure did about them, is what makes the rest of the document checkable rather than '
            'merely confident.</p></div>')

    def _months_phrase(self) -> str:
        rows = self.sql("SELECT period, state FROM completeness_summary WHERE quarter=$q "
                        "ORDER BY period", q=self.q)
        got = [r[0] for r in rows if r[1] != "absent"]
        missing = [r[0] for r in rows if r[1] == "absent"]
        p = f"{len(got)} of {len(rows)} expected months"
        return p + (f" &mdash; <b>{', '.join(missing)} absent</b>" if missing else "")

    # -- assembly --------------------------------------------------------------
    def build(self) -> str:
        self.completeness()
        self.top_facilities()
        self.maternal()
        self.capability()
        self.district_nmr()
        self.withheld_panels()
        self.defects()

        n_prov = self.sql("SELECT count(*) FROM nmr_district_quarter WHERE quarter=$q "
                          "AND provisional", q=self.q)[0][0]
        stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        return f"""<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>Quarterly Health Bulletin &mdash; {e(self.q)}</title><style>{CSS}</style></head>
<body><div class="page" id="top">
<header class="head">
<div class="eyebrow">Ministry of Health &middot; Rwanda &middot; neonatal &middot; prototype</div>
<h1>Quarterly Health Bulletin &mdash; {e(self.q)}</h1>
<p class="dek">Generated from the provided sample data. Every figure carries its state and a
link to the rows, rules and gaps behind it. Two standard panels are withheld because the data
cannot support them; both say so with the measurement that decided it.</p>
</header>
{''.join(self.parts)}
<h2><span class="n">&sect;8</span>Lineage</h2>
<p>One record per figure above. In the full system these are addressable URLs
(<code>/metric/nmr/district/nyanza/{e(self.q)}/lineage</code>); in this artifact they are
anchors in the same file, so it works offline and forwards intact.</p>
{''.join(self.lineage)}
<footer class="prov-foot">
Generated {stamp} &middot; {n_prov} of 30 district figures provisional &middot;
2 panels withheld &middot; source <code>assignment_csv</code> + <code>dhis2</code><br>
Pipeline <code>run.py</code> (Hamilton &rarr; DuckDB &rarr; Parquet) &middot;
renderer <code>render.py</code> &middot; no JavaScript, no external assets<br>
Regenerate: <code>uv run python run.py &amp;&amp; uv run python render.py</code>
</footer>
</div></body></html>"""


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--quarter", default="2024-Q3")
    args = ap.parse_args()

    OUT.mkdir(exist_ok=True)
    con = duckdb.connect(str(MART / "mart.duckdb"), read_only=True)
    doc = Bulletin(con, args.quarter).build()
    path = OUT / f"bulletin-{args.quarter}.html"
    path.write_text(doc, encoding="utf-8")
    con.close()

    print(f"wrote {path}  ({len(doc):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
