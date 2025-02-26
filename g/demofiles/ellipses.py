"""
Draw a number of filled elliptical arcs with randomly-chosen colors.
This example draws a set of ellipses in the center of the screen, then
shows how easy it is to make the set of ellipses in a smaller part of
the screen by translating and scaling the coordinate system.
"""

from g import *
import random

# Convenience name for a random number generator that returns a
# uniformly-distributed random number between 0.0 and 1.0.
rand = random.random


def BlackBackground():
    """Fill the whole drawing area with black."""
    push()
    reset()
    move(-10, -10)
    fillColor(black)
    fillOn()
    rectangle(1000, 1000)
    pop()


def GetRandomColor():
    return (rand(), rand(), rand())


def RandomEllipticalArcs(numArcs=20):
    for ix in range(numArcs):
        r, g, b = rand(), rand(), rand()
        start_angle = 360 * rand()
        stop_angle = 360 * rand()
        fillColor((r, g, b))
        r, g, b = rand(), rand(), rand()
        lineColor((r, g, b))
        major_diameter = rand()
        minor_diameter = rand()
        if rand() >= 0.5:
            fillOn()
        else:
            fillOff()
        move(rand(), rand())
        ellipticalArc(major_diameter, minor_diameter, start_angle, stop_angle)


def DrawEllipses(file):
    s = Setup(file, portrait, inches)
    random.seed(1)
    BlackBackground()
    translate(2, 1)
    scale(4, 4)
    lineWidth(0.001)
    RandomEllipticalArcs()
    # Now put them in the upper left corner, but smaller
    push()
    translate(-0.3, 1.7)
    scale(0.5, 0.5)
    RandomEllipticalArcs()
    pop()
    # Upper right corner, but smaller
    push()
    translate(0.7, 1.9)
    scale(0.25, 0.25)
    RandomEllipticalArcs()
    pop()
    s.close()


DrawEllipses("out/ellipses.ps")
