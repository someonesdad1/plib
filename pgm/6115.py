'''
'''
_pgminfo = '''
<oo 
    Script to calculate current limit from 10-turn dial reading for HP 6115A power
    supply.  This is done using interpolation from a calibration done with my Aneng 870
    #2 on 6 Sep 2026.  Note the Aneng's calibration was NOT checked with the L&N 0.1 ohm
    resistance standard.
oo>
<oo cr Copyright © 2026 Don Peterson oo>
<oo cat elec oo>
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
        import scipy
        from columnize import Columnize
        from dpmath import RoundOff
        from get import GetNumber
        from f import flt
        from wrap import dedent
        import trm
        t = trm.TrmDP()
        from lwtest import Assert
        from dputil import PP
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
        t.mA = t.whtl
        t.dial = t.orn
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
        Usage:  {sys.argv[0]} [options] [mA1 [mA2...]]
          Display the dial reading for the desired current limit in mA.  Dial reading is
          a float on [0, 10].  Setting accuracy is one to two mA.  For no argument,
          print a table of current in mA versus dial setting.
        Options:
            -i      Inversion:  for the dial setting on the command line, print the
                    resulting current in mA.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = False     # Inversion calculation
        d["-t"] = False     # Current table
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hi") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("it"):
                d[o] = not d[o]
            elif o == "-h":
                Usage()
        GetColors()
        if not args:
            DialTable() if d["-i"] else CurrentTable()
            exit()
        return args
if 1:   # Core functionality
    dial = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10)
    current_mA = (0, 99.2, 196.2, 290.1, 380.9, 469.8, 555.8, 639.8, 721.3, 800.4, 877.4)
    forward_interp = scipy.interpolate.interp1d(dial, current_mA)
    reverse_interp = scipy.interpolate.interp1d(current_mA, dial)
    def GetDialReading(mA):
        'mA is a float on [0, max(current_mA)]'
        try:
            y = float(reverse_interp(mA))  # The interp returns a numpy.ndarry of size 1
        except ValueError:
            print(f"{mA} mA is out of allowed current bounds:")
            Error(f"  Current must be in [0, {max(current_mA)}] mA")
        reading = RoundOff(y, 3)
        return reading
    def GetCurrentReading(reading):
        'reading is a float on [0, 10]'
        try:
            y = float(forward_interp(reading))  # The interp returns a numpy.ndarry of size 1
        except ValueError:
            print(f"{reading} is out of allowed dial values:")
            Error(f"  Dial reading must be a float in [0, 10]")
        current = RoundOff(y, 3)
        return current
    def CalculateDialReading(mA):
        'mA is a float on [0, max(current_mA)]'
        reading = GetDialReading(mA)
        print(f"Current = {RoundOff(mA)} mA  Dial = {reading:5.2f}")
    def CalculateCurrent(reading):
        'reading is a float on [0, 10]'
        y = float(forward_interp(reading))  # The interp returns a numpy.ndarry of size 1
        current = GetCurrentReading(reading)
        print(f"Dial = {RoundOff(reading)}  current = {int(current):3d} mA")
    def CurrentTable():
        o = [f" {t.mA}mA{t.N}  {t.dial}Dial{t.N}"]
        for mA in range(0, 877, 5):
            dial = GetDialReading(mA)
            o.append(f"{t.mA}{mA:3d} {t.dial}{dial:5.2f}{t.N}")
        t.print(f"{t.trq}Dial setting for desired current in mA for HP 6115A power supply")
        for i in Columnize(o, sep=" "*5):
            print(i)
    def DialTable():
        o = [f" {t.dial}Dial{t.N}   {t.mA}mA{t.N}"]
        for int_dial in range(0, 1000, 5):
            dial = int_dial/100
            mA = GetCurrentReading(dial)
            o.append(f"{t.dial}{dial:5.2f}{t.N}  {t.mA}{int(mA):3d}{t.N}")
        t.print(f"{t.trq}Current in mA for dial setting for HP 6115A power supply")
        for i in Columnize(o, sep=" "*5):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-i"]:
        msg = "Dial reading must be float on [0, 10]"
        for dial_reading in args:
            try:
                reading = float(dial_reading)
            except Exception:
                Error(msg)
            CalculateCurrent(reading)
    else:
        msg = f"Current in mA must be float on [0, {max(current_mA)}]"
        for milliamperes in args:
            try:
                mA = float(milliamperes)
            except Exception:
                Error(msg)
            CalculateDialReading(mA)
