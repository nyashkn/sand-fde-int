#!/usr/bin/env python3
# ponytail: one-shot script, no error handling beyond what's needed to see a clear failure
import base64
import json
import os
import sys
import urllib.request
import urllib.error

PROMPT = """You are analyzing a Sand Technologies healthcare product video for a Forward
Deployed Engineer job assignment. Watch the video and extract, in detail:

1. What is actually shown on screen (UI/dashboards/facility footage/people/settings)
2. Any product name, platform name, or feature labels visible on screen
3. What workflow or capability is being demonstrated
4. Any data types, metrics, or indicators visible (e.g. patient counts, facility status,
   maps, charts)
5. Any spoken claims about product capabilities, outcomes, or deployment details
6. Overall: what does this video tell us about how Sand's Health Operating System (HOS) /
   RHOS / Symmetri platform actually works and looks, in concrete, specific terms (not
   marketing language)

Be specific and grounded in what you actually observe — flag anything you're inferring vs
directly seeing/hearing."""


def encode_video(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def main():
    video_path = sys.argv[1]
    api_key = os.environ["OPENROUTER_API_KEY"]

    data_url = f"data:video/mp4;base64,{encode_video(video_path)}"

    payload = {
        "model": "meta/muse-spark-1.2",
        "messages": [
            {
                "role": "user",
                "content": [
                    {"type": "text", "text": PROMPT},
                    {"type": "video_url", "video_url": {"url": data_url}},
                ],
            }
        ],
    }

    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
        },
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=280) as resp:
            result = json.loads(resp.read())
    except urllib.error.HTTPError as e:
        body = e.read().decode("utf-8", errors="replace")
        print(f"HTTP {e.code}: {body}", file=sys.stderr)
        sys.exit(1)

    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
