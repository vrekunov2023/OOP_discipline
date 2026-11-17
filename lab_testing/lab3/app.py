class Figure:
    FIGURES = ["квадрат", "прямокутник", "трикутник"]

    def __init__(self, figure_type: str, length: int):
        assert length > 0, "Довжина має бути більшою за 0!"
        assert figure_type in self.FIGURES, "Невідомий тип фігури"

        self.type = figure_type
        self.length = length

    @property
    def get_figure_type(self):
        return self.type

    @property
    def get_figure_length(self):
        return self.length

    @property
    def get_angles(self):
        if self.type == "квадрат":
            return 4
        elif self.type == "прямокутник":
            return 4
        else:
            return 3


if __name__ == "__main__":  # pragma: no cover
    print("Для перевірки програми запустіть тести.")