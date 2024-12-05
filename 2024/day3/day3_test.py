import unittest
from unittest.mock import patch
import script

class TestDay3(unittest.TestCase):

    file_path = '2024/day3/input.txt'

    text_input_1 = """xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))"""
    text_input_2 = """xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)un,do()?mul(8,5))"""

    with open(file_path, 'r') as f:
        data = f.read()

    def test_task1_with_example_data(self):
        self.assertEqual(script.task_1(self.text_input_1), 161)

    def test_task2_with_example_data(self):
        self.assertEqual(script.task_2(self.text_input_2), 48)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.data), 174561379)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.data), 106921067)

if __name__ == '__main__':
    unittest.main()