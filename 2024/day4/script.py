def parse_file(file_path):
    """Зчитує рядки з файлу."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_word_count(grid, word):
    """
    Шукає кількість появ слова у матриці в різних напрямках.
    grid: матриця символів (список списків)
    word: слово для пошуку

    Це алгоритм пошуку підрядка у 2D-матриці. (Схожий але складніший: Кнута-Морріса-Пратта)
    Складність: 𝑂(𝑁*𝑀*𝐾), де N — кількість рядків, M — кількість стовпців матриці, K — довжина слова.
    """
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    directions = [
        (0, 1),  # Праворуч
        (1, 0),  # Вниз
        (1, 1),  # Діагональ праворуч вниз
        (1, -1), # Діагональ праворуч вверх
        (0, -1), # Ліворуч
        (-1, 0), # Вгору
        (-1, -1),# Діагональ ліворуч вверх
        (-1, 1)  # Діагональ ліворуч вниз
    ]
    
    count = 0 # Кількості знайдених слів
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions: # Перебір всіх напрямків
                
                # Перевіряємо, чи слово поміщається у межах матриці
                if 0 <= x + (word_len - 1) * dx < rows and 0 <= y + (word_len - 1) * dy < cols:

                    # Перевіряємо, чи всі символи співпадають
                    if all(grid[x + k * dx][y + k * dy] == word[k] for k in range(word_len)):
                        count += 1
    return count

def task_1(file_path):
    word = "XMAS" # Слово для пошуку
    return find_word_count(parse_file(file_path), word)

def task_2(file_path):
    grid = parse_file(file_path)

    def is_valid_cell(y, x):

        # Перевіряємо сусідні діагональні клітини
        top_left, bottom_right = grid[y - 1][x - 1], grid[y + 1][x + 1]
        top_right, bottom_left = grid[y - 1][x + 1], grid[y + 1][x - 1]

        # Перевірка умов для обох діагоналей
        return (
            top_left + bottom_right in {"MS", "SM"} and
            top_right + bottom_left in {"MS", "SM"}
        )

    # Підрахунок валідних клітин
    return sum(
        1 for y in range(1, len(grid) - 1) for x in range(1, len(grid[0]) - 1)
        if grid[y][x] == 'A' and is_valid_cell(y, x)
    )


def main(file_path='2024/day4/input.txt'):
    print('Part one:', task_1(file_path))  # 2521
    print('Part two:', task_2(file_path))  # 1912


if __name__ == "__main__":
    main()
