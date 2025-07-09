'''
'''
_pgminfo = '''
<oo 
    Script to calculate resistance values for a remote control box for the HP 6033A DC
    power supply (and similar power supplies).
oo>
<oo cr Copyright © 2025 Don Peterson oo>
<oo cat oo>
<oo test none oo>
<oo todo oo>
'''
 
if 1:  # Header
    if 1:   # Standard imports
        from collections import deque, namedtuple
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:   # Custom imports
        from get import GetNumber
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
        t.v = t.trql
        t.i = t.lipl
        t.err = t.redl
        t.warn = t.ornl
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
        Usage:  {sys.argv[0]} [options] cmd
          Interactive script to calculate the needed resistances for the remote
          programming box for the HP 603X power supplies.  You will input the desired
          current and voltage levels.  For cmd, use '3' for the 6033A and '8' for the
          6038A.
        
          These calculations are specific to the custom box I plan to make for these
          power supplies.  This box has one coarse-adjust pot and one fine-adjust pot.
          This fits the following use case:  a typical experiment needs to have either
          voltage or current set to some maximum value, then the other parameter is
          finely adjusted for the experiment's output.  These pots have auxiliary pots
          or resistors that can be used to limit the low and high values reachable.
        Options:
            -3      Use the 6033A power supply [default]
            -8      Use the 6038A power supply
            -v v    Set the input voltage to resistance box
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-3"] = False     # HP 6033A supply
        d["-8"] = False     # HP 6038A supply
        d["-v"] = 5         # Input voltage in V to resistor box
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "38hv:") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("38"):
                d[o] = not d[o]
            elif o == "-v":
                try:
                    d[o] = flt(a)
                    if d[o] < 5:
                        raise ValueError()
                except ValueError:
                    Error(f"-v option's argument must be a number >= 5 V")
            elif o == "-h":
                Usage()
        GetColors()
        return args
if 1:   # Core functionality
    # Power supply data
    ps = namedtuple('PowerSupply', 'V i Vcontrol')
    five_volt = 5
    data = {
        # The values given are the maximum readings I can get from the supplies that I
        # have on hand
        "HP6033A": ps(20.4, 30.7, five_volt),
        "HP6038A": ps(61.3, 10.24, five_volt),
    }
    def GetParameter(name, minimum, maximum, unit, c=t.wht):
        ok = False
        while not ok:
            s = f"{c}What is minimum {name} [{minimum} to {maximum} {unit}]?{t.n}"
            pmin = GetNumber(s, default=minimum, low=minimum, high=maximum)
            s = f"{c}What is maximum {name} [{minimum} to {maximum} {unit}]?{t.n}"
            pmax = GetNumber(s, default=maximum, low=minimum, high=maximum)
            if pmin != pmax:
                ok = True
            else:
                t.print(f"{t.warn}Minimum and maximum {name} cannot be equal")
        pmin, pmax = (pmax, pmin) if pmax < pmin else (pmin, pmax)
        return pmin, pmax
    def HP6033A():
        model = "HP6033A"
        Vmax, Imax, Vcontrol = data["HP6033A"]
        print(f"{t.yel}{model}{t.n} power supply")
        vmin, vmax = GetParameter(f"voltage", 0, Vmax, "V", c=t.v)
        imin, imax = GetParameter(f"current", 0, Imax, "A", c=t.i)
        #
        print(f"Voltage range = {vmin}, {vmax} V")
        print(f"Current range = {imin}, {imax} A")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    cmd = args[0]
    if cmd == "3":
        HP6033A()
    elif cmd == "8":
        HP6033A()
    else:
        Error(f"{cmd!r} unrecognized")

