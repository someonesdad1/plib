'''
Find rational approximations
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
        # Find rational approximations
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        from fractions import Fraction
        from decimal import Decimal
        import sys
        from math import *
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import flt
        if 1:
            import debug
            debug.SetDebugger()
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
        Usage:  {sys.argv[0]} [options] n1 [n2...]
          Find rational approximations to the numbers n1, etc.
        Examples:
          3.1 gives 
        Options:
            -d n    Number of figures [{d['-d']}] 
                    (e.g., sets maximum denominator as 10**{d['-d']})
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 2         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = flt(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def Header():
        s, n = "-", w[1] + w[2]
        print(f"{'':^{w[0]}s} {'Approximation':^{n}s} {'':^{w[3]}s}")
        print(f"{'Input':^{w[0]}s} {'Improper':^{w[1]}s} {'Proper':^{w[2]}s} "
              f"{'Δ%':^{w[3]}s}")
        print(f"{s*w[0]:^{w[0]}s} {s*n:^{n}s} {s*w[3]:^{w[3]}s}")
    def FindRationalApprox(num, value):
        assert(ii(value, flt))
        n = Fraction.from_float(flt(value))
        n = n.limit_denominator(max_denominator)
        ip = int(n.numerator/n.denominator)
        fp = n - ip
        s = f"{ip}+{fp}"
        try:
            with value:
                value.N = 1
                diff = 100*(flt(n) - value)/value
                pct = f"{diff}"
        except Exception:
            pct = ""
        # Print approximation
        print(f"{num:^{w[0]}s} "
              f"{n!s:^{w[1]}s} "
              f"{s:^{w[2]}s} "
              f"{pct:^{w[3]}s}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    nums = ParseCommandLine(d)
    w = (15, 15, 15, 15)
    max_denominator = int(10**d['-d'])
    dx = 1/flt(10**d['-d'])
    with dx:
        dx.N = 1
        print(f"Rational approximations to within about {dx}\n")
    Header()
    for num in nums:
        value = flt(eval(num))
        FindRationalApprox(num, value)
