'''
Interesting illusion from
http://www.ritsumei.ac.jp/~akitaoka/saishin-e.html
'''
import sys
import string
import math
from g import *
# Global variables
nx = 1    # Number of circles in X direction
ny = 1    # Number of circles in Y direction
nc = 20   # Number of items around the circumference
nr = 10   # Number of radii to plot on
D = 2     # Circle diameter
# Starting circle's center
X0 = 4.25
Y0 = 5.75
# Spacing of circles
dX = 2
dY = 2
def PlotItem(width, height):
    '''This is the basic graphical unit that the whole picture is made
    up from.
    '''
    push()
    # Draw a black rectangle
    rmove(-width / 2, -height / 2)
    rectangle(width, height)
    # Draw a blue ellipse on the left side
    rmove(0, height / 2)
    fillColor(blue)
    major_diameter = width / 1.5
    minor_diameter = height
    ellipse(major_diameter, minor_diameter)
    # Draw a yellow ellipse on the left side
    rmove(width, 0)
    fillColor(yellow)
    ellipse(major_diameter, minor_diameter)
    pop()
def PlotCircle(xcenter, ycenter):
    push()
    nr = 22
    nc = 26
    global D
    D *= 2
    translate(xcenter, ycenter)
    move(0, 0)
    for r in range(nr):
        dtheta = 360 / nc * math.pow(r / nr, 0.6)
        for angle in range(nc):
            move(0, 0)
            push()
            theta = (360 * angle / nc + r * dtheta) % 360
            rotate(theta)
            # print theta
            rmove(0, r / nr * D)
            factor = math.pow((r + 1) / nr, 1.7)
            scale(factor, factor)
            width = 0.5
            height = 0.5
            PlotItem(width, height)
            pop()
    pop()
if __name__ == "__main__": 
    os = open("out/illusion.ps", "w")
    ginitialize(os)
    # setOrientation(landscape, inches)
    setOrientation(portrait, inches)
    # Set main graphic properties
    fillOn()
    lineOff()
    for ix in range(nx):
        for jx in range(ny):
            x = X0 + ix * dX
            y = Y0 + ix * dY
            PlotCircle(x, y)
    if 0:  # Plot some circles in the lower left corner
        translate(1, 1)
        move(0, 0)
        circle(0.2)
        fillColor(green)
        n = 10
        for i in range(n):
            push()
            rotate(i / n * 360)
            rmove(0, 0.5)
            circle(0.2)
            pop()
        # rectangle(1, 1)
    os.close()
