# Compatibility log

G M Shashank Showrya · 17 November 2026 · `TRACKER_AUDIT_12CHECKS.xlsx`

Monday's three checks (1, 4, and 12) and Tuesday's other nine are in the same workbook. This log is the calculated result on the 30-row sample.

## Applications actually opened

| Application | Exact version | Workbook opened here | What this run can say |
|-------------|----------------|----------------------|------------------------|
| Microsoft Excel | 16.0.20527.20150 (Application.Version 16.0, Application.Build 20527, 64-bit Windows) | Yes. Full calculate, then the AUDIT counts below were read from the cells. | This is Office build 16.0.20527.20150, not Excel 2019. No formula returned `#NAME?`. |
| Excel 2019 | Not installed on this machine | No | Every check is untested on Excel 2019 until someone opens this file in that edition. |
| Google Sheets | Web app. No build number is shown. Opened in the browser on 17 November 2026 as `TRACKER_AUDIT_12CHECKS-sheets.xlsx`. | Yes. AUDIT D2:E13 were read from the cells. | Counts and PASS or FLAG are in the table below. Check 6’s count cell is the text `no formula, see instructions`, not a formula. |
| LibreOffice Calc | 26.8.3.1 (About box `ooSetupVersionAboutBox`). Product version 26.8, extension .3.1. Build id `861effc5289d539f15c4c18d1ba8579ffd78728b`. Vendor: The Document Foundation. | Yes. The workbook was recalculated and AUDIT D2:E13 were read from the cells. The file was closed without saving. | Same twelve results as Excel. No cell returned an error. This run is Calc 26.8.3.1, not Excel 2019. |

Standup note: Excel 2019 was not available. Google Sheets was opened in the browser and every AUDIT count was read back. LibreOffice Calc 26.8.3.1 recalculated the same file. The formulas stay on the brief's allow list (`SUMPRODUCT`, `COUNTIF`, `ISTEXT`, `ISNUMBER`, `SEARCH`, `TRIM`, `CLEAN`, `SUBSTITUTE`, `EXACT`, `UPPER`, `PROPER`, `SUBTOTAL`, `COUNTA`, `MIN`, `MAX`, `CHAR`, `ROW`, `IF`, `N`). None of `XLOOKUP`, `UNIQUE`, `FILTER`, `SORT`, `LET`, `LAMBDA`, `TEXTSPLIT`, or `TRIMRANGE` is in the workbook.

## Sample the formulas ran against

Thirty synthetic rows on DATA, Excel rows 2 to 31. Five deliberate breaks, and no others:

| Break | Where | What was typed |
|-------|--------|----------------|
| FeeBilled stored as text | DATA J5 | `1820.00` with text format |
| FeeBilled stored as text | DATA J12 | `960.50` with text format |
| Trailing space | DATA B8 | `Brooks Holdings LLC ` |
| Spelling pair | DATA B15 and B16 | `Caldwell Holdings LLC` and `Caldwell Holdings, L.L.C.` |
| Hidden block | DATA rows 26, 27, and 28 | three otherwise ordinary rows, hidden |

Yellow cell AUDIT H16 is 31, the last sample row. Blank rows 32 to 5000 were left empty.

## Named result per check

Excel counts are from Excel 16.0.20527.20150 after a full calculate. Google Sheets counts were read from the open sheet on 17 November 2026. Sheets shows no build number. LibreOffice counts are from Calc 26.8.3.1 after `calculateAll`. On the DATA sheet, Calc read SUBTOTAL visible IDs 27 and COUNTA all IDs 30. AUDIT H16 was 31.

