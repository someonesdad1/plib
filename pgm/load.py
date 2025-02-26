"""
This computes a table of allowed currents and voltages for a DC or AC load constructed from 120 W
power resistors.  These are found at https://www.mpja.com/ for $6 to $7 each.  I wrote this script
so I could print the table on the outside of a box with switches that allows choosing any of these
resistors to get from 1 to 31 ohms (putting them in series), capable of running at up to 120 W of
dissipated power with an internal fan.  The box was $10 from a surplus store, the fan was
salvaged, the resistors were $32, and some toggle switches and 12 V SPDT relays were under $10 (I
used a scrapped 12 V wall wart), and an IEC socket were used to give a useful AC or DC 100 W load
of 1 to 31 ohms in steps of 1 ohm for the bench that cost under $60.

    Components used (quantity)
        - (1) Surplus metal box                     $10
        - (5) 120 W resistors (1/2/4/8/16 Ω)        $32
        - (6) mini toggle switches                  $6
        - (6) 10 A 12 V SPDT relays                 $12
        - (1) 10 A circuit breaker                  $3
        - (1) IEC jack for 120 V power              $1
        - (1) 120 V fan for cooling                 $5
        - (1) Normally-open thermostatic switch     $1

Total cost should be under $70.  I used the mini toggle switches to switch the relays on and off.
The extra toggle switch switches the whole series load of resistors in and out of the circuit.

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
        from itertools import combinations
        from pathlib import Path as P
        from pprint import pprint as pp
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
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
        g.dbg = True
        g.dbg = False
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
        Usage:  {sys.argv[0]} [options] [power_W]
          Print a table of the allowed voltages and currents for the series combinations of the
          power resistors in 1, 2, 4, 8, 16 Ω, each rated to 120 W.  The table is printed for 120
          W maximum dissipation unless you include a power on the command line.
        Options:
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-a"] = False  # Need description
        d["-n"] = 3  # Number of significant digits
        # if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "an:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-n":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"{o} option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        return args


if 1:  # Core functionality

    def PrintPowers(power_W):
        """Given a set of resistors of values 1, 2, 4, 8, 16 in series, selected by toggle
        switches or relays.  Print out a table of the allowed current and voltage across the
        selected resistance value.
        """
        o = []
        # Construct all combinations
        for k in range(1, 6):
            for c in combinations((1, 2, 4, 8, 16), k):
                o.append((sum(c), c))
        if g.dbg:
            print("Resistance in Ω and the resistors making it up:")
            for R, comb in sorted(o):
                print(R, comb)
        # Print allowed current and voltage
        w = 8
        flt(0).rtz = False
        print(f"Maximum power in W is {power_W}")
        print(f"R, Ω    Volts       Amperes     Hottest resistor % of maximum power")
        for R, comb in sorted(o):
            V = (power_W * R) ** 0.5
            i = (power_W / R) ** 0.5
            # Get maximum power of hottest resistor
            p = []
            for j, r in enumerate(comb):
                p.append((i**2 * r, j))
            P, n = p[-1]
            pct = 100 * P / power_W
            print(
                f"{R:2d}       {V!s:{w}s}     {i!s:{w}s}      {int(round(pct, 0)):3d}"
            )


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    power_W = flt(args[0]) if args else flt(120)
    PrintPowers(power_W)
