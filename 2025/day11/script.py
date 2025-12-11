"""
Програма для підрахунку кількості всіх шляхів у орієнтованому ациклічному графі (DAG).
Підрахунок виконується як:
- Для Part 1: кількість шляхів від "you" до "out"
- Для Part 2: максимальне добуток кількостей шляхів по заданих послідовностях вершин
Оптимізовано для великих графів (сотні тисяч вузлів, мільйони ребер).

Використані алгоритми:
1. BFS для визначення релевантного підграфа.
2. Kahn Topological Sort (Kahn, 1962) для топологічного порядку.
3. Dynamic Programming (DP) на DAG для підрахунку кількості шляхів (класичний DP на DAG).
"""

import logging
import time
from pathlib import Path
from typing import Dict, List, Set
from collections import deque

logging.basicConfig(level=logging.INFO, format="%(message)s")


def parse_graph(filename: Path) -> Dict[str, List[str]]:
    """
    Парсинг графа з файлу.
    Формат рядка: node: neighbor1 neighbor2 ...

    Вхідні дані:
        filename - шлях до файлу

    Повертає:
        graph: словник node -> list of neighbors

    Складність: O(V + E), де V - кількість вершин, E - кількість ребер
    """
    graph: Dict[str, List[str]] = {}
    with open(filename, "r", encoding="utf-8") as f:
        for line in f:
            s = line.strip()
            if not s or ":" not in s:
                continue
            node, rest = line.split(":", 1)
            node = node.strip()
            if rest.strip():
                graph[node] = rest.split()
            else:
                graph[node] = []

    # Переконатись, що всі згадані сусіди теж є ключами
    for _, nbrs in list(graph.items()):
        for v in nbrs:
            if v not in graph:
                graph[v] = []

    return graph


def build_index(graph: Dict[str, List[str]]):
    """
    Перетворює словник з іменами вузлів у компактну індексацію int для швидкого доступу.

    Вхідні дані:
        graph - словник node -> neighbors

    Повертає:
        name_to_id: Dict[str, int] - мапування імен вузлів на індекси
        adj: List[List[int]] - список суміжності з int індексами

    Алгоритм:
    - Створюємо словник name -> id
    - Створюємо порожній список суміжності
    - Замінюємо імена сусідів на індекси

    Складність: O(V + E)
    """
    names = list(graph.keys())
    name_to_id = {name: i for i, name in enumerate(names)}
    n = len(names)
    adj: List[List[int]] = [[] for _ in range(n)]
    for u_name, nbrs in graph.items():
        u = name_to_id[u_name]
        for v_name in nbrs:
            adj[u].append(name_to_id[v_name])
    return name_to_id, adj


def build_rev(adj: List[List[int]]) -> List[List[int]]:
    """
    Створює зворотній граф (reverse graph) для швидкого обходу до цільових вершин.

    Вхідні дані:
        adj - список суміжності

    Повертає:
        rev - список суміжності зворотнього графа

    Складність: O(V + E)
    """
    n = len(adj)
    rev = [[] for _ in range(n)]
    for u, nbrs in enumerate(adj):
        for v in nbrs:
            rev[v].append(u)
    return rev


def bfs_reachable_from(starts: List[int], adj: List[List[int]]) -> Set[int]:
    """
    BFS для визначення всіх вершин, до яких можна дістатись з певних стартових вузлів.

    Вхідні дані:
        starts - список стартових вузлів
        adj - список суміжності

    Повертає:
        seen - множина всіх досяжних вузлів

    Алгоритм:
    - Класичний BFS
    - Використовується deque для черги
    - Перевірка відвіданих вузлів

    Складність: O(V_r + E_r), де V_r і E_r - вузли та ребра в релевантному підграфі
    """
    seen: Set[int] = set()
    dq = deque(starts)
    while dq:
        u = dq.popleft()
        if u in seen:
            continue
        seen.add(u)
        for v in adj[u]:
            if v not in seen:
                dq.append(v)
    return seen


