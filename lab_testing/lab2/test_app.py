import pytest

from app import Figure


@pytest.mark.unit
def test_square_length(square):
    assert square.get_figure_length == 5


@pytest.mark.unit
def test_triangle_type():
    triangle = Figure("трикутник", 4)
    assert triangle.type == "трикутник"


@pytest.mark.parametrize(
    "figure_type",
    Figure.FIGURES,
    ids=["square", "rectangle", "triangle"],
)
def test_allowed_figure(figure_type):
    figure = Figure(figure_type, 1)
    assert figure.get_figure_type == figure_type


def test_fixture_length(figure_ten):
    assert figure_ten.get_figure_length == 10


def test_fixture_type(figure_ten):
    assert figure_ten.get_figure_type == "квадрат"


def test_fixture_angles(figure_ten):
    assert figure_ten.get_angles() == 4


@pytest.mark.parametrize(
    "figure_type",
    ["коло", "ромб", "", "КВАДРАТ"],
    ids=["circle", "rhombus", "empty", "uppercase"],
)
def test_invalid_figure(figure_type):
    with pytest.raises(AssertionError, match="Невідомий тип фігури"):
        Figure(figure_type, 5)


@pytest.mark.parametrize(
    "length",
    [0, -1, -10],
    ids=["zero", "negative_one", "negative_ten"],
)
def test_invalid_length(length):
    with pytest.raises(
        AssertionError,
        match="Довжина має бути більшою за 0!",
    ):
        Figure("квадрат", length)


def test_module_fixture_types(allowed_figures):
    assert allowed_figures == (
        "квадрат",
        "прямокутник",
        "трикутник",
    )


def test_module_fixture_count(allowed_figures):
    assert len(allowed_figures) == 3


def test_text_file(text_file):
    assert text_file.read_text(encoding="utf-8") == "готово"