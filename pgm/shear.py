'''
Print out shear strength of various bolts
    For steel, take the ultimate shear strength as 60% of the ultimate tensile
    strength.

    1 kpsi = 6.89 MPa

    Ref 
        http://www.portlandbolt.com/technical/strength-requirements-by-grade/
        https://en.wikipedia.org/wiki/Ultimate_tensile_strength#Typical_tensile_strengths
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2018 Don Peterson #∞copyright∞#
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
    from math import pi
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from f import flt
if 1:   # Global variables
    materials = (
        # Name, yield strength, UTS [both in MPa]
        # From https://en.wikipedia.org/wiki/Ultimate_tensile_strength except
        # for first three, which are from 
        # http://www.portlandbolt.com/technical/strength-requirements-by-grade/
        ("low carbon steel", 248, 414),
        ("grade 5 steel", 634, 827),
        ("grade 8 steel", 896, 1034),
        ("4130 heat treated steel", 951, 1110),
        ("302 cold rolled stainless steel", 520, 860),
        ("6061 aluminum", 241, 300),
        ("brass", 200, 500),
        ("annealed copper", 117, 210),
    )
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] material_number
      Print out a table of shear and tensile strengths for common bolt sizes. 
    Options
      -a    Print abbreviated set of sizes
      -d n  Use n significant figures [{d["-d"]}]
      -m    Print out metric sizes
      -t    Print out a table for each material
    '''))
    # Print materials
    print("Material numbers:")
    for i, item in enumerate(materials):
        m = item[0] 
        s = m[0].upper() + m[1:]
        print(f"  {i + 1:2d}  {s}")
    exit(status)
def ParseCommandLine(d):
    d["-a"] = True      # Abbreviate sizes
    d["-d"] = 2         # Significant figures
    d["-m"] = False     # Metric
    d["-t"] = False     # Print out for each material type
    try:
        opts, args = getopt.getopt(sys.argv[1:], "ad:hmt")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-a", "-m", "-t"):
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
            Usage(status=0)
    if not args:
        Usage()
    x = flt(0)
    x.n = d["-d"]
    x.rtz = x.rtdp = True
    return args
def GetSizes(d):
    sizes, mm2in = [], flt(1/25.4)
    if d["-m"]:
        if d["-a"]:
            sizes += [
                ("2", 2*mm2in),
                ("3", 2*mm2in),
            ]
        sizes += [
            ("4", 2*mm2in),
            ("5", 5*mm2in),
            ("6", 6*mm2in),
            ("8", 8*mm2in),
            ("10", 10*mm2in),
            ("12", 12*mm2in),
        ]
        if d["-a"]:
            sizes += [
                ("14", 14*mm2in),
                ("16", 16*mm2in),
                ("18", 18*mm2in),
                ("20", 20*mm2in),
                ("22", 22*mm2in),
                ("24", 24*mm2in),
            ]
    else:
        if d["-a"]:
            sizes += [
                ("#2 (0.086)", flt(0.086)),
                ("#4 (0.112)", flt(0.112)),
            ]
        sizes += [
            ("#6 (0.138)", flt(0.138)),
            ("#8 (0.164)", flt(0.164)),
            ("#10 (0.190)", flt(0.19)),
            ("1/4", flt(1/4)),
            ("5/16", flt(5/16)),
            ("3/8", flt(3/8)),
            ("7/16", flt(7/16)),
            ("1/2", flt(1/2)),
        ]
        if d["-a"]:
            sizes += [
                ("5/8", flt(5/8)),
                ("3/4", flt(3/4)),
                ("7/8", flt(7/8)),
                ("1", flt(1)),
            ]
    return sizes
def Table(material, d):
    sizes = GetSizes(d)
    name, YS, UTS = material  # YS, UTS in MPa
    YS_kpsi = flt(YS)/6.89
    UTS_kpsi = flt(UTS)/6.89
    if d["-m"]:
        ys = str(YS) + " MPa"
        uts = str(UTS) + " MPa"
    else:
        ys = str(YS_kpsi) + " kpsi"
        uts = str(UTS_kpsi) + " kpsi"
    s = "kN" if d["-m"] else "klbf"
    print(f"Strengths in {s} of bolts made from {name}")
    print(f"  Calculations are for nominal diameter (thread depth ignored)")
    if d["-m"]:
        print("  (1 kN = 0.225 klbf)")
    print(f"  Yield strength = {ys}, UTS = {uts}")
    s = "mm" if d["-m"] else "in"
    print('''
                       Tension               Shear = 0.6*Tension
Size ({})         Yield      Ultimate        Yield      Ultimate
'''[:-1].format(s))
    fmt = " {:14s}  {:^8s}    {:^8s}       {:^8s}    {:^8s}"
    c = 4.44822 if d["-m"] else 1  # Converts lbf to N
    for n, dia_in in sizes:
        A = pi*dia_in**2/4
        Ty = A*YS_kpsi
        Tu = A*UTS_kpsi
        Sy = 0.6*Ty
        Su = 0.6*Tu
        Ty, Tu, Sy, Su = [str(i*c) for i in (Ty, Tu, Sy, Su)]
        print(fmt.format(n, Ty, Tu, Sy, Su))
    if d["-t"]:
        print()
if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    if d["-t"]:
        for material_index in range(len(materials)):
            material = materials[material_index]
            Table(material, d)
    else:
        material_index = int(args[0]) - 1
        try:
            material = materials[material_index]
        except Exception:
            Error("Material number must be between 1 and {}".format(len(materials)))
        Table(material, d)
