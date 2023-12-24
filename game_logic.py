import pygame

from settings import *
from player_ship import PlayerShip
from enemy import *
from exp import Exp
from scipy.spatial import KDTree
from math import hypot
import random


class GameLogic:

    def __init__(self):
        self.player = PlayerShip(initial_position=Vector2(SCREEN_SIZE.x / 2, SCREEN_SIZE.y * 3 / 4))
        normal_gun = NormalGun()
        self.player.weapons.append(normal_gun)

        self.skill_list = {}
        self.skill_list.update(normal_gun.upgradable_skills())

        self.player_bullets: list[Bullet] = []
        self.enemy_bullets: list[Bullet] = []
        self.enemies: list[Ship] = []
        self.last_enemy_generate_time = 0
        self.enemy_generate_rate = 0.5
        self.exp = Exp()
        self.score = 0
        self.game_over = False
        self.level_up = 0

    def random_skills(self, n=3):
        skill_list = random.sample(list(self.skill_list.items()), k=n)

        return skill_list

    def update(self):
        self.handle_player_input()

        for enemy in self.enemies:
            self.enemy_bullets += enemy.attack()
            enemy.update()

        for bullet in self.player_bullets:
            bullet.update()
        for bullet in self.enemy_bullets:
            bullet.update()

        self.collision_detection()

        self.exp_reward()

        self.score_reward()

        self.border_detection()

        self.health_check()

        self.enemy_generate()

        self.adjust_enemy_generate_rate()

    def handle_player_input(self):
        keys = pygame.key.get_pressed()
        if keys[KEY_MODE.LEFT]:
            self.player.move(Vector2(-1, 0))
        if keys[KEY_MODE.RIGHT]:
            self.player.move(Vector2(1, 0))
        if keys[KEY_MODE.UP]:
            self.player.move(Vector2(0, -1))
        if keys[KEY_MODE.DOWN]:
            self.player.move(Vector2(0, 1))
        if keys[KEY_MODE.SHOOT]:
            self.player_bullets += self.player.attack()

    def collision_detection(self):
        objects = self.enemies + self.player_bullets
        if len(objects) != 0:
            bullets_to_remove = set()
            tree = KDTree([obj.rect.center for obj in objects])
            distance = max(hypot(*obj.rect.size) for obj in objects)
            collisions = tree.query_pairs(distance)
            for i, j in collisions:
                bullet = None
                ship = None
                if isinstance(objects[i], Bullet):
                    bullet = objects[i]
                if isinstance(objects[i], Ship):
                    ship = objects[i]
                if isinstance(objects[j], Bullet):
                    bullet = objects[j]
                if isinstance(objects[j], Ship):
                    ship = objects[j]
                if bullet and ship:
                    if pygame.sprite.collide_mask(ship, bullet) and bullet not in bullets_to_remove:
                        bullets_to_remove.add(bullet)
                        ship.health.reduce(bullet.damage)
            for bullet in bullets_to_remove:
                self.player_bullets.remove(bullet)

        for enemy in self.enemies:
            if pygame.sprite.collide_mask(self.player, enemy):
                self.player.health.reduce(enemy.collision_damage)
                enemy.health.reduce(self.player.collision_damage)

        for bullet in self.enemy_bullets:
            if pygame.sprite.collide_mask(self.player, bullet):
                self.player.health.reduce(bullet.damage)

        self.enemy_bullets = [bullet for bullet in self.enemy_bullets
                              if not pygame.sprite.collide_mask(self.player, bullet)]

    def border_detection(self):
        self.enemies = [enemy for enemy in self.enemies if BATTLEFIELD_RECT.contains(enemy.rect)]
        self.player_bullets = [bullet for bullet in self.player_bullets if SCREEN_RECT.contains(bullet.rect)]
        self.enemy_bullets = [bullet for bullet in self.enemy_bullets if BATTLEFIELD_RECT.contains(bullet.rect)]

    def health_check(self):
        if not self.player.health.alive():
            self.game_over = True

        self.enemies = [enemy for enemy in self.enemies if enemy.health.alive()]

    def enemy_generate(self):
        if pygame.time.get_ticks() - self.last_enemy_generate_time < 1000 / self.enemy_generate_rate:
            return

        enemy_type = random.randint(1, 100)
        if enemy_type < 85:
            x = random.randrange(SCREEN_SIZE.x)
            self.enemies.append(SmallEnemy(initial_position=Vector2(x, 0)))
        elif enemy_type < 99:
            x = random.randrange(SCREEN_SIZE.x)
            self.enemies.append(MediumEnemy(initial_position=Vector2(x, 0)))
        elif not any(isinstance(enemy, BossEnemy) for enemy in self.enemies):
            self.enemies.append(BossEnemy(Vector2(SCREEN_SIZE.x / 2, -BossEnemy.image.get_height() / 2)))

        self.last_enemy_generate_time = pygame.time.get_ticks()

    def exp_reward(self):
        total_exp_reward = sum(enemy.exp_reward for enemy in self.enemies if not enemy.health.alive())
        last_level = self.exp.level
        self.exp.increase(total_exp_reward)
        self.level_up = self.exp.level - last_level

    def adjust_enemy_generate_rate(self):
        self.enemy_generate_rate = 0.5 + pygame.time.get_ticks() / 1000 / 100

    def score_reward(self):
        total_score_reward = sum(enemy.score_reward for enemy in self.enemies if not enemy.health.alive())
        self.score += total_score_reward
