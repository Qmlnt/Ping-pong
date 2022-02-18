import json
import pygame as pg
from random import randint as ri

with open("config.json", "r") as config:
    cfg = json.load(config)

FPS = cfg["FPS"]
HALF_HEIGHT = int(cfg["WINDOW_HEIGHT"]/2)
HALF_WIDTH = int(cfg["WINDOW_WIDTH"]/2)
BALL_VECTOR = (ri(-cfg["BALL_VECTOR"], cfg["BALL_VECTOR"]), ri(-cfg["BALL_VECTOR"], cfg["BALL_VECTOR"]))
PLAYER1_UP = pg.K_w
PLAYER1_DOWN = pg.K_s
PLAYER2_UP = pg.K_UP
PLAYER2_DOWN = pg.K_DOWN
PLAYER2_X = cfg["WINDOW_WIDTH"]-cfg["PLAYER_DIMENSIONS"][0]-cfg["PLAYER1_X"]
TEXT_COUNT_Y = cfg["TEXT_SIZE"]/5*3
TEXT_COUNTER2_X = cfg["WINDOW_WIDTH"]-cfg["TEXT_COUNTER1_X"]
TEXT_WIN_Y = HALF_HEIGHT-cfg["TEXT_SIZE"]
TEXT_MENU2_X = cfg["WINDOW_WIDTH"]-cfg["TEXT_MENU1_X"]

pg.display.set_caption(cfg["WINDOW_CAPTION"])              # configuring window
pg.display.set_icon(pg.image.load(cfg["WINDOW_ICON_IMG"]))
main_window = pg.display.set_mode((cfg["WINDOW_WIDTH"], cfg["WINDOW_HEIGHT"]))

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
    def __init__(self, image: pg.Surface, x: int, y: int, color: tuple, border_color: tuple, border_thickness: int, txt_content: str, txt_font: str, txt_size: int, txt_color: tuple) -> None:
        super().__init__(image, x, y, color)
        self.text = Text(txt_font, txt_size, self.rect.centerx, self.rect.centery, txt_color)
        self.border_thickness = border_thickness
        self.border_color = border_color
        self.content = txt_content

    def clicked(self) -> bool:
        for event in event_list:
            if event.type == pg.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if self.rect.collidepoint(event.pos):
                        return True
        return False

    def draw(self) -> None:
        super().draw()
        self.text.draw(self.content)
        pg.draw.rect(self.image, self.border_color, (0,0, self.rect.width, self.rect.height), self.border_thickness)

class Settings_block(GameSprite):
    def __init__(self, x: int, y: int, description: str, variable: float, change: float) -> None:
        super().__init__(pg.Surface(cfg["SETTINGS_DIMENSIONS"]), x, y, cfg["SETTINGS_BUTTON_COLOR"])
        self.change = change
        self.variable = variable
        self.description = description
        self.border_color = cfg["BUTTON_BORDER_COLOR"]
        self.border_thickness = cfg["BUTTON_BORDER_THICKNESS"]

        self.description_text = Text(cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], self.rect.centerx, self.rect.y-cfg["SETTINGS_TEXT_SIZE"]/2-6, cfg["SETTINGS_TEXT_COLOR"])
        self.text = Text(cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], self.rect.centerx, self.rect.centery, cfg["BUTTON_TEXT_COLOR"])
        self.left = Button(pg.Surface((self.rect.height, self.rect.height)), self.rect.x-2-self.rect.height/2, y, cfg["SETTINGS_BUTTON_COLOR"], self.border_color,
            self.border_thickness, "<", cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
        self.right = Button(pg.Surface((self.rect.height, self.rect.height)), self.rect.x+self.rect.width+2+self.rect.height/2, y, cfg["SETTINGS_BUTTON_COLOR"],
            self.border_color, self.border_thickness, ">", cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])

    def update(self) -> None:
        if self.left.clicked():
            self.variable -= self.change
        elif self.right.clicked():
            self.variable += self.change

    def draw(self) -> None:
        super().draw()
        self.right.draw()
        self.left.draw()
        self.text.draw(str(self.variable))
        self.description_text.draw(self.description)
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

