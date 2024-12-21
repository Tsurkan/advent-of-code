import heapq

# Складність: O(N*M), де N — кількість рядків у файлі, а M — кількість стовпців у кожному рядку
def read_input(file_path):
    """Читання та обробка вхідних даних з файлу."""
    grid = []
    start = None
    end = None
    with open(file_path) as file:
        for row_index, line in enumerate(file):
            row = list(line.strip())  # Перетворюємо рядок в список символів
            grid.append(row)
            for col_index, cell in enumerate(row):
                if cell == 'S':  # Знайшли стартову точку
                    start = (row_index, col_index)
                elif cell == 'E':  # Знайшли кінцеву точку
                    end = (row_index, col_index)
    return grid, start, end

def draw_grid(grid):
    """Виведення сітки в консоль."""
    for row in grid:
        print(''.join(row))

# Складність: O(E log V), де E — кількість ребер, а V — кількість вершин.
def a_star(grid, start, end):
    """Реалізація алгоритму A* для пошуку найкоротшого шляху між двома точками на сітці."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Можливі напрямки руху
    distances = {start: 0}  # Відстань від старту до кожної точки
    parent = {}  # Батьківська точка для відтворення шляху
    priority_queue = [(0, start)]  # Черга пріоритетів (відстань, точка)

    def heuristic(a, b):
        """Евристична функція для оцінки відстані між двома точками (манхеттенська відстань)."""
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    while priority_queue:
        _, (current_row, current_col) = heapq.heappop(priority_queue)  # Вибір поточної точки

        if (current_row, current_col) == end:  # Якщо знайшли кінцеву точку
            break

        for d_row, d_col in directions:
            new_row, new_col = current_row + d_row, current_col + d_col  # Нові координати

            # Перевірка на вихід за межі сітки
            if not (0 <= new_row < len(grid) and 0 <= new_col < len(grid[0])):
                continue

            # Якщо клітинка є стіною, пропускаємо її
            if grid[new_row][new_col] == '#':
                continue

            new_distance = distances[(current_row, current_col)] + 1  # Відстань до нової точки

            # Якщо нова точка ще не відвідана або знайдена коротша відстань
            if (new_row, new_col) not in distances or new_distance < distances[(new_row, new_col)]:
                distances[(new_row, new_col)] = new_distance
                parent[(new_row, new_col)] = (current_row, current_col)  # Встановлюємо батьківську точку
                priority = new_distance + heuristic((new_row, new_col), end)  # Пріоритет
                heapq.heappush(priority_queue, (priority, (new_row, new_col)))  # Додаємо в чергу

    # Відновлення шляху з кінцевої точки до старту
    path = []
    current = end
    while current in parent:
        path.append(current)
        current = parent[current]
    path.append(start)
    path.reverse()

    return set(path), distances

# Складність: O(K * N * M), де K — кількість можливих напрямків (4), а N, M — розміри решітки.
def compute_shortcuts(grid, original_path, distances):
    """Обчислення потенційних коротших шляхів."""
    directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    shortcut_opportunities = {}

    for row, col in original_path:
        for d_row, d_col in directions:
            adj_row, adj_col = row + 2 * d_row, col + 2 * d_col  # Переміщаємось на два кроки

            if (adj_row, adj_col) not in distances:
                continue

            # Якщо знайдена можливість для коротшого шляху
            if distances[(row, col)] + 2 < distances[(adj_row, adj_col)]:
                delta = distances[(adj_row, adj_col)] - (distances[(row, col)] + 2)
                shortcut_opportunities[delta] = shortcut_opportunities.get(delta, 0) + 1

    return shortcut_opportunities

def analyze_cheatspace():
    """Створення простору для потенційних обходів."""
    cheatspace = {}

    for i in range(-20, 21):
        for j in range(-20, 21):
            if abs(i) + abs(j) <= 20 and (abs(i) >= 2 or abs(j) >= 2):
                key = abs(i) + abs(j)
                if key not in cheatspace:
                    cheatspace[key] = []
                cheatspace[key].append((i, j))

    return cheatspace

# Складність: O(K * N * M), де K — кількість можливих варіантів читерських обходів, а N, M — розміри решітки.
def find_cheats_in_path(original_path, distances, cheatspace):
    """Пошук варіантів для оптимізації шляху через читерські обходи."""
    cheats = {}

    for row, col in original_path:
        for key, points in cheatspace.items():
            for d_row, d_col in points:
                new_row, new_col = row + d_row, col + d_col  # Переміщаємось за координатами з читерського простору

                if (new_row, new_col) not in distances:
                    continue

                if distances[(row, col)] + key < distances[(new_row, new_col)]:
                    delta = distances[(new_row, new_col)] - (distances[(row, col)] + key)
                    cheats[delta] = cheats.get(delta, 0) + 1

    return cheats

def visualize_path(grid, path):
    """Відображення шляху на сітці."""
    for row, col in path:
        if grid[row][col] not in ('S', 'E'):
            grid[row][col] = '*'  # Позначаємо клітинки шляху зірочкою

def part1(shortcut_opportunities):
    return sum(value for key, value in shortcut_opportunities.items() if key >= 100)

def part2(cheats):
    sorted_keys = sorted(cheats.keys(), reverse=True)
    return sum(cheats[key] for key in sorted_keys if key >= 100)

def main(file_path="2024/day20/input.txt"):
    grid, start, end = read_input(file_path)

    original_path, distances = a_star(grid, start, end)
    shortcut_opportunities = compute_shortcuts(grid, original_path, distances)  # Обчислення коротших шляхів
    cheatspace = analyze_cheatspace()  # Створення простору для обходів
    cheats = find_cheats_in_path( original_path, distances, cheatspace)  # Пошук читерських обходів

    # visualize_path(grid, original_path)
    # draw_grid(grid)

    print('Part 1:', part1(shortcut_opportunities)) # 1389
    print('Part 2:', part2(cheats))                 # 1005068

if __name__ == "__main__":
    main()
