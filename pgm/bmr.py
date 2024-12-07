'''
Estimate daily energy need
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
        Usage:  {sys.argv[0]} [options] mass_kg height_m age_years
          Estimate an adult male's daily energy need.  Activity level is
            1   Sedentary (default)
            2   Moderate
            3   Active
            4   Very active
        Options:
            -f      Prediction for a female
            -h      Print a manpage
            -u      Use mass in lb and height in inches
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-f"] = False     # Female
        d["-d"] = 3         # Number of significant digits
        d["-u"] = False     # Use lbm and inches
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "fd:hu") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("fu"):
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
        if len(args) not in (3, 4):
            Usage()
        return args
if 1:   # Core functionality
    def HarrisBenedict(m, h, y, a, female=False):
        '''Harris-Benedict 1919, revised by Mifflin and St Jeor in 1990.
        https://en.wikipedia.org/wiki/Harris%E2%80%93Benedict_equation
            m is mass in kg
            h is height in m
            y is age in years
            a is activity level in (1, 2, 3, 4)
        Test case:  should return xxxxxx for m = 70 kg, h = 1.75 m, y = 70 years, a = 1, and for a
        male.  For a female, it should return xxxxxx.
        '''
        kcal = 10*m + 625*h - 5*y
        if female:
            activity = {1: 1.3, 2: 1.5, 3: 1.6, 4: 1.9, 5: 2.2}
            p = activity[a]
            kcal -= 161
        else:
            activity = {1: 1.3, 2: 1.6, 3: 1.7, 4: 2.1, 5: 2.4}
            p = activity[a]
            kcal += 5
        kcal *= p
        return flt(kcal)
    def IofM(m, h, y, a, female=False):
        '''Institute of Medicine formula, dated 2002.  Return daily energy need in kcal.
        Ref. https://en.wikipedia.org/wiki/Institute_of_Medicine_Equation
            m is mass in kg
            h is height in m
            y is age in years
            a is activity level in (1, 2, 3, 4)
        Test case:  should return 2052.9 for m = 70 kg, h = 1.75 m, y = 70 years, a = 1, and for a
        male.  For a female, it should return 1796.6.
        '''
        if female:
            activity = {1: 1, 2: 1.12, 3: 1.27, 4: 1.45}
            p = activity[a]
            EER = 354.6 - 6.91*y + 9.36*m*p + 726*h
        else:
            activity = {1: 1, 2: 1.11, 3: 1.25, 4: 1.48}
            p = activity[a]
            EER = 662 - 9.53*y + 15.91*m*p + 539.6*h
        return flt(EER)
    def Test():
        m = 70; h = 1.75; y = 70; a = 1
        if 1:   # IofM
            assert IofM(m, h, y, a, False) == 2052.9
            assert IofM(m, h, y, a, True) == 1796.6

if __name__ == "__main__":
    d = {}      # Options dictionary
    Test()
    args = ParseCommandLine(d)
    to_kg = 0.45359237 if d["-u"] else 1
    to_m = 0.0254 if d["-u"] else 1
    m = flt(args[0])*to_kg
    h = flt(args[1])*to_m
    y = flt(args[2])
    # Check parameters
    if m < 30:
        Error("Mass less than 30 kg")
    if h < 1:
        Error("Height less than 1 m")
    if y < 18:
        Error("Age less than 18 years")
    print("Input:")
    print(f"    Mass           = {m} kg")
    print(f"    Height         = {h} m")
    print(f"    Age            = {y} years\n")
    print(f"Institute of Medicine formula:  daily energy need in kcal")
    A = {1: "Sedentary", 2: "Moderate", 3: "Active", 4:"Very active"}
    print(f"  Activity level    Male    Female")
    print(f"  --------------    ----    ------")
    w = 14
    for a in range(1, 5):
        kcal_male = IofM(m, h, y, a, False)
        kcal_female = IofM(m, h, y, a, True)
        print(f"  {A[a]:^{w}s}    {kcal_male!s:4s}     {kcal_female!s:4s}")
    print(f"\nHarris-Benedict formula:  daily energy need in kcal")
    A = {1: "Sedentary", 2: "Light", 3: "Moderate", 4:"Very", 5: "Extremely"}
    print(f"  Activity level    Male    Female")
    print(f"  --------------    ----    ------")
    for a in range(1, 6):
        kcal_male = HarrisBenedict(m, h, y, a, False)
        kcal_female = HarrisBenedict(m, h, y, a, True)
        print(f"  {A[a]:^{w}s}    {kcal_male!s:4s}     {kcal_female!s:4s}")
