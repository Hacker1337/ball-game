import os

import pygame
from pygame.draw import *
from random import randint
from random import random

pygame.init()

FPS = 60
field_height = 900
field_width = 1200
screen = pygame.display.set_mode((field_width, field_height))
score = 0

RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
BLACK = (0, 0, 0)
COLORS = [RED, BLUE, YELLOW, GREEN, MAGENTA, CYAN]


def new_ball():
    """
    Paints new ball
    :returns his position and size
    """
    x = randint(100, field_width - 100)
    y = randint(100, field_height - 100)
    r = randint(20, 100)
    color = COLORS[randint(0, 5)]
    circle(screen, color, (x, y), r)
    return (x, y), r


def click(e, x, y, r):
    """Runs after mouse click"""
    mx, my = e.pos  # mouse position
    inside = (x - mx) ** 2 + (y - my) ** 2 <= r * r
    return inside
    # if inside:
    # print(x, y, r)
    # print(e.pos)


def speed_modification():
    """Generates coefficient for multiplying balls speed"""
    return 0.90 + random() * 0.15


class Target:
    def __init__(self, screen):
        self.screen = screen
        self.x = randint(100, field_width - 100)
        self.y = randint(100, field_height - 100)
        self.r = randint(10, 100)
        self.color = COLORS[randint(0, 5)]
        self.dx = randint(1, 5)
        self.dy = randint(1, 5)
        self.score_rate = 1  # how difficult the target is

    def paint(self):
        pass

    def move(self):
        if (self.x + self.r >= field_width) or (self.x - self.r <= 0):
            self.dx = -self.dx * speed_modification()
            self.dy = self.dy * speed_modification()
        if (self.y + self.r >= field_height) or (self.y - self.r <= 0):
            self.dx = self.dx * speed_modification()
            self.dy = -self.dy * speed_modification()
        self.x += self.dx
        self.y += self.dy
        self.paint()

    def insight(self, mx, my):
        pass


class Ball(Target):
    def paint(self):
        circle(screen, self.color, (self.x, self.y), self.r)

    def insight(self, mx, my):
        return (self.x - mx) ** 2 + (self.y - my) ** 2 <= self.r * self.r


class Square(Target):
    def paint(self):
        rect(screen, self.color, [(self.x - self.r, self.y - self.r), (2 * self.r, 2 * self.r)])

    def insight(self, mx, my):
        return (abs(mx - self.x) <= self.r) and (abs(my - self.y) <= self.r)


pygame.display.update()
clock = pygame.time.Clock()
finished = False

# Balls initialization
targets = []
ball_number = 5
for i in range(ball_number):
    tar = Ball(screen)
    targets.append(tar)

square_number = 5
for i in range(square_number):
    square = Square(screen)
    targets.append(square)

while not finished:
    clock.tick(FPS)
    screen.fill(BLACK)
    # Balls movement
    for tar in targets:
        tar.move()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            finished = True
        elif event.type == pygame.MOUSEBUTTONDOWN:
            for i in range(len(targets)):
                tar = targets[i]
                if click(event, tar.x, tar.y, tar.r):
                    score += 1000 / tar.r * tar.score_rate * (tar.dx ** 2 + tar.dy ** 2)
                    if random() > 0.5:
                        targets[i] = Ball(screen)
                    else:
                        targets[i] = Square(screen)
                    print(format(score, '0.1f'))
    pygame.display.update()

pygame.quit()

name = input("Enter your nickname:\n")

scorefile = "score.txt"
file = open(scorefile, 'a')
print(f"{name}\t {format(score, '0.1f')}")
print(f"{name}\t {score}", file=file)
