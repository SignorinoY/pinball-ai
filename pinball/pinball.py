from pinball.ball import Ball
from pinball.segment import Segment
from pinball.point import Point

import pygame
import math

RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RAD = math.pi / 180

FPS = 60

class Pinball(object):

    def __init__(self, level, render=False):

        self.level = level
        self.render = render

        self.width = self.level['size']['width']
        self.height = self.level['size']['height']

        self.obstacles = []
        for obstacle in self.level['obstacles']:
            self.obstacles.append(
                Segment(
                    Point(*obstacle['from']),
                    Point(*obstacle['to']),
                    WHITE
                )
            )
        
        self.mu = self.level['mu']

        self.reset()

        if self.render:
            pygame.init()
            pygame.display.set_caption("Pinball")
            self.screen = pygame.display.set_mode((self.width, self.height), pygame.DOUBLEBUF, 32)
            self.clock = pygame.time.Clock()

    def reset(self):

        self.player = Ball(
            Point(*self.level['player']['position']),
            self.level['player']['radius'],
            RED,
            0
        )

        self.enemies = []
        for enemy in self.level['enemies']:
            self.enemies.append(
                Ball(
                    Point(*enemy['position']),
                    enemy['radius'],
                    WHITE,
                    enemy['score']
                )
            )

        self.chance = self.level['chance']
        
        self.reward = 0
        self.done = False

        return self.observation() 

    def step(self, action):

        if not self.done:

            self.chance -= 1
            self.simulation(action)

            if self.chance == 0:
                self.done = True

        return self.observation(), self.reward, self.done

    def simulation(self, action):

        speed_x = action[0]
        speed_y = action[1]

        speed = math.sqrt(speed_x ** 2 + speed_y ** 2)

        while speed > 0:

            for i in range(len(self.enemies) - 1, -1, -1):
                enemy = self.enemies[i]
                if self.player.hit(enemy):
                    self.reward += enemy.score
                    self.enemies.pop(i)

            # 墙壁反弹 临时修复卡墙角问题
            if self.player.center.x <= self.player.radius:
                self.player.center.x = self.player.radius + 1
                speed_x *= -1
            elif self.player.center.x >= self.width - self.player.radius:
                self.player.center.x = self.width - self.player.radius - 1
                speed_x *= -1
            if self.player.center.y <= self.player.radius:
                self.player.center.y = self.player.radius + 1
                speed_y *= -1
            elif self.player.center.y >= self.height - self.player.radius:
                self.player.center.y = self.height - self.player.radius - 1
                speed_y *= -1

            # 障碍物反弹
            # [bug] 穿模问题未解决以及卡在墙角
            for obstacle in self.obstacles:
                if self.player.collision(obstacle):
                    speed_x, speed_y = self.player.rebound(obstacle, speed_x, speed_y)
                    break
            
            mu = - self.mu * 100 * 9.8
            speed_slowed = speed + mu * 1/FPS if (speed + mu * 1/FPS) > 0 else 0
            speed_x = speed_x * speed_slowed / speed
            speed_y = speed_y * speed_slowed / speed
            speed = speed_slowed

            self.player.center.x += speed_x * 1/FPS
            self.player.center.y += speed_y * 1/FPS

            if self.render:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        quit()
                self.draw()
                pygame.display.flip()
                self.clock.tick(FPS)

    def draw(self):
        self.screen.fill(BLACK)

        for obstacle in self.obstacles:
            obstacle.draw(self.screen)

        for enemy in self.enemies:
            enemy.draw(self.screen)

        self.player.draw(self.screen)

    def observation(self):

        observation = {}

        observation['size'] = {}
        observation['size']['width'] = self.width
        observation['size']['height'] = self.height

        observation['mu'] = - self.mu / 100 / 9.8

        observation['chance'] = self.chance

        observation['player'] = {}
        observation['player']['position'] = self.player.center.x, self.player.center.y
        observation['player']['radius'] = self.player.radius

        observation['obstacles'] = []
        for obstacle in self.obstacles:
            observation['obstacles'].append(
                {
                    'from': (obstacle.p1.x, obstacle.p1.y),
                    'to': (obstacle.p2.x, obstacle.p2.y),
                }
            )

        observation['enemies'] = []
        for enemy in self.enemies:
            observation['enemies'].append(
                {
                    'position': (enemy.center.x, enemy.center.y),
                    'radius': enemy.radius,
                    'score': enemy.score
                }
            )

        return observation
