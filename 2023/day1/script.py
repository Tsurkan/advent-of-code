def part_One(file_path):
    with open(file_path) as f:
        total_sum = 0
        for line in f:
            numbers = ''.join(c for c in line if c.isdigit())
            if numbers:  # Check if any digits were found
                total_sum += int(numbers[0] + numbers[-1])
                
    return total_sum

def part_Two(file_path):
    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']

    with open(file_path) as f:
        total_sum = 0
        for line in f:
            line_digits = ''
            for t in range(len(line)):
                for i in range(len(digits)):
                    if line[t:].startswith(digits[i]):
                        line_digits += str(i+1)
                    elif line[t].isdigit():
                        line_digits += line[t]
            if line_digits: # Check if any digits were found
                total_sum += int(line_digits[0] + line_digits[-1])

        return total_sum

def main():
    print('Part one:', part_One('day1/input1.txt')) # 56042
    print('Part two:', part_Two('day1/input2.txt')) # 55358

if __name__ == "__main__":
    main()