import logging
import time
from pathlib import Path
from typing import List, Tuple, Optional
from math import ceil
import heapq

logging.basicConfig(level=logging.INFO, format="%(message)s")


# ==============================
# ======== Disjoint Set ========
# ==============================

class DisjointSet:
    """
    Структура даних Disjoint Set Union (DSU) / Union-Find.
    Використовується для швидкого об'єднання компонентів та перевірки їх належності.

    Оптимізації:
    - Path compression: зменшує висоту дерева при find()
    - Union by rank: додає менше дерево до більшого, зменшує глибину

    Складність:
        - __init__: O(n)
        - find: O(α(n)), де α(n) — функція інверсії Аккермана, майже константа.
        - union: O(α(n)), де α(n) — функція інверсії Аккермана
        - get_component_sizes: O(n)
    """
    def __init__(self, size: int):
        self.parent = list(range(size))  # батько кожного елементу
        self.rank = [0] * size           # ранг дерева
        self.size = [1] * size           # розмір компоненту
        self.components = size           # кількість компонентів

    def find(self, node: int) -> int:
        """Знаходить корінь компоненту node з path compression"""
        if self.parent[node] != node:
            self.parent[node] = self.find(self.parent[node])
        return self.parent[node]

    def union(self, a: int, b: int) -> bool:
        """
        Об'єднує два компоненти a і b.
        Повертає True, якщо вони були різними, False — якщо вже в одному компоненті.
        Складність: O(α(n)), де α(n) — функція інверсії Аккермана
        """
        root_a = self.find(a)
        root_b = self.find(b)
        if root_a == root_b:
            return False
        if self.rank[root_a] < self.rank[root_b]:
            root_a, root_b = root_b, root_a
        self.parent[root_b] = root_a
        self.size[root_a] += self.size[root_b]
        if self.rank[root_a] == self.rank[root_b]:
            self.rank[root_a] += 1
        self.components -= 1
        return True

    def get_component_sizes(self) -> List[int]:
        """
        Повертає список розмірів всіх компонентів.
        Складність: O(n)
        """
        root_sizes = [0] * len(self.parent)
        for i in range(len(self.parent)):
            root_sizes[self.find(i)] += 1
        return [sz for sz in root_sizes if sz > 0]


# ==============================
# ========== KD-Tree ==========
# ==============================

class KDNode:
    """
    Вузол KD-дерева для пошуку k найближчих сусідів у 3D.
    __slots__ для зменшення пам'яті.
    """
    __slots__ = ("point", "index", "left", "right", "axis")

    def __init__(self, point: Tuple[int, int, int], index: int, axis: int):
        self.point = point        # координати точки (x, y, z)
        self.index = index        # індекс точки у масиві
        self.left: Optional[KDNode] = None   # ліве піддерево
        self.right: Optional[KDNode] = None  # праве піддерево
        self.axis = axis          # вісь розділу (0=x,1=y,2=z)


def build_kdtree(points_with_index: List[Tuple[Tuple[int, int, int], int]], depth: int = 0) -> Optional[KDNode]:
    """
    Рекурсивне побудова KD-дерева.
    Середня складність: O(n log n)
    Гірший випадок: O(n log^2 n) через сортування на кожному рівні
    """
    if not points_with_index:
        return None
    axis = depth % 3
    points_with_index.sort(key=lambda pi: pi[0][axis])
    mid = len(points_with_index) // 2
    node = KDNode(points_with_index[mid][0], points_with_index[mid][1], axis)
    node.left = build_kdtree(points_with_index[:mid], depth + 1)
    node.right = build_kdtree(points_with_index[mid + 1:], depth + 1)
    return node


