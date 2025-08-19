#!/usr/bin/env python3
"""
Generate evaluation prompts CSV.

- Scans data/<lang>/corpus.txt for BENIGN prompts (one per line).
- Optionally appends UNSAFE prompts from templates/prompt_templates.yaml (unsafe_templates).
- Optionally appends ADVERSARIAL prompts from adversarial/prompts.jsonl.
- Writes reports/eval_prompts.csv (default) with columns:
  id,lang,category,attack_type,prompt
"""

import argparse
import csv
import json
from pathlib import Path
from typing import Dict, List

try:
    import yaml  # optional; only needed if templates YAML exists
except Exception:
    yaml = None  # we'll handle absence gracefully

ROOT = Path(__file__).resolve().parents[1]


def read_corpora() -> List[Dict]:
    """Read benign prompts from data/*/corpus.txt."""
    rows = []
    data_dir = ROOT / "data"
    if not data_dir.exists():
        print("[warn] data/ directory not found; skipping corpora.")
        return rows

    lang_dirs = sorted([p for p in data_dir.iterdir() if p.is_dir()])
    for lang_dir in lang_dirs:
        code = lang_dir.name
        corpus_path = lang_dir / "corpus.txt"
        if not corpus_path.exists():
            print(f"[warn] missing {corpus_path}, skipping language '{code}'.")
            continue

        lines = corpus_path.read_text(encoding="utf-8").splitlines()
        # strip, skip blanks and comments (allow leading whitespace before '#')
        clean_lines = [
            ln.strip()
            for ln in lines
            if ln.strip() and not ln.lstrip().startswith("#")
        ]
        for i, line in enumerate(clean_lines, 1):
            rows.append(
                {
                    "id": f"safe_{code}_{i:02d}",
                    "lang": code,
                    "category": "benign",
                    "attack_type": "",
                    "prompt": line,
                }
            )
    return rows


def read_templates_unsafe() -> List[Dict]:
    """
    Read UNSAFE templates from templates/prompt_templates.yaml.
    Only the 'unsafe_templates' section is used to avoid unresolved vars in safe templates.
    """
    rows = []
    tmpl_path = ROOT / "templates" / "prompt_templates.yaml"
    if not tmpl_path.exists():
        return rows
    if yaml is None:
        print("[warn] PyYAML not installed; skipping templates.")
        return rows

    data = yaml.safe_load(tmpl_path.read_text(encoding="utf-8")) or {}
    for t in data.get("unsafe_templates", []) or []:
        text = (t.get("text") or "").strip()
        cat = t.get("category") or "general_safety"
        _id = t.get("id") or f"unsafe_{cat}"
        if not text:
            continue
        rows.append(
            {
                "id": _id,
                "lang": "mixed",
                "category": cat,
                "attack_type": "template",
                "prompt": text,
            }
        )
    return rows


def read_adversarial() -> List[Dict]:
    """Read adversarial JSONL rows from adversarial/prompts.jsonl."""
    rows = []
    adv_path = ROOT / "adversarial" / "prompts.jsonl"
    if not adv_path.exists():
        return rows

    for ln in adv_path.read_text(encoding="utf-8").splitlines():
        if not ln.strip():
            continue
        obj = json.loads(ln)
        rows.append(
            {
                "id": obj.get("id"),
                "lang": obj.get("lang", "mixed"),
                "category": obj.get("category", "general_safety"),
                "attack_type": obj.get("attack_type", "adversarial"),
                "prompt": obj.get("prompt", "").strip(),
            }
        )
    return rows


def ensure_unique_ids(rows: List[Dict]) -> List[Dict]:
    """De-duplicate IDs by appending a numeric suffix if needed."""
    seen = {}
    out = []
    for r in rows:
        base = r["id"] or "item"
        if base not in seen:
            seen[base] = 0
            r["id"] = base
        else:
            seen[base] += 1
            r["id"] = f"{base}__{seen[base]}"
        out.append(r)
    return out


def summarize(rows: List[Dict]) -> None:
    from collections import Counter

    by_lang = Counter(r["lang"] for r in rows)
    by_cat = Counter(r["category"] for r in rows)
    print(f"[info] total rows: {len(rows)}")
    print(f"[info] by language: {dict(sorted(by_lang.items()))}")
    print(f"[info] by category: {dict(sorted(by_cat.items()))}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--out",
        type=Path,
        default=ROOT / "reports" / "eval_prompts.csv",
        help="Output CSV path",
    )
    ap.add_argument(
        "--no-templates",
        action="store_true",
        help="Do not include unsafe templates from templates/prompt_templates.yaml",
    )
    ap.add_argument(
        "--no-adversarial",
        action="store_true",
        help="Do not include adversarial/prompts.jsonl",
    )
    args = ap.parse_args()

    rows: List[Dict] = []
    rows += read_corpora()
    if not args.no_templates:
        rows += read_templates_unsafe()
    if not args.no_adversarial:
        rows += read_adversarial()

    # Clean & de-dup
    rows = [r for r in rows if r.get("prompt")]
    rows = ensure_unique_ids(rows)

    # Ensure output dir
    args.out.parent.mkdir(parents=True, exist_ok=True)

    # Write CSV
    fieldnames = ["id", "lang", "category", "attack_type", "prompt"]
    with open(args.out, "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in rows:
            w.writerow({k: r.get(k, "") for k in fieldnames})

    summarize(rows)
    print(f"Wrote {len(rows)} prompts to {args.out}")


if __name__ == "__main__":
    main()
