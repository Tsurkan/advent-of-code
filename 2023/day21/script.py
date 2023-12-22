from collections import deque

# Функция находит начальную точку "S" в лабиринте, определяя её координаты.
# O(n * m), где n - количество строк в лабиринте, а m - максимальная длина строки.
def find_starting_point(lines):
    for y, line in enumerate(lines):
        for x, character in enumerate(line):
            if character == "S":
                return x, y

# Эта функция проверяет, является ли заданное перемещение допустимым:
#   Не выходит ли за границы лабиринта.
#   Не является ли целевая клетка препятствием или уже посещенной.
#  Сложность данной функции будет O(1).
def is_valid_move(row, col, lines, visited):
    return (
        0 <= row < len(lines)
        and 0 <= col < len(lines[0])
        and (row, col) not in visited
        and lines[row][col] not in {"#", "@"}
    )

# Эта функция использует BFS для исследования лабиринта из начальной точки "S". 
# Она перемещается в четыре направления (вверх, вниз, влево, вправо) на каждом шаге, 
# сохраняя посещенные участки каждый второй шаг.
# В худшем случае сложность BFS O(n * m), где n - количество строк в лабиринте, а m - максимальная длина строки. 
# Однако в данной реализации алгоритм ограничен 64 шагами, поэтому его сложность ограничена константой.
def explore_maze(lines):
    start_x, start_y = find_starting_point(lines)
    plots = set()
    visited = {(start_x, start_y)}
    queue = deque([(start_x, start_y, 64)]) # по условию нужно ограничить в 64 шага

    while queue:
        x, y, steps = queue.popleft()

        if steps % 2 == 0:
            plots.add((x, y))

        if steps == 0:
            continue

        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            new_x, new_y = x + dx, y + dy

            if is_valid_move(new_x, new_y, lines, visited):
                visited.add((new_x, new_y))
                queue.append((new_x, new_y, steps - 1))

    return len(plots)

def task_1(file_path):
    with open(file_path) as file:
        lines = [line.strip() for line in file]
    return explore_maze(lines)

# Основная идея - генерировать и заполнять карту пошагово, сохраняя и обновляя доступные позиции на каждом шаге, 
# и возвращать количество позиций на определенных этапах этого заполнения.

# О(n * m), где n - число шагов, m - количество возможных позиций.
def fill_map(matrix, start):
    """
    Generates positions based on certain rules within a matrix.

    Args:
    - matrix (list): Matrix representation.
    - start (tuple): Starting position coordinates.

    Yields:
    - int: Count of positions at specific steps.
    """
    positions = {start}
    matrix_dimension = len(matrix) # 131

    starting_step = matrix_dimension // 2           # 65 = the starting step for positions.
    steps = matrix_dimension * 2 + starting_step    # 327 = total steps to positions.
    
    for current_step in range(steps): # можно вписать любое число больше 327 потому, что мы дальше просто повторяем ромбы
        next_positions = calculate_next_positions(positions, matrix)
        positions = next_positions

        if current_step % matrix_dimension + 1 == starting_step:
            yield len(positions)

# Функция ищет следующие точки для движения по принцыпу BFS. Но в данном случае она не строит граф и 
# не ищет кратчайший путь, а просто исследует доступные соседние клетки относительно текущей позиции, 
# чтобы определить, куда можно перейти из текущего положения.
# O(n), где n - количество текущих позиций.
def calculate_next_positions(positions, matrix):
    """
    Calculates the next set of positions based on certain conditions.

    Args:
    - positions (set): Current set of positions.
    - matrix (list): Matrix representation.

    Returns:
    - set: New set of positions based on movement conditions.
    """
    new_positions = set()
    for position in positions:
        x = position[0]
        y = position[1]
        for x_move, y_move in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
            if matrix[(y + y_move) % len(matrix)][(x + x_move) % len(matrix[0])] == '.':
                new_positions.add((x + x_move, y + y_move))
    return new_positions

# Заполняем матрицу и находим координаты начальной точки "S".
# O(rows * cols), где rows - количество строк, cols - средняя длина строки.
def initialize_matrix(input_file):
    """
    Reads an input file and initializes the matrix and find start position.

    Args:
    - input_file (str): Path to the file describing the matrix.

    Returns:
    - tuple: Matrix and start position.
    """
    matrix = []
    start = None

    with open(input_file) as file:
        for y, line in enumerate(file.readlines()):
            matrix.append([])
            for x, char in enumerate(line.rstrip()):
                if char == 'S':
                    start = (x, y)
                    matrix[y].append('.')
                else:
                    matrix[y].append(char)
                    
    return matrix, start

# По комментариям из reddi я понял, что большинство будет вычислять полином Лагранжа через необходимое количество шагов 
# (26501365 % 131 = 65) и форму ромба входной сетки в данных. Я использую форму ромба разницу между интервалами шагов.
# O(steps)
def calculate_values(dimension, positions, steps):
    """
    Performs calculations based on generated positions.

    Args:
    - dimension (int): Matrix dimension.
    - positions (generator): Generated positions.
    - steps (int): Total steps.

    Returns:
    - int: Result based on positions.
    """
    positions_list = list(positions) # [3893, 34785, 96471]
    
    current_step = dimension
    step_difference = positions_list[1] - positions_list[0] # 30892
    difference_step = positions_list[2] - positions_list[1] # 61686
    difference = difference_step - step_difference          # 30794
    result = positions_list[1]
    
    # Кожного разу додаємо різницю між інтервалами. Так як перша ітеріція починається в (65, 65), то умова виходу зменшується на 65.
    while current_step != steps - dimension // 2:
        current_step += dimension
        result += difference_step
        difference_step += difference
    return result

# I learned about the rhombus shape of the input grid on the forum. This information helped a lot with the denouement.
def task_2(file_path):
    matrix, start_position = initialize_matrix("2023/day21/input.txt") # start_position = (65, 65)
    positions = fill_map(matrix, start_position)
    return calculate_values(len(matrix), positions, 26501365) # По условию шагов 26501365

# Main function
def main():
    file_path = '2023/day21/input.txt'
    print('Part one:', task_1(file_path)) # 3795
    print('Part two:', task_2(file_path)) # 630129824772393

if __name__ == "__main__":
    main()