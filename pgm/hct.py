'''
Description of program
'''
 
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
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
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
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
        Usage:  {sys.argv[0]} [options] arg
          Calculate the output of the high current transformer when arg is an integer between 0
          and 115 representing the Variac % output.  Use the -i option to make arg a desired
          shorted secondary current in A and you'll get the required Variac setting for each terminal
          that is capable of meeting the goal.
        Options:
            -d n    Set significant digits to display [{d['-d']}]
            -h      Print a manpage
            -i      Interpret command line argument as desired current in A
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-i"] = False     # Interpret arg as desired current in A
        d["-d"] = 2         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h", "--debug") 
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
            elif o == "-h":
                Usage()
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def GetVariacSetting(desired_current_A):
        pass
    def DisplayOutputCurrent(Variac_percent):
        '''Given a Variac percent from 0 to 110, calculate what the shorted secondary output
        current in A will be for each terminal.

        The model is gotten from experimental measurements and assumes a linear relationship.  The
        equation is i = m*v + b where i is current in A and v is the Variac percentage that must
        be on [0, 110] when the Variac is using the 120 V range winding.

            Terminal    m = slope   b = intercept
                1         25            5.33
                2         18.77         10.7
                3         11.7971       7.57143
                4         8.23214       6.05
                5         6.22188      -0.614545
        '''
        if not (0 <= Variac_percent <= 110):
            raise ValueError("Variac_percent must be on [0, 110]")
        const = {
            1: (25,      5.33),
            2: (18.77,   10.7),
            3: (11.7971, 7.57143),
            4: (8.23214, 6.05),
            5: (6.22188, -0.614545),
        }
        print(f"Variac setting = {Variac_percent}%")
        for terminal in const:
            m, b = const[terminal]
            i = m*Variac_percent + b
            print(f"  Terminal {terminal}:  {i} A")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-i"]:
        desired_current_A = flt(args[0])
        GetVariacSetting(desired_current_A)
    else:
        Variac_percent = flt(args[0])
        DisplayOutputCurrent(Variac_percent)
