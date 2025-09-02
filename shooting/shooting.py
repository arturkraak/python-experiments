import pygame
import math

pygame.init()
pygame.mixer.init()
pygame.mixer.set_num_channels(8)

fire = pygame.mixer.Sound('snd/shot.ogg') 
hit = pygame.mixer.Sound('snd/impact.ogg')
equip = pygame.mixer.Sound('snd/buttonclickrelease.wav')

volume = 0.2
fire.set_volume(volume)
hit.set_volume(volume)
equip.set_volume(volume)

size = WIDTH, HEIGHT = (1280, 720)
screen = pygame.display.set_mode(size)

clock = pygame.time.Clock()
border = pygame.Rect(0, 0, WIDTH, HEIGHT)

HALF_WIDTH = WIDTH // 2
HALF_HEIGHT = HEIGHT // 2
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
COLORS = [WHITE, GREEN, RED] 

gun_speeds = [500, 250, 1]

class Player():
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.speed = 5
        self.cooldown = 0
        self.gun_cd = 1000 # gun cooldown in ticks
        self.gun_iterator = 0
        self.trace_bullets = True

    def update(self):
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        return False
                    if event.key == pygame.K_TAB:
                        self.trace_bullets = not self.trace_bullets
                    if event.key == pygame.K_1:
                        self.gun_iterator = 0
                        equip.stop()
                        equip.play()
                    if event.key == pygame.K_2:
                        self.gun_iterator = 1
                        equip.stop()
                        equip.play()
                    if event.key == pygame.K_3:
                        self.gun_iterator = 2
                        equip.stop()
                        equip.play()
                    if event.key == pygame.K_c:
                        global bullets
                        bullets = []
                    if event.key == pygame.K_q:
                        self.gun_iterator += 1
                        equip.stop()
                        equip.play()
                        if self.gun_iterator >= len(gun_speeds):
                            self.gun_iterator = 0
                        
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.cooldown = pygame.time.get_ticks() + self.gun_cd
                    Bullet((self.x, self.y), pygame.mouse.get_pos())
                    fire.play()
            self.gun_cd = gun_speeds[self.gun_iterator]
            move_x = 0
            move_y = 0
            key = pygame.key.get_pressed()
            if key[pygame.K_w]:
                move_y = -1 * self.speed
            if key[pygame.K_s]:
                move_y = 1 * self.speed
            if key[pygame.K_a]:
                move_x = -1 * self.speed
            if key[pygame.K_d]:
                move_x = 1 * self.speed

            if pygame.mouse.get_pressed()[0] and self.cooldown < pygame.time.get_ticks():
                self.cooldown = pygame.time.get_ticks() + self.gun_cd
                Bullet((self.x, self.y), pygame.mouse.get_pos())
                fire.play()

            if move_x and move_y:
                self.x += move_x * 0.7
                self.y += move_y * 0.7  # / 1.41421
            else:
                self.x += move_x 
                self.y += move_y

            self.draw()
            return True
    
    def draw(self):
        pygame.draw.rect(screen, (50, 50, 50), (self.x, self.y, 20, 20))
        # DRAW GUN
        ## in pygame draw a line of fixed length rotating towards the mouse
        # Get mouse position
        mouse_x, mouse_y = pygame.mouse.get_pos()

        # Calculate the angle between the line and the mouse position
        angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

        gun_length = 25 * (self.gun_iterator + 1)

        # Calculate the end point of the line
        end_x = self.x + gun_length * math.cos(angle)
        end_y = self.y + gun_length * math.sin(angle)

        # Draw line
        pygame.draw.line(screen, COLORS[self.gun_iterator], (self.x, self.y), (end_x, end_y), 2)

bullets = []
class Bullet():
    def __init__(self, pos, target):
        self.x = pos[0]
        self.y = pos[1]
        self.speed = 100
        self.is_moving = True
        self.rect = pygame.Rect(pos[0], pos[1], 10, 10)
        dist_x, dist_y = target[0] - pos[0], target[1] - pos[1]
        total_dist = math.sqrt(dist_x**2 + dist_y**2)
        if total_dist != 0:
            mult = self.speed / total_dist
            self.speed_x = dist_x * mult
            self.speed_y = dist_y * mult
        bullets.append(self)

    def update(self):
        if self.is_moving:
            self.x += self.speed_x
            self.y += self.speed_y
            # If the bullet hits an enemy
            for enemy in enemies:
                entry_point = enemy.rect.clipline((self.x-self.speed_x, self.y-self.speed_y), (self.x, self.y))
                if len(entry_point) == 2:
                    self.x, self.y = entry_point[0]
                    self.is_moving = False
                    hit.play() 
            # If the bullet hits the edge of the screen
            if self.x > WIDTH or self.x < 0 or self.y > HEIGHT or self.y < 0:
                exit_point = border.clipline((self.x-self.speed_x, self.y-self.speed_y), (self.x, self.y))
                if len(exit_point) == 2:
                    self.x, self.y = exit_point[1]
                self.is_moving = False
                hit.play()
        self.draw()

    def draw(self):
        if player.trace_bullets:
            pygame.draw.line(screen, (255, 0, 0), (self.x-self.speed_x, self.y-self.speed_y), (self.x, self.y))
        self.rect = pygame.Rect(self.x, self.y, 1, 1)
        pygame.draw.rect(screen, (0, 255, 0), self.rect)

enemies =[]
class Enemy():
    def __init__(self, rect):
        self.rect = pygame.Rect(rect)
        enemies.append(self)

    def update(self):
        self.draw()

    def draw(self):
        pygame.draw.rect(screen, (255, 255, 255), self.rect, 1, 1)

enemy = Enemy((HALF_WIDTH + 100, HALF_HEIGHT - 100, 10, 200))
player = Player(HALF_WIDTH, HALF_HEIGHT)
running = True
while running:
    screen.fill((0,0,0))

    for enemy in enemies:
        enemy.update()

    for bullet in bullets:
        bullet.update()

    running = player.update()

    pygame.display.set_caption(f"FPS: {clock.get_fps()} | Bullets: {len(bullets)}")
    pygame.display.flip()
    clock.tick(60)