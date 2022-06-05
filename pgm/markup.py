'''
Interactive utility to calculate profit and markup

c = cost of an item
s = selling price of an item
p = profit as a fraction of the selling price
m = markup as a fraction of the cost

Equations
    c = s*(1 - p)
    s = c*(1 + m)
    p = m/(1 + m) = 1 - 1/p
    m = p/(1 - p)
    μ = 1/(1 - p) = multiplier
    m = p*μ


Prompt for c, s, p, m.  Leave one of them blank.  Calculate results with:

    csp:  m = p/(1 - p)
    csm:  p = m/(1 + m)
    cpm:  s = c*(1 + m)
    spm:  c = s*(1 - p)

This should also include the ability to let you enter '.' when
you are prompted for cost.  You're then prompted for $/hr for labor (enter
'.' to use a default value), number of hours labor, and parts cost.  This
gives you a total cost and lets you put a cost on your time.

An example of use is to estimate the actual profit on a project. 

The output report can report in color, with the color designating the
goodness of a result:  
                p                 m
    red      < 0.25           < 0.3
    wht    0.25 - 0.5           0.3 - 1
    yell   0.5 - 0.66          1 - 2
    ornl   0.66 - 0.8          2 - 4
    magl   0.8 - 0.83          4 - 5

'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Program description string
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        import getopt
        import os
        from pathlib import Path as P
        import sys
        from pdb import set_trace as xx
    # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
    # Global variables
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
        if len(sys.argv) < 2:
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
                Usage(status=0)
            elif o in ("--debug",):
                # Set up a handler to drop us into the debugger on an
                # unhandled exception
                import debug
                debug.SetDebugger()
        return args
if 1:   # Core functionality
    pass

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
