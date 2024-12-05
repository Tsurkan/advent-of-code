import unittest
from unittest.mock import patch
import script

class TestDay4(unittest.TestCase):

    file_path = '2024/day4/input.txt'

    text_input = """MMMSXXMASM
                    MSAMXMSMSA
                    AMXSXMAAMM
                    MSAMASMSMX
                    XMASAMXAMM
                    XXAMMXXAMA
                    SMSMSASXSS
                    SAXAMASAAA
                    MAMMMXMMMM
                    MXMXAXMASX"""

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task1_with_example_data(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 18)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 9)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 2521)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 1912)

if __name__ == '__main__':
    unittest.main()