from app import Figure


def test_triangle_type():
    triangle = Figure("трикутник", 4)
    assert triangle.get_figure_type == "трикутник"


def test_triangle_length():
    triangle = Figure("трикутник", 4)
    assert triangle.get_figure_length == 4


def test_triangle_angles():
    triangle = Figure("трикутник", 4)
    assert triangle.get_angles == 3

def test_square_angles():
    square = Figure("квадрат", 5)
    assert square.get_angles == 4


def test_rectangle_angles():
    rectangle = Figure("прямокутник", 8)
    assert rectangle.get_angles == 4