import time

# Читаємо вхідний файл
def read_input(filepath):
    with open(filepath, "r") as f:
        return f.read().strip()

# В таблиці Unicode символи: .=46 �=65533 Тому можна використовувати будьякий смайл АЛЕ не знак .
CONST_CHAR = '�' # символ для порожніх місць
# CONST_CHAR = '😊' # символ для порожніх місць

# Створюємо диск за описом
def create_disk(line):
    disk = ""
    empty = False
    i = 0
    for char in line:
        if empty:
            disk += CONST_CHAR * int(char)  # Додаємо порожні блоки
        else:
            disk += chr(i) * int(char)  # Додаємо блоки з символами
            i += 1
        empty = not empty  # Змінюємо стан
    return disk

# Обчислюємо загальну суму згідно умов задачі
def calculate_total(disk):
    total = 0
    for i, c in enumerate(disk):
        if c != CONST_CHAR:  # Ігноруємо порожні блоки
            total += i * ord(c)  # Додаємо вагу символа до суми
    return total


def task_one(filepath):
    line = read_input(filepath)
    start = time.time()

    disk = create_disk(line)
    disk = list(disk)
    first_dot = 0

    # Основний алгоритм переміщення файлів. Загальна складність: O(n**2)
    while True:
        while disk[-1] == CONST_CHAR:  # Видаляємо порожні блоки з кінця
            disk.pop()
        try:
            first_dot = disk.index(CONST_CHAR, first_dot)  # Знаходимо перший порожній блок
        except ValueError:
            break
        disk[first_dot] = disk[-1]  # Переміщуємо файл
        disk.pop()

    total = calculate_total(disk)

    end = time.time()
    print(f"Task 1 Result: {total}")
    print(f"Task 1 Time: {end - start:.2f}s")


def task_two(filepath):
    line = read_input(filepath)
    start = time.time()

    disk = create_disk(line)
    disk = remove_trailing_empty_blocks(disk)
    files = split_files(disk)
    disk = move_files(disk, files)
    total = calculate_total(disk)
    
    end = time.time()
    print(f"Task 2 Result: {total}")
    print(f"Task 2 Time: {end - start:.2f}s")

# Видаляє порожні блоки з кінця
def remove_trailing_empty_blocks(disk):
    while disk[-1] == CONST_CHAR:
        disk.pop()
    return disk

# Розділення диску на окремі файли
def split_files(disk):
    files = []
    last = disk[0]
    file_length = 0
    for i, char in enumerate(disk):
        if char != last:
            files.append((last * file_length, i - file_length)) if last != CONST_CHAR else 0
            file_length = 1
        else:
            file_length += 1
        last = char
    files.append((last * file_length, len(disk) - file_length))
    return files

# Переміщення файлів у відповідні місця
def move_files(disk, files):
    while len(files) > 0:
        length_last = len(files[-1][0])
        try:
            first_dot = disk.index(CONST_CHAR * length_last, 0, files[-1][1])
        except ValueError:
            files.pop()
            continue
        # Переміщуємо файл
        disk = (
            disk[:first_dot] 
            + files[-1][0] 
            + disk[first_dot + length_last:files[-1][1]] 
            + CONST_CHAR * length_last 
            + disk[files[-1][1] + length_last:]
        )
        files.pop()
    return disk


def main(file_path='2024/day9/input.txt'):
    task_one(file_path)  # 6200294120911
    task_two(file_path)  # 6227018762750


if __name__ == "__main__":
    main()
