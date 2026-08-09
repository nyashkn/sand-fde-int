#!/usr/bin/env python3
# ponytail: one-shot red-team runner. stdlib only, threads for parallelism.
import json
import os
import sys
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

MODELS = [
    "openai/gpt-5.6-sol",
    "google/gemini-3.1-pro-preview",
    "x-ai/grok-4.5",
]

SYSTEM = """You are a hostile reviewer. Your job is to find what is WRONG with the
document you are given, not to praise it. Sycophancy is a failure condition for this task.

You are reviewing a scoping document written by a candidate for a Forward Deployed Engineer
role at Sand Technologies, deploying to Rwanda's Ministry of Health. The candidate must pick
ONE of three problems for a 6-week sprint. They picked Problem A (automating a Quarterly
Health Bulletin) plus one bounded handover act.

CRITICAL CONTEXT ABOUT HOW THIS DOCUMENT WAS PRODUCED: the problem selection was reviewed by a
six-persona "council" — but all six personas were the SAME underlying model (Claude), given
different character prompts. That is not six independent opinions. It is one model's priors
sampled six ways. You are being called specifically because you are a DIFFERENT model family,
to catch what that process structurally could not.

Do not assume the document is good because it is thorough. Thoroughness and correctness are
different properties. A confidently-argued wrong answer is exactly what this exercise is
designed to catch."""

PROMPT = """Read the scoping document below in full, then answer the five questions.

Be specific and concrete. Cite the section number you are attacking. Generic strategy
commentary is worthless — if you cannot name the specific claim you think is wrong and why,
say "no substantive objection" rather than inventing one.

---

QUESTION 1 — THE CORE CHOICE.
Is Problem A the right pick for a 6-week first engagement? If you disagree, name which of
A, B or C you would pick and the specific argument that beats the document's reasoning.
If you agree, say so plainly and move on — do not manufacture disagreement.

QUESTION 2 — THE STRONGEST ATTACK.
Regardless of your answer to Q1: what is the single strongest argument that this commitment
is wrong? Steelman it. This is the most important question — answer it even if you agree
with the choice.

QUESTION 3 — FACTUAL AND LOGICAL ERRORS.
Identify any claim in the document that is factually wrong, internally inconsistent, or
unsupported by the evidence cited. Quote it and explain. Include reasoning errors, not just
factual ones.

QUESTION 4 — WHAT IS MISSING.
What should a scoping document for this engagement contain that this one does not? Be
specific about what the omission would cost.

QUESTION 5 — CONVERGENCE CHECK.
The document's own appendix admits its review process could not separate "A is correct" from
"one model's priors reliably land on A." As a different model family: do you independently
arrive at Problem A, or do you think that convergence is an artifact? Answer honestly — if you
would also have picked A, that is useful evidence and you should say so.

---

Finish with a single line in EXACTLY this format:

VERDICT: survives | survives-with-amendments | does-not-survive
TOP_FIX: <one sentence — the single most important change, or "none">

---

# THE DOCUMENT UNDER REVIEW

{doc}
"""


def call(model, doc, key):
    body = {
        "model": model,
        "messages": [
            {"role": "system", "content": SYSTEM},
            {"role": "user", "content": PROMPT.format(doc=doc)},
        ],
    }
    req = urllib.request.Request(
        "https://openrouter.ai/api/v1/chat/completions",
        data=json.dumps(body).encode(),
        headers={"Authorization": f"Bearer {key}", "Content-Type": "application/json"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=600) as r:
            out = json.loads(r.read())
        return model, out["choices"][0]["message"]["content"]
    except urllib.error.HTTPError as e:
        return model, f"HTTP {e.code}: {e.read().decode('utf-8', 'replace')[:1200]}"
    except Exception as e:  # noqa: BLE001
        return model, f"ERROR {type(e).__name__}: {e}"


def main():
    key = os.environ["OPENROUTER_API_KEY"]
    doc = open("/tmp/d1-under-review.md").read()
    with ThreadPoolExecutor(max_workers=3) as ex:
        results = list(ex.map(lambda m: call(m, doc, key), MODELS))
    for model, text in results:
        slug = model.replace("/", "_")
        with open(f"/tmp/redteam-{slug}.md", "w") as f:
            f.write(f"# {model}\n\n{text}\n")
        print(f"=== {model} === ({len(text)} chars)")
    print("done")


if __name__ == "__main__":
    main()
