'''
This shows that you can change the font color in the middle of a
sentence.  It also demonstrates that the text() function puts text at
the end of the previous text, assuming the PostScript current point
hasn't changed.  This is advantageous for placing text, but will
generate an error in the g.py module's use if you try to draw
something that uses the current point.  This happens because
PostScript keeps track of the current point, but we have no way of
asking PostScript where the current point is.  Thus, remember to issue
a move() command before the next drawing command.
'''
from g import *
import random
import sys
rand = random.random # Convenience name for a random number generator that 
                     # returns a uniformly-distributed random number between
                     # 0.0 and 1.0.
def RadialText(file):
    s = Setup(file, portrait, inches)
    translate(4.25, 5.5)  # Put origin at middle of page
    textName(UniversCondensedBold)
    textSize(0.25)  # 1/4 inch high letters
    radius = 1  # The radius text will start at
    angle_step = 20  # Text at increments of this radial
    # Place the text on radial arcs
    push()
    for ix in range(0, 360, angle_step):
        rotate(angle_step)
        move(radius, 0)
        textColor(navy)
        text("Navy ")
        textColor(blue)
        text("blue ")
        textColor(deepskyblue)
        text("deepskyblue ")
        textColor(lightblue)
        text("lightblue")
    pop()
    # Put a big Dingbat in the center
    textName(Dingbats)
    textSize(2)  # Make a 2 inch high character
    x = 1
    line(-x, 0, x, 0)  # Draw some crosshairs
    line(0, -x, 0, x)
    textColor(dodgerblue)
    move(-0.85, -0.62)  # I fiddled until it was correct
    text("O")
    s.close()
RadialText("out/radial_text.ps")
