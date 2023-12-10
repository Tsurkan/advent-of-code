# only 12 red cubes, 13 green cubes, and 14 blue cubes
def part_One(file_path):
    cubes = ['red', 'green', 'blue']

    with open(file_path) as f:
        games = {}
        for line in f:
            game = {}
            parts = line.split(':')
            for element in parts[1].strip().split('; '):
                for item in element.split(', '):
                    quantity, color = item.split(' ')
                    if color in game:
                        if game[color] < int(quantity):
                            game[color] = int(quantity)
                    else:
                        game[color] = int(quantity)
            games[parts[0]] = game

    valid_sum = 0
    for game, cube_counts in games.items():
        valid = True
        for cube, limit in zip(cubes, [12, 13, 14]):
            if cube_counts.get(cube, 0) > limit:
                valid = False
                break
        if valid:
            valid_sum += int(game.split(' ')[1])
            
    return valid_sum

def part_Two(file_path):
    cubes = ['red', 'green', 'blue']

    with open(file_path) as f:
        games = {}
        for line in f:
            game = {}
            parts = line.split(':')
            for element in parts[1].strip().split('; '):
                for item in element.split(', '):
                    quantity, color = item.split(' ')
                    game[color] = max(game.get(color, 0), int(quantity))
            games[parts[0]] = game

    total_sum = 0
    for game in games.values():
        product = 1
        for quantity in game.values():
            product *= quantity
        total_sum += product

    return total_sum

def main():
    print('Part one:', part_One('day2/input.txt')) # 3099
    print('Part two:', part_Two('day2/input.txt')) # 72970

if __name__ == "__main__":
    main()