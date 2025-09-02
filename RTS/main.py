import pygame

pygame.init()

block_width = 128
speed = 4

id = 0

def get_id():
    global id
    id += 1
    return id

object_events = []

class GameObject:
    
    def __init__(self, name, x, y, hp = 5):
        width = block_width
        height = block_width
        collisions = False

        objectImage = pygame.image.load("img/"+name+".png")
        self.name = name
        self.hp = hp
        self.image = pygame.transform.scale(objectImage, (width, height))
        self.x = x * width
        self.y = y * height
        self.width = width
        self.height = height
        self.collisions = collisions
        self.tx = self.x
        self.ty = self.y
        self.move_h = False
        self.move_v = False
        self.action = "idle"
        self.id = get_id()
        self.inventory = []
        self.target_object = None
        self.occupation = None

    def draw(self, surface, x_offset = 0, y_offset = 0):
        surface.blit(self.image, (self.x + x_offset, self.y + y_offset))

    def update(self):
        if self.x + speed < self.tx:
            self.x += speed
            self.move_h = True
        elif self.x - speed > self.tx:
            self.x -= speed
            self.move_h = True
        else:
            self.move_h = False

        if self.y - speed > self.ty:
            self.y -= speed
            self.move_v = True
        elif self.y + speed < self.ty:
            self.y += speed
            self.move_v = True
        else:
            self.move_v = False

        if self.move_h or self.move_v:
            pass
            # self.action = "walking"
        else:
            if self.action != "gathering":
                if self.action == "depositing":
                    self.inventory = []
                    self.action = "walking"
                else:
                    self.action = "idle"
            if self.target_object != None:
                self.tx = self.target_object.x
                self.ty = self.target_object.y

                if self.collision():
                    if self.action != "gathering":
                        self.action = "gathering"
                        self.gather()
        
    def collision(self, obj = None):
        if obj == None:
            obj = self.target_object
        if self.y > obj.y + obj.height:
            return False
        elif self.y + self.height < obj.y:
            return False
        
        if self.x > obj.x + obj.width:
            return False
        elif self.x + self.width < obj.x:
            return False

        # if self.collisions and obj.collisions:
        return True 

    def gather(self):
        if self.action == "gathering":
            NEW_EVENT = pygame.USEREVENT + self.id
        
            if not NEW_EVENT in object_events:
                object_events.append(NEW_EVENT)
                pygame.time.set_timer(NEW_EVENT, 1000)
                if len(self.inventory) < 5:
                    sound.play()
                    self.inventory.append(self.target_object.name)
                    self.target_object.hp -= 1
                    if self.target_object.hp < 1:
                        objects.remove(self.target_object)
                        self.target_object = None
                        self.deposit()
                else:
                    print("inventory full")
                    self.deposit()

    def deposit(self):
        for o in objects:
            if o.name == "hut":
                self.tx = o.x
                self.ty = o.y
                self.action = "depositing"

selected_object = None

font_arial = pygame.font.SysFont("Arial", 20)

size = width, height = 1280, 720

black = (0, 0, 0)
red = (255, 0, 0)
gray = (50, 50, 50)
clear = (0, 0, 0, 0)
white = (255, 255, 255)
green = (0, 255, 0, 200)
light_gray = (100, 100, 100)
alpha_green = (0, 255, 0, 50)
x_offset = -580
y_offset = -370

map_width = 21
map_height = 13


scroll_speed = 10
selected_text = "None"
screen = pygame.display.set_mode(size)

# Setup a drawing surface with alpha
draw_surf = pygame.Surface(size, pygame.SRCALPHA)
draw_surf.fill(pygame.Color('#00000000'))


selected_image = None
# images = [grass_img, tree_img, birch_img, rocks_img, hut_img, man_img]

# Objects
rocks_object = GameObject("rocks", 7, 5)
birch_object = GameObject("birch", 11, 5)
birch_object = GameObject("birch", 11, 5)
tree_object = GameObject("tree", 9, 3)
hut_object = GameObject("hut", 9, 5)
man_object = GameObject("man", 9, 6)

objects = []
objects.append(rocks_object)
objects.append(birch_object)
birch_object = GameObject("birch", 11, 4)
objects.append(birch_object)
birch_object = GameObject("birch", 12, 5)
objects.append(birch_object)
objects.append(tree_object)
objects.append(hut_object)
objects.append(man_object)

select_box = pygame.Rect(0, 0, 0, 0)
initpoint = pygame.Rect(0, 0, 0, 0)

ui_box = pygame.Rect(0, height-150, width, 150)

sound = pygame.mixer.Sound("sounds/3037.wav")
sound.set_volume(0.2)


clock = pygame.time.Clock()

run = True

# Generate Map
map = []
i = 0
j = 0
while j < map_height + 1:
    while i < map_width + 1:
        grass_object = GameObject("grass", i, j)
        map.append(grass_object)
        i += 1
    j+=1
    i=0

