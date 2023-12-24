import unittest
import script

class TestDay1(unittest.TestCase):

    def test_part1_with_test_example(self):
        self.assertEqual(script.task1("1abc2"), 12)
        self.assertEqual(script.task1("pqr3stu8vwx"), 38)
        self.assertEqual(script.task1("a1b2c3d4e5f"), 15)
        self.assertEqual(script.task1("treb7uchet"), 77)

    def test_part1_with_my_test(self):
        self.assertEqual(script.task1("99ldffbjq"), 99)
        self.assertEqual(script.task1("q7cndbhsf"), 77)
        self.assertEqual(script.task1("lkdsffjd5"), 55)
        self.assertEqual(script.task1("3lqrzdq16"), 36)
        self.assertEqual(script.task1("plt468652"), 42)

    def test_part1_with_puzzle_input(self):
        file_path = '2023/day1/input1.txt'
        self.assertEqual(script.process_file(file_path, 'task1'), 56042)
    
    def test_part2_with_test_example(self):
        self.assertEqual(script.task2("two1nine"), 29)
        self.assertEqual(script.task2("eightwothree"), 83)
        self.assertEqual(script.task2("abcone2threexyz"), 13)
        self.assertEqual(script.task2("xtwone3four"), 24)
        self.assertEqual(script.task2("4nineeightseven2"), 42)
        self.assertEqual(script.task2("zoneight234"), 14)
        self.assertEqual(script.task2("7pqrstsixteen"), 76)

    def test_part2_with_my_test(self):
        pass
    
    def test_part2_with_puzzle_input(self):
        file_path = '2023/day1/input2.txt'
        self.assertEqual(script.process_file(file_path, 'task2'), 55358)

if __name__ == '__main__':
    unittest.main()