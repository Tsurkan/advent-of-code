def read_input(file_path):
    """
    Функція для читання даних з файлу.
    """
    with open(file_path) as file:
        return file.read().split("\n\n")

def no_common_hashes(str1, str2):
    """
    Функція перевіряє, чи два рядки не мають символу '#' на однакових позиціях.
    Параметри:
    str1 (str): Перший рядок.
    str2 (str): Другий рядок.
    Повертає:
    bool: True, якщо немає спільних символів '#', інакше False.
    """
    return all(x != '#' or y != '#' for x, y in zip(str1, str2))

def count_valid_pairs(input_data):
    """
    Функція для підрахунку кількості валідних пар рядків з масиву,
    де кожна пара не має символу '#' на однакових позиціях.
    Параметри:
    input_data (list): Список рядків для перевірки.
    Повертає:
    int: Кількість валідних пар.
    """
    valid_pairs_count = 0
    for i in range(len(input_data)):
        for j in range(i + 1, len(input_data)):
            if no_common_hashes(input_data[i], input_data[j]):
                valid_pairs_count += 1
    return valid_pairs_count

def main(file_path = '2024/day25/input.txt'):
    input_data = read_input(file_path)

    print("Part 1:", count_valid_pairs(input_data)) # 3133

if __name__ == "__main__":
    main()
