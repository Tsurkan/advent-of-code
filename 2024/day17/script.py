from re import findall

def parse_input(file_path):
    """
    Розбирає вхідний файл і повертає початкові змінні та інструкції програми.
    """
    with open(file_path, "r") as file:
        numbers = [int(n) for n in findall(r"(\d+)", file.read())]
    return numbers[0], numbers[1], numbers[2], numbers[3:]

# Cкладність: O(n)
def run_program(prog, a, b=0, c=0):
    """
    Виконує програму з заданими інструкціями та початковим значенням `a`.
    Алгоритм обробляє послідовність команд і змінює стан змінних `a`, `b`, `c`.
    Це схоже на роботу віртуальної машини.
    """
    ip, out = 0, []
    while 0 <= ip < len(prog):
        lit = prog[ip + 1]
        combo = [0, 1, 2, 3, a, b, c, 99999][prog[ip + 1]]
        match prog[ip]:
            case 0: a = a // 2 ** combo             # adv: операція поділу `a` на ступінь двійки
            case 1: b = b ^ lit                     # bxl: XOR змінної `b` із літеральним значенням
            case 2: b = combo % 8                   # bst: залишок від ділення `combo` на 8
            case 3: ip = ip if a == 0 else lit - 2  # jnz: перехід, якщо `a` дорівнює нулю
            case 4: b = b ^ c                       # bxc: XOR між `b` і `c`
            case 5: out.append(combo % 8)           # out: додати до виходу залишок від ділення
            case 6: b = a // 2 ** combo             # bdv: поділ `a` на ступінь двійки, запис у `b`
            case 7: c = a // 2 ** combo             # cdv: поділ `a` на ступінь двійки, запис у `c`
        
        ip += 2  # Перехід до наступної команди
    return out

# Cкладність у найгіршому випадку: O(8**d), де d — глибина рекурсії.
def find_initial_a(prog, target, a=0, depth=0):
    """
    Знаходить початкове значення `a`, яке дає бажаний вихідний результат.
    Використовує деревоподібний рекурсивний пошук для перевірки можливих значень `a`.
    """
    if depth == len(target):  # Якщо всі елементи цілі досягнуті, повертаємо `a`
        return a

    for i in range(8):
        output = run_program(prog, a * 8 + i)
        if output and output[0] == target[depth]:
            result = find_initial_a(prog, target, a * 8 + i, depth + 1)
            if result:
                return result
    return 0

def main(file_path='2024/day17/input.txt'):
    a, b, c, prog = parse_input(file_path)

    # Частина 1
    part1_output = run_program(prog, a, b, c)
    print("Part 1:", ",".join(map(str, part1_output)))

    # Частина 2
    target = prog[::-1]
    part2_result = find_initial_a(prog, target)
    print("Part 2:", part2_result)

if __name__ == "__main__":
    main()
