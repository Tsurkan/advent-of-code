from functools import cache

def read_input(file_path: str) -> list[int]:
    """Зчитує список чисел із файлу."""
    with open(file_path, "r") as file:
        return [int(part) for part in file.readline().split()]


def blink(stone: int) -> list[int]:
    """
    Визначає наступний крок для каменю.
    
    Якщо камінь дорівнює 0, повертає список із одного елемента [1].
    Якщо кількість цифр парна, камінь розділяється на дві рівні частини.
    Якщо кількість цифр непарна, множиться на 2024.
    """
    if stone == 0:
        return [1]
    str_stone = str(stone)
    length = len(str_stone)
    if length % 2 == 0:
        half = length // 2
        return [int(str_stone[:half]), int(str_stone[half:])]
    else:
        return [stone * 2024]

@cache
def fast_forward(stone: int, steps: int) -> int:
    """
    Рекурсивно обчислює кількість кроків.
    
    Найгірший випадок має складність O(b^d), де b — середня кількість нових станів (гілок) для кожного кроку, а
    d — кількість кроків (steps). Проте кешування значно оптимізує виконання, знижуючи реальну кількість обчислень.
    """
    if steps == 1:
        return len(blink(stone))
    return sum(fast_forward(s, steps - 1) for s in blink(stone))


def main(file_path='2024/day11/input.txt'):
    stones = read_input(file_path)

    print('Part one:', sum(fast_forward(s, 25) for s in stones)) # 194782
    print('Part two:', sum(fast_forward(s, 75) for s in stones)) # 233007586663131


if __name__ == '__main__':
    main()
