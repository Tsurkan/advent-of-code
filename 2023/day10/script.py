# Функция читает содержимое построчно, удаляя символы новой строки (\n). 
# Она возвращает список строк, представляющих собой сетку.
def read_grid_from_file(file_name):
    with open(file_name) as file:
        return [line.strip() for line in file]

# Функция создает словарь, отображающий символы трубопроводов на числовые значения. 
# Значения в этом словаре были сконструированы таким образом, чтобы каждый символ трубопровода 
# соответствовал определенному числовому значению при использовании битовых операций. 
# Например, 16644 может быть представлено в двоичной системе как 100000011011100, где каждые 
# два бита представляют направление трубы (например, 10 может обозначать вертикальную трубу, 
# cледующие два бита 00 могут представлять, отсутствие трубы и так далее.
def create_pipe_types():
    return {
        '|': 16644,  # Вертикальная труба: 100000011011100
        '-': 1344,   # Горизонтальная труба: 10100110000
        'L': 1284,   # Изгиб, соединяющий север и восток: 10100000100
        'J': 324,    # Изгиб, соединяющий север и запад: 101000100
        '7': 16704,  # Изгиб, соединяющий юг и запад: 100000111000
        'F': 17664,  # Изгиб, соединяющий юг и восток: 100010011000
        'S': 17988,  # Начальная позиция: 1000110111100
        '.': 0       # Пустое место
    }

# Функция преобразует символы сетки в числа, представляющие различные направления трубопроводов, 
# и добавляет их в одномерный список grid. Здесь используется битовая операция >> для получения 
# конкретных значений из числовых представлений трубопроводов.
# O(R*C), где R - количество строк в сетке, а C - средняя длина строки.
def create_pipeline_grid(grid_data, pipe_types):
    grid = []
    for row in grid_data:
        for i in (0, 6, 12):
            for char in row:
                for j in (0, 2, 4):
                    value = (pipe_types[char] >> i + j) & 3
                    grid.append(value)
    return grid

# Функция подсчитывает закрытые тайлы в сетке, используя поиск в ширину (BFS). 
# Она итеративно проходит через соседние тайлы от начальных позиций, помечая посещенные тайлы и подсчитывая закрытые тайлы.
# O(E+V), где E - количество ребер, V - количество вершин
def count_closed_tiles(n, grid, s, v=0):
    visited = set()
    result = 0
    for q in s:
        for p in (q - n, q + n, q + 1, q - 1):
            if v <= grid[p] < 2 and p not in visited:
                visited.add(p)
                result += 1
                grid[p] = 2
                s.append(p)
    return result

def solve_tasks(grid, n):
    start_positions = [i for i, val in enumerate(grid) if val == 2]
    result_task1 = (count_closed_tiles(n, grid, start_positions, 1) - 1) // 6
    result_task2 = count_closed_tiles(n, grid, [0]) and n * n // 9 - sum(grid[n * i + 1:n * i + n + 1:3].count(2) for i in range(1, n, 3))
    return result_task1, result_task2

# Main function
def main(file_path):
    grid_data = read_grid_from_file(file_path)
    grid = create_pipeline_grid(grid_data, create_pipe_types())
    return solve_tasks(grid, 3 * len(grid_data))

if __name__ == "__main__":
    file_path = '2023/day10/input.txt'
    
    task1, task2 = main(file_path)
    print('Part one:', task1) # 6903
    print('Part two:', task2) # 265