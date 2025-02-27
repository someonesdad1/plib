"""
Print out tables of gas cost as function of $/gal and miles/gal.
    You'll want to edit the seq_dollars_per_gallon and seq_miles_per_gallon
    sequences to reflect your own vehicles and prices.
"""

if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Print out tables of gas cost as function of $/gal and miles/gal
    ##∞what∞#
    ##∞test∞# #∞test∞#
    # Standard imports
    import getopt
    import os
    from pathlib import Path as P
    import sys
    from pdb import set_trace as xx

    # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from frange import frange
    from color import TRM as t

    # Global variables
    ii = isinstance
    t.cost = t("ornl")
    t.mpg = t("yell")
    t.mi = t("grn")
    t.c = t("royl")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(d, status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]}
          Print out tables to help with calculating the cost of gasoline
          to drive a desired distance.
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        x = flt(0)
        x.n = 3
        x.rtdp = True


def PrintTables(seq_dollars_per_gallon, seq_miles_per_gallon):
    for dpg in seq_dollars_per_gallon:
        t.print(f"{t.cost}Gas cost = ${dpg} per gallon")
        for mpg in seq_miles_per_gallon:
            t.print(f"  {t.mpg}Miles per gallon = {mpg}")
            for miles in range(1000, 10000, 1000):
                s = " " * 4
                for i in (1, 10, 100, 1000):
                    mi = miles // i
                    cost = flt(mi) * dpg / mpg
                    if i in (100, 1000):
                        s += f"{t.mi}{mi:5d} {t.c}{cost:>6.1f}{t.n}    "
                    else:
                        s += f"{t.mi}{mi:5d} {t.c}{cost!s:>6s}{t.n}    "
                print(s)


if __name__ == "__main__":
    d = {}  # Options dictionary
    ParseCommandLine(d)
    seq_dollars_per_gallon = (3.5, 4)
    seq_miles_per_gallon = (10, 18, 28)
    PrintTables(seq_dollars_per_gallon, seq_miles_per_gallon)
    print(f"Colors:  {t.mi}miles{t.n}, {t.c}cost in ${t.n}")
