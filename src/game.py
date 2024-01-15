from sys import exit

from pyglet.app import run
from pyglet.clock import schedule_interval
from pyglet.window import FPSDisplay, Window

from game_modules.consts import WINDOW_HEIGHT, WINDOW_WIDTH
from game_modules.game_states import GameState, MainMenuState


class Game(Window):
    def __init__(self):
        super().__init__(
            width=WINDOW_WIDTH, height=WINDOW_HEIGHT, caption='PyPong'
        )
        self._set_window_configs()
        self.state = None
        self.show_fps = False
        self.set_state(state=MainMenuState())

    def _set_window_configs(self):
        self.set_mouse_visible(visible=False)
        self.fps_display = FPSDisplay(self)

    def set_state(self, state: GameState) -> None:
        if self.state:
            self.state.exit()
        self.state = state
        self.state.game = self
        self.state.enter()

    def update(self, dt) -> None:
        self.state.update(dt=dt)
        if self.show_fps:
            self.fps_display.update()

    def on_draw(self) -> None:
        self.clear()
        self.state.draw()
        if self.show_fps:
            self.fps_display.draw()

    def on_key_press(self, symbol, modifiers):
        """
        Prevents pyglet from closing the window when clicking the "ESC" button
        """
        pass

    def quit(self) -> None:
        exit(0)


if __name__ == '__main__':
    game = Game()
    schedule_interval(func=game.update, interval=1 / 120.0)
    run()
