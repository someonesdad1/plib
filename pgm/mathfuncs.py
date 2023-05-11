'''
Identify the functions in math/cmath and print out their return types
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2023 Don Peterson #∞copyright∞#
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
        import getopt
        import math
        import cmath
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from columnize import Columnize
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] etc.
          Explanations...
        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        #if len(sys.argv) < 2:
        #    Usage()
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
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    def Math():
        funcs = []
        for i in dir(math):
            if i.startswith("__"):
                continue
            f = eval(f"math.{i}")
            t = type(f)
            if "float" in str(t):
                continue
            funcs.append(i)
        print("Math functions:")
        for i in Columnize(funcs, indent=" "*2):
            print(i)
    def CMath():
        funcs = []
        print()
        for i in dir(cmath):
            if i.startswith("__"):
                continue
            f = eval(f"cmath.{i}")
            t = type(f)
            if "float" in str(t):
                continue
            funcs.append(i)
        print("Cmath functions:")
        for i in Columnize(funcs, indent=" "*2):
            print(i)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    Math()
    CMath()
