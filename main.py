import pygame as pg
from random import choice as ch

FPS = 60
WINDOW_WIDTH = 800              # window params
WINDOW_HEIGHT = 500
WINDOW_CAPTION = "Ping pong"
WINDOW_ICON_IMG  = "icon.png"
BACKGROUND_IMG = "background.jpg"
BALL_IMG = "ball.png"           #................................... ball params
BALL_VECTOR = [ch([-4, 4]), ch([-4, 4])] # ball vector - x and y
BALL_SPEED = 0.5               # speed of changing vector
BALL_TOP_SPEED = 20
BALL_DIMENSIONS = (50,50)      # width and height
PLAYER_DIMENSIONS = (30, 150)   #................................... player params
PLAYER_SPEED = 8
PLAYER1_UP = pg.K_w            # movement
PLAYER1_DOWN = pg.K_s
PLAYER2_UP = pg.K_UP
PLAYER2_DOWN = pg.K_DOWN
PLAYER_COLOR = (0,255,255)        # RGB
PLAYER1_X = 10
PLAYER_Y = int((WINDOW_HEIGHT-PLAYER_DIMENSIONS[1])/2)      #....... auto params
PLAYER2_X = WINDOW_WIDTH-PLAYER_DIMENSIONS[0]-PLAYER1_X
BALL_X = int((WINDOW_WIDTH-BALL_DIMENSIONS[0])/2)
BALL_Y = int((WINDOW_HEIGHT-BALL_DIMENSIONS[0])/2)

pg.display.set_caption(WINDOW_CAPTION)              # configuring window
pg.display.set_icon(pg.image.load(WINDOW_ICON_IMG))
main_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pg.transform.scale(pg.image.load(BACKGROUND_IMG), (WINDOW_WIDTH, WINDOW_HEIGHT))

timer = pg.time.Clock() # timer for fps

# Classes for the game
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
    def __init__(self, image: pg.Surface, x: int, y: int, speed: float, up: int, down: int, color: tuple) -> None:
        super().__init__(image, x, y, speed)
        self.image.fill(color)
        self.up = up
        self.down = down
    
    def update(self) -> None:
        keys = pg.key.get_pressed()
        if keys[self.up] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys[self.down] and self.rect.y < WINDOW_HEIGHT-PLAYER_DIMENSIONS[1]:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: int, vector: list) -> None:
        super().__init__(image, x, y, speed)
        self.vector = vector

    def change_vector(self, vector: int) -> None:
        self.vector[vector] *= -1
        for i in range(2):
            if self.vector[i] > 0 and self.vector[i] < BALL_TOP_SPEED:
                self.vector[i] += self.speed
            else:
                self.vector[i] -= self.speed

    def update(self) -> None:
        if self.rect.x < 0:
            self.change_vector(0)
            self.rect.x = 1
        elif self.rect.x > WINDOW_WIDTH-BALL_DIMENSIONS[0]:
            self.change_vector(0)
            self.rect.x = WINDOW_WIDTH-BALL_DIMENSIONS[0] -1

        if self.rect.y < 0:
            self.change_vector(1)
            self.rect.y = 1
        elif self.rect.y > WINDOW_HEIGHT-BALL_DIMENSIONS[1]:
            self.change_vector(1)
            self.rect.y = WINDOW_HEIGHT-BALL_DIMENSIONS[1] -1

        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]


# configuring objects
ball = Ball(pg.transform.scale(pg.image.load(BALL_IMG), BALL_DIMENSIONS), BALL_X, BALL_Y, BALL_SPEED, BALL_VECTOR)
player1 = Player(pg.Surface(PLAYER_DIMENSIONS), PLAYER1_X, PLAYER_Y, PLAYER_SPEED, PLAYER1_UP, PLAYER1_DOWN, PLAYER_COLOR)
player2 = Player(pg.Surface(PLAYER_DIMENSIONS), PLAYER2_X, PLAYER_Y, PLAYER_SPEED, PLAYER2_UP, PLAYER2_DOWN, PLAYER_COLOR)

# the game itself
executing = True
while executing:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            executing = False

    main_window.blit(background, (0,0))

    player1.update()
    player2.update()
    ball.update()
    ball.draw()
    player1.draw()
    player2.draw()

    pg.display.update()
    timer.tick(FPS)