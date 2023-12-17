def get_final_sum_task_1(history):
    final_sum = 0
    for i in range(len(history), 0, -1):
        final_sum += history[-1]
        history = [history[j + 1] - history[j] for j in range(i - 1)]
    return final_sum

def get_final_sum_task_2(history):
    current_nums = []
    while any(history):
        current_nums.append(history[0])
        history = [history[i + 1] - history[i] for i in range(len(history) - 1)]

    return sum(current_nums[::2]) - sum(current_nums[1::2])

def task_1(file_path):
    with open(file_path, 'r') as f:
        histories = [[int(x) for x in line.split()] for line in f.read().strip().split('\n')]

    return sum([get_final_sum_task_1(h) for h in histories])

def task_2(file_path):
    with open(file_path, 'r') as f:
        histories = [[int(x) for x in line.split()] for line in f.read().strip().split('\n')]

    return sum([get_final_sum_task_2(h) for h in histories])

def main():
    file_path = '2023/day9/input.txt'
    print('Part one:', task_1(file_path)) # 1762065988
    print('Part two:', task_2(file_path)) # 1066

if __name__ == "__main__":
    main()