def read_matrix(file_path):
    """Зчитує масив з файлу."""
    with open(file_path, 'r') as f:
        return [list(map(int, line.split())) for line in f]


def task_1(file_path):
    col1, col2 = zip(*read_matrix(file_path)) # Транспонуємо матрицю, отримуючи два стовпці

    # Сортуємо стовпці для полегшення порівняння мінімальних значень
    col1, col2 = sorted(col1), sorted(col2)

    # Обчислюємо суму абсолютних різниць між елементами одного стовпця та іншого
    # Складність: O(n log n) через сортування.
    return sum(abs(a - b) for a, b in zip(col1, col2))


def task_2(file_path):
    col1, col2 = zip(*read_matrix(file_path)) # Транспонуємо матрицю, отримуючи два стовпці

    # Підрахунок кількості елементів у другому стовпці. Складність: O(n)
    col2_counts = {}
    for val in col2:
        col2_counts[val] = col2_counts.get(val, 0) + 1

    # Обчислюємо суму добутків елементів першого стовпця та їх кількості у другому стовпці. Складність: O(n)
    total_sum = sum(value * col2_counts.get(value, 0) for value in col1)

    return total_sum


def main():
    file_path = '2024/day1/input1.txt'
    print('Part one:', task_1(file_path))  # 1941353
    print('Part two:', task_2(file_path))  # 22539317


if __name__ == "__main__":
    main()
