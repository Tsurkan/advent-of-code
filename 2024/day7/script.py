import time
from pathlib import Path


def read_input(file_name: str) -> list:
    """
    Зчитування і розбиття вхідних даних на рядки.
    Повертає список рядків з файлу.
    """
    return open(Path(__file__).parent.joinpath(file_name), "r").read().splitlines()


def get_operator_function(op: str):
    """
    Повертає функцію для заданого оператора.
    """
    if op == "+":
        return lambda a, b: a + b  # Додавання
    elif op == "*":
        return lambda a, b: a * b  # Множення
    elif op == "||":
        return lambda a, b: a * (10 ** len(str(b))) + b  # Конкатенація чисел (ни використовуємо строки)
    else:
        raise ValueError(f"Невідомий оператор: {op}")


# Складність: O(n!)
def evaluate(values: list, test_value: int, operators: list) -> bool:
    """
    Рекурсивно обчислює результат, перевіряючи, чи можна отримати test_value.
    values - список чисел, з якими виконуються операції.
    test_value - цільове значення.
    operators - список операторів.
    """
    if len(values) == 1:  # Базовий випадок: лише одне значення залишилося
        return values[0] == test_value
    for op in operators:
        value = op(values[0], values[1])  # Застосовуємо оператор до перших двох чисел
        if evaluate([value] + values[2:], test_value, operators): # Рекурсивно перевіряємо решту списку
            return True
    return False  # Якщо результат не знайдено


def process(file: list, operators: list) -> int:
    """
    Обробляє файл з даними, використовуючи задані оператори.
    file - список рядків з вхідними даними.
    operators - список операторів.
    Повертає суму всіх test_value, які можуть бути отримані.
    """
    result = 0
    for line in file:
        terms = line.split(":")
        test_value = int(terms[0])
        values = [int(v) for v in terms[1].split()]
        if evaluate(values, test_value, operators):  # Перевіряємо, чи можливо отримати test_value
            result += test_value
    return result


def task(file_name: str, operation_symbols: list):
    """
    Основна функція для виконання завдання.
    file_name - ім'я файлу з вхідними даними.
    operation_symbols - список символів операторів.
    """
    start_time = time.time()

    operators = [get_operator_function(op) for op in operation_symbols]
    result = process(read_input(file_name), operators)
    
    print("\n--- %s seconds ---" % (time.time() - start_time))  # Виводимо час виконання
    return result


def main(file_path='input.txt'):
    print('Part one:', task(file_path, ["+", "*"]))        # 6231007345478
    print('Part two:', task(file_path, ["+", "*", "||"]))  # 333027885676693


if __name__ == "__main__":
    main()
