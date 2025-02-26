"""
Calculate the binary products of all the numbers on the command line or
from a file.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Calculate products of numbers on command line
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from itertools import combinations
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
    from f import flt
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] n1 [n2 ...]
          Show all binary products of the numbers on the command line.
        Options:
            -h      Print a manpage
            -m x    Multiply each product by this value
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-m"] = flt(1)  # Multiply all numbers by this
        d["-d"] = 3  # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hm:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o == "-m":
                d["-m"] = x = flt(a)
                if x <= 0:
                    Error("-m option needs to be > 0")
            elif o == "-d":
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
        x = flt(0)
        x.n = d["-d"]
        x.rtz = x.rtdp = True
        return args


if 1:  # Core functionality

    def Calculate(args):
        results = []
        for i in combinations([flt(j) for j in args], 2):
            p = flt(i[0] * i[1] * d["-m"])
            results.append((p, *i))
        w = 12
        for p, a, b in sorted(results):
            s = f"{p!s:{w}s} {a!s:{w}s} {b!s:{w}s}"
            print(s)


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    Calculate(args)
