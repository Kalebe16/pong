from abc import ABC, abstractmethod
from time import time
from typing import Literal

from pyglet.text import Label
from pyglet.window.key import DOWN, ENTER, SPACE, UP, KeyStateHandler, S, W

from .assets import font_press_start_2p, sound_click
from .consts import COLOR_GREEN, COLOR_WHITE, WINDOW_HEIGHT, WINDOW_WIDTH
from .game_objects import Ball, Player
from .gui import Checkbox


class GameState(ABC):
    def __init__(self) -> None:
        self.game = None

    @abstractmethod
    def enter(self):
        pass

    @abstractmethod
    def exit(self):
        pass

    @abstractmethod
    def update(self, dt):
        pass

    @abstractmethod
    def draw(self):
        pass


class MainMenuState(GameState):
    def __init__(self) -> None:
        super().__init__()

    def enter(self) -> None:
        # Key handler
        self.keyboard = KeyStateHandler()
        self.game.push_handlers(self.keyboard)
        self.last_key_action_time = 0
        self.key_action_cooldown = 0.2

        # GUI Components
        self.title_label = Label(
            'MENU INICIAL',
            font_name=font_press_start_2p,
            font_size=36,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT - 100,
            anchor_x='center',
            anchor_y='center',
        )
        self.start_label = Label(
            'Iniciar Jogo',
            font_name=font_press_start_2p,
            font_size=24,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2,
            anchor_x='center',
            anchor_y='center',
        )
        self.options_label = Label(
            'Opções',
            font_name=font_press_start_2p,
            font_size=24,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2 - 50,
            anchor_x='center',
            anchor_y='center',
        )
        self.exit_label = Label(
            'Sair',
            font_name=font_press_start_2p,
            font_size=24,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2 - 100,
            anchor_x='center',
            anchor_y='center',
        )
        self.pointer_label = Label(
            '→',
            font_name=font_press_start_2p,
            font_size=30,
            x=WINDOW_WIDTH // 2 - 220,
            y=WINDOW_HEIGHT // 2,
            anchor_x='center',
            anchor_y='center',
        )
        self.pointer_selected_option: Literal[
            'Iniciar Jogo', 'Opções', 'Sair'
        ] = 'Iniciar Jogo'

    def exit(self) -> None:
        pass

    def update(self, dt) -> None:
        self._update_pointer_position()
        if self._is_time_for_action():
            if self.keyboard[UP] or self.keyboard[W]:
                self._move_pointer_to_up()
            elif self.keyboard[DOWN] or self.keyboard[S]:
                self._move_pointer_to_down()
            elif self.keyboard[ENTER] or self.keyboard[SPACE]:
                self._execute_option()

    def draw(self):
        self.title_label.draw()
        self.start_label.draw()
        self.options_label.draw()
        self.exit_label.draw()
        self.pointer_label.draw()

    def _update_pointer_position(self) -> None:
        if self.pointer_selected_option == 'Iniciar Jogo':
            self.pointer_label.y = self.start_label.y
        elif self.pointer_selected_option == 'Opções':
            self.pointer_label.y = self.options_label.y
        elif self.pointer_selected_option == 'Sair':
            self.pointer_label.y = self.exit_label.y

    def _is_time_for_action(self) -> bool:
        current_time = time()
        elapsed_time = current_time - self.last_key_action_time
        if elapsed_time > self.key_action_cooldown:
            return True
        elif elapsed_time < self.key_action_cooldown:
            return False

    def _update_last_key_action_time(self) -> None:
        current_time = time()
        self.last_key_action_time = current_time

    def _move_pointer_to_up(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Iniciar Jogo':
            self.pointer_selected_option = 'Sair'
        elif self.pointer_selected_option == 'Opções':
            self.pointer_selected_option = 'Iniciar Jogo'
        elif self.pointer_selected_option == 'Sair':
            self.pointer_selected_option = 'Opções'

    def _move_pointer_to_down(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Iniciar Jogo':
            self.pointer_selected_option = 'Opções'
        elif self.pointer_selected_option == 'Opções':
            self.pointer_selected_option = 'Sair'
        elif self.pointer_selected_option == 'Sair':
            self.pointer_selected_option = 'Iniciar Jogo'

    def _execute_option(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Iniciar Jogo':
            self.game.set_state(state=GameplayState())
        elif self.pointer_selected_option == 'Opções':
            self.game.set_state(state=OptionMenuState())
        elif self.pointer_selected_option == 'Sair':
            self.game.quit()


class OptionMenuState(GameState):
    def __init__(self) -> None:
        super().__init__()

    def enter(self) -> None:
        # Key handler
        self.keyboard = KeyStateHandler()
        self.game.push_handlers(self.keyboard)
        self.last_key_action_time = 0
        self.key_action_cooldown = 0.2

        # GUI Components
        self.title_label = Label(
            'OPÇÕES',
            font_name=font_press_start_2p,
            font_size=36,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT - 100,
            anchor_x='center',
            anchor_y='center',
        )
        self.show_fps_label = Label(
            'Mostrar FPS',
            font_name=font_press_start_2p,
            font_size=24,
            x=WINDOW_WIDTH // 2,
            y=WINDOW_HEIGHT // 2,
            anchor_x='center',
            anchor_y='center',
        )
        self.show_fps_button = Checkbox(
            x=self.show_fps_label.x - 220,
            y=self.show_fps_label.y - 10,
            size=20,
            checked=self.game.show_fps,
            line_color=COLOR_GREEN,
            border_color=COLOR_WHITE,
            fill_type='v',
        )
        self.return_to_main_menu_label = Label(
            'Voltar ao menu principal',
            font_name=font_press_start_2p,
            font_size=24,
            x=WINDOW_WIDTH // 2,
            y=self.show_fps_label.y - 60,
            anchor_x='center',
            anchor_y='center',
        )
        self.pointer_label = Label(
            '→',
            font_name=font_press_start_2p,
            font_size=30,
            x=self.show_fps_button.x - 200,
            y=self.show_fps_button.y,
            anchor_x='center',
            anchor_y='center',
        )
        self.pointer_selected_option: Literal[
            'Mostrar FPS', 'Voltar ao menu principal'
        ] = 'Mostrar FPS'

    def exit(self) -> None:
        pass

    def update(self, dt) -> None:
        self._update_pointer_position()
        if self._is_time_for_action():
            if self.keyboard[UP] or self.keyboard[W]:
                self._move_pointer_to_up()
            elif self.keyboard[DOWN] or self.keyboard[S]:
                self._move_pointer_to_down()
            elif self.keyboard[ENTER]:
                self._execute_option()
        self.game.show_fps = self.show_fps_button.checked

    def draw(self) -> None:
        self.title_label.draw()
        self.show_fps_label.draw()
        self.show_fps_button.draw()
        self.return_to_main_menu_label.draw()
        self.pointer_label.draw()

    def _update_pointer_position(self) -> None:
        if self.pointer_selected_option == 'Mostrar FPS':
            self.pointer_label.y = self.show_fps_button.y
        elif self.pointer_selected_option == 'Voltar ao menu principal':
            self.pointer_label.y = self.return_to_main_menu_label.y

    def _is_time_for_action(self) -> bool:
        current_time = time()
        elapsed_time = current_time - self.last_key_action_time
        if elapsed_time > self.key_action_cooldown:
            return True
        elif elapsed_time < self.key_action_cooldown:
            return False

    def _update_last_key_action_time(self) -> None:
        current_time = time()
        self.last_key_action_time = current_time

    def _move_pointer_to_up(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Mostrar FPS':
            self.pointer_selected_option = 'Voltar ao menu principal'
        elif self.pointer_selected_option == 'Voltar ao menu principal':
            self.pointer_selected_option = 'Mostrar FPS'

    def _move_pointer_to_down(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Mostrar FPS':
            self.pointer_selected_option = 'Voltar ao menu principal'
        elif self.pointer_selected_option == 'Voltar ao menu principal':
            self.pointer_selected_option = 'Mostrar FPS'

    def _execute_option(self) -> None:
        sound_click.play()
        self._update_last_key_action_time()
        if self.pointer_selected_option == 'Mostrar FPS':
            if self.show_fps_button.checked:
                self.show_fps_button.checked = False
            elif not self.show_fps_button.checked:
                self.show_fps_button.checked = True
        elif self.pointer_selected_option == 'Voltar ao menu principal':
            self.game.set_state(state=MainMenuState())


class GameplayState(GameState):
    def __init__(self) -> None:
        super().__init__()

    def enter(self) -> None:
        # Key handler
        self.keyboard = KeyStateHandler()
        self.game.push_handlers(self.keyboard)

        # Game objects
        self.player_1 = Player(
            keyboard=self.keyboard,
            key_to_up=W,
            key_to_down=S,
            x=20,
            y=WINDOW_HEIGHT / 2,
        )
        self.player_2 = Player(
            keyboard=self.keyboard,
            key_to_up=UP,
            key_to_down=DOWN,
            x=WINDOW_WIDTH - 20,
            y=WINDOW_HEIGHT / 2,
        )
        self.ball = Ball(x=WINDOW_WIDTH / 2, y=WINDOW_HEIGHT / 2, radius=10)

    def exit(self) -> None:
        pass

    def update(self, dt) -> None:
        self.player_1.update(dt=dt)
        self.player_2.update(dt=dt)
        self.ball.update(dt=dt)

    def draw(self) -> None:
        self.player_1.draw()
        self.player_2.draw()
        self.ball.draw()
