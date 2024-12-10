def read_input(file_path):
    """Зчитує матрицю з файлу."""
    with open(file_path, "r") as file:
        return [list(map(int, line.strip())) for line in file]


def is_within_bounds(row, col, rows, cols):
    """Перевіряє, чи клітинка (row, col) знаходиться у межах матриці."""
    return 0 <= row < rows and 0 <= col < cols

# Рекурсивний пошук шляхів. Використовую DFS. 
# Складність: O(4**d), де d — глибина рекурсії (максимум 10) і 4 сторони.
def find_trails(matrix, row, col, value, visited):
    """
    Рекурсивно шукає шляхи у матриці, починаючи з точки (row, col),
    збільшуючи значення value. Відмічає вже відвідані клітинки.
    
    Аргументи:
    - matrix: Матриця значень.
    - row, col: Поточна клітинка.
    - value: Поточне значення у шляху.
    - visited: Словник для відмітки відвіданих клітинок.
    """
    # Якщо досягли кінцевого значення
    if value == 9 and matrix[row][col] == 9:
        if (row, col) in visited:
            visited[(row, col)] += 1  # Збільшуємо лічильник для цієї клітинки
            return 0
        visited[(row, col)] = 1  # Відмічаємо клітинку як відвідану
        return 1

    path_count = 0

    # Визначення напрямків для перевірки сусідів (верх, ліво, право, низ)
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]

    for dr, dc in directions:
        next_row, next_col = row + dr, col + dc

        # Перевірка, чи сусідня клітинка знаходиться у межах та має потрібне значення
        if is_within_bounds(next_row, next_col, len(matrix), len(matrix[0])) and matrix[next_row][next_col] == value + 1:
            path_count += find_trails(matrix, next_row, next_col, value + 1, visited)
    
    return path_count

# Складність: O(N×M×4**d), де N і M — розміри матриці, 4**d — складність функції find_trails.
def process_matrix(matrix):
    """
    Обробляє матрицю для підрахунку кількості унікальних шляхів (total_paths)
    та загальної кількості відвіданих клітинок (total_visits).

    Повертає:
    - total_paths: Кількість унікальних шляхів.
    - total_visits: Загальна кількість відвідувань клітинок.
    """
    total_paths = 0
    total_visits = 0

    for row in range(len(matrix)):
        for col in range(len(matrix[0])):
            if matrix[row][col] == 0:  # Початок нового шляху
                visited = {}
                total_paths += find_trails(matrix, row, col, 0, visited)
                total_visits += sum(visited.values())  # Сума відвідувань усіх клітинок

    return total_paths, total_visits


def main(file_path='2024/day10/input.txt'):
    paths, visits = process_matrix(read_input(file_path))
    print('Part one:', paths)   # 778
    print('Part two:', visits)  # 1925


if __name__ == "__main__":
    main()
