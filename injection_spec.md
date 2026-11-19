# Injection specification (illustrative synthetic tracker)

This document describes the **test fixture** used in the article and audit demo. It is written so a business owner can disagree with a specific count without arguing about the whole approach.

## Illustrative data — read this first

The tracker in this repo is **synthetic**. It models a **2,000-row** master client and matter register for a small title and insurance agency. **It is not a client file.**

Every defect in the broken copy was **injected deliberately by script**, with fixed seed **20261120**. The counts below describe **this file only**. They are **not** a rate we found in real businesses.

True totals for comparison come from **`tracker_clean_seed1.xlsx`**, the clean control copy built from the same base rows with zero defects.

## Columns (14)

Row 1 is the header. Data rows are 2 through 2001 in the clean file (before extra rows from injections).

| # | Column | Role |
|---|--------|------|
| A | MatterID | Sequential matter ID (text), e.g. M-2026-00001 |
| B | ClientName | Individual or entity name |
| C | ClientType | Individual or Entity |
| D | MatterType | Title Search, Policy Issue, Closing, Refinance, Endorsement, Claim Review |
| E | OpenDate | Matter open date |
| F | TargetCloseDate | Target close |
| G | Status | Open, Pending, Closed, On Hold |
| H | Owner | Staff initials (six values) |
| I | PolicyAmount | Policy amount |
| J | FeeBilled | Fees billed (focus column for gap demos) |
| K | FeeCollected | Never greater than FeeBilled |
| L | InvoiceCount | 1–4 |
| M | LastContactDate | Last contact |
| N | Notes | Short text, mostly blank |

In the **clean** copy, dates use **ISO `YYYY-MM-DD`**. **OpenDate** spans **1 January 2025** through **31 October 2026**.

## Injected error classes

Each injection is logged in **`injection_log_seed1.csv`** with: `row`, `column`, `class`, `original_value`, `corrupted_value`.

| Check | Error class | Injected count | Notes |
|-------|-------------|----------------|-------|
| 1 | Numbers stored as text | 6 | FeeBilled four times, PolicyAmount twice |
| 2 | Leading and trailing whitespace | 5 | ClientName three times, Status twice |
| 3 | Mixed US and ISO dates | 5 | OpenDate three times, LastContactDate twice |
| 4 | Duplicate client under spelling variant | 4 | Extra rows when variants are added |
| 5 | Exact duplicate MatterID | 3 | Copy-paste duplicate IDs |
| 6 | Merged cells | 2 | One 3-row merge in ClientName, one 2-row merge in Owner |
| 7 | Invisible characters | 3 | Apostrophe-prefixed and non-breaking space numerics |
| 8 | Case and punctuation variants in Status | 4 | e.g. open, OPEN, On-Hold vs On Hold |
| 9 | Currency formatted text and bracket negatives | 3 | e.g. `$1,250.00` or `(450.00)` as text |
| 10 | Rows appended below the total's range | 3 | Rows past where a fixed SUM ends |
| 11 | TOTAL row inside the data range | 1 | Double-count risk in a naive SUM |
| 12 | Hidden rows | 1 | One contiguous block of 5 hidden rows |

**Total injected defects: 40.**

The four spelling-variant duplicate injections and three appended rows bring the broken file to **2,007 data rows** (plus header)—realistic for a hand-kept file that grew at the bottom.

## Clean control copy

**`tracker_clean_seed1.xlsx`**: same 2,000 base rows, **zero** defects. All twelve checks should return **zero** when run against this file before Tuesday scoring.

## Reproducibility

- Seed: **20261120** (also `CONFIG["SEED"]` in `build_tracker.py`).
- Rerunning the script on a clean checkout should reproduce the same logs byte-for-byte once generation is complete.

## Sign-off

Pending — Suhas GS will append confirmation after the four-point check (clean file, 40-row log, reproducibility, CONFIG matches this table).