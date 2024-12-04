def parse_file(file_path):
    """Reads rows from a file as a generator."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_word_count(grid, word):
    rows, cols = len(grid), len(grid[0])
    word_len = len(word)
    directions = [
        (0, 1),  # Вправо
        (1, 0),  # Вниз
        (1, 1),  # Диагональ вправо вниз
        (1, -1), # Диагональ вправо вверх
        (0, -1), # Влево
        (-1, 0), # Вверх
        (-1, -1),# Диагональ влево вверх
        (-1, 1)  # Диагональ влево вниз
    ]
    
    count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                
                # Проверяем, укладывается ли слово в сетку
                if 0 <= x + (word_len - 1) * dx < rows and 0 <= y + (word_len - 1) * dy < cols:
                    if all(grid[x + k * dx][y + k * dy] == word[k] for k in range(word_len)):
                        count += 1
    return count

def task_1(file_path):
    word = "XMAS" # Слово для поиска
    return find_word_count(parse_file(file_path), word)

def task_2(file_path):
    grid = parse_file(file_path)

    def is_valid_cell(y, x): 

        # Соседние диагональные клетки
        top_left, bottom_right = grid[y - 1][x - 1], grid[y + 1][x + 1]
        top_right, bottom_left = grid[y - 1][x + 1], grid[y + 1][x - 1]

        # Проверяем обе диагонали
        return (
            top_left + bottom_right in {"MS", "SM"} and
            top_right + bottom_left in {"MS", "SM"}
        )

    # Подсчёт валидных клеток
    return sum(
        1 for y in range(1, len(grid) - 1) for x in range(1, len(grid[0]) - 1)
        if grid[y][x] == 'A' and is_valid_cell(y, x)
    )


def main(file_path='2024/day4/input.txt'):
    print('Part one:', task_1(file_path))  # 2521
    print('Part two:', task_2(file_path))  # 1912


if __name__ == "__main__":
    main()