class Bot(Player):
    def update(self) -> None:
        ball_center = ball_g.rect.centery
        if self.rect.centery > ball_center and self.rect.y > 0:
            self.rect.y -= self.speed
        elif self.rect.centery < ball_center and self.rect.y < main_window.get_height()-self.rect.height:
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
        if self.rect.x < 0:
            self.change_vector(0)
            self.rect.x = 1
            left_player.score -= 1
        elif self.rect.x > main_window.get_width()-self.rect.width:
            self.change_vector(0)
            self.rect.x = main_window.get_width()-self.rect.width -1
            right_player.score -= 1
        elif self.rect.colliderect(left_player.rect):
            self.change_vector(0)
            self.rect.x = left_player.rect.x + left_player.rect.width +1
        elif self.rect.colliderect(right_player.rect):
            self.change_vector(0)
            self.rect.x = right_player.rect.x-self.rect.width -1

        if self.rect.y < 0:
            self.change_vector(1)
            self.rect.y = 1
        elif self.rect.y > main_window.get_height()-self.rect.height:
            self.change_vector(1)
            self.rect.y = main_window.get_height()-self.rect.height -1

        self.rect.x += self.vector[0]
        self.rect.y += self.vector[1]


# configuring objects

background_game = pg.transform.scale(pg.image.load(cfg["BACKGROUND_IMG"]), (cfg["WINDOW_WIDTH"], cfg["WINDOW_HEIGHT"]))
background_menu = pg.Surface((cfg["WINDOW_WIDTH"], cfg["WINDOW_HEIGHT"]))
background_menu.fill(cfg["MENU_COLOR"])

