import logging
import time
from pathlib import Path
from typing import List, Dict
import pulp
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(message)s")


def read_input(file_path: Path) -> List[Dict]:
    """
    Читання вхідних даних з файлу.
    
    Параметри:
        file_path: шлях до файлу з описом машин
    
    Повертає:
        Список словників для кожної машини:
            "lights" - список символів '#' або '.' для лампочок
            "buttons" - список списків індексів лампочок, які впливають кнопки
            "joltages" - список цілих чисел джолтажів для лампочок

    Складність: O(L * B), де L - кількість лампочок, B - кількість кнопок
    """
    if not file_path.exists():
        logging.info(f"No data to process: {file_path}")
        return []

    machines = []
    with file_path.open("r") as f:
        for line in f:
            parts = line.strip().split(" ")
            try:
                # Парсимо лампочки
                lights = list(parts[0][1:-1])
                # Парсимо кнопки: кожна кнопка - список індексів лампочок
                buttons = [list(map(int, btn[1:-1].split(","))) for btn in parts[1:-1]]
                # Парсимо джолтажі
                joltages = list(map(int, parts[-1][1:-1].split(",")))
                machines.append({"lights": lights, "buttons": buttons, "joltages": joltages})
            except Exception as e:
                logging.warning(f"Skipping invalid line: {line.strip()} ({e})")
    return machines


def part_one(machines: List[Dict]) -> int:
    """
    Частина 1: знаходимо мінімальну кількість натискань кнопок для досягнення цільового стану лампочок.
    
    Суть рішення:
    - Кожну лампочку кодуємо бітами (1 - увімкнена '#', 0 - вимкнена '.')
    - Кожну кнопку також кодуємо як бітову маску лампочок, які вона змінює (XOR)
    - Задача зводиться до пошуку мінімального числа комбінацій кнопок, що дають target_mask.
    - Використовуємо BFS по бітових масках. Це схоже на алгоритм "Shortest Path in Unweighted Graph".
    
    Чому не обійтись без BFS:
    - Простий перебір всіх 2^B комбінацій кнопок працює тільки для B < 25-30.
    - BFS гарантує мінімальне число натискань і працює ефективно для B ~ 200 (завдяки побітовому представлення).
    
    Складність:
        - У найгіршому випадку O(2^B * B), де B - кількість кнопок
        - Практично швидше завдяки відсіканню вже відвіданих масок.
    """
    total_min_presses = 0

    for machine in machines:
        lights = machine["lights"]
        buttons = machine["buttons"]

        # Цільова маска лампочок
        target_mask = sum(1 << i for i, c in enumerate(lights) if c == "#")

        # Маски кнопок
        button_masks = [sum(1 << idx for idx in btn) for btn in buttons]

        # BFS по масках для мінімального числа натискань
        visited = {0: 0}  # словник: маска -> мінімальна кількість натискань
        queue = deque([0])

        while queue:
            current_mask = queue.popleft()
            current_steps = visited[current_mask]

            if current_mask == target_mask:
                total_min_presses += current_steps
                break

            for mask in button_masks:
                next_mask = current_mask ^ mask  # застосування кнопки через XOR
                if next_mask not in visited or visited[next_mask] > current_steps + 1:
                    visited[next_mask] = current_steps + 1
                    queue.append(next_mask)

    return total_min_presses


def part_two(machines: List[Dict]) -> int:
    """
    Частина 2: мінімізація загальної кількості натискань кнопок для джолтажів (числових значень).
    
    Суть рішення:
    - Задача перетворюється на лінійне ціле програмування (Integer LP) через pulp:
    - Це класична задача мінімізації лінійної цільової функції з цілими обмеженнями.
    
    Чому саме pulp:
    - Інші методи (BFS по сумі, динаміка) не підходять для джолтажів > 1
    - LP забезпечує точне рішення для будь-яких цілих джолтажів
    - Підходить для задач до сотень кнопок і лампочок (для 20-30 можна було залишити BFS)
    
    Складність:
        - LP через CBC теоретично експоненційна, але на практиці швидка для помірних розмірів (до ~200 кнопок)
        - Побудова моделі O(B * L), де B - кнопки, L - лампочки
    """
    total_presses = 0

    for machine in machines:
        buttons = machine["buttons"]
        joltages = machine["joltages"]

        # Видаляємо кнопки, що ні на що не впливають
        useful_buttons = []
        button_mapping = {}
        for idx, btn in enumerate(buttons):
            if btn:
                button_mapping[len(useful_buttons)] = idx
                useful_buttons.append(btn)

        # Видаляємо джолтажі, що ні від чого не залежать
        useful_joltages = []
        for idx, val in enumerate(joltages):
            if any(idx in btn for btn in useful_buttons):
                useful_joltages.append((idx, val))

        if not useful_buttons or not useful_joltages:
            total_presses += 0
            continue

        # Матриця впливу кнопок на лампочки
        influence_matrix = [
            [1 if light_idx in btn else 0 for btn in useful_buttons]
            for light_idx, _ in useful_joltages
        ]
        target_joltages = [val for _, val in useful_joltages]

        # LP задача
        prob = pulp.LpProblem("MinButtonPresses", pulp.LpMinimize)
        button_presses = [pulp.LpVariable(f"btn_{i}", lowBound=0, cat="Integer")
                          for i in range(len(useful_buttons))]

        # Цільова функція
        prob += pulp.lpSum(button_presses)

        # Обмеження
        for row_idx, row in enumerate(influence_matrix):
            prob += pulp.lpSum(row[col_idx] * button_presses[col_idx]
                               for col_idx in range(len(useful_buttons))) == target_joltages[row_idx]

        # Рішення LP через CBC (точне ціле рішення)
        prob.solve(pulp.PULP_CBC_CMD(msg=False))

        # Сума натискань
        solution = [int(v.value()) for v in button_presses]
        total_presses += sum(solution)

    return total_presses


if __name__ == "__main__":
    machines = read_input(Path("2025/day10/input.txt"))
    if not machines:
        logging.info("No data to process.")
    else:
        start_time = time.perf_counter()
        result1 = part_one(machines)
        logging.info(f"Part 1: {result1}\t(time: {time.perf_counter() - start_time:.6f}s)")

        start_time = time.perf_counter()
        result2 = part_two(machines)
        logging.info(f"Part 2: {result2}\t(time: {time.perf_counter() - start_time:.6f}s)")
