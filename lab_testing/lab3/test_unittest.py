import unittest

from app import Figure


class TestFigure(unittest.TestCase):
    def setUp(self):
        self.triangle = Figure("трикутник", 4)

    def test_triangle_type(self):
        self.assertEqual(
            "трикутник",
            self.triangle.get_figure_type,
        )

    def test_triangle_length(self):
        self.assertEqual(4, self.triangle.get_figure_length)

    def test_triangle_angles(self):
        self.assertEqual(3, self.triangle.get_angles)


if __name__ == "__main__":
    unittest.main(verbosity=2)