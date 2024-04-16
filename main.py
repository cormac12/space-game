import pygame
from player import Player
import globals
from enemy import Enemy
import random

# set up pygame modules
pygame.init()
pygame.font.init()
my_font = pygame.font.SysFont('Arial', 15)
pygame.display.set_caption("Space Fight!")

# set up variables for the display
size = (1500, 1000)
screen = pygame.display.set_mode(size)

name = "Mr. Das"

# render the text for later
display_name = my_font.render(name, True, (255, 255, 255))

# The loop will carry on until the user exits the game (e.g. clicks the close button).
run = True

p = Player()

camera_pos = (0,0)

globals.globals_dict["player_x"] = p.x
globals.globals_dict["player_y"] = p.y

enemies = [Enemy(0, 0, 0, 0), Enemy(100, 100, 0, 0)]

clock = pygame.time.Clock()

# -------- Main Program Loop -----------
while run:

    clock.tick(30)

    keys = pygame.key.get_pressed()

    if keys[pygame.K_d]:
        p.rotate("clockwise")
    if keys[pygame.K_a]:
        p.rotate("counterclockwise")
    if keys[pygame.K_w]:
        p.accelerate()

    p.update_pos()
    # camera_pos = (p.x + p.rect.width/2 - 750, p.y + p.rect.height/2 - 500)
    camera_pos = (p.x - 750, p.y - 500)

    for i in enemies:
        if random.randint(1,1) == 1:
            i.rotate("clockwise")
            i.accelerate()

    for i in enemies:
        i.update_pos()

    # --- Main event loop
    for event in pygame.event.get():  # User did something
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                print("Add in sprite change pls")
        if event.type == pygame.QUIT:  # If user clicked close
            run = False

    display_x = my_font.render(str(camera_pos[0]), True, (255,255,255))
    display_y = my_font.render(str(camera_pos[1]), True, (255,255,255))

    screen.fill((0, 0, 0))
    # ------Blit Zone Start------

    screen.blit(p.display_image, p.rect)

    for i in enemies:
        screen.blit(i.display_image, pygame.Rect(i.x - camera_pos[0] - i.display_image.get_width()/2,
                                                 i.y - camera_pos[1] - i.display_image.get_height()/2, i.display_image.get_width(),
                                                 i.display_image.get_height()))
    screen.blit(display_x, (0, 0))
    screen.blit(display_y, (0, 15))
    # screen.blit(i, (100-p.x, 100-p.y))

    # ------Blit Zone End------

    pygame.display.update()

# Once we have exited the main program loop we can stop the game engine:
pygame.quit()


