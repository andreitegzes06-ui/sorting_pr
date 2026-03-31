import os
import csv
from collections import defaultdict

BASE_FOLDER = "/home/zxz/Documents/coding/Sorting_Project"
RESULTS_FOLDER = os.path.join(BASE_FOLDER, "results")
INPUT_FILE = os.path.join(RESULTS_FOLDER, "benchmark_results.csv")
OUTPUT_FILE = os.path.join(RESULTS_FOLDER, "summary_results.csv")


def average(numbers):
    return sum(numbers) / len(numbers)


def main():
    grouped_data = defaultdict(list)

    with open(INPUT_FILE, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            algorithm = row["algorithm"]
            input_type = row["input_type"]
            size = row["size"]
            time_value = float(row["time_seconds"])

            key = (algorithm, input_type, size)
            grouped_data[key].append(time_value)

    with open(OUTPUT_FILE, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow([
            "algorithm",
            "input_type",
            "size",
            "runs",
            "mean_time_seconds",
            "min_time_seconds",
            "max_time_seconds"
        ])

        for key in sorted(grouped_data):
            algorithm, input_type, size = key
            times = grouped_data[key]

            writer.writerow([
                algorithm,
                input_type,
                size,
                len(times),
                average(times),
                min(times),
                max(times)
            ])

    print("Analysis finished.")
    print("Summary saved in:", OUTPUT_FILE)


if __name__ == "__main__":
    main()