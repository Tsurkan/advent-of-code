# Складність: O(n*m), де n — кількість рядків у файлі, а m — кількість елементів у кожному рядку.
def parse_file(file_path):
    """Зчитує рядки з файлу як генератор."""
    with open(file_path, 'r') as f:
        for line in f:
            yield list(map(int, line.split()))


# Складність: O(m), де m — кількість елементів у масиві
def is_trend_valid(arr):
    """Перевіряє, чи є масив строго зростаючим або спадаючим з допустимими відмінностями."""
    increasing, decreasing = True, True
    for i in range(len(arr) - 1):
        diff = arr[i + 1] - arr[i]
        if not (1 <= abs(diff) <= 3): # від 1 до 3
            return False  # Повертаємо False при недопустимій відмінності
        if diff > 0:
            decreasing = False # Якщо відмінність додатна, масив не є спадаючим
        elif diff < 0:
            increasing = False # Якщо відмінність від'ємна, масив не є зростаючим
        if not (increasing or decreasing):
            return False  # Якщо обидва умови порушені, повертаємо False
    return True


# Складність: O(m^2), де m — кількість елементів у рядку. 
def check_row(row):
    """Перевіряє, чи рядок або будь-яка його варіація з видаленим одним елементом є дійсною."""
    # Перевіряємо без змін
    if is_trend_valid(row):
        return True
    
    # Перевіряємо всі можливі варіації з видаленим одним елементом
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
