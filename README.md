# Python Sorting Algorithm Benchmark

This project compares the runtime performance of common sorting algorithms implemented in Python.

The goal is to test how simple algorithms such as Bubble Sort, Selection Sort, and Insertion Sort behave compared to more efficient algorithms such as Merge Sort, Quick Sort, Heap Sort, Shell Sort, and Python's built-in sorting function.

The project generates input data, runs each algorithm on the same types of lists, checks that the output is correct, saves the results, and creates visual graphs for comparison.

## Project Overview

Sorting is a basic problem in computer science. Many programs need ordered data for searching, ranking, scheduling, indexing, and data analysis.

This project studies sorting from a practical point of view. Instead of only discussing Big O complexity, it measures how the algorithms actually run in Python on different input types and input sizes.

The benchmark answers three main questions:

1. Do the measured runtimes match the theoretical complexity?
2. Does the input type affect algorithm performance?
3. How much faster is Python's built-in sort compared to manual implementations?

## Algorithms Compared

The project compares the following algorithms:

- Bubble Sort
- Selection Sort
- Insertion Sort
- Merge Sort
- Quick Sort
- Heap Sort
- Shell Sort
- Python built-in sort

## Input Types

The benchmark uses several types of generated input lists:

- random integers
- random floating-point numbers
- random strings
- sorted lists
- reverse-sorted lists
- almost-sorted lists
- half-sorted lists
- flat lists with repeated values

This is important because sorting algorithms do not only depend on input size. They can also behave differently depending on the structure of the data.

## Results

### Overall Runtime Comparison

![Overall runtime comparison](graphics/figure_2_overall_runtime_comparison.png)

This graph compares the average runtime of the algorithms across input sizes. The results show that the simple quadratic algorithms become slow quickly as input size increases. Python's built-in sort is the fastest overall because it uses an optimized implementation.

### Runtime by Input Type

![Average runtime by input type](graphics/figure_3_average_runtime_by_input_type.png)

This figure shows how each algorithm behaves on different input structures. Insertion Sort performs especially well on sorted or almost-sorted data, while Selection Sort is more stable because it performs a similar number of comparisons regardless of input order.

### Heatmap Summary

![Average runtime heatmap](graphics/figure_4_average_runtime_heatmap.png)

The heatmap gives a compact overview of the benchmark. Darker cells represent faster runtimes, while lighter cells represent slower runtimes. The heatmap shows that practical performance depends on both algorithm design and input structure.

## Main Findings

The results support the expected theoretical behavior.

Bubble Sort, Selection Sort, and Insertion Sort are useful for learning because they are simple, but they do not scale well for large inputs.

Merge Sort, Quick Sort, Heap Sort, and Shell Sort scale better, although their performance still depends on implementation details and input structure.

Python's built-in sorting function performs best overall. This is expected because it is highly optimized and can take advantage of partially ordered input data.

## Project Structure

```text
sorting_pr/
├── data/
│   └── knowledge_base/
├── src/
│   └── source files
├── README.md
├── requirements.txt
└── .env
