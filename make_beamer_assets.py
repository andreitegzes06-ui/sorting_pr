from pathlib import Path
import shutil

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PIL import Image
from matplotlib.patches import Rectangle


BASE_FOLDER = Path(__file__).resolve().parents[1]
RESULTS_FOLDER = BASE_FOLDER / "results"
PRESENTATION_FOLDER = BASE_FOLDER / "presentation"
FIGURES_FOLDER = PRESENTATION_FOLDER / "figures"
INPUT_FILE = RESULTS_FOLDER / "summary_results.csv"
HEATMAP_GIF_NAME = "animated_heatmap.gif"
BEAMER_HEATMAP_FRAME_COUNT = 5

ALGORITHM_ORDER = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "python_sort",
]
INPUT_TYPE_ORDER = [
    "almost_sorted_int",
    "flat_int",
    "half_sorted_int",
    "random_float",
    "random_int",
    "random_string",
    "reverse_sorted_int",
    "sorted_int",
]


def load_results():
    df = pd.read_csv(INPUT_FILE)
    df["size"] = df["size"].astype(int)
    df["mean_time_seconds"] = df["mean_time_seconds"].astype(float)
    return df


def ordered_values(values, preferred_order):
    existing = set(values)
    ordered = [value for value in preferred_order if value in existing]
    ordered.extend(sorted(existing - set(ordered)))
    return ordered


def heatmap_table(df):
    table = df.pivot_table(
        index="algorithm",
        columns="input_type",
        values="mean_time_seconds",
        aggfunc="mean",
    )
    algorithms = ordered_values(table.index, ALGORITHM_ORDER)
    input_types = ordered_values(table.columns, INPUT_TYPE_ORDER)
    return table.reindex(index=algorithms, columns=input_types)


def draw_heatmap(table, output_file, title, vmin, vmax, highlights=None):
    log_table = np.log10(table)
    labels = table.map(lambda value: "" if pd.isna(value) else f"{value:.2e}")

    fig, ax = plt.subplots(figsize=(10.4, 4.8))
    image = ax.imshow(log_table, cmap="viridis", aspect="auto", vmin=vmin, vmax=vmax)

    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Input type", fontsize=9)
    ax.set_ylabel("Algorithm", fontsize=9)
    ax.set_xticks(range(len(table.columns)))
    ax.set_xticklabels(table.columns, rotation=45, ha="right", fontsize=8)
    ax.set_yticks(range(len(table.index)))
    ax.set_yticklabels(table.index, fontsize=9)

    for row_index, algorithm in enumerate(table.index):
        for column_index, input_type in enumerate(table.columns):
            label = labels.loc[algorithm, input_type]
            if label:
                ax.text(
                    column_index,
                    row_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=6.5,
                    color="white",
                )

    if highlights:
        for row_name, column_names, color in highlights:
            if row_name not in table.index:
                continue

            row_index = table.index.get_loc(row_name)
            for column_name in column_names:
                if column_name not in table.columns:
                    continue

                column_index = table.columns.get_loc(column_name)
                ax.add_patch(
                    Rectangle(
                        (column_index - 0.5, row_index - 0.5),
                        1,
                        1,
                        fill=False,
                        edgecolor=color,
                        linewidth=3,
                    )
                )

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("log10 average time in seconds", fontsize=9)
    colorbar.ax.tick_params(labelsize=8)

    fig.tight_layout()
    fig.savefig(output_file, dpi=220)
    plt.close(fig)


def make_heatmap_frames(df):
    FIGURES_FOLDER.mkdir(parents=True, exist_ok=True)

    full_table = heatmap_table(df)
    full_log_table = np.log10(full_table)
    vmin = np.nanmin(full_log_table.to_numpy())
    vmax = np.nanmax(full_log_table.to_numpy())

    sizes = sorted(df["size"].unique())
    for frame_index, max_size in enumerate(sizes):
        frame_data = df[df["size"] <= max_size]
        table = heatmap_table(frame_data)
        output_file = FIGURES_FOLDER / f"heatmap_cumulative_{frame_index}.png"
        draw_heatmap(
            table,
            output_file,
            f"Heatmap of Average Runtime up to n = {max_size:,}",
            vmin,
            vmax,
        )

    draw_heatmap(
        full_table,
        FIGURES_FOLDER / "heatmap_final.png",
        "Heatmap of Average Runtime by Algorithm and Input Type",
        vmin,
        vmax,
    )
    draw_heatmap(
        full_table,
        FIGURES_FOLDER / "heatmap_adaptive_highlight.png",
        "Adaptive Cases: Existing Order Can Make Sorting Much Faster",
        vmin,
        vmax,
        highlights=[
            ("bubble_sort", ["sorted_int"], "#ffffff"),
            ("insertion_sort", ["almost_sorted_int", "sorted_int"], "#ffffff"),
            ("python_sort", ["reverse_sorted_int", "sorted_int"], "#ffffff"),
        ],
    )
    draw_heatmap(
        full_table,
        FIGURES_FOLDER / "heatmap_slow_highlight.png",
        "Slow Cases: Large Light Cells Mark Higher Running Times",
        vmin,
        vmax,
        highlights=[
            ("bubble_sort", ["random_string", "reverse_sorted_int"], "#ffffff"),
            ("selection_sort", ["random_string"], "#ffffff"),
            ("insertion_sort", ["reverse_sorted_int"], "#ffffff"),
        ],
    )

    return len(sizes)