pvp_button = Button(pg.Surface(cfg["BUTTON_DIMENSIONS"]), HALF_WIDTH, HALF_HEIGHT-cfg["BUTTON_DISTANCES"]-cfg["BUTTON_DIMENSIONS"][1], cfg["BUTTON_COLOR"],
    cfg["BUTTON_BORDER_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "Player VS Player", cfg["TEXT_FONT"], cfg["BUTTON_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
pvbot_button = Button(pg.Surface(cfg["BUTTON_DIMENSIONS"]), HALF_WIDTH, HALF_HEIGHT, cfg["BUTTON_COLOR"], cfg["BUTTON_BORDER_COLOR"], cfg["BUTTON_BORDER_THICKNESS"],
    "Player VS Bot", cfg["TEXT_FONT"], cfg["BUTTON_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
settings_button = Button(pg.Surface(cfg["BUTTON_DIMENSIONS"]), HALF_WIDTH, HALF_HEIGHT+cfg["BUTTON_DISTANCES"]+cfg["BUTTON_DIMENSIONS"][1], cfg["BUTTON_COLOR"],
    cfg["BUTTON_BORDER_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "Settings", cfg["TEXT_FONT"], cfg["BUTTON_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
counter1_m = Text(cfg["TEXT_FONT"], cfg["TEXT_MENU_SIZE"], cfg["TEXT_MENU1_X"], HALF_HEIGHT, cfg["TEXT_COUNT_COLOR"])
counter2_m = Text(cfg["TEXT_FONT"], cfg["TEXT_MENU_SIZE"], TEXT_MENU2_X, HALF_HEIGHT, cfg["TEXT_COUNT_COLOR"])
player1_menu_score = 0
player2_menu_score = 0


right_layer_x = cfg["WINDOW_WIDTH"]/4
left_layer_x = cfg["WINDOW_WIDTH"]-right_layer_x
back_to_menu = Button(pg.Surface((120, 40)), 70, 30, cfg["BUTTON_COLOR"], cfg["BUTTON_BORDER_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "<- back",
    cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
save_and_quit = Button(pg.Surface((210, 60)), HALF_WIDTH, 40, cfg["BUTTON_COLOR"], cfg["BUTTON_BORDER_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "Save and Quit",
    cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["BUTTON_TEXT_COLOR"])
settings_window_width = Settings_block(right_layer_x, 150, "Window width", cfg["WINDOW_WIDTH"], 20)
get_x = lambda num: settings_window_width.rect.y+settings_window_width.rect.height/2 + (settings_window_width.rect.height+cfg["SETTINGS_TEXT_SIZE"]+10)*num
settings_window_height = Settings_block(right_layer_x, get_x(1), "Window height", cfg["WINDOW_HEIGHT"], 20)
settings_ball_acceleration = Settings_block(right_layer_x, get_x(2), "Ball acceleration", cfg["BALL_SPEED"], 0.1)
settings_ball_top_speed = Settings_block(right_layer_x, get_x(3), "Ball top speed", cfg["BALL_TOP_SPEED"], 2)
settings_ball_initial_speed = Settings_block(right_layer_x, get_x(4), "Ball initial speed", cfg["BALL_VECTOR"], 1)
settings_player_speed = Settings_block(left_layer_x, 150, "Player speed", cfg["PLAYER_SPEED"], 1)
settings_player_score = Settings_block(left_layer_x, get_x(1), "Player score", cfg["PLAYER_SCORE"], 1)
settings_ball_size = Settings_block(left_layer_x, get_x(2), "Ball size", cfg["BALL_SIZE"], 2)
settings_player_width = Settings_block(left_layer_x, get_x(3), "Player width", cfg["PLAYER_DIMENSIONS"][0], 2)
settings_player_height = Settings_block(left_layer_x, get_x(4), "Player height", cfg["PLAYER_DIMENSIONS"][1], 10)


menu_g = Button(pg.Surface((120, 40)), HALF_WIDTH, 25, cfg["SETTINGS_TEXT_COLOR"], cfg["SETTINGS_TEXT_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "MENU",
    cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["MENU_COLOR"])
pause_g = Button(pg.Surface((100, 50)), HALF_WIDTH, 60, cfg["SETTINGS_TEXT_COLOR"], cfg["SETTINGS_TEXT_COLOR"], cfg["BUTTON_BORDER_THICKNESS"], "pause",
    cfg["TEXT_FONT"], cfg["SETTINGS_TEXT_SIZE"], cfg["MENU_COLOR"])
counter1_g = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], cfg["TEXT_COUNTER1_X"], TEXT_COUNT_Y, cfg["TEXT_COUNT_COLOR"])
counter2_g = Text(cfg["TEXT_FONT"], cfg["TEXT_SIZE"], TEXT_COUNTER2_X, TEXT_COUNT_Y, cfg["TEXT_COUNT_COLOR"])
ball_g = Ball(pg.transform.scale(pg.image.load(cfg["BALL_IMG"]), (cfg["BALL_SIZE"], cfg["BALL_SIZE"])), HALF_WIDTH, HALF_HEIGHT, cfg["BALL_SPEED"], cfg["BALL_TOP_SPEED"], BALL_VECTOR)
player1_g = Player(pg.Surface(cfg["PLAYER_DIMENSIONS"]), cfg["PLAYER1_X"], HALF_HEIGHT, cfg["PLAYER_SPEED"], PLAYER1_UP, PLAYER1_DOWN, cfg["PLAYER_SCORE"], cfg["PLAYER_COLOR"])
player2_g = None
player2 = Player(pg.Surface(cfg["PLAYER_DIMENSIONS"]), PLAYER2_X, HALF_HEIGHT, cfg["PLAYER_SPEED"], PLAYER2_UP, PLAYER2_DOWN, cfg["PLAYER_SCORE"], cfg["PLAYER_COLOR"])
bot2 = Bot(pg.Surface(cfg["PLAYER_DIMENSIONS"]), PLAYER2_X, HALF_HEIGHT, cfg["PLAYER_SPEED"], PLAYER2_UP, PLAYER2_DOWN, cfg["PLAYER_SCORE"], cfg["PLAYER_COLOR"])

def normalize() -> None:
    global pause
    pause = False
    ball_g.rect.center, ball_g.vector = (HALF_WIDTH, HALF_HEIGHT), list((ri(-cfg["BALL_VECTOR"], cfg["BALL_VECTOR"]), ri(-cfg["BALL_VECTOR"], cfg["BALL_VECTOR"])))
    player1_g.rect.x, player1_g.rect.centery, player1_g.score = cfg["PLAYER1_X"], HALF_HEIGHT, cfg["PLAYER_SCORE"]
    player2_g.rect.x, player2_g.rect.centery, player2_g.score = PLAYER2_X, HALF_HEIGHT, cfg["PLAYER_SCORE"]

# the game itself
menu = True
game = False
pause = False
settings = False
executing = True
while executing:
    event_list = pg.event.get()
    for e in event_list:
        if e.type == pg.QUIT:
            executing = False
        elif e.type == pg.KEYDOWN:
            if e.key == pg.K_r:
                normalize()


    if menu:
        main_window.blit(background_menu, (0,0))
        pvp_button.draw()
        pvbot_button.draw()
        settings_button.draw()
        counter1_m.draw(str(player1_menu_score))
        counter2_m.draw(str(player2_menu_score))
        if pvp_button.clicked() or pvbot_button.clicked():
            player2_g = player2 if pvp_button.clicked() else bot2
            normalize()
            game = True
            menu = False
        elif settings_button.clicked():
            menu = False
            settings = True

    if settings:
        main_window.blit(background_menu, (0,0))

        for el in [settings_window_width, settings_window_height, settings_ball_top_speed, settings_ball_acceleration, settings_ball_initial_speed,
        settings_ball_size, settings_player_speed, settings_player_score, settings_player_width, settings_player_height]: el.draw(); el.update()

        back_to_menu.draw()
        save_and_quit.draw()

        if save_and_quit.clicked():
            cfg["WINDOW_WIDTH"] = settings_window_width.variable
            cfg["WINDOW_HEIGHT"] = settings_window_height.variable
            cfg["BALL_SPEED"] = settings_ball_acceleration.variable
            cfg["BALL_TOP_SPEED"] = settings_ball_top_speed.variable
            cfg["BALL_VECTOR"] = settings_ball_initial_speed.variable
            cfg["BALL_SIZE"] = settings_ball_size.variable
            cfg["PLAYER_SPEED"] = settings_player_speed.variable
            cfg["PLAYER_SCORE"] = settings_player_score.variable
            cfg["PLAYER_DIMENSIONS"] = [settings_player_width.variable, settings_player_height.variable]

            with open("config.json", 'w', encoding='utf-8') as f:
                json.dump(cfg, f, ensure_ascii=False, indent=2)
            executing = False

        elif back_to_menu.clicked():
            menu = True
            settings = False


    if game:
        main_window.blit(background_game, (0,0))
        if not pause:
            player1_g.update()
            player2_g.update()
            ball_g.update(player1_g, player2_g)
        counter1_g.draw(str(player1_g.score))
        counter2_g.draw(str(player2_g.score))
        pause_g.draw()
        menu_g.draw()
        ball_g.draw()
        player1_g.draw()
        player2_g.draw()

        if pause_g.clicked(): pause = not pause

        if player1_g.score < 1 or player2_g.score < 1 or menu_g.clicked():
            menu = True
            game = False
            if player2_g.score < 1:
                player1_menu_score +=1
            elif player1_g.score < 1:
                player2_menu_score += 1

    pg.display.update()
    timer.tick(FPS)