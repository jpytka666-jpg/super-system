# CSV Report Pipeline

Collect CSV reports from an input folder, remove duplicate rows, and write a
Markdown summary. Uses only the Python 3.9+ standard library.

## Architecture

```
trigger                 processor                          output
-------                 ---------                          ------
run.sh (manual/cron) -> pipeline.py                     -> output/clean/<name>_clean.csv
run.sh --watch          1. list input/*.csv                output/reports/summary_<run>.md
/csv-report command     2. normalize whitespace            output/reports/manifest_<run>.json
                        3. drop exact duplicates           input/processed/<run>/  (originals)
                           - within a file
                           - across files with same header
                        4. write summary + sha256 manifest
                        5. archive originals (checksum-verified move)
                     -> validate.py  (Show Proof: PASS/FAIL, exit code)
```

## Constraints (what it will not do)

- Writes only inside its base directory (`workspace/` by default, or `--base`);
  any path that resolves outside it raises an error.
- Never deletes input files. It moves them to `input/processed/<run_id>/` and
  verifies the sha256 checksum after the move.
- Skips symlinks and non-regular files. It does not follow them.
- `--watch` mode is capped at 15 polls (`MAX_ITERATIONS`), whatever value `--iterations` is given.
- Never edits `sample_data/` or the pipeline's own code.

## Usage

```bash
./run.sh --demo                      # fresh demo workspace from sample_data, then validate
./run.sh                             # process workspace/input once
./run.sh --watch --interval 60       # poll up to 15 times
CSV_PIPELINE_BASE=/data/reports ./run.sh
python3 -m unittest discover -s tests -v
```

In Claude Code, run `/csv-report demo` from the repo root.

## Deduplication rules

- Cells are trimmed and internal whitespace is collapsed before comparison
  (`" South "` equals `"South"`).
- Blank lines are ignored and not counted.
- The first occurrence is kept. Later copies count as either `Dup (file)` or
  `Dup (cross)`, depending on where the earlier copy was.
- Files are processed in filename order, so name reports sortably
  (e.g. `sales_2026-01.csv`) to keep the earliest copy of a row.
- Cross-file dedupe applies only to files whose headers match after
  normalization.
