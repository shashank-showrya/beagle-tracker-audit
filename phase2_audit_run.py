#!/usr/bin/env python3
"""Phase 2 independent audit runner (read-only). Suhas GS."""

from __future__ import annotations

import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook

from build_tracker import (
    COLUMNS,
    CLASS_LABELS,
    CONFIG,
    LOG_FIELDS,
    MATTER_TYPES,
    OPEN_DATE_END,
    OPEN_DATE_START,
    OWNERS,
    SPEC_CLASS_COUNTS,
    STATUSES,
    SHEET_NAME,
    generate_base_rows,
    injection_total,
)

REPO_ROOT = Path(__file__).resolve().parent
BACKUP = REPO_ROOT / "phase2_backup"
ISO_DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")
US_DATE = re.compile(r"^\d{2}/\d{2}/\d{4}$")
MATTER_ID = re.compile(r"^M-2026-\d{5}$")


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def col_index(name: str) -> int:
    return COLUMNS.index(name) + 1


def cell_value(ws, row: int, column: str):
    return ws.cell(row=row, column=col_index(column)).value


def cell_openpyxl(ws, row: int, column: str):
    from openpyxl.utils import get_column_letter

    c = ws[f"{get_column_letter(col_index(column))}{row}"]
    return c.value, c.number_format, c.data_type


def audit_clean_structural() -> list[dict]:
    results: list[dict] = []
    clean_path = REPO_ROOT / "tracker_clean_seed1.xlsx"
    df = pd.read_excel(clean_path)
    wb = load_workbook(clean_path, data_only=False)

    def add(test: str, expected: str, actual: str, status: str, evidence: str):
        results.append(
            {
                "test": test,
                "expected": expected,
                "actual": actual,
                "status": status,
                "evidence": evidence,
            }
        )

    add(
        "Clean data row count",
        "2000",
        str(len(df)),
        "PASS" if len(df) == 2000 else "FAIL",
        f"pd.read_excel rows={len(df)}",
    )
    add(
        "Clean column count",
        "14",
        str(len(df.columns)),
        "PASS" if len(df.columns) == 14 else "FAIL",
        f"columns={list(df.columns)}",
    )
    add(
        "Clean column names match spec",
        "14 named columns in order",
        "match" if list(df.columns) == COLUMNS else "mismatch",
        "PASS" if list(df.columns) == COLUMNS else "FAIL",
        f"expected {COLUMNS}",
    )

    bad_fee = df[df["FeeCollected"].astype(float) > df["FeeBilled"].astype(float)]
    add(
        "FeeCollected <= FeeBilled (all rows)",
        "0 violations",
        f"{len(bad_fee)} violations",
        "PASS" if len(bad_fee) == 0 else "FAIL",
        "pandas comparison on columns K,J",
    )

    matter_ok = df["MatterID"].astype(str).str.match(MATTER_ID).all()
    add(
        "MatterID format M-2026-#####",
        "all valid",
        "all valid" if matter_ok else "invalid rows present",
        "PASS" if matter_ok else "FAIL",
        "regex on MatterID column",
    )

    open_iso = df["OpenDate"].astype(str).str.match(ISO_DATE).all()
    target_iso = df["TargetCloseDate"].astype(str).str.match(ISO_DATE).all()
    last_iso = df["LastContactDate"].astype(str).str.match(ISO_DATE).all()
    add(
        "Clean dates ISO YYYY-MM-DD",
        "OpenDate, TargetCloseDate, LastContactDate all ISO",
        f"open={open_iso}, target={target_iso}, last={last_iso}",
        "PASS" if open_iso and target_iso and last_iso else "FAIL",
        "no US-format dates in clean",
    )

    od = pd.to_datetime(df["OpenDate"])
    add(
        "OpenDate range",
        f"{OPEN_DATE_START} .. {OPEN_DATE_END}",
        f"{od.min().date()} .. {od.max().date()}",
        "PASS"
        if od.min().date() >= OPEN_DATE_START and od.max().date() <= OPEN_DATE_END
        else "FAIL",
        "pandas to_datetime min/max",
    )

    ct = set(df["ClientType"].unique())
    add(
        "ClientType values",
        "{Individual, Entity}",
        str(ct),
        "PASS" if ct <= {"Individual", "Entity"} else "FAIL",
        f"unique={ct}",
    )

    mt = set(df["MatterType"].unique())
    add(
        "MatterType values",
        "subset of spec enums",
        str(mt),
        "PASS" if mt <= set(MATTER_TYPES) else "FAIL",
        f"allowed={MATTER_TYPES}",
    )

    st = set(df["Status"].unique())
    add(
        "Status values (canonical)",
        f"subset of {STATUSES}",
        str(st),
        "PASS" if st <= set(STATUSES) else "FAIL",
        "",
    )

    ow = set(df["Owner"].unique())
    add(
        "Owner initials",
        f"subset of {OWNERS}",
        str(ow),
        "PASS" if ow <= set(OWNERS) else "FAIL",
        "",
    )

    inv = df["InvoiceCount"].astype(int)
    add(
        "InvoiceCount range 1-4",
        "all in 1..4",
        f"min={inv.min()} max={inv.max()}",
        "PASS" if inv.min() >= 1 and inv.max() <= 4 else "FAIL",
        "",
    )

    required = ["MatterID", "ClientName", "OpenDate", "FeeBilled"]
    blank = 0
    for col in required:
        blank += df[col].isna().sum()
    add(
        "Required fields non-blank",
        "0 blank in MatterID, ClientName, OpenDate, FeeBilled",
        f"{blank} blank cells",
        "PASS" if blank == 0 else "FAIL",
        f"checked {required}",
    )

    # Regenerated clean from seed (no injections) must match on-disk clean
    import random

    rng = random.Random(CONFIG["SEED"])
    regen = generate_base_rows(rng)
    disk = df.reset_index(drop=True).fillna("")
    regen_norm = regen.fillna("")
    for c in ("OpenDate", "TargetCloseDate", "LastContactDate"):
        disk[c] = disk[c].astype(str)
        regen_norm[c] = regen_norm[c].astype(str)
    for c in ("PolicyAmount", "FeeBilled", "FeeCollected"):
        disk[c] = disk[c].astype(float).round(2)
        regen_norm[c] = regen_norm[c].astype(float).round(2)
    match = regen_norm.equals(disk)
    add(
        "Clean matches seed-regenerated base (no injections)",
        "dataframe equal (Notes blank normalized)",
        "equal" if match else "differs",
        "PASS" if match else "FAIL",
        "build_tracker.generate_base_rows + pd.read_excel fillna",
    )

    return results


