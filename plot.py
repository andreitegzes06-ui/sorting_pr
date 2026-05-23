from pathlib import Path

import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


BASE_FOLDER = Path(__file__).resolve().parents[1]
RESULTS_FOLDER = BASE_FOLDER / "results"
INPUT_FILE = RESULTS_FOLDER / "summary_results.csv"
MAX_PLOT_SIZE = 1000000

ALGORITHM_ORDER = [
    "bubble_sort",
    "selection_sort",
    "insertion_sort",
    "merge_sort",
    "quick_sort",
    "python_sort",
    "heap_sort",
    "shell_sort",
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
ALGORITHM_COLORS = {
    "bubble_sort": "C0",
    "selection_sort": "C1",
    "insertion_sort": "C2",
    "merge_sort": "C3",
    "quick_sort": "C4",
    "python_sort": "C5",
    "heap_sort": "C6",
    "shell_sort": "C7",
}


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


def plot_overall_runtime(df):
    plot_data = (
        df.groupby(["algorithm", "size"], as_index=False)["mean_time_seconds"]
        .mean()
        .sort_values("size")
    )

    algorithms = ordered_values(plot_data["algorithm"].unique(), ALGORITHM_ORDER)

    fig, ax = plt.subplots(figsize=(9, 5.4))

    for algorithm in algorithms:
        alg_data = plot_data[plot_data["algorithm"] == algorithm]
        ax.plot(
            alg_data["size"],
            alg_data["mean_time_seconds"],
            marker="o",
            color=ALGORITHM_COLORS.get(algorithm),
            linewidth=1.8,
            markersize=4,
            label=algorithm,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(plot_data["size"].min(), MAX_PLOT_SIZE)
    ax.set_title("Sorting Algorithm Comparison", fontsize=11)
    ax.set_xlabel("Input size", fontsize=9)
    ax.set_ylabel("Average time across input types (seconds)", fontsize=9)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8, loc="upper left")
    ax.tick_params(axis="both", labelsize=8)

    fig.tight_layout()

    output_file = RESULTS_FOLDER / "figure_2_overall_runtime_comparison.png"
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print("Overall runtime plot saved in:", output_file)


def plot_algorithm_group(df, algorithms, title, output_name):
    plot_data = (
        df.groupby(["algorithm", "size"], as_index=False)["mean_time_seconds"]
        .mean()
        .sort_values("size")
    )
    plot_data = plot_data[plot_data["algorithm"].isin(algorithms)]
    algorithms = ordered_values(plot_data["algorithm"].unique(), algorithms)

    fig, ax = plt.subplots(figsize=(9, 5.4))

    for algorithm in algorithms:
        alg_data = plot_data[plot_data["algorithm"] == algorithm]
        ax.plot(
            alg_data["size"],
            alg_data["mean_time_seconds"],
            marker="o",
            color=ALGORITHM_COLORS.get(algorithm),
            linewidth=1.8,
            markersize=4,
            label=algorithm,
        )

    ax.set_xscale("log")
    ax.set_yscale("log")
    ax.set_xlim(plot_data["size"].min(), MAX_PLOT_SIZE)
    ax.set_title(title, fontsize=11)
    ax.set_xlabel("Input size", fontsize=9)
    ax.set_ylabel("Average time across input types (seconds)", fontsize=9)
    ax.grid(True, which="both", alpha=0.25)
    ax.legend(fontsize=8, loc="upper left")
    ax.tick_params(axis="both", labelsize=8)

    fig.tight_layout()

    output_file = RESULTS_FOLDER / output_name
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print("Algorithm group plot saved in:", output_file)


def plot_algorithm_groups(df):
    plot_algorithm_group(
        df,
        ["bubble_sort", "selection_sort", "insertion_sort"],
        "Slower Sorting Algorithms",
        "figure_2a_slow_algorithms.png",
    )
    plot_algorithm_group(
        df,
        ["merge_sort", "quick_sort"],
        "Medium Sorting Algorithms",
        "figure_2b_medium_algorithms.png",
    )
    plot_algorithm_group(
        df,
        ["python_sort"],
        "Python Sort Runtime",
        "figure_2c_python_sort_brown_algorithm.png",
    )


def plot_runtime_by_input_type(df):
    plot_data = (
        df.groupby(["algorithm", "input_type"], as_index=False)["mean_time_seconds"]
        .mean()
    )

    algorithms = ordered_values(plot_data["algorithm"].unique(), ALGORITHM_ORDER)
    input_types = ordered_values(plot_data["input_type"].unique(), INPUT_TYPE_ORDER)

    columns = 2
    rows = int(np.ceil(len(algorithms) / columns))
    fig, axes = plt.subplots(rows, columns, figsize=(9, rows * 2.25))
    axes = np.array(axes).reshape(-1)

    for index, algorithm in enumerate(algorithms):
        ax = axes[index]
        alg_data = (
            plot_data[plot_data["algorithm"] == algorithm]
            .set_index("input_type")
            .reindex(input_types)
        )

        ax.bar(input_types, alg_data["mean_time_seconds"], color="#1f77b4")
        ax.set_title(algorithm, fontsize=9)
        ax.set_ylabel("Average time (seconds)", fontsize=7)
        ax.set_yscale("log")
        ax.tick_params(axis="x", rotation=45, labelsize=6)
        ax.tick_params(axis="y", labelsize=7)
        ax.grid(True, axis="y", alpha=0.2)

    for ax in axes[len(algorithms):]:
        ax.axis("off")

    fig.suptitle("Average Runtime by Input Type", fontsize=11)
    fig.tight_layout(rect=(0, 0, 1, 0.97))

    output_file = RESULTS_FOLDER / "figure_3_average_runtime_by_input_type.png"
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print("Input-type runtime plot saved in:", output_file)


def plot_heatmap(df):
    heatmap_data = df.pivot_table(
        index="algorithm",
        columns="input_type",
        values="mean_time_seconds",
        aggfunc="mean",
    )

    algorithms = ordered_values(heatmap_data.index, ALGORITHM_ORDER)
    input_types = ordered_values(heatmap_data.columns, INPUT_TYPE_ORDER)
    heatmap_data = heatmap_data.reindex(index=algorithms, columns=input_types)

    log_data = np.log10(heatmap_data)
    annotations = heatmap_data.map(lambda value: "" if pd.isna(value) else f"{value:.2e}")

    fig, ax = plt.subplots(figsize=(9.5, 4.3))
    image = ax.imshow(log_data, cmap="viridis", aspect="auto")

    ax.set_title("Heatmap of Average Runtime by Algorithm and Input Type", fontsize=10)
    ax.set_xlabel("Input type", fontsize=8)
    ax.set_ylabel("Algorithm", fontsize=8)
    ax.set_xticks(range(len(input_types)))
    ax.set_xticklabels(input_types, rotation=45, ha="right", fontsize=7)
    ax.set_yticks(range(len(algorithms)))
    ax.set_yticklabels(algorithms, fontsize=8)

    for row_index, algorithm in enumerate(algorithms):
        for column_index, input_type in enumerate(input_types):
            label = annotations.loc[algorithm, input_type]
            if label:
                ax.text(
                    column_index,
                    row_index,
                    label,
                    ha="center",
                    va="center",
                    fontsize=6,
                    color="white",
                )

    colorbar = fig.colorbar(image, ax=ax)
    colorbar.set_label("log10 average time in seconds", fontsize=8)
    colorbar.ax.tick_params(labelsize=7)

    fig.tight_layout()

    output_file = RESULTS_FOLDER / "figure_4_average_runtime_heatmap.png"
    fig.savefig(output_file, dpi=300)
    plt.close(fig)
    print("Heatmap saved in:", output_file)


def main():
    df = load_results()
    plot_overall_runtime(df)
    plot_algorithm_groups(df)
    plot_runtime_by_input_type(df)
    plot_heatmap(df)


if __name__ == "__main__":
    main()
