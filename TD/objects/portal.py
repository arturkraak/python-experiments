from game_object import GameObject
from objects.creep import Creep
from consts import RED

class Portal(GameObject):
    def __init__(self, x, y, w, h, hp, color, delay = 2500):
        super().__init__(x, y, w, h, hp, color)
        self.delay = delay
        self.spawn_delay = 0

    def update(self, ticks):
        if self.hp > 0:
            if ticks > self.spawn_delay:
                Creep(self.x+self.w, self.y+self.h//2, self.w//2, self.h//2, 3, RED)
                self.spawn_delay = ticks + self.delay
                self.hp -= 1
                super().update()