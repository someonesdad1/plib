'''
Print i-V characteristics of on-hand diodes
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Print i-V characteristics of on-hand diodes
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        g.digits = 2
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        The characteristics printed came from the measurement of one diode, so ensemble estimates
        will differ.  Because of this, the default numbers only contain {g.digits} digits.
        '''))
        exit(0)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] num
          Print i-V characteristics of on-hand diodes.  Current is always in mA and voltage is
          always in mV.
            1   1N4148 Si
            2   1N4004 Si
            3   1N5818 Schottky
        Options:
            -d n    Number of digits [{d["-d"]}]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = g.digits  # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:Hh", "--debug") 
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
            elif o == "-h":
                Usage()
            elif o == "-H":
                Manpage()
        x = flt(0)
        x.N = d["-d"]
        return args
if 1:   # Core functionality
    def D1():
        pass
    def D2():
        pass
    def D3():
        '1N5818 Schottky'
        Vi = (  # V in mV, i in mA
            (15.34, 0.00047),
            (63.16, 0.00645),
            (101.38, 0.02969),
            (156.36, 0.2436),
            (203.3, 1.2),
            (295.5, 42.3),
            (322.3, 104),
            (369, 383),
            (397, 680),
            (420, 980),
        )
        w = 10
        for V, i in Vi:
            print(f"{flt(V)!s:^{w}s} {flt(i)!s:^{w}s}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    nums = [int(i) for i in ParseCommandLine(d)]
    f = {1: D1, 2: D2, 3: D3}
    for num in nums:
        f[num]()
