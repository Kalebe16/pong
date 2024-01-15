from typing import Literal

from pyglet.shapes import Line, Rectangle


class Checkbox:
    def __init__(
        self,
        x: int,
        y: int,
        size: int,
        checked: bool,
        line_color: tuple[
            int, int, int, int
        ],  # Color rgbo = (RED, GREEN, BLUE, OPACITY)
        border_color: tuple[
            int, int, int, int
        ],  # Color rgbo = (RED, GREEN, BLUE, OPACITY)
        fill_type: Literal['x', 'v'],
    ) -> None:
        self.x = x
        self.y = y
        self.checked = checked
        self.line_color = line_color
        self.border_color = border_color
        self.fill_type = fill_type
        self.box = Rectangle(
            x=self.x,
            y=self.y,
            width=size,
            height=size,
            color=self.border_color,
        )
        if self.fill_type == 'x':
            self.line_1 = Line(
                x=self.x,
                y=self.y,
                x2=self.x + size,
                y2=self.y + size,
                width=2,
                color=self.line_color,
            )
            self.line_2 = Line(
                x=self.x + size,
                y=self.y,
                x2=self.x,
                y2=self.y + size,
                width=2,
                color=self.line_color,
            )
        elif self.fill_type == 'v':
            self.line_1 = Line(
                x=self.x,
                y=self.y + size,
                x2=self.x + size / 2,
                y2=self.y,
                width=4,
                color=self.line_color,
            )
            self.line_2 = Line(
                x=self.x + size,
                y=self.y + size,
                x2=self.x + size / 2,
                y2=self.y,
                width=4,
                color=self.line_color,
            )

    def draw(self) -> None:
        self.box.draw()
        if self.checked:
            self.line_1.draw()
            self.line_2.draw()
