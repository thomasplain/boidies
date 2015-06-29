import pygame

screen = None

WHITE = 255, 255, 255
BLACK = 0, 0, 0
GREEN = 0, 255, 0

def init(width, height):
    global screen

    pygame.init()

    size = width, height

    screen = pygame.display.set_mode(size)

def bg_colour(colour):
    screen.fill(colour)

def rect(top, left, width, height, colour):
    rect_object = pygame.Rect(top, left, width, height)

    pygame.draw.rect(screen, colour, rect_object)

def circle(pos, radius, colour):
    pygame.draw.circle(screen, colour, map(int, pos), radius)

def curve(points, colour):
    print ('Points : {0}'.format(', '.join(map(str, points))))
    pygame.draw.lines(screen, colour, False, points)

def draw():
    pygame.display.flip()
