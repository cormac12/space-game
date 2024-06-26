import math
import pygame
from bullet import Bullet
import globals
from laser import Laser


class Player:
    def __init__(self):
        self.angle = 0



        self.images = {"engine off": pygame.image.load("spaceship off.png"), "engine on": pygame.image.load(
            "spaceship.png")}
        self.image_index = "engine off"
        self.display_image = pygame.transform.rotate(self.images[self.image_index], self.angle)
        self.rect = pygame.Rect(750 - self.display_image.get_width()/2,
                                500 - self.display_image.get_height()/2,
                                self.display_image.get_width(),
                                self.display_image.get_height())
        self.mask = pygame.mask.from_surface(self.display_image)

        self.x = 750
        self.y = 500
        self.vx = 0
        self.vy = 0

        self.health = 1000
        self.mass = 100


        self.energy = 1000
        self.energy_regen = 5
        self.power_off = False

        self.engine_on = False
        self.main_engine_str = .15

        self.laser_on = False
        self.laser = Laser((self.x, self.y), self.angle, 5, (10, 255, 10), 7, -1)

        self.current_weapon = 0


        self.live_rounds = []
        self.fire_rate = 1 # frames per round
        self.last_railgun_time = 0
        self.railgun_cooldown = 30

    def rotate(self, direction, magnitude):
        if direction == "clockwise":
            self.angle -= magnitude

        elif direction == "counterclockwise":
            self.angle += magnitude

        self.angle %= 360
        self.display_image = pygame.transform.rotate(self.images[self.image_index], self.angle)
        self.rect = pygame.Rect(750 - self.display_image.get_width()/2,
                                500 - self.display_image.get_height()/2,
                                self.display_image.get_width(),
                                self.display_image.get_height())

    def accelerate(self):
        self.vy -= math.cos(math.radians(self.angle)) * self.main_engine_str
        self.vx -= math.sin(math.radians(self.angle)) * self.main_engine_str


    def start_engine(self):
        self.engine_on = True
        self.image_index = "engine on"
        self.display_image = pygame.transform.rotate(self.images[self.image_index], self.angle)

    def stop_engine(self):
        self.engine_on = False
        self.image_index = "engine off"
        self.display_image = pygame.transform.rotate(self.images[self.image_index], self.angle)

    def fire_point_defense(self, angle):
        globals.globals_dict["bullets"].append(Bullet(self.x, self.y, self.vx - 5 * math.sin(math.radians(angle)),
                                                      self.vy - 5 * math.cos(math.radians(angle)), (3,3), (255,50,0), 8, -1))

        self.energy -= 7

    def fire_railgun(self, angle):
        globals.globals_dict["bullets"].append(Bullet(self.x, self.y, self.vx - 30 * math.sin(math.radians(angle)),
                                                      self.vy - 30 * math.cos(math.radians(angle)), (5,5), (200,200, 255), 200, -1))
        self.last_railgun_time = globals.globals_dict["frame"]

        self.energy -= 250

    def update(self):
        if self.engine_on:
            self.accelerate()
        self.x += self.vx
        self.y += self.vy
        self.mask = pygame.mask.from_surface(self.display_image)
        self.energy += self.energy_regen
        if self.energy > 1000:
            self.energy = 1000

        if self.engine_on:
            self.energy -= 3
        if self.laser_on:
            self.energy -= 10
        if self.energy <= 0:
            self.power_off = True
        if self.power_off and self.energy >= 500:
            self.power_off = False


    def move(self, offset, angle=None ):
        if type(angle) == None:
            self.x += offset[0]
            self.y -= offset[1]
        else:
            self.x -= math.sin(math.radians(angle)) * offset
            self.y -= math.cos(math.radians(angle)) * offset
        self.rect = pygame.Rect(self.x - globals.globals_dict["camera_pos"][0] - self.display_image.get_width() / 2,
                    self.y - globals.globals_dict["camera_pos"][1] - self.display_image.get_height() / 2, self.display_image.get_width(),
                    self.display_image.get_height())

    def change_velocity(self, offset, angle=None):
        if type(angle) == None:
            self.vx += offset[0]
            self.vy -= offset[1]
        else:
            self.vx -= math.sin(math.radians(angle)) * offset
            self.vy -= math.cos(math.radians(angle)) * offset