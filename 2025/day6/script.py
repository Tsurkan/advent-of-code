import logging
import time
from pathlib import Path
from typing import List, Callable
from operator import add, mul


logging.basicConfig(level=logging.INFO, format="%(message)s")

def read_lines_from_file(path: Path) -> List[str]:
    """
    Функція читання рядків з файлу.
    Складність: O(N), де N — кількість рядків у файлі.
    """
    if not path.exists():
        logging.error(f"Input file not found: {path}")
        return []
    return path.read_text().splitlines()

def parse_worksheet(lines: List[str]) -> tuple[List[List[int]], List[Callable]]:
    """
    Розбираємо оператори та числа.
    Складність: O(N·M), де N — кількість рядків, M — кількість чисел у рядку.
    """
    *number_lines, ops_line = lines

    operators = []
    for symbol in ops_line.split():
        operators.append(add if symbol == "+" else mul)

    rows = []
    for line in number_lines:
        rows.append(list(map(int, line.split())))

    return rows, operators

def task_1(numbers: List[List[int]], operators: List[Callable]) -> int:
    """
    Для кожної колонки застосовуємо відповідний оператор.
    Складність: O(N·M).
    """
    num_cols = len(operators)
    num_rows = len(numbers)

    column_results = []

    for col in range(num_cols):
        op = operators[col]
        acc = numbers[0][col]

        # послідовно застосовуємо оператор до значень у колонці
        for row in range(1, num_rows):
            acc = op(acc, numbers[row][col])

        column_results.append(acc)

    return sum(column_results)

def task_2(lines: List[str], ops_line: str) -> int:
    """
    Частина 2: "справжня" цифроподібна математика — читаємо стовпці справа-наліво.
    Складність: O(N·M).
    """
    # Дістаємо оператори з останнього рядка
    operator_symbols = [c for c in ops_line if c in "+*"]
    operators = [add if c == "+" else mul for c in operator_symbols]

    number_lines = lines[:-1]

    # Транспонуємо "матрицю символів" — кожна колонка стає кортежем символів
    columns = list(zip(*number_lines))

    grand_total = 0
    op_index = len(operators) - 1  # починаємо з правого оператора

    current_problem_columns = []

    def process_problem(col_block: List[List[str]], operator: Callable) -> int:
        """
        Обробляє блок колонок та рахує задачу.
        Кожна колонка → число.
        Складність: O(K·H), де K — кількість колонок задачі, H — висота.
        """
        col_block = list(reversed(col_block))

        numbers = []
        for col in col_block:
            digit_str = "".join(col).strip()
            numbers.append(int(digit_str))

        acc = numbers[0]
        for n in numbers[1:]:
            acc = operator(acc, n)

        return acc

    # Читаємо колонки справа наліво
    for col in reversed(columns):
        # якщо колонка пуста → роздільник між задачами
        if all(c == " " for c in col):
            if current_problem_columns:
                operator = operators[op_index]
                grand_total += process_problem(current_problem_columns, operator)
                current_problem_columns = []
                op_index -= 1
        else:
            # додаємо непорожню колонку до поточної задачі
            current_problem_columns.append(list(col))

    # обробка останньої (лівої) задачі
    if current_problem_columns:
        operator = operators[op_index]
        grand_total += process_problem(current_problem_columns, operator)

    return grand_total

if __name__ == "__main__":
    lines = read_lines_from_file(Path("2025/day6/input.txt"))

    if not lines:
        logging.info("No data to process.")
    else:
        number_rows, ops = parse_worksheet(lines)

        start = time.perf_counter()
        result_part1 = task_1(number_rows, ops)
        logging.info(f"Task 1: {result_part1}\t(time: {time.perf_counter() - start:.6f}s)")

        start = time.perf_counter()
        result_part2 = task_2(lines, lines[-1])
        logging.info(f"Task 2: {result_part2}\t(time: {time.perf_counter() - start:.6f}s)")
