import json
import pygame as pg
from random import choice as ch

with open("config.json", "r") as config:
    cfg = json.load(config)

FPS = cfg["FPS"]
HALF_HEIGHT = int(cfg["WINDOW_HEIGHT"]/2)
HALF_WIDTH = int(cfg["WINDOW_WIDTH"]/2)

BALL_VECTOR = (ch(cfg["BALL_VECTOR"]), ch(cfg["BALL_VECTOR"]))
PLAYER1_UP = pg.K_w
PLAYER1_DOWN = pg.K_s
PLAYER2_UP = pg.K_UP
PLAYER2_DOWN = pg.K_DOWN
PLAYER2_X = cfg["WINDOW_WIDTH"]-cfg["PLAYER_DIMENSIONS"][0]-cfg["PLAYER1_X"]
TEXT_COUNT_Y = cfg["TEXT_SIZE"]/5*3
TEXT_COUNTER2_X = cfg["WINDOW_WIDTH"]-cfg["TEXT_COUNTER1_X"]
TEXT_WIN_Y = HALF_HEIGHT-cfg["TEXT_SIZE"]

pg.display.set_caption(cfg["WINDOW_CAPTION"])              # configuring window
pg.display.set_icon(pg.image.load(cfg["WINDOW_ICON_IMG"]))
main_window = pg.display.set_mode((cfg["WINDOW_WIDTH"], cfg["WINDOW_HEIGHT"]))
background = pg.transform.scale(pg.image.load(cfg["BACKGROUND_IMG"]), (cfg["WINDOW_WIDTH"], cfg["WINDOW_HEIGHT"]))

pg.font.init()          # for Text class
timer = pg.time.Clock() # timer for fps


# Classes for the game
class Text():
    def __init__(self, font: str, size: int, x: int, y: int, color: tuple) -> None:
        self.font = pg.font.SysFont(font, size)
        self.x = x
        self.y = y
        self.color = color
    
    def draw(self, content: str) -> None:
        text = self.font.render(content, True, self.color)
        main_window.blit(text, text.get_rect(center = (self.x, self.y)))

class GameSprite(pg.sprite.Sprite):
    def __init__(self, image: pg.Surface, x: int, y: int, color: tuple = None) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = x, y
        if color: self.image.fill(color)

    def draw(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))

class Button(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, color: tuple, border_color: tuple, border_thickness: tuple, txt_content: str, txt_font: str, txt_size: int, txt_color: tuple, show: bool = False) -> None:
        super().__init__(image, x, y, color)
        self.text = Text(txt_font, txt_size, self.rect.centerx, self.rect.centery, txt_color)
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.content = txt_content
        self.show = show

    def clicked(self) -> bool:
        if self.show:
            for event in event_list:
                if event.type == pg.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.rect.collidepoint(event.pos):
                            return True
        return False

    def draw(self) -> None:
        if self.show:
            super().draw()
            self.text.draw(self.content)
            pg.draw.rect(self.image, self.border_color, (0,0, self.rect.width, self.rect.height), self.border_thickness)

class Player(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: float, up: int, down: int, score: int, color: tuple) -> None:
        super().__init__(image, x, y, color)
        self.up = up
        self.down = down
        self.speed = speed
        self.score = score
        self.rect.x = x

    def update(self) -> None:
        keys = pg.key.get_pressed()
        if keys[self.up] and self.rect.y > 0:
            self.rect.y -= self.speed
        elif keys[self.down] and self.rect.y < main_window.get_height()-self.rect.height:
            self.rect.y += self.speed

