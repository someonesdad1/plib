"""
Draw a grid of 1 inch squares, 0.1 inch tick marks, and label things.
"""

from g import *


def AddTickMarks(tick_interval, tick_length, skip=0, down=0):
    """Add 10 tick marks with a wider fifth one.  This assumes that
    the origin is at the beginning point we need to mark and that the
    tick marks start along the positive x axis between 0 and 1 and go
    down in the y direction.
    """
    if down:
        tick_length = -tick_length
    for i in range(1, 10):
        if skip:
            skip = skip - 1
            continue
        x = i / 10.0
        move(x, 0)
        if i == 5:
            rline(0, tick_length * 1.5)
        else:
            rline(0, tick_length)


def Grid(file):
    """Draw a grid of 1 inch squares."""
    s = Setup(file, portrait, inches)
    translate(0.25, 0.5)  # Center the grid on the page (assumes a sheet
    # of paper of 8.5" by 11" (letter size).
    text_size = 11.0 / 72  # Use an 11 point font
    textSize(text_size)
    textName(SansBold)
    lineColor(red)
    textColor(green)
    lineWidth(0.01)
    box_width = 8
    box_height = 10
    delta = 0.02  # Offset text just a little from the lines
    tick_mark_length = 0.05
    # Draw the horizontal lines
    for i in range(box_height + 1):
        move(0, i)
        rline(box_width, 0)
        move(tick_mark_length + 2 * delta, i + delta)
        text("%d" % i)
        # Put in tick marks
        if i < box_height:
            push()
            translate(0, i)
            rotate(90)
            AddTickMarks(tick_mark_length, 0.05, down=1)
            pop()
    # Draw the vertical lines
    for i in range(box_width + 1):
        move(i, 0)
        rline(0, box_height)
        # Draw the rotated characters.  We push() the current graphics state
        # so that the rotation won't affect the next grid line.
        push()
        translate(i, 0)
        rotate(-90)
        move(delta, delta - text_size / 2.5)
        if i != 0:  # Don't do the zero, since it will overlap with the other
            text("%d" % i)
        pop()
        # Put in tick marks
        if i < box_width:
            push()
            translate(i, 0)
            AddTickMarks(tick_mark_length, 0.05, 1 * (i == 0))
            pop()
    # Label the page so we know the orientation; put it on a white box
    text_size = 2 * text_size
    textSize(text_size)
    fillOn()
    x = 3.25
    y = 5
    delta = 0.25
    lineWidth(0.04)
    lineColor(blue)
    fillColor(white)
    move(x - delta, y - delta)
    roundedRectangle(2.0, 0.5, 0.3)
    move(x - delta / 3, y - text_size / 2.5)
    textColor(green)
    text('8"x10" grid')
    s.close()


Grid("out/grid.ps")
