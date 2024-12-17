import re

# Ширина та висота області
WIDTH, HEIGHT = 101, 103

def read_bots_data(file_path):
    """Читання даних роботів з файлу"""
    with open(file_path) as f:
        return [list(map(int, re.findall(r'-?\d+', line))) for line in f]

def calculate_new_position(x, y, dx, dy, time):
    """Визначення нових координат робота з урахуванням часу"""
    new_x = (x + dx * time) % WIDTH
    new_y = (y + dy * time) % HEIGHT
    return new_x, new_y
    
def get_region(x, y, center_x, center_y):
    """Визначення, в якій частині області знаходиться робот"""
    if x > center_x and y > center_y:
        return 'top_right'
    elif x > center_x and y < center_y:
        return 'top_left'
    elif x < center_x and y > center_y:
        return 'bottom_right'
    elif x < center_x and y < center_y:
        return 'bottom_left'

def calculate_danger(time, bots):
    """Обчислення ступеня небезпеки для заданого часу"""
    regions = {'top_right': 0, 'top_left': 0, 'bottom_right': 0, 'bottom_left': 0}

    # Обчислюємо центр області
    center_x, center_y = WIDTH // 2, HEIGHT // 2

    for x, y, dx, dy in bots:
        new_x, new_y = calculate_new_position(x, y, dx, dy, time)
        region = get_region(new_x, new_y, center_x, center_y)
        if region: 
            regions[region] += 1  # Збільшуємо лічильник для відповідної частини області

    return regions['top_right'] * regions['top_left'] * regions['bottom_right'] * regions['bottom_left']

def main(file_path='2024/day14/input.txt'):
    bots = read_bots_data(file_path)

    # Частина 1: Виведення небезпеки для часу 100
    print('Part 1:', calculate_danger(100, bots))                                   # 215987200

    # Частина 2: Пошук часу, коли небезпека є мінімальною
    print('Part 2:', min(range(10_000), key=lambda x: calculate_danger(x, bots)))   # 8050

if __name__ == "__main__":
    main()
