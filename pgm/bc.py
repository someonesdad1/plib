'''
Cartesian coordinates of bolt holes on a circle
'''
if 1:   # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Cartesian coordinates of bolt holes on a circle
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:   # Custom imports
        from f import flt, sin, cos, pi, degrees, radians, fmod
        from get import GetNumber
        from wrap import dedent
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from wsl import wsl     # wsl is True when running under WSL Linux
        #from columnize import Columnize
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
        # Problem variables
        g.num_holes = 0                     # Number of holes
        g.bc_dia = 0                        # Bolt circle diameter
        g.angle_offset_degrees = flt(0)
        g.origin = (flt(0), flt(0))         # Origin
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        A shop task is to drill a set of n equally-spaced holes on a circle.  For example, an
        exhaust flange on a car engine might have three holes equally spaced on a circle about 50
        mm in diameter.  The problem's variables are (angles are in radians)

            n = number of equally-spaced holes
            d = bolt circle diameter
            r = bolt circle radius = d/2
            θ = angle between adjacent holes = 2π/n
            β = divider setting (distance between adjacent holes) = 2*r*sin(θ/2)

        There are various ways of laying out the hole locations:

            - If you have the work in a milling machine with a dividing head, you locate the
              spindle at the correct radius from the dividing head's center of rotation and rotate
              the dividing head appropriately.  Most of us don't have a dividing head.
            - If you have the work mounted in a lathe on center and you can index the spindle, you
              can mark the hole locations.  Most of us don't have a lathe.
            - If you scribe the bolt circle onto the work around its center and put a punch mark
              for the first hole, set your dividers to β and you can mark the hole location on the
              scribed circle for the adjacent hole from the punch mark.  Punch and repeat.  The
              hexagon is the best example of this, as the divider setting is the radius of the bolt
              circle.  Caution:  step off the divider setting first to see that you get back
              exactly to the first hole.
            - Use this script to calculate the Cartesian coordinates of the hole locations and lay
              them out with a rule, height gauge, etc.

        The hole locations before any optional transformations are at polar radius r and angle
        2πi/n radians, where i is an integer from 0 to n - 1.

        Transformations:  the angle offset is added to the calculated angle.  The origin's
        coordinates are added to the calculated Cartesian coordinates.  A use case where you might
        need to use this -o origin offset is when the workpiece has a hole where the center of the
        bolt circle is, so you can't e.g. scribe a bolt circle on the workpiece with your dividers.
        You can make a temporary plug to fix this problem, but an origin offset probably takes less
        time.

        '''.rstrip()))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] N bc_dia 
          Print a table of Cartesian coordinates of bolt holes on a circle.  Standard Cartesian and
          polar coordinate systems in analytic geometry are assumed.
        Options:
            -0          Use zero-based hole numbering
            -a ang      Angle offset in degrees [{d["-a"]}]
            -d n        Number of significant figures [{d["-d"]}]
            -h          Print a manpage
            -o 'x,y'    Location of origin
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-0"] = False     # Zero-based hole numbering
        d["-a"] = 0         # Angle offset in degrees
        d["-d"] = 5         # Number of significant digits
        d["-o"] = (0, 0)    # Location of origin
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "0a:d:ho:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("0"):
                d[o] = not d[o]
            elif o == "-a":     # Angle offset in degrees
                g.angle_offset_degrees = flt(a)
            elif o == "-d":     # Significant digits
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error("-d option's argument must be an integer between 1 and 15")
            elif o == "-o":     # Origin
                g.origin = [flt(i) for i in a.split(",")]
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Core functionality
    def Report():
        # Origin translation offsets
        x0, y0 = g.origin
        # Angle offset in radians
        θ0 = radians(g.angle_offset_degrees)
        # Print report
        print(f"{g.num_holes} equally-spaced holes")
        print(f"    Bolt circle diameter    {g.bc_dia}")
        print(f"    Origin                  {g.origin}")
        print(f"    Angle offset            {g.angle_offset_degrees}°")
        s = "Table of hole positions"
        print()
        print(s)
        print("-"*len(s))
        print()
        w, eps, r = 15, 1e-14, g.bc_dia/2
        s = "-"*(w - 4)
        print(f"Hole {'x':^{w}} {'y':^{w}} {'θ, °':^{w}}")
        print(f"---- {s:^{w}} {s:^{w}} {s:^{w}}")
        def f(x):
            return f"{x!s:^{w}}" if abs(x) >= eps else f"{flt(0)!s:^{w}}"
        z = 0 if d["-0"] else 1     # Hole numbering correction
        for i in range(g.num_holes):
            θ = 2*pi*i/g.num_holes + θ0
            X, Y = r*cos(θ) + x0, r*sin(θ) + y0
            x, y, t = f(X), f(Y), f(fmod(flt(degrees(θ)), 360))
            print(f"{i + z:^4} {x:^{w}} {y:^{w}} {t:^{w}}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    g.num_holes = int(args[0])      # Number of holes
    g.bc_dia = flt(args[1])         # Bolt circle diameter
    Report()

'''
Validation:  I drew a 100 mm diameter circle on paper, then drew an origin at (0, -71.2 mm) below
the circle's center.  I stepped off the 6 points using the circle's radius set on the compass and
measured these coordinates in the translated coordinate system.  The numbers were (0-based hole
numbering)
 
Hole    x       y
--------------------
 0      50      71.2
 1      24.6    114.5
 5      24.6    28.0
 
With the arguments "-0 -o '0,71.2' 6 100", the script printed
 
Hole        x               y             θ, °
----   -----------     -----------     -----------
 0         50             71.2              0
 1         25              115             60
 5         25             27.9             300
 
which check.
'''
