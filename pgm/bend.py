if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Bend allowance computation for sheet metal
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import sys
        from functools import partial
    if 1:   # Custom imports
        from wrap import dedent
        from get import GetNumber
        from f import flt, radians
def BendAllowance():
    g = partial(GetNumber, low_open=True, low=0)
    print("Bend Allowance Computation (length units are arbitrary)\n")
    t = flt(g("t = thickness of material? "))
    r = flt(g("r = radius of bend?        "))
    θ = flt(g("θ = angle of bend in °?    "))
    θ = radians(θ)
    x = t/3 if r < 2*t else 2*t/10
    if r > 4*t:
        x = t/2
    t.N = 3
    print(dedent(f'''
    
    Length of bend exterior          {θ*(r + t)}
    Length of bend interior          {θ*r}
    Length of material to form bend  {θ*(r + x)}
 
    Formulas:
        if r < 2*t:
            x = t/3
        elif 2*t <= r <= 4*t:
            x = t/5
        else:
            x = t/2
        and
            Length of bend exterior          = θ*(r + t)
            Length of bend interior          = θ*r
            Length of material to form bend  = θ*(r + x)
    '''))
if 0 and __name__ == "__main__": 
    Intro()
    BendAllowance()

'''
ToDo
    - Use various algorithms

Bend allowance computation for sheet metal

    The fundamental dimensions for bending sheet metal are

        r = inside radius of the bend
        L = length of straight stock needed before bending
        θ = angle of bend in radians

    Important:  θ is how much the metal has to be bent from the flat to form the
    desired shape.  A bracket with an interior angle of 60 degrees needs to be bent by an
    angle of 120 degrees.  Conversely, a bracket with an interior angle of 120 degrees has a bend
    angle of 60 degrees.

    Algorithm 1:  Based on bend.c by M. Klotz.  Klotz lost the attribution, but thought it was
    probably one of Hoffman's articles in "Home Shop Machinist".

    Algorithm 2:  Base on MH 19th ed pg 1857.  The three formulas came from Westinghouse
    experiments for bench bending with simple tools and working to ±1/64th of an inch.
    The three cases are: 1) soft brass/copper, 2) half-hard copper/brass, soft steel, and
    aluminum, and 3) bronze, hard copper, cold-rolled steel, and spring steel.

        L = k*t + r*θ

    where k = 0.55 for case 1, 0.64 for case 2, 0.71 for case 3.

'''
if 1:   # Header
    if 1:   # Copyright, license
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
        import subprocess
        import sys
    if 1:   # Custom imports
        from color import t
        from dpprint import PP
        pp = PP()   # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl     # wsl is True when running under WSL Linux
        #from columnize import Columnize
    if 1:   # Global variables
        class G:
            # Storage for global variables as attributes
            pass
        g = G()
        g.dbg = False
        ii = isinstance
