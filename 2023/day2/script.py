# Reading data from the file and processing game information
def input_data(file_path):
    with open(file_path) as f:
        games = {}
        for line in f:
            game = {}
            parts = line.split(':')
            for element in parts[1].strip().split('; '):
                for item in element.split(', '):
                    quantity, color = item.split(' ')

                    # Update the maximum count of each cube color
                    game[color] = max(game.get(color, 0), int(quantity)) 
            games[parts[0]] = game
    return games

def task1(file_path):
    cube_limits = { 'red': 12, 'green': 13, 'blue': 14 } # Cube colors and their limits

    games = input_data(file_path)

    # Calculating the sum of valid game scores based on cube counts
    valid_sum = 0
    for game, cube_counts in games.items():
        if all(cube_counts.get(cube, 0) <= limit for cube, limit in cube_limits.items()):
            valid_sum += int(game.split(' ')[1])
            
    return valid_sum

def task2(file_path):
    games = input_data(file_path)

    # Calculating the total sum based on products of cube quantities in each game
    total_sum = 0
    for game in games.values():
        product = 1
        for quantity in game.values():
            product *= quantity
        total_sum += product

    return total_sum

def main():
    file_path = '2023/day2/input.txt'
    print('Part one:', task1(file_path)) # 3099
    print('Part two:', task2(file_path)) # 72970

if __name__ == "__main__":
    main()