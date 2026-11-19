# Your hand-kept tracker has errors that never break a formula

> Draft outline — numbers must come from `summary_output.txt` only. Use `[FIGURE NEEDED]` until Suhas's generator and Tuesday validation land.

---

*(Opening — no heading)*

Your tracker looks normal. Your total looks confident. Nothing in the formula bar complains. The errors that move a total are often the ones formulas **accept**, not the ones they reject.

One more beat: the same client twice under two spellings; amounts stored as text; new rows below where your SUM stops. Each is valid spreadsheet behavior—and that is the problem.

## The worked example, and why it is illustrative

The tracker in this article is a synthetic 2,000 row file we built for this purpose. It is not a client file. The errors in it were injected deliberately, by script, with a fixed seed, so every count below is reproducible. The script and its spec are published with this article.

The forty defects are a property of our file, chosen by us. They are not a rate we found in real businesses. The twelve checks are what transfers to your file.

## Why a wrong total never announces itself

SUM skips text silently. COUNTIF matches strings exactly—`Open` and `Open ` are two states. Merged cells can survive a sort while dropping rows underneath. A range that ends at row 1800 in a 2,007 row file is still a valid formula. Every one of those behaviors is "correct." That is why you need checks that do not wait for `#VALUE!`.

## How we built a broken file on purpose

[FIGURE NEEDED — from `summary_output.txt`: column count, row counts, OpenDate range, per-class injection counts]

*(Insert chart_a.png when available.)*

Fourteen columns, twelve error classes, clean control copy, injection log as ground truth. Suhas describes the script in plain language in the final package.

## The total was wrong and nothing said so

[FIGURE NEEDED — naive total, true total, gap by class]

*(Insert chart_b.png when gap_by_class.csv exists.)*

## Twelve checks to run on your own tracker this week

*(Pull from `CHECKS_COPY.md` — one short paragraph per check in final edit.)*

1. Numbers stored as text  
2. Leading and trailing spaces *(before dedupe)*  
3. Mixed US and ISO dates  
4. Duplicate client under a spelling variant  
5. Exact duplicate MatterID  
6. Merged cells *(menu path, not formula)*  
7. Invisible characters  
8. Case and punctuation variants in Status  
9. Currency symbols and bracket negatives  
10. Rows below the total's range  
11. A totals row inside the data range  
12. Hidden or filtered rows  

## Which three to run first if you only have ten minutes

Checks **1**, **10**, and **12**: text amounts, rows past your range, hidden rows. Fast to run and often moves the total.

## What to do after the flags clear

Fix once, then prevent re-entry: Data Validation on status, one date format, a Table instead of a fixed range, totals above the header. Re-audit monthly.

## What this is not

This does not estimate what a wrong total means in fees, rework, or missed deadlines—that is not in this data. It **does** name which errors survive silently and how to find them in **your** tracker.

## Close

The audit sheet is free and recommends no purchase. Download it, run it on your own tracker this week, and note which check fired first.

---

*The tracker in this article is a synthetic illustration; the forty defects were injected by script and the counts describe that file and nothing else.*