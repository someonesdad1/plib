"""
Calculate diameter needed to get a perfect knurl.

    Adapted from Marv Klotz's
    http://www.myvirtualnetwork.com/mklotz/fckeditor/UserFiles/File/knurl.zip.
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
        from math import pi, floor, gcd
        import getopt
        import sys
        from collections import defaultdict
    if 1:  # Custom imports
        from color import t
        from dpprint import PP

        pp = PP()  # Screen width aware form of pprint.pprint
        from get import GetLines
        from wrap import dedent
        from wsl import wsl  # wsl is True when running under WSL Linux
        from u import ParseUnit
        from f import flt
        from color import t
        from columnize import Columnize
        # from columnize import Columnize
    if 1:  # Global variables

        class G:
            # Storage for global variables as attributes
            pass

        g = G()
        g.dbg = False
        ii = isinstance
        # Knurl wheel characteristics
        knurl_wheel_diameter = None
        knurl_wheel_units = None
        number_of_teeth = None
        knurls = {
            # Knurl name:  (diameter, number of teeth)
            # Make sure to include units in diameter, as those units will be used
            # in a printout.
            1: ("3/4 inch", 40),  # Enco holder's default wheels
            2: ("1 inch", 160),  # 0.5 mm pitch banggood
            3: ("1 inch", 80),  # 1.0 mm pitch banggood
            4: ("1 inch", 40),  # 2.0 mm pitch banggood
        }
if 1:  # Utility

    def Usage(d):
        print(
            dedent(
                f"""
        Usage:  knurl [options] dia1 [dia2...]
          Calculate the correct diameter to turn command line diameters in inches to get an integer
          number of knurls around the circumference.  The supported knurls are:
                n           Diameter        Number of teeth
               ---        ------------      ---------------
        """.rstrip()
            )
        )
        for i in knurls:
            D, n = knurls[i]
            print(f"{i:>9d}        {D:^14s}          {n:^5d}")
        print(
            dedent(
                f"""
        Options:
          -k n      Choose which knurl wheels to use.  Default is {d["-k"]}.
          -d n      Find the next smaller diameter for the 1 inch knurls as these require the same
                    diameter as the nominal diameter.  However, sometimes you want the knurling pattern
                    to be just under the nominal diameter.  This is done by subtracting n from the number
                    of teeth.
          -m        Input diameters are in mm
          -T        Print a decimal table from 0.2 to 2 inches.
          -t        Print a fractional table from 0.2 to 2 inches.
        """.rstrip()
            )
        )
        exit(1)

    def ParseCommandLine(d):
        global knurl_wheel_diameter, knurl_wheel_units, number_of_teeth
        # Options
        d["-k"] = 1  # Which set of knurls to use
        d["-d"] = 0  # Decrement number of teeth
        d["-m"] = False  # Input diameters are mm
        d["-t"] = False  # Fractional table
        d["-T"] = False  # Decimal table
        # Set up knurl wheel size
        dia, nteeth = knurls[d["-k"]]
        knurl_wheel_diameter, knurl_wheel_units = ParseUnit(dia, allow_expr=True)
        number_of_teeth = int(nteeth)
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:hk:mtT")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in "mtT":
                d[o] = not d[o]
            elif o in ("-d",):
                d["-d"] = int(a)
                assert int(a) >= 0
            elif o in ("-k",):
                d["-k"] = int(a)
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        if not args and not d["-t"] and not d["-T"]:
            Usage(d)
        dia, nteeth = knurls[d["-k"]]
        knurl_wheel_diameter, knurl_wheel_units = ParseUnit(dia, allow_expr=True)
        knurl_wheel_diameter = eval(knurl_wheel_diameter)
        number_of_teeth = int(nteeth) - d["-d"]
        return args


if 1:  # Core functionality

    def FractionInLowestTerms(numerator, denominator):
        # Reduce to lowest terms
        divisor = gcd(numerator, denominator)
        return numerator // divisor, denominator // divisor

    def ImproperFraction(numerator, denominator):
        # Return fraction as an improper fraction string.
        s = ""
        ip = numerator // denominator
        if ip != 0:
            s = str(ip)
        fp = numerator % denominator
        if fp != 0:
            num, den = FractionInLowestTerms(fp, denominator)
            t = str(num) + "/" + str(den)
            if ip == 0:
                s += t
            else:
                s += "-" + t
        return s

    def FractionalTable():
        print("Perfect knurling diameter for common fractional sizes.")
        print(
            "(For %g inch diameter knurl with %d teeth)"
            % (knurl_wheel_diameter, number_of_teeth + d["-d"])
        )
        if d["-d"]:
            print("  -d option was {}".format(d["-d"]))
        print()
        print("  Size,      Perfect")
        print("  inches    Diameter")
        print("  ------    --------")
        for sixteenth in list(range(4, 17)) + list(range(18, 41, 2)):
            diameter = sixteenth / 16
            print(
                "  {:^6s}      {:.3f}".format(
                    ImproperFraction(sixteenth, 16), GetPerfectDiameter(diameter)
                )
            )

    def DecimalTable():
        """For 200 to 2000 mil diameters, group by requisite knurling
        diameter.
        """
        di = defaultdict(list)
        for d in range(200, 2001):
            D = int(GetPerfectDiameter(d / 1000) * 1000)
            di[D].append(d)
        k = di.keys()
        # Group by size
        s = []
        for i in sorted(k):
            s.append((min(di[i]), max(di[i]), i))
        s.sort()
        # Put into string form
        t, fmt = [], "%5.3f-%5.3f %5.3f"
        for i in s:
            t.append(fmt % tuple([j / 1000 for j in i]))
        for i in Columnize(t):
            print(i)

    def GetPerfectDiameter(nominal_diameter):
        """The method is to find the diameter just under nominal_diameter that has an integer
        number of knurl wheel pitches for the circumference.

        Numerical example:  (3/4 inch knurl wheel, 40 teeth)

            Calculate pitch of knurl wheel:  The circumference is pi*3/4 = 2.3562.  Dividing by 40
            teeth gives the pitch = 0.058905.

            We want the diameter just under nominal_diameter that has an integral number of these
            pitches.

            Calculate the number of pitches with the nominal_diameter:  pi*nominal_diameter/pitch
            is 3.14159*1.3/0.058905 = 69.333.

            We thus must turn the diameter down enough so it has a circumference of 69 pitches.
            This circumference is 69*0.058905 = 4.0644 inches.  Divide this by pi to get the
            required diameter of 1.2938 inches.
        """
        pitch = pi * knurl_wheel_diameter / (number_of_teeth - d["-d"])
        integer_num_crests = int(floor(pi * nominal_diameter / pitch))
        required_circumference = integer_num_crests * pitch
        return required_circumference / pi


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    dia, teeth = knurls[d["-k"]]
    msg = f"Workpiece diameter for perfect knurling (knurl {dia} diameter, {teeth} teeth):"
    x = flt(0)
    x.N = 4
    if d["-t"]:
        FractionalTable()
    elif d["-T"]:
        DecimalTable()
    else:
        print(msg)
        for dia in args:
            try:
                nominal_diameter = flt(dia)
                if d["-m"]:
                    nominal_diameter /= 25.4  # Convert mm to inches
            except ValueError:
                print(f"{dia!r} is not a valid diameter")
                continue
            if d["-m"]:
                print(f"  Diameter of workpiece = {nominal_diameter} inches = {dia} mm")
            else:
                print(
                    f"  Diameter of workpiece = {dia} inches = {nominal_diameter * 25.4} mm"
                )
            D = GetPerfectDiameter(nominal_diameter)
            t.print(
                f"    Workpiece diameter for perfect knurling = {t('ornl')}{D:.3f} inches "
                f"= {t('royl')}{D * 25.4:.2f} mm"
            )
