# Преобразуем каждый символ в число с помощью функции ord(), 
# затем выполняет операции умножения, сложения и взятия остатка, 
# чтобы сгенерировать число от 0 до 255 включительно.
# O(n), где n - длина входной строки
def hash_text(text):
    r = 0
    for char in text:
        r += ord(char)
        r *= 17
        r %= 256
    return r

# Разбиваем инструкции на два типа: которые содержат дефис ("-") и которые содержат знак равенства ("=").
# O(m), где m - количество инструкций.
def parsing_step(file_content):
    boxes = {}

    for step in file_content:
        if "-" in step:
            label = step.split("-")[0]
            box = hash_text(label)
            if box in boxes:
                boxes[box] = [(box_label, focal) for box_label, focal in boxes[box] if box_label != label]
        else:
            label, focal = step.split("=")
            focal = int(focal)
            box = hash_text(label)
            if box in boxes:
                found = False
                for i, (box_label, _) in enumerate(boxes[box]):
                    if box_label == label:
                        boxes[box][i] = (box_label, focal)
                        found = True
                        break
                if not found:
                    boxes[box].append((label, focal))
            else:
                boxes[box] = [(label, focal)]

    return boxes

def task_1(file_path):
    with open(file_path) as file:
        steps = file.read().split(",")

    return sum(hash_text(step) for step in steps)

def task_2(file_path):
    with open(file_path, "r") as file:
        file_content = file.read().split(",")

    boxes = parsing_step(file_content)
    return sum((box + 1) * (lens + 1) * focal for box in range(256) if box in boxes for lens, (_, focal) in enumerate(boxes[box]))


# Main function
def main():
    file_path = '2023/day15/input.txt'
    print('Part one:', task_1(file_path)) # 517315
    print('Part two:', task_2(file_path)) # 247763

if __name__ == "__main__":
    main()