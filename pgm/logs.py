'''

Produce log tables

'''
_pgminfo = '''
<oo 
    desc Produce log tables
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat math oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque
        from pathlib import Path as P
        from math import log10
        import getopt
        import math
        import os
        import re
        import statistics
        import sys
    if 1:   # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from dpprint import PP
        pp = PP()   # Get pprint with current screen width
        import termtables as tt
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
    def GetColors():
        t.stuff = t.lill
        t.err = t.redl
        t.dbg = t.lill if g.dbg else ""
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
    def Warn(*msg, status=1):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warn(*msg)
        exit(status)
    def Usage(status=0):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] type
          Type
            1       4 figure text [default]
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        if 0 and len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    def Logs_4figures():
        def header_row():
            print(t.ornl, end="")
            print(" "*3, end="")
            for i in range(10):
                print(f"{' ' + str(i):^4s}", end=" ")
            for i in range(1, 10):
                print(f"{' ' + str(i):^2s}", end=" ")
            print(t.n)
        o = []
        t.print(f"{t('whtl', attr='ul')}4 place log table")
        for row in range(10, 100):
            d, remainder = divmod(row - 10, 10)
            if not remainder:
                header_row()
            PP = []     # Accumulate proportional parts for row
            print(f"{row}", end=" ")
            for i in range(10):
                l = log10(row + i/10) - 1
                PP.append(l)
                s = f"{l:.4f}"[2:]
                print(f"{s}", end=" ")
            # Now print PP
            p = []
            for i, pp in enumerate(PP):
                if not i:
                    continue
                p.append(int(1e4*(PP[i] - PP[i - 1])))
            mean = statistics.mean(p)
            for i in range(1, 10):
                print(f"{int(i/10*mean + 0.5):2d}", end=" ")
            print()

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    try:
        typ = int(args[0])
    except IndexError:
        typ = 1
    if typ == 1:
        Logs_4figures()
    else:
        Error("Number not recognized")
