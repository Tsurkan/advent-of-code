import unittest
from unittest.mock import patch
import script

class TestDay5(unittest.TestCase):

    file_path = '2024/day5/input.txt'
    
    rules =[(47, 53),
            (97, 13),
            (97, 61),
            (97, 47),
            (75, 29),
            (61, 13),
            (75, 53),
            (97, 29),
            (53, 29),
            (61, 53),
            (29, 13),
            (97, 53),
            (61, 29),
            (47, 13),
            (75, 47),
            (97, 75),
            (47, 61),
            (75, 61),
            (47, 29),
            (75, 13),
            (53, 13)]
    
    updates = [ [75, 47, 61, 53, 29],
                [97, 61, 53, 29, 13],
                [75, 29, 13],
                [75, 97, 47, 61, 53],
                [61, 13, 29],
                [97, 13, 75, 29, 47]]
        

    def test_task1_with_example_data(self ):
        self.assertEqual(script.task_1(self.rules, self.updates), 143)

    def test_task2_with_example_data(self):
        self.assertEqual(script.task_2(self.rules, self.updates), 123)

    def test_part1_with_puzzle_input(self):
        self.rules, self.updates = script.read_input_file(self.file_path)
        self.assertEqual(script.task_1(self.rules, self.updates), 5651)

    def test_part2_with_puzzle_input(self):
        self.rules, self.updates = script.read_input_file(self.file_path)
        self.assertEqual(script.task_2(self.rules, self.updates), 4743)

if __name__ == '__main__':
    unittest.main()