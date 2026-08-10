#!/usr/bin/env python3
"""Machine-vision review of a rendered artifact screenshot.

fabro agent nodes are text-only (read_file does NOT attach images to the model),
so visual review lives here: base64 the PNG -> OpenRouter kimi-k3 vision -> write a
concrete, actionable critique the refine node can apply. Run under the Infisical
wrapper so OPENROUTER_API_KEY is present:

    infisical-kn-personal-dev python3 scripts/vision_review.py <png> <out_md> [pass_label]
"""
import base64
import json
import os
import sys
import urllib.error
import urllib.request

MODEL = "moonshotai/kimi-k3"

PROMPT = """You are a senior information-designer reviewing a RENDERED screenshot of a \
single-page HTML briefing artifact (Rwanda MoH digital-health landscape). You can see the \
pixels. Judge it as a reader would, then give the developer a precise, actionable punch-list.

Assess and report, in this order:
1. VERDICT: one line — is this readable and visually credible as an executive briefing? \
(strong / acceptable / weak)
2. READABILITY: contrast, font sizes, line length, whitespace, visual hierarchy. Name the \
SPECIFIC element (by its visible heading/section) and the SPECIFIC fix (e.g. "Section 3 persona \
cards: body text too low-contrast grey on cream, darken to #333; cards cramped, add 16px padding").
3. VISUALS: are the diagrams (systems map SVG, integration/data-flow SVG) clear, labelled, and \
information-dense — or thin/ugly/empty? Where should a visual be ADDED or UPGRADED (tables->\
diagrams, plain lists->timelines, add legends, add per-persona journey lanes, colour-code tiers)?
4. LAYOUT DEFECTS: anything overflowing, overlapping, misaligned, clipped, or blank.
5. CITATIONS: are source links / a Sources section visibly present and credible? If not, say so.

Be concrete and reference visible section names. Output GitHub-flavoured markdown as a checklist \
of fixes ordered by impact. Do NOT rewrite the HTML; only critique. If you truly cannot see the \
image, output the single line: NO VISION"""


def main() -> int:
    if len(sys.argv) < 3:
        print("usage: vision_review.py <png> <out_md> [pass_label]", file=sys.stderr)
        return 2
    png, out_md = sys.argv[1], sys.argv[2]
    label = sys.argv[3] if len(sys.argv) > 3 else ""
    key = os.environ.get("OPENROUTER_API_KEY")
    if not key:
        print("OPENROUTER_API_KEY not in env (run under infisical wrapper)", file=sys.stderr)
        return 1
    with open(png, "rb") as f:
        b64 = base64.b64encode(f.read()).decode()

    payload = {
        "model": MODEL,
        "messages": [{
            "role": "user",
            "content": [
                {"type": "text", "text": PROMPT},
                {"type": "image_url", "image_url": {"url": "data:image/png;base64," + b64}},
            ],
        }],
        "max_tokens": 4000,
        "temperature": 0.3,
        # kimi-k3 defaults to heavy reasoning that eats the whole budget -> content:null.
        "reasoning": {"enabled": False},
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode(),
        headers={"Authorization": "Bearer " + key, "Content-Type": "application/json"},
    )
    try:
        r = json.load(urllib.request.urlopen(req, timeout=180))
    except urllib.error.HTTPError as e:
        print(f"OpenRouter HTTP {e.code}: {e.read().decode()[:400]}", file=sys.stderr)
        return 1

    msg = (r.get("choices") or [{}])[0].get("message", {}) or {}
    # Fall back to the reasoning field if the provider dumped the answer there.
    content = ((msg.get("content") or "") or (msg.get("reasoning") or "")).strip()
    if not content:
        print("empty vision response: " + json.dumps(r)[:400], file=sys.stderr)
        return 1

    os.makedirs(os.path.dirname(out_md) or ".", exist_ok=True)
    header = f"# Vision review {label}\n\n_model: {MODEL} · usage: {r.get('usage')}_\n\n"
    with open(out_md, "w") as f:
        f.write(header + content + "\n")
    print(f"vision review -> {out_md} ({len(content)} chars)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
