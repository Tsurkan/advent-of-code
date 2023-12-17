# s, t = open("2023/day10/input.txt").read().splitlines(), dict(zip("|-LJ7FS.", (16644, 1344, 1284, 324, 16704, 17664, 17988, 0)))
# g, n = [(t[c] >> i+j) & 3 for r in s for i in (0, 6, 12) for c in r for j in (0, 2, 4)], 3*len(s); import operator as o
# def f(s, v=0): return len([o.setitem(g, p, s.append(p) or 2) for q in s for p in (q-n, q+n, q+1, q-1) if v <= g[p] < 2])
# print((f([g.index(2)], 1)-1)//6, f([0]) and n*n//9 - sum(g[n*i+1:n*i+n+1:3].count(2) for i in range(1, n, 3)))


# Чтение данных из файла input.txt
with open("2023/day10/input.txt") as file:
    s = file.read().splitlines()

# Создание словаря для типов труб и их кодирования
t = {
    '|': 16644, '-': 1344, 'L': 1284, 'J': 324,
    '7': 16704, 'F': 17664, 'S': 17988, '.': 0
}

# Создание сетки трубопроводов на основе данных из файла
g = []
for r in s:
    for i in (0, 6, 12):
        for c in r:
            for j in (0, 2, 4):
                # Выполняем операции с битами: сдвигаем вправо значение t[c] на i + j и выполняем побитовое И с 3
                result = (t[c] >> i + j) & 3
                g.append(result)


# Функция для определения количества закрытых плиток в трубопроводе
def f(s, v=0):
    return len([
        (g.__setitem__(p, s.append(p) or 2), 1)[1]
        for q in s for p in (q - n, q + n, q + 1, q - 1) if v <= g[p] < 2
    ])
    
# Выполнение функции f() и вывод результатов
n = 3 * len(s)  # Размер сетки
print((f([g.index(2)], 1) - 1) // 6, f([0]) and n * n // 9 - sum(g[n * i + 1:n * i + n + 1:3].count(2) for i in range(1, n, 3)))
