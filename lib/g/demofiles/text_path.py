"""
Demonstrates text along a path.
"""

from g import *
from math import sqrt

Setup("out/text_path.ps", orientation=landscape, units=inches)
translate(1, 1)
move(0, 0)
# Create an elliptical path
NewPath()
a, b = 6, 3  # Major, minor diameters
n = 20
dx = a / (n + 1)
for i in range(n):
    x = i * dx
    y = sqrt(b**2 * (1 - (x / a) ** 2))
    PathAdd((x, y))
p = GetPath()
LineWidth(0.001)
LineType(little_dash)
DrawPath(p)
s = "This is a string printing along an elliptical arc"
t = 0.2
TextSize(t)
TextColor(red)
TextPath(s, p, 0.5)
move(1, 2)
TextColor(blue)
text("Here's a fraction:  ")
TextFraction(31, 47)
# Text along a circle
a, b, d = 7, 6, 2
TextSize(0.15)
move(a, b)
TextColor(black)
TextCircle("Text along a circle at 90 deg", d)
LineColor(darkgreen)
LineType(solid_line)
LineWidth(0.01)
move(a, b)
circle(d)
b = 4
move(a, b)
TextColor(black)
TextCircle("Text along a circle at 0 deg", d, 0)
LineColor(blue3)
move(a, b)
circle(d)
b = 2
move(a, b)
TextColor(black)
TextCircle("Text along a circle at 270 deg inside", d, 270, inside=yes)
LineColor(maroon)
move(a, b)
circle(d)
