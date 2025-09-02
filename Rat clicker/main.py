import pygame as pg
import random
pg.mixer.pre_init(44100, -16, 2, 2048)
pg.init()

size = width, height = 1280, 720
screen = pg.display.set_mode(size)

bg = pg.image.load("img/bg2.png")
bg_rect = bg.get_rect()

rat = pg.image.load("img/rat.png")
rat = pg.transform.flip(rat, True, False)
rat_rect = rat.get_rect()
rat_rect.x = width / 2 - rat_rect.width 
rat_rect.y = height - rat_rect.height * 1.5
rat_angle = 0

hurt_sound = pg.mixer.Sound("snd/hurt.wav")
hurt_sound.set_volume(0.2)

kick_sound = pg.mixer.Sound("snd/kick.mp3")
kick_sound.set_volume(0.2)

kick_sound2 = pg.mixer.Sound("snd/kick2.mp3")
kick_sound2.set_volume(0.2)

clock = pg.time.Clock()

font = pg.font.SysFont('Arial', 36)
font2 = pg.font.SysFont('Arial', 36)

Running = True
text_value = str(random.randint(0, 10))

crit = False

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

def text_outline(text_value, x, y, color, outline_color, offset):
    text_surface = font.render(text_value, False, outline_color)
    y = y - 30 + abs(rat_angle) / 3
    # text_surface.set_alpha(255 - 243 + abs(rat_angle) * 2.7)
    # Draw outline
    # # # 
    #   #
    # # #
    screen.blit(text_surface, (x - offset, y - offset))
    screen.blit(text_surface, (x, y - offset))          
    screen.blit(text_surface, (x + offset, y - offset))

    screen.blit(text_surface, (x -offset, y)) 
    screen.blit(text_surface, (x + offset, y))
    
    screen.blit(text_surface, (x - offset, y + offset)) 
    screen.blit(text_surface, (x, y + offset))
    screen.blit(text_surface, (x + offset, y + offset))

    # Draw text center
    # # # 
    # x #
    # # #
    text_surface = font.render(text_value, False, color)
    # text_surface.set_alpha(255 - 243 + abs(rat_angle) * 2.7)
    # text_surface.set
    screen.blit(text_surface, (x, y))

while Running:
    screen.fill(pg.Color("BLACK"))
    screen.blit(bg, bg_rect)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            Running = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                Running = False

    mouse_x, mouse_y = pg.mouse.get_pos()[0], pg.mouse.get_pos()[1]
    
    if mouse_x > rat_rect.x and mouse_x < rat_rect.x + rat_rect.width and mouse_y > rat_rect.y and mouse_y < rat_rect.y + rat_rect.height and rat_angle <= 0:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_HAND)
        if pg.mouse.get_just_pressed()[0]:
            # if random.random() > 0.5:
            rat_angle = -90
            # else:
            #     rat_angle = 90
            if random.random() > 0.2:
                crit = False
                font = pg.font.SysFont('Arial', 36)
                font2 = pg.font.SysFont('Arial', 36)
                text_value = str(random.randint(8, 10))
                kick_sound.play()
            else:
                crit = True
                font = pg.font.SysFont('Arial', 64)
                font2 = pg.font.SysFont('Arial', 64)
                text_value = str(random.randint(8, 10)*2)
                kick_sound2.play()
                hurt_sound.play()
    else:
        pg.mouse.set_cursor(pg.SYSTEM_CURSOR_ARROW)


    if not rat_angle == 0:
        if rat_angle < 0:
            rat_angle += 3
        elif rat_angle > 0:
            rat_angle -= 3
        rat_rotated =  pg.transform.rotate(rat, rat_angle)
        rat_rotated_rect = rat_rotated.get_rect(center = (rat_rect.x + rat_rect.width / 2, rat_rect.y+rat_rect.height / 2))
        screen.blit(rat_rotated, rat_rotated_rect)
        
        text_surface = font2.render(text_value, False, black)
        if crit:
            text_outline("CRIT!\n"+text_value, rat_rect.x + rat_rect.width / 2 - text_surface.get_width() / 2, rat_rect.y - rat_rect.height, red, black, 2)
        else:
            text_outline(text_value, rat_rect.x + rat_rect.width / 2 - text_surface.get_width() / 2, rat_rect.y - rat_rect.height, white, black, 2)
    else:
        screen.blit(rat, rat_rect)

    clock.tick(60)
    pg.display.update()
pg.quit()