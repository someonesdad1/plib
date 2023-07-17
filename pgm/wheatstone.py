'''
Calculation Wheatstone bridge problems
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
        import os
        from pathlib import Path as P
        import sys
    if 1:   # Custom imports
        from wrap import wrap, dedent
        from color import Color, TRM as t
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from lwtest import Assert
        from f import flt
    if 1:   # Global variables
        ii = isinstance
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        Use of the Wheatstone bridge script
        '''))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] R1 R2 R3 Vin [Vout]

          Calculate the unknown resistance Rx of a Wheatstone bridge.  Left
          arm of bridge is R1 and R3.  Right arm is R2 and Rx.  +Vin is
          applied to the common connection of R1 and R2 and -Vin is applied
          to the common connection of R3 and Rx.  If Vout is not given, it
          is assumed the bridge is balanced (i.e., Vout = 0).  You can use
          the short-form notation for uncertainty as e.g.  1.00(3) to mean
          1.00 ± 0.03 where 0.03 is the standard uncertainty.

        Options:
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-v"] = False     # Debugging output
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "hv", 
                    ["help", "debug"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("v"):
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
        return args
if 1:   # Core functionality
    def GetNum(s):
        '''Return a ufloat from s, which can either be a regular float
        string like '1.23' or '1.23e9' or contain a short-form uncertainty
        as in '1.23(3)'.  Note these are the only two allowed forms.
        '''
        try:
            if "(" in s:
                return ufloat_fromstr(s)
            else:
                return ufloat(float(s), 0)
        except Exception:
            print(f"{s!r} is not a valid number")
            exit(1)
    def Calculate(R1, R2, R3, Vin, Vout):
        a = (R1 + R2)*Vout/Vin
        return (R2*R3 + a)/(R1 - a)
    def P(x):
        '''Return a string for the ufloat x.  The first string is the short
        form and the second is the % level of the uncertainty.
        '''
        Assert(ii(x, UFloat))
        s1 = f"{x:fS}"
        m, s = flt(x.n), flt(x.s)
        p = flt(100*s/m)
        return f"{s1} = {m} ± {p}%"
    def Report(R1, R2, R3, Rx, Vin, Vout):
        print(f"Vin  = {P(Vin)}")
        print(f"Vout = {P(Vout)}")
        print(f"R1   = {P(R1)}")
        print(f"R2   = {P(R2)}")
        print(f"R3   = {P(R3)}")
        print(f"Rx   = {P(Rx)}")

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    R1 = GetNum(args[0])
    R2 = GetNum(args[1])
    R3 = GetNum(args[2])
    Vin = GetNum(args[3])
    Vout = GetNum(args[4]) if len(args) == 5 else GetNum("0")
    Rx = Calculate(R1, R2, R3, Vin, Vout)
    Report(R1, R2, R3, Rx, Vin, Vout)
