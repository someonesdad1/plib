'''
Command-line inch/mm converter
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Inch/mm converter
    ##∞what∞#
    ##∞test∞# #∞test∞#
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
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dist1 [dist2...]
      Convert the arguments in inches to mm.  If -r is used, convert the 
      arguments in mm to inches.  Use "t" for a table.
    Options:
      -d n  Number of significant figures [{d["-d"]}]
    '''))
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
    flt(0).N = 4
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
    # Print common metric threads
    coarse = (
        (1, 0.25),
        (1.1, 0.25),
        (1.2, 0.25),
        (1.4, 0.3),
        (1.6, 0.35),
        (1.8, 0.35),
        (2, 0.4),
        (2.2, 0.45),
        (2.5, 0.45),
        (3, 0.5),
        (3.5, 0.6),
        (4, 0.7),
        (4.5, 0.75),
        (5, 0.8),
        (6, 1),
        (7, 1),
        (8, 1.25),
        (9, 1.25),
        (10, 1.5),
        (11, 1.5),
        (12, 1.75),
        (14, 2),
        (16, 2),
        (18, 2.5),
        (20, 2.5),
        (22, 2.5),
        (24, 3),
        (27, 3),
        (30, 3.5),
        (33, 3.5),
        (36, 4),
        (39, 4),
        (42, 4.5),
        (45, 4.5),
        (48, 5),
        (52, 5),
    )
    fine = (
        (1, 0.2),
        (1.1, 0.2),
        (1.2, 0.2),
        (1.4, 0.2),
        (1.6, 0.2),
        (1.8, 0.2),
        (2, 0.25),
        (2.2, 0.25),
        (2.5, 0.35),
        (3, 0.35),
        (3.5, 0.35),
        (4, 0.5),
        (4.5, 0.5),
        (5, 0.5),
        (6, 0.75),
        (7, 0.75),
        (8, 0.75),
        (8, 1),
        (9, 0.75),
        (10, 0.75),
        (10, 1),
        (10, 1.25),
        (11, 0.75),
        (11, 1),
        (12, 1),
        (12, 1.5),
        (14, 1),
        (14, 1.25),
        (14, 1.5),
        (16, 1),
        (16, 1.5),
        (18, 1),
        (18, 1.5),
        (18, 2),
        (20, 1),
        (20, 1.5),
        (20, 2),
        (22, 1),
        (22, 1.5),
        (22, 2),
        (24, 1),
        (24, 1.5),
        (24, 2),
    )
    t.print(f"{t.purl}\nMetric fine threads")
    x = flt(0)
    x.N = 3
    x.rtz = x.rtdp = True
    o = []
    for d, p in fine:
        o.append(f"M{flt(d)}-{flt(p)}")
    for i in Columnize(o, indent=" "*4):
        print(i)
    t.print(f"{t.purl}\nMetric coarse threads")
    for d, p in coarse:
        o.append(f"M{flt(d)}-{flt(p)}")
    for i in Columnize(o, indent=" "*4, col_width=12):
        print(i)

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if "t" in args:
        Table()
    else:
        flt(0).n = d["-d"]
        for i in args:
            print(f"{g.i}{flt(i)} inches{g.n} = {g.m}{flt(i) * 25.4} mm{g.n}", end="    ")
            print(f"{g.m}{flt(i)} mm{g.n} = {g.i}{flt(i) / 25.4} inches{g.n}")
