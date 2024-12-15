def calculate_coordinates(ax, ay, bx, by, target_x, target_y):
    # Обчислюємо детермінант системи рівнянь
    determinant = ax * by - bx * ay

    # Перевірка на нульовий детермінант (якщо він нульовий, то розв'язків немає)
    if determinant == 0:
        return 0

    # Обчислюємо координати i та j
    i = round((by * target_x - bx * target_y) / determinant)
    j = round((-ay * target_x + ax * target_y) / determinant)

    # Перевіряємо, чи задовольняють знайдені координати систему рівнянь
    if ax * i + bx * j == target_x and ay * i + by * j == target_y:
        return i * 3 + j
    return 0  # Якщо рівняння не виконано, повертаємо 0

def parse_input(file_path):
    """Функція для парсингу даних з файлу"""
    with open(file_path) as file:
        for machine in file.read().split('\n\n'):
            lines = machine.splitlines()
            # Розбираємо координати ax, ay, bx, by, target_x, target_y
            (ax, ay), (bx, by), (target_x, target_y) = (
                (int(coord.strip()[2:]) for coord in line.split(':')[1].split(','))
                for line in lines
            )
            yield ax, ay, bx, by, target_x, target_y

def main(file_path='2024/day13/input.txt'):
    part1_result = 0
    part2_result = 0

    for ax, ay, bx, by, target_x, target_y in parse_input(file_path):
        part1_result += calculate_coordinates(ax, ay, bx, by, target_x, target_y)

        # Збільшуємо значення target_x та target_y для розрахунку другої частини
        target_x += 10**13  # Більш компактне представлення великого числа
        target_y += 10**13
        
        part2_result += calculate_coordinates(ax, ay, bx, by, target_x, target_y)

    print('Part one:', part1_result) # 36870
    print('Part two:', part2_result) # 78101482023732

if __name__ == "__main__":
    main()
