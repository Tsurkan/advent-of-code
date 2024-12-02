def parse_file(file_path):
    """Reads rows from a file as a generator."""
    with open(file_path, 'r') as f:
        for line in f:
            yield list(map(int, line.split()))


def is_trend_valid(arr):
    """Checks if the array is strictly increasing or decreasing with valid differences."""
    increasing, decreasing = True, True
    for i in range(len(arr) - 1):
        diff = arr[i + 1] - arr[i]
        if not (1 <= abs(diff) <= 3): # от 1 до 3
            return False  # Прерываем сразу при недопустимой разнице
        if diff > 0:
            decreasing = False
        elif diff < 0:
            increasing = False
        if not (increasing or decreasing):
            return False  # Прерываем, если оба условия нарушены
    return True


def check_row(row):
    """Checks if the row or any of its one-element-removed variants is valid."""
    if is_trend_valid(row):
        return True
    for i in range(len(row)):
        if is_trend_valid([row[j] for j in range(len(row)) if j != i]):
            return True
    return False


def task_1(file_path):
    return sum(1 for row in parse_file(file_path) if is_trend_valid(row))


def task_2(file_path):
    return sum(1 for row in parse_file(file_path) if check_row(row))


def main(file_path='2024/day2/input.txt'):
    print('Part one:', task_1(file_path))  # 369
    print('Part two:', task_2(file_path))  # 428


if __name__ == "__main__":
    main()
