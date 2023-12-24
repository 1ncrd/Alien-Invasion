from ship import Ship
import pygame
from settings import *
from weapon import *


class PlayerShip(Ship):

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/spaceship.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 0.3)
        self.shoot_point_offset = self._image.get_size()[0] / 2
        self.speed = 3

    def move(self, direction: Vector2):
        self.center_pos += direction * self.speed
        if not BATTLEFIELD_RECT.contains(self.rect):
            self.center_pos -= direction * self.speed

    def update(self):
        pass
