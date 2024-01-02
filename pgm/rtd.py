'''
Print RTD tables
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2005, 2023 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print RTD tables
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from math import sqrt
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from columnize import Columnize
        from wrap import wrap, dedent
        from color import t
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
        Usage:  {sys.argv[0]} [options] 
          Print RTD table over 0 to 200 °C range.
        Options:
            -f      Print both R to T and T to R tables
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-f"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "fh") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("f"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args
if 1:   # Core functionality
    def Report():
        a, b, R0 = 3.9083e-3, -5.775e-7, 100
        t.r = ""
        t.t = t("denl")
        print("DIN EN 60751 RTD α = 0.00385")
        if d["-f"]:   # Resistance to temperature
            print(f"\n{t.r}Resistance in Ω{t.n} to {t.t}temperature in °C{t.n}")
            o = []
            for R in range(100, 176):
                if R == 100:
                    T = 0.0
                else:
                    T = (sqrt(a*a - 4*b*(1 - R/R0)) - a)/(2*b)
                o.append(f"{t.r}{R:3d}{t.n} {t.t}{T:5.1f}{t.n}")
            for i in Columnize(o):
                print(i)
            print()
        if 1:   # Temperature to resistance
            print(f"{t.t}Temperature in °C{t.n} to {t.r}resistance in Ω{t.n}")
            o = []
            for T in range(0, 200):
                R = R0*(1 + a*T + b*T**2)
                o.append(f"{t.t}{T:3d}{t.n} {t.r}{R:5.1f}{t.n}")
            for i in Columnize(o):
                print(i)
            print("\nClass B:  dT = ±(0.3 + 0.005 |T|) °C")
            print("Class A:  dT = ±(0.15 + 0.002 |T|) °C")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Report()
