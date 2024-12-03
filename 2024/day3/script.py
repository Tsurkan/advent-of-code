import re

def read_file(file_path):
    """Reads the entire content of a file."""
    with open(file_path, 'r') as f:
        return f.read()


def task_1(data):
    """Calculates the sum of all products found in mul(a, b)."""

    # Шаблон для поиска *mul(число1,число2) в разных формах
    pattern = r"[a-zA-Z_]*mul\((\d+),(\d+)\)"

    return sum(int(a) * int(b) for a, b in re.findall(pattern, data))



def task_2(data):
    """Calculates the sum of products for mul(a, b) considering control instructions."""

    # Шаблон для поиска mul(число1,число2), do() и don't()
    mul_pattern = r"[a-zA-Z_]*mul\((\d+),(\d+)\)"
    control_pattern = r"\b(do|don't)\(\)"

    # Собираем события: mul и инструкции
    events = []
    events.extend((m.start(), 'mul', m.groups()) for m in re.finditer(mul_pattern, data))
    events.extend((m.start(), 'control', m.group(1)) for m in re.finditer(control_pattern, data))
    
    # Сортируем по порядку появления
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
