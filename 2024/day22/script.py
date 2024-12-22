def transform_number(number):
    """Преобразує число за допомогою заданих математичних операцій."""
    number = ((number * 64) ^ number) % 16777216
    number = ((number // 32) ^ number) % 16777216
    number = ((number * 2048) ^ number) % 16777216
    return number

def initialize(current_number):
    """Ініціалізує перших 4 ітерацій."""
    sliding = 0
    for _ in range(4):
        next_number = transform_number(current_number)
        sliding = sliding * 20 + (next_number % 10) - (current_number % 10)
        current_number = next_number
    return current_number, sliding

def process(sliding, current_number, sums, current_seen):
    """Оновлююмо суми в словнику та перевіряючи унікальність."""
    if sliding not in current_seen:
        if sliding not in sums:
            sums[sliding] = 0
        sums[sliding] += current_number % 10
        current_seen.add(sliding)
    return sums, current_seen

def update_window(sliding, current_number):
    """Оновлює значення для наступної ітерації."""
    next_number = transform_number(current_number)
    sliding = (sliding * 20 + (next_number % 10) - (current_number % 10)) % (20 ** 4)
    return sliding, next_number

def process_file(file_path):
    """Основний процес обробки даних з файлу."""
    total_sum = 0  # Загальна сума
    sums = {}  # Словник для зберігання сум
    
    with open(file_path, 'r') as file:
        for line in file:
            current_number = int(line)
            current_number, sliding = initialize(current_number)
            current_seen = set()  # Множина для відстеження вже побачених чисел
            
            for i in range(1997):  # Проходимо по 1997 ітераціям, бо перші 4 вже порахували
                if i == 1996:
                    total_sum += current_number
                
                # Оновлюємо суми і перевіряємо унікальність
                sums, current_seen = process(sliding, current_number, sums, current_seen)
                
                # Оновлюємося для наступної ітерації
                sliding, current_number = update_window(sliding, current_number)

    return total_sum, max(sums.values(), default=0)

def main(file_path = '2024/day22/input.txt'):
    total_sum, max_window_sum = process_file(file_path)  

    print(f"Part 1: {total_sum}")       # 17612566393
    print(f"Part 2: {max_window_sum}")  # 1968

if __name__ == "__main__":
    main()
