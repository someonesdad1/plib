'''
Help with rattle measurements.

Roll rattle

    d = diameter = L/sqrt(1 - a**2/4)
    L = caliper length setting
    w = a*L

Pitch rattle

    d = desired diameter
    c = d + eps
    eps = desired interference
    a = rattle measurement is approximately sqrt(2*d*eps)

'''
dbg = 1
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Help with rattle measurements
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
        from functools import partial
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, t
        from u import u
        from f import flt, sqrt
        import get
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        t.ans = t("purl")
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] type
          Use 'r[oll]' or 'p[itch]' for the type of rattle measurement.
          Prompts you for the needed dimensions and calculates the third.
          L = rod length, a = rattle distance, D = diameter
          Inches are the default unit, but you can append a unit to any
          dimensions you're prompted for.
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 4         # Number of significant digits
        d["-m"] = False     # Default to mm
        if not dbg and len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Manpage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        # Set up flt characteristics
        x = flt(0)
        x.N = d["-d"]
        x.rtz = False
        if dbg:
            args = ["r"]
        return args[0]
    def Manpage():
        print(dedent(f'''
        Roll rattle
        -----------

        Rattle measurements use a rod of known length to measure a hole
        diameter.  The principle is that the rod length L is slightly less
        than the diameter d to be measured.  When the rod is inserted into
        the hole, one side is stationary on the bore diameter and the other
        side "rattles" back and forth a distance w between two points of
        contact with the bore.  The rattle distance w can be measured with
        a rule to about 1 mm resolution.  The bore diameter can be
        calculated from

            d = L/sqrt(1 - a**2/4)

        where a = w/L.

        Example:  a bore uses a rod length of 99 mm with a rattle distance
        of w = 6 mm.  What is the bore diameter?  Here, a = w/L = 6/99.

            d = 99/sqrt(1 - a**2/4) = 99/sqrt(1 - 36/(99**2*4) 
              = 98.955 mm

        Pitch rattle
        ------------

        This is used to create an interference fit.  Let L be the rod
        length (i.e., setting of the inside calipers) and let d be the 
        basic shaft diameter.  eps is the desired interference.  a is the
        rattle distance.  We have approximately

            a ≅ sqrt(2*d*eps)

        Example:  a d = 4 inch basic bore needs a shaft with a 0.002
        inch interference fit.  What should the rattle distance a be?

            a = sqrt(2*4*0.002) = sqrt(0.016) = 0.126

        Thus, set your calipers to 4.126 inches and bore the hole out until
        the pitch rattle is 1/8 inches from the entry to the bore.
        '''))
        exit(0)
if 1:   # Core functionality
    GetNum = partial(get.GetNumber, allow_none=True, numtype=flt)
    def RollRattle():
        print("Roll rattle:  enter nothing for the unknown")
        while True:
            if dbg:
                d = None
                L = sqrt(2)
                w = flt(2)
                w.N = 6
                w.rtz = 0
            else:
                d = GetNum("What is diameter? ")
                L = GetNum("What is rod length? ")
                w = GetNum("What is rattle distance? ")
            if d is None:
                if L is None or w is None:
                    print("Not enough things defined")
                    continue
                a = flt(w/L)
                b = 1 - a**2/4
                if b <= 0:
                    print(f"Bad w and L values give complex result")
                    if dbg:
                        exit(1)
                    continue
                if b == 0:
                    print(f"Bad w and L values give infinite result")
                    if dbg:
                        exit(1)
                    continue
                d = flt(L/sqrt(b))
                print(f"L = {L}")
                print(f"w = {w}")
                t.print(f"{t.ans}d = {d}")
            elif L is None:
                if L is None or w is None:
                    print("Not enough things defined")
                    continue
            elif w is None:
                if L is None or w is None:
                    print("Not enough things defined")
                    continue
            else:
                print("Leave one variable undefined")
            if dbg: exit(0) #xx
            
    def PitchRattle():
        pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    arg = ParseCommandLine(d)
    RollRattle() if arg.lower()[0] == "r" else PitchRattle()
