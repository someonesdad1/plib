_pgminfo = '''
<oo desc
    Show properties of on-hand shunts
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat Put_category_here oo>
<oo test none oo>
<oo todo

    - List of todo items here

oo>
'''
 
if 1:  # Header
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
        from dpprint import PP
        import termtables as tt
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
if 1:   # Shunt data
    # Fields:  ID, manufacturer, model, rating in A, drop in mV, note
    data = '''
    GS1; ?; ?; 200; 100; From Greg Sali, in oak box for Westinghouse 50 A 100 mV shunt, probably from 1940's or before
    S100; ?; ?; 100; 50;
    S200; ?; ?; 200; 50;
    S300; Qeco; SWO300; 300; 50;
    S25; Weston; ?; 25; 50;
    S75-1; ?; ?; 75; 50; ebay 2010
    S75-2; ?; ?; 75; 50; ebay 2010
    S75-3; ?; ?; 75; 50; ebay 2010
    Si1; Simpson; ?; 10; 100; ebay 2022
    Si2; Simpson; ?; 10; 100; ebay >= 2022
    SF10; Fluke; 80J-10; 10; 100; ebay 2022
    '''
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
        Usage:  {sys.argv[0]} [options]
          Display my shunt numbering and properties.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
        #if len(sys.argv) < 2:
        #    Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
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
    def DisplayShuntData():
        o = [["Symbol", "Manufacturer", "Amperes", "mV"]]
        for shunt in data.split("\n"):
            shunt = shunt.strip()
            if not shunt or shunt[0] == "#":
                continue
            f = shunt.split(";")
            Assert(len(f) == 6)
            id, mfg, model, A, drop_mV, note = f
            o.append([f"{id}", f"{mfg}", f"{A}", f"{drop_mV}"])
        tt.print(o, style=" "*15, alignment="lcrr")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    DisplayShuntData()
