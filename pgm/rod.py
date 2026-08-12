'''
Print out estimates of shear, compressive, and tensile strengths of
metal rods.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Estimate strengths of metal rods
        ##∞what∞#
        ##∞test∞# #∞test∞#
        pass
    if 1:  # Imports
        import getopt
        import os
        import sys
    if 1:  # Custom imports
        import trm
        t = trm.TrmDP()
        from wrap import dedent
        from f import flt, pi
        from u import u, ParseUnit
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        if 1:   # Old format
            # Metal ultimate strengths from Machinery's Handbook, 19th
            # ed., page 444.  Ranges are given.
            # kpsi = 6.9 MPa
            # Mpsi = 6.9 GPa
            materials = (
                # Fields are:
                #   0  Material name & state
                #   1  Ultimate tensile strength in kpsi
                #   2  Ultimate compressive strength in kpsi
                #   3  Ultimate shear strength in kpsi
                #   4  Yield point kpsi (0.2% offset)
                #   5  E = Modulus of elasticity in tension, Mpsi
                #   6  Modulus of elasticity in shear in terms of E
                # None means no number available.
                (
                    "Steel, low carbon 1025",
                    (flt(60), flt(103)),
                    (flt(60), flt(103)),
                    (flt(45), flt(77.25)),
                    (flt(40), flt(90)),
                    1000 * flt(30),
                    0.38,
                ),
                (
                    "Steel, medium carbon 1045",
                    (flt(80), flt(182)),
                    (flt(80), flt(182)),
                    (flt(60), flt(136.5)),
                    (flt(50), flt(162)),
                    1000 * flt(30),
                    0.38,
                ),
                (
                    "Steel, high carbon 1095",
                    (flt(90), flt(213)),
                    (flt(90), flt(213)),
                    (flt(67.5), flt(160)),
                    (flt(20), flt(150)),
                    1000 * flt(30),
                    0.39,
                ),
                (
                    "Steel, structural (common)",
                    (flt(60), flt(75)),
                    (flt(60), flt(75)),
                    (flt(45), flt(56.25)),
                    (flt(33), flt(33)),
                    1000 * flt(29),
                    0.41,
                ),
                (
                    "Steel, 4130 alloy",
                    (flt(81), flt(179)),
                    (flt(81), flt(179)),
                    (flt(60.75), flt(134.25)),
                    (flt(46), flt(161)),
                    1000 * flt(30),
                    0.38,
                ),
                (
                    "Steel, 52100 alloy",
                    (flt(100), flt(238)),
                    (flt(100), flt(238)),
                    (flt(75), flt(178.5)),
                    (flt(81), flt(228)),
                    1000 * flt(30),
                    0.38,
                ),
                (
                    "Steel, 302 stainless",
                    (flt(85), flt(125)),
                    (flt(85), flt(125)),
                    # Following from https://www.makeitfrom.com/material-properties/AISI-302-S30200-Stainless-Steel
                    # which gave 400 to 830 MPa
                    (flt(58), flt(120)),
                    (flt(35), flt(95)),
                    1000 * flt(28),
                    0.45,
                ),
                (
                    "Aluminum alloy, sand cast",
                    (flt(19), flt(35)),
                    # I have approximated the compressive strength as equal to 3/4
                    # of the tensile strength
                    (flt(19*3/4), flt(35*3/4)),
                    (flt(14), flt(26)),
                    (flt(8), flt(25)),
                    1000 * flt(10.3),
                    None,
                ),
                # Old data from American Machinist's handbook, 1945
                #    ("Aluminum, cast", 12, 12, 15),
                #    ("Brass, cast", 36, 30, 30),
                #    ("Bronze, manganese", None, 120, 70),
                #    ("Copper, cast", 25, 40, 24),
                #    ("Copper, rolled", 28, 60, 37),
                #    ("Copper, wire, annealed", None, None, 36),
                #    ("Iron, cast", 25, 90, 22),
                #    ("Lead", 4, None, 3),
                #    ("Steel, mild", 55, 65, 70),
                #    ("Steel, tempered tool steel", 190, None, 250),
                #    ("Steel wire, soft", None, None, 80),
                #    ("Steel, piano wire", None, None, 300),
                #    ("Zinc, sand cast", 14, 20, 9),
                # From https://www.unipunch.com/support/charts/material-specifications/
                # Shear strengths in kpsi
                #   Steel, low carbon hot rolled            50
                #   Steel, low carbon cold rolled           40
                #   Steel, 1074 spring temper              200
                #   Steel, stainless 302/3/4 annealed       75
                #   Aluminum, 2024-T3                       41
                #   Aluminum, 6061-T6                       30
                #   Cu, electrolytic, 1/2 hard              26
                #   Cu, 220 bronze, 1/2 hard                35
                #   Cu, 230 red brass, 1/4 hard             35
                #   Cu, 260 cartridge brass, 1/2 hard       40
                #   Cu, 342 high lead, 1/2 hard             40
                #   Cu, 672 Mn bronze                       42
            )
        else:   # New format (easier to read)
            # UTS = ultimate tensile strength, UCS = ultimate compressive strength
            # USS = ultimate shear strength, YP = yield point (0.2% offset)
            # MOE = modulus of elasticity
            # name; UTS kpsi, UCS kpsi, USS kpsi, YP kpsi, MOE Mpsi, MOE shear (fraction of E)
            names = {
                0: "Steel, low carbon 1025",
                1: "Steel, medium carbon 1045",
                2: "Steel, high carbon 1095",
                3: "Steel, structural (common)",
                4: "Steel, 4130 alloy",
                5: "Steel, 52100 alloy",
                6: "Steel, 302 stainless",
                7: "Aluminum alloy, sand cast",
            }
            materials = '''
                0, 60 103,  60 103,         45 77.25,      40 90,   3e4,    0.38
                1, 80 182,  80 182,         60 136.5,      50 162,  3e4,    0.38
                2, 90 213,  90 213,         67.5 160,      20 150,  3e4,    0.39
                3, 60 75,   60 75,          45 56.25,      33 33,   2.9e4,  0.41
                4, 81 179,  81 179,         60.75 134.25,  46 161,  3e4,    0.38
                5, 100 238, 100 238,        75 178.5,      81 228,  3e4,    0.38
                6, 85 125,  85 125,         58 120,        35 95,   2.8e4,  0.45
                7, 19 35,   14.25 26.25,    14 26,         8 25,    1.03e4, None'''[1:]
            # Construct the data from the string information
            materials = []
            for line in _materials.split("\n"):
                o = []
                for i, item in enumerate(line.split(",")):
                    item = item.strip()
                    if not i:
                        o.append(names[int(item)])
                    else:
                        if " " in item:
                            o.append([flt(i) for i in item.split()])
                        else:
                            try:
                                o.append(flt(item))
                            except Exception:
                                o.append(None)
                print(o)
                materials.append(o)
        if 1:   # Factors of safety
            # Numbers from
            # http://www.engineersedge.com/analysis/factor-of-safety-review.htm
            safety = '''
            Approximate factors of safety:
                3       Ultimate strength of material is known exactly, steady load.
                4       Same, variable loads.
                5-6     Whole (or nearly whole) load to be applied and removed.
                6       Reversed in direction (tension to compression and back).
                10      Subject to shock loads.
                >10     High cost/risk of failure.
            '''
if 1:  # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} diameter [length_unit]
          Prints a table of ultimate or maximum design strengths for metal rods.  The
          diameter units default to inches.  The output forces are in lbf; use the -o
          option to change.  diameter can be an expression; the local math library's
          symbols are in scope.  The ranges come from the ultimate strength ranges given
          in Machinery's Handbook, 19th ed., page 444-445.
        Example
          How much shear load in lbf can I put on a 1/4-20 thread in low carbon
          steel?  Use a factor of safety of 5.  
          
          Run the script with the -t option to find that the UNC minor diameter for a
          1/4-20 thread is 0.188 inches.  Then run the script with the arguments of '-s
          5 0.188'.  The maximum load in shear is 56-96 lbf.  The breaking load in shear
          is 280-480 lbf.
        Options
          -d n  Round answers to n significant figures [{d["-d"]}]
          -o u  Set the force output units [{d["-o"]}]
          -p n  The cross section of the rod is a regular polygon with the indicated
                number of sides.  The diameter is the inscribed circle diameter.  A
                round rod is the default.
          -s sf Use a specified factor of safety.  The default is None, which means
                the printed numbers are estimates of the forces where things break.
          -t    Print root diameters of common UN threads
        {safety}'''))
        exit(status)
    def ParseCommandLine():
        d["-d"] = 2  # Number of significant digits
        d["-o"] = "lbf"  # Output units
        d["-s"] = None  # Factor of safety
        d["-p"] = 0  # Number of sides in regular polygon
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "d:o:p:s:t")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = "-d option's argument must be an integer between 1 and 15"
                    Error(msg)
            elif o in ("-o",):
                d["-o"] = a
                try:
                    u(a)
                except NameError:
                    Error("'{}' is an unrecognized force unit".format(a))
            elif o in ("-p",):
                try:
                    d["-p"] = int(a)
                    if d["-p"] < 3:
                        raise ValueError()
                except ValueError:
                    msg = "-p option's argument must be an integer > 3"
                    Error(msg)
            elif o in ("-s",):
                try:
                    d["-s"] = float(a)
                    if int(a) == d["-s"]:
                        d["-s"] = int(a)
                    if d["-s"] < 1:
                        raise ValueError()
                except ValueError:
                    Error("-s option's argument must be >= 1")
            elif o in ("-t",):
                PrintThreadData()
                exit(0)
        if len(args) < 1:
            Usage(d)
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = True
        return args
