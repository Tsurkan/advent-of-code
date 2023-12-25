import unittest
from unittest.mock import patch
import script

class TestDay9(unittest.TestCase):

    file_path = '2023/day9/input.txt'

    text_input = """0 3 6 9 12 15
                    1 3 6 10 15 21
                    10 13 16 21 30 45"""

    def test_get_final_sum_task_1_with_example_data(self):
        self.assertEqual(script.get_final_sum_task_1([0, 3, 6, 9, 12, 15]), 18)
        self.assertEqual(script.get_final_sum_task_1([1, 3, 6, 10, 15, 21]), 28)
        self.assertEqual(script.get_final_sum_task_1([10, 13, 16, 21, 30, 45]), 68)

    def test_get_final_sum_task_2_with_example_data(self):
        self.assertEqual(script.get_final_sum_task_2([0, 3, 6, 9, 12, 15]), -3)
        self.assertEqual(script.get_final_sum_task_2([1, 3, 6, 10, 15, 21]), 0)
        self.assertEqual(script.get_final_sum_task_2([10, 13, 16, 21, 30, 45]), 5)
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task_1_with_example_data(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 114)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task_2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 2)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 1762065988)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 1066)

if __name__ == '__main__':
    unittest.main()