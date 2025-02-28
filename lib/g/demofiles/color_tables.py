"""
The following functions help print a table of the named color values
used in g.py.  This is an excellent example of what the g.py module
and python are good at, since it was a task that cried out for
automation (I certainly didn't want to place every one of the boxes by
hand).  There are around 140 different named colors and I wanted a
table that showed the colors that I could print out and have as a
handy reference.  I also wanted the colors sorted by both their name
(so if I wanted to know what the color darkkhaki looked like, I could
find it in an alphabetical list) and their color type (so that I could
see all colors that were predominantly blue grouped together).
Generating the first page (sorted by name) was easy.  But the second
display (grouped by color) took more work to get the colors sorted as
needed.  Python's data containers (lists in this case) are perfect for
such tasks.

In the ColorChart() function, try generating charts using both white
and black backgrounds (change the black_background variable).  You'll
find that the black background helps you distinguish between dark
colors better and the white backgound makes the differences in the
light colors more apparent.  Don't be surprised if there's a lot of
difference between what you see on the screen and what you see on your
printer -- accurate color rendition is a complicated topic.

This is also a good example of why using python gives subtle power,
since the code-test-fix sequence is so quick.  I generated the first
page showing the colors in boxes with their text labels in perhaps 10
minutes; it wasn't perfect, since I had forgotten that reflection to
get a convenient coordinate system, resulting in mirror-image text.
But that was quickly fixed with a few iterations and playing around.
I probably had what I wanted in half an hour or so, since I could make
a change to the python code, run the script in another window, then
switch the focus to the GSview window and see the new result, all in a
couple of seconds (GSview has a nice option to automatically reload a
file if it changes).  This code-test-fix method enables quick
development.
"""

import sys
from g import *


def BlackBackground():
    """Fill the whole drawing area with black."""
    push()
    reset()
    move(-10, -10)
    fillColor(black)
    fillOn()
    rectangle(1000, 1000)
    pop()


def GetColors():
    """Return a list of lists relating color name to the RGB tuple.
    The form of the list is:
        [
            [ colorname1, (r, g, b), 0],
            [ colorname2, (r, g, b), 0],
            ...
        ]
    The trailing 0 is used as a flag to indicate when the rectangle
    with color shouldn't be printed.
    """
    G = globals()
    colors = []
    for key in G.keys():
        element = G[key]
        if type(element) == type(()) and len(element) == 3:
            colors.append([key, element, 0])
    return colors


def ColorChartByName(file):
    """Print a color chart with the colors sorted by name."""
    colors = list(GetColors())
    colors.sort()
    ColorChart(file, colors)


def ColorChart(file, colors):
    """For each color defined in the g.py file, draw a box, fill it with
    that color, then label the box with the color name.  The colors are
    in the colors list and are in the order they should be printed.  The
    structure of the colors list is:
        [
            [colorname, (r, g, b), 0],
            [colorname, (r, g, b), 0],
            ...
        ]
    If you'd like to see the chart drawn with a black background, set
    black_background to true.
    """
    black_background = no
    # Initialize our graphics environment
    s = Setup(file, portrait, inches)
    lineWidth(0.01)
    if black_background == yes:
        lineColor(white)
        textColor(white)
        BlackBackground()
    else:
        lineColor(black)
        textColor(black)
    # Write a title.  Here's a case where python's sensitivity to indenting
    # is constraining:  I'd like to indent the code between the push and
    # pop to emphasize that this won't affect the graphics state and make
    # it easy to see this chunk of code.
    push()
    textName(HelveticaBold)
    textSize(0.25)
    move(1.7, 10.6)
    text("Color names for use with the g.py module")
    pop()
    # Put the origin at the upper left corner of the page and make the
    # y coordinate increasing down the page.  Note this uses a reflection
    # which will cause mirrored text.
    translate(0, 10.75)
    scale(1, -1)
    # Now move the origin down and over for comfortable margins.
    translate(0.4, 0.4)
    # Set up our variables
    column_spacing = 1.3
    row_spacing = 0.20
    boxes_per_column = 50  # When to move to the next column
    box_width = 0.3
    box_height = 0.8 * row_spacing
    textSize(0.12)
    textName(HelveticaNarrow)
    fillOn()
    lineOn()
    for ix in range(len(colors)):  # For every color in the list ...
        name = colors[ix][0]
        color = colors[ix][1]
        no_box = colors[ix][2]
        row = ix % boxes_per_column  # The mod function
        column = ix // boxes_per_column  # Integer division
        # Locate where to draw the box
        x = column * column_spacing
        y = row * row_spacing
        move(x, y)
        if black_background == yes:
            lineColor(white)
        else:
            lineColor(black)
        fillColor(color)
        if not no_box:
            rectangle(box_width, box_height)
        # Label the box.  Since we're in a coordinate system with a
        # reflection in it, translate to the desired printing point,
        # then undo the reflection.  We push/pop the graphics state so
        # we don't mess up the current one.
        push()
        if black_background == yes:
            lineColor(white)
        else:
            lineColor(black)
        translate(x, y)
        # The constants used in the following line come from trying
        # different ones and seeing what works best.
        move(box_width + 0.05, 0.65 * row_spacing)
        scale(1, -1.2)  # Not only reflect, but stretch the font up a bit
        text(name)
        pop()
    s.close()