class PathsComputer:
    """
    Клас для обчислення кількості шляхів від будь-якого вузла до цільового.
    Використовує:
    - Кешування результатів DP (для швидкого повторного доступу)
    - Обхід релевантного підграфа
    - Topological sort (Kahn)
    - DP по DAG
    """

    def __init__(self, adj: List[List[int]], rev: List[List[int]]):
        self.adj = adj
        self.rev = rev
        self.n = len(adj)
        self.cache: Dict[int, Dict[int, int]] = {} # target -> node->#paths
        self.infinite_targets: Set[int] = set()    # targets з нескінченними шляхами (цикли)

    def compute_paths_to(self, target: int):
        """
        Обчислює кількість шляхів до target для всіх релевантних вузлів.

        Алгоритм:
        1. Знаходимо всі вузли, які можуть дістатись до target (BFS на rev)
        2. Створюємо in-degree для релевантних вузлів
        3. Топологічне сортування Kahn
        4. DP у зворотному порядку топології
        5. Якщо є цикл у релевантному підграфі -> infinite_targets

        Складність: O(V_r + E_r), де V_r і E_r - вузли та ребра релевантного підграфа
        """
        if target in self.cache or target in self.infinite_targets:
            return

        relevant = bfs_reachable_from([target], self.rev)
        if not relevant:
            self.cache[target] = {}
            return

        in_deg = {u: 0 for u in relevant}
        for u in relevant:
            for v in self.adj[u]:
                if v in in_deg:
                    in_deg[v] += 1

        q = [u for u, d in in_deg.items() if d == 0]
        topo = []
        idx = 0
        while idx < len(q):
            u = q[idx]; idx += 1
            topo.append(u)
            for v in self.adj[u]:
                if v not in in_deg:
                    continue
                in_deg[v] -= 1
                if in_deg[v] == 0:
                    q.append(v)

        if len(topo) != len(relevant):
            self.infinite_targets.add(target)
            return

        # DP по DAG у зворотному порядку топології
        paths: Dict[int, int] = {target: 1}
        for u in reversed(topo):
            if u == target:
                continue
            total = 0
            for v in self.adj[u]:
                if v in paths:
                    total += paths[v]
            if total:
                paths[u] = total
        self.cache[target] = paths

    def count_paths(self, a: int, b: int) -> float | int:
        """
        Повертає кількість шляхів a -> b:
        - int >= 0: кількість шляхів
        - float('inf'): нескінченна кількість шляхів через цикл
        - 0: якщо шляху немає

        Складність:
            O(V_r + E_r) для нового target
            O(1) для повторного виклику через кеш
        """
        if b < 0 or b >= self.n or a < 0 or a >= self.n:
            return 0
        self.compute_paths_to(b)
        if b in self.infinite_targets:
            paths_dict = self.cache.get(b, {})
            seen = set()
            dq = deque([a])
            while dq:
                u = dq.popleft()
                if u in seen:
                    continue
                seen.add(u)
                if u == b:
                    return float("inf")
                if paths_dict and u in paths_dict:
                    return float("inf")
                for v in self.adj[u]:
                    if v not in seen:
                        dq.append(v)
            return 0
        paths = self.cache.get(b, {})
        return paths.get(a, 0)


def max_path_product(paths_comp: PathsComputer, paths_list: List[List[int]]) -> float | int:
    """
    Обчислює максимальний добуток кількостей шляхів по заданих послідовностях вершин.

    Алгоритм:
    - Для кожного шляху:
        - Перемножуємо кількість шляхів між парами вузлів
        - Якщо зустрічається нескінченна кількість -> повертаємо float('inf')
    - Повертає максимальний добуток серед всіх шляхів

    Складність:
        O(k * len(path) * (V_r + E_r)), де k - кількість послідовностей,
        але DP для кожного target виконується лише один раз
    """
    best = 0
    for path in paths_list:
        prod = 1
        infinite = False
        for a, b in zip(path, path[1:]):
            val = paths_comp.count_paths(a, b)
            if val == float("inf"):
                infinite = True
                break
            prod *= val
            if prod == 0:
                break
        if infinite:
            return float("inf")
        if prod > best:
            best = prod
    return best


def format_result(x: float | int) -> str:
    """
    Форматує результат для виводу
    """
    if x == float("inf"):
        return "infinite"
    return str(x)


def main():
    graph = parse_graph(Path("2025/day11/input.txt"))
    if not graph:
        logging.info("No data to process.")
        return

    # Індексування вузлів для швидкого доступу
    name_to_id, adj = build_index(graph)
    rev = build_rev(adj)
    pc = PathsComputer(adj, rev)

    logging.info(f"Nodes: {len(adj)}, Edges: {sum(len(x) for x in adj)}\n")

    # --- Part 1 ---
    start_id = name_to_id.get("you", None)
    end_id = name_to_id.get("out", None)

    start_time = time.perf_counter()
    if start_id is None or end_id is None:
        part1 = 0
    else:
        part1 = pc.count_paths(start_id, end_id)
    logging.info(f"Part 1: {format_result(part1)}\t\t(time: {time.perf_counter() - start_time:.6f}s)")

    # --- Part 2 ---
    raw_paths = [
        ["svr", "fft", "dac", "out"],
        ["svr", "dac", "fft", "out"]
    ]

    # Переведення імен у індекси
    start_time = time.perf_counter()
    id_paths = [[name_to_id.get(name, -1) for name in p] for p in raw_paths]
    part2 = max_path_product(pc, id_paths)
    logging.info(f"Part 2: {format_result(part2)}\t(time: {time.perf_counter() - start_time:.6f}s)")


if __name__ == "__main__":
    main()
