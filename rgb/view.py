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
    from color import Color, t
    #from clr import Clr
    #from rgb import Color
    if 1:
        import debug
        debug.SetDebugger()
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
          Print the colors' hex string to stdout wrapped in its 24-bit ANSI escape code.  RGB hex
          values are shown in lower case; upper case is used for HSV.
          
          The sort order is given by the order of the letters of "rgb", "hsv", or "HLS".
          Unfortunately, the 's' in 'hls' and 'hsv' mean different things, though they both are
          described by 'saturation'.  Example: "hvs" means to sort by hue first, followed by
          value, and finally by saturation.
        Options:
            -d      Truncate data for debugging
            -h      Show hsv values
            -l      Show HLS values
            -r      Show rgb values (default)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = False     # Debug:  truncate the data for debugging
        d["-h"] = False     # Show hsv values
        d["-l"] = False     # Show HLS values
        d["-r"] = False     # Show rgb values
        try:
            opts, args = getopt.getopt(sys.argv[1:], "dhlr")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("dhlr"):
                d[o] = not d[o]
        if not args:
            Usage()
        if not d["-h"] and not d["-l"] and not d["-r"]:
            d["-r"] = True
        sort_order = CheckSortLetters(args[0])
        return sort_order
if 1:   # Core functionality
    def CheckSortLetters(letters):
        allowed = [set("rgb"), set("hsv"), set("HLS")]
        s = set(letters)
        if s not in allowed:
            Error("sort_order must be orderings of 'rgb', 'hsv', or 'HLS'")
        return letters
    def GetColors(sort_order):
        'Return a sorted list of rgb.Color objects'
        colors = [i[2] for i in color_data]
        if d["-d"]:
            colors = colors[:50]
        # Sort the data
        sorted_colors = list(Color.Sort(colors, keys=sort_order))
        return sorted_colors
    def DumpColors(colors):
        size = len(colors)
        w = int(os.environ.get("COLUMNS", "80"))
        # Each output string (e.g. '#ff7f00 ') takes 8 characters, so N will be the number of
        # these we can print on a single line before needing a newline.
        N = w//8
        count = 0
        used = set()
        while colors:
            color = colors.pop(0)
            # Make sure we use this color only once
            if color in used:
                continue
            used.add(color)
            if d["-h"]:
                s = color.xhsv
            elif d["-l"]:
                s = color.xhls
            elif d["-r"]:
                s = color.xrgb
            else:
                raise Exception("-h or -l or -r should have been defined")
            print(f"{t(s)}{s}{t.n}", end=" ")
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
