import pytest
from script import task_1, task_2, parse_range

# Приклад з умови задачі
example_ranges = [
    "11-22",
    "95-115",
    "998-1012",
    "1188511880-1188511890",
    "222220-222224",
    "1698522-1698528",
    "446443-446449",
    "38593856-38593862",
    "565653-565659",
    "824824821-824824827",
    "2121212118-2121212124"
]

def test_task_1_example():
    """
    Task 1: старі правила (двічі повторюється підпослідовність)
    За прикладом умови sum = 1227775554
    """
    result = task_1(example_ranges)
    assert result == 1227775554, f"Expected 1227775554, got {result}"

def test_task_2_example():
    """
    Task 2: нові правила (повторюється ≥2 разів)
    За прикладом умови sum = 4174379265
    """
    result = task_2(example_ranges)
    assert result == 4174379265, f"Expected 4174379265, got {result}"

def test_parse_range_valid():
    """
    Перевірка функції parse_range на валідному рядку
    """
    assert parse_range("10-20") == (10, 20)

def test_parse_range_invalid():
    """
    Перевірка parse_range на невалідному рядку
    """
    assert parse_range("abc") is None
    assert parse_range("10-xyz") is None
