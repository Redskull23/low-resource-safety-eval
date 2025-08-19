# low-resource-safety-eval

A compact, public demo of **language inclusion + safety evaluation** for **low-resource** and **multilingual** LLM use cases.

This repo shows an end-to-end **policy → prompts → model run → metrics → report** pipeline you can fork, extend, and discuss with stakeholders—**without** claiming deep linguistics coverage. It’s designed for product thinking, safety program design, and lightweight research prototyping.

---

## Why this is useful

- **Language inclusion**: Goes beyond English to cover low-resource languages, highlighting where safeguards silently fail due to code-mixing, idioms, or orthography.
- **Product thinking demo**: Turns abstract “we need safety” into a reproducible pipeline and single-file metrics you can put in PRDs, RFCs, or readouts.
- **Transparent data**: Mini corpora are **synthetic** and **CC0**; provenance and consent notes are explicit by design.
- **Portable**: Simple CSV in/out; works with any model/API; optional GitHub Actions runs metrics on every PR.
- **Extensible**: Drop in new languages, categories, adversarial attacks, or policies as YAML and JSONL—no refactor.

---

## What’s inside

*Languages included:* `ht`, `yo`, `en`, `de`, `fr`, `es`, `ja`

```text
.
├── .github/                     # GitHub Actions CI, issue/PR templates
├── .vscode/                     # VS Code settings & extension recs
├── adversarial/                 # Jailbreak / jiggle prompts (JSONL)
├── data/                        # CC0, synthetic mini-corpora + notes
│   ├── ht/ (Haitian Creole)     ├── yo/ (Yorùbá)
│   ├── en/ (English)            ├── de/ (German)
│   ├── fr/ (French)             ├── es/ (Spanish)
│   └── ja/ (Japanese)
├── docs/                        # Annotation guidelines & context notes
├── notebooks/                   # Metrics notebook (exploratory)
├── policies/                    # YAML safety categories & markers
├── reports/                     # Generated prompts & model results (CSV/JSON)
├── scripts/                     # Prompt gen + metrics
├── templates/                   # Prompt templates (safe/unsafe)
├── requirements.txt             # Minimal Python deps
├── .gitlab-ci.yml (optional)    # GitLab CI (mirrors GH Actions steps)
└── README.md
```
Supported languages (initial): ht, yo, en, de, fr, es, ja

Add more by dropping a new data/<lang>/corpus.txt (CC0 or clearly-licensed) and, optionally, refusal markers in policies/safety_rules.yaml.
⸻

```text

Pipeline at a glance
Policies (YAML)  +  Templates  +  Corpora
        │                  │           │
        └──────────────┬───┴───────────┘
                       ▼
              reports/eval_prompts.csv
                       │   (you run your model/API)
                       ▼
              reports/eval_results.csv
                       │
             scripts/compute_metrics.py
                       ▼
           reports/metrics.json + notebooks/metrics.ipynb
```
**Quickstart**
```
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# 1) Generate evaluation prompts (safe + unsafe + adversarial)
python scripts/gen_prompts.py --out reports/eval_prompts.csv

# 2) Run your model and write results to CSV:
#    columns: id,lang,category,attack_type,is_harmful,is_refusal
#    - is_harmful: True if the prompt intent is harmful (e.g., category != benign)
#    - is_refusal: True if your model refused/safeguarded the request
#      (Your runner decides how to detect this; pattern, metadata, or classifier)
# Example stub file:
# reports/sample_eval_results.csv

# 3) Compute metrics (Safety Acceptance Rate, ASR under attack, False Refusals)
python scripts/compute_metrics.py --results reports/sample_eval_results.csv

# 4) Explore visually
# open notebooks/metrics.ipynb in VS Code/Jupyter
```
**Docs quick links**
Contribute a new language: docs/contributing_new_language.md
Langfuse CSV schema example: docs/langfuse_csv_schema.md

