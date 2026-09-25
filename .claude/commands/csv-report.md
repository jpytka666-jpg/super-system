---
description: Run the CSV dedupe + Markdown summary pipeline and show proof it worked
allowed-tools: Bash(examples/automation/csv-report-pipeline/run.sh:*), Bash(python3 -m unittest:*), Read
---

Run the CSV report pipeline in `examples/automation/csv-report-pipeline/`.

1. If `$ARGUMENTS` is `demo`, run `examples/automation/csv-report-pipeline/run.sh --demo`;
   otherwise run `examples/automation/csv-report-pipeline/run.sh $ARGUMENTS`.
2. Read the newest `output/reports/summary_*.md` in the workspace that was used and show it.
3. Report the validator line (`VALIDATION PASS` / `VALIDATION FAIL`) verbatim.
   Never claim success without that line in the tool output.

Do not modify `pipeline.py`, `validate.py` or `sample_data/` while running this command.
