"""
Simple script to download openFDA label records for given brand names and store them as JSON docs for indexing.
Usage:
    python scripts/ingest_openfda.py --drugs aspirin ibuprofen --outdir data/labels
"""
import argparse
import requests
import os
import json
from pathlib import Path

API = "https://api.fda.gov/drug/label.json"

FIELD_KEYS = [
    "openfda", "purpose", "indications_and_usage", "dosage_and_administration", "warnings", "adverse_reactions"
]


def fetch_labels_for(drug: str, limit: int = 5):
    q = f"openfda.brand_name:{drug}"
    url = f"{API}?search={q}&limit={limit}"
    r = requests.get(url)
    if r.status_code != 200:
        print(f"Warning: failed to fetch {drug} -> status {r.status_code}")
        return []
    j = r.json()
    return j.get("results", [])


def summarize_label(rec: dict) -> dict:
    pieces = []
    for k in ["indications_and_usage", "dosage_and_administration", "purpose", "warnings", "adverse_reactions"]:
        v = rec.get(k)
        if v:
            if isinstance(v, list):
                pieces.append(f"{k}: \n" + "\n".join(v))
            else:
                pieces.append(f"{k}: \n{v}")
    text = "\n\n".join(pieces)
    return {
        "drug_name": ",".join(rec.get("openfda", {}).get("brand_name", [])) or rec.get("id", "unknown"),
        "text": text,
        "raw": rec
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--drugs", nargs="+", required=True)
    parser.add_argument("--outdir", default="data/labels")
    args = parser.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    for d in args.drugs:
        recs = fetch_labels_for(d)
        if not recs:
            print(f"No records for {d}")
            continue
        for i, r in enumerate(recs):
            s = summarize_label(r)
            fname = outdir / f"{d.replace(' ','_')}_{i}.json"
            with open(fname, "w", encoding="utf-8") as f:
                json.dump(s, f, ensure_ascii=False, indent=2)
            print(f"Wrote {fname}")

    print("Ingestion done. Run your app to let the retriever pick up new files (or call retriever.rebuild()).")

if __name__ == "__main__":
    main()