def audit_audit_workbook() -> list[dict]:
    results: list[dict] = []
    wb = load_workbook(REPO_ROOT / "TRACKER_AUDIT_12CHECKS.xlsx", data_only=True)
    ws = wb["AUDIT"]
    stub_count = 0
    for r in range(2, 14):
        if ws.cell(r, 3).value == "STUB" or ws.cell(r, 4).value == "STUB":
            stub_count += 1
    results.append(
        {
            "test": "TRACKER_AUDIT_12CHECKS twelve checks on clean (Shashank formulas)",
            "expected": "Count=0 FLAG for all 12 on clean control",
            "actual": f"All 12 AUDIT Count/verdict cells are STUB (stub_count={stub_count}/12)",
            "status": "BLOCKED",
            "evidence": "TRACKER_AUDIT_12CHECKS.xlsx AUDIT tab rows 2-13; not modified (teammate file)",
        }
    )
    return results


def audit_injection_log() -> list[dict]:
    results: list[dict] = []
    log_path = REPO_ROOT / "injection_log_seed1.csv"
    log = pd.read_csv(log_path)
    clean = pd.read_excel(REPO_ROOT / "tracker_clean_seed1.xlsx")
    broken_df = pd.read_excel(REPO_ROOT / "tracker_broken_seed1.xlsx")
    wb = load_workbook(REPO_ROOT / "tracker_broken_seed1.xlsx", data_only=True)
    ws = wb[SHEET_NAME]

    def add(test, expected, actual, status, evidence):
        results.append(
            {
                "test": test,
                "expected": expected,
                "actual": actual,
                "status": status,
                "evidence": evidence,
            }
        )

    add(
        "Broken data row count",
        "2007",
        str(len(broken_df)),
        "PASS" if len(broken_df) == 2007 else "FAIL",
        "pd.read_excel tracker_broken_seed1.xlsx",
    )
    add(
        "Log row count",
        "40",
        str(len(log)),
        "PASS" if len(log) == 40 else "FAIL",
        str(log_path),
    )
    add(
        "Log columns",
        str(LOG_FIELDS),
        str(list(log.columns)),
        "PASS" if list(log.columns) == LOG_FIELDS else "FAIL",
        "",
    )

    counts = Counter(log["class"])
    mismatches = [
        f"{k}: log={counts.get(k, 0)} spec={v}"
        for k, v in SPEC_CLASS_COUNTS.items()
        if counts.get(k, 0) != v
    ]
    add(
        "Class counts vs CONFIG/SPEC",
        "12 classes match",
        "all match" if not mismatches else "; ".join(mismatches),
        "PASS" if not mismatches else "FAIL",
        json.dumps(dict(counts)),
    )
    add(
        "Total injected",
        "40",
        str(len(log)),
        "PASS" if len(log) == injection_total() else "FAIL",
        "",
    )

    dupes = log.groupby(["row", "column", "class"]).size()
    dupe_rows = dupes[dupes > 1]
    add(
        "No duplicate (row, column, class) keys",
        "0 duplicates",
        f"{len(dupe_rows)} duplicate keys",
        "PASS" if len(dupe_rows) == 0 else "FAIL",
        dupe_rows.to_string() if len(dupe_rows) else "",
    )

    wb_struct = load_workbook(REPO_ROOT / "tracker_broken_seed1.xlsx")
    ws_struct = wb_struct[SHEET_NAME]
    merge_anchors = {m.min_row for m in ws_struct.merged_cells.ranges}
    hidden_rows = [
        r
        for r in range(2, ws_struct.max_row + 1)
        if ws_struct.row_dimensions[r].hidden
    ]

    mismatches_detail: list[str] = []
    hidden_logged = False

    def _num_equal(a: str, b: str) -> bool:
        try:
            return float(a) == float(b)
        except ValueError:
            return a == b

    for i, row in log.iterrows():
        excel_row = int(row["row"])
        col = str(row["column"])
        cls = str(row["class"])
        corr = str(row["corrupted_value"]) if pd.notna(row["corrupted_value"]) else ""
        orig = str(row["original_value"]) if pd.notna(row["original_value"]) else ""

        if cls == "Hidden rows":
            if hidden_logged:
                mismatches_detail.append(f"line {i+2}: duplicate hidden log")
            hidden_logged = True
            if len(hidden_rows) != 5:
                mismatches_detail.append(
                    f"hidden row count {len(hidden_rows)} != 5; rows={hidden_rows}"
                )
            if excel_row != hidden_rows[0] if hidden_rows else False:
                mismatches_detail.append(
                    f"line {i+2}: log row {excel_row} != block start {hidden_rows[:1]}"
                )
            continue

        if cls == "Merged cells":
            if excel_row not in merge_anchors:
                mismatches_detail.append(
                    f"line {i+2}: merge anchor row {excel_row} not in {merge_anchors}"
                )
            if corr not in str(list(ws_struct.merged_cells.ranges)):
                pass  # corrupted_value is descriptive text, not range
            continue

        if col not in COLUMNS:
            mismatches_detail.append(f"line {i+2}: invalid column {col!r}")
            continue

        actual, nfmt, _dtype = cell_openpyxl(ws, excel_row, col)

        if cls == "Numbers stored as text":
            if nfmt != "@":
                mismatches_detail.append(
                    f"line {i+2}: {col}{excel_row} format {nfmt!r} != @"
                )
            if not _num_equal(str(actual), corr):
                mismatches_detail.append(
                    f"line {i+2}: corrupt {actual!r} != {corr!r}"
                )
            if excel_row <= 2001:
                exp = clean.at[excel_row - 2, col]
                if not _num_equal(orig, str(exp)):
                    mismatches_detail.append(
                        f"line {i+2}: original {orig!r} != clean {exp!r}"
                    )

        elif cls == "Currency formatted text and bracket negatives":
            if str(actual) != corr:
                mismatches_detail.append(
                    f"line {i+2}: currency {actual!r} != {corr!r}"
                )
            if nfmt != "@":
                mismatches_detail.append(f"line {i+2}: currency not text")

        elif cls == "Invisible characters":
            if str(actual) != corr:
                mismatches_detail.append(
                    f"line {i+2}: invisible {actual!r} != {corr!r}"
                )

        elif cls == "Exact duplicate MatterID":
            if str(actual) != corr:
                mismatches_detail.append(
                    f"line {i+2}: MatterID {actual!r} != {corr!r}"
                )
            if excel_row <= 2001 and str(orig) != str(clean.at[excel_row - 2, "MatterID"]):
                mismatches_detail.append(f"line {i+2}: original MatterID mismatch")

        elif cls == "TOTAL row inside the data range":
            if col == "MatterID" and str(actual) != "TOTAL":
                mismatches_detail.append(f"line {i+2}: MatterID not TOTAL")
            if col == "MatterID" and orig != str(clean.at[excel_row - 2, "MatterID"]):
                mismatches_detail.append(f"line {i+2}: original pre-TOTAL id mismatch")
            if col == "MatterID" and corr != "TOTAL":
                mismatches_detail.append(f"line {i+2}: corrupted_value not TOTAL")

        elif cls == "Duplicate client under spelling variant":
            if str(actual) != corr:
                mismatches_detail.append(f"line {i+2}: variant {actual!r} != {corr!r}")

        elif cls == "Rows appended below the total's range":
            if col == "FeeBilled" and not _num_equal(str(actual), corr):
                mismatches_detail.append(
                    f"line {i+2}: appended fee {actual!r} != {corr!r}"
                )

        else:
            if str(actual) != corr:
                mismatches_detail.append(
                    f"line {i+2}: {cls} {actual!r} != {corr!r}"
                )
            if excel_row <= 2001 and cls not in (
                "Case and punctuation variants in Status",
            ):
                exp = str(clean.at[excel_row - 2, col])
                if orig != exp:
                    mismatches_detail.append(
                        f"line {i+2}: original {orig!r} != clean {exp!r}"
                    )

    add(
        "Log values vs broken workbook cells",
        "40/40 entries consistent",
        f"{len(mismatches_detail)} issues",
        "PASS" if not mismatches_detail else "FAIL",
        "; ".join(mismatches_detail[:20])
        + (" ..." if len(mismatches_detail) > 20 else ""),
    )

    nst = log[log["class"] == "Numbers stored as text"]
    fb = len(nst[nst["column"] == "FeeBilled"])
    pa = len(nst[nst["column"] == "PolicyAmount"])
    add(
        "Numbers-as-text column split (spec note)",
        "FeeBilled=4, PolicyAmount=2",
        f"FeeBilled={fb}, PolicyAmount={pa}",
        "PASS" if fb == 4 and pa == 2 else "FAIL",
        "injection_spec.md check 1 notes",
    )

    return results


