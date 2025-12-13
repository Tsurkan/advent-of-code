from __future__ import annotations

import logging
import time
from dataclasses import dataclass # Зручний спосіб створювати класи, які зберігають дані.
from pathlib import Path
from typing import Tuple


logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")


@dataclass(frozen=True)         # Створюємо свою структуру даних, об’єкти незмінні після створення
class Task:
    width: int                  # ширина дошки
    height: int                 # висота дошки
    counts: Tuple[int, ...]     # кортеж кількостей кожного з 6 типів фігур
    total_shapes: int           # загальна кількість фігур
    required_area: int          # загальна площа, яку займають фігури
    board_area: int             # площа дошки (кеш для швидкого доступу)


def read_input(path: Path) -> tuple[Task, ...]:
    """
    Читає файл та повертає кортеж.
    Складність: O(N) + O(M), де N — кількість рядків у файлі, де M — кількість завдань.
    """
    lines = path.read_text().splitlines()  # читаємо всі рядки файлу

    shape_areas: list[int] = [0] * 6   # площа кожного типу фігур
    task_lines: list[str] = []         # рядки завдань

    section = 0       # поточна секція файлу
    shape_index = 0   # індекс фігури (0-5)

    # Проходимо по всіх рядках
    for i, line in enumerate(lines):
        line = line.strip()
        if not line:  # порожній рядок → нова секція
            section += 1
            continue

        if section < 6:  # блок для підрахунку фігур
            if ":" in line:
                continue  # пропускаємо заголовки
            shape_areas[shape_index] += line.count("#")  # підрахунок площі
            # перевіряємо кінець блоку
            if i + 1 >= len(lines) or not lines[i + 1].strip():
                shape_index += 1
        else:
            task_lines.append(line)  # рядки завдань

    # Обробляємо рядки завдань
    tasks: list[Task] = []
    for line in task_lines:
        size_part, counts_part = line.split(": ")
        w, h = map(int, size_part.split("x"))         # ширина і висота дошки
        counts = tuple(map(int, counts_part.split())) # кількості фігур
        total_shapes = sum(counts)                    # загальна кількість фігур
        required_area = sum(shape_areas[i] * counts[i] for i in range(6))  # сумарна площа фігур
        board_area = w * h                             # площа дошки
        tasks.append(Task(w, h, counts, total_shapes, required_area, board_area))

    return tuple(tasks)


def fits_gridwise(task: Task) -> bool:
    """
    Евристична оцінка: кожна фігура займає 3x3 клітинки.
    Це не точне рішення (не розставляє фігури), а швидка перевірка можливості.
    Складність: O(1) — обчислення за константний час.
    """
    cells_x = task.width // 3
    cells_y = task.height // 3
    return cells_x > 0 and cells_y > 0 and task.total_shapes <= cells_x * cells_y


def part_one(tasks: tuple[Task, ...]) -> int:
    """
    Рахує кількість разів, де всі фігури можуть поміститися на дошку.
    Умови:
      1. Загальна площа фігур <= площа дошки
      2. Евристика сітки (fits_gridwise) дозволяє розмістити фігури
    Евристика клітинок нагадує задачу про упакування в сітку (grid packing), але без точного розташування.
    Складність: O(M), де M — кількість завдань.
    """
    valid = 0
    for task in tasks:
        if task.required_area <= task.board_area and fits_gridwise(task):
            valid += 1
    return valid


if __name__ == "__main__":
    tasks = read_input(Path("2025/day12/input.txt"))

    start = time.perf_counter()
    result = part_one(tasks)
    logging.info("Part 1: %d (%.6fs)", result, time.perf_counter() - start)
