#!/usr/bin/env python3
"""CSV report pipeline: collect -> deduplicate -> summarize.

Trigger:   CSV files dropped into <base>/input/
Processor: whitespace normalization + exact-row deduplication
           (within a file and across files sharing the same header)
Output:    <base>/output/clean/*.csv          cleaned copies
           <base>/output/reports/summary_*.md Markdown summary
           <base>/output/reports/manifest_*.json checksums + stats
           <base>/input/processed/<run_id>/   archived originals (never deleted)

Standard library only. Run `python pipeline.py --help` for options.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import shutil
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

MAX_ITERATIONS = 15  # hard cap for --watch mode (cost/loop safety net)


class PipelineError(Exception):
    """Raised when the pipeline cannot run safely."""


@dataclass
class FileResult:
    """Statistics for one processed input file."""

    name: str
    sha256_in: str
    rows_in: int
    rows_out: int
    duplicates_in_file: int
    duplicates_cross_file: int
    columns: list[str]
    output: str = ""
    sha256_out: str = ""
    error: str = ""


@dataclass
class RunResult:
    """Aggregate statistics for one pipeline run."""

    run_id: str
    started_at: str
    files: list[FileResult] = field(default_factory=list)
    skipped: list[str] = field(default_factory=list)

    @property
    def total_in(self) -> int:
        return sum(f.rows_in for f in self.files)

    @property
    def total_out(self) -> int:
        return sum(f.rows_out for f in self.files)


def sha256_of(path: Path) -> str:
    """Return the hex sha256 digest of a file."""
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def ensure_inside(base: Path, target: Path) -> Path:
    """Resolve target and refuse anything that escapes base."""
    resolved = target.resolve()
    if resolved != base and base not in resolved.parents:
        raise PipelineError(f"refusing to touch path outside base dir: {resolved}")
    return resolved


def normalize(row: list[str]) -> tuple[str, ...]:
    """Trim whitespace and collapse internal runs of spaces in every cell."""
    return tuple(" ".join(cell.split()) for cell in row)


def process_file(
    path: Path, clean_dir: Path, seen_by_header: dict[tuple[str, ...], set[tuple[str, ...]]]
) -> FileResult:
    """Deduplicate one CSV file and write its cleaned copy."""
    with path.open(newline="", encoding="utf-8-sig") as handle:
        rows = list(csv.reader(handle))
    if not rows:
        return FileResult(path.name, sha256_of(path), 0, 0, 0, 0, [], error="empty file")

    header = normalize(rows[0])
    seen_global = seen_by_header.setdefault(header, set())
    seen_local: set[tuple[str, ...]] = set()
    kept: list[tuple[str, ...]] = []
    dup_local = dup_cross = rows_in = 0

    for raw in rows[1:]:
        row = normalize(raw)
        if not any(row):
            continue  # blank line, not counted as data
        rows_in += 1
        if row in seen_local:
            dup_local += 1
            continue
        seen_local.add(row)
        if row in seen_global:
            dup_cross += 1
            continue
        seen_global.add(row)
        kept.append(row)

    out_path = clean_dir / f"{path.stem}_clean.csv"
    with out_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(kept)

    return FileResult(
        name=path.name,
        sha256_in=sha256_of(path),
        rows_in=rows_in,
        rows_out=len(kept),
        duplicates_in_file=dup_local,
        duplicates_cross_file=dup_cross,
        columns=list(header),
        output=out_path.name,
        sha256_out=sha256_of(out_path),
    )


def render_markdown(result: RunResult) -> str:
    """Render the run summary as Markdown."""
    removed = result.total_in - result.total_out
    ratio = (removed / result.total_in * 100) if result.total_in else 0.0
    lines = [
        f"# CSV Report Summary - {result.run_id}",
        "",
        f"- Started: {result.started_at}",
        f"- Files processed: {len(result.files)}",
        f"- Files skipped: {len(result.skipped)}",
        f"- Rows in: {result.total_in}",
        f"- Rows out: {result.total_out}",
        f"- Duplicates removed: {removed} ({ratio:.1f}%)",
        "",
        "## Files",
        "",
        "| File | Rows in | Rows out | Dup (file) | Dup (cross) | Columns | Status |",
        "|---|---:|---:|---:|---:|---:|---|",
    ]
    for f in result.files:
        status = f"ERROR: {f.error}" if f.error else "ok"
        lines.append(
            f"| {f.name} | {f.rows_in} | {f.rows_out} | {f.duplicates_in_file} "
            f"| {f.duplicates_cross_file} | {len(f.columns)} | {status} |"
        )
    if result.skipped:
        lines += ["", "## Skipped", ""] + [f"- {s}" for s in result.skipped]
    lines += ["", "## Checksums (sha256)", ""]
    for f in result.files:
        lines.append(f"- `{f.name}` in: `{f.sha256_in[:16]}` out: `{f.sha256_out[:16]}`")
    return "\n".join(lines) + "\n"


def run_once(base: Path, archive: bool = True) -> RunResult | None:
    """Process every CSV currently in <base>/input. Returns None when idle."""
    base = base.resolve()
    input_dir = ensure_inside(base, base / "input")
    clean_dir = ensure_inside(base, base / "output" / "clean")
    report_dir = ensure_inside(base, base / "output" / "reports")
    for d in (input_dir, clean_dir, report_dir):
        d.mkdir(parents=True, exist_ok=True)

    candidates = sorted(p for p in input_dir.iterdir() if p.suffix.lower() == ".csv")
    if not candidates:
        return None

    now = datetime.now(timezone.utc)
    result = RunResult(run_id=now.strftime("%Y%m%dT%H%M%S%fZ"), started_at=now.isoformat())
    seen_by_header: dict[tuple[str, ...], set[tuple[str, ...]]] = {}

    for path in candidates:
        if path.is_symlink() or not path.is_file():
            result.skipped.append(f"{path.name}: not a regular file")
            continue
        try:
            result.files.append(process_file(path, clean_dir, seen_by_header))
        except (UnicodeDecodeError, csv.Error) as exc:
            result.skipped.append(f"{path.name}: {type(exc).__name__}: {exc}")

    md_path = report_dir / f"summary_{result.run_id}.md"
    md_path.write_text(render_markdown(result), encoding="utf-8")
    manifest = {
        "run_id": result.run_id,
        "started_at": result.started_at,
        "totals": {"rows_in": result.total_in, "rows_out": result.total_out},
        "files": [asdict(f) for f in result.files],
        "skipped": result.skipped,
        "summary": md_path.name,
    }
    (report_dir / f"manifest_{result.run_id}.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8"
    )

    if archive:
        dest = ensure_inside(base, input_dir / "processed" / result.run_id)
        dest.mkdir(parents=True, exist_ok=True)
        for path in candidates:
            if path.is_file() and not path.is_symlink():
                checksum = sha256_of(path)
                moved = Path(shutil.move(str(path), dest / path.name))
                if sha256_of(moved) != checksum:
                    raise PipelineError(f"checksum mismatch after archiving {path.name}")
    return result


def main(argv: list[str] | None = None) -> int:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--base", type=Path, default=Path(__file__).parent / "workspace",
                        help="working directory holding input/ and output/")
    parser.add_argument("--watch", action="store_true", help="poll input/ repeatedly")
    parser.add_argument("--interval", type=float, default=5.0, help="seconds between polls")
    parser.add_argument("--iterations", type=int, default=MAX_ITERATIONS,
                        help=f"max polls in watch mode (capped at {MAX_ITERATIONS})")
    parser.add_argument("--no-archive", action="store_true",
                        help="leave originals in input/ (re-processed next run)")
    args = parser.parse_args(argv)

    iterations = min(max(args.iterations, 1), MAX_ITERATIONS) if args.watch else 1
    for i in range(1, iterations + 1):
        result = run_once(args.base, archive=not args.no_archive)
        if result is None:
            print(f"[{i}/{iterations}] idle: no CSV files in {args.base / 'input'}")
        else:
            print(f"[{i}/{iterations}] run {result.run_id}: {len(result.files)} files, "
                  f"{result.total_in} rows in -> {result.total_out} rows out, "
                  f"{len(result.skipped)} skipped")
            print(f"  summary: {args.base / 'output' / 'reports' / f'summary_{result.run_id}.md'}")
        if i < iterations:
            time.sleep(args.interval)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except PipelineError as exc:
        print(f"pipeline error: {exc}", file=sys.stderr)
        sys.exit(2)
