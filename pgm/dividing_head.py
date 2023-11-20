'''
Calculate characteristics of a dividing head

See PIM Feb 1991, "The Mathematics of a Dividing Head", pg 17

The fundamental characteristic of the dividing head is the gear ratio R.
If you want N divisions, then you'll need to make R/N turns of the worm
gear shaft to get 1/N of a circle of movement.  Here, assume R and N are
both integers.

    Example:  suppose R = 40 and we want N = 24 divisions.  Then 1/24th of
    a revolution is gotten by a turn of 40/24 or 1-16/24 of a turn.  This
    is the fraction 1-2/3 in lowest terms.  We can perform this operation
    if we have a dividing plate with 3 equally-spaced holes in it.

The number of holes needed for N turns is thus Fraction(R % N, N).denominator.

This lets us construct a table of N versus number of holes in a plate for a
given ratio R.

'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
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
        from fraction import Fraction
        import getopt
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import dedent
        from color import t
        from columnize import Columnize
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] R N
          For a dividing head with a ratio R, construct a table showing the
          number of holes needed to get all the divisions from 2 to N.  R
          and N must be integers.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Describe this option
        d["-d"] = 3         # Number of significant digits
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
            elif o == "-h":
                Usage(status=0)
        if len(args) != 2:
            Usage(status=1)
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    R, N = [int(i) for i in args]
    print(f"Ratio = {R}")
    di = {}
    for n in range(2, N + 1):
        if R % n:
            di[n] = Fraction(R % n, n).denominator
        else:
            di[n] = R // n
    o = []
    for n in di:
        o.append(f"{n}:{di[n]}")
    for i in Columnize(o):
        print(i)
