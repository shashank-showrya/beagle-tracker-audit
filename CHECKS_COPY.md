# Twelve checks — reader-facing copy

Use this wording in the article checklist and align the AUDIT tab with Shashank's formulas.

**Order note:** Run **check 2** (trim spaces) before any dedupe or **check 4**, or trailing spaces will defeat duplicate detection.

---

## 1. Numbers stored as text

**What it looks for:** Amount cells Excel or Sheets treat as text—often FeeBilled or PolicyAmount. The cell looks like a number; SUM skips it and never warns you.

**Why it never raises an error:** SUM and other aggregates ignore text silently. The formula returns a number that looks valid.

**What to do when it fires:** Select the column, **Data → Text to Columns → Finish** (or equivalent in Sheets). Re-read your total; it often moves on the first pass.

---

## 2. Leading and trailing spaces

**What it looks for:** Extra spaces in names or status values, e.g. `Caldwell LLC` vs `Caldwell LLC ` (with a trailing space). COUNTIF and lookups treat them as different values.

**Why it never raises an error:** Every formula sees a valid string. Nothing flags "almost duplicate."

**What to do when it fires:** Add a helper column with `=TRIM(B2)` (or your name column), paste back as values. **Do this before dedupe or check 4.**

---

## 3. Mixed US and ISO dates

**What it looks for:** One date column mixing real dates with text that looks like a date—e.g. `03/04/2026` beside `2026-03-04`.

**Why it never raises an error:** Text dates do not break SUM on other columns; date MIN/MAX and sorts can still run while part of the column is wrong.

**What to do when it fires:** Pick one format for the whole column. Convert text entries with **Text to Columns → Date**. Do not re-type thousands of rows by hand.

---

## 4. Duplicate client under a spelling variant

**What it looks for:** The same client entered twice with different punctuation or spacing, e.g. `Caldwell Holdings LLC` and `Caldwell Holdings, L.L.C.`

**Why it never raises an error:** Each row is a valid client name. Your client count stays high unless you normalize spelling first.

**What to do when it fires:** Decide the canonical spelling, merge or consolidate rows, and move amounts before you delete anything.

---

## 5. Exact duplicate MatterID

**What it looks for:** Two rows sharing the same matter or policy ID—usually from copy-paste during a busy week.

**Why it never raises an error:** Duplicate IDs are still valid text. No `#REF!` or duplicate warning unless you add one.

**What to do when it fires:** Compare the two rows field by field. One is often a stale revision; keep the current row and retire the other.

---

## 6. Merged cells

**What it looks for:** Merged cells in the data area—often in ClientName or Owner—so one value appears to cover several rows.

**Why it never raises an error:** Merges are allowed formatting. Sort and filter can drop rows underneath without any formula error.

**What to do when it fires:** There is **no reliable formula** for merges in every app. In Excel: **Home → Find & Select → Find → Format → Alignment → Merge cells → Find All**. In Sheets: unmerge and look for gaps. Unmerge, fill blanks down, and confirm row count before and after.

---

## 7. Invisible characters

**What it looks for:** Leading apostrophes or non-breaking spaces in numeric columns—common when pasting from PDFs or portals. The value looks identical on screen.

**Why it never raises an error:** The cell behaves as text. SUM skips it like any other text amount.

**What to do when it fires:** Clean with SUBSTITUTE/CLEAN (or paste through Notepad), then paste back as values. Re-check FeeBilled totals.

---

## 8. Case and punctuation variants in Status

**What it looks for:** One status column storing `Open`, `open`, `OPEN`, `On Hold`, `On-Hold`, etc. COUNTIF by status undercounts or splits one state into many.

**Why it never raises an error:** Each variant is a valid string. Charts and pivot tables look fine while filters lie.

**What to do when it fires:** Add **Data Validation** with a fixed list, then correct stragglers. Put validation in place first or bad values return on entry.

---

## 9. Currency symbols and bracket negatives

**What it looks for:** Amounts typed as `$1,250.00` or `(450.00)` inside the cell instead of a real number with number formatting.

**Why it never raises an error:** They are stored as text. SUM ignores them.

**What to do when it fires:** Strip symbols, store the numeric value, apply currency **format** for display—not as part of the stored value.

---

## 10. Rows below the total's range

**What it looks for:** New rows appended below the last row your total formula includes—e.g. data to row 2007 while `=SUM(J2:J2001)` still runs.

**Why it never raises an error:** The formula is valid. It simply does not see the new work.

**What to do when it fires:** Convert the range to a **Table** (Ctrl+T in Excel) or use a whole-column reference that grows with the file. Extend the range and re-check the total.

---

## 11. A totals row inside the data range

**What it looks for:** A row labeled TOTAL or SUBTOTAL sitting inside the rows your SUM includes, so the total adds itself.

**Why it never raises an error:** SUM happily includes every numeric cell in the range, including the total row.

**What to do when it fires:** Move totals **above** the header or to their own tab—never inside the data block.

---

## 12. Hidden or filtered rows

**What it looks for:** Filters or hidden rows still active from an earlier review. You may see hundreds of rows while the file still holds thousands.

**Why it never raises an error:** SUM still includes hidden rows unless you use SUBTOTAL functions intentionally. Your eyes and your total disagree.

**What to do when it fires:** **Data → Clear filters**, unhide all rows, then re-read the total. Compare visible row count to `COUNTA` on an ID column if unsure.