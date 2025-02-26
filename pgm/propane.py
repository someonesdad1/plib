"""
Estimate quantity of propane left in our trailer's tanks

    - Units:  gallons and lb
    - Liquid propane is 4.28 lb/gal at around 25 °C
    - Luggage scale weights of tanks
        - Tare weight is 25.4 lb
        - Tanks are only filled 80% full
        - Labeled WC = 71.4 lb, which I interpret as a water capacity.  Since water is 8.345
          lb/gal, this means the tank would hold 71.4/8.345 or 8.56 gal
            - 0.8 of this gives a tank capacity of 6.84 gal
        - One of these tanks full should then weigh 25.4 lb + (6.84 gal)(4.2 lb/gal) or 54.1 lb
        - I've measured full tanks at 54.7 lb, so these numbers are fairly close
    - Algorithm
        - Assume tare weight of tank is Wt = 25.4 lb
        - Let W = weight of tank in lb from luggage scale
        - Volume of propane in gallons is (W - Wt)/4.28

"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from frange import frange
        from columnize import Columnize
        from f import flt, ceil
        from wrap import dedent
        from color import t
        from lwtest import Assert

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        g.dbg = False
        g.tare = flt(25.4)  # Tare mass of RV tank in lb
        g.full = flt(54.7)  # Mass of full RV tank in lb
        g.density = flt(4.28)  # Density of liquid propane in lb/gal
        g.vol = 8.56  # Geometrical volume in gal
        ii = isinstance
if 1:  # Utility

    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )

    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status=0):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] [weight_in_lb]
          Estimate gallons of propane left in our trailer's propane tanks if weight_in_lb is
          given.  Assumes tare weight of tank is 25.4 lb and propane density at 25 °C is 4.28
          lb/gal.  For no input, print out a table.
        Options:
            -d n    Set number of figures [{d["-d"]}]
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Need description
        d["-d"] = 3  # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", "--debug")
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
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Usage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an unhandled exception
                import debug

                debug.SetDebugger()
        return args


if 1:  # Core functionality

    def Estimate(wt_lb):
        w = flt(wt_lb)
        if not (g.tare <= w <= 55):
            t.print(f"{t.lill}Tank mass must be between {g.tare} and 55 lb")
            return
        v = (w - g.tare) / g.density  # Propane volume in gallons
        print("Mass in lb")
        print(f"    Entered mass of tank        {w}")
        print(f"    Tare mass of tank           {g.tare}")
        print(f"    Mass of propane in tank     {w - g.tare}")
        with v:
            v.N = 2
            t.print(f"{t.ornl}{v} gallons of propane remaining")

    def Table():
        # start = g.tare
        start = flt(25.5)
        end = g.full
        t.lb = t.grnl
        t.gal = t.lill
        t.pct = t.yell
        w1, w2, w3, w = 6, 4, 4, 5
        vfull = (g.full - g.tare) / g.density
        print("Remaining propane as a function of tank mass\n")
        o = [f"{t.ornl}{'lb':^{w1}s} {'gal':^{w2}s} {'%':^{w3}s}"]
        full = g.vol * g.density  # Max possible mass of completely full tank
        for mass in frange(str(start), str(start + full + 0.01), "0.5"):
            v = (mass - g.tare) / g.density  # Propane volume in gallons
            pct = int(round(100 * v / vfull, 0))
            with v:
                v.N = 3
                v.rtz = v.rtdp = False
                if pct > 100:
                    o.append(
                        f"{t.lb}{mass!s:^{w1}s} {t.gal}{v:^{w2}.1f} {t.redl}{pct:^{w3}d}"
                    )
                else:
                    o.append(
                        f"{t.lb}{mass!s:^{w1}s} {t.gal}{v:^{w2}.1f} {t.pct}{pct:^{w3}d}"
                    )
        for i in Columnize(o, col_width=w1 + w2 + w3 + w):
            t.print(i)
        print()
        print(
            dedent(f"""
        Details
            Near 25 °C, liquid propane is {g.density} lbm/gal
            Tare mass of tanks is {g.tare} lbm
            Full tank from propane vendor is {g.full} lbm = {(g.full - g.tare) / g.density} gal
            Tank geometrical volume
                Tank's water capacity is 71.4 lbm.  Water is 8.345 lbm/gal, so this implies the
                tank's volume is 71.4/8.345 gal = 8.56 gal
            Tanks are typically filled to 80% full = {flt(0.8 * 8.56)} gal
        From M = mass of tank and propane in lbm, % full is 3.416*M - 86.7
        """)
        )


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if args:
        Estimate(args[0])
    else:
        Table()
