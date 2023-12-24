import pygame

from health import Health
from settings import *
from weapon import *


class Ship(pygame.sprite.Sprite):
    MAX_HEALTH = 100

    def __init__(self, initial_position: Vector2) -> None:
        super().__init__()
        # initial position
        self.center_pos = initial_position
        self._image = pygame.image.load(r'res/spaceship.png')
        self.speed = 5

        # weapon
        self.weapons: list[Weapon] = []
        self.bullets: list[Bullet] = []

        # health
        self.health = Health(Ship.MAX_HEALTH)
        self.shoot_point_offset = self._image.get_size()[0] / 2

        self.collision_damage = 10

        self.exp_reward = 0

        self.score_reward = 3

    def update(self) -> None:
        pass

    @property
    def shoot_point(self):
        return self.center_pos + self.forward_direction * self.shoot_point_offset

    def attack(self) -> list[Bullet]:
        bullets = []
        for weapon in self.weapons:
            bullets += weapon.attack(self.shoot_point, self.forward_direction)

        return bullets

    @property
    def image(self):
        return self._image

    @property
    def rect(self):
        return self.image.get_rect(center=self.center_pos)

    def is_alive(self) -> bool:
        return self.health.alive()

    def get_health_bar_rect(self) -> pygame.Rect:
        health_bar_size = Vector2(40, 5)
        health_bar_height_offset = 60
        center = Vector2(self.rect.center)
        return pygame.Rect(center.x - health_bar_size.x / 2,
                           center.y - health_bar_height_offset / 2,
                           health_bar_size.x, health_bar_size.y)

    @property
    def forward_direction(self) -> Vector2:
        return Vector2(0, -1)

    def move(self, direction: Vector2):
        """
        Move towards the direction.
        :param direction: normalized Vector2
        :return: None
        """
        self.center_pos += direction * self.speed

