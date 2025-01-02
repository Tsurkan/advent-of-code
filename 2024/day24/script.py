# Складність: O(n*k), де n - кількість строчок у файлі, k - довжина рядка
def task_1(file_path):
    # Словник для зберігання динамічно створених лямбда-функцій (Мемоїзація)
    fun = {}

    # Відображення операторів до їх еквівалентів
    operator_map = {'XOR': '^', 'OR': '|', 'AND': '&'}

    # Зчитуємо та обробляємо кожен рядок файлу
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line: # Пропускаємо порожні рядки
                continue  
            
            # Парсимо рядок як бінарну операцію
            parts = line.split()
            if len(parts) == 5:
                var_a, operator, var_b, _, result_var = parts

                # Динамічно створюємо лямбда-функцію для результатної змінної
                fun[result_var] = ( lambda a=var_a, b=var_b, op=operator_map[operator]:
                                    lambda: eval(f"{fun[a]()} {op} {fun[b]()}"))()
            else:
                var_name, expression = line.split(':', 1)
                fun[var_name.strip()] = eval(f"lambda: {expression.strip()}", {}, fun)

    return sum(fun[f'z{i:02}']() << i for i in range(46))

# По суті cкладність: O(n**2), де n — число операцій із файлу
def task_2(file_path):
    # Зчитування логічних операцій із файлу
    logic_operations = [line.split() for line in open(file_path) if '->' in line]

    # O(k*m), де k — кількість перевірок, m — число операцій
    is_related_to = lambda candidate_var, target_var: any(
        target_var == operator and candidate_var in (input_a, input_b)
        for input_a, operator, input_b, _, _ in logic_operations
    )

    print(*sorted(
        output_var for input_a, operator, input_b, _, output_var in logic_operations if
        operator == "XOR" and all(d[0] not in 'xyz' for d in (input_a, input_b, output_var)) or
        operator == "AND" and "x00" not in (input_a, input_b) and is_related_to(output_var, 'XOR') or
        operator == "XOR" and "x00" not in (input_a, input_b) and is_related_to(output_var, 'OR') or
        operator != "XOR" and output_var[0] == 'z' and output_var != "z45"
    ), sep=',')


def main(file_path='2024/day24/input.txt'):
    print("Part 1:", task_1(file_path))             # 57270694330992
    print("Part 2:", end=' '), task_2(file_path)    # gwh,jct,rcb,wbw,wgb,z09,z21,z39


if __name__ == "__main__":
    main()
