# Function to extract digits and compute a value based on the first and last digits found
def task1(line):
    numbers = ''.join(c for c in line if c.isdigit()) # Find all digits in the line
    if numbers:
        return int(numbers[0] + numbers[-1]) # Sum the first and last digits and return their sum
    return 0  # Return 0 if no digits are found

# Function to convert textual representations of numbers to digits and compute a value based on the first and last digits found
# (eightwothree = 823)
def task2(line):
    digits = ['one', 'two', 'three', 'four', 'five', 'six', 'seven', 'eight', 'nine']
        
    line_digits = '' # Initialize an empty string to store converted digits
    for t in range(len(line)):
        for i in range(len(digits)):

            # If the word represents a number, convert it to its digit equivalent
            if line[t:].startswith(digits[i]):
                line_digits += str(i+1)

            # If the character is already a digit, append it directly
            elif line[t].isdigit():
                line_digits += line[t]
    
    if line_digits:
        return int(line_digits[0] + line_digits[-1]) # Sum the first and last digits and return their sum
    return 0  # Return 0 if no digits are found

# Function to process the file based on the specified mode ('task1' or 'task2')
def process_file(file_path, mode):
    total_sum = 0

    # Determine the appropriate processing function based on the mode
    process_func = task1 if mode == 'task1' else task2

    # Open the file and process each line
    with open(file_path) as f:
        for line in f:
            total_sum += process_func(line) # Add the computed value to the total sum

    return total_sum

def main():
    print('Part one:', process_file('2023/day1/input1.txt', 'task1')) # 56042
    print('Part two:', process_file('2023/day1/input2.txt', 'task2')) # 55358

if __name__ == "__main__":
    main()