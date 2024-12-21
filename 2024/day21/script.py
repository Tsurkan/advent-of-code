from functools import cache
from itertools import permutations

def read_input(file_path):
    """Читає вхідні дані з файлу та повертає список рядків."""
    with open(file_path, 'r') as f:
        return f.read().splitlines()

# Генерація макету клавіатури
def create_keypad(layout):
    """Створює словник, де ключі - це кнопки, а значення - це їх координати (x, y)."""
    return {key: (x, y) for y, line in enumerate(layout) for x, key in enumerate(line) if key != ' '}

# Визначення макетів клавіатури
NUM_KEYPAD_LAYOUT = ['789', '456', '123', ' 0A']
DIR_KEYPAD_LAYOUT = [' ^A', '<v>']

# Створення клавіатур
num_keypad = create_keypad(NUM_KEYPAD_LAYOUT)
dir_keypad = create_keypad(DIR_KEYPAD_LAYOUT)

# Визначення напрямків руху
directions = {'^': (0, -1), '>': (1, 0), 'v': (0, 1), '<': (-1, 0)}

# У найгіршому випадку складність цього алгоритму може бути O(n!), де n — кількість елементів у послідовності кнопок
@cache
def calculate_presses(sequence, depth=2, use_dir_keypad=False, current_position=None):
    """
    Обчислює мінімальну кількість натискань кнопок для послідовності з урахуванням руху по клавіатурі.
    Використовує кешування для покращення ефективності.

    sequence - послідовність кнопок для натискання
    depth - глибина рекурсії (кількість роботів)
    use_dir_keypad - чи використовувати напрямкову клавіатуру
    current_position - поточна позиція на клавіатурі
    """
    keypad = dir_keypad if use_dir_keypad else num_keypad
    if not sequence:
        return 0  # Якщо послідовність порожня, натискати нічого не потрібно
    if not current_position:
        current_position = keypad['A']  # Початкова позиція - 'A'

    current_x, current_y = current_position
    target_x, target_y = keypad[sequence[0]]  # Цільова позиція для першої кнопки
    delta_x, delta_y = target_x - current_x, target_y - current_y  # Різниця в координатах

    button_sequence = ''
    if delta_x > 0:
        button_sequence += '>' * delta_x  # Додати переміщення вправо
    elif delta_x < 0:
        button_sequence += '<' * -delta_x  # Додати переміщення вліво
    if delta_y > 0:
        button_sequence += 'v' * delta_y  # Додати переміщення вниз
    elif delta_y < 0:
        button_sequence += '^' * -delta_y  # Додати переміщення вгору

    # Якщо є глибина, рекурсивно обчислюємо для всіх роботів послідовності натискань
    if depth:
        perm_lengths = []
        for perm in set(permutations(button_sequence)):  # Генерація всіх унікальних перестановок кнопок
            temp_x, temp_y = current_position
            for button in perm:
                move_x, move_y = directions[button]  # Отримуємо зміщення для кнопки
                temp_x += move_x
                temp_y += move_y
                if (temp_x, temp_y) not in keypad.values():
                    break  # Якщо нова позиція не на клавіатурі, виходимо з циклу
            else:
                perm_lengths.append(calculate_presses(perm + ('A',), depth - 1, True))  # Рекурсивний виклик для наступного етапу
        min_length = min(perm_lengths)  # Мінімальна кількість натискань для пермутації
    else:
        min_length = len(button_sequence) + 1  # Якщо глибина 0, просто додаємо 1 натискання для кнопки 'A'

    # Повертаємо загальну кількість натискань для поточної та наступної послідовності
    return min_length + calculate_presses(sequence[1:], depth, use_dir_keypad, (target_x, target_y))

def main(file_path = '2024/day21/input.txt'):
    part1 = 0
    part2 = 0
    for code in read_input(file_path):
        code_number = int(code[:-1])
        part1 += code_number * calculate_presses(code, 2)
        part2 += code_number * calculate_presses(code, 25)

    print("Part 1:", part1)  # 212488
    print("Part 2:", part2)  # 258263972600402

if __name__ == "__main__":
    main()
