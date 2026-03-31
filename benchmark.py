import os
import json
import csv
import time

from sorting_algorithms import (
    bubble_sort,
    selection_sort,
    insertion_sort,
    merge_sort,
    quick_sort,
    python_sort
)

BASE_FOLDER = "/home/zxz/Documents/coding/Sorting_Project"
DATASETS_FOLDER = os.path.join(BASE_FOLDER, "datasets")
RESULTS_FOLDER = os.path.join(BASE_FOLDER, "results")
RESULTS_FILE = os.path.join(RESULTS_FOLDER, "benchmark_results.csv")


def load_data(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def benchmark_algorithm(sort_function, data):
    start = time.perf_counter()
    result = sort_function(data.copy())
    end = time.perf_counter()

    if result != sorted(data):
        print("Sorting error")

    return end - start


def get_size_from_filename(filename):
    name = filename.replace(".json", "")
    parts = name.split("_")
    return int(parts[-1])


def get_input_type_from_filename(filename):
    name = filename.replace(".json", "")
    parts = name.split("_")
    return "_".join(parts[:-1])


def main():
    os.makedirs(RESULTS_FOLDER, exist_ok=True)

    algorithms = {
        "bubble_sort": bubble_sort,
        "selection_sort": selection_sort,
        "insertion_sort": insertion_sort,
        "merge_sort": merge_sort,
        "quick_sort": quick_sort,
        "python_sort": python_sort
    }

    with open(RESULTS_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["algorithm", "input_type", "size", "time_seconds"])

        for filename in os.listdir(DATASETS_FOLDER):
            if not filename.endswith(".json"):
                continue

            filepath = os.path.join(DATASETS_FOLDER, filename)
            data = load_data(filepath)

            size = get_size_from_filename(filename)
            input_type = get_input_type_from_filename(filename)

            print(f"Working on {filename}...")

            for algorithm_name, algorithm_function in algorithms.items():
                if size > 1000 and algorithm_name in ["bubble_sort", "selection_sort", "insertion_sort"]:
                    continue

                elapsed = benchmark_algorithm(algorithm_function, data)
                writer.writerow([algorithm_name, input_type, size, elapsed])

    print("Benchmark finished.")
    print("Results saved in:", RESULTS_FILE)


if __name__ == "__main__":
    main()