import sys

sys.setrecursionlimit(15000)  # Set a higher recursion limit, adjust as needed

def find_all_paths(layout):
    def next_position(i, j, direction):
        moves = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}
        di, dj = moves[direction]
        return i + di, j + dj

    def determine_direction(layout, i, j):
        directions = {
            '|': ('south' if (i - 1, j) in visited else 'north'),
            '-': ('east' if (i, j - 1) in visited else 'west'),
            'L': ('east' if (i - 1, j) in visited else 'north'),
            'J': ('west' if (i - 1, j) in visited else 'north'),
            '7': ('south' if (i, j - 1) in visited else 'west'),
            'F': ('east' if (i + 1, j) in visited else 'south')
        }

        if layout[i][j] == 'S':
            a[0] += 1
            return a[a[0]]

        return directions.get(layout[i][j], None)

    def explore_path(current_i, current_j, path, steps):
        visited.add((current_i, current_j))
        direction = determine_direction(layout, current_i, current_j)

        if direction is None:
            visited.remove((current_i, current_j))
            return steps, path

        next_i, next_j = next_position(current_i, current_j, direction)

        if next_i < 0 or next_i >= len(layout) or next_j < 0 or next_j >= len(layout[0]):
            visited.remove((current_i, current_j))
            return steps, path

        if (next_i, next_j) in visited:
            visited.remove((current_i, current_j))
            return steps, path

        new_path = path + [(next_i, next_j)]

        if len(new_path) > 2 and new_path[0] == new_path[-1]:
            visited.remove((current_i, current_j))
            return steps, new_path

        return explore_path(next_i, next_j, new_path, steps + 1)

    layout = layout.split('\n')

    start_i, start_j = next(
        ((i, j) for i, row in enumerate(layout) for j, val in enumerate(row) if val == 'S'),
        (None, None)
    )

    if start_i is None:
        return []

    a = [0, 'north', 'south', 'west', 'east']
    visited = set()
    paths = []

    for _ in range(4):
        steps, path = explore_path(start_i, start_j, [(start_i, start_j)], 1)
        paths.append(path)

    return paths

def part_One(file_path):
    def max_points_before_intersection(lists):
        max_points = 0
        intersection_index = None

        for i in range(min(len(lists[0]), len(lists[1]))):
            if lists[0][i] == lists[1][i]:
                intersection_index = i
                break

        if intersection_index is not None:
            max_points = intersection_index + 1
        else:
            max_points = min(len(lists[0]), len(lists[1]))

        return max_points

    with open(file_path) as f:
        input_data = f.read()

    paths = find_all_paths(input_data)
    paths = [path[0][1:] for path in paths if path and len(path[0]) > 1]

    return max_points_before_intersection(paths)

print('Part one:', part_One('day10/input.txt'))
