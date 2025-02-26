"""
Demonstrates a simple gradient file of a path.
"""

from g import *

SetUp("out/gradient_fill.ps", landscape, inches)
translate(1, 1)
FillOn()
FillColor(lightblue)
FillType(gradient_fill)
a, f = 5, 50
GradientFill(lightyellow, factor=f)
# Draw a square
NewPath()
PathAdd((0, 0))
PathAdd((a, 0))
PathAdd((a, a))
PathAdd((0, a))
PathClose()
p = GetPath()
FillPath(p)
# Draw a gradient-filled circle with heavy black border
FillColor(red)
GradientFill(yellow, factor=f)
LineWidth(0.05)
move(7, 5)
circle(3)
