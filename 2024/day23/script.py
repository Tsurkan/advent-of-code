import timeit

def read_graph(file_path):
    """
    Читає граф з вхідного файлу.
    :param file_path: Шлях до файлу з описом графа.
    :return: Граф у вигляді словника, де ключі — це вузли, а значення — множини сусідів.
    """
    with open(file_path) as file:
        edges = [line.strip().split("-") for line in file.readlines()]

    graph = {}
    for edge in edges:
        # Додаємо ребра до графа, забезпечуючи двосторонній зв'язок.
        graph.setdefault(edge[0], set()).add(edge[1])
        graph.setdefault(edge[1], set()).add(edge[0])

    return graph

# Складність у гіршому випадку: O(n**3), де n — кількість вузлів.
# Більш ефективний алгоритм, алгоритм Еджері, має складність O(m**3/2) для розріджених графів,
# але у мене час на виконання стає більшим, тому залишився на цьому.
def count_triangle_subgraphs_with_t(graph):
    """
    Рахує кількість трикутних підграфів, що містять хоча б один вузол, ім'я якого починається з 't'.
    :param graph: Вхідний граф у вигляді словника.
    :return: Кількість трикутних підграфів.
    """
    triangle_count = 0
    visited = set()

    for node in graph:
        neighbors = list(graph[node])
        for i in range(len(neighbors)):
            for j in range(i + 1, len(neighbors)):
                # Перевіряємо, чи є ребро між сусідами.
                if neighbors[j] in graph[neighbors[i]]:
                    triangle = frozenset([node, neighbors[i], neighbors[j]])
                    if triangle not in visited:
                        visited.add(triangle)
                        # Перевіряємо, чи є вузол, ім'я якого починається з 't'.
                        if any(v.startswith("t") for v in triangle):
                            triangle_count += 1
    return triangle_count

# Складність у гіршому випадку O(3**n/3), де n — кількість вузлів.
def find_largest_fully_connected_subgraph(graph):
    """
    Знаходить найбільший повністю зв'язний підграф (кліку) у графі.
    Використовує оптимізований алгоритм Брона-Кербоша з півотуванням.
    Алгоритм Брона-Кербоша є одним із найефективніших для пошуку клік у розріджених графах. 
    :param graph: Вхідний граф у вигляді словника.
    :return: Найбільша кліка у вигляді відсортованого рядка вузлів.
    """
    def bron_kerbosch_with_pivot(r, p, x):
        """
        Рекурсивний метод для пошуку за алгоритмом Брона-Кербоша.
        :param r: Поточний вузол.
        :param p: Кандидати для розширення.
        :param x: Вузли, що вже виключені.
        """
        nonlocal max_clique
        if not p and not x:
            if len(r) > len(max_clique):
                max_clique = r
            return
        # Вибираємо півот-вузол з найбільшою кількістю сусідів.
        u = next(iter(p.union(x)))
        for v in list(p - graph[u]):
            bron_kerbosch_with_pivot(r.union([v]), p.intersection(graph[v]), x.intersection(graph[v]))
            p.remove(v)
            x.add(v)

    max_clique = set()
    nodes = set(graph.keys())
    bron_kerbosch_with_pivot(set(), nodes, set())
    return ",".join(sorted(max_clique))

def main(file_path="2024/day23/input.txt"):
    graph = read_graph(file_path)

    part1_result = count_triangle_subgraphs_with_t(graph)
    part2_result = find_largest_fully_connected_subgraph(graph)

    # print(f"Part 1 (ms): {timeit.timeit(lambda: count_triangle_subgraphs_with_t(graph), number=1) * 1000:.2f}")
    # print(f"Part 2 (ms): {timeit.timeit(lambda: find_largest_fully_connected_subgraph(graph), number=1) * 1000:.2f}")
    print(f"Part 1 result: {part1_result}") # 1200
    print(f"Part 2 result: {part2_result}") # ag,gh,hh,iv,jx,nq,oc,qm,rb,sm,vm,wu,zr

if __name__ == "__main__":
    main()
