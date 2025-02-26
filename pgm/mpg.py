"""
Print cost of gas
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print cost of gas
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from clr import Clr
if 1:  # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()

    class g:
        pass

    g.mpg = flt(18)  # mpg of your default car
    g.tank = flt(26)  # Tank volume in gallons of your car
    g.name = "2011 Suburban"  # Name of default car
    g.mpg.rtz = g.mpg.rtdp = True
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] dpg [mpg]
          Print a table of the cost in $ to drive a distance in miles given
          mpg (miles per gallon) and dpg ($ per gallon).  The default mpg
          is {g.mpg}.
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-e"] = 2000  # Ending number of miles driven
        d["-n"] = g.name  # Name of vehicle
        d["-t"] = g.tank  # Tank volume in gallons
        try:
            opts, args = getopt.getopt(sys.argv[1:], "e:hn:t:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o == "-e":
                d["-e"] = abs(int(a))
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "-n":
                d["-n"] = a
            elif o == "-t":
                d["-t"] = abs(flt(a))
        if len(args) not in (1, 2):
            Usage()
        return args


if 1:  # Core functionality

    def Table(mpg, dpg):
        "Table for miles per gallon and dollars per gallon"
        # This is meant to print in at least an 80 column window
        print(
            dedent(f"""
        Car is {d["-n"]}
            Car mileage                 {mpg} miles/gallon
            Cost of fuel                {dpg} $/gallon
            Tank volume in gallons      {d["-t"]}

        Cost in $ vs. miles driven
        """)
        )
        w = 7  # Width of first column
        n = 4  # First column number width
        W = 6  # Width of table's columns
        # Column header
        print(f"{'Miles':^79s}")
        print(f"{'':{w}s}", end="")
        for m in range(0, 100, 10):
            print(f"{m:^{W}d}", end=" ")
        print()
        # Hyphens for column markers
        print(f"{'':{w}s}", end="")
        for m in range(0, 100, 10):
            print(f"{'-' * W:^{W}s}", end=" ")
        print()
        # Table detail
        for M in range(0, d["-e"] + 1, 100):
            s = f"{M:{n}d}" + (" " * (w - n))
            print(f"{s}", end="")
            for m in range(0, 100, 10):
                miles = M + m
                gallons = flt(miles / mpg)
                cost = flt(gallons * dpg)
                print(f"{cost!s:^{W}s}", end=" ")
            print()


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dpg = flt(args[0])
    mpg = flt(args[1]) if len(args) == 2 else g.mpg
    Table(mpg, dpg)
