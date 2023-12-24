import re
import math

# Розуміння полягає в тому, що нас не цікавлять окремі виміри, а лише суми всіх вимірів. 
# Тому для значень суми координат, застосовуємо китайську теорему про залишки, далі видаляємо все, 
# що призводять до будь-яких зіткнень у минулому або в нецілий момент часу, і отримую відповідь.

# Класс, представляющий объект Hailstone, хранящий координаты и скорости по осям x, y и z для градиентного спуска.
class Hailstone:
    def __init__(self, x, y, z, dx, dy, dz):
        self.x = x
        self.y = y
        self.z = z
        self.dx = dx
        self.dy = dy
        self.dz = dz
        self.initial_sum = x + y + z
        self.direction_sum = dx + dy + dz

# Класс для реализации китайской теоремы об остатках с заданными базами.
class ChineseRemainderConstructor:

    # Сложность: O(n) - где n - количество баз.
    def __init__(self, bases):
        self._bases = bases
        self._prod = math.prod(bases)
        self._inverses = [self._prod // x for x in bases]
        self._muls = [inv * self.mul_inv(inv, base) for base, inv in zip(self._bases, self._inverses)]

    # Вычисляет остаток по китайской теореме об остатках.
    # Сложность: O(n) - где n - количество баз.
    def rem(self, mods):
        return sum(mul * mod for mul, mod in zip(self._muls, mods)) % self._prod

    # Вычисления мультипликативной инверсии.
    # Сложность: O(log(min(a, b))) - из-за алгоритма нахождения обратного элемента.
    @staticmethod
    def mul_inv(a, b):
        x0, x1 = 0, 1
        while a > 1:
            div, mod = divmod(a, b)
            a, b = b, mod
            x0, x1 = x1 - div * x0, x0
        return (x1 if x1 >= 0 else x1 + b)

IDENTICAL = object()
MIN_COORDINATE, MAX_COORDINATE = 2 * 10**14, 4 * 10**14

# Функция вычисляет параметры линии (угловой коэффициент и свободный член) на основе координаты и скорости.
# Сложность: O(1).
def calculate_line_params(hailstone):
    slope = hailstone.dy / hailstone.dx
    intercept = hailstone.y - slope * hailstone.x
    return slope, intercept

# Функция проверяет параллельность двух линий на основе их угловых коэффициентов и свободных членов.
# Сложность: O(1).
def check_parallel_lines(slope1, slope2, intercept1, intercept2):
    if math.isclose(slope1, slope2):
        return IDENTICAL if math.isclose(intercept1, intercept2) else None
    return slope1, slope2, intercept1, intercept2

# Функция вычисляет точку пересечения двух линий.
# Сложность: O(1).
def calculate_intersection_point(slope1, slope2, intercept1, intercept2):
    intersection_x = (intercept2 - intercept1) / (slope1 - slope2)
    intersection_y = intersection_x * slope1 + intercept1
    return intersection_x, intersection_y

# Функция определяет, находится ли точка пересечения в будущем для двух hailstones,
# исходя из их скоростей и текущих координат.
# Сложность: O(1).
def is_intersection_in_future(hailstone1, hailstone2, intersection_x):
    return (intersection_x > hailstone1.x) == (hailstone1.dx > 0) and \
           (intersection_x > hailstone2.x) == (hailstone2.dx > 0)

# Функция вычисляет количество пересечений траекторий всех hailstones.
# Сложность в худшем случае O(n^2), где n - количество hailstones.
def find_intersection(hailstones):
    count = 0
    num_hailstones = len(hailstones)

    for i in range(num_hailstones - 1):
        for j in range(i + 1, num_hailstones):
            slope1, intercept1 = calculate_line_params(hailstones[i])
            slope2, intercept2 = calculate_line_params(hailstones[j])
            parallel_check = check_parallel_lines(slope1, slope2, intercept1, intercept2)

            if parallel_check == IDENTICAL:
                count += 1
            elif parallel_check is not None:
                slope1, slope2, intercept1, intercept2 = parallel_check
                intersection_x, intersection_y = calculate_intersection_point(slope1, slope2, intercept1, intercept2)
                in_future = is_intersection_in_future(hailstones[i], hailstones[j], intersection_x)
                valid_range = MIN_COORDINATE <= intersection_x <= MAX_COORDINATE and MIN_COORDINATE <= intersection_y <= MAX_COORDINATE
                count += int(in_future and valid_range)
    return count

# Функция для чтения данных из файла и создания экземпляров Hailstone на основе этих данных.
# Сложность O(m), где m - количество строк в файле.
def read_hailstones_data(file_path):
    with open(file_path) as file:
        return [Hailstone(*map(int, re.split(r'\s*[,@]\s*', line))) for line in file]

# Функция проверяет параллельность последовательностей, вычисляя ряд и возвращая результат.
# Сложность: О(n^2 * log(n)) - где n - количество элементов. Это из-за циклов и сортировки.
def check_parallel(direction_sums, initial_sums):
    for sd_r in range(1000):
        if sd_r in direction_sums:
            continue
        
        m_and_s = [(sd - sd_r, s % (sd - sd_r)) for s, sd in zip(initial_sums, direction_sums)]
        m_and_s.sort(key=lambda p: abs(p[0]), reverse=True)
        
        m, s_ = [], []
        while m_and_s:
            m_i, s_i = m_and_s.pop(0)
            abs_m_i = abs(m_i)
            m.append(abs_m_i)
            s_.append(s_i + abs_m_i)
            m_and_s = [(m_j, s_j) for m_j, s_j in m_and_s if math.gcd(m_j, m_i) == 1]
        
        s_r = ChineseRemainderConstructor(m).rem(s_)
        
        if all(((s_r - s_i) / (sd_i - sd_r)).is_integer() and (s_r - s_i) / (sd_i - sd_r) > 0 for s_i, sd_i in zip(initial_sums, direction_sums)):
            return s_r

def task_1(file_path):
    return find_intersection(read_hailstones_data(file_path))

def task_2(file_path):
    initial_sums, direction_sums = zip(*[(stone.initial_sum, stone.direction_sum) for stone in read_hailstones_data(file_path)])
    return check_parallel(direction_sums, initial_sums)

# Main function
def main():
    file_path = '2023/day24/input.txt'
    print('Part one:', task_1(file_path)) # 25261
    print('Part two:', task_2(file_path)) # 549873212220117

if __name__ == "__main__":
    main()