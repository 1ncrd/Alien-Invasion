import pygame
from pygame import Vector2

from health import Health
from ship import Ship
from settings import *
from weapon import *


class SmallEnemy(Ship):
    MAX_HEALTH = 10

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/small-ufo.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 0.1)
        self.speed = 2

        self.exp_reward = 3

        self.score_reward = 3

        self.health = Health(SmallEnemy.MAX_HEALTH)

    @property
    def forward_direction(self) -> Vector2:
        return Vector2(0, 1)

    def update(self) -> None:
        self.move(self.forward_direction)


class MediumEnemy(Ship):
    MAX_HEALTH = 20

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/medium-ufo.png')
        self._image = pygame.transform.rotozoom(self._image, 0, 1)
        self.speed = 1

        self.exp_reward = 6

        self.score_reward = 10

        self.health = Health(MediumEnemy.MAX_HEALTH)
        self.collision_damage = 20
        self.shoot_point_offset = self._image.get_size()[0] / 2
        self.weapons.append(EnemyNormalGun())

    @property
    def forward_direction(self) -> Vector2:
        return Vector2(0, 1)

    def update(self) -> None:
        self.move(self.forward_direction)


class BossEnemy(Ship):
    image = pygame.image.load(r'res/big-ufo.png')
    MAX_HEALTH = 200

    def __init__(self, initial_position: Vector2):
        super().__init__(initial_position)
        self._image = pygame.image.load(r'res/big-ufo.png')
        self.speed = 2
        self.health = Health(BossEnemy.MAX_HEALTH)
        self.target_pos = Vector2(SCREEN_SIZE.x // 2, self.rect.height)
        self.collision_damage = 100
        self.exp_reward = 20

        gun = NormalGun()
        gun.scatter_angle = 20
        gun.scatter_count = 3
        gun.shoot_rate = 1
        self.weapons.append(gun)

    @property
    def forward_direction(self) -> Vector2:
        return Vector2(0, 1)

    def update(self) -> None:
        if self.center_pos.y < self.target_pos.y:
            self.move(self.forward_direction)
