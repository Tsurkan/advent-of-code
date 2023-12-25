import unittest
from unittest.mock import patch
import script

class TestDay3(unittest.TestCase):

    file_path = '2023/day3/input.txt'

    text_input = """467..114..
                    ...*......
                    ..35..633.
                    ......#...
                    617*......
                    .....+.58.
                    ..592.....
                    ......755.
                    ...$.*....
                    .664.598.."""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task1_with_example_data(self, mock_open):
        self.assertEqual(script.task1('some_file_path'), 4361)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task2_with_example_data(self, mock_open):
        self.assertEqual(script.task2('some_file_path'), 467835)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task1(self.file_path), 527369)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task2(self.file_path), 73074886)

if __name__ == '__main__':
    unittest.main()