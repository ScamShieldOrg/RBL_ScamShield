"""Regenerate the RC-5 five-run comparison chart from results/summary.csv.

Uses Pillow because this workspace does not have Matplotlib installed. Value
labels occupy a dedicated right-hand column so they never sit on the bars.
"""

from __future__ import annotations

import csv
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont


ROOT = Path(__file__).resolve().parents[1]
INPUT = ROOT / "results" / "summary.csv"
OUTPUT = ROOT / "figures" / "rc5_five_run_comparison.png"

WIDTH, HEIGHT = 1500, 900
BG = "#FFFFFF"
TEXT = "#1F3B57"
SUBTEXT = "#607080"
GRID = "#D7E0E8"
ERROR = "#203B55"
COLORS = {
    "Accuracy": "#2E6DB4",
    "Scam recall": "#E98A1D",
    "Scam-F1": "#2D936C",
}


def font(size: int, bold: bool = False) -> ImageFont.FreeTypeFont:
    name = "arialbd.ttf" if bold else "arial.ttf"
    path = Path("C:/Windows/Fonts") / name
    return ImageFont.truetype(str(path), size)


def load_rows() -> list[dict[str, str]]:
    with INPUT.open("r", newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    return [r for r in rows if r.get("status", "").startswith("Completed")]


def main() -> None:
    rows = load_rows()
    image = Image.new("RGB", (WIDTH, HEIGHT), BG)
    draw = ImageDraw.Draw(image)

    title_font = font(32, True)
    subtitle_font = font(19)
    label_font = font(20, True)
    value_font = font(16)
    tick_font = font(15)
    axis_font = font(17, True)
    legend_font = font(17)

    draw.text((110, 42), "Five-run validation comparison", fill=TEXT, font=title_font)
    draw.text(
        (110, 89),
        "Mean metric values (%) from results/summary.csv; labels report mean ± standard deviation",
        fill=SUBTEXT,
        font=subtitle_font,
    )

    x0, plot_width = 410, 890
    y_top, y_bottom = 172, 770
    value_x = 1322  # A dedicated column, to the right of the 0–100% plot.
    centers = [230 + i * 115 for i in range(len(rows))]
    bar_h = 19
    offsets = [-24, 0, 24]
    metrics = [
        ("Accuracy", "accuracy_mean", "accuracy_std"),
        ("Scam recall", "recall_scam_mean", "recall_scam_std"),
        ("Scam-F1", "f1_scam_mean", "f1_scam_std"),
    ]

    # Grid, scale and axis ticks.
    for tick in range(0, 101, 10):
        x = x0 + plot_width * tick / 100
        draw.line((x, y_top, x, y_bottom), fill=GRID, width=1)
        label = str(tick)
        box = draw.textbbox((0, 0), label, font=tick_font)
        draw.text((x - (box[2] - box[0]) / 2, 784), label, fill=SUBTEXT, font=tick_font)

    for row, center in zip(rows, centers):
        name = row["model_name"].replace(" (alpha=5.0)", " (α=5.0)")
        draw.text((105, center - 14), name, fill=TEXT, font=label_font)

        for offset, (metric, mean_key, std_key) in zip(offsets, metrics):
            mean = float(row[mean_key])
            std = float(row[std_key])
            y = center + offset
            end_x = x0 + plot_width * mean / 100
            low_x = x0 + plot_width * max(0, mean - std) / 100
            high_x = x0 + plot_width * min(100, mean + std) / 100

            draw.rounded_rectangle(
                (x0, y - bar_h // 2, end_x, y + bar_h // 2),
                radius=4,
                fill=COLORS[metric],
            )
            value = f"{mean:.2f} ± {std:.2f}"
            draw.text((value_x, y - 10), value, fill=TEXT, font=value_font)

    # Axis title.
    axis_label = "Metric value (%)"
    axis_box = draw.textbbox((0, 0), axis_label, font=axis_font)
    draw.text(
        (x0 + (plot_width - (axis_box[2] - axis_box[0])) / 2, 824),
        axis_label,
        fill=TEXT,
        font=axis_font,
    )

    # Legend centered beneath the axis.
    legend_items = list(COLORS.items())
    item_widths = [116, 148, 111]
    total_width = sum(item_widths) + 62 * (len(legend_items) - 1)
    start_x = (WIDTH - total_width) / 2
    legend_y = 875
    x = start_x
    for (label, color), width in zip(legend_items, item_widths):
        draw.rounded_rectangle((x, legend_y - 9, x + 21, legend_y + 10), radius=4, fill=color)
        draw.text((x + 30, legend_y - 11), label, fill=TEXT, font=legend_font)
        x += width + 62

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    image.save(OUTPUT, format="PNG", optimize=True)
    print(f"Wrote {OUTPUT} ({WIDTH}x{HEIGHT})")


if __name__ == "__main__":
    main()
