def parse_file(file_path):
    """Reads rows from a file as a generator."""
    with open(file_path, 'r') as f:
        return [line.strip() for line in f if line.strip()]

def find_word_count(grid, word):
    rows = len(grid)
    cols = len(grid[0])
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
    
    def is_valid(x, y):
        return 0 <= x < rows and 0 <= y < cols
    
    def search(x, y, dx, dy):
        for k in range(word_len):
            nx, ny = x + k * dx, y + k * dy
            if not is_valid(nx, ny) or grid[nx][ny] != word[k]:
                return False
        return True

    count = 0
    for x in range(rows):
        for y in range(cols):
            for dx, dy in directions:
                if search(x, y, dx, dy):
                    count += 1
    return count

def task_1(file_path):
    word = "XMAS" # Слово для поиска
    return find_word_count(parse_file(file_path), word)

def task_2(file_path):
    grid = parse_file(file_path)

    def is_valid_cell(y, x): 
        # Проверка, что элементы в соседних диагональных ячейках удовлетворяют условию
        diagonal_check  = all(
            any(x in diagonal for x in ["MS", "SM"]) 
            for diagonal in [grid[y - 1][x - 1] + grid[y + 1][x + 1], grid[y - 1][x + 1] + grid[y + 1][x - 1]]
        )
        return 1 if diagonal_check else 0

    valid_cell_count = 0
    valid_cell_count += sum(
        is_valid_cell(y, x) 
        for y in range(1, len(grid) - 1) 
        for x in range(1, len(grid[0]) - 1) 
        if grid[y][x] == 'A'
    )

    return valid_cell_count


def main(file_path='2024/day4/input.txt'):
    print('Part one:', task_1(file_path))  # 2521
    print('Part two:', task_2(file_path))  # 1912


if __name__ == "__main__":
    main()
