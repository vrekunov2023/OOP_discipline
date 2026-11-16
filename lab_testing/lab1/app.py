class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]

    def __init__(self, figure_type: str, length: int) -> None:
        assert length > 0, "Довжина має бути більшою за 0!"
        assert figure_type in self.FIGURES, "Невідомий тип фігури"

        self.type = figure_type
        self.length = length

    @property
    def get_figure_type(self) -> str:
        return self.type

    @property
    def get_figure_length(self) -> int:
        return self.length + 1

    def get_angles(self) -> int:
        """Повертає кількість кутів фігури."""
        if self.type == "трикутник":
            return 3
        return 4


def validate_number(value: str) -> int:
    """Перевіряє введення додатного цілого числа."""
    try:
        number = int(value)
    except ValueError:
        raise ValueError("Потрібно ввести ціле число!") from None

    if number <= 0:
        raise ValueError("Число має бути більшим за нуль!")

    return number


def read_number() -> int:
    """Зчитує число з клавіатури та перевіряє його."""
    value = input("Введіть додатне ціле число: ")
    return validate_number(value)


def count_symbols(text: str) -> int:
    return len(text)


def count_vowels(text: str) -> int:
    """Рахує українські та англійські голосні."""
    vowels = "аеєиіїоуюяaeiou"
    return sum(letter in vowels for letter in text.lower())


def divide(a: float, b: float) -> float:
    return a / b


def main():
    print("=== Ручна перевірка фігур ===")

    figures = [
        Figure("квадрат", 5),
        Figure("прямокутник", 8),
        Figure("трикутник", 3),
    ]

    for figure in figures:
        print(
            f"Фігура: {figure.get_figure_type}; "
            f"довжина: {figure.get_figure_length}; "
            f"кількість кутів: {figure.get_angles()}"
        )

    print("\n=== Підрахунок голосних ===")

    for text in ["Hello", "Україна", "12345", ""]:
        print(f"{text!r}: {count_vowels(text)}")

    print("\n=== Перевірка введеного числа ===")

    try:
        number = read_number()
        print(f"Число прийнято: {number}")
    except ValueError as error:
        print(f"Помилка: {error}")


if __name__ == "__main__":
    main()