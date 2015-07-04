#!/usr/bin/python
from __future__ import print_function
import pygame
import sys

import graphics
import boids

import math

from random import randrange, random, seed

boidflock = pygame.sprite.Group()

def start():
    global boidflock

    seed(time.time())

    graphics.init(width=640, height=480)

    graphics.bg_colour(graphics.BLACK)

    #splatter a flock in the space randomly
    def generate_boid():
        x = randrange(0, 640) #random left-right
        y = randrange(0, 480) #random up-down

        position = pygame.math.Vector2(x, y)
        #splat a boid, add to flock list
        velocity = pygame.math.Vector2((random() * 2) - 1, (random() * 2) - 1)
        velocity.scale_to_length(50)

        boidflock.add(boids.Boid(position, velocity))

    for _ in range(50):
        generate_boid()

    for b in boidflock:
        b.image = pygame.Surface((1, 1))
        b.image.fill(graphics.WHITE)

    boidflock.draw(graphics.screen)

    graphics.draw()

def update(dt):
    boidflock.update(dt, 0, 640, 0, 480)

    graphics.bg_colour(graphics.BLACK)

    boidflock.draw(graphics.screen)

    graphics.draw()

import time

def update_loop(fps):
    last_loop = time.time()
    while True:
        loop_start = time.time()

        update(loop_start - last_loop)

        last_loop = loop_start

        sleep_time = max(0, 1.0 / fps - (time.time() - loop_start))

if __name__ == '__main__':
    start()
    update_loop(25)
