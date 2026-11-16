import unittest
from unittest.mock import patch

from app import (
    Figure,
    validate_number,
    read_number,
    count_symbols,
    count_vowels,
    divide,
)


class TestFigure(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.figure_types = Figure.FIGURES.copy()

    def setUp(self) -> None:
        self.obj = Figure("квадрат", 5)

    def tearDown(self) -> None:
        self.obj = None

    @classmethod
    def tearDownClass(cls):
        cls.figure_types = []

    def test_figure_type(self):
        self.assertEqual("квадрат", self.obj.get_figure_type)

    def test_figure_length(self):
        self.assertEqual(5, self.obj.get_figure_length)

    def test_invalid_figure(self):
        with self.assertRaises(AssertionError):
            Figure("коло", 1)

    def test_zero_length(self):
        with self.assertRaises(AssertionError):
            Figure("квадрат", 0)

    def test_negative_length(self):
        with self.assertRaises(AssertionError):
            Figure("квадрат", -5)

    def test_all_figure_types(self):
        for figure_type in self.figure_types:
            with self.subTest(figure_type=figure_type):
                figure = Figure(figure_type, 5)
                self.assertEqual(
                    figure_type,
                    figure.get_figure_type,
                )

    def test_different_lengths(self):
        for length in [1, 5, 10]:
            with self.subTest(length=length):
                figure = Figure("квадрат", length)
                self.assertEqual(
                    length,
                    figure.get_figure_length,
                )

    def test_angles(self):
        cases = [
            ("квадрат", 4),
            ("прямокутник", 4),
            ("трикутник", 3),
        ]

        for figure_type, expected in cases:
            with self.subTest(figure_type=figure_type):
                figure = Figure(figure_type, 5)
                self.assertEqual(expected, figure.get_angles())


class TestFunctions(unittest.TestCase):
    def test_count_symbols(self):
        self.assertEqual(3, count_symbols("abc"))
        self.assertEqual(0, count_symbols(""))
        self.assertEqual(1, count_symbols("а"))

    def test_vowels_english(self):
        self.assertEqual(2, count_vowels("Hello"))

    def test_vowels_uppercase(self):
        self.assertEqual(5, count_vowels("AEIOU"))

    def test_vowels_without_vowels(self):
        self.assertEqual(0, count_vowels("bcdfg"))

    def test_vowels_empty(self):
        self.assertEqual(0, count_vowels(""))

    def test_vowels_digits(self):
        self.assertEqual(0, count_vowels("123456"))

    def test_vowels_ukrainian(self):
        self.assertEqual(4, count_vowels("Україна"))
        self.assertEqual(2, count_vowels("Єнот"))

    def test_divide(self):
        self.assertEqual(5, divide(10, 2))

    def test_divide_by_zero(self):
        with self.assertRaises(ZeroDivisionError):
            divide(10, 0)


class TestNumberInput(unittest.TestCase):
    def test_valid_number(self):
        self.assertEqual(5, validate_number("5"))

    def test_minimum_positive_number(self):
        self.assertEqual(1, validate_number("1"))

    def test_invalid_numbers(self):
        for value in ["0", "-5", "abc", "", "2.5"]:
            with self.subTest(value=value):
                with self.assertRaises(ValueError):
                    validate_number(value)

    @patch("builtins.input", return_value="5")
    def test_read_number(self, mock_input):
        self.assertEqual(5, read_number())

        mock_input.assert_called_once_with(
            "Введіть додатне ціле число: "
        )

    @patch("builtins.input", return_value="abc")
    def test_read_invalid_number(self, mock_input):
        with self.assertRaises(ValueError):
            read_number()

        mock_input.assert_called_once_with(
            "Введіть додатне ціле число: "
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)