def selected_frame_sizes(sizes, frame_count):
    if len(sizes) <= frame_count:
        return sizes

    indexes = np.linspace(0, len(sizes) - 1, frame_count, dtype=int)
    return [sizes[index] for index in indexes]


def make_beamer_heatmap_frames(df, frame_count=BEAMER_HEATMAP_FRAME_COUNT):
    FIGURES_FOLDER.mkdir(parents=True, exist_ok=True)

    full_table = heatmap_table(df)
    full_log_table = np.log10(full_table)
    vmin = np.nanmin(full_log_table.to_numpy())
    vmax = np.nanmax(full_log_table.to_numpy())

    sizes = selected_frame_sizes(sorted(df["size"].unique()), frame_count)
    for frame_index, max_size in enumerate(sizes):
        frame_data = df[df["size"] <= max_size]
        table = heatmap_table(frame_data)
        output_file = FIGURES_FOLDER / f"heatmap_beamer_{frame_index}.png"
        draw_heatmap(
            table,
            output_file,
            f"Heatmap of Average Runtime up to n = {max_size:,}",
            vmin,
            vmax,
        )

    return len(sizes)


def make_gif(frame_files, output_file, duration_ms=900, palindrome=True):
    if palindrome and len(frame_files) > 2:
        frame_files = frame_files + frame_files[-2:0:-1]

    frames = [Image.open(frame_file).convert("P", palette=Image.Palette.ADAPTIVE) for frame_file in frame_files]
    frames[0].save(
        output_file,
        save_all=True,
        append_images=frames[1:],
        duration=duration_ms,
        loop=0,
        optimize=False,
    )

    for frame in frames:
        frame.close()


def make_heatmap_animation(frame_count):
    frame_files = [
        FIGURES_FOLDER / f"heatmap_cumulative_{frame_index}.png"
        for frame_index in range(frame_count)
    ]
    output_file = FIGURES_FOLDER / HEATMAP_GIF_NAME
    make_gif(frame_files, output_file)

    results_output_file = RESULTS_FOLDER / HEATMAP_GIF_NAME
    shutil.copy2(output_file, results_output_file)
    return output_file, results_output_file


def draw_overall_runtime(df, output_file, max_size):
    plot_data = (
        df[df["size"] <= max_size]
        .groupby(["algorithm", "size"], as_index=False)["mean_time_seconds"]
        .mean()
        .sort_values("size")
    )
    algorithms = ordered_values(plot_data["algorithm"].unique(), ALGORITHM_ORDER)

    fig, ax = plt.subplots(figsize=(10, 5.6))

    for algorithm in algorithms:
        alg_data = plot_data[plot_data["algorithm"] == algorithm]
        ax.plot(
            alg_data["size"],
            alg_data["mean_time_seconds"],
            marker="o",
            linewidth=2,
            markersize=4,
            label=algorithm,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(df["size"].min(), df["size"].max())
    ax.set_title(f"Overall Runtime Comparison up to n = {max_size:,}", fontsize=12)
    ax.set_xlabel("Input size", fontsize=10)
    ax.set_ylabel("Average time across input types (seconds)", fontsize=10)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8, loc="upper left")

    fig.tight_layout()
    fig.savefig(output_file, dpi=220)
    plt.close(fig)


def make_runtime_frames(df):
    sizes = sorted(df["size"].unique())
    for frame_index, max_size in enumerate(sizes):
        draw_overall_runtime(
            df,
            FIGURES_FOLDER / f"overall_runtime_{frame_index}.png",
            max_size,
        )

    return len(sizes)


def main():
    df = load_results()
    heatmap_count = make_heatmap_frames(df)
    beamer_heatmap_count = make_beamer_heatmap_frames(df)
    heatmap_gif, results_heatmap_gif = make_heatmap_animation(heatmap_count)
    runtime_count = make_runtime_frames(df)
    print(f"Created {heatmap_count} heatmap frames in {FIGURES_FOLDER}")
    print(f"Created {beamer_heatmap_count} Beamer heatmap frames in {FIGURES_FOLDER}")
    print(f"Created animated heatmap GIF: {heatmap_gif}")
    print(f"Copied animated heatmap GIF to: {results_heatmap_gif}")
    print(f"Created {runtime_count} runtime frames in {FIGURES_FOLDER}")


if __name__ == "__main__":
    main()
