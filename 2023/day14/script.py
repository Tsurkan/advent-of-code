# Транспонирование, сортировка, поворот имеют сложность O(N*M), где N - количество строк, M - количество столбов
# Функция для транспонирования матрицы (меняет строки и столбцы местами).
def transpose(matrix):
    return list(map("".join, zip(*matrix)))

# Функция для поворота матрицы
def rotate(reflector):
    return tuple(row[::-1] for row in reflector)

# Функция для сортировки элементов в строках матрицы
def sort(reflector):
    return ['#'.join(''.join(sorted(group, reverse=True)) for group in row.split('#')) for row in transpose(reflector)]

# Функция повторяющяя поворот и сортировку
def spin_cycle(reflector):
    for _ in range(4):
        reflector = rotate(sort(reflector))
    return reflector

def task_1(file_path):

    # читаем строки из файла и формируем из них матрицу
    with open('2023/day14/input.txt') as file:
        reflector = [line.strip() for line in file]
    
    # Транспонируем матрицу.
    # Сортирует символы в каждой группе, разделенной '#', в обратном порядке
    # Транспонирует матрицу обратно
    reflector = [''.join(row) for row in zip(*sort(reflector))]

    # Подсчитывает количество символов 'O' в преобразованной матрице
    # Каждая строка имеет вес, который увеличивается с увеличением индекса строки (снизу вверх).
    # Количество 'O' в каждой строке умножается на её вес, и эти значения суммируются.
    # O(N*M), где N - количество строк, M - количество 
    return sum(row.count("O") * (i + 1) for i, row in enumerate(reversed(reflector)))

def task_2(file_path):
    with open('2023/day14/input.txt') as file:
        reflector = tuple(line.strip() for line in file)

    # Словарь для отслеживания уже просмотренных сеток и список индексов
    seen = {}
    indexes = []

    # Продолжаем повороты и сортировки пока не обнаружим повторяющуюся матрицу
    while reflector not in seen:
        seen[reflector] = len(indexes)
        indexes.append(reflector)
        reflector = spin_cycle(reflector)

    # Находим индекс первого вхождения текущей сетки
    first = seen[reflector]

    # Вычисляем, сколько циклов нужно пропустить, чтобы достичь миллиарда повторений
    # Находим конечную сетку после выполнения всех циклов
    reflector = indexes[(1000000000 - first) % (len(indexes) - first) + first]
        
    # Подсчитывает количество символов 'O' в матрице
    return sum((i + 1) * row.count('O') for i, row in enumerate(reversed(reflector)))

# Main function
def main():
    file_path = '2023/day14/input.txt'
    print('Part one:', task_1(file_path)) # 113424
    print('Part two:', task_2(file_path)) # 96003

if __name__ == "__main__":
    main()