# Функция перебирает каждый ход из списка moves, разбирает его на направление и расстояние, 
# добавляет расстояние к предыдущей позиции, вычисляя новую позицию после хода.
# O(n), где n - количество ходов.
def process_moves(moves, instruction = None):
    directions = {"U": (0, -1), "D": (0, 1), "L": (-1, 0), "R": (1, 0)} # соотносим символы направлений с их изменением координат. 
    dig_plan = [(0, 0)] # координаты точек после каждого хода, начиная с начальной точки (0, 0).
    boundary_points = 0 # общее количество шагов

    for line in moves:
        direction, distance, color = line.split()


        if instruction == 'hex':
            color = color[2:-1]
            direction = "RDLU"[int(color[-1])]
            distance = int(color[:-1], 16)
        else:
            distance = int(distance)
            
        dr, dc = directions[direction]
        row, col = dig_plan[-1]

        boundary_points += distance
        dig_plan.append((row + dr * distance, col + dc * distance))
    
    return dig_plan, boundary_points

# Функция использует формулу "Shoelace" для вычисления площади многоугольника по координатам его вершин. 
# https://en.wikipedia.org/wiki/Shoelace_formula
# O(n), где n - количество вершин многоугольника.
def calculate_polygon_area(dig_plan):
    area = 0
    num_points = len(dig_plan)

    # Проходим по координатам вершин многоугольника и суммирует площади трапеций между вершинами.
    for i, (x1, y1) in enumerate(dig_plan):
        x2, y2 = dig_plan[i - 1]
        area += x1 * (y2 - dig_plan[(i + 1) % num_points][1])

    return abs(area) // 2 # Нормализуем площадь.

# Данная функция использует теорему Пика для вычисления количества внутренних точек в многоугольнике на плоскости 
# по известной площади area и количеству граничных точек boundary_points.
# https://en.wikipedia.org/wiki/Pick%27s_theorem
# Эта функция имеет сложность O(1),
def calculate_interior(area, boundary_points):
    return area - boundary_points // 2 + 1

def task_1(file_path):
    with open("2023/day18/input.txt") as file:
        moves = file.readlines()

    dig_plan, boundary_points = process_moves(moves)
    interior_points = calculate_interior(calculate_polygon_area(dig_plan), boundary_points)
    return interior_points + boundary_points

def task_2(file_path):
    with open("2023/day18/input.txt") as file:
        moves = file.readlines()

    dig_plan, boundary_points = process_moves(moves, 'hex')
    interior_points = calculate_interior(calculate_polygon_area(dig_plan), boundary_points)
    return interior_points + boundary_points

# Main function
def main():
    file_path = '2023/day18/input.txt'
    print('Part one:', task_1(file_path)) # 108909
    print('Part two:', task_2(file_path)) # 133125706867777

if __name__ == "__main__":
    main()