def IsAGrey(color):
    r, g, b = color
    if r == g and r == b and g == b:
        return 1
    else:
        return 0


def IsARed(color):
    r, g, b = color
    if r > g and r > b:
        return 1
    else:
        return 0


def IsAGreen(color):
    r, g, b = color
    if g > r and g > b:
        return 1
    else:
        return 0


def IsABlue(color):
    r, g, b = color
    if b > r and b > g:
        return 1
    else:
        return 0


def IsAYellow(color):
    r, g, b = color
    if r == g and r > b:
        return 1
    else:
        return 0


def IsACyan(color):
    r, g, b = color
    if g == b and g > r:
        return 1
    else:
        return 0


def IsAMagenta(color):
    r, g, b = color
    if r == b and r > g:
        return 1
    else:
        return 0


def Nm(name):
    """Return a color with the flag element set to true to indicate that
    only the name should be printed.
    """
    return [[name, (0, 0, 0), 1]]


def SortByIntensity(colors):
    """The incoming list is of the following form:
        [
            [name, (r, g, b), 0],
            [name, (r, g, b), 0],
            ...
        ]
    Calculate the intensity of each (r, g, b) tuple by summing the squares,
    then storing the sum as a new first element of the element.  When the
    sort method is called, it will sort on this number.  Then remove the
    intensity from each element.  The form of the list we'll sort is:
        [
            [intensity, name, (r, g, b), 0],
            [intensity, name, (r, g, b), 0],
            ...
        ]
    """
    for ix in range(len(colors)):
        element = colors[ix]
        r, g, b = element[1]
        # Summing the squares gives a more pleasing sort than just summing
        # the numbers.
        intensity = r * r + g * g + b * b
        colors[ix] = [intensity] + element
    colors.sort()
    # Now delete the intensity element
    for ix in range(len(colors)):
        del colors[ix][0]


def MoveColor(name, from_list, to_list):
    """Find the element in from_list that has name as its first element
    and move it to the to_list.
    """
    for ix in range(len(from_list)):
        element = from_list[ix]
        if name == element[0]:
            del from_list[ix]
            to_list.append(element)
            return
    raise "Element not found"


