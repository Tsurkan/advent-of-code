HORIZONTAL = 0
VERTICAL = 1

# Функция для разбора входных данных на отражения
# O(N), где N - количество строк во входных данных.
def parse_input(input_lines):
    reflections = []
    this_reflection = []

    for line in input_lines:
        if line == "":
            reflections.append(this_reflection[:])  # Используем срез для поверхностной копии
            this_reflection = []
        else:
            this_reflection.append(line)

    reflections.append(this_reflection[:])  # Добавляем последнее отражение
    return reflections

# Нахождение отражения
# O(M * N), где M - средняя длина отражения, N - количество отражений.
def find_reflection(reflection):
    h_answers = find_horizontal_reflection(reflection)
    v_answers = find_vertical_reflection(reflection)
    if h_answers:
        return HORIZONTAL, h_answers
    else:
        return VERTICAL, v_answers

# Нахождение вертикального отражения
def find_vertical_reflection(reflection):
    # Поворот на 90 градусов, затем использование поиска горизонтального отражения
    rotated_reflection = rotate_reflection(reflection)

    return find_horizontal_reflection(rotated_reflection)

# Поворот отражения на 90 
#  O(M * N), где M - средняя длина отражения, N - количество отражений.
def rotate_reflection(reflection):
    rotated_reflection = []

    for x in range(len(reflection[0])):
        line = ""
        for y in range(len(reflection) - 1, -1, -1):
            line += reflection[y][x]
        rotated_reflection.append(line)

    return rotated_reflection

# Нахождение горизонтального отражения
# O(M * N), где M - средняя длина отражения, N - количество отражений.
def find_horizontal_reflection(reflection):
    # Находим две строки подряд, которые идентичны
    answers = []
    for idx, line in enumerate(reflection):
        if idx < len(reflection) - 1:
            next_line = reflection[idx + 1]
            # Нашли возможное отражение?
            if line == next_line:
                # Это предполагает, что существует только *одно* действительное отражение, так что если
                # мы его нашли, можем завершить работу
                if is_actual_reflection(reflection, idx, idx + 1):
                    answers.append(idx + 1)

    return answers

# Проверка на действительное отражение
# O(M), где M - средняя длина отражения.
def is_actual_reflection(reflection, l1, l2):
    check = 1
    reflection_reaches_edge = True
    while True:
        c1 = l1 - check
        c2 = l2 + check

        # Достигли края?
        if c1 < 0 or c2 == len(reflection):
            break

        # Совпадают ли отраженные строки?
        if reflection[c1] != reflection[c2]:
            reflection_reaches_edge = False
            break

        check += 1

    if reflection_reaches_edge:
        return True
    else:
        return False

# Вычисление ответа для первой части
# O(M * N), где M - средняя длина отражения, N - количество отражений.
def calc_answer_for_part_one(reflections):
    answer = 0
    for idx, reflection in enumerate(reflections):
        direction, answers = find_reflection(reflection)

        if direction == HORIZONTAL:
            answer = answer + answers[0] * 100
        else:
            answer = answer + answers[0]

    return answer

# Функция для нахождения всех отражений
# O(M * N), где M - средняя длина отражения, N - количество отражений.
def find_all_reflections(reflection):
    h_answers = find_horizontal_reflection(reflection)
    v_answers = find_vertical_reflection(reflection)
    return h_answers, v_answers

# Нахождение отражения с пятном
# O(M^2 * N), где M - средняя длина отражения, N - количество отражений.
def find_reflection_with_smudge(reflection):
    # Сначала нам нужно найти исходное отражение, потому что новое (как только мы исправим пятно)
    # *должно* быть в другом месте
    orig_dir, answers = find_reflection(reflection)
    orig_answer = answers[0]

    for y in range(len(reflection)):
        for x in range(len(reflection[0])):
            reflection_copy = reflection.copy()
            line = reflection_copy[y]
            c = line[x]
            if c == ".":
                line = line[:x] + "#" + line[x + 1:]
            else:
                line = line[:x] + "." + line[x + 1:]

            reflection_copy[y] = line

            h_answers, v_answers = find_all_reflections(reflection_copy)

            if orig_dir == HORIZONTAL:
                h_answers = [answer for answer in h_answers if answer != orig_answer]
            else:
                v_answers = [answer for answer in v_answers if answer != orig_answer]

            if not h_answers and not v_answers:
                continue

            if h_answers:
                return HORIZONTAL, h_answers[0]
            else:
                return VERTICAL, v_answers[0]

# Вычисление ответа для второй части
# O(M^2 * N), где M - средняя длина отражения, N - количество отражений.
def calc_answer_for_part_two(reflections):
    answer = 0
    for idx, reflection in enumerate(reflections):
        direction, num = find_reflection_with_smudge(reflection)

        if direction == HORIZONTAL:
            answer = answer + num * 100
        else:
            answer = answer + num

    return answer

def task_1(file_path):
    with open('2023/day13/input.txt') as f:
        input_lines = f.read().splitlines()
    return calc_answer_for_part_one(parse_input(input_lines))

def task_2(file_path):
    with open('2023/day13/input.txt') as f:
        input_lines = f.read().splitlines()
    return calc_answer_for_part_two(parse_input(input_lines))

# Main function
def main():
    file_path = '2023/day13/input.txt'
    print('Part one:', task_1(file_path)) # 32035
    print('Part two:', task_2(file_path)) # 24847

if __name__ == "__main__":
    main()