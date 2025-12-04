import pytest
from script import max_joltage_monotonic, task_1, task_2

@pytest.mark.parametrize(
    "bank,n,expected",
    [
        # Приклади з умови Task 1 (n = 2)
        ([9,8,7,6,5,4,3,2,1,1,1,1,1,1], 2, 98),
        ([8,1,1,1,1,1,1,1,1,1,1,1,1,9], 2, 89),
        ([2,3,4,2,3,4,2,3,4,2,7,8], 2, 78),
        ([8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], 2, 92),

        # Task 2 (n = 12)
        ([9,8,7,6,5,4,3,2,1,1,1,1,1,1], 12, 987654321111),
        ([8,1,1,1,1,1,1,1,1,1,1,1,1,9], 12, 811111111119),
        ([2,3,4,2,3,4,2,3,4,2,7,8],     12, 434234234278),
        ([8,1,8,1,8,1,9,1,1,1,1,2,1,1,1], 12, 888911112111),
    ]
)
def test_max_joltage_monotonic(bank, n, expected):
    assert max_joltage_monotonic(bank, n) == expected


def test_task_1_example():
    lines = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_total = 98 + 89 + 78 + 92  # 357
    assert task_1(lines) == expected_total


def test_task_2_example():
    lines = [
        "987654321111111",
        "811111111111119",
        "234234234234278",
        "818181911112111",
    ]
    expected_total = (
        987654321111
        + 811111111119
        + 434234234278
        + 888911112111
    )  # 3121910778619
    assert task_2(lines) == expected_total
