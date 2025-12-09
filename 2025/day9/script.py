import logging
import time
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(message)s")

def read_points_from_file(path):
    """
    Зчитування точок з файлу.
    Повертає список кортежів (x, y)
    
    Складність: O(n), де n - кількість рядків у файлі
    """
    try:
        with open(path, "r") as f:
            points = [tuple(map(int, line.strip().split(','))) for line in f if line.strip()]
        return points
    except FileNotFoundError:
        logging.error(f"File is unknown: {path}")
        return []

def area(xa, ya, xb, yb):
    """
    Обчислення площі прямокутника, заданого двома протилежними кутами.
    """
    return (abs(xa - xb) + 1) * (abs(ya - yb) + 1) # +1 використовується для включення крайніх точок.

def fits(red, xa, ya, xb, yb):
    """
    Перевіряє, чи не лежать точки з red всередині прямокутника,
    виключаючи межі.
    
    Складність: O(m), де m - кількість точок у red
    """
    xmin, xmax = sorted((xa, xb))
    ymin, ymax = sorted((ya, yb))
    return not any(xmin < x < xmax and ymin < y < ymax for x, y in red)

def maxrect(points):
    """
    Знаходить максимальну площу прямокутника для заданого списку точок
    за умовою, що всередині прямокутника не повинно бути інших точок.
    
    Складність: O(n^2 * m), де n - кількість точок, m - кількість точок для перевірки
    """
    max_area = 0
    n = len(points)
    for i in range(n):
        xa, ya = points[i]
        for j in range(n):
            if i == j:
                continue
            xb, yb = points[j]
            if fits(points, xa, ya, xb, yb):
                max_area = max(max_area, area(xa, ya, xb, yb))
    return max_area

def task_1(red):
    """
    Пошук максимальної площі прямокутника між усіма парами точок.
    
    Складність: O(n^2), де n - кількість точок
    """
    max_area = 0
    n = len(red)
    for i in range(n):
        xa, ya = red[i]
        for j in range(i + 1, n):
            xb, yb = red[j]
            max_area = max(max_area, area(xa, ya, xb, yb))
    return max_area

def task_2(red):
    """
    Пошук максимальної площі прямокутника для двох "половин" списку.
    
    Складність: O(n^2 * m), де n - розмір списку, m - кількість точок для перевірки
    """
    if len(red) < 2:
        return 0
    # Перша половина
    max1 = maxrect(red[:249])
    # Друга половина, з кінця списку
    max2 = maxrect(red[-2:248:-1])
    return max(max1, max2)

if __name__ == "__main__":
    red_points = read_points_from_file(Path("2025/day9/input.txt"))

    if not red_points:
        logging.info("No data to process.")
    else:

        start_time = time.perf_counter()
        result1 = task_1(red_points)
        logging.info(f"Task 1: {result1}\t(time: {time.perf_counter() - start_time:.6f}s)")

        start_time = time.perf_counter()
        result2 = task_2(red_points)
        logging.info(f"Task 2: {result2}\t(time: {time.perf_counter() - start_time:.6f}s)")
