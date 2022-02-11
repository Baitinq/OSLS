from random import randint

import pygame
from pygame.locals import *

from simulation import Simulation

class Sprite_Background(pygame.sprite.Sprite):
    def __init__(self, simulation: type[Simulation]):
        super().__init__()
        self.simulation = simulation

    def update(self, display_width, display_height):
        self.image = pygame.Surface([display_width, display_height])

        #TODO: put into its own functions drawBg() drawStars()
        self.image.fill(self.get_color_for_height(self.simulation.rocket_altitude()))
        
        #draw stars, TODO: should be its own sprite and speed should actually matter
        if self.simulation.rocket_altitude() > 30000:
            for _ in range(100):
                self.image.set_at((randint(0, display_width), randint(0, display_height)), (255, 255, 255))
        
        self.rect = self.image.get_rect()

    def linear_gradient(self, start_color, end_color, length, value_at):
        return [
            int(start_color[j] + (float(value_at)/(length-1))*(end_color[j]-start_color[j]))
            for j in range(3)
        ]

    def get_color_for_height(self, height: float) -> (int, int, int):
        if height < 70000:
            return self.linear_gradient((31,118,194), (0, 0, 0), 70000, int(height))
        else:
            return (0, 0, 0)