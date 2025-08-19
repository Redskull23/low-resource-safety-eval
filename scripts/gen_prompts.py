#!/usr/bin/env python3
import csv, json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
rows = []
for lang_dir in sorted([p for p in (ROOT/'data').iterdir() if p.is_dir()]):
    code = lang_dir.name
    for i, line in enumerate([l for l in (lang_dir/'corpus.txt').read_text(encoding='utf-8').splitlines() if l and not l.startswith('#')], 1):
        rows.append({'id': f'safe_{code}_{i:02d}','lang':code,'category':'benign','attack_type':'','prompt':line})
(out:=ROOT/'reports'/'eval_prompts.csv').parent.mkdir(parents=True, exist_ok=True)
with open(out,'w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f, fieldnames=['id','lang','category','attack_type','prompt']); w.writeheader(); w.writerows(rows)
print(f'Wrote {len(rows)} prompts to {out}')
