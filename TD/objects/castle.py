from game_object import GameObject
import pygame.mixer
pygame.mixer.init()
collapse = pygame.mixer.Sound("sound/explode.ogg")
collapse.set_volume(0.2)

class Castle(GameObject):
    def __init__(self, x, y, w, h, hp, color):
        super().__init__(x, y, w, h, hp, color)

    def update(self):
        col = round(self.hp * 255 / 10)
        self.color = (col, col, col)

    def damage(self, dmg):
        self.hp -= dmg
        if self.hp < 1:
            collapse.play()
        super().update()