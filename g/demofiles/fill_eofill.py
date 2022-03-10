'''
Draw two little squares inside of a square as part of the same path,
then fill it.  The square at the bottom of the page is filled with the
default filling method.  You'll see that the inner square marked CCW
(means it was traversed in the counterclockwise direction) is filled,
but the CW sqare is not.   The upper square on the page is filled with
a different PostScript filling method called eofill, or "even-odd"
fill. 

See the documentation for an explanation of the difference between the
fillPath() and the eofillPath() commands.
'''
from g import *
import random
rand = random.random  # Convenience name for a random number generator that
# returns a uniformly-distributed random number between
# 0.0 and 1.0.
def ShowDifferentFillTypes(file):
    s = Setup(file, portrait, inches)
    textName(Sans)
    lineWidth(0.03)
    newPath()
    fill_color = yellow
    border_color = navy
    # Draw some lines to show the background
    push()
    lineColor(red)
    lineWidth(0.01)
    translate(0.75, 0)
    for ix in range(15):
        move(0, 0)
        rline(4, 4)
        translate(0, 0.5)
    pop()
    # Make a big square; add points counterclockwise
    pathAddPoint(1, 1)
    pathAddPoint(4, 1)
    pathAddPoint(4, 4)
    pathAddPoint(1, 4)
    pathClose()
    # Make two smaller squares; add points clockwise and counterclockwise
    ll = 1.5
    delta = 1
    pathAddPoint(ll + delta, ll)
    pathAddPoint(ll, ll)
    pathAddPoint(ll, ll + delta)
    pathAddPoint(ll + delta, ll + delta)
    pathClose()
    ll = 2.5
    pathAddPoint(ll, ll)
    pathAddPoint(ll + delta, ll)
    pathAddPoint(ll + delta, ll + delta)
    pathAddPoint(ll, ll + delta)
    pathClose()
    p = getPath()
    # Fill the path
    fillOn()
    fillColor(fill_color)
    fillPath()
    # Draw a border
    setPath(p)
    lineColor(border_color)
    drawPath()
    # Label the inner squares
    textSize(0.3)
    move(1.7, 1.9)
    text("CW")
    move(2.65, 2.9)
    text("CCW")
    # Label the fill type
    move(5, 2.5)
    text("non-zero winding fill")
    move(5, 2.2)
    text("(default)")
    # Move to a location above the squares just drawn, redraw the path,
    # and use eofillPath() this time.
    translate(0, 5)
    setPath(p)
    fillColor(fill_color)
    eoFillPath()
    # Draw a border
    setPath(p)
    lineColor(border_color)
    drawPath()
    # Label the inner squares
    textSize(0.3)
    move(1.7, 1.9)
    text("CW")
    move(2.65, 2.9)
    text("CCW")
    move(5, 2.5)
    text("eofill")
    # Put some explanation at the top
    translate(0, 4.2)
    move(0, 0)
    fillColor(white)
    fillOn()
    lineOff()
    rectangle(8.5, 2)
    translate(0.5, 0)  # Left margin
    move(0, 1.3)
    textSize(0.2)
    text(
        "This demonstrates the differences between two PostScript filling methods."
    )
    move(0, 1.1)
    text(
        "eofill is even-odd fill:  an area is filled if a line from inside to infinity crosses an odd"
    )
    move(0, 0.9)
    text(
        "number of lines.  The default fill is non-zero winding, in which the direction of the "
    )
    move(0, 0.7)
    text("lines crossed is included in the sum.")
    s.close()
ShowDifferentFillTypes("out/fill_eofill.ps")
