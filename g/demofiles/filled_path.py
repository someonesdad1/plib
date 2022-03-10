'''
Draw a filled path.  This path consists of intersecting subpaths, two
triangles and a square.  Since they intersect, you'll see that some of
the path doesn't get filled.  We also show how using getPath() can get
a copy of the path to use later; we go to a new page and draw the same
path with different colors.  To understand why some areas get filled
and some don't, refer to "non-zero winding" in the reference manual
glossary in the doc directory.
'''
from g import *
def FilledPath(file):
    s = SetUp(file, portrait, inches)
    lineWidth(0.01)
    newPath()
    # Make a triangle
    pathAddPoint(1, 1)
    pathAddPoint(1, 7)
    pathAddPoint(4, 1)
    pathClose()
    # Make another triangle
    pathAddPoint(7, 6)
    pathAddPoint(0.5, 6)
    pathAddPoint(7, 4)
    pathClose()
    # Make a square
    pathAddPoint(0.5, 5)
    pathAddPoint(5.5, 5)
    pathAddPoint(5.5, 10)
    pathAddPoint(0.5, 10)
    # Note the missing pathClose() still allows the path to be closed, but
    # when the path is drawn, the last edge of the square is missing.
    # Get a copy of the path so we can use it again (filling the path causes
    # it to be deleted as the current path).
    p = getPath()
    # Fill the path
    fillColor(grey(0.8))
    fillOn()
    fillPath()
    # Draw a border
    setPath(p)
    lineColor(blue)
    lineWidth(0.05)
    drawPath()
    # Go to a new page and draw the path again, but use different colors.
    # We'll also use a reflection to change the shape.
    newPage()
    translate(8.5, 0)
    f = 1
    scale(-f, f)  # Reflect about the y axis
    lineWidth(0.05)
    fillColor(skyblue)
    fillPath(p)
    lineColor(red)
    drawPath(p)
    # We're finished
    s.close()
FilledPath("out/filled_path.ps")
