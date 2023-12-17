import sys

# Set a higher recursion limit, adjust as needed
sys.setrecursionlimit(15000)  

# Function to find all paths in the layout
def find_all_paths(layout):

    # Function to find the next position in the loop
    def next_position(i, j, direction):
        moves = {'north': (-1, 0), 'south': (1, 0), 'east': (0, 1), 'west': (0, -1)}
        di, dj = moves[direction]
        return i + di, j + dj

    # Function to determine the direction at a specific position
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

    # Recursive function to explore paths from a given position
    def explore_path(current_i, current_j, path):
        visited.add((current_i, current_j))
        direction = determine_direction(layout, current_i, current_j)

        if direction is None:
            path.pop()
            all_paths.append(path)
            visited.remove((current_i, current_j))
            return

        next_i, next_j = next_position(current_i, current_j, direction)

        if next_i < 0 or next_i >= len(layout) or next_j < 0 or next_j >= len(layout[0]):
            visited.remove((current_i, current_j))
            return

        if (next_i, next_j) in visited:
            all_paths.append(path)
            visited.remove((current_i, current_j))
            return

        new_path = path + [(next_i, next_j)]

        if len(new_path) > 2 and new_path[0] == new_path[-1]:
            all_paths.append(new_path)
            visited.remove((current_i, current_j))
            return

        explore_path(next_i, next_j, new_path)
        visited.remove((current_i, current_j))

    # Convert input layout to a list of lists
    layout = layout.split('\n')

    # Find the starting position
    start_i, start_j = next(
        ((i, j) for i, row in enumerate(layout) for j, val in enumerate(row) if val == 'S'),
        (None, None)
    )

    if start_i is None:
        return []
    
    # Initialize variables
    a = [0, 'north', 'south', 'west', 'east']
    alles = []
    visited = set()
    
    # Explore paths from the starting position in all directions
    for _ in range(4):
        all_paths = []
        explore_path(start_i, start_j, [(start_i, start_j)])
        alles.append(all_paths)
        
    return alles

# Function to calculate maximum points intersection
def max_points_before_intersection(lists):

    # Initialize variables to store maximum points and track intersection
    max_points = 0
    intersection_index = None
    
    # Iterate through the lists and find the intersection index
    for i in range(min(len(lists[0]), len(lists[1]))):
        if lists[0][i] == lists[1][i]:
            intersection_index = i
            break
    
    # Calculate the maximum points before the intersection
    if intersection_index is not None:
        max_points = intersection_index + 1
    else:
        max_points = min(len(lists[0]), len(lists[1]))
    
    return max_points


def task_1(file_path):

    # Example input data
    with open(file_path) as f:
        input_data = f.read()

    # Find all possible paths
    paths = [path[0][1:] for path in find_all_paths(input_data) if path and len(path[0]) > 1]
    
    # Return the result of maximum points before intersection
    return max_points_before_intersection(paths)



def task_2(file_path):
    pass

# Main function
def main():
    file_path = '2023/day10/input.txt'
    print('Part one:', task_1(file_path)) # 6903
    # print('Part two:', task_2(file_path)) # 265

if __name__ == "__main__":
    main()