'''
Print out estimates of shear, compressive, and tensile strengths of
metal rods.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2016 Don Peterson #∞copyright∞#
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
if 1:   # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    import color as color
    from wrap import dedent
    from f import flt, pi
    from u import u, ParseUnit
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    # Metal ultimate strengths from Machinery's Handbook, 19th
    # ed., page 444.  Ranges are given.
    f = flt
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
        ("Steel, low carbon 1025", 
            (f(60), f(103)), 
            (f(60), f(103)), 
            (f(45), f(77.25)), 
            (f(40), f(90)),
            1000*f(30),
            0.38,
        ),
        ("Steel, medium carbon 1045", 
            (f(80), f(182)), 
            (f(80), f(182)), 
            (f(60), f(136.5)), 
            (f(50), f(162)),
            1000*f(30),
            0.38,
        ),
        ("Steel, high carbon 1095", 
            (f(90), f(213)), 
            (f(90), f(213)), 
            (f(67.5), f(160)), 
            (f(20), f(150)),
            1000*f(30),
            0.39,
        ),
        ("Steel, structural (common)", 
            (f(60), f(75)), 
            (f(60), f(75)), 
            (f(45), f(56.25)), 
            (f(33), f(33)),
            1000*f(29),
            0.41,
        ),
        ("Steel, 4130 alloy", 
            (f(81), f(179)), 
            (f(81), f(179)), 
            (f(60.75), f(134.25)), 
            (f(46), f(161)),
            1000*f(30),
            0.38,
        ),
        ("Steel, 52100 alloy", 
            (f(100), f(238)), 
            (f(100), f(238)), 
            (f(75), f(178.5)), 
            (f(81), f(228)),
            1000*f(30),
            0.38,
        ),
        ("Steel, 302 stainless", 
            (f(85), f(125)), 
            (f(85), f(125)), 
            # Following from https://www.makeitfrom.com/material-properties/AISI-302-S30200-Stainless-Steel
            # which gave 400 to 830 MPa
            (f(58), f(120)),
            (f(35), f(95)),
            1000*f(28),
            0.45,
        ),
        ("Aluminum alloy, sand cast", 
            (f(19), f(35)), 
            # I have approximated the compressive strength as equal to 3/4
            # of the tensile strength
            (f(19*3/4), f(35*3/4)),
            (f(14), f(26)),
            (f(8), f(25)),
            1000*f(10.3),
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
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} diameter [length_unit]
      Prints a table of ultimate or maximum design strengths for metal rods.
      The diameter units default to inches.  The output forces are in pounds;
      use the -o option to change.  diameter can be an expression; the local
      math library's symbols are in scope.
    Example
      How much shear load in lbf can I put on a 1/4-20 thread in low carbon
      steel?  Use a factor of safety of 5.  
      
      Run the script with the -t option to find that the UNC minor diameter for
      a 1/4-20 thread is 0.188 inches.  Then run the script with the arguments
      of '-s 5 0.188'.  The maximum load in shear is 250-430 pounds force.
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
    d["-d"] = 2         # Number of significant digits
    d["-o"] = "lbf"     # Output units
    d["-s"] = None      # Factor of safety
    d["-p"] = 0         # Number of sides in regular polygon
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
                msg = ("-d option's argument must be an integer between "
                       "1 and 15")
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
                msg = ("-p option's argument must be an integer > 3")
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
            PrintThreadData(d)
            exit(0)
    if len(args) < 1:
        Usage(d)
    flt(0).n = d["-d"]
    flt(0).rtz = True
    flt(0).rtdp = True
    return args
def PrintThreadData():
    'Print a table of the minor diameters of commonly-used threads'
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
    'Compute the cross-sectional area of the shape'
    if d["-p"]:     # Area of a regular polygon
        return d["-p"]*dia**2/4*tan(pi/d["-p"])
    else:           # Area of a circle
        return pi/4*dia**2
def PrintReport(dia):
    '''dia is a flt gotten from the diameter expression and optional units on the
    command line.  It will be a flt in units of m.
    '''
    # Convert diameter to inches
    dia /= u("inches")
    print(f"Diameter = {dia} inches = {dia*25.4} mm")
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
    print(f"Area = {A} in2 = {A/u('mm2')} mm2")
    # Force data
    sp = 15
    indent = " "*35
    f, fos = d["-o"], d["-s"]
    n = 30  # Approximate width of columns to get centering
    if fos is not None:
        color.fg(color.lgreen)
        print("  Factor of safety =", fos)
        color.normal()
        s = "Maximum load in " + f
        print(" "*40, "{:^{}}".format(s, n))
    else:
        s = "Breaking load in " + f
        print(" "*40, "{:^{}}".format(s, n))
        fos = 1
    print(indent, "Shear       Compression       Tension")
    NA = "--"
    for item in materials:
        name = item[0]
        uts_low, uts_high = [1000*i for i in item[1]]   # Ultimate tensile strength range
        ucs_low, ucs_high = [1000*i for i in item[2]]   # Ultimate compr. str.
        uss_low, uss_high = [1000*i for i in item[3]]   # Ultimate shear str.
        yp_low, yp_high = [1000*i for i in item[4]]     # Yield point (0.2% offset)
        if item[5] is not None and item[6] is not None:
            E_tension = item[5]                             # Modulus of elasticity
            E_shear = item[6]*E_tension     # Shear modulus
        # Shear
        if uss_low is not None:
            f = uss_low*A/fos
            sh = str(f/u(d["-o"])) + "-"
            f = uss_high*A/fos
            sh += str(f/u(d["-o"]))
        else:
            sh = NA
        # Compression
        if ucs_low is not None:
            f = ucs_low*A/fos
            comp = str(f/u(d["-o"])) + "-"
            f = ucs_high*A/fos
            comp += str(f/u(d["-o"]))
        else:
            comp = NA
        # Tension
        f = uts_low*A/fos
        tens = str(f/u(d["-o"])) + "-"
        f = uts_high*A/fos
        tens += str(f/u(d["-o"]))
        # Print results
        if name == "Steel, structural (common)":
            color.fg(color.lred)
        print(f"{name:30s} {sh:^{sp}s} {comp:^{sp}s} {tens:^{sp}s}")
        color.normal()
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine()
    dia = eval(args[0], globals())
    dia_units = args[1] if len(args) > 1 else "inches"
    dia = flt(dia)*u(dia_units)  # Converts to m
    PrintReport(dia)
