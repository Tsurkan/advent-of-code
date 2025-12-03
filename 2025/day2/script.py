from pathlib import Path
import logging
import time
from typing import Iterator

logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s: %(message)s"
)

def read_lines_from_file(path: Path) -> list[str]:
    """
    Читаємо файл і повертаємо список рядків.
    """
    try:
        return path.read_text(encoding="utf-8").strip().split(",")
    except FileNotFoundError:
        logging.error(f"File not found: {path}")
        return []
    except Exception as exc:
        logging.error(f"Error reading file {path}: {exc}")
        return []

def parse_range(rng: str) -> tuple[int, int] | None:
    """
    Розділяємо рядок 'start-end' у (int(start), int(end))
    """
    try:
        start_str, end_str = rng.split("-")
        return int(start_str), int(end_str)
    except Exception as exc:
        logging.warning(f"Invalid range {rng!r}: {exc}")
        return None

def is_double_sequence(num: int) -> bool:
    """
    Перевіряємо правило для першої частини завдання.
    Число невалідне, якщо воно = A + A, тобто рівно два повторення.
    Алгоритм:
    - O(L) для числа довжини L
    """
    s = str(num)
    L = len(s)
    if L % 2 != 0:
        return False
    mid  = L // 2
    return s[:mid] == s[mid:]

def is_repeated_pattern(num: int) -> bool:
    """
    Число невалідне, якщо воно складається з повторення
    одного і того ж блоку мінімум 2 рази.

    Наприклад:
        123123123  → "123" * 3
        121212     → "12" * 3
        1111111    → "1" * 7

    Перебираємо можливу довжину блоку: O(L²)
    """
    s = str(num)
    L = len(s)

    # довжина блоку може бути від 1 до L//2
    for block_size in range(1, L // 2 + 1):
        if L % block_size != 0:
            continue
        block = s[:block_size]
        if block * (L // block_size) == s:
            return True

    return False

def task_1(ranges: list[str]) -> int:
    """
    Рахуємо числа, які підпадають під умову для першої частини.

    Складність: O(N * L/2), де N — кількість чисел у всіх діапазонах, L — довжина числа
    """
    total = 0
    for rng in ranges:
        parsed = parse_range(rng)
        if parsed is None:
            continue
        start, end = parsed
        for num in range(start, end + 1):
            if is_double_sequence(num):
                total += num
    return total

def task_2_v1(ranges: list[str]) -> int:
    """
    Перша не оптимізована реалізація.
    Число invalid якщо будь-яка послідовність повторюється >=2 разів

    Складність: O(N * L²). На практиці працює швидко, бо L ≤ 10.
    """
    total = 0
    for rng in ranges:
        parsed = parse_range(rng)
        if parsed is None:
            continue
        start, end = parsed
        for num in range(start, end + 1):
            if is_repeated_pattern(num):
                total += num
    return total

def generate_candidates(length_max: int) -> Iterator[int]:
    """
    Генерує всі числа, які складаються з повторення однієї й тієї ж послідовності цифр.
    Приклад:
        base = "123" → "123123", "123123123", ...

    Обмеження:
        - Загальна довжина числа ≤ length_max
        - repeat >= 2 (повторення мінімум двічі — згідно правил задачі)

    Чому цей метод оптимальний?
        Замість перебору всіх чисел у діапазонах (що може бути мільярди комбінацій),
        ми перебираємо тільки можливі патерни, тобто → BLOCK × REPEAT.

        Це дає складність O(P), де P — кількість можливих патернів,
        і вона в десятки тисяч разів менша за повний перебір.
    """
    # Перебираємо можливу довжину блоку (половина від максимальної довжини числа)
    for part_len in range(1, length_max // 2 + 1):
        
        # base — це саме повторювана частина
        start_base = 10 ** (part_len - 1)
        end_base = 10 ** part_len

        for base in range(start_base, end_base):
            s = str(base)
            
            # repeat починається з 2 шт — мінімум два повторення
            k = 2
            while len(s) * k <= length_max:
                yield int(s * k)
                k += 1

def filter_candidates_for_range(start: int, end: int, candidates: list[int]) -> Iterator[int]:
    """Повертає кандидатів, які потрапляють у діапазон.
    Чому так?
        - Усі кандидати відсортовані
        - Діапазон може бути великим, але фільтрація O(P) дуже швидка
        - Повторну генерацію патернів ми не робимо (економимо час у рази)
    """
    for c in candidates:
        if start <= c <= end:
            yield c

def task_2(ranges: list[str]) -> int:
    """Оптимізований Task 2 — знаходимо числа, які складаються
    з повторення однієї й тієї ж послідовності цифр ≥ 2 рази.

    Основна ідея:
        - Не перевіряємо кожне число у діапазонах.
        - Генеруємо лише ті числа, які МОЖУТЬ бути невалідними за визначенням.
        - Потім лише перевіряємо, чи входять вони у діапазон.

    Алгоритм:
        1. Знаходимо максимальну довжину чисел серед усіх діапазонів.
        2. Генеруємо ВСІ можливі повторювані числа (кандидати),
           наприклад:
              "1"*6 = 111111
              "12"*3 = 121212
              "824824" = "824" * 2
        3. Сортуємо й унікалізуємо (set) → гарантує, що "1111" (1*4) і "1111" (11*2)
           не додадуться подвійно.
        4. Для кожного діапазону фільтруємо ці кандидати та додаємо в суму.

    Чому це працює швидше?
        - Найважче — перебирати діапазони довжиною тисячі–мільйони чисел.
        - Але кількість можливих повторюваних чисел дуже мала.
        - Наприклад: для довжин до 12 цифр — це всього кілька сотень тисяч патернів.

    Складність:
        O(P + R * log(P)), де: P — кількість патернів, R — кількість діапазонів.
    """

    # 1. Знайти максимальну довжину чисел серед усіх діапазонів
    global_max_len = max(len(str(parse_range(r)[1])) for r in ranges)

    # 2. Згенерувати всі унікальні кандидати
    candidates = sorted(set(generate_candidates(global_max_len)))

    total = 0

    # 3. Перевірити кожен діапазон
    for rng in ranges:
        parsed = parse_range(rng)
        if parsed is None:
            continue

        start, end = parsed

        # 4. Вибрати кандидатів, що входять у діапазон
        for c in filter_candidates_for_range(start, end, candidates):
            total += c

    return total

if __name__ == "__main__":
    ranges = read_lines_from_file(Path("2025/day2/input.txt"))
    if not ranges:
        logging.info("No ranges to process.")
    else:
        start_time = time.perf_counter()
        result_1 = task_1(ranges)
        end_time = time.perf_counter()
        logging.info(f"Task 1: {result_1}")
        logging.info(f"Execution time: {end_time - start_time:.6f} seconds")

        start_time = time.perf_counter()
        result_2 = task_2(ranges)
        end_time = time.perf_counter()
        logging.info(f"Task 2: {result_2}")
        logging.info(f"Execution time: {end_time - start_time:.6f} seconds")
