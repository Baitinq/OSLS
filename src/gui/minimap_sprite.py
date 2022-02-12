import math

import pygame
from pygame.locals import *

from simulation import Simulation

class Sprite_Minimap(pygame.sprite.Sprite):
    def __init__(self, simulation: type[Simulation], radius: int):
        super().__init__()
        self.simulation = simulation
        self.radius = radius

    def update(self, display_width, display_height):
        self.image = pygame.Surface([self.radius * 2, self.radius * 2], pygame.SRCALPHA)

        #body
        pygame.draw.circle(self.image, (0, 255, 0), (self.radius, self.radius), self.radius, width=2)
        
        #rocket position (TODO, show actual position in relation to surface. allow zoom?)
        normalized_x = math.sin(math.radians(self.simulation.angle_of_position_with_respect_to_origin())) * (self.radius)
        normalized_y = math.cos(math.radians(self.simulation.angle_of_position_with_respect_to_origin())) * (self.radius)
        normalized_rocket_pos = [self.radius + normalized_x, self.radius - normalized_y]
        pygame.draw.circle(self.image, (255, 0, 0), normalized_rocket_pos, 4)

        self.rect = self.image.get_rect()
        self.rect.topright = [display_width, 0]