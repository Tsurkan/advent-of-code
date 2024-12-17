# Функція для руху в певному напрямку
def move(p, d, grid):
    p += d  # Зміщуємо позицію
    # Перевіряємо різні умови для руху в межах сітки
    if all([ 
        grid[p] != '[' or move(p+1, d, grid) and move(p, d, grid),
        grid[p] != ']' or move(p-1, d, grid) and move(p, d, grid),
        grid[p] != 'O' or move(p, d, grid), grid[p] != '#']) :
            grid[p], grid[p-d] = grid[p-d], grid[p]
            return True

def task(grid, moves):
    # Створюємо словник для представлення сітки, де ключі — координати
    grid = {i+j*1j:c for j,r in enumerate(grid.split()) 
                     for i,c in enumerate(r)}

    # Знаходимо початкову позицію позначену '@'
    pos, = (p for p in grid if grid[p] == '@')

    for m in moves.replace('\n', ''):
        # Визначаємо напрямок руху
        dir = {'<':-1, '>':+1, '^':-1j, 'v':+1j}[m]
        copy = grid.copy()

        if move(pos, dir, grid): pos += dir
        else: grid = copy  # Якщо рух неможливий, сітка залишається без змін

    ans = sum(pos for pos in grid if grid[pos] in 'O[')
    return int(ans.real + ans.imag*100)


def main(file_path='2024/day15/input.txt'):
    grid, moves = open(file_path).read().split('\n\n')

    print('Part 1:', task(grid, moves))  # 1430439

    # Збільшуэмо карту подвоюючи кожний едемент на карті
    grid = grid.translate(str.maketrans({'#':'##', '.':'..', 'O':'[]', '@':'@.'}))
    
    print('Part 2:', task(grid, moves))  # 1458740

if __name__ == "__main__":
    main()
