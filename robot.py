import pygame as pg
import time

class Robot():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.last_move_time  = 0
        self.move_delay = 0.5

    def draw(self, display):
        image = pg.image.load(r"C:\Users\s162010061001\OneDrive - Ons Middelbaar Onderwijs\fontys_project\sources\robot.png").convert()
        display.blit(image,(self.x, self.y))

    # def move(self, event):
    #     now = time.time()
    #     if now - self.last_move_time < self.move_delay:
    #         return

    #     keys = pg.key.get_pressed()

    #     if keys[pg.K_w] or keys[pg.K_UP]:  
    #         self.y -= 3
    #     if keys[pg.K_s] or keys[pg.K_DOWN]:
    #         self.y += 3
    #     if keys[pg.K_a] or keys[pg.K_LEFT]:
    #         self.x -= 3
    #     if keys[pg.K_d] or keys[pg.K_RIGHT]:
    #         self.x += 3 
    #     print(self.x, self.y)

    #     self.last_move_time = now
    #     return 

    def update_position(self, x, y):
        self.x = x
        self.y = y