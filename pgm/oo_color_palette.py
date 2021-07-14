'''
Generate an XML color palette for Open Office
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generates an Open Office color palette
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import colorsys
if 1:   # Custom imports
    try:
        # Used to generate PostScript output
        import g
    except ImportError:
        # Put in dummies to swallow the library calls
        def g(*p):
            pass
        g.portrait, g.inches = None, None
        g.inches = None
        (g.ginitialize, g.setOrientation, g.translate, g.push, g.pop, g.FillOn,
        g.FillColor, g.move, g.black, g.white, g.gray, g.circle,
        g.rtext,) = [g]*13
if 1:   # Global variables
    # Format for XML line
    fmt = '<draw:color draw:color="%s" draw:name="%s"/>\n'
def GetColorString(color, name):
    '''Return the HTML version of the color.  color is a tuple of
    three floating point numbers between 0 and 1.
    '''
    return "#%02x%02x%02x" % tuple(int(0xff*i) for i in color)
def RowOfColors(hue, name, y, X, dia, stream):
    '''For hue in [0, 360), plot 12 colors horizontally at vertical
    location y.  X is the x width of the plotting area.
    '''
    g.push()
    data = (
        # S = saturation in %, V = value in %
        #  S,  V
        (100, 25),
        (100, 35),
        (100, 45),
        (100, 60),
        (100, 75),
        (100, 100),
        (60, 100),
        (40, 100),
        (30, 100),
        (15, 100),
        (7, 100),
        (3, 100),
    )
    n = len(data)  # Number of columns
    g.translate(0, y)
    g.move(-X/(3*n), -0.04)
    g.rtext("%d %s" % (hue, name))
    g.FillOn()
    Y = -(y + 0.3)  # Bottom label location
    for i, (sat, val) in enumerate(data):
        x = i/n*X
        g.move(x, 0)
        c = colorsys.hsv_to_rgb(hue/360, sat/100, val/100)
        g.FillColor(c)
        g.circle(dia)
        s = "#%02x%02x%02x" % tuple(int(0xff*i) for i in c)
        stream.write(fmt % (s, name + str(i + 1)))
        if not hue:  # Label columns with saturation/value
            g.move(x, -(y + 0.3))
            if sat == 100:
                s = "Pure" if val == 100 else "V%d" % val
            elif val == 100:
                s = "S%d" % sat
            g.ctext(s)
    g.pop()
def CreateFile(stream):
    '''Generate a PostScript plot using the g library showing the
    color choices and their names.  stream is the stream to the XML
    data, so write that at the same time.
    '''
    script = open(__file__).read()
    # The following is used because we can't have the XML comment
    # strings explicitly in this script's text.
    start_of_comment = chr(0x3c) + "!" + "-"*2
    end_of_comment = "-"*2 + chr(0x3e)
    # Insert this python script into the XML file as a comment.
    stream.write('''<?xml version="1.0" encoding="UTF-8"?>
{start_of_comment}
{script}
{end_of_comment}
<ooo:color-table
    xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0"
    xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0"
    xmlns:xlink="http://www.w3.org/1999/xlink"
    xmlns:svg="http://www.w3.org/2000/svg"
    xmlns:ooo="http://openoffice.org/2004/office">
'''.format(**locals()))
    g.translate(1.5, 1)  # Locate origin
    X, Y = 7, 9  # Rectangle size in inches of drawing area
    #
    # The following hues were checked in the gimp and need to be
    # divided by 360 to get a suitable decimal value.  There are 24
    # hues, each separated by 15 units of hue.  Virtually no one will
    # agree about the naming, so pick your own names; I tried to find
    # short names (6 letters maximum; see the documentation) so they'll
    # fit in GUI boxes.
    #
    # Ordering:  I want the primary colors near the top, as they are
    # the ones I use the most.  Then they come in triplets of (roughly)
    # red/green/blue or magenta/yellow/cyan.
    #
    # These hues are linear in hue value, but whether those are good
    # choices or not probably depend on your monitor's rendering, what
    # other colors they're close to, and your perception.  For my
    # setup, the greens are hard to differentiate (mint looks very
    # close to green and aqua and cyan are close).
    hues = (
        (0, "red"),
        (120, "green"),
        (240, "blue"),

        (60, "yellow"),
        (180, "cyan"),
        (300, "rose"),

        (30, "orange"),
        (150, "sea"),
        (270, "purple"),

        (15, "coral"),
        (135, "forest"),
        (255, "indigo"),

        (285, "violet"),
        (45, "gold"),
        (165, "aqua"),

        (315, "mauve"),
        (75, "spring"),
        (195, "teal"),

        (330, "pink"),
        (90, "lime"),
        (210, "sky"),

        (345, "apple"),
        (105, "mint"),
        (225, "navy"),
    )
    n = len(hues)
    dy = Y/n
    # Generate the first row of gray stuff
    g.push()
    y, dia = Y, Y/(1.5*n)
    g.translate(0, y)
    g.FillOn()
    # I want black followed by white, the two colors I use the most.
    ncols = 12
    g.move(0, 0)
    g.FillColor(g.black)
    g.circle(dia)
    stream.write(fmt % ("#000000", "black"))
    dx = X/ncols
    g.move(dx, 0)
    g.FillColor(g.white)
    g.circle(dia)
    stream.write(fmt % ("#ffffff", "white"))
    # Remaining gray values
    values = (10, 25, 50, 60, 70, 80, 90, 95, 97, 99)
    for i in range(2, 12):
        x = i*dx
        g.move(x, 0)
        c = colorsys.hsv_to_rgb(0, 0, values[i - 2]/100)
        g.FillColor(c)
        g.circle(dia)
        s = "#%02x%02x%02x" % tuple(int(0xff*i) for i in c)
        stream.write(fmt % (s, "gray" + str(i - 1)))
    g.pop()
    Y -= dy
    # Generate each row of hues
    for i, (hue, name) in enumerate(hues):
        y = Y - i*dy
        RowOfColors(hue, name, y, X, dia, stream)
    stream.write("</ooo:color-table>\n")
if __name__ == "__main__":
    name = "ideal_palette"
    stream = open(name + ".soc", "w")
    g.ginitialize(open(name + ".ps", "w"))
    g.setOrientation(g.portrait, g.inches)
    CreateFile(stream)