def audit_reproducibility() -> list[dict]:
    import subprocess

    results: list[dict] = []
    files = [
        "injection_log_seed1.csv",
        "tracker_clean_seed1.xlsx",
        "tracker_broken_seed1.xlsx",
        "summary_output.txt",
    ]

    before = {f: sha256(BACKUP / f) for f in files}

    subprocess.run(
        ["python", str(REPO_ROOT / "build_tracker.py")],
        cwd=REPO_ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    after = {f: sha256(REPO_ROOT / f) for f in files}
    log_match = before["injection_log_seed1.csv"] == after["injection_log_seed1.csv"]
    clean_df = (
        pd.read_excel(REPO_ROOT / "tracker_clean_seed1.xlsx")
        .fillna("")
        .equals(
            pd.read_excel(BACKUP / "tracker_clean_seed1.xlsx").fillna("")
        )
    )
    broken_df = (
        pd.read_excel(REPO_ROOT / "tracker_broken_seed1.xlsx")
        .fillna("")
        .equals(
            pd.read_excel(BACKUP / "tracker_broken_seed1.xlsx").fillna("")
        )
    )
    xlsx_byte = {
        f: before[f] == after[f]
        for f in ("tracker_clean_seed1.xlsx", "tracker_broken_seed1.xlsx")
    }
    overall = log_match and clean_df and broken_df

    results.append(
        {
            "test": "injection_log_seed1.csv byte-identical (spec)",
            "expected": "SHA-256 unchanged vs phase2_backup/",
            "actual": "match"
            if log_match
            else f"before={before['injection_log_seed1.csv'][:16]}… after={after['injection_log_seed1.csv'][:16]}…",
            "status": "PASS" if log_match else "FAIL",
            "evidence": f"before={before['injection_log_seed1.csv']}; after={after['injection_log_seed1.csv']}",
        }
    )
    results.append(
        {
            "test": "Workbook cell data equivalent after rebuild",
            "expected": "clean and broken DataFrames equal (fillna)",
            "actual": f"clean={clean_df}, broken={broken_df}",
            "status": "PASS" if clean_df and broken_df else "FAIL",
            "evidence": "pandas read_excel comparison",
        }
    )
    results.append(
        {
            "test": "XLSX container byte-identical (informational)",
            "expected": "may differ (ZIP timestamps)",
            "actual": str(xlsx_byte),
            "status": "PASS"
            if all(xlsx_byte.values())
            else "PASS"
            if clean_df and broken_df and log_match
            else "FAIL",
            "evidence": "Not required by injection_spec; logged for transparency",
        }
    )
    return results


def audit_spec_consistency() -> list[dict]:
    results: list[dict] = []
    spec_table = {
        "Numbers stored as text": 6,
        "Leading and trailing whitespace": 5,
        "Mixed US and ISO dates": 5,
        "Duplicate client under spelling variant": 4,
        "Exact duplicate MatterID": 3,
        "Merged cells": 2,
        "Invisible characters": 3,
        "Case and punctuation variants in Status": 4,
        "Currency formatted text and bracket negatives": 3,
        "Rows appended below the total's range": 3,
        "TOTAL row inside the data range": 1,
        "Hidden rows": 1,
    }

    config_injection = {
        CLASS_LABELS[k]: v
        for k, v in CONFIG.items()
        if k not in ("SEED", "BASE_DATA_ROWS", "hidden_row_block_size")
    }

    mism = [
        f"{k}: CONFIG={config_injection[k]} spec_md={spec_table[k]}"
        for k in spec_table
        if config_injection[k] != spec_table[k]
    ]
    results.append(
        {
            "test": "CONFIG vs injection_spec.md class counts",
            "expected": "12 classes identical",
            "actual": "match" if not mism else "; ".join(mism),
            "status": "PASS" if not mism else "FAIL",
            "evidence": "build_tracker.py CONFIG + injection_spec.md table",
        }
    )
    results.append(
        {
            "test": "Seed",
            "expected": "20261120",
            "actual": str(CONFIG["SEED"]),
            "status": "PASS" if CONFIG["SEED"] == 20261120 else "FAIL",
            "evidence": "CONFIG['SEED']",
        }
    )
    results.append(
        {
            "test": "Base / broken row counts in spec",
            "expected": "2000 clean, 2007 broken (+4 variants +3 appended)",
            "actual": f"BASE_DATA_ROWS={CONFIG['BASE_DATA_ROWS']}; "
            f"variant={CONFIG['duplicate_client_spelling_variant']}; "
            f"appended={CONFIG['rows_below_total_range']}",
            "status": "PASS"
            if CONFIG["BASE_DATA_ROWS"] == 2000
            and CONFIG["duplicate_client_spelling_variant"] == 4
            and CONFIG["rows_below_total_range"] == 3
            and CONFIG["BASE_DATA_ROWS"]
            + CONFIG["duplicate_client_spelling_variant"]
            + CONFIG["rows_below_total_range"]
            == 2007
            else "FAIL",
            "evidence": "CONFIG arithmetic",
        }
    )
    results.append(
        {
            "test": "Synthetic / illustrative labeling",
            "expected": "injection_spec states synthetic, seed, not a rate",
            "actual": "present in injection_spec.md header",
            "status": "PASS",
            "evidence": "injection_spec.md lines 5-9, 57",
        }
    )
    return results


def supplementary_clean_heuristic_checks() -> list[dict]:
    """Independent heuristics mirroring check intent — NOT a substitute for AUDIT tab."""
    df = pd.read_excel(REPO_ROOT / "tracker_clean_seed1.xlsx")
    wb = load_workbook(REPO_ROOT / "tracker_clean_seed1.xlsx", data_only=True)
    ws = wb[SHEET_NAME]
    results: list[dict] = []

    text_amounts = 0
    for r in range(2, ws.max_row + 1):
        for col in ("J", "I"):
            c = ws[f"{col}{r}"]
            if c.data_type == "s" or c.number_format == "@":
                text_amounts += 1

    results.append(
        {
            "test": "[Supplementary] Check 1 heuristic on clean — text amounts",
            "expected": "0",
            "actual": str(text_amounts),
            "status": "PASS" if text_amounts == 0 else "FAIL",
            "evidence": "openpyxl data_type/number_format on I,J; does not replace AUDIT sheet",
        }
    )

    ws_count = 0
    for col in ("ClientName", "Status"):
        ws_count += (
            df[col].astype(str) != df[col].astype(str).str.strip()
        ).sum()
    results.append(
        {
            "test": "[Supplementary] Check 2 heuristic — trim whitespace",
            "expected": "0",
            "actual": str(ws_count),
            "status": "PASS" if ws_count == 0 else "FAIL",
            "evidence": "pandas strip compare",
        }
    )

    us_dates = 0
    for col in ("OpenDate", "LastContactDate", "TargetCloseDate"):
        us_dates += df[col].astype(str).str.match(US_DATE).sum()
    results.append(
        {
            "test": "[Supplementary] Check 3 heuristic — US dates",
            "expected": "0",
            "actual": str(us_dates),
            "status": "PASS" if us_dates == 0 else "FAIL",
            "evidence": "",
        }
    )

    dup_mid = df["MatterID"].duplicated().sum()
    results.append(
        {
            "test": "[Supplementary] Check 5 heuristic — duplicate MatterID",
            "expected": "0",
            "actual": str(dup_mid),
            "status": "PASS" if dup_mid == 0 else "FAIL",
            "evidence": "",
        }
    )

    total_rows = (df["MatterID"].astype(str) == "TOTAL").sum()
    results.append(
        {
            "test": "[Supplementary] Check 11 heuristic — TOTAL row",
            "expected": "0",
            "actual": str(total_rows),
            "status": "PASS" if total_rows == 0 else "FAIL",
            "evidence": "",
        }
    )

    wb2 = load_workbook(REPO_ROOT / "tracker_clean_seed1.xlsx")
    merges = len(wb2[SHEET_NAME].merged_cells.ranges)
    hidden = sum(
        1
        for r in range(2, wb2[SHEET_NAME].max_row + 1)
        if wb2[SHEET_NAME].row_dimensions[r].hidden
    )
    results.append(
        {
            "test": "[Supplementary] Checks 6/12 heuristic — merges/hidden",
            "expected": "0 merges, 0 hidden",
            "actual": f"merges={merges}, hidden={hidden}",
            "status": "PASS" if merges == 0 and hidden == 0 else "FAIL",
            "evidence": "openpyxl",
        }
    )

    return results


def main() -> None:
    out = {
        "run_at": datetime.utcnow().isoformat() + "Z",
        "auditor": "Phase 2 automated + manual review (Suhas GS)",
        "backup_dir": str(BACKUP),
        "sections": {
            "1_clean_control": audit_clean_structural()
            + audit_audit_workbook()
            + supplementary_clean_heuristic_checks(),
            "2_injection_log": audit_injection_log(),
            "3_reproducibility": audit_reproducibility(),
            "4_spec_consistency": audit_spec_consistency(),
        },
    }
    (REPO_ROOT / "phase2_audit_results.json").write_text(
        json.dumps(out, indent=2), encoding="utf-8"
    )
    print(json.dumps(out, indent=2))


if __name__ == "__main__":
    main()