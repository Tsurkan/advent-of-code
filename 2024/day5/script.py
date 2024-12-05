def read_input_file(filename):
    """
    Зчитує правила та оновлення зі вхідного файлу.
    :param filename: Назва вхідного файлу.
    :return: Кортеж (rules, updates) - список правил і оновлень.
    """
    with open(filename, 'r') as file:
        lines = file.read().strip().split('\n')

    # Розділяємо правила та оновлення
    rules = []
    updates = []
    is_updating = False

    for line in lines:
        if not line.strip():
            is_updating = True
            continue
        if not is_updating:
            rules.append(tuple(map(int, line.split('|'))))
        else:
            updates.append(list(map(int, line.split(','))))

    return rules, updates


def is_correct_order(update, rules):
    """
    Перевіряє, чи оновлення дотримується заданих правил порядку.
    :param update: Список сторінок в оновленні.
    :param rules: Список правил у вигляді кортежів (before, after).
    :return: True, якщо порядок правильний, інакше False.
    """
    # Індексуємо сторінки для швидкого пошуку порядку
    page_index = {page: i for i, page in enumerate(update)}
    for before, after in rules:
        if before in page_index and after in page_index:
            if page_index[before] > page_index[after]:
                return False
    return True


def find_middle_page(update):
    """
    Знаходить середню сторінку в оновленні.
    :param update: Список сторінок в оновленні.
    :return: Номер середньої сторінки.
    """
    mid_index = len(update) // 2
    return update[mid_index]


def topological_sort(pages, rules):
    """
    Сортує сторінки за допомогою топологічного сортування відповідно до заданих правил.
    Топологічне сортування використовується для впорядкування вузлів у DAG 
    (орієнтованому ациклічному графі), щоб для кожного ребра uv вузол u 
    був перед вузлом v у впорядкуванні.

    Складність:
    - Побудова графа: O(E), де E - кількість правил.
    - Топологічне сортування: O(V + E), де V - кількість сторінок (вузлів).

    :param pages: Список сторінок для сортування.
    :param rules: Список правил у вигляді кортежів (before, after).
    :return: Відсортований список сторінок.
    """
    # Побудова графа та підрахунок вхідних ступенів
    graph = {page: [] for page in pages}
    indegree = {page: 0 for page in pages}

    for before, after in rules:
        if before in pages and after in pages:
            graph[before].append(after)
            indegree[after] += 1

    # Топологічне сортування за алгоритмом Кана
    queue = [page for page in pages if indegree[page] == 0]
    sorted_pages = []

    while queue:
        current = queue.pop(0)  # FIFO: видаляємо перший елемент
        sorted_pages.append(current)
        for neighbor in graph[current]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return sorted_pages


def task_1(rules, updates):
    correct_updates = []
    for update in updates:
        if is_correct_order(update, rules):
            correct_updates.append(update)

    return sum([find_middle_page(update) for update in correct_updates])


def task_2(rules, updates):
    # incorrect_updates = []
    corrected_middle_pages = []

    for update in updates:
        if not is_correct_order(update, rules):
            # incorrect_updates.append(update)
            sorted_update = topological_sort(update, rules)
            corrected_middle_pages.append(find_middle_page(sorted_update))

    return sum(corrected_middle_pages)


def main(file_path='2024/day5/input.txt'):
    rules, updates = read_input_file(file_path)

    print('Part one:', task_1(rules, updates))  # 5651
    print('Part two:', task_2(rules, updates))  # 4743


if __name__ == "__main__":
    main()
