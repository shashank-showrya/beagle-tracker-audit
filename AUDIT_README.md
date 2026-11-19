# Twelve-check tracker audit

A free sheet that flags errors a hand-kept client or matter tracker can hide. The formulas still return a total. They do not tell you the total skipped something.

This workbook recommends no purchase. Every fix uses a command already in Excel or Google Sheets.

The thirty rows on the DATA tab are a synthetic sample. Five of them were broken on purpose so you can see a flag before you replace them. Those five are a property of this sample. They are not a rate from any real business.

## Download

The workbook is `TRACKER_AUDIT_12CHECKS.xlsx`, in the same folder as this file. Open that file. You do not need another installer.

## Before you paste your own rows

Open the AUDIT tab on the sample. A calculated copy shows:

| Check | Count | Result |
|-------|------:|--------|
| 1 Numbers stored as text | 2 | FLAG |
| 2 Leading and trailing spaces | 1 | FLAG |
| 4 Duplicate client under a spelling variant | 2 | FLAG |
| 12 Hidden or filtered rows | 3 | FLAG |
| 6 Merged cells | no formula, see instructions | see instructions |
| Every other check | 0 | PASS |

Check 4 counts both rows of the pair, so the count is 2, not 1. If those four FLAGs are missing, the workbook has not calculated. In Excel, use Formulas, Calculate Now.

## Which tab to paste into

Paste into the DATA tab, columns A through N, starting at row 2. Leave row 1 as it is. Your columns have to follow that header row, left to right:

MatterID, ClientName, ClientType, MatterType, OpenDate, TargetCloseDate, Status, Owner, PolicyAmount, FeeBilled, FeeCollected, InvoiceCount, LastContactDate, Notes.

Checks look at fixed columns. MatterID is A, ClientName is B, OpenDate is E, TargetCloseDate is F, Status is G, PolicyAmount is I, FeeBilled is J, and LastContactDate is M. A tracker pasted in a different order will flag the wrong field.

## Paste values, not formulas

Use Home, Paste, Values. A formula pasted from another file still points at that file.

Do not paste into columns O through T. Column O is the check 4 key and column R is the trimmed spelling. Column S flags a plain text amount and column T flags an apostrophe or a non-breaking space. P2 and Q2 are the hidden-row count for check 12. Delete those and checks 1, 4, 7, and 12 stop working.

The formulas already read down to row 5000. A tracker of 300 rows does not need a new formula. Rows left blank are not counted.

## What a flag looks like

On the AUDIT tab, column D is the count and column E is the result. FLAG means the count is above zero. PASS means the count is zero. A zero means that check found nothing in rows 2 to 5000. It does not mean the formula cell is empty.

Check 6 is the exception. Its count cell reads `no formula, see instructions`. Merged cells have no formula that works in both Excel and Google Sheets. The menu path is in column F.

If a cell shows `#NAME?`, that check did not run. The workbook uses functions from Excel 2019 and Google Sheets. It does not use XLOOKUP, UNIQUE, FILTER, SORT, LET, LAMBDA, TEXTSPLIT, or TRIMRANGE.

## What to do first

Column F on each AUDIT row says what to do when that check flags.

If check 2 and check 4 both flag, trim the extra spaces before you merge spelling variants. A trailing space will hide a duplicate.

If you have about ten minutes, run checks 1, 10, and 12 first. They are the ones that move a total without an error message.

Check 10 stays quiet until you type a row number. The yellow cell is AUDIT cell H16, labeled "Last row your fee total includes." The sample says 31 because the sample IDs end on row 31. If your own total is `=SUM(J2:J400)`, replace 31 with 400. The count is how many MatterIDs sit below that row.

## How long

Reading the flags on a pasted tracker takes about ten minutes. Fixing the rows that flagged takes as long as the rows take. The sheet does not fix them for you.

## Google Sheets

Upload the whole workbook and open it with Google Sheets, or copy all three tabs. The formulas are the same ones as in Excel. Keep P2 and Q2 on the DATA tab. Check 12 cannot see hidden rows from a formula on another tab.

The sample was calculated in Microsoft Excel 16.0.20527.20150 on this machine. The same workbook was opened in Google Sheets on 17 November 2026, and recalculated in LibreOffice Calc 26.8.3.1 (The Document Foundation, build `861effc5289d539f15c4c18d1ba8579ffd78728b`). In both, checks 1, 2, 4, and 12 were FLAG (2, 1, 2, and 3). Checks 3, 5, 7, 8, 9, 10, and 11 were 0 and PASS. Check 6’s count cell read `no formula, see instructions`. Sheets shows no build number. Excel 2019 is not installed here. `COMPAT_LOG.md` records the read-back.
