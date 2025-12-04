import pytest
from script import (
    parse_grid,
    count_neighbors,
    simulate_first_wave,
    simulate_full_removal,
    task_1,
    task_2,
)

# ---------------------------------------------------------
#   ТЕСТИ ЗА ПРИКЛАДОМ ІЗ ЗАВДАННЯ
# ---------------------------------------------------------

EXAMPLE = [
    "..@@.@@@@.",
    "@@@.@.@.@@",
    "@@@@@.@.@@",
    "@.@@@@..@.",
    "@@.@@@@.@@",
    ".@@@@@@@.@",
    ".@.@.@.@@@",
    "@.@@@.@@@@",
    ".@@@@@@@@.",
    "@.@.@@@.@.",
]

def test_task1_example():
    assert task_1(EXAMPLE) == 13

def test_task2_example():
    assert task_2(EXAMPLE) == 43


# ---------------------------------------------------------
#   ДОДАТКОВІ ТЕСТИ НА КРАЙОВІ ВИПАДКИ
# ---------------------------------------------------------

def test_empty_grid():
    """Порожня сітка не містить рулонів."""
    lines = ["....", "...."]
    assert task_1(lines) == 0
    assert task_2(lines) == 0

def test_full_dense_block():
    """
    Повний блок '@' 3x3.
    """
    lines = [
        "@@@",
        "@@@",
        "@@@",
    ]
    assert task_1(lines) == 4
    assert task_2(lines) == 9

def test_single_roll():
    """Один рулон паперу завжди доступний одразу."""
    lines = ["@"]

    assert task_1(lines) == 1
    assert task_2(lines) == 1

def test_two_adjacent_rolls():
    """
    Два сусідні '@' — кожен має лише 1 сусіда, отже обидва будуть видалені.
    """
    lines = ["@@"]

    assert task_1(lines) == 2
    assert task_2(lines) == 2

def test_line_of_three():
    """
    '@@@' → середній має 2 сусідів, крайні — по 1.
    """
    lines = ["@@@"]

    assert task_1(lines) == 3
    assert task_2(lines) == 3


# ---------------------------------------------------------
#   ТЕСТИ ВНУТРІШНІХ ФУНКЦІЙ 
# ---------------------------------------------------------

def test_count_neighbors_simple():
    grid = parse_grid([
        ".@.",
        "@@@",
        ".@.",
    ])
    neigh = count_neighbors(grid)

    # Центральна клітинка має 4 сусіди
    assert neigh[1][1] == 4

def test_first_wave_detection():
    grid = parse_grid([
        "@.@",
        ".@.",
        "@.@",
    ])
    # Центральний '@' має 4 сусіди → недоступний.
    assert simulate_first_wave(grid) == 4

def test_full_removal_cascade():
    """
    Перевірка, що каскадне видалення працює:
    структура, де всі '@' мають бути видалені хвилеподібно.
    """
    grid = parse_grid([
        ".@.",
        "@@@",
        ".@.",
    ])

    assert simulate_full_removal(grid) == 5
