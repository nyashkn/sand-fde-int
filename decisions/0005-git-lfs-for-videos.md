# 0005, Track source videos with Git LFS rather than excluding them

- **Date:** 2026-08-09
- **Status:** Accepted

## Context

The three Sand product videos total ~145 MB at 720p. They are the primary evidence behind
the most load-bearing claims in the research, the `Bluelake Admin` product name, the
confirmed nav structure, the OpenMRS EMR sighting, the IoT cold-chain charts.

GitHub soft-warns above 50 MB per file and hard-rejects at 100 MB, so committing them
directly is not an option.

## Decision

Track `*.mp4` with Git LFS. Keep the videos in the repo.

The claims they support are unusual enough that a reviewer should be able to check them.
"The dashboard shows fridge temperature charts" is exactly the kind of specific assertion
that deserves a verifiable source rather than a footnote.

## Alternatives

- **Gitignore the videos, cite the Vimeo URLs.** Lighter clone, but the URLs are unlisted
  embeds that could be pulled at any time, and a reviewer would have to re-derive the
  analysis to check anything.
- **Keep only the analysed frames as stills.** Smaller, but loses the audio narration,
  several of the most useful direct quotes are spoken, not shown.
- **Downsample to 360p.** ~45 MB total, but the UI text in the dashboard frames stops being
  legible, which defeats the purpose of keeping them.

## Reverses if

Clone weight becomes a real friction for reviewers. Mitigation is already documented in the
README: the written analysis stands alone, and `git lfs pull` is optional.
