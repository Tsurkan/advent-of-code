def load_data(file_path):
    with open(file_path, 'r') as file:
        return [*map(eval, file)]

# Складість: O(V + E), де: V — кількість вершин, E — кількість ребер
def find_shortest_path(data, target_coordinates, start_index):
    """
    Знайти найкоротший шлях від початку (0,0) до заданих координат
    за допомогою алгоритму пошуку в ширину (BFS).

    Параметри:
    - data: Список точок.
    - target_coordinates: Кортеж, що представляє цільові координати (x, y).
    - start_index: Індекс, з якого почати обробку даних.

    Повертає:
    - Найкоротшу відстань до target_coordinates.
    """
    seen_points = set(data[:start_index])  # Сет вже оброблених точок
    queue = [(0, (0, 0))]  # Черга з кортежів (відстань, координати)

    while queue:
        current_distance, (current_x, current_y) = queue.pop(0)

        if (current_x, current_y) == target_coordinates:
            return current_distance

        # Досліджуємо сусідні точки
        for neighbor_x, neighbor_y in [
            (current_x, current_y + 1),
            (current_x, current_y - 1),
            (current_x + 1, current_y),
            (current_x - 1, current_y),
        ]:
            if (
                (neighbor_x, neighbor_y) not in seen_points
                and 0 <= neighbor_x <= 70
                and 0 <= neighbor_y <= 70
            ):
                queue.append((current_distance + 1, (neighbor_x, neighbor_y)))
                seen_points.add((neighbor_x, neighbor_y))  # Маркуємо точку як відвідану

    return None  # Якщо шлях не знайдено

# Складість: O(log n), де n — кількість елементів в списку
def binary_search_for_target(data, target_coordinates):
    """
    Виконати бінарний пошук для знаходження індексу.

    Параметри:
    - data: Список точок.
    - target_coordinates: Кортеж, що представляє цільові координати (x, y).

    Повертає:
    - Iндекс у списку даних.
    """
    left, right = 1024, len(data)  # Початкові межі пошуку

    while left < right - 1:
        mid = (left + right) // 2  # Знаходимо середину
        if find_shortest_path(data, target_coordinates, mid):  # Перевіряємо наявність шляху
            left = mid  # Якщо шлях є, рухаємо ліву межу вправо
        else:
            right = mid  # Якщо шляху немає, рухаємо праву межу вліво

    return left

def main(file_path='2024/day18/input.txt'):
    data = load_data(file_path)
    target_coordinates = (70, 70)

    print("Part 1:", find_shortest_path(data, target_coordinates, 1024)) # 260

    optimal_index = binary_search_for_target(data, target_coordinates)
    print("Part 2:", *data[optimal_index], sep=',')                      # 24,48

if __name__ == "__main__":
    main()
