# Phase 2 audit — four-point quality sign-off

**Auditor:** Suhas GS (independent checks, read-only on generator)  
**Run timestamp (UTC):** 2026-11-17 (see `phase2_audit_results.json` → `run_at`)  
**Artifacts audited:** `tracker_clean_seed1.xlsx`, `tracker_broken_seed1.xlsx`, `injection_log_seed1.csv`, `build_tracker.py` CONFIG vs `injection_spec.md`  
**Pre-rebuild backup:** `phase2_backup/` (SHA-256 recorded below)  
**Re-runnable evidence:** `python phase2_audit_run.py` → writes `phase2_audit_results.json`

## Executive verdict

| Four-point requirement | Verdict |
|------------------------|---------|
| 1. Clean control + twelve audit checks on clean | **PARTIAL** — structural checks **PASS**; official AUDIT sheet **BLOCKED** |
| 2. Injection log (40 defects, ground truth) | **PASS** |
| 3. Reproducibility | **PASS** (log byte-identical; workbook **data** equivalent) |
| 4. CONFIG ↔ `injection_spec.md` | **PASS** |

**Phase 2 fully passed:** **No** — criterion **1** remains **BLOCKED** until `TRACKER_AUDIT_12CHECKS.xlsx` AUDIT tab has live formulas and clean file returns zero on all twelve checks.

**`injection_spec.md` sign-off:** **Not appended** (per Phase 2 instructions).

**`build_tracker.py`:** **Not modified** during this audit.

---

## Backup before controlled rebuild

| File | SHA-256 |
|------|---------|
| `injection_log_seed1.csv` | `4c48b998aa210cca3a415e4889341b3492c0ba6d2e29a8b62dbf57a228f47b7c` |
| `tracker_clean_seed1.xlsx` | `168b7105390a4c43d717e8f299f841aa23d5d0f0215e2f1037ed9ae93254c9de` |
| `tracker_broken_seed1.xlsx` | `7e7b8231f68249b14d82404301a4df657bd59b42c6e25f184dd7c90b42984d0c` |
| `summary_output.txt` | `c91b723968f24f3fee7b68af311f2a2c360febdd5f4e50fc69624bc04ccbd5ef` |

---

## 1. Clean control validation

### 1a. Structural / integrity (no audit workbook)

| Test | Expected | Actual | Status | Evidence |
|------|----------|--------|--------|----------|
| Data row count | 2000 | 2000 | **PASS** | `pd.read_excel` |
| Column count | 14 | 14 | **PASS** | Column list matches `COLUMNS` in `build_tracker.py` |
| FeeCollected ≤ FeeBilled | 0 violations | 0 violations | **PASS** | All 2000 rows |
| MatterID format `M-2026-#####` | all valid | all valid | **PASS** | Regex |
| Dates ISO on clean | all ISO | all ISO | **PASS** | No `MM/DD/YYYY` in clean |
| OpenDate range | 2025-01-01 … 2026-10-31 | 2025-01-01 … 2026-10-31 | **PASS** | Min/max |
| ClientType | Individual, Entity only | OK | **PASS** | |
| MatterType / Status / Owner | Spec enums | OK | **PASS** | |
| InvoiceCount | 1–4 | 1–4 | **PASS** | |
| Required fields non-blank | 0 blanks | 0 blanks | **PASS** | MatterID, ClientName, OpenDate, FeeBilled |
| Matches seed-regenerated base | DataFrame equal | equal | **PASS** | `generate_base_rows(20261120)` vs on-disk clean (Notes `fillna`, floats rounded) |

**Conclusion:** Clean file meets generator and `injection_spec.md` structural requirements. No evidence of injected defects in the clean copy.

### 1b. Twelve audit checks on clean (`TRACKER_AUDIT_12CHECKS.xlsx`)

| Test | Expected | Actual | Status | Evidence |
|------|----------|--------|--------|----------|
| AUDIT tab checks 1–12 on clean data pasted into DATA | Count = 0, PASS/FLAG = zero flags | All 12 rows: Count = `STUB`, verdict = `STUB` | **BLOCKED** | Teammate workbook; **not modified** |