class Ball(GameSprite):
    def __init__(self, image: pg.Surface, x: int, y: int, speed: int, top_speed: int, vector: list) -> None:
        super().__init__(image, x, y)
        self.top_speed = top_speed
        self.vector = list(vector)
        self.speed = speed

    def change_vector(self, vector: int) -> None:
        self.vector[vector] *= -1
        for i in range(2):
            if self.vector[i] >= 0 and self.vector[i] < self.top_speed:
                self.vector[i] += self.speed
            elif self.vector[i] < 0 and self.vector[i] > -self.top_speed:
                self.vector[i] -= self.speed

    def update(self, left_player: Player, right_player: Player) -> None:
        if self.rect.colliderect(left_player.rect):
            self.change_vector(0)
            self.rect.x = left_player.rect.x + left_player.rect.width +1
        elif self.rect.colliderect(right_player.rect):
            self.change_vector(0)
            self.rect.x = right_player.rect.x-self.rect.width -1
        elif self.rect.x < 0:
            self.change_vector(0)
            self.rect.x = 1
            left_player.score -= 1
        elif self.rect.x > main_window.get_width()-self.rect.width:
            self.change_vector(0)
            self.rect.x = main_window.get_width()-self.rect.width -1
            right_player.score -= 1

        if self.rect.y < 0:
            self.change_vector(1)
            self.rect.y = 1
        elif self.rect.y > main_window.get_height()-self.rect.height:
            self.change_vector(1)
            self.rect.y = main_window.get_height()-self.rect.height -1

        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]


# configuring objects
# test_button = Button(pg.Surface((200, 200)), 300, 150, (255,100,200), (0,255,0), 5, "TESTOO", cfg["TEXT_FONT"], 40, (0,255,0), True)

counter1 = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], cfg["TEXT_COUNTER1_X"], TEXT_COUNT_Y, cfg["TEXT_COUNT_COLOR"])
counter2 = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], TEXT_COUNTER2_X, TEXT_COUNT_Y, cfg["TEXT_COUNT_COLOR"])
win = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], HALF_WIDTH, TEXT_WIN_Y, cfg["TEXT_WIN_COLOR"])
restart = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], HALF_WIDTH, HALF_HEIGHT, cfg["TEXT_RESTART_COLOR"])
ball = Ball(pg.transform.scale(pg.image.load(cfg["BALL_IMG"]), cfg["BALL_DIMENSIONS"]), HALF_WIDTH, HALF_HEIGHT, cfg["BALL_SPEED"], cfg["BALL_TOP_SPEED"], BALL_VECTOR)
player1 = Player(pg.Surface(cfg["PLAYER_DIMENSIONS"]), cfg["PLAYER1_X"], HALF_HEIGHT, cfg["PLAYER_SPEED"], PLAYER1_UP, PLAYER1_DOWN, cfg["PLAYER_SCORE"], cfg["PLAYER_COLOR"])
player2 = Player(pg.Surface(cfg["PLAYER_DIMENSIONS"]), PLAYER2_X, HALF_HEIGHT, cfg["PLAYER_SPEED"], PLAYER2_UP, PLAYER2_DOWN, cfg["PLAYER_SCORE"], cfg["PLAYER_COLOR"])

# the game itself
executing = True
game = True
while executing:
    event_list = pg.event.get()
    for e in event_list:
        if e.type == pg.QUIT:
            executing = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                game = True
                ball.rect.center, ball.vector = (HALF_WIDTH, HALF_HEIGHT), list(BALL_VECTOR)
                player1.rect.x, player1.rect.centery, player1.score = cfg["PLAYER1_X"], HALF_HEIGHT, cfg["PLAYER_SCORE"]
                player2.rect.x, player2.rect.centery, player2.score = PLAYER2_X, HALF_HEIGHT, cfg["PLAYER_SCORE"]

    if game:
        main_window.blit(background, (0,0))

        # test_button.draw()
        # if test_button.clicked():
        #     print("CLICKED!!!!!")

        player1.update()
        player2.update()
        ball.update(player1, player2)
        counter1.draw(str(player1.score))
        counter2.draw(str(player2.score))
        ball.draw()
        player1.draw()
        player2.draw()

        if player1.score < 1 or player2.score < 1:
            game = False
            win.draw(cfg["TEXT_WIN"].format("<-" if player2.score<1 else "->"))
            restart.draw(cfg["TEXT_RESTART"])

    pg.display.update()
    timer.tick(FPS)