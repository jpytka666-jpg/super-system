#!/usr/bin/env bash
# Trigger wrapper: run pipeline, then validator. Exit code = validator result.
# Usage:
#   ./run.sh                 process workspace/input once
#   ./run.sh --demo          copy sample_data into a fresh demo workspace first
#   ./run.sh --watch         poll up to 15 times (extra args pass to pipeline.py)
# Cron example (every hour at :07):
#   7 * * * * /path/to/run.sh >> /path/to/workspace/pipeline.log 2>&1
set -euo pipefail
HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE="${CSV_PIPELINE_BASE:-$HERE/workspace}"
PY="${PYTHON:-python3}"

if [[ "${1:-}" == "--demo" ]]; then
  shift
  BASE="$HERE/workspace-demo"
  rm -rf "$BASE"
  mkdir -p "$BASE/input"
  cp "$HERE"/sample_data/*.csv "$BASE/input/"
  echo "demo workspace prepared at $BASE"
fi

echo "== pipeline $(date -u +%FT%TZ)"
"$PY" "$HERE/pipeline.py" --base "$BASE" "$@"
echo "== validation"
if ls "$BASE"/output/reports/manifest_*.json >/dev/null 2>&1; then
  "$PY" "$HERE/validate.py" --base "$BASE"
else
  echo "nothing processed yet; validation skipped"
fi
