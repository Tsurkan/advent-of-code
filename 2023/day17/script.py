from heapq import heappush, heappop

# Define directional movements
UP, DOWN, LEFT, RIGHT = (1, 0), (-1, 0), (0, -1), (0, 1)

# Считываем сетку из файла
def read_grid_from_file(filename):
    """Read the grid from a file and return it as a list."""
    with open(filename) as file:
        return [list(map(int, line.strip())) for line in file]

# Эта функция исследует соседние ячейки и обновляет очередь с приоритетами.
def explore_neighbors(grid, queue, heat_loss, row, col, delta_row, delta_col, steps=1):
    """Explore neighboring cells and update the priority queue.
    
    grid (list of lists) - The grid representation.
    queue (priority queue) - The priority queue holding the cells to be explored.
    heat_loss (numeric) - The current heat loss at the current cell.
    row (int) - The current row index of the cell.
    col (int) - The current column index of the cell.
    delta_row (int) - The change in row index (movement in the row direction).
    delta_col (int) - The change in column index (movement in the column direction).
    steps (int, default=1) - The number of steps taken to reach the current cell.
    """
    new_row, new_col = row + delta_row, col + delta_col

    if 0 <= new_row < len(grid) and 0 <= new_col < len(grid[0]):
        heappush(queue, (heat_loss + grid[new_row][new_col], new_row, new_col, delta_row, delta_col, steps))

# Используем модификацию алгоритма Дейкстры для нахождения кратчайшего пути от начальной точки (0,0) до конечной точки (нижний правый угол).
# Алгоритм работает с использованием очереди с приоритетами для поиска оптимального пути.
def find_shortest_path(grid, max_move, min_move):
    visited = set()
    priority_queue = [(0, 0, 0, 0, 0, 0)]

    while priority_queue:
        heat_loss, row, col, d_row, d_col, steps = heappop(priority_queue)
        
        if row == len(grid) - 1 and col == len(grid[row]) - 1:
            return heat_loss

        if (row, col, d_row, d_col, steps) in visited:
            continue

        visited.add((row, col, d_row, d_col, steps))

        if steps < max_move and (d_row, d_col) != (0, 0):
            explore_neighbors(grid, priority_queue, heat_loss, row, col, d_row, d_col, steps + 1)

        if steps >= min_move or (d_row, d_col) == (0, 0):
            for new_d_row, new_d_col in (UP, DOWN, LEFT, RIGHT):
                if (new_d_row, new_d_col) != (d_row, d_col) and (new_d_row, new_d_col) != (-d_row, -d_col):
                    explore_neighbors(grid, priority_queue, heat_loss, row, col, new_d_row, new_d_col)

   
def task_1(file_path):
    return find_shortest_path(read_grid_from_file(file_path), 3, 1)

def task_2(file_path):
    return find_shortest_path(read_grid_from_file(file_path), 10, 4)

# Main function
def main():
    file_path = '2023/day17/input.txt'
    print('Part one:', task_1(file_path)) # 1110
    print('Part two:', task_2(file_path)) # 1294

if __name__ == "__main__":
    main()