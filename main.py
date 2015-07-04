#!/usr/bin/python
import pygame
import sys

import graphics
import boids

boid_obj = None

def start():
    global boid_obj

    graphics.init(width=640, height=480)

    graphics.bg_colour(graphics.BLACK)

    boid_obj = boids.Boids(dimensions={'x':640,'y':480})

    map(lambda pos: graphics.circle(pos, 1, graphics.WHITE), zip(*boid_obj.boidflock)[0])

    graphics.draw()

def update(dt):
    boid_obj.moveAllBoidsToNewPositions(dt)

    graphics.bg_colour(graphics.BLACK)

    map(lambda pos: graphics.circle(pos, 1, graphics.WHITE), zip(*boid_obj.boidflock)[0])

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
#        print sleep_time
        time.sleep(sleep_time)

if __name__ == '__main__':
    start()
    update_loop(25)