if 1:  # Core functionality
    def PrintThreadData():
        "Print a table of the minor diameters of commonly-used threads"
        print(dedent('''
        Commonly used UN thread root diameters in inches
           Size        UNC     UNF
            4         0.080   0.086
            6         0.099   0.106
            8         0.125   0.129
            10        0.138   0.151
            1/4       0.188   0.205
            5/16      0.243   0.260
            3/8       0.297   0.324
            7/16      0.348   0.375
            1/2       0.404   0.437
            5/8       0.512   0.555
            3/4       0.625   0.672
          '''))
        exit(0)
    def Area(dia):
        "Compute the cross-sectional area of the shape"
        if d["-p"]:  # Area of a regular polygon
            return d["-p"] * dia**2 / 4 * tan(pi / d["-p"])
        else:  # Area of a circle
            return pi / 4 * dia**2
    def PrintReport(dia):
        '''dia is a flt gotten from the diameter expression and optional units on the
        command line.  It will be a flt in units of m.
        '''
        # Convert diameter to inches
        dia /= u("inches")
        print(f"Diameter = {dia} inches = {dia * 25.4} mm")
        # Shape
        n = d["-p"]
        print("Shape =", end=" ")
        if n:
            shapes = {
                3: "triangle",
                4: "square",
                5: "pentagon",
                6: "hexagon",
                8: "octagon",
            }
            if n in shapes:
                print(shapes[n])
            else:
                print(f"polygon with {n} sides")
        else:
            print("round")
        # Area
        A = Area(dia)
        print(f"Area = {A} in² = {A / u('mm2')} mm²")
        # Number of digits
        print(f"Number of digits = {d['-d']}")
        # Force data
        sp = 15
        indent = " " * 35
        f, fos = d["-o"], d["-s"]
        n = 30  # Approximate width of columns to get centering
        if fos is not None:
            t.print(f"  {t('orn')}Factor of safety =", fos)
            s = "Maximum load in " + f
            print(" " * 40, "{:^{}}".format(s, n))
        else:
            s = "Breaking load in " + f
            print(" " * 40, "{:^{}}".format(s, n))
            fos = 1
        print(indent, "Shear       Compression       Tension")
        NA = "--"
        for item in materials:
            name = item[0]
            uts_low, uts_high = [
                1000 * i for i in item[1]
            ]  # Ultimate tensile strength range
            ucs_low, ucs_high = [1000 * i for i in item[2]]  # Ultimate compr. str.
            uss_low, uss_high = [1000 * i for i in item[3]]  # Ultimate shear str.
            yp_low, yp_high = [1000 * i for i in item[4]]  # Yield point (0.2% offset)
            if item[5] is not None and item[6] is not None:
                E_tension = item[5]  # Modulus of elasticity
                E_shear = item[6] * E_tension  # Shear modulus
            # Shear
            if uss_low is not None:
                f = uss_low * A / fos
                sh = str(f / u(d["-o"])) + "-"
                f = uss_high * A / fos
                sh += str(f / u(d["-o"]))
            else:
                sh = NA
            # Compression
            if ucs_low is not None:
                f = ucs_low * A / fos
                comp = str(f / u(d["-o"])) + "-"
                f = ucs_high * A / fos
                comp += str(f / u(d["-o"]))
            else:
                comp = NA
            # Tension
            f = uts_low * A / fos
            tens = str(f / u(d["-o"])) + "-"
            f = uts_high * A / fos
            tens += str(f / u(d["-o"]))
            # Print results
            c = t("ornl") if name == "Steel, structural (common)" else ""
            t.print(f"{c}{name:30s} {sh:^{sp}s} {comp:^{sp}s} {tens:^{sp}s}")
        print("\n1 lbf = 4.45 N")
if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine()
    dia = eval(args[0], globals())
    dia_units = args[1] if len(args) > 1 else "inches"
    dia = flt(dia) * u(dia_units)  # Converts to m
    PrintReport(dia)
