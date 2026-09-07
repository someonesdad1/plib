'''
ToDo
    - -y option doesn't work.  Default should be equal steps in longitudinal direction
      and -y should change output to what's used currently.

Turning a ball on the lathe:  calculations via the incremental cut method
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2012 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Ball turning in the lathe
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        from math import sqrt
        import sys
        import os
        import getopt
    if 1:  # Custom imports
        from wrap import dedent
        import termtables as tt
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} OD step
          Print a table of incremental cuts to form a spherical shape on a lathe.  
            x direction = parallel to the rotation axis towards the tailstock 
            y direction = cross slide movement towards the back of the lathe
          The table that is printed out cuts half of the sphere, so you'll need to use
          it in both longitudinal directions to cut a complete sphere.  OD and step are
          lengths and must use the same units, but the printout doesn't assume any
          units.

          The formula used is y = r - sqrt(r² - x²).  This assumes you'll turn a
          ball on the end of some bar stock and you start at x = 0 where the y
          coordinate is also 0.  This is where you touch the edge of the cutting tool to
          the work and set the cross slide to zero.  Move the longitudinal feed to the
          right by step, feed the cross slide in to the indicated y value, and thus make
          the first step cut.  Repeat until the cutting tool is at the center of
          rotation.
        Options
          -d n  Number of decimal places to use [{d['-d']}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-d"] = 3  # Number of decimal places
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "d:h")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o in "":
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Manpage()
        if len(args) != 2:
                Usage()
        return args
if 1:  # Core functionality
    def Script():
        'This is a stand-alone script to do what Calculate() does'
        OD = 1          # Outside diameter of ball
        step = 0.05     # Longitudinal movement for each step
        r, x, i = OD/2, 0, 0    # Radius, x coordinate, step number
        digits = 3
        w1, w2, w3 = 3, 12, 9
        print(f"Ball diameter  = {OD}")
        print(f"Longitudinal step = {step}\n")
        print("Num  Longitudinal  Crossfeed")
        print("---  ------------  ---------")
        while True:
            x = i*step
            if x > r:
                break
            y = r - sqrt(r**2 - x**2)
            print(f"{i:^{w1}d}  {x:^{w2}.{digits}f} {y:^{w3}.{digits}f}")
            i += 1
    def Calculate(OD, step):
        print(f"Ball diameter  = {OD}")
        print(f"Longitudinal step = {step}\n")
        o = [
            ["Num", "Longitudinal", "Crossfeed"],
            ["---", "------------", "---------"],
        ]
        digits = d["-d"]
        r = OD/2
        x = 0
        i = 0
        while True:
            x = i*step
            if x > r:
                break
            y = r - sqrt(r**2 - x**2)
            o.append([f"{i:d}", f"{x:.{digits}f}", f"{y:.{digits}f}"])
            i += 1
        tt.print(o, style=" "*15, alignment="c"*3)

if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    OD = float(args[0])
    step = float(args[1])
    if OD <= 0:
        Error("OD must be > 0")
    if step <= 0:
        Error("step must be > 0")
    Calculate(OD, step)
    Script()
