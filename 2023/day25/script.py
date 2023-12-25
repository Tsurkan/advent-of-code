import networkx as nx

# Эта функция читает файл с данными о графе и создает ориентированный граф с помощью библиотеки NetworkX.
# O(V + E), где V - количество узлов, E - количество ребер в графе.
def read_graph(file_path):
    with open(file_path) as file:
        lines = file.read().strip().split('\n')

    # Построение ориентированного графа с помощью NetworkX
    network_graph = nx.DiGraph()
    for line in lines:
        node, edges = line.split(':')
        edges = edges.split()

        # Добавляем одни и те же ребра, но в разных направлениях.
        network_graph.add_edges_from((node, edge, {'capacity': 1.0}) for edge in edges)
        network_graph.add_edges_from((edge, node, {'capacity': 1.0}) for edge in edges)
    
    return network_graph

# Эта функция ищет минимальный разрез в графе с заданным значением разреза (в данном случае - 3).
# Для решения задачи минимального разреза (minimum_cut) NetworkX использует алгоритм Каргера ("Karger's algorithm") или его вариации.
# идея заключается в многократном случайном удалении рёбер из графа до тех пор, пока не будет достигнуто минимальное значение разреза.
# O(V^3), где V - количество узлов в графе (из-за вложенных циклов).
def find_desired_cut(graph):
    for start_node in graph.nodes():
        for end_node in graph.nodes():
            if start_node != end_node:
                cut_value, partitions = nx.minimum_cut(graph, start_node, end_node)
                if cut_value == 3:
                    left_partition, right_partition = partitions
                    return len(left_partition) * len(right_partition)
    return None

def task_1(file_path):
    network_graph = read_graph(file_path)
    return find_desired_cut(network_graph)

def task_2(file_path):
    pass

# Main function
def main():
    file_path = '2023/day25/input.txt'
    print('Part one:', task_1(file_path)) # 619225

if __name__ == "__main__":
    main()