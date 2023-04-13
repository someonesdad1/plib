'''
Dump the colors in rgbdata.py's list to stdout
    They are decorated with their ANSI escape codes and will display in a
    24-bit color terminal.  In a mintty terminal full-screen on cygwin with
    548 columns and 157 lines, all 6743 of these colored strings are shown
    at the same time on my 4k monitor (there are over 10000 in the
    rgbdata.py file, but there are many duplicates.  They are sorted by HSV
    numbers.

'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Program description string
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from collections import deque
    from pdb import set_trace as xx
if 1:   # Custom imports
    from rgbdata import color_data
    from wrap import wrap, dedent
    #from clr import Clr
    from color import Color, t
    #from rgb import Color
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    #c = Clr()
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] sort_order
          Print the colors' hex string to stdout wrapped in its 24-bit ANSI
          escape code.  RGB hex values are shown in lower case; upper case
          is used for HSV.

          The sort order is given by the order of the letters of "hsv" or
          "rgb".  "hvs" means to sort by hue first, followed by value, and
          finally by saturation.  You only need to supply the first two
          letters.
        Options:
            -h      Show HSV values (upper case)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug:  truncate the data for debugging
        d["-H"] = False     # Show HSV values
        d["-h"] = False     # Sort by HSV
        d["-R"] = False     # Show RGB values
        d["-r"] = False     # Sort by RGB
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dHhRr", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dHhRr"):
                d[o] = not d[o]
        if not args:
            Usage()
        sort_order = CheckSortLetters(args[0])
        return sort_order
if 1:   # Core functionality
    def CheckSortLetters(letters):
        allowed = [list("bgr"), list("hsv")]
        s = letters.lower()
        if list(sorted(s)) not in allowed:
            Error("sort_order must be orderings of 'rgb' or 'hsv'")
        return letters.lower()
    def GetColors(sort_order):
        'Return a sorted list of rgb.Color objects'
        colors = [i[2] for i in color_data]
        breakpoint() #xx
        if d["-d"]:
            colors = colors[:50]
        # Sort the data
        if "r" in sort_order:
            pass #xx
        else:
            pass #xx
#yy
        raise Exception("yy")
        return list(sorted(colors, key=f))
    def DumpColors(colors):
        size = len(colors)
        w = int(os.environ.get("COLUMNS", "80"))
        N = w//7
        count = 0
        used = set()
        while colors:
            color = colors.pop(0)
            # Make sure we use this color only once
            if color in used:
                continue
            used.add(color)
            if d["-H"]:
                s = color.hsvhex
            elif d["-R"]:
                s = color.hex
            else:
                raise Exception("-H or -R should have been defined")
            #print(f"{c('#' + s)}{s}{c.n}", end=" ")
            print(f"{t('#' + s)}{s}{t.n}", end=" ")
            count += 1
            if count and not (count % N):
                print()
        duplicates = size - len(used)
        print(f"\n{count} colors printed ({duplicates} duplicates)")

if __name__ == "__main__":
    d = {}      # Options dictionary
    sort_order = ParseCommandLine(d)
    colors = GetColors(sort_order)
    DumpColors(colors)
