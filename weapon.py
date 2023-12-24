import random
from typing import Any

import pygame
from pygame.sprite import AbstractGroup

from settings import *
from abc import ABC, abstractmethod


class Bullet(pygame.sprite.Sprite):
    image = pygame.image.load(r'res/fire_bullet_no_bound.png')
    image = pygame.transform.rotozoom(image, 0, 1)

    def __init__(self, position: Vector2 = None, direction: Vector2 = None, damage=0, speed=0) -> None:
        super().__init__()
        if position:
            self.center_pos = position.copy()
        if direction:
            self.direction = direction.copy().normalize()
        self.damage = damage
        self.speed = speed

    @property
    def rect(self):
        return Bullet.image.get_rect(center=self.center_pos)

    def update(self, *args: Any, **kwargs: Any) -> None:
        dx = self.speed * self.direction.x
        dy = self.speed * self.direction.y
        self.center_pos += (dx, dy)


class NormalBullet(Bullet):
    pass


class Weapon(ABC):
    @abstractmethod
    def attack(self, *args: Any, **kwargs: Any) -> list[Bullet]:
        pass


class NormalGun(Weapon):
    def __init__(self):
        self.shoot_rate = 5
        self.scatter_count = 1
        self.scatter_angle = 3
        self.last_shoot_time = 0
        self.bullet = Bullet(damage=2, speed=7)

    def attack(self, start_pos: Vector2, direction: Vector2) -> list[Bullet]:
        if pygame.time.get_ticks() - self.last_shoot_time < 1000 / self.shoot_rate:
            return []

        bullets = []
        angle = -(self.scatter_count // 2) * self.scatter_angle
        for i in range(self.scatter_count):
            new_bullet = NormalBullet(start_pos, direction.rotate(angle), self.bullet.damage, self.bullet.speed)
            bullets.append(new_bullet)
            angle += self.scatter_angle

        self.last_shoot_time = pygame.time.get_ticks()

        return bullets

    def bullet_damage_up(self):
        self.bullet.damage += 1

    def bullet_speed_up(self):
        self.bullet.speed += 1

    def shoot_rate_up(self):
        self.shoot_rate += 1

    def scatter_count_up(self):
        self.scatter_count += 1

    def upgradable_skills(self):
        return {
            self.__class__.__name__ + ": Add bullet damage": self.bullet_damage_up,
            self.__class__.__name__ + ": Add bullet speed": self.bullet_speed_up,
            self.__class__.__name__ + ": Add shoot rate": self.shoot_rate_up,
            self.__class__.__name__ + ": Add scatter count": self.scatter_count_up,
        }


class EnemyNormalGun(NormalGun):
    def __init__(self):
        super().__init__()
        self.shoot_rate = 0.5
        self.speed = 4
