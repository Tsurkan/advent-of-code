from collections import deque

# Зміщення для сусідніх клітин (вверх, вниз, ліворуч, праворуч)
NEIGHBOR_OFFSETS = [-1, 1, -1j, 1j]

grid = {
        complex(x, y): cell_value
        for x, row in enumerate(open('2024/day12/input.txt'))
        for y, cell_value in enumerate(row)
        if cell_value != '\n'
    }

def calculate_area_and_perimeter(start_cell, visited_cells=set()):
    # Знаходимо усі з'єднані клітини, починаючи з початкової клітини
    connected_cells = find_connected_cells(start_cell, visited_cells)
    visited_cells.update(connected_cells)
    perimeter = calculate_perimeter(connected_cells) # Обчислюємо периметр з'єднаних клітин
    edges = find_edges(connected_cells) # Знаходимо краї з'єднаних клітин
    
    area = len(connected_cells)
    perimeter_length = perimeter * area
    edge_count = len(edges) * area
    return perimeter_length, edge_count

# Використовується BFS. 
# Складність: O(V + E), де V — кількість клітин (вершин), E — кількість зв'язків між сусідніми клітинами (ребер).
def find_connected_cells(start_cell, visited_cells):
    connected_cells = set()
    
    if start_cell not in visited_cells:
        target_value = grid[start_cell]
        
        queue = deque([start_cell]) # Черга для обходу клітин

        while queue:
            current_cell = queue.popleft()
            
            # Якщо клітина має таке ж значення, додаємо її до з'єднаних клітин
            if grid.get(current_cell) == target_value:
                connected_cells.add(current_cell)
                
                # Додаємо сусідів до черги для обробки
                for offset in NEIGHBOR_OFFSETS:
                    neighbor = current_cell + offset
                    if neighbor not in visited_cells and grid.get(neighbor) == target_value:
                        visited_cells.add(neighbor)
                        queue.append(neighbor)
    return connected_cells

# Обчислюємо периметр з'єднаних клітин
def calculate_perimeter(connected_cells):
    perimeter = 0
    for cell in connected_cells:
        for offset in NEIGHBOR_OFFSETS:
            neighbor = cell + offset
            if grid.get(neighbor) != grid[cell]:
                perimeter += 1
    return perimeter

# Знаходимо краї між з'єднаними клітинами
def find_edges(connected_cells):
    edges = [] 
    
    for direction in NEIGHBOR_OFFSETS:
        for edge_cell in sorted(
            {cell + direction for cell in connected_cells} - connected_cells,
            key=lambda point: (point.real, point.imag)
        ):
            matching_edge_group = next(
                (
                    edge_group
                    for edge_group in edges
                    for point, dir_offset in edge_group
                    if abs(point - edge_cell) == abs(direction) and dir_offset == direction
                ),
                None
            )

            if matching_edge_group:
                matching_edge_group.add((edge_cell, direction))
            else:
                edges.append({(edge_cell, direction)})
    return edges


def main():
    area_perimeters, area_edge_counts = zip(*map(calculate_area_and_perimeter, grid))

    print('Part 1:', sum(area_perimeters))  # 1375476
    print('Part 2:', sum(area_edge_counts)) # 821372


if __name__ == '__main__':
    main()
