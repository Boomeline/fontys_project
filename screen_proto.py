import pygame as pg 
import sys
from grid_cell import Cell
from robot import Robot 
from camara import Track

pg.init()


width = 900
height = 650
scale = 50
grid = [] 
display = pg.display.set_mode((width, height), pg.RESIZABLE)
# pg.display.toggle_fullscreen()

for y in range(int(height / scale)):
    for x in range(int(width / scale)):
        grid.append(Cell(scale, x, y))

robot = Robot(0, 0)
tracker = Track()
cam_width = tracker.width
cam_height = tracker.height

clock = pg.time.Clock()

while True:

    # clock.tick(60)
    # fps = clock.get_fps()
    # print(fps)

    display.fill((255,255,255))
  
    # pg.draw.rect(display,(0,0,255),(200,150,100,50))  

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            sys.exit()
        # if event.type == pg.KEYDOWN:    
        #     if event.key == pg.K_ESCAPE:
        #         pg.quit()
        #         sys.exit()
        #     robot.move(event.key)

    marker_id, center_x, center_y = tracker.cam()
    if marker_id is not None:
        world_x = center_x * (width / cam_width) * -1 + width
        world_y = center_y * (height / cam_height)* -1 + height
        robot.update_position(world_x, world_y)

    for cell in grid:
        rec = pg.Rect(cell.x * scale + ((pg.display.get_window_size()[0] - width) // 2), cell.y * scale + ((pg.display.get_window_size()[1] - height) // 2), cell.size, cell.size)
        pg.draw.rect(display, (0, 0, 0), rec, 1)
        robot.draw(display)


    pg.display.flip()
    



