from functools import cache

def read_input(file_path):
    """Читання та обробка вхідних даних з файлу."""
    with open(file_path, "r") as file:
        lines = file.read().splitlines()
    patterns, designs = lines[0].split(", "), lines[2:]
    return patterns, designs

@cache
def count_combos(d, patterns):
    """Рекурсивно обчислюємо кількість комбінацій для заданого дизайну."""
    if not d:
        return 1
    return sum(count_combos(d[len(p):], patterns) for p in patterns if d.startswith(p))

def calculate_results(patterns, designs):
    """Обчислюємо результати для кожного дизайну."""
    result1, result2 = 0, 0
    for d in designs:
        count = count_combos(d, tuple(patterns))
        if count:
            result1 += 1
            result2 += count
    return result1, result2

def main(file_path="2024/day19/input.txt"):
    result1, result2 = calculate_results(*read_input(file_path))
    print("Part 1:", result1) # 330
    print("Part 2:", result2) # 950763269786650

if __name__ == "__main__":
    main()