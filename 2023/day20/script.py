from math import gcd
from collections import deque

# Функция вычисления НОК (наименьшего общего кратного) списка чисел.
# O(n*log(max(числа))) - где n - количество чисел в списке.
def lcm(numbers):
    result = 1
    for num in numbers:
        result = (result * num) // gcd(num, result)
    return result

# Функция подгонки сигнала с учетом типов входных сигналов.
def adjust(signal, input_types):
    if signal in input_types:
        return input_types[signal] + signal
    return signal

# Инициализация сигналов и узлов на основе входных данных.
def initialize(input_data):
    wiring = {}
    input_types = {}
    for line in input_data:
        src, dest = line.split('->')
        src = src.strip()
        dest = dest.strip().split(', ')
        wiring[src] = dest
        input_types[src[1:]] = src[0]
    return wiring, input_types

# Создание связей для входов и выходов на основе инициализированных данных.
def create_mappings(wiring, input_types):
    input_connections = {}
    input_inverse = {}
    for node, signals in wiring.items():
        wiring[node] = [adjust(signal, input_types) for signal in signals]
        for signal in wiring[node]:
            if signal[0] == '&':
                if signal not in input_connections:
                    input_connections[signal] = {}
                input_connections[signal][node] = 'lo'
            if signal not in input_inverse:
                input_inverse[signal] = []
            input_inverse[signal].append(node)
    return wiring, input_connections, input_inverse

# Симуляция работы цепи. Используем поиск в ширину (BFS).
def simulate_circuit(wiring, input_connections, input_inverse, watching, pushing_quantity):
    
    # Инициализация переменных и структур данных
    low_signal = 0
    high_signal = 0
    queue = deque()
    activated_nodes = set()
    previous_count = {}
    signal_count = {}
    to_lcm = []

    # Симуляция работы цепи на протяжении множества итераций
    for time in range(1, pushing_quantity + 1):
        queue.append(('broadcaster', 'button', 'lo'))

        while queue:
            node, from_node, signal_type = queue.popleft()

            if node not in signal_count:
                signal_count[node] = 0

            if signal_type == 'lo':
                if node in previous_count and signal_count[node] == 2 and node in watching:
                    to_lcm.append(time - previous_count[node])
                previous_count[node] = time
                signal_count[node] += 1

            if len(to_lcm) == len(watching): # task 2
                return lcm(to_lcm) 

            if signal_type == 'lo':
                low_signal += 1
            else:
                high_signal += 1

            if node not in wiring:
                continue

            if node == 'broadcaster':
                for signal in wiring[node]:
                    queue.append((signal, node, signal_type))
            elif node[0] == '%':
                if signal_type == 'hi':
                    continue
                else:
                    if node not in activated_nodes:
                        activated_nodes.add(node)
                        new_signal_type = 'hi'
                    else:
                        activated_nodes.discard(node)
                        new_signal_type = 'lo'
                    for signal in wiring[node]:
                        queue.append((signal, node, new_signal_type))
            elif node[0] == '&':
                if node not in input_connections:
                    input_connections[node] = {}
                input_connections[node][from_node] = signal_type
                new_signal_type = 'lo' if all(s == 'hi' for s in input_connections[node].values()) else 'hi'
                for signal in wiring[node]:
                    queue.append((signal, node, new_signal_type))

        # if time == 1000: # task 1
    return low_signal * high_signal

def task_1(file_path):
    with open('2023/day20/input.txt') as file:
        input_data = file.read().strip().split('\n')
    
    # Инициализация
    wiring, input_types = initialize(input_data)
    wiring, input_connections, input_inverse = create_mappings(wiring, input_types)

    # Определение переменной watching. Можно взять любое значение. Я беру первое и к нему будем идти.
    watching = list(input_inverse.keys())[0]

    # Симуляция работы цепи. По условию нажать кнопку 1000 раз
    return simulate_circuit(wiring, input_connections, input_inverse, watching, 1000) 

def task_2(file_path):
    # Чтение входных данных
    with open('2023/day20/input.txt') as file:
        input_data = file.read().strip().split('\n')

    # Инициализация
    wiring, input_types = initialize(input_data)
    wiring, input_connections, input_inverse = create_mappings(wiring, input_types)
    
    # Определение переменной watching. По условию нужно дойти до модуля rx.
    watching = input_inverse[input_inverse['rx'][0]]

    # Симуляция работы цепи. После 100_000 повторений ответ не меняется, значит дошли.
    return simulate_circuit(wiring, input_connections, input_inverse, watching, 10**5)

# Main function
def main():
    file_path = '2023/day20/input.txt'
    print('Part one:', task_1(file_path)) # 680278040
    print('Part two:', task_2(file_path)) # 243548140870057

if __name__ == "__main__":
    main()