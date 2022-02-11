import pygame as pg
from random import choice as ch

#............................................................. window params
FPS = 60
WINDOW_WIDTH = 1920
WINDOW_HEIGHT = 1080
WINDOW_CAPTION = "Ping pong"
WINDOW_ICON_IMG  = "icon.png"
BACKGROUND_IMG = "background.jpg"
#............................................................. ball params
BALL_IMG = "ball.png"
BALL_VECTOR = (ch([-4, 4]), ch([-4, 4])) # ball vector - x and y
BALL_SPEED = 0.2               # speed of changing vector
BALL_TOP_SPEED = 20
BALL_DIMENSIONS = (50,50)      # width and height
BALL_X = int((WINDOW_WIDTH-BALL_DIMENSIONS[0])/2)
BALL_Y = int((WINDOW_HEIGHT-BALL_DIMENSIONS[0])/2)
#............................................................. player params
PLAYER_DIMENSIONS = (30, 150)
PLAYER_SPEED = 10
PLAYER_SCORE = 10
PLAYER1_UP = pg.K_w            # movement
PLAYER1_DOWN = pg.K_s
PLAYER2_UP = pg.K_UP
PLAYER2_DOWN = pg.K_DOWN
PLAYER_COLOR = (0,255,255)        # RGB
PLAYER1_X = 10
PLAYER_Y = int((WINDOW_HEIGHT-PLAYER_DIMENSIONS[1])/2)
PLAYER2_X = WINDOW_WIDTH-PLAYER_DIMENSIONS[0]-PLAYER1_X
#............................................................. text params
TEXT_SIZE = 50
TEXT_Y = 4
TEXT_COLOR = (155, 255, 255)
TEXT_FONT = "Comic Sans MS"
TEXT_CONTENT = str(PLAYER_SCORE)
TEXT1_X = int(WINDOW_WIDTH/2)-TEXT_SIZE*4
TEXT2_X = WINDOW_WIDTH-TEXT1_X-TEXT_SIZE/2
TEXT_WIN = "Player {} WON!"
TEXT_WIN_Y = WINDOW_HEIGHT/2-TEXT_SIZE
TEXT_WIN_COLOR = (255, 255, 0)
TEXT_WIN_X = int((WINDOW_WIDTH)/2-TEXT_SIZE*7/2)
TEXT_RESTART = "Press 'R' to restart"
TEXT_RESTART_COLOR = (255, 100, 200)
TEST_RESTART_Y = TEXT_WIN_Y+TEXT_SIZE
TEXT_RESTART_X = int((WINDOW_WIDTH)/2-TEXT_SIZE*9/2)


pg.display.set_caption(WINDOW_CAPTION)              # configuring window
pg.display.set_icon(pg.image.load(WINDOW_ICON_IMG))
main_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pg.transform.scale(pg.image.load(BACKGROUND_IMG), (WINDOW_WIDTH, WINDOW_HEIGHT))

pg.font.init()          # for Text class
timer = pg.time.Clock() # timer for fps


# Classes for the game
class Text():
    def __init__(self, font: str, size: int, x: int, y: int, color:tuple, back_color: tuple = None) -> None:
        self.font = pg.font.SysFont(font, size)
        self.x = x
        self.y = y
        self.color = color
        self.back_color = back_color
    
    def draw(self, content: str):
        main_window.blit(self.font.render(content, True, self.color, self.back_color), (self.x, self.y))

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: float = 0) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def draw(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))

