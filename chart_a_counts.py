#!/usr/bin/env python3
"""Chart A: defect counts per error class from injection_log_seed1.csv."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent
LOG_PATH = REPO_ROOT / "injection_log_seed1.csv"
OUT_PATH = REPO_ROOT / "chart_a.png"

CAPTION = (
    "counts of defects injected into an illustrative 2,000 row synthetic tracker, "
    "not a rate observed in any real business."
)


def main() -> None:
    df = pd.read_csv(LOG_PATH)
    if df.empty:
        print("injection_log_seed1.csv has no data rows yet (stub phase).")
        counts = pd.Series(dtype=int)
    else:
        counts = df["class"].value_counts().sort_values(ascending=True)
        for label, value in counts.items():
            print(f"{label}: {value}")

    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    if counts.empty:
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.text(0.5, 0.5, "No defect rows in log yet", ha="center", va="center")
    else:
        counts.plot(kind="barh", ax=ax)
    ax.set_xlabel("Injected defect count")
    ax.set_ylabel("Error class")
    fig.text(0.5, 0.02, CAPTION, ha="center", fontsize=9, wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT_PATH.name}")


if __name__ == "__main__":
    main()