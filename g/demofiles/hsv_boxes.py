'''
Draw a rectangular array of boxes on the screen that are filled with
colors specified by HSV values, demonstrating the use of the hsv2rgb
conversion function.  H is hue, S is saturation, V is value (all
numbers between 0 and 1).
'''
from g import *
def HSVColoredBoxes(ncol, nrow, file):
    os = Setup(file, portrait, points)
    # Set the coordinate system so that the origin is the top left corner of
    # the paper, x increases to the right, and y increases down the page.
    # Because of the reflection, this is a left-handed coordinate system,
    # so don't print any text...
    translate(1, 789)
    scale(1, -1)
    scale(610, 785)
    lineWidth(0.001)
    fillOn()
    lineOn()
    # lineOff()
    if 0:
        # Draw a black background
        fillColor(black)
        lineOff()
        move(-1, -1)
        rectangle(3, 3)
    else:
        # Leave the background white
        fillColor(white)
        lineColor(black)
    border_factor = 0.85
    v = 1
    for row in range(nrow):
        for col in range(ncol):
            x = col * 1.0 / ncol
            y = row * 1.0 / nrow
            h, s = y, 1 - x  # 1-x puts the saturated value at the left
            r, g, b = hsv2rgb(h, s, v)
            fillColor((r, g, b))
            move(x, y)
            rectangle(
                border_factor * 1.0 / nrow, border_factor * 1.0 / ncol
            )
    os.close()
HSVColoredBoxes(8, 8, "out/hsv_boxes.ps")
