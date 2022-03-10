'''
Draw a rectangular array of boxes that are filled with randomly-selected
colors.
'''
from g import *
import random
# Convenience name for a random number generator that returns a
# uniformly-distributed random number between 0.0 and 1.0.
rand = random.random  
def RandomColoredBoxes(ncol, nrow, file):
    # Initialize the graphics library by giving it a file to put its
    # drawing output into.  Also set the drawing units to points.
    s = Setup(file, orientation=portrait, units=inches)
    random.seed(11549)  # Get the same sequence of random numbers
    # First scale the screen conveniently.  We'll have the x direction
    # going to the right and the y direction increasing downwards.  The
    # origin will be the top left corner.  This requires a translation
    # and a reflection about the x axis.
    translate(0, 11)  # Put origin at top left corner
    scale(1, -1)  # Reflection:  change the direction of the Y axis
    # Make the screen coords go from (0,0) to (1,1)
    scale(8.5, 11.0)
    # Make the screen all black by drawing a rectangle filled with black
    # that is larger than the displayable area.
    fillOn()
    move(0, 0)
    rectangle(1, 1)
    fillOff()
    # Draw a box around the screen area, which has been anistropically sized
    # to extend from (0,0) (upper left corner) to (1,1) (lower right corner).
    move(0, 0)
    lineColor(red)
    lineWidth(0.005)  # If you forget to resize the line width, you'll get
    # what appears to be a filled rectangle.  In reality,
    # it's just that the line width is very wide (in this
    # case, 1.0).
    rectangle(1, 1)  # Draws a box around the whole screen area
    lineColor(black)
    fillType(solid_fill)
    fillOn()
    rand = random.random  # Random number generator in python library
    random.seed(8)  # Remove this line to see a different
    # coloring each time.
    border_factor = 0.75
    for row in range(nrow):
        for col in range(ncol):
            x = (
                col * 1.0 / ncol
            )  # The 1.0 is there to make this calculation
            # be done as floating point; otherwise,
            # since row and nrow are integers, x would
            # be zero, since nrow is always greater
            # than row.
            y = row * 1.0 / nrow
            # Randomly select a color
            r = rand()
            g = rand()
            b = rand()
            fillColor((r, g, b))
            move(x, y)
            rectangle(
                border_factor * 1.0 / nrow, border_factor * 1.0 / ncol
            )
    s.close()
RandomColoredBoxes(20, 20, "out/colored_boxes.ps")
