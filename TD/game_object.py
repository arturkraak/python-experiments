game_objects = []
from consts import WHITE, RED
from pygame import font, draw
font.init()
my_font = font.SysFont('DejaVu Sans', 48)

class GameObject:
    def __init__(self, x, y, w, h, hp, color):
        self.self = self
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.hp = hp
        self.last_hp = hp
        self.color = color
        self.text_color = WHITE
        self.color_speed = 6
        game_objects.append(self)
    
    def draw(self, surf):
        draw.rect(surf, self.color, (self.x, self.y, self.w, self.h))
        if self.last_hp != self.hp:
            self.text_color = RED
        if self.text_color[1] + self.color_speed < 255:
            self.text_color = (255, self.text_color[1] + self.color_speed, self.text_color[2] + self.color_speed)
        else:
            self.text_color = WHITE

            
        text = my_font.render(str(self.hp), True, self.text_color)
        surf.blit(text, (self.x+self.w//2-text.get_width()//2, self.y-text.get_height()))
        self.last_hp = self.hp

    def update(self):
        if self.hp < 1:
            game_objects.remove(self)