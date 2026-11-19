# tracker-audit-12-checks

A free **twelve-check audit sheet** for a hand-kept client or matter tracker, plus the script that builds a deliberately broken **illustrative** test file and the article that explains it.

**Illustrative data:** The bundled tracker is synthetic, not a client file. All **40** defects were injected by script (seed **20261120**). Counts describe **this file only**, not a rate in real businesses.

## What this is

- **`TRACKER_AUDIT_12CHECKS.xlsx`** — paste your tracker into **DATA**, read flags on **AUDIT**, start on **START HERE**.
- **`build_tracker.py`** — rebuilds clean/broken XLSX files, logs, gap file, and `summary_output.txt`.
- Charts and article assets for the Beagle LinkedIn publish package.

## Requirements

- Python **3.11**
- Excel **2019** or Google **Sheets** (for the audit workbook)
- See `requirements.txt`

## Install

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
bash run_all.sh
```

Until `build_tracker.py` is fully implemented, `run_all.sh` stops with **STUB NOT IMPLEMENTED: build_tracker** after writing stub data files.

## Expected output

After a full generator run (Suhas):

- `tracker_clean_seed1.xlsx`, `tracker_broken_seed1.xlsx`
- `injection_log_seed1.csv` (40 data rows + header)
- `gap_by_class.csv`, `summary_output.txt`
- `chart_a.png`, `chart_b.png`

## Illustrative data label

Numbers in the article must match `summary_output.txt`. The audit sheet recommends **no purchase**—fixes use built-in Excel/Sheets tools only.