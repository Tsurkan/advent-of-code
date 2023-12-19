from collections import deque

def add(row, col, dr, dc, visited, queue):
    """Функция добавляет новые координаты в очередь для последующего посещения
    и помечает их как посещенные. Принимает аргументы:

    row: текущая строка
    col: текущий столбец
    dr: изменение в строке (delta row)
    dc: изменение в столбце (delta column)
    visited: множество посещенных координат
    queue: очередь для обхода
    """
    
    # Проверяем, были ли данные координаты посещены
    if (row, col, dr, dc) not in visited:
        visited.add((row, col, dr, dc))
        queue.append((row, col, dr, dc)) # Добавляем координаты в очередь для последующего посещения

# Функция для обхода сетки. Использует BFS для нахождения координат, 
# которые можно достичь согласно определенным правилам, связанным с символами на сетке.
# Возвращает множество посещенных координат.
def calculate(grid, ir, ic, idr, idc):
    queue = deque([(ir, ic, idr, idc)]) # Начальные координаты
    visited = set() # Множество для отслеживания посещенных координат

    while queue:
        row, col, dr, dc = queue.popleft()

        row += dr
        col += dc

        # Проверяем, находятся ли координаты в пределах сетки
        if not (0 <= row < len(grid) and 0 <= col < len(grid[row])):
            continue

        char = grid[row][col] # Получаем символ по текущим координатам

        # Проверяем символы и изменяем направление движения в зависимости от символов
        if char == "." or (dc != 0 and ("|-" in char)):
            add(row, col, dr, dc, visited, queue)

        elif char == "/":
            dr, dc = -dc, -dr  # Поворачиваем налево
            add(row, col, dr, dc, visited, queue)

        elif char == "\\":
            dr, dc = dc, dr  # Поворачиваем направо
            add(row, col, dr, dc, visited, queue)

        elif char == "|":
            for dr, dc in ((1, 0), (-1, 0)):  # Движение вверх и вниз
                add(row, col, dr, dc, visited, queue)

        elif char == "-":
            for dr, dc in ((0, 1), (0, -1)):  # Движение вправо и влево
                add(row, col, dr, dc, visited, queue)

    # множество координат, которые были посещены
    return len({(row, col) for row, col, _, _ in visited})

def task_1(file_path):
    with open(file_path) as file:
        grid = [line.strip() for line in file.readlines()]
    
    return calculate(grid, 0, -1, 0, 1)

def task_2(file_path):
    with open(file_path) as file:
        grid = [line.strip() for line in file.readlines()]

    max_energized = 0
    grid_rows = len(grid)
    grid_cols = len(grid[0])

    # Можем начать с любого угла
    for row in range(grid_rows):
        max_energized = max(max_energized, calculate(grid, row, -1, 0, 1))
        max_energized = max(max_energized, calculate(grid, row, len(grid[row]), 0, -1))

    for col in range(grid_cols):
        max_energized = max(max_energized, calculate(grid, -1, col, 1, 0))
        max_energized = max(max_energized, calculate(grid, len(grid), col, -1, 0))

    return max_energized

def main():
    file_path = '2023/day16/input.txt'
    print('Part one:', task_1(file_path)) # 7562
    print('Part two:', task_2(file_path)) # 7793

if __name__ == "__main__":
    main()