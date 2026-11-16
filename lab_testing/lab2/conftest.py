import pytest

from app import Figure


@pytest.fixture
def square():
    """Окремий квадрат для кожного тесту."""
    return Figure("квадрат", 5)


@pytest.fixture
def length():
    return 10


@pytest.fixture
def figure_ten(length):
    """Приклад залежності однієї fixture від іншої."""
    return Figure("квадрат", length)


@pytest.fixture(scope="module")
def allowed_figures():
    """Створюється один раз для тестового модуля."""
    return tuple(Figure.FIGURES)


@pytest.fixture
def text_file(tmp_path):
    """Створює тимчасовий файл та видаляє його після тесту."""
    path = tmp_path / "result.txt"
    path.write_text("готово", encoding="utf-8")

    yield path

    path.unlink()