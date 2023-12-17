# Функция для чтения карты вселенной из файла
def read_universe_map(file_path):
    with open(file_path, 'r') as file:
        return file.read().splitlines()

# Определение пустых строк и столбцов
def find_empty_areas(universe):
    empty_rows = [i for i, row in enumerate(universe) if '#' not in row]
    empty_cols = [i for i in range(len(universe[0])) if all(row[i] == '.' for row in universe)]
    return empty_rows, empty_cols

# Функция для расширения вселенной
def expand_universe(universe, empty_rows, empty_cols):
    expanded_universe = []
    empty_cols_str = '.' * len(empty_cols)

    for i, row in enumerate(universe):
        if i in empty_rows:
            expanded_row = row + empty_cols_str  # Дублируем пустую строку
            expanded_universe.append(expanded_row)
        else:
            expanded_row = ''.join(row[j] * 2 if j in empty_cols else row[j] for j in range(len(row)))
        expanded_universe.append(expanded_row)

    return expanded_universe

# Получаем координаты каждой галактики c ее номером
def universe_to_coordinates(universe):
    coordinates = {}
    counter = 1
    
    for row_idx, row in enumerate(universe):
        for col_idx, char in enumerate(row):
            if char == '#':
                coordinates[counter] = (col_idx, row_idx)
                counter += 1
    
    return coordinates

# Функция для вычисления суммы длин кратчайших путей между всеми парами галактик
def calculate_shortest_paths_sum(coordinates):
    distances = {}
    galaxies = len(coordinates) + 1

    for galaxy in range(1, galaxies):
        for pair in range(galaxy + 1, galaxies): 
            distances[(galaxy, pair)] = abs(coordinates[galaxy][0] - coordinates[pair][0]) + abs(coordinates[galaxy][1] - coordinates[pair][1])
    
    return sum(distances.values())

# Функция для вычисления суммы длин кратчайших путей между всеми парами галактик 
# с возможностью увеличить каждый пустой столбец и строчку на large раз.
def calculate_shortest_paths_sum_with_large(coordinates, empty_rows, empty_cols, large = 999999):
    """Используем алгоритм поиска кратчайших путей "Manhattan distance", 
    с добавление строк и столбцов с использованием больших значений. O(n^2).

    Keyword arguments:
    coordinates -- координаты всех вершин
    empty_rows -- номера пустых строк
    empty_cols -- номера пустых столбцов
    large -- на сколько увеличить каждый пустой столбец и строчку (default 999999)

    """
    distances = {}
    excluded_rows = set(empty_rows)
    excluded_cols = set(empty_cols)
    len_galaxies = len(coordinates) + 1

    for galaxy in range(1, len_galaxies):
        for pair in range(galaxy + 1, len_galaxies):
            base_dist = abs(coordinates[galaxy][0] - coordinates[pair][0]) + abs(coordinates[galaxy][1] - coordinates[pair][1])
            adj_dist = 0

            galaxy_y, pair_y = coordinates[galaxy][1], coordinates[pair][1]
            galaxy_x, pair_x = coordinates[galaxy][0], coordinates[pair][0]

            galaxy_y_range = range(galaxy_y, pair_y) if galaxy_y < pair_y else range(pair_y, galaxy_y)
            galaxy_x_range = range(galaxy_x, pair_x) if galaxy_x < pair_x else range(pair_x, galaxy_x)

            for j in excluded_rows:
                if j - 1 in galaxy_y_range:
                    adj_dist += large

            for j in excluded_cols:
                if j - 1 in galaxy_x_range:
                    adj_dist += large

            distances[(galaxy, pair)] = base_dist + adj_dist

    return sum(distances.values())

def task_1(file_path):
    # Чтение карты вселенной из файла
    universe = read_universe_map(file_path)

    # Определение пустых строк и столбцов
    empty_rows, empty_cols = find_empty_areas(universe)

    # Расширение вселенной
    expanded_universe = expand_universe(universe, empty_rows, empty_cols)

    # Получаем координаты каждой галактики
    coordinates_galaxies = universe_to_coordinates(expanded_universe)

    # Вычисление суммы длин кратчайших путей
    sum_of_paths = calculate_shortest_paths_sum(coordinates_galaxies)

    return sum_of_paths

def task_2(file_path):
    universe = read_universe_map(file_path)
    empty_rows, empty_cols = find_empty_areas(universe)
    coordinates_galaxies = universe_to_coordinates(universe)
    sum_of_paths = calculate_shortest_paths_sum_with_large(coordinates_galaxies, empty_rows, empty_cols, 999999)
    return sum_of_paths


# Main function
def main():
    file_path = '2023/day11/input.txt'
    print('Part one:', task_1(file_path)) # 9329143
    print('Part two:', task_2(file_path)) # 710674907809

if __name__ == "__main__":
    main()