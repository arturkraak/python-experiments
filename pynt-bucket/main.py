import pygame as pg
from tkinter import Tk
from tkinter.filedialog import asksaveasfile
Tk().withdraw()

pg.init()

max_height = 1024
canvas = cols, rows = (48, 24) # x, y

mult = max_height // max(canvas)

SIZE = WIDTH, HEIGHT = (cols * mult, rows * mult)
FPS = 60

W = (255, 255, 255)
B = (0, 0, 0)
colors = [W, B]

screen = pg.display.set_mode(SIZE)
clock = pg.time.Clock()
run = True

pixels = [0 if (i + j) % 2 == 0 else 1 for i in range(rows) for j in range(cols)]

x_unit = y_unit = mult
# x_unit = WIDTH // cols
# y_unit = HEIGHT // rows

def bits_to_custom_bytes(pixels: list[int], width: int) -> bytes:
    bytes_data = []
    bits_per_byte = 8
    bytes_per_row = (width + bits_per_byte - 1) // bits_per_byte  # Ceiling division: 16 ÷ 8 = 2 bytes
    
    for row in range(0, len(pixels), width):  # Process each row
        row_bits = pixels[row:row + width]  # Get 16 bits for the row
        row_bytes = []
        
        for byte_idx in range(bytes_per_row):  # Process 2 bytes per row
            byte = 0
            for i in range(8):  # Process 8 bits per byte
                bit_idx = byte_idx * 8 + i
                if bit_idx < width:  # Ensure we don't exceed row width
                    bit = row_bits[bit_idx]
                    byte |= (bit << (7 - i))  # Pack bit into byte (MSB first)
            row_bytes.append(byte)
        bytes_data.extend(row_bytes)
    
    return bytes(bytes_data)

def save_image_as():
    name=asksaveasfile(mode='w', filetypes=[("Portable BitMap (P4)", ".pbm"), ("Portable GrayMap (P5)", ".pgm"), ("Portable Pixmap (P6)", ".ppm")], defaultextension=".pbm")
    if name:
        name.close()
        print(name.name)
        with open(name.name, "wb") as f:
            # Headers
            f.write(f"P4\n{cols} {rows}\n".encode("ascii"))
            # Image Data
            f.write(bits_to_custom_bytes(pixels, cols))  

while run:
    mouse_x, mouse_y = pg.mouse.get_pos()
    # Don't track mouse pos outside of the window
    if mouse_x >= WIDTH:
        mouse_x = WIDTH-1
    if mouse_x < 0:
        mouse_x = 0
    if mouse_y >= HEIGHT:
        mouse_y = HEIGHT-1
    if mouse_y < 0:
        mouse_y = 0
    row_pos = mouse_y // y_unit
    col_pos = mouse_x // x_unit
    pixel_id = row_pos * cols + col_pos
    if pixel_id > len(pixels)-1:
        pixel_id = len(pixels)-1
    if pixel_id < 0:
        pixel_id = 0
    ifo = f"ID={pixel_id} COL={mouse_x // x_unit} ROW={mouse_y // y_unit} PIX={pixels[pixel_id]}"
    pg.display.set_caption(ifo)

    for event in pg.event.get():
        if event.type == pg.QUIT:
            save_image_as()
            run = False
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_ESCAPE:
                save_image_as()
                run = False
            if event.key == pg.K_s:
                save_image_as()
            # Invert color
            if event.key == pg.K_i:
                pixels = [1 if pix == 0 else 0 for pix in pixels]
            # Clear image
            if event.key == pg.K_c:
                pixels = [0 for _ in pixels]

    if pg.mouse.get_pressed()[0]:
        pixels[pixel_id] = 1
    if pg.mouse.get_pressed()[2]:
        pixels[pixel_id] = 0

    for id, p in enumerate(pixels):
        j, i = divmod(id, cols)
        pg.draw.rect(screen, colors[p], (x_unit * i, y_unit * j, x_unit, y_unit))

    pg.display.flip()
    clock.tick(FPS)