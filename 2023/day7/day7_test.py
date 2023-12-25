import unittest
from unittest.mock import patch
import script

class TestDay7(unittest.TestCase):

    file_path = '2023/day7/input.txt'

    text_input = """32T3K 765
                    T55J5 684
                    KK677 28
                    KTJJT 220
                    QQQJA 483"""
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_read_input_file_with_example_data(self, mock_open):
        result = [['32T3K', '765'], ['T55J5', '684'], ['KK677', '28'], ['KTJJT', '220'], ['QQQJA', '483']]
        self.assertEqual(script.read_input_file('some_file_path'), result)
    
    def test_determine_hand_score_task2_with_example_data(self):
        self.assertEqual(script.determine_hand_score_task2([11, 12, 4, 11, 2]), 2)
        self.assertEqual(script.determine_hand_score_task2([4, 9, 9, 13, 9]), 6)
        self.assertEqual(script.determine_hand_score_task2([2, 2, 8, 7, 7]), 3)
        self.assertEqual(script.determine_hand_score_task2([2, 4, 13, 13, 4]), 6)
        self.assertEqual(script.determine_hand_score_task2([3, 3, 3, 13, 1]), 6)

    def test_determine_hand_score_task1_with_example_data(self):
        self.assertEqual(script.determine_hand_score_task1([12, 13, 5, 12, 2]), 2)
        self.assertEqual(script.determine_hand_score_task1([5, 10, 10, 4, 10]), 4)
        self.assertEqual(script.determine_hand_score_task1([2, 2, 9, 8, 8]), 3)
        self.assertEqual(script.determine_hand_score_task1([2, 5, 4, 4, 5]), 3)
        self.assertEqual(script.determine_hand_score_task1([3, 3, 3, 4, 1]), 4)
    
    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task_1_with_example_data(self, mock_open):
        self.assertEqual(script.task_1('some_file_path'), 6440)

    @patch('builtins.open', new_callable=unittest.mock.mock_open, read_data=text_input)
    def test_task_2_with_example_data(self, mock_open):
        self.assertEqual(script.task_2('some_file_path'), 5905)

    def test_part1_with_puzzle_input(self):
        self.assertEqual(script.task_1(self.file_path), 250453939)

    def test_part2_with_puzzle_input(self):
        self.assertEqual(script.task_2(self.file_path), 248652697)

if __name__ == '__main__':
    unittest.main()