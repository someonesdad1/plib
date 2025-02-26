"""
Make a 4x6 card

    Contains year, title, date, and an engineering grid.  This is intended
    to be used as project/idea cards in the shop.  The output file is
    suitable for printing on a 4x6 card when put in the manual feed tray of
    a LaserJet 4050.

    The grid is on a 0.1 inch spacing.
"""

from g import *
from math import modf, fabs
import time
import sys

eps = 1e-6
debug = 0
heavy_color = grey(0.7)
medium_color = grey(0.8)
light_color = grey(0.9)


def IsMinor(x):
    "If the fractional part is 0.5, return true; otherwise, return 0"
    fp, ip = modf(x)
    if fabs(fp - 0.5) < 1e-4:
        return 1
    else:
        return 0


def IsMajor(x):
    """If the value is a whole number of inches, return 1.  Otherwise,
    return 0.
    """
    fp, ip = modf(x)
    if fp < 1e-4 or fp > (1 - 1e-6):
        return 1
    else:
        return 0


def Grid(file, increment=0.2):
    "Draw a grid of 1 inch squares"
    s = Setup(file, portrait, inches)
    lineWidth(0.005)
    box_width = 4
    box_height = 6
    # We'll assume a letter sized piece of paper
    paper_width = 8.5
    paper_height = 11.0
    top_margin = 0.20
    X = (paper_width - box_width) / 2.0
    Y = paper_height - box_height - top_margin
    translate(X, Y)
    # Draw the horizontal lines
    y = 0.0
    while y <= box_height:
        move(0, y)
        if IsMajor(y):
            lineColor(heavy_color)
        elif IsMinor(y):
            lineColor(medium_color)
        else:
            lineColor(light_color)
        rline(box_width, 0)
        y = y + increment
    # Draw the vertical lines
    x = 0.0
    while x <= box_width + eps:
        move(x, 0)
        if IsMajor(x):
            lineColor(heavy_color)
        elif IsMinor(x):
            lineColor(medium_color)
        else:
            lineColor(light_color)
        rline(0, box_height)
        x = x + increment
    # Put in labels
    translate(0, Y + 1 + top_margin)
    move(0, 0)
    textName(SansBold)
    textSize(0.2)
    move(0, -0.2)
    # text("Title" + (" " * 54) + "Date")
    # Put in year in black box
    translate(-0.15, -0.2)
    rotate(-90)
    textSize(0.3)
    textColor(white)
    fillColor(black)
    fillOn()
    x = top_margin
    y = box_width - top_margin
    delta = 0.05
    move(x - delta, y - delta)
    rectangle(0.75, 0.3)
    move(x, y)
    if len(sys.argv) > 1:
        text(sys.argv[1])
    else:
        text(time.strftime("%Y"))
    s.close()


Grid("out/4x6_card.ps", 0.1)
