# Determine the score of a given hand based on card combinations
def determine_hand_score_task1(hand):
    s = sorted(hand) # Sort the hand
    if len(set(s)) == 1:
        return 7
    elif s[0] == s[1] == s[2] == s[3] or s[1] == s[2] == s[3] == s[4]:
        return 6
    elif s[0] == s[1] == s[2] and s[3] == s[4] or s[0] == s[1] and s[2] == s[3] == s[4]:
        return 5
    elif s[0] == s[1] == s[2] or s[1] == s[2] == s[3] or s[2] == s[3] == s[4]:
        return 4
    elif s[0] == s[1] and s[2] == s[3] or s[0] == s[1] and s[3] == s[4] or s[1] == s[2] and s[3] == s[4]:
        return 3
    elif len(set(s)) == 4:
        return 2
    else:
        return 1

def determine_hand_score_task2(hand):
    if len(set(hand)) == 1 or len(set(hand)) == 2 and 13 in hand:
        return 7
    replace = min([c for c in hand if hand.count(c) == max([hand.count(c) for c in hand if c != 13])])
    s = sorted([replace if c == 13 else c for c in hand])
    if s[0] == s[1] == s[2] == s[3] or s[1] == s[2] == s[3] == s[4]:
        return 6
    elif s[0] == s[1] == s[2] and s[3] == s[4] or s[0] == s[1] and s[2] == s[3] == s[4]:
        return 5
    elif s[0] == s[1] == s[2] or s[1] == s[2] == s[3] or s[2] == s[3] == s[4]:
        return 4
    elif s[0] == s[1] and s[2] == s[3] or s[0] == s[1] and s[3] == s[4] or s[1] == s[2] and s[3] == s[4]:
        return 3
    elif len(set(s)) == 4:
        return 2
    else:
        return 1

# Calculate the total score for groups of hands in the game
def calculate_total_score(groups):

    # Sort the groups based on score and card values
    groups.sort(key=lambda x: x[2])

    prev_score = None
    ranked_groups = []
    current_ranked_group = []

    # Rank the groups based on their scores
    for group in groups:
        if group[2] != prev_score:
            if current_ranked_group:
                ranked_groups.append(current_ranked_group)
                current_ranked_group = []
        current_ranked_group.append(group)
        prev_score = group[2]

    if current_ranked_group:
        ranked_groups.append(current_ranked_group)

    # Sort the ranked groups based on card values
    for group in ranked_groups:
        group.sort(key=lambda x: x[0], reverse=True)

    # Calculate the total score by summing up scores multiplied by their positions
    flat_groups = [group for sublist in ranked_groups for group in sublist]
    return sum(int(group[1]) * (i + 1) for i, group in enumerate(flat_groups))

def read_input_file(file_path):
    with open(file_path, 'r') as f:
        data = f.read().strip()
    return [x.split() for x in data.split('\n')] # Split the data into groups of hands

def task_1(file_path):
    groups = read_input_file(file_path)

    # Assign scores to each hand
    for group in groups:
        group[0] = ['AKQJT98765432'.index(card) + 1 for card in group[0]]
        group.append(determine_hand_score_task1(group[0]))
    return calculate_total_score(groups)

def task_2(file_path):
    groups = read_input_file(file_path)
    
    # Assign scores to each hand
    for group in groups:
        group[0] = ['AKQT98765432J'.index(card) + 1 for card in group[0]]
        group.append(determine_hand_score_task2(group[0]))

    return calculate_total_score(groups)
    

def main():
    file_path = '2023/day7/input.txt'

    print('Part one:', task_1(file_path)) # 250453939
    print('Part two:', task_2(file_path)) # 248652697

if __name__ == "__main__":
    main()