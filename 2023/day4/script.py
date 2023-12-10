def task1(file_path):
    with open(file_path, 'r') as file:
        game_array = file.readlines()
    
    total_sum = 0

    for card_info in game_array:

        # Parsing the card information
        _, numbers = card_info.strip().split(': ')
        win_numbers, all_numbers = map(lambda x: set(map(int, x.split())), numbers.split(' | '))
            
        points = 0
        for num in all_numbers:
            if num in win_numbers:
                points = points + 1 if points == 0 else points * 2
        total_sum += points

    return total_sum

def task2(file_path):
    with open(file_path, 'r') as file:
        game_array = file.readlines()

    total_sum = 0
    copy_card = [1] * len(game_array)

    for i, card_info in enumerate(game_array):
        total_sum += copy_card[i]

        # Parsing the card information
        _, numbers = card_info.strip().split(': ')
        win_numbers, all_numbers = map(lambda x: set(map(int, x.split())), numbers.split(' | '))

        points = 0
        for num in all_numbers:
            if num in win_numbers:
                points += 1
                if i + points < len(copy_card):
                    copy_card[i + points] += copy_card[i]

    return total_sum

def main():
    print('Part one:', task1('2023/day4/input.txt')) # 25231
    print('Part two:', task2('2023/day4/input.txt')) # 9721255

if __name__ == "__main__":
    main()