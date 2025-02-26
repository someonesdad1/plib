"""
Bend allowance computation for sheet metal
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Program description string
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import subprocess
        import sys
    if 1:  # Custom imports
        from color import t
        from f import flt, radians
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
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
        print(
            dedent(
                f"""
        Bend allowance = X = amount to add to a desired length of sheet metal to get a desired
        finished length L after making a bend.

        Suppose you want to bend a piece of sheet metal to make a right angle bracket with legs 1
        unit long.  If you could make a perfectly sharp bend in very thin metal, you'd start with a
        flat piece of 2 units long and make the bend.  With real materials of nonzero thickness,
        the final bend will have a radius (i.e., it can't be a geometrically sharp bend) and you'll
        need to add extra material to the calculated length to get the desired finished length
        after bending.  This extra length is due to the arc length of the material in the nonzero
        radius bend.  Because of non-elastic distortions in the material when bending, there is no
        exact formula to calculate the needed allowance.

        But we can approximate it.  Consider this right angle bracket with infinitely thin metal.
        If the resulting bend has a radius of r, then the needed metal length is the length of the
        two legs plus the length of a quarter of a circle's circumference, which will be the bend
        radius r times the bend angle θ in radians.  Thus, the bend allowance is X = r*θ.

        If the sheet metal has a thickness of t and you make a sketch of the bend with the inside
        radius r, you'll see you need to add a small correction dr to the radius to calculate the
        arc length for the bend allowance at about the average radius of the metal.  Geometrically,
        dr should be half of the sheet's thickness.  We thus get the approximation

            X = (r + dr)*θ          dr ≅ t/2

        The dr term's effect on the bend allowance is the arc length difference between the inside
        of the bend and the arc in the middle of the metal.  I call this X the geometrical bend
        allowance and it's not significantly different from the empirical formulas.

        For a numerical example, suppose we're bending 1/8 inch thick sheet in a right angle and
        the resulting inside bend radius is 1/8 inch.  We'll choose dr = t/2, so the geometrical
        bend allowance is (1/8 + (1/8)/2)*1.57 = (3/16)*1.57 = 0.29 inches.

        You can run the script with arguments '1/8 2 1/8' and you'll get

            Bending half-hard copper/brass, soft steel, or aluminum sheet
              t  = sheet metal thickness       0.125
              L  = finished length             2
              r  = inside bend radius          0.125
              θ  = bend angle                  90° = 1.57 radians
              X  = bend allowance              0.276 (geometrical 0.295)
              L' = cut to length = L + X       2.28

        The empirical formula used in this script came from Machinery's Handbook:

            c*t + θ*r      (θ in radians)

        where c is a constant:

            c = 0.55 for soft copper/brass
            c = 0.64 for half-hard copper/brass, soft steel, aluminum
            c = 0.71 for hard copper, cold-rolled steel, spring steel

        Machinery's Handbook's formula is based on experimental work by Westinghouse for bench work
        with tolerances of about 1/2 mm.  I'd estimate this experimental work was done in the
        1930's, as some of the bending allowance material in Machinery's Handbook was in the 1919
        edition.  For modern manufacturing methods with powered machinery, high volumes, and
        significant lead times & tooling costs, you'd want to consult the more detailed empirical
        methods by the experts.  

        For a home shop person like myself, the geometrical approximation works OK and if it's a
        little long, it's not hard to file some material off -- but it's an annoyance if you make
        things too short.  In the above example, if I had used the geometrical bend allowance, I
        would have added 0.30 inches to the material length.  The Machinery's Handbook formula gave
        0.28 inches to add.  The difference is a 50th of an inch.

        A practical approach is to use the above geometrical approximation to the bend allowance,
        fabricate your piece, and see how much it differs from the desired form.  Then correct the
        bend allowance used and you should be able to make a few more parts pretty close to the
        desired dimension.

        A detail is that the bend angle might not be what you see on a drawing of the part to make.
        A designer might want a bracket with an inside angle of 60°:

                  /
                 / 
                /  60°
                -------
    
        For this part, the bend angle is the 180° complement of this angle or 120°, as that's the
        angle you have to bend a flat piece of material to get the inside 60° angle.  If you forget
        this detail, you'll use a too-small θ and the bend allowance will be too small.

        """.rstrip()
            )
        )
        exit(0)

    def Usage(status=1):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] t L r [θ]
          Calculate the needed length L' of stock to make a bend in sheet metal of thickness t.
          The angle θ is the bend angle from the flat form and r is the inside radius of the bend.
          θ must be in degrees and is 90° if omitted.  L is the finished dimension.  L, r, and t
          are assumed to have the same physical units.  The material is assumed to be half-hard
          brass/copper, soft steel, or aluminum.  The forming is done at the bench with hand tools.
          Working tolerances are about half a mm.
        Options:
            -1      Material is soft brass or copper
            -2      Material is bronze, hard copper, cold-rolled steel or spring steel
            -d n    Number of significant figures to use [{d["-d"]}]
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["c"] = 0.64  # Constant for half-hard copper/brass, soft steel, aluminum
        d["-1"] = False  # Soft brass or copper
        d["-2"] = False  # Bronze, hard copper, cold-rolled steel or spring steel
        d["-d"] = 3  # Number of significant digits
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
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Manpage()
        GetColors()
        g.W, g.L = GetScreen()
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = True
        if len(args) not in (3, 4):
            Usage()
        if d["-1"]:
            if d["-2"]:
                Error("Can't set both -1 and -2")
            d["c"] = 0.55
        elif d["-2"]:
            d["c"] = 0.71
        return args


if 1:  # Core functionality

    def Westinghouse(t, L, r, θ):
        c = d["c"]
        X = c * t + radians(θ) * r  # Bend allowance from Machinery's handbook
        X1 = (r + t / 2) * radians(θ)  # Basic bend allowance
        if d["-1"]:
            print(f"Bending soft copper or brass sheet")
        elif d["-2"]:
            print(f"Bending hard copper, cold-rolled steel, or spring steel sheet")
        else:
            print(f"Bending half-hard copper/brass, soft steel, or aluminum sheet")
        i = " " * 2
        print(f"{i}t  = sheet metal thickness       {t}")
        print(f"{i}L  = finished length             {L}")
        print(f"{i}r  = inside bend radius          {r}")
        print(f"{i}θ  = bend angle                  {θ}° = {radians(θ)} radians")
        print(f"{i}X  = bend allowance              {X} (geometrical {X1})")
        print(f"{i}L' = cut to length = L + X       {L + X}")


if __name__ == "__main__":
    d = {}  # Options dictionary
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
