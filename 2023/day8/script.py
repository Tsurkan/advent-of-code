import math

# Process the instructions and create a node map
def preprocess_instructions(data):
    instructions = {}
    nodes = data[1].split('\n')
    for line in nodes:
        parts = line.split(' = (')
        node = parts[0]
        left, right = parts[1][:-1].split(', ')

        # Save instructions for the node in the dictionary
        instructions[node] = (left, right)
    return instructions

def task_1(file_path):
    with open(file_path, 'r') as f:
        data = f.read().strip().split('\n\n')
    
    node_map = preprocess_instructions(data)

    cur = 'AAA' # Start from node 'AAA
    steps = 0

    # Traverse nodes until 'ZZZ' is reached
    while cur != 'ZZZ':
        for instruction in data[0]:

            # Update current node based on the instruction (either left or right)
            cur = node_map[cur][0 if instruction == 'L' else 1]
            steps += 1

            # If 'ZZZ' is reached, return the total steps taken
            if cur == 'ZZZ':
                return steps

    return steps

def task_2(file_path):
    with open(file_path, 'r') as f:
        data = f.read().strip().split('\n\n')
    
    node_map = preprocess_instructions(data)

    all_steps = []

    # Iterate through nodes ending with 'A'
    for node in (n for n in node_map if n.endswith('A')):
        cur = node
        steps = 0
        while not cur.endswith('Z'): # Continue until node ends with 'Z'
            for instruction in data[0]:
                cur = node_map[cur][0 if instruction == 'L' else 1]
                steps += 1
        all_steps.append(steps) # Save steps for each node ending with 'A'

    # Calculate the least common multiple(lcm) of all recorded steps
    return math.lcm(*all_steps)

def main():
    file_path = '2023/day8/input.txt'
    print('Part one:', task_1(file_path)) # 16531
    print('Part two:', task_2(file_path)) # 24035773251517

if __name__ == "__main__":
    main()