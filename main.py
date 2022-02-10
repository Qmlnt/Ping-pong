import pygame as pg

FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_CAPTION = "Ping pong"
WINDOW_ICON_IMG  = "icon.png"
BACKGROUND_IMG = "background.jpg"
BALL_IMG = "ball.png"
BALL_DIMENSIONS = (50,50)
ball_x, ball_y = 300, 200

pg.display.set_caption(WINDOW_CAPTION)
pg.display.set_icon(pg.image.load(WINDOW_ICON_IMG))
main_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pg.transform.scale(pg.image.load(BACKGROUND_IMG), (WINDOW_WIDTH, WINDOW_HEIGHT))

timer = pg.time.Clock()


class GameSprite(pg.sprite.Sprite):
    def __init__(self, image:pg.Surface, x:int, y:int, speed:float=0) -> None:
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.speed = speed
    
    def draw(self):
        main_window.blit(self.image, (self.rect.x, self.rect.y))


ball = GameSprite(pg.transform.scale(pg.image.load(BALL_IMG), BALL_DIMENSIONS), ball_x, ball_y)

executing = True
while executing:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            executing = False

    main_window.blit(background, (0,0))

    ball.draw()

    pg.display.update()
    timer.tick(FPS)