| Check | Excel count | Excel result | Google Sheets count | Google Sheets result | LibreOffice 26.8.3.1 count | LibreOffice result |
|------:|-------------|--------------|---------------------|----------------------|---------------------------:|--------------------|
| 1 Numbers stored as text | 2 | FLAG | 2 | FLAG | 2 | FLAG |
| 2 Leading and trailing spaces | 1 | FLAG | 1 | FLAG | 1 | FLAG |
| 3 Mixed US and ISO dates | 0 | PASS | 0 | PASS | 0 | PASS |
| 4 Duplicate client under a spelling variant | 2 | FLAG | 2 | FLAG | 2 | FLAG |
| 5 Exact duplicate MatterID | 0 | PASS | 0 | PASS | 0 | PASS |
| 6 Merged cells | no formula, see instructions | see instructions | no formula, see instructions | see instructions | no formula, see instructions | see instructions |
| 7 Invisible characters | 0 | PASS | 0 | PASS | 0 | PASS |
| 8 Case and punctuation variants in Status | 0 | PASS | 0 | PASS | 0 | PASS |
| 9 Currency symbols and bracket negatives | 0 | PASS | 0 | PASS | 0 | PASS |
| 10 Rows below the total's range | 0 | PASS | 0 | PASS | 0 | PASS |
| 11 A totals row inside the data range | 0 | PASS | 0 | PASS | 0 | PASS |
| 12 Hidden or filtered rows | 3 | FLAG | 3 | FLAG | 3 | FLAG |

Supporting cells from the same calculate: earliest OpenDate 2025-01-06, latest OpenDate 2026-05-14, slashed text dates 0, status counts Open 8, Pending 8, Closed 7, On Hold 7. Check 12 on the DATA sheet: SUBTOTAL visible IDs 27, COUNTA all IDs 30. The empty rows through 5000 did not increase any count.

Checks 1, 2, 4, and 12 match the five breaks. The other live checks did not flag a clean sample row.

## Check 7 does not use the brief table's one-liner

The table's formula is `=SUMPRODUCT(--(J2:J5000<>CLEAN(SUBSTITUTE(J2:J5000,CHAR(160),""))))`.

On a scratch range in this same Excel session, a plain number 100 compared not-equal to its cleaned text, so that formula would FLAG ordinary fees. The scratch count for that formula was 3 out of 3 cells.

The shipped test is row by row, in DATA column T, for PolicyAmount and FeeBilled. A row counts only when the cell is already text and still contains an apostrophe or a non-breaking space. Plain text numbers stay on check 1. Currency text stays on check 9.

On the 30-row sample, which has no invisible character, the count is 0 and the result is PASS. That was true in Excel, in Google Sheets, and in Calc 26.8.3.1.

## Seed 1 scope for checks 1, 3, 4, and 7

Revised 19 November 2026 so the clean 2,000-row file does not flag these four checks, and the broken file still shows the injected rows.

The clean contract stores ISO dates as text, and the same client name on many matters. Check 3 counts a slash in OpenDate, TargetCloseDate, or LastContactDate. It does not count an ISO text date. Check 4 counts a spelling only when another spelling of the same key is at least as common. An exact repeated name counts as 0. A one-and-one pair counts as 2.

Calc 26.8.3.1, after `calculateAll` on the pasted seed files:

| Check | Clean count | Broken count | What the broken count is |
|------:|------------:|-------------:|--------------------------|
| 1 | 0 PASS | 6 FLAG | Four FeeBilled text numbers and two PolicyAmount text numbers |
| 3 | 0 PASS | 5 FLAG | Three slashed OpenDate values and two slashed LastContactDate values |
| 4 | 0 PASS | 4 FLAG | The four added spelling-variant rows |
| 7 | 0 PASS | 3 FLAG | Two apostrophe-prefixed FeeBilled values and one PolicyAmount with a non-breaking space |

The 30-row sample was recalculated after this change. Its twelve results are the ones in the table above this section. Check 10 on a pasted 2,000-row file still needs the yellow cell H16 set to the last row of that file's SUM. The sample leaves H16 at 31.

## Check 12 lives on DATA

`SUBTOTAL(103, A2:A5000)` is in DATA!P2 and `COUNTA(A2:A5000)` is in DATA!Q2. The AUDIT count is Q2 minus P2. A SUBTOTAL on the AUDIT tab would not see hidden DATA rows. Google Sheets has the same limit. That is a placement difference, not a different function.

## Google Sheets formula differences

No check needs a different primary formula in Google Sheets. Check 6 has no formula in either application. Optional Sheets functions (`QUERY`, `REGEXMATCH`, `ARRAYFORMULA`) are not used.
