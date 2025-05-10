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
            1       4 place table, text
            2       4 place table, graphical
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
        GetColors()
        return args
if 1:   # Core functionality
    def Manpage_Logs_4figures():
        print()
        print(dedent('''

        This type of table is probably the most commonly-used logarithm table for
        routine calculations.  With care, you can get nearly 4 significant figures in
        the calculated results.  Most practical calculations that rely on measurements
        typically have 2 or 3 figures (1% to 0.1% resolution), so these log tables can
        help you perform mulitiplication and division with such numbers and avoid loss
        of accuracy due to roundoff errors.

        Example

            4.38**(-0.28).  Estimate the answer:  this is approximately 1/4**0.25 or the
            reciprocal of the fourth root of 4.  The fourth root of 4 is 1.414, the
            square root of 2 and the reciprocal is 0.707, which most folks who do
            calculations will remember.  Thus, 0.7 is an estimate.  Since 4.38 is about
            10% larger than 4, the result will be smaller than 0.7, so we'll estimate
            larger than 0.65 and less than 0.7.

            The log of 4.38 is found in the 43 row:

                     0    1    2    3    4    5    6    7    8    9
                43 6335 6345 6355 6365 6375 6385 6395 6405 6415 6425

            Looking under the 8 column, we get the log as 0.6415.  We must multiply this
            by -0.28 and it's something you'll have to do manually, giving -0.1795.
            Add 1 to get 0.8205.

            Row 66 in the table is

                     0    1    2    3    4    5    6    7    8    9
                66 8195 8202 8209 8215 8222 8228 8235 8241 8248 8254

            and 8205 is not quite half way between the 1 and 2 column:  it's 3/7ths of
            the way; knowing 1/7 is 0.14, this is 0.4, giving our estimate of 0.6614.
            If you check this with a calculator, you find the answer is 0.6613.

        '''))
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
        show_header = (10, 54)
        for row in range(10, 100):
            if row in show_header:
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
        Manpage_Logs_4figures()

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
