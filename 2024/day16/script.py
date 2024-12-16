import heapq
from collections import deque

# Константи
MOVE_COST = 1  # Вартість переміщення на одну клітинку
TURN_COST = 1000  # Вартість повороту

DIRECTIONS = {
    "right": (1, 0),  # Напрямок вправо
    "down": (0, 1),   # Напрямок вниз
    "left": (-1, 0),  # Напрямок вліво
    "up": (0, -1),    # Напрямок вгору
}
ROTATION_ORDER = ["right", "down", "left", "up"]  # Порядок обертання

# Функція для пошуку найкоротшого шляху за алгоритмом Дейкстри
def dijkstra_shortest_path(start_position, walkable_cells):
    """
    Використовується алгоритм Дейкстри для пошуку найкоротшого шляху в графі.
    Складність: O(V + E * log(V)), де V - кількість вершин, E - кількість ребер.
    """
    priority_queue = []  # Черга з пріоритетом
    visited_states = {}  # Відвідані стани

    # Додаємо початкову точку до черги
    heapq.heappush(priority_queue, (0, "right", start_position))
    visited_states[(start_position, "right")] = 0

    while priority_queue:
        # Отримуємо елемент з найменшою вартістю
        current_cost, current_direction, (current_x, current_y) = heapq.heappop(priority_queue)

        # Пропускаємо стан, якщо знайдено більш короткий шлях
        if visited_states.get(((current_x, current_y), current_direction), float('inf')) < current_cost:
            continue

        # Рухаємося вперед у поточному напрямку
        dx, dy = DIRECTIONS[current_direction]
        next_position = (current_x + dx, current_y + dy)

        if next_position in walkable_cells:
            new_cost = current_cost + MOVE_COST
            if new_cost < visited_states.get((next_position, current_direction), float('inf')):
                visited_states[(next_position, current_direction)] = new_cost
                heapq.heappush(priority_queue, (new_cost, current_direction, next_position))

        # Виконуємо повороти вліво та вправо
        for turn_offset in [-1, 1]:
            new_direction = ROTATION_ORDER[(ROTATION_ORDER.index(current_direction) + turn_offset) % 4]
            new_cost = current_cost + TURN_COST
            if new_cost < visited_states.get(((current_x, current_y), new_direction), float('inf')):
                visited_states[((current_x, current_y), new_direction)] = new_cost
                heapq.heappush(priority_queue, (new_cost, new_direction, (current_x, current_y)))

    return visited_states

def parse_input(file_path):
    """
    Зчитує початкову і кінцеву позиції та прохідні клітинки.
    """
    start_position, end_position, walkable_cells = (-1, -1), (-1, -1), set()

    with open(file_path) as file:
        for y, line in enumerate(file):
            for x, char in enumerate(line.strip()):
                if char == "E":  # Кінцева позиція
                    end_position = (x, y)
                    walkable_cells.add((x, y))
                elif char == "S":  # Початкова позиція
                    start_position = (x, y)
                    walkable_cells.add((x, y))  # Початкова клітинка також прохідна
                elif char == ".":  # Прохідна клітинка
                    walkable_cells.add((x, y))

    return start_position, end_position, frozenset(walkable_cells)

# Відновлення шляху за результатами
def reconstruct_path(visited_states, target_state):
    """
    Відновлює шлях до цільової точки на основі збережених станів.
    """
    backtrack_queue = deque([target_state])
    reconstructed_path = set()

    while backtrack_queue:
        current_position, current_direction = backtrack_queue.popleft()
        reconstructed_path.add(current_position)

        # Зворотній рух
        dx, dy = DIRECTIONS[current_direction]
        previous_position = (current_position[0] - dx, current_position[1] - dy)
        if visited_states.get((previous_position, current_direction), float('inf')) + MOVE_COST == visited_states.get((current_position, current_direction), float('inf')):
            backtrack_queue.append((previous_position, current_direction))

        # Повороти
        for turn_offset in [-1, 1]:
            new_direction = ROTATION_ORDER[(ROTATION_ORDER.index(current_direction) + turn_offset) % 4]
            if visited_states.get((current_position, new_direction), float('inf')) + TURN_COST == visited_states.get((current_position, current_direction), float('inf')):
                backtrack_queue.append((current_position, new_direction))

    return reconstructed_path

def part_1(file_path):
    """
    Обчислює вартість найкоротшого шляху від старту до фінішу.
    """
    start_position, end_position, walkable_cells = parse_input(file_path)
    visited_states = dijkstra_shortest_path(start_position, walkable_cells)
    shortest_path_cost = min(
        cost for (position, _), cost in visited_states.items() if position == end_position
    )
    return shortest_path_cost

def part_2(file_path):
    """
    Обчислює довжину відновленого шляху використовуючи всю логіку part_1.
    """
    start_position, end_position, walkable_cells = parse_input(file_path)
    visited_states = dijkstra_shortest_path(start_position, walkable_cells)
    shortest_path_cost = min(
        cost for (position, _), cost in visited_states.items() if position == end_position
    )
    #######################################################################################
    
    target_state = next(
        state for state, cost in visited_states.items() if state[0] == end_position and cost == shortest_path_cost
    )
    reconstructed_path = reconstruct_path(visited_states, target_state)
    return len(reconstructed_path)

# Головна функція
def main(file_path='2024/day16/input.txt'):
    print('Part one:', part_1(file_path)) # 143564
    print('Part two:', part_2(file_path)) # 593

if __name__ == '__main__':
    main()
