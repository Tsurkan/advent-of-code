from collections import deque

# O(n * m), где n - количество кирпичей в файле, m - количество измерений у каждого кирпича.
def read_bricks_from_file(file_name):
    """
    Read brick from a file.
    """
    with open(file_name) as file:
        bricks = []
        for line in file:
            line = line.replace("~", ",").split(",")
            bricks.append([int(item) for item in line])
        return bricks

# Функция сортирует кирпичи по их высоте, используя третье измерение каждого кирпича.
# O(n log n), где n - количество кирпичей.
def sort_bricks_by_height(bricks):
    """
    Sort bricks by their height.
    """
    return sorted(bricks, key=lambda brick: brick[2])

# Эта функция корректирует высоту каждого кирпича на основе отношений поддержки между ними. 
# Она проверяет каждый кирпич и устанавливает его высоту в зависимости от максимальной высоты, 
# на которой он может находиться без пересечения с другими кирпичами.
# O(n^2), где n - количество кирпичей.
def adjust_brick_heights(bricks):
    """
    Adjust brick heights based on support relationships.
    """
    for i, brick in enumerate(bricks):
        max_supported_z = 1
        for prev_brick in bricks[:i]:
            if do_bricks_intersect(brick, prev_brick):
                max_supported_z = max(max_supported_z, prev_brick[5] + 1)
        brick[5] -= brick[2] - max_supported_z
        brick[2] = max_supported_z

# Эта функция проверяет, пересекаются ли два кирпича.
# Сложность: O(1)
def do_bricks_intersect(brick_a, brick_b):
    """
    Check if two bricks intersect.
    """
    start_a, start_b = brick_a[0], brick_b[0]
    end_a, end_b = brick_a[3], brick_b[3]
    start_a_z, start_b_z = brick_a[1], brick_b[1]
    end_a_z, end_b_z = brick_a[4], brick_b[4]

    return (
        max(start_a, start_b) <= min(end_a, end_b) and
        max(start_a_z, start_b_z) <= min(end_a_z, end_b_z)
    )

# Эта функция находит отношения поддержки между кирпичами, 
# то есть кирпичи, которые могут поддерживать другие кирпичи.
# O(n^2), где n - количество кирпичей.
def find_support_relationships(bricks):
    """
    Find support relationships between bricks.
    """
    upper_supports_lower = {upper_index: set() for upper_index in range(len(bricks))}
    lower_supports_upper = {lower_index: set() for lower_index in range(len(bricks))}

    for upper_index, upper_brick in enumerate(bricks):
        for lower_index, lower_brick in enumerate(bricks[:upper_index]):
            if do_bricks_intersect(lower_brick, upper_brick) and upper_brick[2] == lower_brick[5] + 1:
                upper_supports_lower[lower_index].add(upper_index)
                lower_supports_upper[upper_index].add(lower_index)

    return upper_supports_lower, lower_supports_upper

# Эта функция подсчитывает количество кирпичей, которые поддерживаются как минимум двумя другими снизу.
# O(n^2), где n - количество кирпичей. 
def count_supported_bricks(bricks, upper_supports_lower, lower_supports_upper):
    """
    Count bricks supported by at least two below.
    """
    count = 0
    for i in range(len(bricks)):
        if i not in upper_supports_lower:
            upper_supports_lower[i] = set()
        for j in upper_supports_lower[i]:
            if len(lower_supports_upper[j]) < 2:
                break
        else:
            count += 1
    return count

def task_1(file_path):
    bricks = sort_bricks_by_height(read_bricks_from_file(file_path))
    adjust_brick_heights(bricks)
    upper_supports_lower, lower_supports_upper = find_support_relationships(bricks)
    return count_supported_bricks(bricks, upper_supports_lower, lower_supports_upper)

# Функция использует алгоритм обхода в ширину (BFS) для подсчета кирпичей.
# O(V + E), где V - количество вершин (кирпичей), а E - количество ребер (отношений поддержки)
def calculate_supported_bricks_count(bricks, upper_supports_lower, lower_supports_upper):
    """
    Determines the number of bricks that satisfy certain conditions.
    """
    count = 0
    for i in range(len(bricks)):
        queue = deque(
            item_index
            for item_index in upper_supports_lower[i]
            if len(lower_supports_upper[item_index]) == 1
        )
        visited = set(queue)

        while queue:
            j = queue.popleft()

            for k in upper_supports_lower[j] - visited:
                if lower_supports_upper[k] <= visited:
                    queue.append(k)
                    visited.add(k)

        count += len(visited)

    return count

def task_2(file_path):
    bricks = sort_bricks_by_height(read_bricks_from_file(file_path))
    adjust_brick_heights(bricks)
    upper_supports_lower, lower_supports_upper = find_support_relationships(bricks)
    return calculate_supported_bricks_count(bricks, upper_supports_lower, lower_supports_upper)

# Main function
def main():
    file_path = '2023/day22/input.txt'
    print('Part one:', task_1(file_path)) # 492
    print('Part two:', task_2(file_path)) # 86556

if __name__ == "__main__":
    main()