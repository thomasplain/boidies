#boids.py
"""
Explores flocking behavior of flying "boids" aka "bird android".

Requires Python (www.python.org), my favorite programming language, and
and VPython (www.vpython.org), a fine Python graphics simulation extension for beginners.

Thanks to Conrad Parker conrad@vergenet.net for the boids pseudocode.
http://www.vergenet.net/~conrad/boids/pseudocode.html


Eric Nilsen
September 2003
ericjnilsen@earthlink.net

Ideas for version 2.0:
    predators
    obstructions
    perching on the ground for a bit
    prevailing wind
    random flock scattering
    cone boid shape --> change boid axis to indicate direction
"""

from random import randrange, random, seed
import time
import graphics
import pygame
from pygame.math import Vector2
import pygame.sprite

import operator
import math

class Boid(pygame.sprite.Sprite):
    def __init__(self, pos, vel, top_speed = 50):
        super(Boid, self).__init__()
        self.pos_vec = pos
        self.rect = pygame.Rect(pos.x, pos.y, 1, 1)
        self.velocity = vel
        self.heading = vel
        self.top_speed = top_speed

    @property
    def position(self):
        return self.pos_vec

    @position.setter
    def position(self, pos):
        self.pos_vec = pos
        self.rect.x = self.pos_vec.x
        self.rect.y = self.pos_vec.y

    def update(self, dt, MINX, MAXX, MINY, MAXY):

        mob = self.groups()[0]

        if self.position.x < MINX:
            self.position.x = MINX
            self.velocity.x = -self.velocity.x

        if self.position.x > MAXX:
            self.position.x = MAXX
            self.velocity.x = -self.velocity.x

        if self.position.y < MINY:
            self.position.y = MINY
            self.velocity.y = -self.velocity.y

        if self.position.y > MAXY:
            self.position.y = MAXY
            self.velocity.y = -self.velocity.y

        v1 = self.rule1(mob)              #get the vector for rule 1
        v2 = self.rule2(mob)              #get the vector for rule 2
        v3 = self.rule3(mob)              #get the vector for rule 3

        boidvelocity = v1 + v2 + v3
        boidvelocity.scale_to_length(self.top_speed)  #accumulate the rules vector results
        self.velocity = self.velocity.lerp(boidvelocity, 0.25)
        self.position += dt * self.velocity

    def rule1(self, mob):    #Rule 1:  boids fly to perceived flock center
        pfc = reduce(operator.add, [x.position for x in mob], Vector2(0, 0))

        pfc = pfc/len(mob)             #average the pfc

        return (pfc - self.position)

    def rule2(self, mob):    #Rule 2: boids avoid other boids
        too_close = pygame.Rect(self)
        too_close.width = 50
        too_close.height = 50

        mob = filter(lambda b: too_close.colliderect(b), mob)

        def get_nudge(x):
            if x == self:
                return Vector2(0, 0)
            dir = self.position - x.position
            mag = 100 - dir.length()

            try:
                return dir.normalize() * mag
            except:
                # return Vector2((random() * 2) - 1, \
                #                (random() * 2) - 1)
                return Vector2(0, 0)

        nudges = map(get_nudge, mob)

        return reduce(operator.add, nudges, Vector2(0, 0))

    def rule3(self, mob):    #Rule 3: boids try to match speed of flock
        pfv = reduce(lambda b, x: b + x.velocity, mob, Vector2(0.0,0.0))   #pfv: perceived flock velocity

        pfv = (pfv + self.velocity) / (len(mob) + 1)

        return pfv
