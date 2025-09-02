import pygame
from random import random
pygame.init()

running = True

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)

clock = pygame.time.Clock()

size = WIDTH, HEIGHT = 600, 900

box_width = 30

STRING_HEIGHT = HEIGHT - HEIGHT / 4

draw_box = pygame.Rect(WIDTH / 2 - box_width / 2, STRING_HEIGHT - box_width, box_width, box_width)
init_box = pygame.Rect(WIDTH / 2 - box_width / 2, STRING_HEIGHT - box_width, box_width, box_width)
proj_box = pygame.Rect(WIDTH / 2 - box_width / 2, STRING_HEIGHT - box_width, box_width / 2, box_width / 2)

diff_x, diff_y = 0, 0
velocity_x, velocity_y = 0, 0
gravity = 10
friction = 10
offset_y = 0

channel0 = pygame.mixer.Channel(1)

release_sound = pygame.mixer.Sound("snd/boing.wav")
release_sound.set_volume(0.2)

land_sound = pygame.mixer.Sound("snd/bop.wav")
land_sound.set_volume(0.2)

hit_sound = pygame.mixer.Sound("snd/hit.wav")
hit_sound.set_volume(0.2)

hit_sound2 = pygame.mixer.Sound("snd/hit2.wav")
hit_sound2.set_volume(0.2)

screen = pygame.display.set_mode(size)

grabbed = False
jump = False
release = False

line_width = 2
while running:
    mouse_x = pygame.mouse.get_pos()[0]
    mouse_y = pygame.mouse.get_pos()[1]
    for event in pygame.event.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_x > draw_box.x and mouse_x < draw_box.x + draw_box.width:
                grabbed = True

        if event.type == pygame.MOUSEBUTTONUP:
            if grabbed:
                release = True
                release_sound.play()
                grabbed = False

    if grabbed:
        velocity_x = 0
        velocity_y = 0
        draw_box.x = mouse_x - draw_box.width / 2
        draw_box.y = mouse_y - draw_box.height / 2

        diff_x = draw_box.x - init_box.x
        diff_y = draw_box.y - init_box.y
        velocity_x = diff_x
        velocity_y = diff_y
        proj_box.x = init_box.x - diff_x
        proj_box.y = init_box.y - diff_y
    else:
        draw_box.y -= velocity_y / 10
        draw_box.x -= velocity_x / 10

    # if draw_box.y < STRING_HEIGHT and jump:
    # velocity_x *= 0.1
    # velocity_y *= 0.1
    # if draw_box.y < proj_box.y:
        # velocity_y = 0
    if velocity_y < 0:
        jump = True
    else: jump = False

    if release:
        velocity_y -= 3

    # if draw_box.x > WIDTH - draw_box.width * 2 and draw_box.y < draw_box.height * 2:
    #     running = False

    if draw_box.x < 0 or draw_box.x + draw_box.width > WIDTH:
        # if random() < 0.5:
            
        # else:

        velocity_x = -velocity_x 
        if draw_box.x < 0:
            draw_box.x = 1
            if not grabbed:
                channel0.play(hit_sound2)
                channel0.set_volume(1, 0.1)
                # hit_sound.play()
        if draw_box.x + draw_box.width > WIDTH:
            draw_box.x = WIDTH - draw_box.width - 1
            if not grabbed:
                channel0.play(hit_sound)
                channel0.set_volume(0.1, 1)
                # hit_sound2.play()

    if velocity_y == 150 and not release and draw_box.y < STRING_HEIGHT - draw_box.height:
        draw_box.y = init_box.y
        velocity_y = 0

    if draw_box.y > STRING_HEIGHT - draw_box.height + 1 - velocity_y / 4 and jump:
        land_sound.play()
        velocity_y = 150
        velocity_x = 0
        # draw_box.y = STRING_HEIGHT - draw_box.height
        jump = False
        release = False

    screen.fill(BLACK)
    pygame.draw.rect(screen, WHITE, draw_box)
    if draw_box.y > STRING_HEIGHT - draw_box.height:
        
        pygame.draw.line(screen, GREEN, (0, STRING_HEIGHT), (draw_box.x, draw_box.y + draw_box.height), line_width)
        pygame.draw.line(screen, GREEN, (WIDTH, STRING_HEIGHT), (draw_box.x + draw_box.width, draw_box.y + draw_box.height), line_width)
        pygame.draw.line(screen, GREEN, (draw_box.x, draw_box.y + draw_box.height), (draw_box.x + draw_box.width, draw_box.y + draw_box.height), line_width)
        if grabbed:
            pygame.draw.rect(screen, GREEN, proj_box)
    else:
        pygame.draw.line(screen, GREEN, (0, STRING_HEIGHT), (init_box.x + init_box.width, init_box.y + init_box.height), line_width)
        pygame.draw.line(screen, GREEN, (WIDTH, STRING_HEIGHT), (init_box.x + init_box.width, init_box.y + init_box.height), line_width)

    pygame.display.update()

    clock.tick(60)
    
pygame.quit()