if 1:   # Utility
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stdout
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Manpage():
        print(dedent(f'''
        Suppose you want to bend a piece of sheet metal to make a right angle bracket with legs 1
        unit long.  If you could make a perfectly sharp bend in very thin metal, you'd start with a
        flat piece of 2 units long and make the bend.  With real materials of nontrivial thickness,
        the final bend will have a radius (i.e., it can't be sharp) and you'll need to add a bit
        extra material to the calculated length to get the desired finished length.  This extra is
        called the bend allowance and is due to the arc length of the material in the bend.

        Let the sheet metal thickness t be 1/8 inch, let the finished length L be 2 inches, and
        assume we'll get an inside radius of 1/8 inch for the 90° bend.  The arguments to the
        script would be '1/8 2 1/8' and the results would be

            Bending half-hard copper/brass, soft steel, or aluminum sheet
            t  = sheet metal thickness       0.125
            L  = finished length             2.00
            r  = inside bend radius          0.125
            θ  = bend angle                  90.0° = 1.57 radians
            BA = bend allowance              0.276
            L' = cut to length = L + BA      2.28

        The formula used in this script came from page 1857 of the 19th edition of Machinery's
        Handbook:

            BA = k*t + θ*r      (θ in radians)

        where 

            k = 0.55 for soft copper/brass
            k = 0.64 for half-hard copper/brass, soft steel, aluminum
            k = 0.71 for hard copper, cold-rolled steel, spring steel

        It is based on experimental work by Westinghouse for simple bench work with tolerances of
        about 1/2 mm.  For modern manufacturing methods with powered machinery and high volume
        work, you'll want to consult more up-to-date methods on the web.
    
        '''.rstrip()))
        exit(0)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] t L r [θ]
          Calculate the needed length L' of stock to make a bend in sheet metal of thickness t.
          The angle θ is from the flat form and r is the inside radius of the bend.  θ must be in
          degrees and is 90° if omitted.  L is the finished dimension.  L, r, and t are assumed to
          have the same physical units.  The material is assumed to be half-hard brass/copper, soft
          steel, or aluminum.  The forming is done at the bench with hand tools.  Working
          tolerances are about half a mm (0.015 inches or 1/64th of an inch).
        Example:
            I want a 90° bracket from 1/8 inch thick aluminum with 1 inch legs on each side.  The
            bend radius should be 1/8 inch.  How long should the starting stock piece be cut to?
            Arguments are L = 2, t = 1/8, r = 1/8 (the program's input can evaluate expressions),
            and we can omit θ because it defaults to 90°.

            The formula from MH is BA = 0.64*t + 1.57*r = 0.64*(1/8) + 1.57*(1/8) = 0.28.  This
            bend allowance should be added to the finished length of the part, which is 2 inches.
            Thus, we cut a piece 2.28 inches long.  I mark a line at 1.14 inches from the end and
            make the 90° bend from this point.
        Options:
            -1      Material is soft brass or copper
            -2      Material is bronze, hard copper, cold-rolled steel or spring steel
            -d n    Number of figures in answer [{d["-d"]}]
            -h      Print a manpage
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["k"] = 0.64       # Constant for half-hard copper/brass, soft steel, aluminum
        d["-1"] = False     # Soft brass or copper
        d["-2"] = False     # Bronze, hard copper, cold-rolled steel or spring steel
        d["-d"] = 3         # Number of significant digits
        try:
            opts, args = getopt.getopt(sys.argv[1:], "12d:h") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("12"):
                d[o] = not d[o]
            elif o == "-d":
                try:
                    d[o] = int(a)
                    if not (1 <= d[o] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o == "-h":
                Manpage()
        GetColors()
        g.W, g.L = GetScreen()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = False
        if len(args) not in (3, 4):
            Usage()
        if d["-1"]:
            if d["-2"]:
                Error("Can't set both -1 and -2")
            d["k"] = 0.55
        elif d["-2"]:
            d["k"] = 0.71
        return args
if 1:   # Core functionality
    def Westinghouse(t, L, r, θ):
        k = d["k"]
        BA = k*t + radians(θ)*r
        if d["-1"]:
            print(f"Bending soft copper or brass sheet")
        elif d["-2"]:
            print(f"Bending hard copper, cold-rolled steel, or spring steel sheet")
        else:
            print(f"Bending half-hard copper/brass, soft steel, or aluminum sheet")
        i = " "*2
        print(f"{i}t  = sheet metal thickness       {t}")
        print(f"{i}L  = finished length             {L}")
        print(f"{i}r  = inside bend radius          {r}")
        print(f"{i}θ  = bend angle                  {θ}° = {radians(θ)} radians")
        print(f"{i}BA = bend allowance              {BA}")
        print(f"{i}L' = cut to length = L + BA      {L + BA}")
    
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    # Get parameters
    t = flt(eval(args[0]))
    if t < 0:
        Error("t must be >= 0")
    L = flt(eval(args[1]))
    if L < 0:
        Error("L must be >= 0")
    r = flt(eval(args[2]))
    if r < 0:
        Error("r must be >= 0")
    θ = flt(eval(args[3])) if len(args) == 4 else flt(90)
    if not (0 <= θ <= 180):
        Error("θ must be >= 0° and <= 180°")
    Westinghouse(t, L, r, θ)
