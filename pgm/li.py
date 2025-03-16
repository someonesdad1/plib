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
        Usage:  {sys.argv[0]} [options] [%step]
          Print out LiFePO₄ battery characteristics for a 1% step in capacity.  Change
          the step percentage by a command line argument.
        Options:
            -h      Print a manpage
            -n c    Number of cells [{d["-n"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = False     # Use colors
        d["-n"] = 4         # Number of cells
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "chn:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
                d[o] = not d[o]
            elif o == "-n":
                try:
                    d[o] = int(a)
                    if d[o] < 1:
                        raise ValueError
                except ValueError:
                    Error(f"-n option's argument must be an integer > 0")
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
    def PrintBatteryDetails(pct_step):
        print(dedent(f'''
        LiFePO₄ battery ({d["-n"]} cells)
        % charge vs. rested open circuit voltage
        '''))
        pct, V = Data()
        f = interp1d(pct, V)
        flt(0).rtz = False
        w1, w2, ten, five = 5, 5, flt(10), flt(5)
        o = [f"{'%':^{w1}s} {'V':^{w2}s}"]
        try:
            step = float(pct_step)
        except ValueError:
            Error(f"{str(pct_step)!r} is not a valid percentage step")
        for p in frange("0", "100", str(float(pct_step)), impl=flt, include_end=True):
            with p:
                p.rtz = p.rtdp = True
                ps = f"{p!s:^{w1}s}"
            try:
                V = flt(d["-n"]*f(p))
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
        if step < 5:
            for i in Columnize(o, columns=5, sep=" "*5):
                print(i)
        else:
            for i in o:
                print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if args:
        for arg in args:
            try:
                p = flt(arg)
                if p <= 0:
                    Error("%step must be a number > 0")
                PrintBatteryDetails(p)
            except ValueError:
                Error(f"{arg!r} isn't a valid integer")
    else:
        PrintBatteryDetails(1)
