'''
Time to drain a tank of water
    Ref. https://en.wikipedia.org/wiki/Torricelli%27s_law
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from f import flt, pi, sqrt
        import u
    # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h", ["help"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
        x.n = d["-d"]
        return args
if 1:   # Core functionality
    def GetNumber(prompt, units, default=None):
        'Return (input, value_in_SI)'
        while True:
            s = input(prompt)
            if not s.strip() and default is not None:
                t, un = default, units
                return ("", flt(t)*u.u(un))
            else:
                t, un = u.ParseUnit(s, allow_expr=True)
                try:
                    needed_units = u.dim(units)
                    got_units = u.dim(un)
                    if needed_units != got_units:
                        raise ValueError(f"Must enter units with dimensions '{u.dim(units)}'")
                    return (s, flt(t)*u.u(un))
                except Exception as e:
                    print(e)
                    print("Try again")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # All units are SI
    if 1:
        Vs, V = GetNumber("What is volume? ", "m3")
        Hs, h = GetNumber("What is height? ", "m")
        Ds, d = GetNumber("What is hole diameter? ", "m")
        Cs, mu = GetNumber("What is coefficient of discharge [0.65]?  ", "", 0.65)
    else:
        # This estimate was made for our sprayer draining through a chunk
        # of 1-1/4 inch pipe and it feels about right.
        Vs, V = "15 gal", flt(15)*u.u("gal")
        Hs, h = "10 in", flt(10)*u.u("in")
        Ds, d = "1.38 in", flt(1.38)*u.u("in")
        Cs, mu = "0.65", flt(0.65)
    g = 9.8     # Acceleration of gravity
    A = pi*d**2/4
    t = mu*V/A*sqrt(2/(h*g))
    # Print report
    print(f"Volume      {Vs:20s} = {V} m³")
    print(f"Height      {Hs:20s} = {h} m")
    print(f"Hole dia    {Ds:20s} = {d} m")
    print(f"Coeff       {Cs:20s} = {mu}")
    if t >= 3600:
        print(f"\nDrain time  {t/3600} = hours")
    elif t >= 60:
        print(f"\nDrain time  {t/60} = minutes")
    else: 
        print(f"\nDrain time  {t} = s")
