_pgminfo = '''
<oo desc
    Script to look up machining data
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo license
    Licensed under the Open Software License version 3.0.
    See http://opensource.org/licenses/OSL-3.0.
oo>
<oo cat shop oo>
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
if 1:   # Data
    # "Manual of Lathe Operation", Clausing, 27th ed, 1973
    # pg 36 Diagrams of tool bit shapes

    # pg 50 Tool angles and speeds for machining steel
    #   Description
    #   SAE number
    #   Machinability %
    #   Speed ft/min
    #   Side clearance, ° 
    #   Front clearance, ° 
    #   Back rake, ° 
    #   Side rake, ° 
    steel = '''
    '''
    # pg 52-64 Tool angles 
    #   Material
    #   Speed ft/min
    #   Front clearance, ° 
    #   Side clearance, ° 
    #   Back rake, ° 
    #   Side rake, ° 
    material = '''
    Cast iron;50;8;10;5;12
    Stainless steel;40;10;12;16.5;10
    Copper;120;12;14;16.5;20
    Brass;200 to 600;8;10;0;0
    Harder copper alloys;80-120;12;10;10;0 to -2
    Hard bronze;40 to 100;8;10;0;0 to -2
    Aluminum;200 to 800;8;12;35;15
    Monel & nickel;100;13;15;8;14
    Phenol plastics (Bakelite);100;8;12;0;0
    Other plastics;200;10;14;0 to 5;0
    Formica;200 to 300;10;15;16.5;10
    Hard rubber;150;15;20;0;0
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
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Need description
        d["-d"] = 3         # Number of significant digits
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
                except ValueError:
                    Error(f"-d option's argument must be an integer between 1 and 15")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
