from pathlib import Path
import logging
import time
from typing import List

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def read_lines_from_file(path: Path) -> List[str]:
    """
    Прочитати всі непорожні рядки з текстового файлу.

    Параметри:
        path : Path = Шлях до текстового файлу.

    Повертає:
        List[str] : Список рядків із цифрами.

    Складність: O(n), де n — кількість рядків у файлі.
    """
    if not path.exists():
        logging.error(f"File not found: {path}")
        return []
    return [line.strip() for line in path.read_text().splitlines() if line.strip()]

def max_joltage_monotonic(bank: List[int], n: int) -> int:
    """
    Побудувати найбільше можливе число довжиною n, зберігаючи порядок цифр у вихідному банку.

    Алгоритм:
    ----------
    Використовується **Monotonic Decreasing Stack** — відомий оптимальний алгоритм для задач:
      - "Create Maximum Number"
      - "Remove K Digits"
      - "Max Subsequence"
      - формування найбільшого можливого числа з обмеженої кількості елементів.

    Ідея алгоритму:
    ----------
    Ми хочемо взяти n цифр так, щоб утворити максимально можливе число.
    Для цього:
    1. Проходимо цифри зліва направо.
    2. Тримаємо стек, що завжди містить найкраще число.
    3. Якщо нова цифра більша за верх стеку — видаляємо меншу (якщо ще можна видаляти).
    4. Додаємо цифру в стек.
    5. В кінці просто обрізаємо стек до потрібної довжини n.

    Параметри:
        bank : List[int] = Список цифр у банку батарей.
        n : int = Скільки цифр треба вибрати.

    Повертає:
        int : Найбільше можливе число, складене з n цифр.

    Складність: O(m), де m — довжина списку цифр.
    """
    to_remove = len(bank) - n  # скільки цифр можна "відкинути"
    stack = []

    for digit in bank:
        # видаляємо всі менші цифри, поки можемо
        while stack and to_remove > 0 and stack[-1] < digit:
            stack.pop()
            to_remove -= 1

        stack.append(digit)

    # беремо тільки перші n цифр — це наше число
    result_digits = stack[:n]

    # перетворюємо список цифр на число
    value = 0
    for d in result_digits:
        value = value * 10 + d

    return value

def task_1(lines: List[str]) -> int:
    """
    Завдання 1: для кожного банку вибрати 2 цифри,
    утворити максимально можливе число і повернути їх суму.

    Складність: O(n * m), де n — кількість банків, m — довжина кожного банку.
    """
    return sum(max_joltage_monotonic(list(map(int, line)), 2) for line in lines)

def task_2(lines: List[str]) -> int:
    """
    Завдання 2: аналогічно першому, але тепер треба вибрати 12 цифр.

    Складність: O(n * m).
    """
    return sum(max_joltage_monotonic(list(map(int, line)), 12) for line in lines)

if __name__ == "__main__":
    banks = read_lines_from_file(Path("2025/day3/input.txt"))

    if not banks:
        logging.info("No banks to process.")
    else:
        start_time = time.perf_counter()
        result_1 = task_1(banks)
        logging.info(f"Task 1: {result_1} (time: {time.perf_counter() - start_time:.6f}s)")

        start_time = time.perf_counter()
        result_2 = task_2(banks)
        logging.info(f"Task 2: {result_2} (time: {time.perf_counter() - start_time:.6f}s)")
