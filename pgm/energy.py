"""
Script to help with estimating daily food energy needs.
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
        # Estimate daily food energy need.
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import deque
        from pathlib import Path as P
        import getopt
        import os
        import re
        import sys
    if 1:  # Custom imports
        from f import flt
        from wrap import dedent
        from color import t
        from lwtest import Assert
        from roundoff import TemplateRound

        if 0:
            import debug

            debug.SetDebugger()
    if 1:  # Global variables

        class G:
            pass

        g = G()
        g.dbg = False
        ii = isinstance
if 1:  # Utility

    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""

    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
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
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] mass_kg height_m age_years 
          If you enter the indicated data, the food energy in kcal/day for a person with those
          statistics is estimated.  You can cuddle 'lb' after mass_kg and it will be interpreted
          as pounds and converted to kg.  Similarly, 'in' after height_m will be inches and
          converted to m.
        Options:
            -d n    Number of digits in figures [{d["-d"]}]
            -h      Print a manpage
        """)
        )
        exit(status)

    def ParseCommandLine(d):
        d["-d"] = 2  # Number of significant digits
        if len(sys.argv) == 1:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o == "-h":
                Manpage()
        flt(0).N = d["-d"]
        if len(args) != 3:
            Usage()
        return args

    def Manpage():
        print(
            dedent(f"""
        The model came from https://en.wikipedia.org/wiki/Institute_of_Medicine_Equation and was
        published in 2002.  A number of other equations can be found at
        https://en.wikipedia.org/wiki/Basal_metabolic_rate.

        Activity levels are:
            Sedentary               Light physical activity associated with independent living
            Moderately active       About 1/2 hour of vigorous exercise per day
            Active                  About 1 hour of vigorous exercise per day
            Very active             Physically active for several hours per day

        It's up to you to decide if this or any model predicts meaningful numbers.  The
        Harris-Benedict formula from the early 1900's with revised information from 1990 seems to
        predict energy needs for me about 10% lower than this IoM formula.  In truth, either is
        probably appropriate for an estimate to guide your dieting choices.  If you're wise,
        you'll include your doctor in the decisions about your tactics.

        I managed my weight loss over a 12 week period and I used the mean of the predictions of
        the IoM equation and the Harris-Benedict equation, primarily because it was a nice round
        number easy to remember.  My mental target was to aim for 50% to 75% of this daily energy
        need.  Based on the weight loss over those three months and assuming 3500 kcal per pound
        of fat, I actually averaged at 65% of the predicted energy need.  My doc was pleased with
        the results and agreed with my longer term weight and BMI goals.  He felt it was positive
        enough that at the next appointment if the lab work shows good adherence, he plans to take
        me off two of the medications I use.  That's good news and I'm also using it as motivation
        to stick with the weight management.
        """)
        )
        exit(0)


if 1:  # Core functionality

    def Condition(energy, round_to=100):
        "Convert to integer and round to round_to, return as string"
        e = TemplateRound(int(energy), round_to)
        return str(e)

    def E_m(mass, height, age, p):
        m_terms = (662, -9.53 * age, 15.91 * mass * p, 539.6 * height)
        return str(sum(m_terms))

    def E_f(mass, height, age, p):
        m_terms = (354, -6.91 * age, 9.36 * mass * p, 726 * height)
        return str(sum(m_terms))

    def GetMass(mass):
        if mass.endswith("lb"):
            mass = flt(mass[:-2]) * 0.45359237
        else:
            mass = flt(mass)
        return mass

    def GetHeight(height):
        if height.endswith("in"):
            height = flt(height[:-2]) * 0.0254
        else:
            height = flt(height)
        return height

    def CheckParameters(mass, height, age):
        if not (30 <= mass <= 140):
            Error(f"Mass must be between 30 and 140 kg")
        if not (1.2 <= height <= 2.1):
            Error(f"Height must be between 1.2 and 2.1 m")
        if not (18 <= age <= 100):
            Error(f"Age must be between 18 and 100 years")


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    # Get arguments
    mass = GetMass(args[0])
    height = GetHeight(args[1])
    age = flt(args[2])
    CheckParameters(mass, height, age)
    # Calculate the energy need in kcal
    # Activity level mappings (key is activity level)
    A = {1: "Sedentary", 2: "Moderately active", 3: "Active", 4: "Very active"}
    A_m = {1: 1, 2: 1.11, 3: 1.25, 4: 1.48}
    A_f = {1: 1, 2: 1.12, 3: 1.27, 4: 1.45}
    # Report
    with mass:
        mass.N = d["-d"] + 1
        print(f"Mass     = {mass} kg = {mass * 2.2046226} lb")
        print(f"Height   = {height} m = {height * 39.370079} inches")
        print(f"Age      = {age} years")
    w1, w2 = 25, 8
    print(f"\n{' ' * 25}Energy need in kcal")
    print(f"{'Activity level':^{w1}s} {'Male':^{w2}s} {'Female':^{w2}s}")
    print(f"{'-' * w1:{w1}s} {'-' * w2:{w2}s} {'-' * w2:{w2}s}")
    with mass:
        mass.N = d["-d"]
        for p in (1, 2, 3, 4):
            print(
                f"{'  ' + A[p]:{w1}s} {E_m(mass, height, age, p):^{w2}s} "
                f"{E_f(mass, height, age, p):^{w2}s}"
            )
