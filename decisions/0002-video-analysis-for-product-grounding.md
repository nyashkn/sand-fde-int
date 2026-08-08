# 0002 — Use native video-input LLM analysis, not audio transcription alone

- **Date:** 2026-08-09
- **Status:** Accepted

## Context

Web research plateaued: Sand's written public materials are marketing copy and job postings,
neither of which shows the product. Three product videos embedded on `healthcare.sandtech.com`
were the only remaining source that could show the actual UI.

Seven other Sand videos on YouTube are talking-head interviews, where the entire payload is
speech.

## Decision

Split by content type rather than using one method for everything:

- **Vimeo product videos** (facility footage, dashboard demos) → `meta/muse-spark-1.2` via
  OpenRouter, which accepts video natively. Visual UI evidence is the whole point; a
  transcript would lose it.
- **YouTube talking-heads** → local `mlx-whisper` if needed. Free, more accurate on speech,
  and no visual content worth paying video-input tokens for.

This is what produced the single most consequential finding in the whole research pack: the
product is called `Bluelake Admin`, its full nav structure, its chart inventory, and the
confirmation that the EMR is OpenMRS — none of which is written down anywhere public.

## Alternatives

- **Transcribe everything with Whisper.** Free and reliable, but returns nothing about the
  UI. Would have missed the `Bluelake Admin` finding entirely.
- **Watch the videos manually.** Fine for three videos, doesn't scale, and produces notes
  nobody else can audit against a timestamp.
- **Frame-extract with ffmpeg then use a vision model.** Cheaper per call, loses temporal
  context, and adds a preprocessing step for no gain at this volume.

## Reverses if

Cost becomes a factor at higher volume, or a longer video needs analysis — the 5:11 clip
failed repeatedly on provider-side gateway timeouts regardless of resolution
(`research/sand-product-research.md` §7.4). At that point, segment the video or fall back
to audio.
