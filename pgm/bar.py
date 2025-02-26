"""
Print out mass of bar stock
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # Print out mass of bar stock
    # ∞what∞#
    # ∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from math import pi, sqrt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
    from columnize import Columnize
    from sig import sig
if 1:  # Global variables
    width = 70  # Screen width to print to
    in2mm = 25.4
    spgr = {
        # Metals
        "aluminum": 2.70,
        "brass": 8.50,
        "bronze": 8.78,
        "cast iron": 7.36,
        "chromium": 6.92,
        "cobalt": 8.70,
        "concrete": 2.2,
        "copper": 8.96,
        "gold": 19.3,
        "iron": 7.36,
        "lead": 11.3,
        "magnesium": 1.74,
        "mercury": 13.5,
        "molybdenum": 10.2,
        "monel": 8.44,
        "nickel": 8.81,
        "platinum": 21.4,
        "silver": 10.4,
        "steel": 7.86,
        "tantalum": 16.6,
        "tin": 7.29,
        "titanium": 4.49,
        "tungsten": 18.7,
        "zinc": 7.11,
        # Plastics
        "abs": 1.07,
        "acrylic": 1.18,
        "bakelite": 1.36,
        "delrin": 1.43,
        "epoxy": 1.11,
        "melamine": 1.50,
        "nylon": 1.14,
        "polycarbonate": 1.2,
        "polyethylene": 0.94,
        "polypropylene": 0.90,
        "polystyrene": 1.06,
        "pvc": 1.39,
        "teflon": 2.20,
        # Other
        "alumina": 3.90,
        "glass": 2.6,
        "granite": 2.7,
        "graphite": 1.7,
        "marble": 2.69,
        "rubber": 1.00,
        # Woods
        "cedar": 0.38,
        "maple": 0.609,
        "oak": 0.720,
        "pine": 0.432,
        # Paired stuff
        "tungsten carbide": 15.6,
        "carbide": 15.6,
        "black cherry": 0.562,
        "cherry": 0.562,
        "douglas fir": 0.546,
        "fir": 0.546,
        "solder 63-37": 8.40,
        "solder": 8.40,
        "stainless 304": 8.02,
        "stainless": 8.02,
    }

    tr_matl = {
        # Convert a lower-case name that can be given on the command line
        # to the normal capitalized name.
        # Metals
        "aluminum": "Aluminum",
        "brass": "Brass",
        "bronze": "Bronze",
        "carbide": "Tungsten carbide",
        "cast iron": "Cast iron",
        "chromium": "Chromium",
        "cobalt": "Cobalt",
        "copper": "Copper",
        "gold": "Gold",
        "iron": "Cast iron",
        "lead": "Lead",
        "magnesium": "Magnesium",
        "mercury": "Mercury",
        "molybdenum": "Molybdenum",
        "monel": "Monel",
        "nickel": "Nickel",
        "platinum": "Platinum",
        "silver": "Silver",
        "solder 63-37": "Solder 63-37",
        "solder": "Solder 63-37",
        "stainless 304": "Stainless 304",
        "stainless": "Stainless 304",
        "steel": "Steel",
        "tantalum": "Tantalum",
        "tin": "Tin",
        "titanium": "Titanium",
        "tungsten": "Tungsten",
        "zinc": "Zinc",
        "tungsten carbide": "Tungsten carbide",
        # Plastics
        "abs": "ABS",
        "acrylic": "Acrylic",
        "bakelite": "Bakelite",
        "delrin": "Delrin",
        "epoxy": "Epoxy",
        "melamine": "Melamine",
        "nylon": "Nylon",
        "polycarbonate": "Polycarbonate",
        "polyethylene": "Polyethylene",
        "polypropylene": "Polypropylene",
        "polystyrene": "Polystyrene",
        "pvc": "PVC",
        "teflon": "Teflon",
        # Woods
        "black cherry": "Black cherry",
        "cedar": "Cedar (red)",
        "cherry": "Black cherry",
        "douglas fir": "Douglas fir",
        "fir": "Douglas fir",
        "maple": "Maple",
        "oak": "Oak",
        "pine": "Pine",
        # Other
        "alumina": "Alumina",
        "cement": "Cement",
        "glass": "Glass",
        "granite": "Granite",
        "graphite": "Graphite",
        "marble": "Marble",
        "rubber": "Rubber",
    }

    # Add the single words to spgr
    spgr["cherry"] = spgr["black cherry"]
    spgr["iron"] = spgr["cast iron"]
    spgr["fir"] = spgr["douglas fir"]
    spgr["solder"] = spgr["solder 63-37"]
    spgr["stainless"] = spgr["stainless 304"]

    # Diameters in inches
    fractions = (
        # Integer part of inches, numerator, denominator
        (0, 1, 16),
        (0, 1, 8),
        (0, 3, 16),
        (0, 1, 4),
        (0, 5, 16),
        (0, 3, 8),
        (0, 7, 16),
        (0, 1, 2),
        (0, 9, 16),
        (0, 5, 8),
        (0, 3, 4),
        (0, 7, 8),
        (1, 0, 1),
        (1, 1, 16),
        (1, 1, 8),
        (1, 1, 4),
        (1, 3, 8),
        (1, 1, 2),
        (1, 3, 4),
        (2, 0, 1),
        (2, 1, 4),
        (2, 1, 2),
        (2, 3, 4),
        (3, 0, 1),
        (3, 1, 2),
        (4, 0, 1),
        (4, 1, 2),
        (5, 0, 1),
        (6, 0, 1),
    )

    decimals = (
        # Integer part of inches, numerator, denominator
        (0, 1, 10),
        (0, 2, 10),
        (0, 3, 10),
        (0, 4, 10),
        (0, 5, 10),
        (0, 6, 10),
        (0, 7, 10),
        (0, 8, 10),
        (0, 9, 10),
        (1, 0, 10),
        (1, 1, 10),
        (1, 2, 10),
        (1, 3, 10),
        (1, 4, 10),
        (1, 5, 10),
        (1, 6, 10),
        (1, 7, 10),
        (1, 8, 10),
        (1, 9, 10),
        (2, 0, 10),
        (2, 2, 10),
        (2, 4, 10),
        (2, 6, 10),
        (2, 8, 10),
        (3, 0, 10),
        (3, 5, 10),
        (4, 0, 10),
        (4, 5, 10),
        (5, 0, 10),
        (6, 0, 10),
    )
    # Diameters in mm
    millimeters = tuple(
        list(range(1, 21)) + [25, 30, 35, 40, 45, 50, 60, 70, 80, 90, 100, 150, 200]
    )


def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    d1, d2, d3, D = "", "", "", "[default]"
    if d["default_output"] == "lbm/ft":
        d1 = D
    elif d["default_output"] == "lbm/in":
        d2 = D
    elif d["default_output"] == "kg/m":
        d3 = D
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] material
      Print out a table of the mass of bar stock for the given material.
      For materials, try "steel", "brass", etc. (use the -l option to see
      the material choices).
    Options:
        -c  Include conversions to other materials.
        -d  Output the diameter in decimal inches instead of fractions.
        -f  Output is in pounds per foot of length of bar stock.  {d1}
        -i  Output is in pounds per inch of length of bar stock.  {d2}
        -k  Output is in kg per m of length of bar stock.  {d3}
        -l  List materials
        -m  Use metric sizes for diameters.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-c"] = False
    d["-d"] = False
    d["-f"] = False
    d["-i"] = False
    d["-k"] = False
    d["-l"] = False
    d["-m"] = False
    # The following can be lbm/ft, lbm/in, or kg/m
    d["default_output"] = "lbm/in"
    d["gap"] = " " * 4
    if len(sys.argv) < 2:
        Usage(d)
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "cdfiklm")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    for opt in optlist:
        if opt[0] == "-c":
            d["-c"] = True
        elif opt[0] == "-d":
            d["-d"] = True
        elif opt[0] == "-f":
            d["-f"] = True
            d["default_output"] = "lbm/ft"
        elif opt[0] == "-i":
            d["-i"] = True
            d["default_output"] = "lbm/in"
        elif opt[0] == "-k":
            d["-k"] = True
            d["default_output"] = "kg/m"
        elif opt[0] == "-l":
            PrintMaterials()
            exit(0)
        elif opt[0] == "-m":
            d["-m"] = True
    if len(args) != 1:
        Usage(d)
    if d["-m"] and d["-d"]:
        Error("Can't use -m and -d options together")
    return args[0]


def PrintHeader(d):
    try:
        mat = tr_matl[d["material"]]
    except KeyError:
        Error("Material '%s' not recognized" % d["material"])
    title = "Mass of bar stock (material = {0})".format(mat)
    print("{0:^{1}}".format(title, width))
    sig.lead_zero = True
    ppci = sig(d["spgr"] * 0.0361273)
    s = "Specific gravity = {0} ({1} lb/in3)".format(sig(d["spgr"]), ppci)
    sig.lead_zero = False
    print("{0:^{1}}".format(s, width))
    df = d["default_output"]
    print(
        dedent(f"""
    Masses are in {df}.  Scale by square of diameter ratio for other diameters.
    """)
    )
    u1, u2 = ("mm", "in") if d["-m"] else ("in", "mm")
    h1, h2 = "-" * 12, "-" * 10
    print(
        dedent(f"""
    Diameter, {u1}      Round          Hex          Square      Diameter, {u2}
    """)
    )
    gap = d["gap"]
    print(h1, gap, h2, gap, h2, gap, h2, gap, h1, sep="")


# Materials for -c and -l options
metals = (
    "aluminum",
    "brass",
    "bronze",
    "iron",
    "chromium",
    "cobalt",
    "gold",
    "lead",
    "magnesium",
    "mercury",
    "molybdenum",
    "monel",
    "nickel",
    "platinum",
    "silver",
    "solder",
    "stainless",
    "steel",
    "tantalum",
    "tin",
    "titanium",
    "tungsten",
    "zinc",
)
plastics = (
    "abs",
    "acrylic",
    "bakelite",
    "delrin",
    "epoxy",
    "melamine",
    "nylon",
    "polycarbonate",
    "polyethylene",
    "polypropylene",
    "polystyrene",
    "pvc",
    "teflon",
)
woods = (
    "cedar",
    "cherry",
    "fir",
    "maple",
    "oak",
    "pine",
)
others = (
    "alumina",
    "glass",
    "granite",
    "graphite",
    "marble",
    "rubber",
)


def PrintMaterials():
    s = []
    s.append(" -- Metals --")
    for i in metals:
        s.append(i)
    s.append("")
    s.append(" -- Plastics --")
    for i in plastics:
        s.append(i)
    s.append("")
    s.append(" -- Woods --")
    for i in woods:
        s.append(i)
    s.append("")
    s.append(" -- Other --")
    for i in others:
        s.append(i)
    for i in Columnize(s, col_width=20, columns=4):
        print(i)


def PrintTrailer(d):
    # Put the dictionary single word entries into the local namespace.
    sig.fit = 8
    sig.dp_position = sig.fit // 2
    for i in spgr:
        try:
            exec("%s = '%s'" % (i, sig(spgr[i] / d["spgr"])))
        except Exception:
            pass
    s = "Mass conversion factors to other materials"
    print("\n{0:^{1}}\n".format(s, width))

    s, col_width, ndigits = [], 25, 3
    ctr = col_width - 4
    s.append("{0:^{1}}".format("Metals", ctr))
    fmt = "%-14s"
    for i in metals:
        u = sig(spgr[i] / d["spgr"], ndigits)
        t = fmt % tr_matl[i] + u
        s.append(t)
    s.append("")
    s.append("{0:^{1}}".format("Plastics", ctr))
    for i in plastics:
        u = sig(spgr[i] / d["spgr"], ndigits)
        t = fmt % tr_matl[i] + u
        s.append(t)
    s.append("")
    s.append("{0:^{1}}".format("Dry Woods", ctr))
    for i in woods:
        u = sig(spgr[i] / d["spgr"], ndigits)
        t = fmt % tr_matl[i] + u
        s.append(t)
    s.append("")
    s.append("{0:^{1}}".format("Other Materials", ctr))
    for i in others:
        u = sig(spgr[i] / d["spgr"], ndigits)
        t = fmt % tr_matl[i] + u
        s.append(t)
    for i in Columnize(s, col_width=col_width, columns=3):
        print(i)


def Line_mm(mm, round, hex, square):
    raise Exception("not impl")


def Line_inches(inches, numer, denom, round, hex, square, d):
    """Print a line of inch data."""
    if d["-d"]:  # Decimal inches
        x = inches + numer / denom
        s = "%.1f" % x
        if s[0] == "0":
            s = " " + s[1:]
            s = " " * 3 + s
        elif s[-1] == "0":
            s = s[:-2]
            s = " " * 3 + s
        else:
            s = " " * 3 + s
    else:  # Fractions
        if not inches:
            s = "   %d/%d" % (numer, denom)
        else:
            if numer:
                s = "%2d %d/%d" % (inches, numer, denom)
            else:
                s = "%2d      " % inches
    print("%-10s" % s, end="")
    print(d["gap"], end="")
    sig.low = 1e-6
    sig.fit = 12
    sig.dp_position = sig.fit // 2
    gap = " " * 1
    for i in (round, hex, square):
        print(sig(i), gap, end="")
    print("%10.1f" % ((inches + numer / denom) * 25.4))
    return s


def Line_mm(diam_mm, round, hex, square, d):
    """Print a line of mm data."""
    if int(diam_mm) == diam_mm:
        s = " %4d" % diam_mm
    else:
        s = "%.1f" % diam_mm
    print("%-10s" % s, end="")
    print(d["gap"], end="")
    sig.low = 1e-6
    sig.fit = 12
    sig.dp_position = sig.fit // 2
    gap = " " * 1
    for i in (round, hex, square):
        print(sig(i), gap, end="")
    print("%10.3f" % (diam_mm / 25.4))
    return s


def GetMass(diam_mm, d):
    """Return a tuple of mass per unit length for round, hex, and
    square cross sections; the units are given by the default_output
    setting in the dictionary d.
    """
    # Do the calculation in cm using specific gravity in g/cc and
    # convert to kg.
    diam_cm, length_cm, g2kg = diam_mm / 10, length_m * 100, 0.001
    round = pi / 4 * diam_cm**2 * length_cm * d["spgr"] * g2kg
    hex = sqrt(3) / 2 * diam_cm**2 * length_cm * d["spgr"] * g2kg
    square = diam_cm**2 * length_cm * d["spgr"] * g2kg
    # Units are kg/m.  Convert to the desired set of units.
    if d["default_output"] == "lbm/ft":
        round, hex, square = [i * 0.671969 for i in (round, hex, square)]
    elif d["default_output"] == "lbm/in":
        round, hex, square = [i * 0.0559974 for i in (round, hex, square)]
    return round, hex, square


def GetMaterial(d):
    """d["material"] contains the material entered by the user.  See if
    we can uniquely identify it; if so, return it; if not, issue an
    error message.
    """
    user_entered = d["material"].lower()
    if user_entered == "al":  # Special case because it's common
        user_entered = "aluminum"
    matches, materials = [], tr_matl.keys()
    for material in materials:
        if material.startswith(user_entered):
            matches.append(material)
    if not matches:
        Error("Material '{}' not recognized".format(d["material"]))
    if len(matches) == 1:
        d["material"] = matches[0]
    else:
        print(
            "Material '{}' matches more than one material:".format(d["material"]),
            file=sys.stderr,
        )
        for material in matches:
            print("  ", material, file=sys.stderr)
        exit(1)


if __name__ == "__main__":
    d = {}  # Options dictionary
    d["material"] = ParseCommandLine(d)
    GetMaterial(d)
    d["spgr"] = spgr[d["material"]]
    sig.lead_zero = False
    PrintHeader(d)
    length_m = 1
    if d["-m"]:
        for diam_mm in millimeters:
            round, hex, square = GetMass(diam_mm, d)
            Line_mm(diam_mm, round, hex, square, d)
    else:
        items = fractions
        if d["-d"]:
            items = decimals
        for i, numer, denom in items:
            diam = i + numer / denom
            round, hex, square = GetMass(diam * in2mm, d)
            Line_inches(i, numer, denom, round, hex, square, d)
    if d["-c"]:
        PrintTrailer(d)
