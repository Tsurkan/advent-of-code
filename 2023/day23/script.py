# Создает список смежности для заданного графа. Этот список смежности отображает связи между ячейками сетки.
# O(N*M), где N - количество строк, а M - средняя длина строк.
def create_adjacency_list(data):
    adjacency = {}
    for r, row in enumerate(data):
        for c, cell_value in enumerate(row):
            if cell_value == ".":
                for dr, dc in [(-1, 0), (0, -1), (0, 1), (1, 0)]:
                    adj_row, adj_col = r + dr, c + dc
                    if not (0 <= adj_row < len(data) and 0 <= adj_col < len(row)):
                        continue
                    if data[adj_row][adj_col] == ".":
                        adjacency.setdefault((r, c), set()).add((adj_row, adj_col))
                        adjacency.setdefault((adj_row, adj_col), set()).add((r, c))
            if cell_value == ">":
                adjacency.setdefault((r, c), set()).add((r, c + 1))
                adjacency.setdefault((r, c - 1), set()).add((r, c))
            if cell_value == "v":
                adjacency.setdefault((r, c), set()).add((r + 1, c))
                adjacency.setdefault((r - 1, c), set()).add((r, c))
    return adjacency

# Ищет самый длинный путь в графе, представленном списком смежности, используя обход в ширину (BFS) с поддержанием очереди.
# O(V+E), где V - количество вершин, а E - количество рёбер в графе.
def find_longest_path(adj_list, rows, cols):
    queue = [(0, 1, 0)]
    visited = set()
    best_distance = 0

    while queue:
        current_row, current_col, distance = queue.pop()
        if distance == -1:
            visited.remove((current_row, current_col))
            continue
        if (current_row, current_col) == (rows - 1, cols - 2):
            best_distance = max(best_distance, distance)
            continue
        if (current_row, current_col) in visited:
            continue
        visited.add((current_row, current_col))
        queue.append((current_row, current_col, -1))
        for adj_row, adj_col in adj_list[(current_row, current_col)]:
            queue.append((adj_row, adj_col, distance + 1))

    return best_distance

# Создает список смежности для графа, но делает это по условию из второй части.
# O(N*M), где N - количество строк в data, а M - средняя длина строк.
def create_adjacency(data):
    edges = {}
    directions = [(-1, 0), (0, -1), (0, 1), (1, 0)]
    rows, cols = len(data), len(data[0])

    def is_valid_cell(row, col):
        return 0 <= row < rows and 0 <= col < cols

    for r, row in enumerate(data):
        for c, v in enumerate(row):
            if v in ".>v":
                edges.setdefault((r, c), set())
                for dr, dc in directions:
                    ar, ac = r + dr, c + dc
                    if is_valid_cell(ar, ac) and data[ar][ac] in ".>v":
                        edges[(r, c)].add((ar, ac, 1))
                        edges.setdefault((ar, ac), set()).add((r, c, 1))
    return edges

# Модифицирует список смежности, удаляя узлы с ровно двумя связями и объединяя их связи для упрощения графа.
# O(V*E), где V - количество вершин, а E - количество рёбер в графе
def remove_degree_two_nodes(adj_list):
    modified_adjacency = adj_list.copy()

    while True:
        for node, edges in modified_adjacency.items():
            if len(edges) == 2:
                edge_a, edge_b = edges
                modified_adjacency[edge_a[:2]].remove(node + (edge_a[2],))
                modified_adjacency[edge_b[:2]].remove(node + (edge_b[2],))
                modified_adjacency[edge_a[:2]].add((edge_b[0], edge_b[1], edge_a[2] + edge_b[2]))
                modified_adjacency[edge_b[:2]].add((edge_a[0], edge_a[1], edge_a[2] + edge_b[2]))
                del modified_adjacency[node]
                break
        else:
            break

    return modified_adjacency

# Ищет самый длинный путь в измененном графе (после удаления узлов с двумя связями) используя обход в ширину (BFS) с поддержанием очереди.
# O(V*E), где V - количество вершин, а E - количество рёбер в графе
def find_longest_path_modified(adj_list_modified, rows, cols):
    queue = [(0, 1, 0)]
    visited = set()
    best_length = 0

    while queue:
        current_row, current_col, length = queue.pop()
        if length == -1:
            visited.remove((current_row, current_col))
            continue
        if (current_row, current_col) == (rows - 1, cols - 2):
            best_length = max(best_length, length)
            continue
        if (current_row, current_col) in visited:
            continue
        visited.add((current_row, current_col))
        queue.append((current_row, current_col, -1))
        for adj_row, adj_col, l in adj_list_modified[(current_row, current_col)]:
            queue.append((adj_row, adj_col, length + l))

    return best_length

def task_1(file_path):
    with open(file_path) as file:
        grid_data = file.read().strip().splitlines()

    rows, cols = len(grid_data), len(grid_data[0])
    return find_longest_path(create_adjacency_list(grid_data), rows, cols)

def task_2(file_path):
    with open(file_path) as file:
        grid_data = file.read().strip().splitlines()

    rows, cols = len(grid_data), len(grid_data[0])
    return find_longest_path_modified(remove_degree_two_nodes(create_adjacency(grid_data)), rows, cols)

# Main function
def main():
    file_path = '2023/day23/input.txt'
    print('Part one:', task_1(file_path)) # 2386
    print('Part two:', task_2(file_path)) # 6246

if __name__ == "__main__":
    main()