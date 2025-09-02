import pygame as pg
import numpy as np
from numba import njit

def main():
    pg.init()
    SIZE = WIDTH, HEIGHT = (800, 600)
    screen = pg.display.set_mode(SIZE)
    running = True
    clock = pg.time.Clock()

    H_RES = 120 # horizontal resolution
    HALF_V_RES = 100 # vertical resolution / 2

    MOD = H_RES / 60 # scaling factor (60 deg FOV)
    posx, posy, rot = 0, 0, 0
    frame = np.random.uniform(0, 1, (H_RES, HALF_V_RES * 2, 3))

    sky = pg.image.load("nightbox.png")
    sky = pg.surfarray.array3d(pg.transform.scale(sky, (360, HALF_V_RES * 2)))
    floor = pg.surfarray.array3d(pg.image.load("stone_floor.png"))

    font = pg.font.SysFont("Consolas", 24)
    text_surface = font.render('Compiling. . .', False, (255, 255, 255))
    compiling = True
    frames = 0
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    running = False
       
        if compiling:
            screen.blit(text_surface, (WIDTH //2 - text_surface.width // 2, HEIGHT // 2))
            pg.display.update()
    
        frame, frames = new_frame(posx, posy, rot, frame, sky, floor, H_RES, HALF_V_RES, MOD, frames)
        
        compiling = False

        surf = pg.surfarray.make_surface(frame * 255)
        surf = pg.transform.scale(surf, (800, 600))
        pg.display.set_caption(f"FPS: {int(clock.get_fps())} posx: {posx} posy: {posy} ticks: {pg.time.get_ticks()}")

        screen.blit(surf, (0, 0))
        posx, posy, rot = movement(posx, posy, rot, pg.key.get_pressed(), clock.tick(60))

        if pg.time.get_ticks() < 12000:
            screen.blit(text_surface, (WIDTH //2 - text_surface.width // 2, HEIGHT // 2))
        pg.display.update()


def movement(posx, posy, rot, keys, et):
    rot_speed = 0.001 * et
    move_speed = 0.001 * et
    if keys[pg.K_LEFT] or keys[ord('a')]:
        rot -= rot_speed
        
    if keys[pg.K_RIGHT] or keys[ord('d')]:
        rot += rot_speed
        
    if keys[pg.K_UP] or keys[ord('w')]:
        posx += np.cos(rot) * move_speed
        posy += np.sin(rot) * move_speed
        
    if keys[pg.K_DOWN] or keys[ord('s')]:
        posx -= np.cos(rot) * move_speed 
        posy -= np.sin(rot) * move_speed

    return posx, posy, rot

@njit()
def new_frame(posx, posy, rot, frame, sky, floor, H_RES, HALF_V_RES, MOD, frames):
        for i in range(H_RES):
            rot_i = rot + np.deg2rad(i / MOD - 30)
            sin, cos, cos2 = np.sin(rot_i), np.cos(rot_i), np.cos(np.deg2rad(i / MOD - 30))
            frame[i][:] = sky[int(np.rad2deg(rot_i) % 359)][:] / 255

            for j in range(HALF_V_RES):
                n = (HALF_V_RES / (HALF_V_RES - j)) / cos2
                x = posx + cos * n
                y = posy + sin * n
                xx = int(x * 2 % 1 * len(floor[0]))
                yy = int(y * 2 % 1 * 100)

                shade = 0.2 + 0.8 * (1 - j / HALF_V_RES) 

                frame[i][HALF_V_RES * 2 -  j - 1] = shade * floor[xx][yy] / 255
        frames += 1
        return (frame, frames)

if __name__ == "__main__":
    main()
    pg.quit()
