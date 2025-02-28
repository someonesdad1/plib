"""
This example makes two different drawings that have the same color in the
center box, but different surrounding colors.  If you display both
drawings at the same time, you'll see that the central box colors don't
look quite the same, even though they are.  This is a well-known
psychological effect.
"""

from g import *


# Set the following variable to nonzero if you want to send the generated
# files directly to a PostScript printer.  Otherwise, set it to zero.
def FirstFile(file):
    os = Setup(file, portrait, inches)
    translate(4.25, 5.5)
    fillOn()
    lineOff()
    fillColor(black)
    center_color = lightblue
    push()
    # Draw a black background
    s = 12
    move(-s, -s)
    rectangle(2 * s, 2 * s)
    # Draw a light colored box inside of a dark one
    fillColor(navy)
    s = 3
    move(-s, -s)
    rectangle(2 * s, 2 * s)
    fillColor(center_color)
    s = 1.5
    move(-s, -s)
    rectangle(2 * s, 2 * s)
    pop()


def SecondFile(file):
    os = SetUp(file, portrait, inches)
    translate(4.25, 5.5)
    fillOn()
    lineOff()
    center_color = lightblue
    # Leave the background white and draw a yellow box inside of
    # a pink one
    fillColor(cyan)
    s = 3
    move(-s, -s)
    rectangle(2 * s, 2 * s)
    fillColor(center_color)
    s = 1.5
    move(-s, -s)
    rectangle(2 * s, 2 * s)
    os.close()


FirstFile("out/center_contrast1.ps")
SecondFile("out/center_contrast2.ps")