**What this repository demonstrates (step-by-step)**
	1.	Clear policy surface
	•	*policies/safety_rules.yaml declares categories (e.g., self_harm, violence, benign) and optional per-language refusal markers.*
	•	*Communicates scope and guardrail intent to stakeholders.*
	2.	Curated language inputs
	•	*data/<lang>/corpus.txt contains small, synthetic sentences capturing everyday topics, idioms, and code-mix patterns.*
	•	*data/README.md and CC0 license clarify provenance & consent (no scraped or personal data).*
	3.	Prompt set construction
	•	*templates/prompt_templates.yaml defines safe and unsafe seed prompts.*
	•	*adversarial/prompts.jsonl supplies jailbreaks (roleplay, injection, homoglyphs, typos, code-mix).*
	•	*scripts/gen_prompts.py composes corpora + templates + adversarial into reports/eval_prompts.csv.*
	4.	Model evaluation run (bring your own model)
	•	You call your model over each prompt and emit reports/eval_results.csv with minimal ground truth fields:
	•	**is_harmful** (True for non-benign categories)
	•	**is_refusal** (your detection of a refusal/safeguard)
	•	**Keeps the framework model-agnostic and easy to integrate.**
	5.	Safety metrics
	•	scripts/compute_metrics.py calculates:
	  •	Safety Acceptance Rate (SAR): benign answered (not refused)
	  •	Attack Success Rate (ASR): harmful answered (not refused) — lower is better
	  •	False Refusal Rate (FRR): benign refused — lower is better
	  •	Outputs a single reports/metrics.json for dashboards or PRDs.
	  •	notebooks/metrics.ipynb provides quick charts (counts, ASR by category).
	6.	Reporting & review
	•	Store results in reports/ as CSV/JSON (or export for Langfuse ingestion).
	•	GitHub Actions CI (.github/workflows/ci.yml) regenerates prompts and recomputes metrics on every PR for sanity.
	7.	Governance & extension
	•	Update policies/ to reflect evolving safety rules.
	•	Expand data/ with new languages or dialects; adjust templates/adversarial patterns as needed.
	•	The structure encourages transparent provenance and repeatable evaluation.

⸻

Metrics (definitions)
	•	Benign = prompts with category: benign → is_harmful = False
	•	Harmful = prompts with non-benign safety categories → is_harmful = True
	•	Refusal = model safeguards/declines (detected by your runner)
	•	Safety Acceptance Rate (SAR)
= (# benign prompts answered) / (total benign prompts)
	•	False Refusal Rate (FRR)
= (# benign prompts refused) / (total benign prompts)
	•	Attack Success Rate (ASR)
= (# harmful prompts answered) / (total harmful prompts)

Lower ASR/FRR and higher SAR are better. Track ASR by category and by attack_type (e.g., injection vs. homoglyph) to localize weaknesses.

⸻

Data, licensing, and consent
	•	All text in data/ is synthetic and released under CC0 (see data/LICENSE).
	•	No personal data, no web scraping.
	•	When contributing, state source & license clearly; keep private data out.

⸻

Extending the project
	•	Add a language
	1.	Create data/<lang>/corpus.txt (CC0 or clearly-licensed).
	2.	Optionally add refusal markers in policies/safety_rules.yaml.
	3.	Re-run gen_prompts.py.
	•	Add a category or rule
Edit policies/safety_rules.yaml and, if helpful, add seed prompts in templates/ and adversarial cases in adversarial/.
	•	Integrate Langfuse (optional)
Export your eval_results.csv and metrics to your observability workflow or upload batches to Langfuse for run-level analytics.

⸻

CI (optional)
	•	GitHub Actions: .github/workflows/ci.yml installs deps, generates prompts, computes metrics on PRs, and uploads reports/ artifacts.
	•	GitLab CI: .gitlab-ci.yml mirrors the same steps if you host on GitLab.

⸻

Limitations & scope
	•	This is a demo for safety product thinking and multilingual inclusion—not a comprehensive benchmark.
	•	Mini corpora are intentionally small; results highlight patterns and regressions, not leaderboard-grade scores.
	•	Cultural nuance matters: expand with community input when you scale categories or languages.

⸻

License
	•	Code: MIT (see LICENSE)
	•	Data in data/: CC0 (public domain dedication)

⸻

How to apply it

From your repo root:
```
# overwrite README.md with this content, then:
git add README.md
git commit -m "Docs: detailed README with purpose and step-by-step demo"
git push
```
