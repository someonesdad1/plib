"""
Print RTD tables
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2005, 2023 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Print RTD tables
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        import getopt
        import os
        from math import sqrt
        from pathlib import Path as P
        import sys
    if 1:  # Custom imports
        from columnize import Columnize
        from wrap import wrap, dedent
        from color import t
    if 1:  # Global variables

        class G:
            pass

        g = G()
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        # Callendar-van Dusen equation constants
        g.A, g.B, g.C, g.R0 = 3.9083e-3, -5.775e-7, -4.183e-12, 100
        # Colors
        t.r = t("ornl")
        t.t = t("denl")
if 1:  # Utility

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] 
          Print RTD table over 0 to 200 °C range.
        Options:
            -f      Print temperature in °F
            -t      Print both R to T and T to R tables
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-f"] = False  # Print in deg F
        d["-t"] = False  # Print both tables
        try:
            opts, args = getopt.getopt(sys.argv[1:], "fht")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("ft"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
        return args


if 1:  # Core functionality

    def Header():
        print(
            dedent(f"""
        DIN EN 60751 RTD α = 0.00385
        Callendar-van Dusen equation:  
            R = R0*(1 + A*T + B*T**2) for R > 0
            R = R0*(1 + A*T + B*T**2 + C*T**3*(T - 100)) for R < 0
            R = RTD resistance in Ω, R0 = RTD resistance in Ω at 0 °C
            T = temperature in °C
            A = 3.9083×10⁻³, B = -5.775×10⁻⁷, C = -4.183×10⁻¹²
            Ref https://www.ti.com/lit/an/sbaa275/sbaa275.pdf
        """)
        )

    def Report():
        Header()
        a, b, R0 = g.A, g.B, g.R0
        toF = lambda T: 9 / 5 * T + 32
        toC = lambda T: 5 / 9 * (T - 32)
        s = "°C"
        if d["-f"]:
            t.t = t("grnl")
            s = "°F"
        if d["-t"]:  # Resistance to temperature
            print(f"\n{t.r}Resistance in Ω{t.n} to {t.t}temperature in {s}{t.n}")
            o = []
            for R in range(100, 176):
                if R == 100:
                    T = 0.0
                else:
                    T = (sqrt(a * a - 4 * b * (1 - R / R0)) - a) / (2 * b)
                    if d["-f"]:
                        T = toF(T)
                o.append(f"{t.r}{R:3d}{t.n} {t.t}{T:5.1f}{t.n}")
            for i in Columnize(o):
                print(i)
            print()
        if 1:  # Temperature to resistance
            print(f"{t.t}Temperature in {s}{t.n} to {t.r}resistance in Ω{t.n}")
            o = []
            R = range(32, 390, 2) if d["-f"] else range(0, 200)
            for T in R:
                if d["-f"]:
                    T = toC(T)
                R = R0 * (1 + a * T + b * T**2)
                if d["-f"]:
                    T = int(round(toF(T), 0))
                o.append(f"{t.t}{T:3d}{t.n} {t.r}{R:5.1f}{t.n}")
            for i in Columnize(o):
                print(i)
            print("\nClass B:  dT = ±(0.3 + 0.005 |T|) °C")
            print("Class A:  dT = ±(0.15 + 0.002 |T|) °C")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    Report()
