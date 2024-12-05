import unittest
from unittest.mock import patch
import script

class TestDay1(unittest.TestCase):

    file_path = '2024/day1/input.txt'

    text_input = """3   4
                    4   3
                    2   5
                    1   3
                    3   9
                    3   3"""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task1_with_example_data(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 11)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 31)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 1941353)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 22539317)

if __name__ == '__main__':
    unittest.main()