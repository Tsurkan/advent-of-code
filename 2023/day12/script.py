# Функция для генерации всех возможных комбинаций символов из списка возможностей
# Используется рекурсивный подход
# Сложность: O(2^n), где n - общее количество символов в possibilities
def generate_combinations(possibilities, index, current, results):
    if index == len(possibilities):
        results.append(current)
        return

    for option in possibilities[index]:
        generate_combinations(possibilities, index + 1, current + option, results)

# Функция для подсчёта допустимых перестановок символов в соответствии с заданными условиями
# Сложность: O(n * 2^m), где n - количество символов, m - максимальное количество ? в строке
def count_permutations(symbols):
    results = set()

    for symbol, counts in symbols:

        # Создание списка возможностей для каждого символа
        possibilities = [['#', '.'] if s == '?' else [s] for s in symbol]

        generated_combinations = []
        generate_combinations(possibilities, 0, '', generated_combinations)

        for candidate in generated_combinations:
            count = 0
            positions = []
            for char in candidate:
                if char == '#':
                    count += 1
                else:
                    if count > 0:
                        positions.append(count)
                    count = 0
            if count > 0:
                positions.append(count)

            if positions == counts:
                results.add(candidate)

    return len(results)

cache = {} # Инициализация словаря кэша для мемоизации

# Рекурсивная функция для подсчета перестановок с использованием мемоизации
def count_permutations_2(symbols, counts, group_loc = 0):
    key = (tuple(symbols), tuple(counts), group_loc)

    # Проверка наличия результата в кэше, возвращаем его, если найден
    if key in cache:
        return cache[key]

    # Базовый случай: если символы закончились, проверяем условия и возвращаем результат
    if not symbols:
        result = not counts and not group_loc
        cache[key] = result
        return result

    results = 0
    possibilities = ['.', '#'] if symbols[0] == '?' else symbols[0]
    for p in possibilities:
        if p == '#':
            results += count_permutations_2(symbols[1:], counts, group_loc + 1)
        else:
            if group_loc > 0 and counts and counts[0] == group_loc:
                results += count_permutations_2(symbols[1:], counts[1:])
            elif group_loc == 0:
                results += count_permutations_2(symbols[1:], counts)

    cache[key] = results
    return results

def task_1(file_path):
    with open(file_path, 'r') as file:
        lines = [x.split() for x in file.read().splitlines()]

    # Формирование списка всех значений из содержимого файла
    springs = [[x[0], list(map(int, x[1].split(',')))] for x in lines]
    return sum([count_permutations([s]) for s in springs])

def task_2(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

    springs_data = [line.split() for line in content.strip().split('\n')]
    springs_data = [(symbol, tuple(map(int, count.split(',')))) for symbol, count in springs_data]
    springs_data = [('?'.join([symbol] * 5) + '.', count * 5) for symbol, count in springs_data]

    # Вычислить сумму для каждого результата функции
    return sum([count_permutations_2(symbol, count) for symbol, count in springs_data])


# Main function
def main():
    file_path = '2023/day12/input.txt'
    print('Part one:', task_1(file_path)) # 7344
    print('Part two:', task_2(file_path)) # 1088006519007

if __name__ == "__main__":
    main()