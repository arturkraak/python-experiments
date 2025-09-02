from game_object import GameObject, game_objects
from objects.castle import Castle
import pygame.mixer
pygame.mixer.init()

damage_sound = pygame.mixer.Sound("sound/clock.wav")
spawn_sound = pygame.mixer.Sound("sound/pop.ogg")

def find_castle():
    for go in game_objects:
        if type(go) is Castle:
            return go
        
class Creep(GameObject):    
    def __init__(self, x, y, w, h, hp, color, speed=2):
        super().__init__(x, y, w, h, hp, color)
        self.to_castle = find_castle()
        self.speed = speed
        spawn_sound.play()

    def update(self):
        if self.x < self.to_castle.x - self.w:
            self.x += self.speed
        else:
            self.to_castle.damage(1)
            damage_sound.play()
            self.hp = 0
            super().update()

    def damage(self, dmg):
        self.hp -= dmg
        super().update()