def distance_squared(a: Tuple[int, int, int], b: Tuple[int, int, int]) -> int:
    """Квадрат евклідової відстані (O(1))"""
    return (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2 + (a[2] - b[2]) ** 2


def k_nearest_neighbors(node: Optional[KDNode], target: Tuple[int, int, int], k: int, heap: List[Tuple[int, int]]):
    """
    Рекурсивний пошук k найближчих сусідів. Використовується heap.
    Складність: O(log n) на проходження дерева × O(log k) на heap операції
    """
    if node is None:
        return

    d = distance_squared(target, node.point)
    if len(heap) < k:
        heapq.heappush(heap, (-d, node.index))
    elif d < -heap[0][0]:
        heapq.heappushpop(heap, (-d, node.index))

    axis = node.axis
    diff = target[axis] - node.point[axis]

    first = node.left if diff < 0 else node.right
    second = node.right if diff < 0 else node.left

    k_nearest_neighbors(first, target, k, heap)
    if len(heap) < k or diff * diff < -heap[0][0]:
        k_nearest_neighbors(second, target, k, heap)


# ==============================
# ========== Utilities =========
# ==============================

def read_points(file_path: Path) -> List[Tuple[int, int, int]]:
    """
    Читання точок з файлу, формат x,y,z
    Складність: O(n)
    """
    with open(file_path, "r", encoding="utf-8") as f:
        return [tuple(map(int, line.strip().split(","))) for line in f if line.strip()]


def build_candidate_edges(points: List[Tuple[int, int, int]], requested_edges: int = 1000, safety_factor: float = 2.0) -> List[Tuple[int, int, int]]:
    """
    Генерація candidate edges для графу.
    Варіанти:
    1. Малий n: повний перебір всіх пар (O(n^2))
    2. Великий n: KD-дерево O(n log n) + kNN (O(k log n))
    """
    n = len(points)
    max_pairs = n * (n - 1) // 2

    if max_pairs <= requested_edges * 4 or n <= 3000:
        edges = []
        t0 = time.perf_counter()
        for i in range(n):
            for j in range(i + 1, n):
                edges.append((distance_squared(points[i], points[j]), i, j))
        logging.info(f"Full all-pairs computed: n={n}, pairs={max_pairs}, time={(time.perf_counter() - t0):.6f}s")
        return edges

    # KD-дерево + kNN
    k = ceil(2.0 * requested_edges * safety_factor / n)
    k = max(10, min(k, n - 1))
    logging.info(f"Using KD-tree neighbor search: n={n}, k={k}")

    indexed_points = [(pt, idx) for idx, pt in enumerate(points)]
    tree = build_kdtree(indexed_points)

    edges_set = set()
    t0 = time.perf_counter()
    for i, point in enumerate(points):
        neighbors_heap: List[Tuple[int, int]] = []
        k_nearest_neighbors(tree, point, k, neighbors_heap)
        for neg_d, j in neighbors_heap:
            if i == j:
                continue
            a, b = (i, j) if i < j else (j, i)
            edges_set.add((-neg_d, a, b))
    logging.info(f"KD-tree edges gathered: {len(edges_set)} in {(time.perf_counter() - t0):.6f}s")
    return list(edges_set)


# ==============================
# ========= Tasks ==============
# ==============================

def largest_components_product(points: List[Tuple[int, int, int]], edges: List[Tuple[int, int, int]], merges: int = 1000) -> int:
    """
    Task 1:
    - З'єднує перші merges рёбер по зростанню distance
    - Повертає добуток розмірів трьох найбільших компонентів
    Складність:
        - Сортування: O(E log E)
        - Об'єднання merges рёбер: O(merges * α(n))
        - Підрахунок компонентів: O(n)
        - Разом: O(E log E)
    """
    dsu = DisjointSet(len(points))
    edges_sorted = sorted(edges, key=lambda x: x[0])
    for _, a, b in edges_sorted[:merges]:
        dsu.union(a, b)

    sizes = sorted(dsu.get_component_sizes(), reverse=True)
    while len(sizes) < 3:
        sizes.append(1)
    return sizes[0] * sizes[1] * sizes[2]


def final_merge_x_product(points: List[Tuple[int, int, int]], edges: List[Tuple[int, int, int]]) -> int:
    """
    Task 2:
    - Продовжує об'єднувати рёбра по зростанню distance
    - Поки не залишиться одна компонента
    - Повертає добуток X-координат останньої з'єднаної пари
    Складність:
        - Сортування: O(E log E)
        - Об'єднання всіх рёбер: O(E α(n))
    """
    dsu = DisjointSet(len(points))
    edges_sorted = sorted(edges, key=lambda x: x[0])
    last_pair = None
    for _, a, b in edges_sorted:
        if dsu.union(a, b):
            last_pair = (a, b)
            if dsu.components == 1:
                break
    if last_pair is None:
        raise RuntimeError("No merges performed — check edges generation.")
    return points[last_pair[0]][0] * points[last_pair[1]][0]


# ==============================
# ========= Main ===============
# ==============================

def main():
    points = read_points(Path("2025/day8/input.txt"))
    if not points:
        logging.info("No data to process.")
        return

    t_start = time.perf_counter()
    candidate_edges = build_candidate_edges(points, requested_edges=1000, safety_factor=2.0)
    logging.info(f"Candidate edges total: {len(candidate_edges)} (build time {time.perf_counter() - t_start:.6f}s)")

    t0 = time.perf_counter()
    ans1 = largest_components_product(points, candidate_edges, merges=1000)
    logging.info(f"\nTask 1: {ans1}\t\t(time: {time.perf_counter() - t0:.6f}s)")

    t0 = time.perf_counter()
    ans2 = final_merge_x_product(points, candidate_edges)
    logging.info(f"Task 2: {ans2}\t(time: {time.perf_counter() - t0:.6f}s)")


if __name__ == "__main__":
    main()