class Player(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: float, up: int, down: int, score:int, color: tuple) -> None:
        super().__init__(image, x, y, speed)
        self.image.fill(color)
        self.up = up
        self.down = down
        self.score = score
    
    def update(self) -> None:
        keys = pg.key.get_pressed()
        if keys[self.up] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys[self.down] and self.rect.y < WINDOW_HEIGHT-PLAYER_DIMENSIONS[1]:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: int, vector: list) -> None:
        super().__init__(image, x, y, speed)
        self.vector = list(vector)

    def change_vector(self, vector: int) -> None:
        self.vector[vector] *= -1
        for i in range(2):
            if self.vector[i] >= 0 and self.vector[i] < BALL_TOP_SPEED:
                self.vector[i] += self.speed
            elif self.vector[i] < 0 and self.vector[i] > -BALL_TOP_SPEED:
                self.vector[i] -= self.speed

    def update(self, left_player: Player, right_player: Player) -> None:
        if self.rect.colliderect(left_player.rect):
            self.change_vector(0)
            self.rect.x = PLAYER1_X+PLAYER_DIMENSIONS[0] +1
        elif self.rect.colliderect(right_player.rect):
            self.change_vector(0)
            self.rect.x = WINDOW_WIDTH-PLAYER1_X-PLAYER_DIMENSIONS[0]-BALL_DIMENSIONS[0] -1
        elif self.rect.x < 0:
            self.change_vector(0)
            self.rect.x = 1
            left_player.score -= 1
        elif self.rect.x > WINDOW_WIDTH-BALL_DIMENSIONS[0]:
            self.change_vector(0)
            self.rect.x = WINDOW_WIDTH-BALL_DIMENSIONS[0] -1
            right_player.score -= 1

        if self.rect.y < 0:
            self.change_vector(1)
            self.rect.y = 1
        elif self.rect.y > WINDOW_HEIGHT-BALL_DIMENSIONS[1]:
            self.change_vector(1)
            self.rect.y = WINDOW_HEIGHT-BALL_DIMENSIONS[1] -1

        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]


# configuring objects
text1 = Text(TEXT_FONT, TEXT_SIZE, TEXT1_X, TEXT_Y, TEXT_COLOR)
text2 = Text(TEXT_FONT, TEXT_SIZE, TEXT2_X, TEXT_Y, TEXT_COLOR)
win = Text(TEXT_FONT, TEXT_SIZE, TEXT_WIN_X, TEXT_WIN_Y, TEXT_WIN_COLOR)
restart = Text(TEXT_FONT, TEXT_SIZE, TEXT_RESTART_X, TEST_RESTART_Y, TEXT_RESTART_COLOR)
ball = Ball(pg.transform.scale(pg.image.load(BALL_IMG), BALL_DIMENSIONS), BALL_X, BALL_Y, BALL_SPEED, BALL_VECTOR)
player1 = Player(pg.Surface(PLAYER_DIMENSIONS), PLAYER1_X, PLAYER_Y, PLAYER_SPEED, PLAYER1_UP, PLAYER1_DOWN, PLAYER_SCORE, PLAYER_COLOR)
player2 = Player(pg.Surface(PLAYER_DIMENSIONS), PLAYER2_X, PLAYER_Y, PLAYER_SPEED, PLAYER2_UP, PLAYER2_DOWN, PLAYER_SCORE, PLAYER_COLOR)

# the game itself
executing = True
game = True
while executing:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            executing = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                game = True
                ball.rect.x, ball.rect.y, ball.vector = BALL_X, BALL_Y, list(BALL_VECTOR)
                player1.rect.x, player1.rect.y, player1.score = PLAYER1_X, PLAYER_Y, PLAYER_SCORE
                player2.rect.x, player2.rect.y, player2.score = PLAYER2_X, PLAYER_Y, PLAYER_SCORE

    if game:
        main_window.blit(background, (0,0))

        player1.update()
        player2.update()
        ball.update(player1, player2)
        text1.draw(str(player1.score))
        text2.draw(str(player2.score))
        ball.draw()
        player1.draw()
        player2.draw()

        if player1.score < 1 or player2.score < 1:
            game = False
            win.draw(TEXT_WIN.format("<-" if player2.score<1 else "->"))
            restart.draw(TEXT_RESTART)

    pg.display.update()
    timer.tick(FPS)