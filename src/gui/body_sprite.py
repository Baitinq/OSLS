import pygame
from pygame.locals import *

from simulation import Simulation
from body import Body

class Sprite_Body(pygame.sprite.Sprite):
    def __init__(self, simulation: type[Simulation], floor: int):
        super().__init__()
        self.simulation = simulation
        self.body = self.simulation.body
        self.floor = floor

    def update(self, display_width, display_height):
        draw_height = self.floor
        rocket_altitude = self.simulation.rocket_altitude()
        body_radius = self.body.radius
        
        #draw circle, but in fixed point, not screen
        self.image = pygame.Surface([display_width, draw_height], pygame.SRCALPHA)
        self.image.fill((0, 155, 155))

        top_of_floor = display_height - draw_height + rocket_altitude
        #print("Top of floor: " + str(top_of_floor))
        
        self.rect = self.image.get_rect()
        self.rect = [0, top_of_floor]