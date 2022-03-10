'''
Interesting optical illusion.  The gray rectangles are the same shade of
gray.
'''
from g import *
def Draw():
    push()
    translate(1, 0.5)
    n, w, h = 7, 7, 9
    # Black rectangle at bottom
    FillColor(black)
    FillOn()
    LineOff()
    move(0, 0)
    rectangle(w, h/2)
    # Gray rectangle
    move(w/3, 0)
    FillColor(gray(0.5))
    rectangle(w/3, h)
    # White rectangles
    dy = h/(4*n)
    FillColor(white)
    for i in range(0, 2*n + 2, 2):
        move(0, i*dy)
        rectangle(w, dy)
    # Black rectangles
    translate(0, (2*n + 1)*dy)
    FillColor(black)
    for i in range(0, 2*n, 2):
        move(0, i*dy)
        rectangle(w, dy)
    pop()
if __name__ == "__main__": 
    SetUp("out/white.ps", orientation=portrait, units=inches)
    Draw()
    # Title
    move(8.5/2, 10)
    TextSize(0.3)
    TextName(SansBold)
    ctext("Optical Illusion")
    move(8.5/2, 9.7)
    TextName(Sans)
    TextSize(0.15)
    ctext("Gray areas are same shade")
