"""
Advent of Code  2025:  Day 1
Рішення для обох варіантів задачі з обертовим циферблатом (0..99) з таймером виконання.

Особливості:
- task_1: рахує лише кінцеві попадання на 0 після кожної команди.
- task_2: рахує ВСІ попадання на 0 під час руху (включно проміжні кліки).

Часова складність:
- O(n) — n = кількість рядків у файлі, мінімально можлива складність.
- Всі операції всередині циклу O(1) → найоптимальніший варіант  на мою думку.
"""

from pathlib import Path # Рекомендований для роботи з файлами в Python з 3.4+
import logging           # В продакшн-проекті print() не використовується — тільки logging.  Звикаю.
import time
from typing import Iterable, Tuple

# --- Налаштування логування ---
logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)


def parse_line(line: str) -> Tuple[str, int] | None:
    """
    Розбирає рядок формату 'L68' або 'R100' -> (буква, число).
    Повертає None, якщо рядок некоректний.

    Часова складність: O(1)
    """
    s = line.strip()
    if not s:
        return None
    if len(s) < 2:
        logging.warning(f"Skipping invalid line: {line!r}")
        return None
    direction = s[0].upper()
    if direction not in {"L", "R"}:
        logging.warning(f"Unknown direction {direction!r} in line: {line!r}")
        return None
    try:
        value = int(s[1:])
    except ValueError:
        logging.warning(f"Invalid number in line: {line!r}")
        return None
    if value < 0:
        logging.warning(f"Expected non-negative number, got: {value}")
        return None
    return direction, value


def task_1(lines: Iterable[str], start: int = 50, period: int = 100) -> int:
    """
    Рахуємо лише кінцеві попадання на 0 після виконання кожної команди.

    Аргументи:
        lines: послідовність рядків-команд ('L68', 'R48', ...)
        start: початкова позиція стрілки (за замовчуванням 50)
        period: розмір кільця (0..period-1), за замовчуванням 100

    Повертає:
        кількість попадань на 0 після завершення кожної команди.
    """

    dial = start % period  # поточна позиція стрілки
    zeros = 0

    for raw in lines:
        parsed = parse_line(raw)
        if parsed is None:
            continue
        direction, value = parsed

        # Лівий рух зменшує індекс, правий — збільшує
        turns = -value if direction == "L" else value

        # Оновлюємо позицію циферблату
        dial = (dial + turns) % period

        # True->1, False->0; додаємо до рахунку попадань на 0
        zeros += (dial == 0)

    return zeros


def task_2(lines: Iterable[str], start: int = 50, period: int = 100) -> int:
    """
    Рахуємо всі випадки, коли стрілка проходить або опиняється на 0 під час обертання.

    Використовуємо "переворот" циферблату для обробки L/R:
      - завжди рухаємося вправо по "перетвореному" циферблату
      - якщо напрям змінюється, обчислюємо cursor := (period - cursor) % period
      - додаємо число кліків, рахуючи повні оберти (cursor // period)
      - оновлюємо залишок (cursor %= period)
    """

    cursor = start % period  # поточна позиція стрілки
    direction = "R"          # поточний напрям руху
    hits = 0                 # рахунок попадань на 0

    for raw in lines:
        parsed = parse_line(raw)
        if parsed is None:
            continue
        letter, number = parsed

        # Якщо напрям змінюється, "перевертаємо" циферблат
        if letter != direction:
            cursor = (period - cursor) % period
            direction = letter

        # рухаємося вперед по "перетвореному" кільцю
        cursor += number

        # повні оберти через period → кожен оберт дорівнює проходженню через 0
        hits += cursor // period

        # залишок — нова позиція на кільці
        cursor %= period

    return hits


def read_lines_from_file(path: Path) -> list[str]:
    """
    Прочитати рядки з файлу.
    Логування помилок при невдалому читанні.

    Часова складність: O(n), де n = кількість рядків
    """
    try:
        return path.read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        return []
    except Exception as exc:
        logging.error(f"Error reading file {path}: {exc}")
        return []


if __name__ == "__main__":
    lines = read_lines_from_file(Path("2025/day1/input.txt"))
    if not lines:
        logging.info("No lines to process.")
    else:
        # --- Task 1 ---
        start_time = time.perf_counter()  # початок таймера
        result_1 = task_1(lines)
        end_time = time.perf_counter()    # кінець таймера
        logging.info(f"Task 1: {result_1}")
        logging.info(f"Execution time Task 1: {end_time - start_time:.6f} seconds")

        # --- Task 2 ---
        start_time = time.perf_counter()  # початок таймера
        result_2 = task_2(lines)
        end_time = time.perf_counter()    # кінець таймера
        logging.info(f"Task 2: {result_2}")
        logging.info(f"Execution time Task 2: {end_time - start_time:.6f} seconds")
