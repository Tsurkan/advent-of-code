from pathlib import Path
from typing import List, Tuple, Deque
import logging
import time
from collections import deque

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def read_lines_from_file(path: Path) -> List[str]:
    """Зчитує текстовий файл та повертає список рядків."""
    return path.read_text().splitlines()

def parse_grid(lines: List[str]) -> List[List[str]]:
    """
    Перетворює список рядків у 2D-матрицю символів.
    """
    return [list(row) for row in lines]

DIRECTIONS: List[Tuple[int, int]] = [
    (-1, -1), (-1, 0), (-1, 1),
    (0, -1),          (0, 1),
    (1, -1), (1, 0),  (1, 1)
]

def count_neighbors(grid: List[List[str]]) -> List[List[int]]:
    """
    Підраховує кількість сусідів '@' для кожної клітинки, перевіряємо 8 напрямків.

    Складність: O(H * W * 8) → O(H * W)
    """
    h = len(grid)
    w = len(grid[0])
    neighbors = [[0] * w for _ in range(h)]

    for r in range(h):
        for c in range(w):
            if grid[r][c] != "@":
                continue

            cnt = 0
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if 0 <= nr < h and 0 <= nc < w and grid[nr][nc] == "@":
                    cnt += 1

            neighbors[r][c] = cnt

    return neighbors

def find_initial_queue(grid: List[List[str]], neighbors: List[List[int]]) -> Deque[Tuple[int, int]]:
    """
    Повертає чергу BFS з усіх клітинок '@', які мають < 4 сусідів.

    Складність: O(H * W)
    """
    q = deque()
    h = len(grid)
    w = len(grid[0])

    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@" and neighbors[r][c] < 4:
                q.append((r, c))

    return q

def simulate_full_removal(grid: List[List[str]]) -> int:
    """
    Повна симуляція видалення всіх доступних рулонів паперу. Використовуємо BFS Wave Elimination.

    Складність: O(H * W)

    Повертає: Загальна кількість видалених рулонів.
    """
    h = len(grid)
    w = len(grid[0])

    neighbors = count_neighbors(grid)
    queue = find_initial_queue(grid, neighbors)

    removed = 0

    while queue:
        r, c = queue.popleft()

        # Якщо вже видалили раніше → пропускаємо
        if grid[r][c] != "@":
            continue

        # Видаляємо рулон
        grid[r][c] = "."
        removed += 1

        # Оновлюємо 8 сусідів
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if not (0 <= nr < h and 0 <= nc < w):
                continue

            # Зменшуємо їхній лічильник сусідів
            if grid[nr][nc] == "@":
                neighbors[nr][nc] -= 1

                # Якщо тепер сусідів < 4 → додаємо в BFS-чергу
                if neighbors[nr][nc] < 4:
                    queue.append((nr, nc))

    return removed

def simulate_first_wave(grid: List[List[str]]) -> int:
    """
    Повертає кількість рулонів, які можна прибрати тільки на ПЕРШОМУ кроці. (Part 1)

    Складність: O(H * W)
    """
    neighbors = count_neighbors(grid)
    removed = 0

    h = len(grid)
    w = len(grid[0])

    for r in range(h):
        for c in range(w):
            if grid[r][c] == "@" and neighbors[r][c] < 4:
                removed += 1

    return removed

def task_1(lines: List[str]) -> int:
    """Рішення Part 1."""
    return simulate_first_wave(parse_grid(lines))

def task_2(lines: List[str]) -> int:
    """Рішення Part 2."""
    return simulate_full_removal(parse_grid(lines))

if __name__ == "__main__":
    lines = read_lines_from_file(Path("2025/day4/input.txt"))

    if not lines:
        logging.info("No data to process.")
    else:
        start_time = time.perf_counter()
        result_1 = task_1(lines)
        logging.info(f"Task 1: {result_1} (time: {time.perf_counter() - start_time:.6f}s)")

        start_time = time.perf_counter()
        result_2 = task_2(lines)
        logging.info(f"Task 2: {result_2} (time: {time.perf_counter() - start_time:.6f}s)")