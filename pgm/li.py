'''

LiFePO₄ battery characteristics

'''
_pgminfo = '''
<oo desc 
    LiFePO₄ battery characteristics
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat elec oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
        from scipy.interpolate import interp1d
    if 1:   # Custom imports
        from f import flt
        from frange import frange
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        from columnize import Columnize
        pp = PP()   # Get pprint with current screen width
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetColors(on=False):
        t.ten = t.grn if on else ""
        t.five = t.whtl if on else ""
        t.err = t.redl
        t.dbg = t.skyl if g.dbg else ""
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
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [N1 [N2...]]
          Print out LiFePO₄ battery characteristics for given number of cells N1.
          Defaults to 4 for a 12 V battery.
        Options:
            -h      Print a manpage
            -p p    Set percentage interval 
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Use colors
        d["-p"] = 10        # Percentage interval
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chp:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
                d[o] = not d[o]
            elif o == "-p":
                try:
                    d[o] = flt(a)
                    if not (0 < d[o] <= 100):
                        Error("-p argument must be > 0 and <= 100")
                except ValueError:
                    Error(f"-p option's argument must be a number > 0")
            elif o == "-h":
                Usage()
        GetColors(d["-c"])
        return args
if 1:   # Core functionality
    def Data():
        'Return [[%chg, OCVoltage], ...]'
        pct = [int(i) for i in reversed("100 90 80 70 60 50 40 30 20 10 0".split())]
        V = [flt(i) for i in reversed("3.40 3.35 3.32 3.30 3.27 3.26 3.25 3.22 3.20 3.00 2.50".split())]
        return pct, V
    def PrintBatteryDetails(num_cells):
        print(dedent(f'''
        LiFePO₄ battery ({num_cells} cells)
        % charge vs. rested open circuit voltage
        '''))
        pct, V = Data()
        f = interp1d(pct, V)
        flt(0).rtz = False
        w1, w2, ten, five = 5, 5, flt(10), flt(5)
        o = [f"{'%':^{w1}s} {'V':^{w2}s}"]
        for p in frange("0", "100", str(flt(d["-p"])), impl=flt, include_end=True):
            with p:
                p.rtz = p.rtdp = True
                ps = f"{p!s:^{w1}s}"
            try:
                V = flt(num_cells*f(p))
            except ValueError:
                continue
            with V:
                V.rtz = V.rtdp = False
                V.N = 4
                Vs = f"{V!s:^{w2}s}"
            c = ""
            if not (p % ten):
                c = t.ten
            elif not (p % five):
                c = t.five
            o.append(f"{c}{ps} {Vs}{t.n}")
        if d["-p"] < 5:
            for i in Columnize(o, columns=5, sep=" "*5):
                print(i)
        else:
            for i in o:
                print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    N = 4
    if args:
        for arg in args:
            try:
                N = int(arg)
                if N < 1:
                    Error("N must be > 0")
                PrintBatteryDetails(N)
            except ValueError:
                Error(f"{arg!r} isn't a valid integer")
    else:
        PrintBatteryDetails(4)
