import pygame as pg

FPS = 60
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 500
WINDOW_ICON  = "icon.png"
WINDOW_CAPTION = "Ping pong"
BACKGROUND_IMG = "background.jpg"

pg.display.set_caption(WINDOW_CAPTION)
pg.display.set_icon(pg.image.load(WINDOW_ICON))
main_window = pg.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
background = pg.transform.scale(pg.image.load(BACKGROUND_IMG), (WINDOW_WIDTH, WINDOW_HEIGHT))

timer = pg.time.Clock()

executing = True
while executing:

    for e in pg.event.get():
        if e.type == pg.QUIT:
            executing = False

    main_window.blit(background, (0,0))



    pg.display.update()
    timer.tick(FPS)