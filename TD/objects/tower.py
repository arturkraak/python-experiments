from game_object import GameObject, game_objects
from objects.creep import Creep
import math
from consts import *
from pygame import draw, surface

class Tower(GameObject):
    def __init__(self, x, y, w, h, hp, color, attack_sound, delay = 2000):
        super().__init__(x, y, w, h, hp, color)
        self.delay = delay
        self.shoot_delay = self.delay
        self.attack_sound = attack_sound
        self.range = UNIT * 3 + 7
        self.surf = surface.Surface(SIZE)
        self.surf.fill(CLEAR)
        self.surf.set_colorkey(BLACK)
        # self.surf.set_alpha(50)

    def distance_between_target(self, x1, y1, x2, y2):
        return math.sqrt((x1-x2)**2 + (y1-y2)**2)

    def draw(self, screen):
        draw.circle(screen, MEDIUMGREEN, (self.x+self.w//2, self.y+self.h//2), self.range)
        super().draw(screen)
        
    def shoot_target(self, hit, color, width = 1):
        # print(hit)
        if type(hit) is tuple:
            draw.line(self.surf, color, (self.x+self.w//2, self.y+self.h//2), hit, width)

    def in_range(self, creep):
        points = [(creep.x, creep.y), (creep.x+creep.w, creep.y), (creep.x, creep.y+creep.h), (creep.x+creep.w, creep.y+creep.h)]
        distance = {}
        for point in points:
            distance[self.distance_between_target(self.x+self.w//2, self.y+self.h//2, point[0], point[1])] = point
        shortest = min(distance.keys())
        if shortest < self.range: # 1 1
            res = distance[shortest]
            self.shoot_target(res, WHITE)
            return res

        return False
    
    def update(self, ticks, paused):
        self.surf.fill(CLEAR)
        creeps = [x for x in game_objects if type(x) is Creep]
        for creep in creeps:
            hit = self.in_range(creep)
            if hit and ticks > self.shoot_delay:
                    print(hit)
                    paused = 1
                    self.attack_sound.play()
                    self.shoot_target(hit, RED, 10)
                    creep.damage(1)
                    self.shoot_delay = ticks + self.delay
        return (paused, self.surf)