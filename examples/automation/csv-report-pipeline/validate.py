#!/usr/bin/env python3
"""Show-Proof validator: checks that the latest pipeline run produced a
well-formed Markdown summary, a consistent manifest, and cleaned CSVs whose
checksums match. Exit 0 = PASS, 1 = FAIL."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import sys
from pathlib import Path

REQUIRED_MD = ["# CSV Report Summary - ", "- Rows in: ", "- Rows out: ",
               "- Duplicates removed: ", "## Files", "| File | Rows in |",
               "## Checksums (sha256)"]


def check(base: Path) -> list[str]:
    """Return a list of problems; empty list means the run is valid."""
    reports = base / "output" / "reports"
    manifests = sorted(reports.glob("manifest_*.json"))
    if not manifests:
        return [f"no manifest found in {reports}"]
    manifest = json.loads(manifests[-1].read_text(encoding="utf-8"))
    problems: list[str] = []

    md_path = reports / manifest["summary"]
    if not md_path.is_file():
        return [f"summary missing: {md_path}"]
    md = md_path.read_text(encoding="utf-8")
    problems += [f"summary lacks section {s!r}" for s in REQUIRED_MD if s not in md]

    rows_out = 0
    for entry in manifest["files"]:
        if entry["error"]:
            continue
        out = base / "output" / "clean" / entry["output"]
        if not out.is_file():
            problems.append(f"clean file missing: {out.name}")
            continue
        if hashlib.sha256(out.read_bytes()).hexdigest() != entry["sha256_out"]:
            problems.append(f"checksum mismatch: {out.name}")
        with out.open(newline="", encoding="utf-8") as handle:
            data = list(csv.reader(handle))[1:]
        if len(data) != len(set(map(tuple, data))):
            problems.append(f"duplicates remain in {out.name}")
        if len(data) != entry["rows_out"]:
            problems.append(f"row count {len(data)} != manifest {entry['rows_out']} for {out.name}")
        if f"| {entry['name']} |" not in md:
            problems.append(f"{entry['name']} not listed in summary")
        rows_out += len(data)

    if rows_out != manifest["totals"]["rows_out"]:
        problems.append(f"total rows_out {rows_out} != manifest {manifest['totals']['rows_out']}")
    return problems


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", type=Path, default=Path(__file__).parent / "workspace")
    args = parser.parse_args()
    problems = check(args.base.resolve())
    if problems:
        print("VALIDATION FAIL")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("VALIDATION PASS: summary, manifest, checksums and dedupe all consistent")
    return 0


if __name__ == "__main__":
    sys.exit(main())
