'''
Given a resistance R, print out the operating characteristics for various
power levels.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
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
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from color import C
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    class g: pass
    g.r = C.lgrn
    g.p = C.lmag
    g.i = C.lred
    g.v = C.lyel
    g.n = C.norm
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] R1 [R2 ...]
          Given one or more shunt resistances in ohms, print out their
          operating characteristics at various powers.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        x = flt(0)
        x.n = 2
        x.rtz = x.rtdp = 3
        return args
if 1:   # Core functionality
    def PrintR(R):
        powers = {
            1/8:  "1/8",
            1/4:  "1/4",
            1/2:  "1/2",
            1:  "1",
            2.5:  "2.5",
            5:  "5",
            10:  "10",
            25:  "25",
            50:  "50",
            100:  "100",
        }
        s = f"{R} Ω"
        w = 4
        print(f"{g.r}R = {s:10s}{g.n}")
        print(f"{'':{w}s}{g.p}Power, W{g.n}       "
              f"{g.i}Current, A{g.n}      "
              f"{g.v}Voltage, V{g.n}")
        for P, Ps in powers.items():
            i = (flt(P)/R)**0.5
            V = P/i
            print(f"{'':{w+1}s}{g.p}{Ps:^8s}{g.n}     "
                  f"{g.i}{i!s:^12s}{g.n}    "
                  f"{g.v}{V!s:^12s}{g.n}")
        if len(args) > 1:
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    for R in args:
        PrintR(flt(R))
