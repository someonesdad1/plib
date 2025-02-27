"""
Construct a graphic that shows the relative sizes of the various sizes
of paper.

You'll need to download the g library from
http://code.google.com/p/pygraphicsps/ if you wish to run this script.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Construct a graphic that shows the relative sizes of the various
    # sizes of paper
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    from math import atan, pi
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from g import *
if 1:  # Global variables
    out = sys.stdout.write
    nl = "\n"
    debug = 0  # Turns on debug printing
    wrap_in_PJL = 0
    cm2in = 1 / 2.54
    mm2in = 1 / 25.4
    # Paper sizes
    #   First two numbers are width and height in mm for portrait.
    #   Second two numbers are offsets in inches for where to put the label.
    #   Last item is color of the line & label.
    iso = {
        "4A0": [1682, 2378, 0, 0, blue],
        "2A0": [1189, 1682, 0, 0, blue],
        "A0": [841, 1189, 0, 0, blue],
        "A1": [594, 841, 0, 0, blue],
        "A2": [420, 594, 0, 0, blue],
        "A3": [297, 420, 0, -0.2, blue],
        "A4": [210, 297, 0, -0.2, blue],
        "A5": [148, 210, 0, -0.2, blue],
        "A6": [105, 148, -0.4, 0.1, blue],
        "A7": [74, 105, 0, -0.3, blue],
        "A8": [52, 74, 0, -0.2, blue],
        "A9": [37, 52, 0, 0, blue],
        "A10": [26, 37, 0, 0, blue],
        "B0": [1000, 1414, 0, 0, magenta],
        "B1": [707, 1000, 0, 0, magenta],
        "B2": [500, 707, 0, 0, magenta],
        "B3": [353, 500, 0, 0, magenta],
        "B4": [250, 353, 0, -0.3, magenta],
        "B5": [176, 250, 0, -0.3, magenta],
        "B6": [125, 176, 0, -0.3, magenta],
        "B7": [88, 125, 0, -0.3, magenta],
        "B8": [62, 88, 0, -0.3, magenta],
        "B9": [44, 62, 0, 0, magenta],
        "B10": [31, 44, 0, 0, magenta],
        "C0": [917, 1297, 0, 0, blue],
        "C1": [648, 917, 0, 0, blue],
        "C2": [458, 648, 0, 0, blue],
        "C3": [324, 458, 0, 0, blue],
        "C4": [229, 324, 0, 0, blue],
        "C5": [162, 229, 0, 0, blue],
        "C6": [114, 162, 0, 0, blue],
        "C7": [81, 114, 0, 0, blue],
        "C8": [57, 81, 0, 0, blue],
        "C9": [40, 57, 0, 0, blue],
        "C10": [28, 40, 0, 0, blue],
    }
    ansi = {
        "A (letter)": [8.5, 11, -2.0, 0.1, red],
        "B (tabloid, ledger)": [11, 17, -3.7, 0.1, red],
        "C": [17, 22, 0, 0, red],
        "D": [22, 34, 0, 0, red],
        "E": [34, 44, 0, 0, red],
    }
    other_color = darkgreen
    other = {
        "Legal": [8.5, 14, -1.7, 0.1, other_color],
        "Executive": [7.25, 10.5, -2.5, 0.1, other_color],
        "US post card": [3.5, 5.5, -3.0, 0.1, other_color],
        "5x8": [5, 8, -2.5, 0.1, other_color],
        "4x6": [4, 6, 0, -0.2, other_color],
        "3x5": [3, 5, -2.2, 0.1, other_color],
        # "#10 env": [3, 5, 0, 0, other_color],
    }
    ansi_types = ("A", "B", "C", "D", "E")


def Dbg(msg, no_newline=0):
    if debug:
        print(msg, file=sys.stderr)
        if not no_newline:
            print(nl, file=sys.stderr)


def SetUp(file, orientation=portrait, units=inches):
    """Convenience function to set up the drawing environment and return a
    file object to the output stream.
    """
    ofp = open(file, "w")
    ginitialize(ofp, wrap_in_PJL)
    setOrientation(orientation, units)
    return ofp


def ParseCommandLine():
    import getopt

    try:
        optlist, args = getopt.getopt(sys.argv[1:], "h")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg + nl)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-h":
            Usage()
    return args


def ConvertISO():
    # Change ISO sizes from mm to inches
    for i in iso:
        iso[i][0] /= 25.4
        iso[i][1] /= 25.4


def Title():
    push()
    dx, dy = 0.5, 0.2
    x, y = 11 / 2 - dx, 7.25
    move(x, y)
    textSize(0.25)
    ctext("Scale Drawing of Paper Sizes")
    textSize(0.15)
    move(x, y - dy)
    ctext(
        "https://someonesdad1.github.io/hobbyutil/project_list.html  misc/paper_sizes.pdf"
    )
    move(x, y - 2 * dy)
    ctext("Numbers in square brackets are aspect ratios (ISO ratio is sqrt(2))")
    pop()


def MakeScale_cm(y, cm):
    push()
    translate(0, y)
    move(0, 0)
    rline(cm * cm2in, 0)
    dy, factor = 0.1, 1.2
    for i in range(cm + 1):
        move(i * cm2in, 0)
        rline(0, dy)
        move(i * cm2in, dy * factor)
        ctext(str(i))
    move((cm + 0.5) * cm2in, dy * factor)
    text("cm")
    pop()


def MakeScale(y, mm, invert=False):
    push()
    translate(0, y)
    t = 0.15
    TextSize(t)
    move(0, 0)
    rline(mm * mm2in, 0)
    dy, factor = t, 1.2
    if invert:
        dy *= -1
        factor = 2.0
    for i in range(0, mm + 1, 10):
        move(i * mm2in, 0)
        rline(0, dy)
        move(i * mm2in, dy * factor)
        ctext(str(i))
    move((mm + 5) * mm2in, dy * factor)
    text("mm")
    pop()


def Table():
    push()
    translate(0.5, 10.5)
    move(0, 0)
    textSize(0.25)
    textName(CourierBold)
    textLines(
        (
            "ISO sizes in mm:",
            "A3  297  420",
            "A4  210  297",
            "A5  148  210",
            "A6  105  148",
            "A7   74  105",
            "A8   52   74",
        )
    )
    move(2.3, 0)
    textLines(
        (
            "",
            "B4  250  353",
            "B5  176  250",
            "B6  125  176",
            "B7   88  125",
            "B8   62   88",
        )
    )
    move(5.3, 0)
    textLines(
        (
            "US sizes in inches and mm:",
            "ANSI A      8.5   11       215.9   279.4",
            "ANSI B     11     17       279.4   431.8",
            "Legal       8.5   14       215.9   355.6",
            "Executive   7.25  10.5     184.15  266.7",
            "Post card   3.5    5.5     88.9    139.7",
        )
    )
    pop()


def Draw(label, size, include_aspect=False):
    push()
    dx = 0.05
    height, width, x_offset, y_offset, color = size  # In inches
    lineColor(color)
    textColor(color)
    if height > width:
        height, width = width, height
    move(0, 0)
    rectangle(width, height)
    move(width + dx + x_offset, height + y_offset)
    if include_aspect:
        aspect_ratio = " [%.2f]" % (width / height)
        text(label + aspect_ratio)
    else:
        text(label)
    pop()


def IsoLine():
    # Draw a blue line to show ISO aspect ratio
    push()
    w, h, a, b, c = iso["A3"]
    t = 0.25
    LineColor(blue)
    LineWidth(0.005)
    line(0, 0, h, w)  # Note dimensions are already converted to inches
    a = 0.77
    translate(a * h, a * w)
    rotate(atan(w / h) * 180 / pi)
    move(0, t / 2)
    TextSize(t)
    TextColor(blue)
    text("ISO aspect ratio = sqrt(2)")
    pop()


def MakeDrawing():
    push()
    lineWidth = 0.02
    margin = 0.7
    translate(margin, margin)
    Title()
    scale_factor = 1 / 1.8
    scale(scale_factor, scale_factor)
    move(0, 0)
    for i in "A3 A4 A5 A6 A7 A8 B4 B5 B6 B7 B8".split():
        Draw(i, iso[i])
    for i in other:
        Draw(i, other[i], include_aspect=True)
    for i in ["A (letter)", "B (tabloid, ledger)"]:
        Draw(i, ansi[i], include_aspect=True)
    # IsoLine()
    textSize(0.2)
    MakeScale(-0.2, 440, invert=True)
    push()
    rotate(90)
    MakeScale(0.2, 300)
    pop()
    Table()
    pop()


if __name__ == "__main__":
    args = ParseCommandLine()
    f = SetUp("paper_sizes.ps", orientation=landscape)
    ConvertISO()
    MakeDrawing()
