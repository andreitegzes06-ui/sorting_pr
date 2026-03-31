import os
import json
import random
import string

BASE_FOLDER = "/home/zxz/Documents/coding/Sorting_Project"
DATASETS_FOLDER = os.path.join(BASE_FOLDER, "datasets")


def save_data(path, data):
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f)


def random_int_array(n):
    arr = []
    for _ in range(n):
        arr.append(random.randint(0, 100000))
    return arr


def sorted_int_array(n):
    arr = []
    for i in range(n):
        arr.append(i)
    return arr


def reverse_sorted_int_array(n):
    arr = []
    for i in range(n, 0, -1):
        arr.append(i)
    return arr


def almost_sorted_int_array(n):
    arr = sorted_int_array(n)
    swaps = max(1, n // 50)   

    for _ in range(swaps):
        i = random.randint(0, n - 1)
        j = random.randint(0, n - 1)
        arr[i], arr[j] = arr[j], arr[i]

    return arr


def half_sorted_int_array(n):
    first_half = []
    second_half = []

    for i in range(n // 2):
        first_half.append(i)

    for _ in range(n - n // 2):
        second_half.append(random.randint(0, 100000))

    return first_half + second_half


def flat_int_array(n):
    values = [1, 2, 3, 4, 5]
    arr = []

    for _ in range(n):
        arr.append(random.choice(values))

    return arr


def random_float_array(n):
    arr = []

    for _ in range(n):
        arr.append(random.uniform(0, 100000))

    return arr


def random_string_array(n, length=6):
    letters = string.ascii_lowercase
    arr = []

    for _ in range(n):
        s = ""
        for _ in range(length):
            s += random.choice(letters)
        arr.append(s)

    return arr


def main():
    os.makedirs(DATASETS_FOLDER, exist_ok=True)

    sizes = [20, 30, 50, 100, 1000, 5000, 10000]

    for size in sizes:
        save_data(os.path.join(DATASETS_FOLDER, f"random_int_{size}.json"), random_int_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"sorted_int_{size}.json"), sorted_int_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"reverse_sorted_int_{size}.json"), reverse_sorted_int_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"almost_sorted_int_{size}.json"), almost_sorted_int_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"half_sorted_int_{size}.json"), half_sorted_int_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"flat_int_{size}.json"), flat_int_array(size))

        save_data(os.path.join(DATASETS_FOLDER, f"random_float_{size}.json"), random_float_array(size))
        save_data(os.path.join(DATASETS_FOLDER, f"random_string_{size}.json"), random_string_array(size))

        print(f"Saved data for size {size}")


if __name__ == "__main__":
    main()