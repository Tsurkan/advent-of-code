def read_matrix(file_path):
    """Reads an array from a file."""
    with open(file_path, 'r') as f:
        return [list(map(int, line.split())) for line in f]


def task_1(file_path):
    # Separate columns
    col1, col2 = zip(*read_matrix(file_path))

    # Сортировка упрощает сравнение минимальных значений. Это заменяет множество операций min и remove, ускоряя код.
    col1, col2 = sorted(col1), sorted(col2)

    # Вычисляем сумму абсолютных разностей. O(n log n)
    return sum(abs(a - b) for a, b in zip(col1, col2))


def task_2(file_path):
    col1, col2 = zip(*read_matrix(file_path))

    # Подсчитываем количество элементов во втором столбце
    col2_counts = {}
    for val in col2:
        col2_counts[val] = col2_counts.get(val, 0) + 1

    # Суммируем произведения
    total_sum = sum(value * col2_counts.get(value, 0) for value in col1)

    return total_sum


def main():
    file_path = '2024/day1/input1.txt'
    print('Part one:', task_1(file_path))  # 1941353
    print('Part two:', task_2(file_path))  # 22539317


if __name__ == "__main__":
    main()
