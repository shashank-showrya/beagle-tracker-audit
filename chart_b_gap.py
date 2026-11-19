#!/usr/bin/env python3
"""Chart B: gap by error class (gap_by_class.csv only — no gap math in this script)."""

from __future__ import annotations

from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt  # noqa: E402
import pandas as pd  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent
GAP_PATH = REPO_ROOT / "gap_by_class.csv"
OUT_PATH = REPO_ROOT / "chart_b.png"

CAPTION = (
    "illustrative synthetic tracker; gap stated in this file's own FeeBilled units only."
)

EXPECTED_DATA_ROWS = 13  # twelve injection classes + interaction row in CSV


def main() -> None:
    df = pd.read_csv(GAP_PATH)

    if len(df) != EXPECTED_DATA_ROWS:
        raise SystemExit(
            f"{GAP_PATH.name}: expected {EXPECTED_DATA_ROWS} data rows, got {len(df)}"
        )

    print("gap_by_class.csv rows:", len(df))
    gaps = df["gap"].astype(float)
    for _, row in df.iterrows():
        print(
            f"{row['error_class']}: reported={row['reported_total']} "
            f"actual={row['actual_total']} gap={row['gap']}"
        )

    # Bar order: CSV order (12 classes, then interaction residual).
    classes = df["error_class"].astype(str)
    colors = ["#4a6fa5" if g >= 0 else "#c45c4a" for g in gaps]

    fig, ax = plt.subplots(figsize=(10, 6), dpi=200)
    ax.barh(classes, gaps, color=colors)
    ax.axvline(0, color="#333333", linewidth=1.0, linestyle="-", zorder=1)
    ax.set_xlabel("Gap in FeeBilled units (illustrative file)")
    ax.set_ylabel("Error class")
    ax.grid(axis="x", linestyle=":", alpha=0.4, zorder=0)

    fig.text(0.5, 0.02, CAPTION, ha="center", fontsize=9, wrap=True)
    fig.tight_layout(rect=(0, 0.06, 1, 1))
    fig.savefig(OUT_PATH, bbox_inches="tight")
    plt.close(fig)
    print(f"Wrote {OUT_PATH.name}")
    print(
        "gap range:",
        f"min={gaps.min():.2f}",
        f"max={gaps.max():.2f}",
        f"zeros={(gaps == 0).sum()}",
        f"negative={(gaps < 0).sum()}",
    )


if __name__ == "__main__":
    main()