'''
Interpolate between colors and show on console

Examples to try:
    - '#000000' 8 '#ffffff'
        - Shows 8 interpolations between black and white.
    - '#ff0000' 10 '#00ff00' 10 '#0000ff'
        - Shows 10 interpolations between red and green, then 10 between green and blue.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Interpolate between colors and show on console
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from collections import deque
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, t
        from util import fDistribute
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        ii = isinstance
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] c1 n c2 [m c3...]
          Interpolate n colors between c1 and c2 and print their values to
          stdout, then for c2 m c3, etc.  
 
          The colors can be specified by hex strings (preface with '#' for
          RGB, '@' for HSV, or '$' for HLS).  You can also use python
          sequences of numbers:  if they are integers in the range of 0 to
          255, they are left as integers, but all others will be converted
          to floats.  If any float is not in [0, 1], the sequence is
          normalized by dividing by the largest value.  The absolute value
          of each number is taken.
        Options:
            -@      Hex digits represent HSV (hue, saturation, value)
            -#      Hex digits represent RGB (red, green, blue) [default]
            -$      Hex digits represent HLS (hue, lightness, saturation)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["typ"] = "rgb"    # Interpolation type
        try:
            opts, args = getopt.getopt(sys.argv[1:], "@#$")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("@#$"):
                if o[1] == "@":
                    d["typ"] = "hsv"
                elif o[1] == "#":
                    d["typ"] = "rgb"
                else:
                    d["typ"] = "hls"
        if len(args) < 2:
            Usage()
        return args
if 1:   # Core functionality
    def InterpretHex(s: str):
        t = s[1:] if s[0] in "@#$" else s
        try:
            return int(t[0:2], 16), int(t[2:4], 16), int(t[4:6], 16)
        except Exception:
            raise ValueError(f"'{s}' is an improper hex form")
    def InterpretArgument(x):
        '''x is a string from the command line representing a color.
        Return a Color object.
        '''
        if x[0] in "@#$":       # Hex string
            c = Color(x)
        else:                   # Must be a tuple or list
            y = eval(x)
            c = Color(x)
        return c
    def Process(s1, n, s2):
        cn1 = InterpretArgument(s1)
        cn2 = InterpretArgument(s2)
        #print(f"Process('{cn1.RGB}', {n}, '{cn2.RGB}')")
        typ = d["typ"]
        for u in fDistribute(n):
            cn3 = cn1.interpolate(cn2, u, typ)
            # Get hex string to display
            if typ == "rgb":
                s = cn3.xrgb
            elif typ == "hsv":
                s = cn3.xhsv
            else:
                s = cn3.xhls
            # Display this string in this color
            print(f"{t(cn3.xrgb)}{s}{t.n} ", end="")
        print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = deque(ParseCommandLine(d))
    color1 = args.popleft()
    while args:
        n = int(args.popleft())
        color2 = args.popleft()
        Process(color1, n, color2)
        color1 = color2
