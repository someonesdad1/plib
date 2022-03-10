'''
Generate different grids of lines to simulate engineering drawing
paper.
'''
from g import *
from math import modf, fabs
eps = 1e-6
debug = 0
# Line widths in inches
line_heavy  = 0.0075
line_medium = 0.005
line_light  = 0.0025
heavy_color  = grey(.7)
medium_color = grey(0.8)
light_color = grey(0.9)
def GrayOffset(g):
    global heavy_color, medium_color, light_color
    heavy_color = grey(0.7 - g)
    medium_color = grey(0.8 - g)
    light_color = grey(0.9 - g)
# Use colors
if 1:
    h = 0.75
    s = 0.25
    b = 1
    heavy_color = hsv2rgb(h, s, b)
    medium_color = hsv2rgb(h, s / 1.2, b)
    light_color = hsv2rgb(h, s / 1.5, b)
if debug:
    heavy_color = red
    medium_color = blue
    light_color = grey(0.5)
def IsMinor(x):
    '''If the fractional part is 0.5, return true; otherwise, return 0.'''
    fp, ip = modf(x)
    if fabs(fp - 0.5) < 1e-4:
        return 1
    else:
        return 0
def IsMajor(x):
    '''If the value is a whole number of inches, return 1.  Otherwise,
    return 0.
    '''
    fp, ip = modf(x)
    if fp < 1e-4 or fp > (1 - 1e-6):
        return 1
    else:
        return 0
def Grid(file, increment=0.2):
    '''Draw a grid of 1 inch squares.'''
    s = Setup(file, portrait, inches)
    translate(0.25, 0.2)  # Center the grid on the page (assumes a sheet
    # of paper of 8.5" by 11" (letter size).
    box_width = 8
    box_height = 10
    # Draw the horizontal lines
    y = 0.0
    while y <= box_height:
        move(0, y)
        if IsMajor(y):
            lineColor(heavy_color)
            lineWidth(line_heavy)
        elif IsMinor(y):
            lineColor(medium_color)
            lineWidth(line_medium)
        else:
            lineColor(light_color)
            lineWidth(line_light)
        rline(box_width, 0)
        y = y + increment
    # Draw the vertical lines
    x = 0.0
    while x <= box_width + eps:
        move(x, 0)
        if IsMajor(x):
            lineColor(heavy_color)
            lineWidth(line_heavy)
        elif IsMinor(x):
            lineColor(medium_color)
            lineWidth(line_medium)
        else:
            lineColor(light_color)
            lineWidth(line_light)
        rline(0, box_height)
        x = x + increment
    s.close()
def PageLines(file, increment=0.2):
    '''Draw vertical lines on a page.  This can be used to print on letter
    paper to make small booklets.
    '''
    s = SetUp(file, portrait, inches)
    box_width = 8.5
    box_height = 11
    eps = 0.001
    dx = 0.2
    # Balance the lines on the page
    hx = box_width / dx - int(box_width / dx)
    translate(-hx / 2, 0)
    # Draw the vertical lines
    x = 0.0
    lineColor(light_color)
    lineWidth(line_light)
    while x <= box_width + dx + eps:
        move(x, 0)
        rline(0, box_height)
        x = x + increment
    s.close()
def PageGrid(file, increment=0.2):
    '''Draw a simple grid on a page.  This can be used to print on letter
    paper to make small booklets.
    '''
    s = SetUp(file, portrait, inches)
    box_width = 8.5
    box_height = 11
    eps = 0.001
    dx = dy = increment
    # Balance the lines on the page
    hx = box_width / dx - int(box_width / dx)
    push()
    translate(-hx / 2, 0)
    # Draw the vertical lines
    x = 0.0
    lineColor(light_color)
    lineWidth(line_light)
    while x <= box_width + dx + eps:
        move(x, 0)
        rline(0, box_height)
        x += dx
    pop()
    # Draw the horizontal lines
    y = 0.0
    lineColor(light_color)
    lineWidth(line_light)
    while y <= box_height + eps:
        move(0, y)
        rline(box_width, 0)
        y += dy
if 1:
    Grid("out/eng_grid1_1.ps", 0.1)
    GrayOffset(0.1)
    Grid("out/eng_grid1_2.ps", 0.1)
    GrayOffset(0.2)
    Grid("out/eng_grid1_3.ps", 0.1)
if 1:
    Grid("out/eng_grid21.ps")
    GrayOffset(0.1)
    Grid("out/eng_grid2_2.ps", 0.1)
    GrayOffset(0.2)
    Grid("out/eng_grid2_3.ps", 0.1)
PageLines("out/lines.ps")
PageGrid("out/grid.ps")
