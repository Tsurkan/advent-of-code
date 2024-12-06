from utils import timer

def read_map_from_file(file_path):
    """Зчитує карту з текстового файлу."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return [list(line.strip()) for line in file.readlines()]
    
def find_start_position(grid):
    """Знаходит стартову позицію охоронця."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "^":
                return (row, col)
    return None

# Складність: O(n*m), де n и m — розміри карти
# Думаю, що алгоритм можна вважати модифікацією обходу в ширину чи глибину, але 
# з фіксованим порядком руху та поверненням праворуч при зустрічі з перешкодою
def task_1(grid):
    """
    Прогнозує маршрут охоронця та повертає унікальні відвідані позиції.
    
    Алгоритм:
    1. Початкове положення охоронця визначається за маркером '^'.
    2. Охоронець рухається в заданому напрямку, якщо шлях відкритий.
    3. Якщо шлях заблоковано (стіна '#'), охоронець повертає направо.
    4. Алгоритм завершується, коли охоронець виходить за межі карти.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Напрямки: вгору, вправо, вниз, вліво
    direction_index = 0  # Початковий напрямок (вгору)

    # Знаходимо стартову позицію охоронця
    start_position = find_start_position(grid)

    visited = set()  # Унікальні відвідані позиції
    position = start_position  # Поточна позиція
    visited.add(position)

    rows, cols = len(grid), len(grid[0])  # Розміри карти

    while True:
        dr, dc = directions[direction_index]
        next_position = (position[0] + dr, position[1] + dc)

        if not (0 <= next_position[0] < rows and 0 <= next_position[1] < cols):  # Вихід за межі карти
            break

        if grid[next_position[0]][next_position[1]] == "#":  # Стіна
            direction_index = (direction_index + 1) % 4  # Повертаємо направо
        else:  # Вільний шлях
            position = next_position
            visited.add(position)

        if not (0 <= position[0] < rows and 0 <= position[1] < cols):  # Якщо вийшли за межі
            break

    return visited

# Складність: O(k*(n*m)), де k - кількість унікальних позицій які були пройдені в 1 завданні, n и m — розміри карти
# Використовую щось схоже на пошук у глибину (DFS) з можливістю відстеження відвіданих станів
def task_2(grid, start_position, visited_positions):
    """
    Розраховує кількість потенційних пасток (циклічних маршрутів).

    Алгоритм:
    1. Для кожної відвіданої позиції (крім стартової) модифікуємо карту, додаючи перешкоду.
    2. Запускаємо симуляцію руху охоронця на модифікованій карті.
    3. Якщо охоронець потрапляє у нескінченний цикл, позиція вважається пасткою.
    """
    directions = [(-1, 0), (0, 1), (1, 0), (0, -1)]  # Напрямки руху
    infinite_loops_count = 0
    rows, cols = len(grid), len(grid[0])

    def simulate(grid, start_position):
        """
        Симуляція руху охоронця на модифікованій карті.

        Повертає True, якщо охоронець потрапляє у нескінченний цикл, інакше False.
        """
        position = start_position
        direction_index = 0
        history = set()

        while True:
            dr, dc = directions[direction_index]
            next_position = (position[0] + dr, position[1] + dc)

            if not (0 <= next_position[0] < rows and 0 <= next_position[1] < cols):
                return False  # Вихід за межі карти

            if grid[next_position[0]][next_position[1]] == "#":
                direction_index = (direction_index + 1) % 4  # Поворот направо
            else:
                position = next_position

            if (position, direction_index) in history:
                return True  # Нескінченний цикл
            history.add((position, direction_index))

    # Перевіряємо кожну відвідану позицію (крім стартової)
    for r, c in visited_positions - {start_position}:
        modified_grid = [row[:] for row in grid]  # Копіюємо карту
        modified_grid[r][c] = "#"  # Додаємо перешкоду

        if simulate(modified_grid, start_position):  # Перевірка на зациклення
            infinite_loops_count += 1

    return infinite_loops_count


def draw_map(grid, visited_positions):
    """Малює карту з позначеними позиціями, які відвідав охоронець."""
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if (row, col) in visited_positions:
                print("X", end="")
            else:
                print(grid[row][col], end="")
        print()


def main(file_path='2024/day6/input.txt'):
    lab_map = read_map_from_file(file_path)

    visited_positions = task_1(lab_map)
    # draw_map(lab_map, visited_positions)
    
    with timer():
        start_position = find_start_position(lab_map)
        infinite_loops_count = task_2(lab_map, start_position, visited_positions)


    print('Part one:', len(visited_positions)) # 5199
    print('Part two:', infinite_loops_count)   # 1915
    # draw_map(lab_map, visited_positions)

if __name__ == "__main__":
    main()
