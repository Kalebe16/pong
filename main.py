import random
import pygame

pygame.init()
pygame.mixer.init()

# WINDOW
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720

# COLOR
PALE_GREEN_COLOR = pygame.Color('#98FB98')
LIGHT_CORAL_COLOR = pygame.Color('#F08080')

# SOUND
TUC_SOUND = pygame.mixer.Sound('./assets/sounds/tuc.mp3')
BRASIL_SOUND = pygame.mixer.Sound('./assets/sounds/brasil.mp3')


class ScoreBoard:
    def __init__(
        self,
        screen: pygame.Surface,
        player_1_points: int,
        player_2_points: int,
    ) -> None:
        self.screen = screen
        self.player_1_points = player_1_points
        self.player_2_points = player_2_points

    def reset(self):
        self.player_1_points = 0
        self.player_2_points = 0

    def draw(self):
        font = pygame.font.Font(None, 36)
        text_surface = font.render(
            f'{str(self.player_1_points)} : {str(self.player_2_points)}',
            True,
            LIGHT_CORAL_COLOR,
        )
        self.screen.blit(text_surface, (WINDOW_WIDTH / 2, 10))


class Player:
    def __init__(self, position: tuple, speed: int | float):
        self.position = pygame.Vector2(position)
        self.speed = speed
        self.width = 20
        self.height = 200
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.update_rect_position()

    def update_rect_position(self):
        self.rect.center = (int(self.position.x), int(self.position.y))

    def move_up(self, dt):
        if self.rect.top > 0:
            self.position.y -= self.speed * dt
        self.update_rect_position()

    def move_down(self, dt):
        if self.rect.bottom < WINDOW_HEIGHT:
            self.position.y += self.speed * dt
        self.update_rect_position()

    def draw(self, screen):
        pygame.draw.rect(
            screen, LIGHT_CORAL_COLOR, self.rect, border_radius=10
        )


class Ball:
    def __init__(
        self,
        position: tuple,
        direction_x: str,
        direction_y,
        speed: int | float,
    ) -> None:
        self.position = pygame.Vector2(position)
        self.direction_x = direction_x
        self.direction_y = direction_y
        self.speed = speed
        self.width = 20
        self.height = 20
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.update_rect_position()

    def reset(self) -> None:
        self.position = pygame.Vector2((WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2))
        self.direction_x = random.choice(['left', 'right'])
        self.direction_y = random.choice(['up', 'down'])
        self.speed = 300

    def update_rect_position(self):
        self.rect.center = (int(self.position.x), int(self.position.y))

    def move(self, dt) -> None:
        if self.direction_x == 'left':
            self.position.x -= self.speed * dt
        elif self.direction_x == 'right':
            self.position.x += self.speed * dt

        if self.direction_y == 'up':
            self.position.y -= self.speed * dt
        elif self.direction_y == 'down':
            self.position.y += self.speed * dt

        self.update_rect_position()

    def draw(self, screen):
        pygame.draw.rect(
            screen, LIGHT_CORAL_COLOR, self.rect, border_radius=10
        )


class Game:
    def __init__(self):
        self.create_screen()
        self.score_board = ScoreBoard(
            screen=self.screen, player_1_points=0, player_2_points=0
        )
        self.player_1 = Player(position=(14, WINDOW_HEIGHT / 2), speed=300)
        self.player_2 = Player(
            position=(WINDOW_WIDTH - 14, WINDOW_HEIGHT / 2), speed=300
        )
        self.ball = Ball(
            position=(WINDOW_WIDTH / 2, WINDOW_HEIGHT / 2),
            direction_x=random.choice(['left', 'right']),
            direction_y=random.choice(['up', 'down']),
            speed=300,
        )
        self.running = True
        self.dt = None
        self.clock = pygame.time.Clock()

    def create_screen(self):
        self.screen = pygame.display.set_mode(
            size=(WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption(title='PYTHON PONG')

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def handle_inputs(self):
        keys = pygame.key.get_pressed()

        # MOVE PLAYER_1
        if keys[pygame.K_w]:
            self.player_1.move_up(dt=self.dt)
        elif keys[pygame.K_s]:
            self.player_1.move_down(dt=self.dt)

        # MOVE PLAYER_2
        if keys[pygame.K_UP]:
            self.player_2.move_up(dt=self.dt)
        elif keys[pygame.K_DOWN]:
            self.player_2.move_down(dt=self.dt)

        # MOVE BALL
        self.ball.move(dt=self.dt)

        # GAME RULES
        self.handle_collisions()
        self.count_points()

    def handle_collisions(self):
        if self.ball.rect.top <= 0:
            self.ball.direction_y = 'down'
            TUC_SOUND.play()
        elif self.ball.rect.bottom >= WINDOW_HEIGHT:
            self.ball.direction_y = 'up'
            TUC_SOUND.play()

        if self.ball.rect.colliderect(self.player_1.rect):
            self.ball.direction_x = 'right'
            TUC_SOUND.play()
        elif self.ball.rect.colliderect(self.player_2.rect):
            self.ball.direction_x = 'left'
            TUC_SOUND.play()

    def count_points(self):
        if self.ball.rect.right <= 0:
            self.score_board.player_2_points += 1
            BRASIL_SOUND.play()
            self.ball.reset()
        elif self.ball.rect.left >= WINDOW_WIDTH:
            self.score_board.player_1_points += 1
            BRASIL_SOUND.play()
            self.ball.reset()

    def draw(self):
        self.screen.fill(PALE_GREEN_COLOR)
        self.player_1.draw(self.screen)
        self.player_2.draw(self.screen)
        self.ball.draw(self.screen)
        self.score_board.draw()
        pygame.display.flip()

    def run(self):
        while self.running:
            self.dt = self.clock.tick(60) / 1000
            self.handle_events()
            self.handle_inputs()
            self.draw()
        pygame.quit()





if __name__ == '__main__':
    game = Game()
    game.run()
