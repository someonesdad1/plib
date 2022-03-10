'''
Draw a circular degree grid.  Make a tick mark at every degree.  Make
a slightly larger tick mark every 5 degrees.  Make a large tick mark
every 10 degrees and label this tick mark.
'''
from g import *
def DegreeScale(file):
    s = Setup(file, portrait, inches)
    lineWidth(0.01)
    textSize(0.15)
    translate(4.25, 5.5)  # Put origin at center of (letter-sized) page
    radius = 3.5
    # Draw circle center crosshairs and axis lines
    delta = 0.1
    line(-delta, 0, delta, 0)
    line(0, -delta, 0, delta)
    push()
    for ix in range(4):
        line(2 * delta, 0, radius - delta, 0)
        rotate(90)
    pop()
    # Draw tick marks every degree
    delta = 0.05  # Tick mark length
    push()  # Isolation so we can use rotate()
    for ix in range(360):
        line(radius, 0, radius + delta, 0)
        rotate(1)
    pop()
    # Draw tick marks every 5 degrees
    push()
    for ix in range(360 // 5):
        line(radius, 0, radius + 1.5 * delta, 0)
        rotate(5)
    pop()
    # Draw tick marks every 10 degrees and add a text label
    push()
    for ix in range(360 // 10):
        line(radius, 0, radius + 2 * delta, 0)
        rmove(delta, -delta)
        text("%d" % (10 * ix))
        rotate(10)
    pop()
    s.close()
DegreeScale("out/degree_scale.ps")
