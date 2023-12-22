import re

# Функция рекурсивно вычисляет условия на основе заданных правил
# O(n), где n - количество шагов
def evaluate_condition(part, current_step, workflow):
    step_rules = workflow[current_step]
    x, m, a, s = part
    
    for rule in step_rules.split(","):
        if rule == "R":
            return False
        if rule == "A":
            return True
        
        split_rule = rule.split(":")

        # Если правило не имеет дополнительных шагов, вызвать рекурсивно evaluate_condition
        if len(split_rule) == 1:
            return evaluate_condition(part, rule, workflow)
        
        condition = split_rule[0]
        if eval(condition):
            action = split_rule[1]
            if action == "R":
                return False
            if action == "A":
                return True

            # Рекурсивно вызвать evaluate_condition для действия
            return evaluate_condition(part, action, workflow)

# Функция принимает символ (character), флаг is_greater для указания больше/меньше, значение (value) 
# и набор диапазонов (ranges). Она адаптирует диапазоны в соответствии с заданными параметрами.
# O(m * k), где m элементов, а каждый элемент имеет длину k.
def adjust_ranges(character, is_greater, value, ranges):
    character_index = 'xmas'.index(character)
    adjusted_ranges = []
    
    for rng in ranges:
        rng = list(rng)
        lo, hi = rng[character_index]
        
        if is_greater:
            lo = max(lo, value + 1)
        else:
            hi = min(hi, value - 1)
        
        if lo <= hi:
            rng[character_index] = (lo, hi)
            adjusted_ranges.append(tuple(rng))
    
    return adjusted_ranges

# Функция определяет диапазоны принятия (acceptance ranges) на основе правил (rules) и рабочего процесса (workflow).
# O(n), где n - количество шагов.
def determine_acceptance_ranges(rules, workflow):
    current_rule = rules[0]
    if current_rule == "R":
        return []
    if current_rule == "A":
        return [((1, 4000), (1, 4000), (1, 4000), (1, 4000))]
    
    current_rule_split = current_rule.split(":")
    if len(current_rule_split) == 1:
        return determine_acceptance_ranges(workflow[current_rule].split(","), workflow)

    condition = current_rule_split[0]
    is_greater = ">" in condition
    character = condition[0]
    value = int(condition[2:])
    inverted_value = value + 1 if is_greater else value - 1
    
    true_ranges = adjust_ranges(character, is_greater, value, determine_acceptance_ranges([current_rule_split[1]], workflow))
    false_ranges = adjust_ranges(character, not is_greater, inverted_value, determine_acceptance_ranges(rules[1:], workflow))
    
    return true_ranges + false_ranges

# Парсинг данных
def pars_data(file_path):
    with open(file_path) as file:
        workflow_description, parts_description = file.read().strip().split('\n\n')
    
    parts = [list(map(int, re.findall(r'\d+', line))) for line in parts_description.split("\n")]
    workflow = {line.split("{")[0]: line.split("{")[1][:-1] for line in workflow_description.split("\n")}
    return parts, workflow

def task_1(file_path):
    parts, workflow = pars_data(file_path)
    part_one_total = 0
    for part in parts:
        if evaluate_condition(part, 'in', workflow):
            part_one_total += sum(part)
    return part_one_total

def task_2(file_path):
    parts, workflow = pars_data(file_path)
    part_two_total = 0
    for rng in determine_acceptance_ranges(workflow['in'].split(","), workflow):
        total = 1
        for low, high in rng:
            total *= high - low + 1
        part_two_total += total
    return part_two_total

# Main function
def main():
    file_path = '2023/day19/input.txt'
    print('Part one:', task_1(file_path)) # 449531
    print('Part two:', task_2(file_path)) # 122756210763577

if __name__ == "__main__":
    main()