import re

def read_file(file_path):
    """Зчитує весь вміст файлу."""
    with open(file_path, 'r') as f:
        return f.read()


def task_1(data):
    """Обчислює суму всіх добутків, знайдених у mul(a, b)."""

    # Шаблон для пошуку *mul(число1,число2) у різних формах
    pattern = r"[a-zA-Z_]*mul\((\d+),(\d+)\)"

    # Складність: O(n)
    return sum(int(a) * int(b) for a, b in re.findall(pattern, data))



def task_2(data):
    """Обчислює суму добутків для mul(a, b) з урахуванням контрольних інструкцій."""

    # Шаблон для пошуку mul(число1,число2)
    mul_pattern = r"[a-zA-Z_]*mul\((\d+),(\d+)\)"

    # Шаблон для пошуку інструкцій do() і don't()
    control_pattern = r"\b(do|don't)\(\)"

    # Складність кожного: O(n)
    events = []
    events.extend((m.start(), 'mul', m.groups()) for m in re.finditer(mul_pattern, data))
    events.extend((m.start(), 'control', m.group(1)) for m in re.finditer(control_pattern, data))
    
    # Сортуємо події за порядком їх появи в тексті. Складність: O(m log m), де m — кількість знайдених подій
    events.sort(key=lambda x: x[0])

    mul_enabled = True
    products = []

    for _, event_type, value in events:
        if event_type == 'mul' and mul_enabled:
            a, b = map(int, value)
            products.append(a * b)
        elif event_type == 'control':
            mul_enabled = (value == 'do')

    return sum(products)

def main():
    data = read_file('2024/day3/input.txt')

    print('Part one:', task_1(data))  # 174561379
    print('Part two:', task_2(data))  # 106921067


if __name__ == "__main__":
    main()
