# How to Contribute a New Language (PR Checklist)

This project aims to demonstrate **language inclusion + safety**. Please keep contributions lightweight, transparent, and clearly licensed.

## Requirements
- **Data must be synthetic or clearly licensed** (prefer **CC0**). No scraped or personal data.
- Keep the corpus small (≈10–30 lines) and **benign**. Harmful/adversarial prompts belong in `adversarial/` or templates.
- If you add refusal heuristics, include them in `policies/safety_rules.yaml` under the new language.

## Folder & file expectations
- `data/<lang>/corpus.txt` — 1 sentence per line. Add a comment header with source/license if not CC0.
- `policies/safety_rules.yaml` — add your language block under `languages` with:
  - `code` (ISO-like short code),
  - optional `name`,
  - optional `refusal_markers` (strings the model might use to refuse in that language).
- (Optional) `adversarial/prompts.jsonl` — add a few entries exercising **attack types** (`prompt_injection`, `homoglyphs`, `code_mix`, `roleplay`, etc.).
- (Optional) `templates/prompt_templates.yaml` — add safe/unsafe seed prompts if they help your use case.

## PR Checklist
- [ ] Added `data/<lang>/corpus.txt` with **synthetic/clearly-licensed** lines and no personal data.
- [ ] Updated `policies/safety_rules.yaml` with the new language (code, optional name, refusal markers).
- [ ] (Optional) Added adversarial rows to `adversarial/prompts.jsonl` with `id`, `lang`, `category`, `attack_type`, `prompt`.
- [ ] (Optional) Added seed entries to `templates/prompt_templates.yaml`.
- [ ] Ran `python scripts/gen_prompts.py --out reports/eval_prompts.csv` and verified the new language appears.
- [ ] Ran your model and produced `reports/eval_results.csv` (or appended to it).
- [ ] Ran `python scripts/compute_metrics.py --results reports/eval_results.csv` and checked metrics do not regress unintentionally.
- [ ] Updated docs (if needed) and ensured **data provenance** is stated.
- [ ] CI green (GitHub Actions / GitLab CI passes).

## Local test steps
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# regenerate prompts (detects new data/<lang>/)
python scripts/gen_prompts.py --out reports/eval_prompts.csv

# run your model, write reports/eval_results.csv
# then compute metrics
python scripts/compute_metrics.py --results reports/eval_results.csv
```
