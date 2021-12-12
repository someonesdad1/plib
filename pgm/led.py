'''
Allows a design of LED and resistor given the power rating of the resistor
you want to use
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
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
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
    from pprint import pprint as pp
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumbers as GN
    from interpolate import LinearInterpFunction
    from frange import frange
    from f import flt
    from resistors import FindClosest
    from fpformat import FPFormat
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    # LED characteristics
    i_mA = GN("0.5 1 2 5 10 15 20 25 30 40 50")
    LED = {
        # V in V array, i in mA array
        "red": GN("1.71 1.77 1.82 1.89 1.97 2.02 2.06 2.09 2.12 2.17 2.21"),
        "grn": GN("2.18 2.30 2.43 2.65 2.89 3.06 3.19 3.30 3.40 3.57 3.72"),
        "blu": GN("2.42 2.52 2.59 2.71 2.89 3.02 3.13 3.23 3.32 3.46 3.58"),
    }
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] color V
          Suppose you want to run an LED of the indicated color at the
          stated supply voltage in volts.  The script will print out the
          resistance to use to run at this voltage, giving the designs for
          every 10% of the resistor power rating.  Colors can be grn, red,
          yel, wht, blu.  (yel, wht not supported yet)

          The output table shows the %power column which is the fraction of
          the rated power of the resistor at the indicated operating
          current.  If a '-' is printed, it means the power is more than 
          the power rating of the resistor.
        Options:
            -a      Show all the current choices
            -d n    Set number of significant figures
            -3      Use 3 mm LED data (5 mm is default)
            -h      Print LED data used
            -p      Print tables for a range of common powers
            -v      Include voltage drop across LED
            -w p    Resistor power in W [{d["-w"]}]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Show all the current choices
        d["-3"] = False     # Use 3 mm LED data
        d["-d"] = 3         # Number of significant digits
        d["-p"] = False     # Print for range of powers
        d["-v"] = False     # Include LED voltage drop
        d["-w"] = 0.25      # Default resistor power in W
        try:
            opts, args = getopt.getopt(sys.argv[1:], "3ad:hpvw:")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("3apv"):
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
            elif o in ("-w",):
                try:
                    d["-w"] = flt(a)
                    if d["-w"] <= 0:
                        raise ValueError()
                except ValueError:
                    Error("-w option's argument must be > 0")
            elif o in ("-h", "--help"):
                Usage(status=0)
        if len(args) != 2:
            Usage()
        if d["-3"]:
            raise ValueError("Not supported yet")
        x = flt(0)
        x.n = d["-d"]
        x.rtz = x.rtdp = True
        return args
if 1:   # Core functionality
    def Solve(color, voltage, pwr):
        FP = FPFormat(num_digits=d["-d"])
        fp = FP.engsi
        FP.trailing_decimal_point(False)
        V = LED[color]
        V2i = LinearInterpFunction(V, i_mA)
        i2V = LinearInterpFunction(i_mA, V)
        I = list(frange("0.5", "1", "0.1"))
        I.extend(range(1, 11, 1))
        I.extend(range(12, 21, 2))
        I.extend(range(25, 51, 5))
        # Make an array of [i, V, voltage - V, R, pct_pwr]
        o = []
        for i in I:
            V = i2V(i)
            ΔV = voltage - V
            if ΔV > 0:
                R = FindClosest(ΔV/(i/1000))
                if R is None:
                    if not d["-a"]:
                        i = 1000
                        continue
                    o.append([i, V, voltage - V, "-", "-"])
            p = (i/1000)**2*R
            pct = flt(100*p/pwr)
            o.append([i, V, fp(R), pct])
        #-------------------------------------------
        # Print results
        w = 40 if d["-v"] else 30
        print(f"{'LED Resistor Selection':^{w}s}")
        print(f"{'----------------------':^{w}s}")
        print()
        print(f"Operating voltage = {voltage} V")
        print(f"LED color = {color}")
        print(f"LED diameter =  mm")
        print(f"Resistor power = {pwr!s:s} W")
        print()
        w = 10
        print(f"{'i, mA':^{w}s} ", end="")
        if d["-v"]:
            print(f"{'V, V':^{w}s} ", end="")
        print(f"{'R, Ω':^{w}s} ", end="")
        print(f"{'%power':^{w}s} ")
        for j in o:
            i, V, R, pct = j
            print(f"{i!s:^{w}s} ", end="")
            if d["-v"]:
                print(f"{V!s:^{w}s} ", end="")
            print(f"{R:^{w}s} ", end="")
            if pct > 100:
                if not d["-a"]:
                    print()
                    break
                print(f"{'-':^{w}s} ")
            else:
                print(f"{str(int(pct)):^{w}s} ")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    color, voltage = args[0], flt(args[1])
    if d["-p"]:
        for pwr in (1/8, 1/4, 1/2, 1, 2, 5):
            Solve(color, voltage, pwr)
    else:
        pwr = d["-w"]
        Solve(color, voltage, pwr)
