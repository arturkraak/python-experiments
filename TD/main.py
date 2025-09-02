import pygame as pg
from game_object import game_objects
from objects import *
from consts import *

pg.mixer.init()
pg.mixer.set_num_channels(16)  # Increase number of channels (default is 8)

pg.font.init()

attack_sound = pg.mixer.Sound("sound/kick.ogg")
speed_down = pg.mixer.Sound("sound/down.ogg")
speed_down.set_volume(0.2)
speed_up = pg.mixer.Sound("sound/up.ogg")
speed_up.set_volume(0.2)

font = pg.font.SysFont('DejaVu Sans', 48)
screen = pg.display.set_mode(SIZE)
screen.convert_alpha()
clock = pg.time.Clock()
run = True

paused = 0
timer_offset = 0
pause_offset = 0

def init_objects():
    global paused
    paused = 0
    game_objects.clear()
    tower_level = 1
    catle_health = 10
    portal_spawns = 10

    Portal(UNIT,  HEIGHT//2-UNIT, UNIT, UNIT*2, portal_spawns, PURPLE)
    Castle(WIDTH-UNIT*2, HEIGHT//2-UNIT, UNIT, UNIT*2, catle_health, WHITE)
    Tower(WIDTH//2-UNIT//2, HEIGHT//2+UNIT*2, UNIT, UNIT, tower_level, GREEN, attack_sound, 1000)

buttons = []
class Button:
    def __init__(self, name, x, y, w, h, text, color):
        self.name = name
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.text = text
        self.color = color
        self.hover = False
        buttons.append(self)
    
    def draw(self, surf):
        pg.draw.rect(screen, self.color, (self.x, self.y-UNIT//2, self.w, self.h))
        surf.blit(self.text, (self.x+self.w//2-self.text.get_width()//2, self.y-UNIT//2))
     
    def update(self, mouse_pos):
        if pg.Rect(self.x, self.y-UNIT//2, self.w, self.h).collidepoint(mouse_pos):
            self.color = LIGHTGRAY
            self.hover = True
            if pg.mouse.get_pressed()[0]:
                self.color = DARKGRAY
        else:
            self.color = GRAY
            self.hover = False

Button("+", UNIT*3.5, HEIGHT-UNIT-UNIT//2, UNIT, UNIT, font.render("+", True, WHITE), GRAY)
Button("-", UNIT*5, HEIGHT-UNIT-UNIT//2, UNIT, UNIT, font.render("-", True, WHITE), GRAY)

init_objects()

while run:
    for event in pg.event.get():
            if event.type == pg.QUIT:
                run = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE:
                    run = False
                if event.key == pg.K_SPACE:
                    if paused:
                        paused = 0
                    else:
                        paused = 1
            if event.type == pg.KEYUP:
                if event.key == pg.K_r:
                    # Restart level   
                    init_objects()
            if event.type == pg.MOUSEBUTTONUP:
                for button in buttons:
                    if button.hover and pg.mouse.get_just_released()[0]:
                        if button.name == "+":
                            speed_up.play()
                        if button.name == "-":
                            speed_down.play()
                        for tower in [t for t in game_objects if type(t) is Tower]:
                            if button.name == "+":
                                tower.delay += 100
                            elif button.name == "-":
                                tower.delay -= 100
    if not paused and run:
        if pause_offset:
            timer_offset = pause_offset
        screen.fill(BLACK)
        pg.draw.rect(screen, DARKGREEN, (0,  HEIGHT//2-UNIT*2, UNIT*20, UNIT*20))

        ticks = pg.time.get_ticks() - timer_offset
        for go in game_objects:
            if type(go) is Creep:
                go.update()
            elif type(go) is Portal:
                go.update(ticks)
            elif type(go) is Tower:
                paused, tower_surf = go.update(ticks, paused)  
                text = font.render(str(go.delay), True, WHITE)
                screen.blit(text, (UNIT, HEIGHT-text.get_height()-UNIT))
            elif type(go) is Castle:
                go.update()
            
            go.draw(screen) 
        screen.blit(tower_surf)
        for button in buttons:
            button.draw(screen)
            button.update(pg.mouse.get_pos())  

        pg.display.flip()
        time = pg.time.get_ticks()
    else:
        pause_offset = timer_offset + pg.time.get_ticks() - time
        # print(pause_offset)
    clock.tick(FPS)
