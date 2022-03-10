''' 

This file produces a drawing similar to the demo picture included with the
piddle (also called sping) package.  I first took a look at piddle before
deciding to implement the g.py functionality.  piddle would be an excellent
choice if you wanted to be able to produce drawings in a variety of output
formats.  The g.py module, in contrast, only produces PostScript output.
The g.py module requires more code to do the same work as piddle, at least
for this drawing.

The piddle code for the picture is:

canvas.defaultLineColor = Color(0.7,0.7,1.0)    # (light blue)
canvas.drawLines(map(lambda i:(i*10,0,i*10,300), range(30)))
canvas.drawLines(map(lambda i:(0,i*10,300,i*10), range(30)))
canvas.defaultLineColor = black         
canvas.drawLine(10,200, 20,190, color=red)
canvas.drawEllipse(130,30, 200,100, fillColor=yellow, edgeWidth=4)
canvas.drawArc(130,30, 200,100, 45,50, fillColor=blue, edgeColor=navy, 
                edgeWidth=4)
canvas.defaultLineWidth = 4
canvas.drawRoundRect(30,30, 100,100, fillColor=blue, edgeColor=maroon)
canvas.drawCurve(20,20, 100,50, 50,100, 160,160)
canvas.drawString("This is a test!", 30,130, Font(face="times",size=16,bold=1), 
             color=green, angle=-45)
polypoints = [(160,120), (130,190), (210,145), (110,145), (190,190)]
canvas.drawPolygon(polypoints, fillColor=lime, edgeColor=red, edgeWidth=3, 
                   closed=1)
canvas.drawRect(200,200,260,260, edgeColor=yellow, edgeWidth=5)
canvas.drawLine(200,260,260,260, color=green, width=5)
canvas.drawLine(260,200,260,260, color=red, width=5)
canvas.flush()
'''
from g import *
def DrawBlueLines():
    push()
    lineColor(lightblue)
    lw = 0.02
    lineWidth(lw)
    increment = 0.2
    width = 7.4
    height = 10
    # Draw horizontal lines
    y = 2.0
    while y <= height:
        line(0, y, width, y)
        y = y + increment
    # Draw vertical lines
    x = 0
    y = 1.8
    while x <= width:
        line(x, y, x, height)
        x = x + increment
    pop()
def RoundedRectangle():
    push()
    lineColor(maroon)
    fillColor(navy)
    fillOn()
    lineWidth(0.1)
    move(0.6, 7.4)
    roundedRectangle(2, 2, 0.4)
    pop()
def ShortRedLine():
    push()
    lineColor(red)
    line(0.2, 5.2, 0.4, 5.4)
    pop()
def BlackPath():
    push()
    lineWidth(0.1)
    lineColor(black)
    newPath()
    move(0.4, 10 - 0.4)
    pathAdd((2.5, 9, 1.6, 7, 3.75, 6), path_bezier)
    drawPath()
    pop()
def Pie():
    push()
    x_center = 4
    y_center = 8.4
    diameter = 2
    # Draw yellow circle
    fillColor(yellow)
    fillOn()
    lineWidth(0.1)
    lineColor(black)
    move(x_center, y_center)
    circle(diameter)
    # Draw navy wedge
    fillColor(navy)
    lineOff()
    newPath()
    pathAddPoint(x_center, y_center)
    pathAdd((x_center, y_center, diameter / 2.0, 45, 100), path_arc_ccw)
    pathClose()
    fillPath()
    pop()
def Star():
    push()
    translate(3.75, 6)
    fillColor(limegreen)
    lineColor(red)
    lineWidth(0.1)
    fillOn()
    lineOn()
    newPath()
    # Construct the points for a 5-pointed star
    from math import sin, cos, pi
    r = 1
    c = pi / 180
    points = [
        (r * cos(20 * c), r * sin(20 * c)),
        (r * cos(230 * c), r * sin(230 * c)),
        (r * cos(90 * c), r * sin(90 * c)),
        (r * cos(310 * c), r * sin(310 * c)),
        (r * cos(160 * c), r * sin(160 * c)),
    ]
    pathAddPoints(points)
    pathClose()
    p = getPath()
    eoFillPath(p)
    drawPath(p)
    pop()
def DrawText():
    push()
    translate(0.6, 6.8)
    textName(SerifBold)
    textSize(0.5)
    textColor(green)
    rotate(-45)
    move(0, 0)
    text("This is a test!")
    pop()
def DrawBox():
    push()
    x = 4.6
    y = 3
    move(x, y)
    lineColor(yellow)
    lineWidth(0.1)
    lineOn()
    fillOff()
    s = 1.8
    rectangle(s, s)
    # Add the colored lines; note the change of the cap type
    lineCap(cap_projecting)
    lineColor(green)
    line(x, y, x + s, y)
    lineColor(red)
    line(x + s, y, x + s, y + s)
    pop()
if __name__ == "__main__": 
    file = "out/piddle_demo.ps"
    Setup(file, orientation=portrait, units=inches)
    margin = 0.5
    translate(margin, margin)
    DrawBlueLines()
    ShortRedLine()
    RoundedRectangle()
    BlackPath()
    Pie()
    Star()
    DrawText()
    DrawBox()
