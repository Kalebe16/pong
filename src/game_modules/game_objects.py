from random import choice
from typing import Literal, Union

from pyglet.shapes import Circle, Rectangle
from pyglet.window.key import DOWN, UP, KeyStateHandler, S, W

from .assets import sound_tuc
from .consts import COLOR_WHITE, WINDOW_HEIGHT, WINDOW_WIDTH


class Player(Rectangle):
    def __init__(
        self,
        keyboard: KeyStateHandler,
        key_to_up: Union[UP, W],
        key_to_down: Union[DOWN, S],
        x: int,
        y: int,
    ) -> None:
        super().__init__(x=x, y=y, width=20, height=120, color=COLOR_WHITE)
        self.keyboard = keyboard
        self.key_to_up = key_to_up
        self.key_to_down = key_to_down
        self.x = x
        self.y = y
        self.speed = 200

        # Centralize anchors from object
        self.anchor_x = self.width / 2
        self.anchor_y = self.height / 2

    def update(self, dt) -> None:
        if (
            self.keyboard[self.key_to_up]
            and not self._collide_with_top_window()
        ):
            self._move_to_up(dt=dt)
        elif (
            self.keyboard[self.key_to_down]
            and not self._collide_with_bottom_window()
        ):
            self._move_to_down(dt=dt)

    def draw(self) -> None:
        super().draw()

    def _get_top(self) -> int:
        top = self.y + (self.height / 2)
        return int(top)

    def _get_bottom(self) -> int:
        bottom = self.y - (self.height / 2)
        return int(bottom)

    def _collide_with_top_window(self) -> bool:
        top = self._get_top()
        if top <= WINDOW_HEIGHT:
            return False
        return True

    def _collide_with_bottom_window(self) -> bool:
        bottom = self._get_bottom()
        if bottom >= 0:
            return False
        return True

    def _move_to_up(self, dt) -> None:
        self.y += self.speed * dt

    def _move_to_down(self, dt) -> None:
        self.y -= self.speed * dt


class Ball(Circle):
    def __init__(
        self,
        x: Union[int, float],
        y: Union[int, float],
        radius: Union[int, float],
    ) -> None:
        super().__init__(x=x, y=y, radius=radius, color=COLOR_WHITE)
        self.x = x
        self.y = y
        self.radius = radius

        # Centralize anchors from object
        # self.anchor_x = self.width / 2
        # self.anchor_y = self.height / 2
        # Circle já é centralizado por padrão

        self.speed = 200
        self.direction_x: Literal['left', 'right'] = choice(['left', 'right'])
        self.direction_y: Literal['up', 'down'] = choice(['up', 'down'])

    def draw(self) -> None:
        super().draw()

    def update(self, dt) -> None:
        self._handle_collide()

        if self.direction_x == 'left':
            self._move_to_left(dt=dt)
        elif self.direction_x == 'right':
            self._move_to_right(dt=dt)

        if self.direction_y == 'up':
            self._move_to_up(dt=dt)
        elif self.direction_y == 'down':
            self._move_to_down(dt=dt)

    def _get_left(self) -> int:
        left = self.x - (self.radius / 2)
        return int(left)

    def _get_right(self) -> int:
        right = self.x + (self.radius / 2)
        return int(right)

    def _get_top(self) -> int:
        top = self.y + (self.radius / 2)
        return int(top)

    def _get_bottom(self) -> int:
        bottom = self.y - (self.radius / 2)
        return int(bottom)

    def _collide_with_left_window(self) -> bool:
        left = self._get_left()
        if left >= 0:
            return False
        return True

    def _collide_with_right_window(self) -> bool:
        right = self._get_right()
        if right <= WINDOW_WIDTH:
            return False
        return True

    def _collide_with_top_window(self) -> bool:
        top = self._get_top()
        if top <= WINDOW_HEIGHT:
            return False
        return True

    def _collide_with_bottom_window(self) -> bool:
        bottom = self._get_bottom()
        if bottom >= 0:
            return False
        return True

    def _handle_collide(self) -> None:
        if self.direction_x == 'left' and self._collide_with_left_window():
            sound_tuc.play()
            self.direction_x = 'right'
        elif self.direction_x == 'right' and self._collide_with_right_window():
            sound_tuc.play()
            self.direction_x = 'left'

        if self.direction_y == 'up' and self._collide_with_top_window():
            sound_tuc.play()
            self.direction_y = 'down'
        elif self.direction_y == 'down' and self._collide_with_bottom_window():
            sound_tuc.play()
            self.direction_y = 'up'

    def _move_to_left(self, dt) -> None:
        self.x -= self.speed * dt

    def _move_to_right(self, dt) -> None:
        self.x += self.speed * dt

    def _move_to_up(self, dt) -> None:
        self.y += self.speed * dt

    def _move_to_down(self, dt) -> None:
        self.y -= self.speed * dt
