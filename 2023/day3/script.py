def task1(file_path):

    with open(file_path, 'r') as f:
        input_data = f.read().splitlines()

    # Function to retrieve slices and handle boundary cases efficiently
    def get_slice(x, y1, y2):
        return input_data[x][max(y1, 0):min(y2, len(input_data[0]))] if 0 <= x < len(input_data) else ''

    part_numbers = []
    max_x, max_y = len(input_data), len(input_data[0])

    for x, line in enumerate(input_data):
        i = 0
        while i < len(line): # Extract the number
            if line[i].isdigit():
                start = i
                while i < len(line) and line[i].isdigit():
                    i += 1
                number = int(line[start:i])

                left, right = start - 1, i # Define slice boundaries for adjacent characters
                adjacent_characters = ''.join([
                    get_slice(x - 1, left, right + 1),
                    get_slice(x, left, left + 1),
                    get_slice(x, right, right + 1),
                    get_slice(x + 1, left, right + 1)
                ])

                # Check for adjacent characters and add the number
                if any(char != '.' for char in adjacent_characters):
                    part_numbers.append(number)
            else:
                i += 1

    return sum(part_numbers)

def task2(file_path):
    with open(file_path, 'r') as file:
        schematic = []
        parts = []
        width = None

        # Read the file and process the schematic
        for line in file.readlines():
            row = ["."] + list(line.strip()) + ["."]  # Add left and right boundaries
            if width is None:
                width = len(row) - 2

            number = None
            for index, char in enumerate(row):
                if char.isdigit():
                    if number is None:
                        number = int(char)
                    else:
                        number = number * 10 + int(char)
                    row[index] = str(len(parts))  # Assign a part index
                else:
                    if number is not None:
                        parts.append(number)
                        number = None

            if number is not None:
                parts.append(number)

            schematic.append(row)

        schematic.append(["."] * len(schematic[0]))  # Add initial and final boundaries
        schematic.insert(0, ["."] * len(schematic[0]))

        total = 0
        for i in range(1, len(schematic) - 1):
            for j in range(1, width + 1):
                if schematic[i][j] == '*':
                    neighbors = set()

                    # Check neighboring cells for interactions
                    for k in (-1, 0, 1):
                        for l in (-1, 0, 1):
                            neighbor_value = schematic[i + k][j + l]
                            if neighbor_value.isdigit():
                                neighbors.add(int(neighbor_value))

                    # Calculate the total based on interactions between parts
                    if len(neighbors) == 2:
                        total += parts[list(neighbors)[0]] * parts[list(neighbors)[1]]
    return total

def main():
    print('Part one:', task1('2023/day3/input.txt')) # 527369
    print('Part two:', task2('2023/day3/input.txt')) # 73074886

if __name__ == "__main__":
    main()