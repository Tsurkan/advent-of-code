import logging
import time
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def read_lines_from_file(file_path: Path):
    """
    Зчитує всі рядки з файлу та повертає список рядків без символів нового рядка.
    Складність: O(L), де L — кількість рядків у файлі.
    """
    try:
        with open(file_path, 'r') as f:
            return [line.strip() for line in f.readlines()]
    except FileNotFoundError:
        logging.error(f"File not found: {file_path}")
        return []

def parse_ranges_and_ingredients(lines):
    """
    Розділяє вхідні дані на:
    - fresh_ranges: список кортежів (start, stop) для свіжих інгредієнтів
    - available_ingredients: список чисел наявних інгредієнтів
    Складність: O(L)
    """
    fresh_ranges = []
    available_ingredients = []

    for line in lines:
        if "-" in line:
            start, end = map(int, line.split("-"))
            fresh_ranges.append((start, end))  # включний діапазон
        elif line:
            available_ingredients.append(int(line))

    return fresh_ranges, available_ingredients

def merge_ranges(ranges_list):
    """
    Алгоритм "Merge Intervals" (злиття перетинаючихся інтервалів)
    Повертає список неперетинаючихся діапазонів (кортежів)
    Складність: O(N log N) через сортування + O(N) проходження
    """
    merged = []
    for start, stop in sorted(ranges_list, key=lambda x: x[0]):
        if not merged:
            merged.append((start, stop))
            continue
        last_start, last_stop = merged[-1]
        if start <= last_stop:  # перетин
            merged[-1] = (last_start, max(last_stop, stop))  # об'єднуємо
        else:
            merged.append((start, stop))
    return merged

def is_fresh(ingredient, merged_ranges):
    """
    Перевіряє, чи належить інгредієнт хоча б одному об'єднаному діапазону.
    Використовується Binary Search:
    Складність: O(log N)
    """
    left = 0
    right = len(merged_ranges) - 1
    while left <= right:
        mid = (left + right) // 2
        start, stop = merged_ranges[mid]
        if start <= ingredient <= stop:
            return True
        elif ingredient < start:
            right = mid - 1
        else:
            left = mid + 1
    return False

def count_fresh_ingredients(available_ingredients, merged_ranges):
    """
    Підраховує кількість свіжих інгредієнтів серед наявних
    Складність: O(M log N), де M — кількість інгредієнтів, N — кількість об'єднаних діапазонів
    """
    fresh_count = 0
    for ingredient in available_ingredients:
        if is_fresh(ingredient, merged_ranges):
            fresh_count += 1
    return fresh_count

def count_total_fresh_ids(merged_ranges):
    """
    Підраховує загальну кількість унікальних свіжих інгредієнтів
    Складність: O(N), де N — кількість об'єднаних діапазонів
    """
    return sum(stop - start + 1 for start, stop in merged_ranges)  # +1 для включності

if __name__ == "__main__":
    lines = read_lines_from_file(Path("2025/day5/input.txt"))

    if not lines:
        logging.info("No data to process.")
    else:
        fresh_ranges, available_ingredients = parse_ranges_and_ingredients(lines)
        merged_ranges = merge_ranges(fresh_ranges)

        # Task 1: Підрахунок свіжих інгредієнтів серед наявних
        start_time = time.perf_counter()
        result_task_1 = count_fresh_ingredients(available_ingredients, merged_ranges)
        logging.info(f"Task 1: {result_task_1} (time: {time.perf_counter() - start_time:.6f}s)")

        # Task 2: Підрахунок загальної кількості унікальних свіжих інгредієнтів
        start_time = time.perf_counter()
        result_task_2 = count_total_fresh_ids(merged_ranges)
        logging.info(f"Task 2: {result_task_2} (time: {time.perf_counter() - start_time:.6f}s)")
