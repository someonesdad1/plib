'''

Script to estimate mass and cost of a number of pieces of barstock material

    - Datafile syntax
        - Units
            - diameter = mm     # Default diameter unit
            - length = m        # Default length unit
            - mass = kg         # Default mass unit
            - cost = $          # Default cost unit
        - Material
            - matl = x          # Current default material
        - Bar specifics
            - rnd: dia = x, L = x
            - hex: dia = x, L = x
            - sq: dia = x, L = x
            - oct: dia = x, L = x
            - rect:  w = x, h = x, L = x
        - Syntax
            - 'dia = x', x is a string for Num constructor, given default diameter units
              if no units given
            - 'L = x', x is a string for Num constructor, given default length units if
              no units given
        
'''
if 1:  # Header
    if 1:   # Standard imports
        #import collections
        import getopt
        import os
        #import pathlib
        import re
        import sys
    if 1:   # Custom imports
        #import columnize
        from dbg import Dbg
        #import dpstr
        import dptypes
        #import f
        import number
        import trm
        import wrap
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Core file gist information
        __gist__      = "Print report on mass & cost of barstock"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "shop"
        __todo__      = ''' '''
    if 1:   # Import symbols
        dedent = wrap.dedent
    if 1:   # Global variables
        t = trm.Trm()
        g = dptypes.Constant()
        g.dbg = False
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = "lil"
        t.err = "redl"
    def Dbg(*p, **kw):
        if not hasattr(Dbg, "file"):
            Dbg.file = sys.stdout
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.n}", end="", file=Dbg.file)
    def Warning(*msg, **kw):
        print(*msg, file=sys.stderr)
    def Error(*msg, status=1):
        Warning(f"{t.err}", end="")
        Warning(*msg)
        Warning(f"{t.n}")
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] datafile
          Print summary report of sizes, overall lengths, mass, and cost of barstock
          pieces specified in datafile.
        Options:
            -c      Print out a sample datafile
            -d n    Number of significant digits
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False  # Description
        d["-d"] = 3      # Description
        if len(sys.argv) < 2:
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
                except Exception:
                    Error(f"{o!r} option must be an int between 1 and 15")
            elif o == "-h":
                Usage(status=0)
        GetColors()
        g.W, g.L = GetScreen()
        return args
if 1:   # Classes
    pass
if 1:   # Functions
    pass

if __name__ == "__main__":  
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if args:
        for arg in args:
            pass    # Do stuff
