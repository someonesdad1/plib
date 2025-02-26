"""
Print a table of color hues
    - Arguments of 18 3 2 give a good general group of 108 colors from
      which a decent set of base colors could be chosen.  Here are the
      hue's colors:
        - 0 red
        - 14 orn
        - 28 ornyel
        - 42 yel
        - 57 slightly yelgrn
        - 71 yelgrn
        - 85 grn
        - 99 teal
        - 113 grncyn
        - 128 cyn
        - 142 sky
        - 156 blu
        - 170 lav
        - 184 lil
        - 198 vio
        - 212 magvio
        - 227 ruby
        - 241 lip

"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print a table of color hues
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent
    from color import Color, TRM as t

    t.on = True
    from util import iDistribute

    # Global variables
    ii = isinstance
    w = int(os.environ.get("COLUMNS", "80")) - 1
    L = int(os.environ.get("LINES", "50"))
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] num_hues [num_sat [num_lightness]]
          Print out a set of hues.  The arguments are the numbers of items
          to use from 0 to 255.  0 for saturation and lightness won't be
          used.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ah", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args


if 1:  # Core functionality

    def GetH(n):
        """Return n integers for hue.  If n is 1, you get [0].  If n is 2, you
        get [0, 128].  Otherwise, things are distributed between 0 and
        255, but the 255 is left off because it's the same as 0.
        """
        assert ii(n, int) and n > 0
        if n == 1:
            return [0]
        elif n == 2:
            return [0, 128]
        a = list(iDistribute(n + 1, 0, 255))
        a.pop(-1)
        return a

    def GetS(n):
        """Return n integers for saturation.  Zero will always be removed.
        Otherwise, things are distributed between 0 and 255.
        """
        assert ii(n, int) and n > 0
        if n == 1:
            return [255]
        elif n == 2:
            return [128, 255]
        o = list(iDistribute(n + 1, 0, 255))
        o.pop(0)
        return o

    def GetL(n):
        "Return n integers for lightness.  Zero and 255 are removed."
        assert ii(n, int) and n > 0
        o = list(iDistribute(n + 2, 0, 255))
        o.pop(0)
        o.pop(-1)
        return o

    def PrintHues(H, S, L):
        print("Color numbers are hls")
        print(
            "   ",
            nh,
            "hues, ",
            ns,
            "saturations, ",
            nl,
            " lightnesses, ",
            nh * ns * nl,
            " total colors",
        )
        used = 0
        for h in H:
            for s in S:
                for l in L:
                    c = Color(h, l, s, hls=True)
                    a = f"{h:3d},{l:3d},{s:3d}"
                    m = len(a)
                    if used + m + 1 > w:
                        print()
                        used = 0
                    u = f"{t(c)}{a}{t.n}"
                    print(u, end=" ")
                    used += m + 1
            print()
            used = 0
        print()


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    nh, ns, nl = 1, 1, 1
    if len(args) == 1:
        nh = int(args[0])
    if len(args) == 2:
        nh = int(args[0])
        ns = int(args[1])
    if len(args) == 3:
        nh = int(args[0])
        ns = int(args[1])
        nl = int(args[2])
    H, S, L = GetH(nh), GetS(ns), GetL(nl)
    PrintHues(H, S, L)