**Conclusion:** Cannot certify “all twelve checks return zero on clean” via the published audit sheet until G M Shashank Showrya ships formulas.

### 1c. Supplementary heuristics (not a substitute for AUDIT tab)

Independent checks aligned with check *intent* on `tracker_clean_seed1.xlsx`:

| Heuristic | Expected | Actual | Status |
|-----------|----------|--------|--------|
| Text-like amounts (I, J) | 0 | 0 | **PASS** |
| Untrimmed ClientName / Status | 0 | 0 | **PASS** |
| US-format dates | 0 | 0 | **PASS** |
| Duplicate MatterID | 0 | 0 | **PASS** |
| TOTAL MatterID row | 0 | 0 | **PASS** |
| Merged cells / hidden rows | 0 / 0 | 0 / 0 | **PASS** |

*These supplement structural validation only; they do not clear the BLOCKED audit-sheet criterion.*

---

## 2. Injection log validation

| Test | Expected | Actual | Status | Evidence |
|------|----------|--------|--------|----------|
| Broken data rows | 2007 | 2007 | **PASS** | `tracker_broken_seed1.xlsx` |
| Log defect rows | 40 | 40 | **PASS** | `injection_log_seed1.csv` |
| Log columns | 5 required fields | match | **PASS** | |
| Per-class counts vs CONFIG / spec | 12 classes match table | all match | **PASS** | See class histogram in `phase2_audit_results.json` |
| Duplicate (row, column, class) keys | 0 | 0 | **PASS** | |
| Log vs broken workbook | 40/40 consistent | 0 issues | **PASS** | openpyxl cell read + clean original for base rows |
| Numbers-as-text split | FeeBilled 4, PolicyAmount 2 | 4 / 2 | **PASS** | `injection_spec.md` check 1 notes |

**Conclusion:** Ground-truth log matches CONFIG, spec counts, and broken workbook locations/values.

---

## 3. Reproducibility validation

Procedure: compare `phase2_backup/` → run `python build_tracker.py` → compare outputs.

| Test | Expected | Actual | Status | Evidence |
|------|----------|--------|--------|----------|
| `injection_log_seed1.csv` byte-identical | SHA-256 match | match | **PASS** | `4c48b998…f47b7c` before and after |
| Workbook **data** after rebuild | clean & broken DataFrames equal | clean=True, broken=True | **PASS** | `pd.read_excel` + `fillna` |
| XLSX file bytes (informational) | may differ | ZIP metadata differs | **PASS** (informational) | Not required by spec; cell data still matches |

**Conclusion:** Meets reproducibility requirement for injection log and dataset content.

---

## 4. Specification consistency

| Test | Expected | Actual | Status |
|------|----------|--------|--------|
| CONFIG vs `injection_spec.md` (12 classes) | identical counts | match | **PASS** |
| Total injections | 40 | 40 | **PASS** |
| Seed | 20261120 | 20261120 | **PASS** |
| Row arithmetic | 2000 + 4 variants + 3 appended = 2007 | CONFIG confirms | **PASS** |
| Synthetic / illustrative labeling in spec | stated | present | **PASS** | `injection_spec.md` § illustrative data |

---

## Blockers and next actions

1. **BLOCKED:** Paste `tracker_clean_seed1.xlsx` into AUDIT workbook DATA tab (or wire pipeline) and run Shashank’s twelve formulas; expect **0** on all checks for clean control.
2. After AUDIT tab is live, re-run `python phase2_audit_run.py` and update this file; then **Phase 2 can close** and `injection_spec.md` sign-off may proceed.
3. **Phase 3** (gap / chart B) — **not started**; awaiting your approval.

---

## Files touched in Phase 2 audit

| File | Role |
|------|------|
| `PHASE2_AUDIT.md` | This report |
| `phase2_audit_run.py` | Read-only audit runner |
| `phase2_audit_results.json` | Machine-readable test results |
| `phase2_backup/` | Pre-rebuild artifact copies |

**Not modified:** `build_tracker.py`, `TRACKER_AUDIT_12CHECKS.xlsx`, teammates’ other deliverables.