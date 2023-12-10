def main():
    with open('day4/t_input2.txt', 'r') as file:
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

    print(f"Total cards: {total_cards}")

main()
