def read_input(file_path):
    return [line.strip() for line in open(file_path, "r")]

# Складність: O(N*M), де N — кількість рядків, M — кількість стовпців.
def prepare_coordinates(lines):
    # Створюємо словник, де кожен унікальний символ матриці буде ключем, а значенням - список координат, де цей символ зустрічається.
    coordinates = {}
    for r, line in enumerate(lines):
        for c, char in enumerate(line):
            if char != '.':
                if char not in coordinates:
                    coordinates[char] = []
                coordinates[char].append((r, c))
    return coordinates

def trace_line(r, c, dr, dc, nr, nc, result_set, part):
    # Рухаємося вказаним напрямком
    while 0 <= r < nr and 0 <= c < nc:
        result_set.add((r, c))
        if part == 1:  # Для part1 додаємо лише перший крок
            break
        r, c = r + dr, c + dc

# Складність: O(N * M + кількість пар символів * (N + M))
def find_nodes(coordinates, nr, nc, part):
    result_set = set()
    
    for points in coordinates.values():
        n = len(points)
        for i in range(n):
            for j in range(i + 1, n):
                ri, ci = points[i]
                rj, cj = points[j]
                dr, dc = rj - ri, cj - ci  # Напрямок руху
                
                # Для part == 2 додаємо кінцеві точки
                if part == 2:
                    result_set.update([(ri, ci), (rj, cj)])
                
                # Рух уперед і назад по лінії
                trace_line(rj + dr, cj + dc, dr, dc, nr, nc, result_set, part)
                trace_line(ri - dr, ci - dc, -dr, -dc, nr, nc, result_set, part)

    return result_set

def main(file_path='2024/day8/input.txt'):
    lines = read_input(file_path)
    nr, nc = len(lines), len(lines[0])
    coordinates = prepare_coordinates(lines)
    
    print('Part one:', len(find_nodes(coordinates, nr, nc, part=1))) # 357
    print('Part two:', len(find_nodes(coordinates, nr, nc, part=2))) # 1266


if __name__ == "__main__":
    main()
