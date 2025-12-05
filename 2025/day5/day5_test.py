
import unittest

from script import (
    parse_ranges_and_ingredients,
    merge_ranges,
    is_fresh,
    count_fresh_ingredients,
    count_total_fresh_ids
)

class TestIngredientFreshness(unittest.TestCase):

    def test_parse_ranges_and_ingredients(self):
        """Тестуємо парсинг вхідних рядків."""
        lines = [
            "10-20",
            "30-40",
            "15",
            "35",
            "200-300",
            "99"
        ]
        fresh_ranges, ingredients = parse_ranges_and_ingredients(lines)

        self.assertEqual(fresh_ranges, [(10,20), (30,40), (200,300)])
        self.assertEqual(ingredients, [15, 35, 99])

    def test_merge_ranges_no_overlap(self):
        """Два діапазони, які не перетинаються."""
        data = [(1, 5), (10, 20)]
        self.assertEqual(merge_ranges(data), [(1, 5), (10, 20)])

    def test_merge_ranges_overlap(self):
        """Діапазони, що перетинаються."""
        data = [(1, 10), (5, 20)]
        self.assertEqual(merge_ranges(data), [(1, 20)])

    def test_merge_ranges_complex(self):
        """Перевірка більш складного випадку."""
        data = [(1, 5), (3, 7), (10, 12), (11, 50)]
        self.assertEqual(merge_ranges(data), [(1, 7), (10, 50)])

    def test_is_fresh_inside(self):
        """Перевірка інгредієнта, що входить у діапазон."""
        ranges = [(10, 20), (30, 40)]
        self.assertTrue(is_fresh(15, ranges))
        self.assertTrue(is_fresh(40, ranges))

    def test_is_fresh_outside(self):
        """Інгредієнт поза діапазонами."""
        ranges = [(10, 20), (30, 40)]
        self.assertFalse(is_fresh(25, ranges))
        self.assertFalse(is_fresh(100, ranges))

    def test_count_fresh_ingredients(self):
        """test M log N — підрахунок свіжих інгредієнтів."""
        merged = [(10,20), (30,40)]
        ingredients = [5, 10, 15, 35, 100]

        result = count_fresh_ingredients(ingredients, merged)
        self.assertEqual(result, 3)  # 10 і 15 → свіжі, 35 теж → 3?
        self.assertEqual(count_fresh_ingredients([10,15,35], merged), 3)

    def test_total_fresh_ids(self):
        """Підрахунок сумарної кількості свіжих ID."""
        merged = [(1, 5), (10, 20)] # (1–5) = 5 чисел і (10–20) = 11 чисел
        self.assertEqual(count_total_fresh_ids(merged), 5 + 11)

    def test_large_ranges(self):
        """Перевірка, що великі діапазони не викликають проблем із пам'яттю."""
        merged = [(1, 1_000_000_000)]
        self.assertTrue(is_fresh(500_000_000, merged))
        self.assertFalse(is_fresh(2_000_000_000, merged))

    def test_edge_cases(self):
        """Перевірка крайових випадків."""
        self.assertEqual(merge_ranges([]), [])
        self.assertEqual(count_fresh_ingredients([], []), 0)
        self.assertEqual(count_total_fresh_ids([]), 0)

        merged = [(10,10)]  # один елемент
        self.assertTrue(is_fresh(10, merged))
        self.assertFalse(is_fresh(9, merged))


if __name__ == "__main__":
    unittest.main()
