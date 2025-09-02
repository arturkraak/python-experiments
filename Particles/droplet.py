import pygame as pg
import random
pg.init()

fullscreen = False

size = width, height = 1280, 720

if fullscreen:
    size = width, height = 1920, 1080

flags = pg.NOFRAME
screen = pg.display.set_mode(size, flags)

def draw_circle_alpha(surface, color, center, radius):
    target_rect = pg.Rect(center, (0, 0)).inflate((radius * 2, radius * 2))
    shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
    pg.draw.circle(shape_surf, color, (radius, radius), radius)
    surface.blit(shape_surf, target_rect)

pg.mouse.set_visible(False)
# Setup a drawing surface with alpha
draw_surf = pg.Surface(size, pg.SRCALPHA)

bubble_list = []

color_list = []
for c in pg.color.THECOLORS.values():
    color_list.append(c)

class Bubble():

    def __init__(self, x, y, r, color):
        self.x = x
        self.y = y 
        self.radius = 0
        self.color_r, self.color_g, self.color_b, self.alpha = color
        self.increase_radius = 1.5
        self.color = color
        self.alpha = 50
        bubble_list.append(self)

    def draw(self):
        if self.alpha > 0:
            draw_circle_alpha(screen, (self.color_r, self.color_b, self.color_g, self.alpha), (self.x, self.y), self.radius)
            self.radius += self.increase_radius
            self.alpha -= 1
            if self.radius < self.increase_radius+1:
                self.color_r *= ( (height - self.y) / height )
                self.color_b *= ( (height - self.y) / height )
                self.color_g *=  ( (height - self.y) / height )
        else:
            bubble_list.remove(self)

clock = pg.time.Clock()
running = True
demo = False
INIT_COLOR = (255, 255, 255, 255)

bubble_spawner_list = []
class Bubble_spawner():

    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.rx = width / 2
        self.ry = height / 2
        self.sx = 1
        self.sy = 1
        self.r = 1
        self.color = (255, 255, 255, 255)
        bubble_spawner_list.append(self)

    def update(self):
        if demo:
            if self.x < self.rx:
                self.x += self.sx
            if self.x > self.rx:
                self.x -= self.sx
            if self.y < self.ry:
                self.y += self.sy
            if self.y > self.ry:
                self.y -= self.sy
            if self.x - self.sx < self.rx and self.x + self.sx > self.rx:
                if self.y - self.sy < self.ry and self.y + self.sy > self.ry:
                    self.rx = random.randint(0, width)
                    self.ry = random.randint(0, height)
                    #self.r = random.randint(2, 8)
                    self.color = random.choice(color_list)
            Bubble(self.x, self.y, 1, self.color)
            self.sx = random.randint(-1, 4)
            self.sy = random.randint(-1, 4)

while running:

    for event in pg.event.get():
        if event.type == pg.KEYDOWN:
            # Toggle fullscreen
            if event.key == pg.K_F11:
                fullscreen = not fullscreen
                if fullscreen:
                    size = width, height = 1920, 1080
                    screen = pg.display.set_mode(size, flags)
                    pg.display.set_window_position((0, 0))
                else:
                    size = width, height = 1280, 720
                    screen = pg.display.set_mode(size, flags)
                    pg.display.set_window_position((1920 / 2 - width / 2, 1080 / 2 - height / 2))
            # Toggle demo
            if event.key == pg.K_SPACE:
                demo = not demo
            # Quit game
            if event.key == pg.K_ESCAPE:
                running = False  
        if event.type == pg.QUIT:
            running = False
    screen.fill((0, 0, 0))
    for i in range(height):
       pg.draw.rect(screen, (0, 0, (height - i) / 5), pg.Rect(0, i, width, 1))
    draw_surf.fill(pg.Color('#00000000'))

    # Spawn bubble on left click
    if pg.mouse.get_just_pressed()[0]:
        new_bubble = Bubble(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 1, INIT_COLOR)

    # Right click to add a new spawner
    if pg.mouse.get_just_pressed()[2]:
        new_spawner = Bubble_spawner(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1])
   
    # Spawn bubble per frame at mouse coordinates
    new_bubble = Bubble(pg.mouse.get_pos()[0], pg.mouse.get_pos()[1], 1, INIT_COLOR)

    for bs in bubble_spawner_list:
        bs.update()

    for b in bubble_list:
        b.draw()

    # special_flags = pg.BLEND_ALPHA_SDL2
    # screen.blit(draw_surf, (0, 0), (0, 0, width, height), special_flags)

    pg.display.update()
    print(pg.Clock.get_fps(clock))
    # print((height - pg.mouse.get_pos()[1]) / height)
    clock.tick(120)
pg.quit()
