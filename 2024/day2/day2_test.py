import unittest
from unittest.mock import patch
import script

class TestDay2(unittest.TestCase):

    file_path = '2024/day2/input.txt'

    text_input = """7 6 4 2 1
                    1 2 7 8 9
                    9 7 6 2 1
                    1 3 2 4 5
                    8 6 4 4 1
                    1 3 6 7 9"""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task1_with_example_data(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 2)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 4)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 369)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 428)

if __name__ == '__main__':
    unittest.main()