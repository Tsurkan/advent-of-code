from script import task_1, task_2

example_lines = [
        "L68",
        "L30",
        "R48",
        "L5",
        "R60",
        "L55",
        "L1",
        "L99",
        "R14",
        "L82",
    ]

print(f"Example Task 1 expected 3 → got: {task_1(example_lines)}")
print(f"Example Task 2 expected 6 → got: {task_2(example_lines)}")