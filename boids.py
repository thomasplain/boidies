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

from random import randrange
import graphics
from pygame.math import Vector2

import operator

class Boids:
    def __init__(self, numboids = 10, sidesize = 120.0):     #class constructor with default parameters filled
        #class constants

        self.SIDE = sidesize            #unit for a side of the flight space

        #the next six lines define the boundaries of the torus
        """
        torus:  donut shaped space, i.e. infinite
        effect: boids flying out of bounds appear at the opposite side
        note:   cartesian matrices don't handle toruses very well, but I couldn't
                figure out a better way to keep the flock in view.
        """
        self.MINX = self.SIDE * -1.0 + 160     #left
        self.MINY = self.SIDE * -1.0 + 120   #bottom
        self.MAXX = self.SIDE + 160           #right
        self.MAXY = self.SIDE +120          #top

        self.RADIUS = 1                 #radius of a boid.  I wimped and used spheres.
        self.NEARBY = self.RADIUS * 5   #the 'halo' of space around each boid
        self.FACTOR = .95               #the amount of movement to the perceived flock center
        self.NEGFACTOR = self.FACTOR * -1.0 #same thing, only negative

        self.NUMBOIDS = numboids        #the number of boids in the flock

        self.boidflock = []             #empty list of boids
        self.velocities = []
        self.DT = 0.02                  #delay time between snapshots

        self.boids()                    #okay, now that all the constants have initialized, let's fly!

        self.greenie_pos = Vector2(0,0)

    def boids(self):
        self.initializePositions()      #create a space with boids
        # while (1==1):                   #loop forever
        #     rate(100)                   #controls the animation speed, bigger = faster
        #     self.moveAllBoidsToNewPositions()   #um ... what it says

    def initializePositions(self):
        #wire frame of space
        leftBottom = graphics.curve([(self.MINX, self.MINY), (self.MINX, self.MINY)], graphics.WHITE)
        leftTop = graphics.curve([(self.MINX, self.MAXY), (self.MINX, self.MAXY)], graphics.WHITE)
        rightBottom = graphics.curve([(self.MAXX, self.MINY), (self.MAXX, self.MINY)], graphics.WHITE)
        rightTop = graphics.curve([(self.MAXX, self.MAXY), (self.MAXX, self.MAXY)], graphics.WHITE)

        #splatter a flock in the space randomly
        c = 0                                   #initialize the color switch
        for b in range(self.NUMBOIDS):          #for each boid, ...
            x = randrange(self.MINX, self.MAXX) #random left-right
            y = randrange(self.MINY, self.MAXY) #random up-down

            # if c > 2:                           #reset the color switch when it grows too big
            #     c = 0
            # if c == 0:
            #     COLOR = color.yellow            #a third of the boids shall have yellow
            # if c == 1:
            #     COLOR = color.red               #and yea a third of the boids shall have red
            # if c == 2:
            #     COLOR = color.blue              #and verily a third of the boids shall have blue

            #splat a boid, add to flock list
            self.boidflock.append((Vector2(x, y), Vector2(0, 0)))

            # c = c + 1                           #increment the color switch

##        self.greenie = sphere(radius=self.RADIUS, color=color.green)    #pseudo-boid for testing

    def moveAllBoidsToNewPositions(self, dt):
        for i, b in enumerate(self.boidflock):
            #manage boids hitting the torus 'boundaries'
            if b[0].x < self.MINX:
                b[0].x = self.MINX

            if b[0].x > self.MAXX:
                b[0].x = self.MAXX

            if b[0].y < self.MINY:
                b[0].y = self.MINY

            if b[0].y > self.MAXY:
                b[0].y = self.MAXY

            #v1 = Vector2(0.0,0.0)        #initialize vector for rule 1
#            without_me = filter(lambda x: x!=b, self.boidflock)
 #           print self.boidflock
 #           print without_me
 #           v1 = reduce(operator.add, without_me, Vector2(0,0))/ self.NUMBOIDS
       #     self.greenie_pos = v1
            v2 = Vector2(0.0,0.0)        #initialize vector for rule 2
            v3 = Vector2(0.0,0.0)        #initialize vector for rule 3


            v1 = self.rule1(b[0])              #get the vector for rule 1
            v2 = self.rule2(b[0])              #get the vector for rule 2
            v3 = self.rule3(b)              #get the vector for rule 3

            boidvelocity = v1 + v2 + v3  #accumulate the rules vector results
#            print boidvelocity
#            old_b = b
            self.boidflock[i] = (b[0] + boidvelocity * dt, boidvelocity) #move the boid


#        print self.boidflock
#        for i, boid in enumerate(self.boidflock):
 #           print boid
 #           self.boidflock[i] = (boid[0] + boid[1] * dt, boid[1])



    def rule1(self, aboid):    #Rule 1:  boids fly to perceived flock center
        without_me = filter(lambda x: x != aboid, zip(*self.boidflock)[0])
#        print without_me
        pfc = reduce(operator.add, without_me, Vector2(0, 0))

        pfc = pfc/(self.NUMBOIDS - 1)             #average the pfc
#        print aboid

        return (pfc - aboid)

    def rule2(self, aboid):    #Rule 2: boids avoid other boids
        distance = 20

        def collision_occurred(b):
            return b.distance_to(aboid) <= distance

        without_me = filter(lambda x : x != aboid, zip(*self.boidflock)[0])

        colliders = filter(collision_occurred, without_me)

        def get_nudge(x):
            dir = aboid - x
            mag = distance - dir.length()

            return dir.normalize() * mag

        nudges = map(get_nudge, colliders)

        return reduce(operator.add, nudges, Vector2(0, 0))

    def rule3(self, aboid):    #Rule 3: boids try to match speed of flock
        distance = 20

#        def collision_occurred(b):
#            return b[0].distance_to(aboid[0]) <= distance

        without_me = filter(lambda x : x[0] != aboid[0], self.boidflock)

#        colliders = filter(collision_occurred, without_me)

        pfv = reduce(lambda b, x: b + x[1], without_me, Vector2(0.0,0.0))   #pfv: perceived flock velocity

        pfv = pfv/len(without_me)
#        pfv = pfv/(aboid + 1)    #some of the boids are more sluggish than others

        return pfv


if __name__ == "__main__":
    #if you run this from Idle via the F5 key, the following occurs:
    b = Boids()     #instantiate the Boids class, the class constructor takes care of the rest.
##    b = Boids(20, 60.0)   #here's a way to change the flock amount, and space size
