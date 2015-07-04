#!/usr/bin/python
from __future__ import print_function
import pygame
import sys

import graphics
import boids

import math

from random import randrange, random, seed

boid_obj = None

boidflock = None

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
        velocity.scale_to_length(10)

        return boids.Boid(position, velocity)

    boidflock = [generate_boid() for x in range(20)]

    list(map(lambda b: print(b.velocity), boidflock))

    map(lambda b: graphics.circle(b.position, 1, graphics.WHITE), boidflock)

    graphics.draw()

def update(dt):
    def boid_update(b):
        without_me = filter(lambda x: x != b, boidflock)

        def collision_occurred(m):
            return math.sqrt(b.position.distance_squared_to(m.position)) <= 100

        mob = filter(collision_occurred, without_me)

        b.update(dt, mob, 0, 640, 0, 480)

    map(boid_update, boidflock)

    graphics.bg_colour(graphics.BLACK)

    map(lambda b: graphics.circle(b.position, 1, graphics.WHITE), boidflock)

#    graphics.circle(boid_obj.greenie_pos, 5, graphics.GREEN)

    graphics.draw()

import time

def update_loop(fps):
    last_loop = time.time()
    while True:
        loop_start = time.time()

        update(loop_start - last_loop)

        last_loop = loop_start

        sleep_time = max(0, 1.0 / fps - (time.time() - loop_start))

        time.sleep(sleep_time)

if __name__ == '__main__':
    start()
    update_loop(25)