while run:    
    for event in pygame.event.get():
        for oe in object_events:
            if event.type == oe:
                for o in objects:
                    if o.id == oe - pygame.USEREVENT:
                        if o.target_object != None:
                            print("gathering "+ o.target_object.name)
                            pygame.time.set_timer(oe, 0)
                            object_events.remove(oe)
                            o.gather()
                            break

        mouse_x, mouse_y = pygame.mouse.get_pos() 

        # Start selection
        if event.type == pygame.MOUSEBUTTONDOWN:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
            pygame.event.set_grab(True)
            # print(pygame.mouse.get_pos())
            initpoint.x = pygame.mouse.get_pos()[0]
            initpoint.y = pygame.mouse.get_pos()[1]
            select_box.x = initpoint.x
            select_box.y = initpoint.y
            select_box.width = 0
            select_box.height = 0

        # End selection
        elif event.type == pygame.MOUSEBUTTONUP:
            pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            # print(pygame.mouse.get_pos())
            select_box.width = 0
            select_box.height = 0

        # Quit game
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
        if event.type == pygame.QUIT:
            run = False

    # Press right mouse button to issue a command to a unit
    if pygame.mouse.get_just_released()[2]:
        if selected_object != None:
            selected_object.tx = mouse_x - x_offset - selected_object.width / 2
            selected_object.ty = mouse_y - y_offset - selected_object.height / 2
            # Select Object
            selected_object.target_object = None
            for o in objects:
                if mouse_x < o.x + o.width + x_offset and mouse_x > o.x + x_offset and mouse_y > o.y + y_offset and mouse_y < o.y + o.height + y_offset:
                    # if o.type == "resource":
                    if o.name == "hut":
                        selected_object.deposit()
                    else:
                        selected_object.target_object = o
                    # selected_object.gather()
                    break
            if selected_object.target_object == None and selected_object.action == "idle":
                selected_object.action = "walking"
        # pygame.event.set_grab(False)


    # Update select box when mouse is held down
    if pygame.mouse.get_pressed()[0]:
        if initpoint.x > mouse_x:
            select_box.x = mouse_x
            select_box.width = abs(initpoint.x - mouse_x)
        elif initpoint.x < mouse_x:
            select_box.x = initpoint.x
            select_box.width = abs(initpoint.x - mouse_x)
        if initpoint.y > mouse_y:
            select_box.y = mouse_y
            select_box.height = abs(initpoint.y - mouse_y)
        elif initpoint.y < mouse_y:
            select_box.y = initpoint.y
            select_box.height = abs(initpoint.y - mouse_y)
    
    # Release left mouse button to select obejct
    if pygame.mouse.get_just_released()[0]:
        # Select Object
        for o in objects:
            if mouse_x < o.x + o.width + x_offset and mouse_x > o.x + x_offset and mouse_y > o.y + y_offset and mouse_y < o.y + o.height + y_offset:
                selected_text = o.name
                selected_image = o.image
                selected_object = o
                break
            else:
                selected_text = "None"
                selected_object = None


    # Scroll map using offset
    if pygame.event.get_grab():
        if mouse_x < 2 and x_offset < block_width:
            x_offset += scroll_speed
        if mouse_x > width-2 and x_offset - scroll_speed > -map_width * block_width + width - block_width * 2:
            x_offset -= scroll_speed
        if mouse_y < 2 and y_offset < block_width:
            y_offset += scroll_speed
        if mouse_y > height-2 and y_offset > -map_height * block_width + height - block_width * 2 -ui_box.height:
            y_offset -= scroll_speed

    # Refresh surfaces
    screen.fill(black)       
    draw_surf.fill(clear)
    
    # Draw selection box
    pygame.draw.rect(draw_surf, alpha_green, select_box)
    pygame.draw.rect(draw_surf, green, select_box, 2)
    
    # # Draw map
    for grass_block in map:
        grass_block.draw(screen, x_offset, y_offset)

    # Draw at cursor pos
    # screen.blit(dark_grass, pygame.mouse.get_pos())

    # Draw objects
    for o in  sorted( objects, key = lambda x : x.y ):
        o.draw(screen, x_offset, y_offset)
        if o.name == "man":
            o.update()

    # UI
    pygame.draw.rect(draw_surf, gray, ui_box)
    text = font_arial.render(selected_text.capitalize(), True, white)
    fps_text = font_arial.render(str(round(clock.get_fps())), True, white)
    draw_surf.blit(text, (ui_box.x + 50, ui_box.y + 20))
    draw_surf.blit(fps_text, (ui_box.x + 500, ui_box.y + 20))
    pygame.draw.rect(draw_surf, light_gray, (ui_box.x + 50, ui_box.y + 50, 64, 64))
    if selected_text != "None":
        selected_image = pygame.transform.scale(selected_image, (64, 64))
        draw_surf.blit(selected_image, (ui_box.x + 50, ui_box.y + 50))
        if selected_text == "man":
            text = font_arial.render(selected_object.action + " " + str(selected_object.inventory), True, white)
            draw_surf.blit(text, (ui_box.x + 50, ui_box.y + 120))
    screen.blit(draw_surf, (0, 0))
    
    pygame.display.update()
    clock.tick(60)
    # print(clock.get_fps())