def ColorChartByColor(file):
    """Print a color chart with the colors sorted by color."""
    colors = GetColors()
    greys = []
    reds = []
    greens = []
    blues = []
    yellows = []
    cyans = []
    magentas = []
    others = []
    # Partition each element into one of the categories.
    for element in colors:
        color = element[1]
        if IsAGrey(color):
            greys.append(element)
            continue
        if IsAYellow(color):
            yellows.append(element)
            continue
        if IsACyan(color):
            cyans.append(element)
            continue
        if IsAMagenta(color):
            magentas.append(element)
            continue
        if IsARed(color):
            reds.append(element)
            continue
        if IsAGreen(color):
            greens.append(element)
            continue
        if IsABlue(color):
            blues.append(element)
            continue
        other.append(element)
    # There should be no elements in the others list
    if len(others) > 0:
        raise "Had some uncategorized colors"
    # The following conditional section is a hand-tuned judgement of which
    # colors should be moved.  For example, a red was defined to be a color
    # which had the red number higher than the other two.  This definition
    # causes hotpink and orchid to be put in the red category; however,
    # you may agree with me that it probably should be under the magenta
    # category (at least, that how it appears on the LCD screen of my
    # laptop which I'm working on).  Leave the conditional commands out
    # and you'll see the mathematically correct sort; include it and you'll
    # see how I judged where the colors should be grouped.  At first, I
    # moved deeppink from the reds to the magentas, but deeppink looked out
    # of place amongst the magentas too.  Orange is a combination of red
    # and yellow; should it be amongst the reds or the yellows?  Clearly,
    # such a classification can only be pushed so far...
    #
    # Another way to do this sorting would be to sort using a hue,
    # saturation, brightness ordering, but I didn't have the formulas
    # handy to make the conversion.
    if 1:
        # MoveColor("orchid",              reds, magentas)
        MoveColor("hotpink", reds, magentas)
        MoveColor("lightpink", reds, magentas)
        MoveColor("pink", reds, magentas)
        MoveColor("darkgoldenrod", reds, yellows)
        MoveColor("goldenrod", reds, yellows)
        MoveColor("gold", reds, yellows)
        # MoveColor("khaki",               reds, yellows)
        MoveColor("darkkhaki", reds, yellows)
        MoveColor("tan", reds, yellows)
        MoveColor("burlywood", reds, yellows)
        MoveColor("palegoldenrod", reds, yellows)
        MoveColor("wheat", reds, yellows)
        MoveColor("papayawhip", reds, yellows)
        MoveColor("lemonchiffon", reds, yellows)
        MoveColor("mediumaquamarine", greens, cyans)
        # MoveColor("mediumturquoise",     greens, cyans)
        # MoveColor("turquoise",           greens, cyans)
        # MoveColor("darkorchid",          blues, magentas)
        # MoveColor("mediumorchid",        blues, magentas)
        MoveColor("mediumpurple", blues, magentas)
        # MoveColor("darkturquoise",       blues, cyans)
        # Moves for larger set of colors
        MoveColor("maroon1", reds, magentas)
        MoveColor("maroon2", reds, magentas)
        MoveColor("maroon3", reds, magentas)
        MoveColor("maroon4", reds, magentas)
        MoveColor("orchid1", reds, magentas)
        MoveColor("orchid2", reds, magentas)
        MoveColor("orchid3", reds, magentas)
        MoveColor("orchid4", reds, magentas)
        MoveColor("mediumvioletred", reds, magentas)
        MoveColor("violetred", reds, magentas)
        MoveColor("deeppink", reds, magentas)
        MoveColor("plum", reds, magentas)
        MoveColor("gold1", reds, yellows)
        MoveColor("gold2", reds, yellows)
        MoveColor("gold3", reds, yellows)
        MoveColor("gold4", reds, yellows)
        MoveColor("goldenrod1", reds, yellows)
        MoveColor("goldenrod2", reds, yellows)
        MoveColor("goldenrod3", reds, yellows)
        MoveColor("goldenrod4", reds, yellows)
        MoveColor("lightgoldenrod", reds, yellows)
        MoveColor("mediumgoldenrod", reds, yellows)
        MoveColor("khaki1", reds, yellows)
        MoveColor("khaki2", reds, yellows)
        MoveColor("khaki3", reds, yellows)
        MoveColor("khaki4", reds, yellows)
        MoveColor("purple", blues, magentas)
        MoveColor("purple1", blues, magentas)
        MoveColor("purple2", blues, magentas)
        MoveColor("purple3", blues, magentas)
        MoveColor("purple4", blues, magentas)
        MoveColor("violet", blues, magentas)
        MoveColor("darkviolet", blues, magentas)
        MoveColor("lavender", blues, magentas)
        MoveColor("blueviolet", blues, magentas)
        MoveColor("aquamarine", blues, cyans)
        MoveColor("turquoise", blues, cyans)
        MoveColor("turquoise1", blues, cyans)
        MoveColor("turquoise2", blues, cyans)
        MoveColor("turquoise3", blues, cyans)
        MoveColor("turquoise4", blues, cyans)
    # Sort the elements in each list by intensity
    for group in [greys, reds, greens, blues, yellows, cyans, magentas]:
        SortByIntensity(group)
    # Combine all the lists into one
    colors = (
        Nm("REDS")
        + reds
        + Nm("GREENS")
        + greens
        + Nm("BLUES")
        + blues
        + Nm("YELLOWS")
        + yellows
        + Nm("CYANS")
        + cyans
        + Nm("MAGENTAS")
        + magentas
        + Nm("GREYS")
        + greys
    )
    ColorChart(file, colors)


ColorChartByName("out/color_by_name.ps")
ColorChartByColor("out/color_by_color.ps")
