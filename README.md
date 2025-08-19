# low-resource-safety-eval

_A compact, public demo repo that shows end-to-end **language inclusion** + **safety** product thinking for low-resource languages._

> **Outcome**: Demonstrates an evaluation flow for 1–2 low-resource languages without claiming deep linguistics expertise.  
> Includes a curated (synthetic) mini-corpus, annotation guidelines, adversarial set, a policy→test pipeline (YAML → eval prompts → CSV/Langfuse report), and a metrics notebook (Safety Acceptance Rate, ASR, False Refusals).

## Repo map

```
.
├── .vscode/                     # VS Code settings & recommendations
├── .devcontainer/               # Optional Dev Container
├── adversarial/                 # Jailbreak / jiggle prompts (JSONL)
├── data/                        # Curated corpora (synthetic; license + consent notes)
│   ├── ht/                      # Haitian Creole sample
│   └── yo/                      # Yoruba sample
├── docs/                        # Annotation guidelines + design notes
├── notebooks/                   # Metrics notebook
├── policies/                    # YAML safety rules & language config
├── reports/                     # Generated eval prompts and model results (CSV)
├── scripts/                     # Prompt generation + metrics computation
├── templates/                   # Prompt templates (Jinja/YAML)
├── .gitlab-ci.yml               # Minimal CI to sanity check the repo
├── LICENSE                      # Code license (MIT)
├── requirements.txt             # Python deps for scripts/notebooks
└── README.md
```

## Quickstart

1. **Set up environment**
   ```bash
   python -m venv .venv && source .venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Generate evaluation prompts** from YAML policies + templates:
   ```bash
   python scripts/gen_prompts.py --out reports/eval_prompts.csv
   ```

3. **(Optional) Run a model** and write a results CSV to `reports/eval_results.csv`  
   Use `scripts/run_eval_stub.py` as a template to connect your model or API.

4. **Compute metrics** (Safety Acceptance Rate, ASR, False Refusal Rate):
   ```bash
   python scripts/compute_metrics.py --results reports/sample_eval_results.csv
   ```

5. **Open the notebook** for graphs and a more exploratory view:
   - `notebooks/metrics.ipynb`

## Metrics definitions (repo-standard)

- **ASR (Attack Success Rate)**: % of **harmful** prompts for which the model **complied** (i.e., did _not_ refuse). Lower is better.
- **Safety Acceptance Rate (SAR)**: % of **harmless** prompts for which the model **answered** (i.e., did _not_ refuse). Higher is better.
- **False Refusal Rate (FRR)**: % of **harmless** prompts for which the model **refused**. Lower is better.
- **(Optional) Strict Refusal Precision/Recall**: if you label refusals explicitly.

See `scripts/compute_metrics.py` for exact formulas & the notebook for visuals.

## Language scope (initial)

- **Haitian Creole** (`ht`)
- **Yorùbá** (`yo`)

> All data in `data/` is **synthetic** and released under **CC0**; see `data/README.md` for consent & license notes.

## Policy → Test pipeline

- Safety categories and rules live in `policies/safety_rules.yaml`.
- Prompt templates live in `templates/`.
- `scripts/gen_prompts.py` composes category rules, language config, and templates into a CSV of evaluation prompts.  
  If `LANGFUSE_PUBLIC_KEY`/`LANGFUSE_SECRET_KEY` are set, the script can emit an ingest-ready CSV for Langfuse.

## Contributing & scope note

This repo is a **product-thinking demo**. It is not a linguistics benchmark.  
Contributions that add **transparent data provenance**, **cultural notes**, and **clearer metrics** are welcome.
