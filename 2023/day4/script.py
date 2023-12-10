def part_One(file_path):
    with open(file_path) as f:
        total_sum = 0
        for line in f:
            p = 0
            numbers = line.strip().split(': ')[1].split(' | ')
            n1 = [int(i)  for i in numbers[0].split(' ') if i.isnumeric()]
            n2 = [int(i)  for i in numbers[1].split(' ') if i.isnumeric()]
            for num in n2:
                if num in n1:
                    if p == 0:
                        p += 1
                    else:
                        p *= 2
            total_sum += p

    return total_sum

def part_Two(file_path):
    with open(file_path, 'r') as file:
        game_array = file.read().split("\n")

    total_cards = 0
    copy_card = [1] * len(game_array)

    for i in range(len(game_array)):
        total_cards += copy_card[i]
        card = game_array[i].split(":")[1].strip().split("|")
        win_numbers = card[0].strip().split()
        all_numbers = card[1] + " "
        points = 0
        win = ""

        for j in range(len(win_numbers)):
            if win_numbers[j]:
                win_number = " " + win_numbers[j].strip() + " "
                if win_number in all_numbers:
                    points += 1
                    if i + points < len(copy_card):
                        copy_card[i + points] += copy_card[i]
                    win += win_number + " "

    return total_cards

def main():
    print('Part one:', part_One('day4/input.txt')) # 25231
    print('Part two:', part_Two('day4/input.txt')) # 9721255

if __name__ == "__main__":
    main()