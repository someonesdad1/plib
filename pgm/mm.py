"""
Command-line inch/mm converter
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Inch/mm converter
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from sig import sig
    from f import flt
    from frange import frange
    from columnize import Columnize
    from color import t
if 1:  # Global variables
    in2mm = flt(25.4)

    class g:
        pass

    g.n = t.n
    g.m = t("denl")
    g.i = t("ornl")


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    digits = d["-d"]
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] dist1 [dist2...]
      Convert the arguments in inches to mm.  If -r is used, convert the 
      arguments in mm to inches.  Use "t" for a table.
    Options:
      -d n      Number of significant figures [{d["-d"]}]
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-d"] = 4  # Number of significant digits
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:m")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-d",):
            try:
                d["-d"] = int(a)
                if not (1 <= d["-d"] <= 15):
                    raise ValueError()
            except ValueError:
                msg = "-d option's argument must be an integer between 1 and 15"
                Error(msg)
    x = flt(0)
    x.N = d["-d"]
    x.rtz = False
    if not args:
        Usage(d)
    return args


def Table():
    s = f"{g.m}mm{g.n} and {g.i}inches{g.n}"
    print(f"{' ' * 30:s}{s}")
    w = 3
    flt(0).n = 4
    # mm to inches
    o = []
    for m in range(1, 101):
        i = flt(m / 25.4)
        s = f"{g.m}{m:3d}{g.n} {g.i}{i!s:{w}s}{g.n}"
        o.append(s)
    for i in Columnize(o):
        print(i)
    print()
    # inches to mm
    o = []
    for i in frange("0.1", "4.01", "0.1", return_type=flt):
        m = flt(i) * flt(25.4)
        s = f"{g.i}{i!s:3s}{g.n} {g.m}{m!s:{w}s}{g.n}"
        o.append(s)
    for i in Columnize(o):
        print(i)
    # mm columns
    print(f"{' ' * 30:s}{g.m}mm{g.n} to {g.i}inches{g.n}")
    f = [1000, 100, 10, 1, 0.1, 0.01]
    print(" " * 8, end="")
    for i in f:
        print(f"{g.m}{str(i):{w + 8}s}{g.n}", end=" ")
    print()
    for i in range(1, 11):
        print(f"{g.m}{i:2d}{g.n}", end=" " * 3)
        for m in f:
            x = m * i / flt(25.4)
            print(f"{g.i}{x!s:^{w + 8}s}{g.n} ", end="")
        print()
    # inch columns
    print(f"{' ' * 30:s}{g.i}inches{g.n} to {g.m}mm{g.n}")
    f = [100, 10, 1, 0.1, 0.01, 0.001]
    print(" " * 8, end="")
    for i in f:
        print(f"{g.i}{str(i):{w + 8}s}{g.n}", end=" ")
    print()
    for o in range(1, 11):
        print(f"{g.i}{o:2d}{g.n}", end=" " * 3)
        for i in f:
            x = o * i * flt(25.4)
            print(f"{g.m}{x!s:^{w + 8}s}{g.n} ", end="")
        print()
    exit(0)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if "t" in args:
        Table()
    flt(0).n = d["-d"]
    for i in args:
        print(f"{g.i}{flt(i)} inches{g.n} = {g.m}{flt(i) * 25.4} mm{g.n}", end="    ")
        print(f"{g.m}{flt(i)} mm{g.n} = {g.i}{flt(i) / 25.4} inches{g.n}")
