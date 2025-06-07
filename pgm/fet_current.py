'''
'''
_pgminfo = '''
<oo 
    Estimate the current you can get from a MOSFET
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
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
        Usage:  {sys.argv[0]} [options] datafile
          Estimate the current you can get from a MOSFET.  Input comes from a datafile
          whose variables are (temperatures are in °C, common values for TO220 devices)

        * fet   Regex to select the MOSFET type
          Tmax  Maximum junction temperature                175
        * Tj    Maximum desired junction temperature        150
        * Tamb  Ambient operating temperature                40
          Rja   Thermal resistance junction to ambient K/W   62
          Rjc   Thermal resistance junction to case         0.5
          Rcs   Thermal resistance case to heat sink        0.5
          Ron   Channel resistance in Ω at Tj

          That 62 K/W junction to ambient thermal resistance means 1 W of power
          dissipated in the device means the junction will be 62 K above ambient
          temperature.  For Tj = 150 and Tamb = 40, ΔT = 110 K.  This lets us dissipate
          about 2 W or 110 K/(62 K/W).  Given Ron, we can calculate the operating 
          current as sqrt(P/Ron).  Suppose Ron is 3 mΩ.  Then i = sqrt(2/0.003) or 26 A.

          If you like, only include 'fet_regex Tj Tamb' on the command line and if the
          selected FET is matched, it will give you the maximum current from the
          internally-stored data.

        Options:
            -c      Print a sample datafile
            -l      List supported FET numbers
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
