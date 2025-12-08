from pathlib import Path
import logging
import time

logging.basicConfig(level=logging.INFO, format="%(message)s")

def load_diagram(lines: list[str]) -> tuple[int, list[int]]:
    """
    Завантажуємо і перетворюємо кожний рядок на бітову маску.
    
    Пояснення:
    - Ми не зберігаємо всю діаграму — лише маски спліттерів.
    - start_col — позиція 'S'
    - splitter_masks — список масок "^" для кожного рядка, де є хоч один "^".
    
    Складність: O(R * C), бо проходимо один раз по даних.
    """
    start_col = -1
    splitter_masks: list[int] = []

    for line in lines:
        line = line.rstrip("\n")
        if "S" in line:
            start_col = line.index("S")

        mask = 0
        for i, ch in enumerate(line):
            if ch == "^":
                mask |= (1 << i)

        if mask != 0:
            splitter_masks.append(mask)

    return start_col, splitter_masks

def count_splits_bitmask(start_col: int, splitter_masks: list[int]) -> int:
    """
    Частина 1: Підрахунок кількості розгалужень.

    Алгоритм:
    - Використовуємо одну довгу бітову маску Python int — beam_mask.
    - Якщо beam_mask & splitter_mask != 0 → відбувається split.
    - Split = знищити старий промінь, створити два нових (вліво та вправо).
    
    Складність:
        Час:  O(R) — найкраща теоретична складність.
        Памʼять: O(1) (маска — один int).
    """
    beam_mask = 1 << start_col
    total_splits = 0

    for mask in splitter_masks:
        # Які промені потрапили у спліттери
        hits = beam_mask & mask
        if hits:
            total_splits += hits.bit_count()

        # Промінь, який НЕ потрапив у спліттер, йде далі вниз
        survivors = beam_mask & ~mask

        # Нові промені — ліворуч і праворуч
        left = hits << 1
        right = hits >> 1

        beam_mask = survivors | left | right

    return total_splits

def count_timelines_dp(start_col: int, splitter_masks: list[int]) -> int:
    """
    Частина 2: Підрахунок кількості фінальних таймлайнів.

    Ідея алгоритму:
    - Ми не зберігаємо dp на весь рядок (що занадто дорого).
    - Зберігаємо тільки "активні колонки" і "кількість шляхів до них".
    - При спліттері dp[col] переноситься у dp[col-1] і dp[col+1].
    - При відсутності спліттера колонка просто копіюється вниз.
    
    Складність:
        Час:  O(S_total) — оптимально (кожний "^" обробляється один раз).
        Пам'ять: O(A), де A = кількість активних колонок.
    """
    active_cols = [start_col]
    active_vals = [1]

    for mask in splitter_masks:
        new_cols: dict[int, int] = {}

        for col, val in zip(active_cols, active_vals):
            is_splitter = (mask >> col) & 1

            if is_splitter:
                # оригінальний шлях зникає, а зʼявляється два нових
                new_cols[col - 1] = new_cols.get(col - 1, 0) + val
                new_cols[col + 1] = new_cols.get(col + 1, 0) + val
            else:
                # Промінь просто падає вниз
                new_cols[col] = new_cols.get(col, 0) + val

        # Перетворюємо назад у два паралельні списки
        active_cols = sorted(new_cols.keys())
        active_vals = [new_cols[c] for c in active_cols]

    return sum(active_vals)

def read_lines_from_file(path: Path) -> list[str]:
    try:
        return path.read_text().splitlines()
    except FileNotFoundError:
        return []

if __name__ == "__main__":
    lines = read_lines_from_file(Path("2025/day7/input.txt"))

    if not lines:
        logging.info("No data to process.")
        exit(0)

    start_col, splitter_masks = load_diagram(lines)

    start = time.perf_counter()
    result_1 = count_splits_bitmask(start_col, splitter_masks)
    logging.info(f"Task 1: {result_1}\t\t(time: {time.perf_counter() - start:.6f}s)")

    start = time.perf_counter()
    result_2 = count_timelines_dp(start_col, splitter_masks)
    logging.info(f"Task 2: {result_2}\t(time: {time.perf_counter() - start:.6f}s)")
