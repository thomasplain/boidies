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
from pygame.math import Vector2

import operator
import math

class Boid(object):
    def __init__(self, x, y):
        pass

class Boids:
    def __init__(self, numboids = 10, dimensions={'x':640, 'y':480}):     #class constructor with default parameters filled
        #class constants

        #the next six lines define the boundaries of the torus
        """
        torus:  donut shaped space, i.e. infinite
        effect: boids flying out of bounds appear at the opposite side
        note:   cartesian matrices don't handle toruses very well, but I couldn't
                figure out a better way to keep the flock in view.
        """
        seed(time.time())

        self.MINX = 0     #left
        self.MINY = 0   #bottom
        self.MAXX = dimensions['x']           #right
        self.MAXY = dimensions['y']          #top

        self.RADIUS = 1                 #radius of a boid.  I wimped and used spheres.
        self.NEARBY = self.RADIUS * 5   #the 'halo' of space around each boid
        self.FACTOR = .95               #the amount of movement to the perceived flock center
        self.NEGFACTOR = self.FACTOR * -1.0 #same thing, only negative

        self.NUMBOIDS = numboids        #the number of boids in the flock

        self.boidflock = []             #empty list of boids
        self.velocities = []
        self.DT = 0.02                  #delay time between snapshots

        self.initializePositions()      #create a space with boids

    def initializePositions(self):
        #wire frame of space
        leftBottom = graphics.curve([(self.MINX, self.MINY), (self.MINX, self.MINY)], graphics.WHITE)
        leftTop = graphics.curve([(self.MINX, self.MAXY), (self.MINX, self.MAXY)], graphics.WHITE)
        rightBottom = graphics.curve([(self.MAXX, self.MINY), (self.MAXX, self.MINY)], graphics.WHITE)
        rightTop = graphics.curve([(self.MAXX, self.MAXY), (self.MAXX, self.MAXY)], graphics.WHITE)

        #splatter a flock in the space randomly
        for b in range(self.NUMBOIDS):          #for each boid, ...
            x = randrange(self.MINX, self.MAXX) #random left-right
            y = randrange(self.MINY, self.MAXY) #random up-down

            #splat a boid, add to flock list
            velocity = Vector2((random() * 2) - 1, (random() * 2) - 1).normalize() * 10
            self.boidflock.append((Vector2(x, y), velocity))

    def moveAllBoidsToNewPositions(self, dt):
        for i, b in enumerate(self.boidflock):
            #manage boids hitting the torus 'boundaries'
            if b[0].x < self.MINX:
                b[0].x = self.MINX
                b[1].x = -b[1].x

            if b[0].x > self.MAXX:
                b[0].x = self.MAXX
                b[1].x = -b[1].x

            if b[0].y < self.MINY:
                b[0].y = self.MINY
                b[1].y = -b[1].y

            if b[0].y > self.MAXY:
                b[0].y = self.MAXY
                b[1].y = -b[1].y

            collision_radius = 100

            def collision_occurred(m):
                return math.sqrt(b[0].distance_squared_to(m[0])) <= collision_radius

            without_me = filter(lambda x: x != b, self.boidflock)

            mob = filter(collision_occurred, without_me)

            v1 = self.rule1(b, mob)              #get the vector for rule 1
            v2 = self.rule2(b, mob)              #get the vector for rule 2
            v3 = self.rule3(b, mob)              #get the vector for rule 3

            boidvelocity = v1 + v2 + v3  #accumulate the rules vector results
#            print boidvelocity
#            old_b = b
            self.boidflock[i] = (b[0], boidvelocity) #move the boid


#       print self.boidflock
        for i, boid in enumerate(self.boidflock):
        #   print boid
           self.boidflock[i] = (boid[0] + boid[1] * dt, boid[1])

    def rule1(self, aboid, mob):    #Rule 1:  boids fly to perceived flock center
        if not mob:
            return Vector2(0, 0)

        pfc = reduce(operator.add, zip(*mob)[0], Vector2(0, 0))

        pfc = pfc/len(mob)             #average the pfc

        return (pfc - aboid[0])

    def rule2(self, aboid, mob):    #Rule 2: boids avoid other boids
        if not mob:
            return Vector2(0, 0)

        def get_nudge(x):
            dir = aboid[0] - x[0]
            mag = 20 - dir.length()

            try:
                return dir.normalize() * mag
            except:
                return Vector2(random(), random()).normalize() * mag

        nudges = map(get_nudge, mob)

        return reduce(operator.add, nudges, Vector2(0, 0))

    def rule3(self, aboid, mob):    #Rule 3: boids try to match speed of flock
        pfv = reduce(lambda b, x: b + x[1], mob, Vector2(0.0,0.0))   #pfv: perceived flock velocity

        pfv = (pfv + aboid[1]) / (len(mob) + 1)

        return pfv
