'''
Print out a decimal equivalents table.

There are two primary behaviors:  
    * A typical fractions of an inch to decimal inches table is printed.
    * An extensive table of fractions, mm, and various gauges is printed
      (this is similar to the spreadsheet printout on my shop wall).
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Decimal equivalents and finding close sizes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import sys
    from math import *
    from fractions import Fraction
    from bisect import bisect_left, bisect_right
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from frange import frange
    from sig import sig
    from columnize import Columnize
    from u import u
    from fraction import FormatFraction, ToFraction
    import color
    import sizes
if 1:   # Global variables
    # How much to indent a fraction to have pleasing offsets to make the
    # table easier to read.
    default_indents = {
        1 : 0,
        2 : 0,
        4 : 0,
        8 : 0,
        16 : 0,
        32 : 4,
        64 : 9,
    }
    max_indent = max(default_indents.values())
    # This color is used to indicate a match in the extended listing that has
    # zero % deviation from the desired value.
    match = color.yellow
    # Names of the gauges
    GN = {
        "awg": "AWG",
        "ltr": "letter drill",
        "#": "number drill",
        "lathe": "lathe tpi",
        "US": "US std sheet",
        "shtstl": "sheet steel",
        "galv": "galv sheet",
        "sst": "stainless sheet",
        "al": "aluminum sheet",
        "zn": "zinc sheet",
        "hyp": "hypodermic needle OD",
        "siron": "Stubs iron wire",
        "wm": "W&M wire",
        "music": "music wire",
        "sstl": "Stubs steel wire",
        "frac": "fractional inch",
        "mm": "mm",
        "cm": "cm",
        "ISO": "ISO metric drill",
        "tap75": "75% tap drill",
        "tap50": "50% tap drill",
        "tmd": "thread major diameter",
        "NPT": "US tapered pipe thread",
        "NPS": "US straight pipe thread",
        "hexn": "hex nut wrench size",
        "hexh": "bolt head wrench size",
        "shcs": "SHCS Allen wrench size",
        "fhcs": "FHCS Allen wrench size",
        "set": "set screw Allen wrench size",
    }
    # The full name should be limited in length so output fits on 80 column
    # screen.
    maxlen = 28
    for gn in GN:
        assert(len(GN[gn]) <= maxlen)
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    print(dedent(f'''
    Usage:  {name} [options] [size [unit]]
      Search for a given size and prints out various common & gauge sizes near
      the given size.  Tap drills are given for common thread sizes at 75%
      (recommended for soft metals and plastics) and 50% (for steels and cast
      iron).  Inches are the default units; other common units are supported.
    Example:  for a 9 mm hole, the closest drill is a T letter drill,
              which is 1% off the needed diameter.
    Options
      -a    Limit the data to number & letter drills, fractional inches, AWG
            sizes, tpi, and mm.
      -c    Don't colorize the extended output.
      -d n  Show the decimal inch equivalents to n digits.  4 is the default.
      -f    Convert the fractional strings on the command line to Unicode
            expressions.  Give mixed fractions as e.g. 1-3/16.
      -H    Extended help information
      -n L  Show L lines before and after the closest match when searching.  Set
            to 0 to see all lines.
      -s c  Sort the output by column c.  1 means sorted by diameter, 2 means
            sorted by designator/gauge, 3 means sorted by gauge type.
      -T    Fractions of an inch table in Unicode.
      -t    Show fractions of an inch table.
      -w    Show metric and inch wrench sizes
      -x    Show extended table.
    '''))
    exit(status)
def ExtendedHelp():
    print(dedent(f'''
    Expressions are allowed on the command line for the size argument and the math
    library functions are in scope.  This allows you to do a size search such as

        '42*cos(radians(44))' mm

    The following size units will be recognized:
        Angstrom         fathom           link             nmi
        ang              feet             ls               nmile
        angstrom         foot             ly               pace
        astronomicalunit ft               meter            parsec
        au               furlong          meters           pc
        cable            furlongs         metre            point
        caliber          hand             metres           pt
        chain            hands            mi               rod
        click            inch             micron           standardgauge
        clicks           inches           mil              sunradius
        ddime            klick            mile             thou
        dhalf            klicks           miles            yard
        dnickel          league           moonradius       yards
        dpenny           lightsecond      nauticalmile     yd
        dquarter         lightyear        nauticalmiles    yds
        earthradius
    The u.py module is used to process these units and it's easy to add
    other units to your tastes.
    '''))
    exit(0)
def WrenchSizes(d):
    '''Print a table showing metric and inch wrench sizes.
    '''
    MM, out = list(range(5, 23)) + [24, 27, 30, 32, 36, 38, 41, 46, 50], []
    inch = (list(frange("3/16", "3/2", "1/16")) + 
            list(frange("3/2", "17/8", "1/8")))
    print("    Wrench size comparisons")
    # Metric columns
    out.append("mm    in    ")
    for mm in MM:
        s = "{:4s} {:5.3f}".format(str(mm), mm/25.4)
        out.append(s)
    # Join them
    sep = " "*12
    out[0] += sep + "in    Decimal   mm"
    for i, inches in enumerate(inch):
        s = "{} {:^6s} {:6.3f} {:6.1f}".format(sep, str(inches), float(inches), inches*25.4)
        out[i + 1] += s
    for i in out:
        print(i)
    exit(0)
def FmtFrac(f, indents=default_indents):
    '''Format a fraction as a string 'numerator/denominator'.  The
    indents are how many spaces the 16th, 32nd, and 64th rows get.
    '''
    N, D = f.numerator, f.denominator
    before = " "*indents[D]
    after = " "*(max_indent - indents[D])
    if d["-T"]:
        s = FormatFraction(f)
    else:
        s = "{0}/{1}".format(N, D)
    if N == 1 and D == 1:
        s = "1"
    return "{0}{1:<5s} {2}".format(before, s, after)
def PrintNormalTable(d):
    out, denom, n = [], 64, d["-d"]
    length = None
    xx()
    for numer in range(1, denom + 1):
        f = Fraction(numer, denom)
        s = FmtFrac(f)
        s += " {:.{}f}".format(float(f), n)
        # Include mm equivalent
        s += " {:>4.1f}".format(float(f)*25.4)
        out.append(s)
    for i in Columnize(out):
        print(i)
def MakeTable(dictionary, identifier):
    '''From the indicated dictionary, construct a table of 
        (dia_inches, gauge, identifier)
    for the indicated items.
    '''
    t = []
    for gauge in dictionary:
        t.append([dictionary[gauge], sizes.TranslateGauge(gauge), identifier])
    return t
def Lathe(lathe_tpi):
    t = []
    for tpi in lathe_tpi:
        dia = round(1/tpi, 6)
        t.append([dia, str(tpi), GN["lathe"]])
    return t
def TapDrills(d):
    '''Calculate the 50% and 75% tap drills for commonly-used threads.
    '''
    from asme import UnifiedThread as UT
    # Number thread major diameter in inches
    nt = lambda n:  round(0.06 + 0.013*n, 4)
    t = []
    # ----------------------------------------------------------------------
    # Inch-based threads
    T = { 
        "C": # UNC coarse numbered sizes
        ((1, 64), (2, 56), (3, 48), (4, 40), (5, 40),
        (6, 32), (8, 32), (10, 24), (12, 24)),
        "F": # UNF fine numbered sizes
        ((0, 80), (1, 72), (2, 64), (3, 48), (4, 48),
        (5, 44), (6, 40), (8, 36), (10, 32), (12, 28)),
    }
    for U in T:
        for n, tpi in T[U]:
            major_dia = nt(n)
            # Thread major diameter
            t.append([major_dia, "#{}-{}{}".format(n, tpi, U), GN["tmd"]])
            # 75% tap drill
            thd = UT(major_dia, tpi)
            td = thd.TapDrill(75)
            t.append([td, "#{}-{}{}".format(n, tpi, U), GN["tap75"]])
            # 50% tap drill
            td = thd.TapDrill(50)
            t.append([td, "#{}-{}{}".format(n, tpi, U), GN["tap50"]])
    T = { 
        "C": # UNC coarse fractional sizes
        (("1/4", 20), ("5/16", 18), ("3/8", 16), ("7/16", 14), ("1/2", 13),
        ("9/16", 12), ("5/8", 11), ("3/4", 10), ("7/8", 8), ("1", 8)),
        "F": # UNF fine fractional sizes
        (("1/4", 28), ("5/16", 24), ("3/8", 24), ("7/16", 20), ("1/2", 20),
        ("9/16", 18), ("5/8", 18), ("3/4", 16), ("7/8", 14), ("1", 12)),
    }
    for U in T:
        for f, tpi in T[U]:
            major_dia = eval(f)
            # Thread major diameter
            t.append([major_dia, "{}-{}{}".format(f, tpi, U), GN["tmd"]])
            # 75% tap drill
            thd = UT(major_dia, tpi)
            td = thd.TapDrill(75)
            t.append([td, "{}-{}{}".format(f, tpi, U), GN["tap75"]])
            # 50% tap drill
            td = thd.TapDrill(50)
            t.append([td, "{}-{}{}".format(f, tpi, U), GN["tap50"]])
    for name, td in (("1/8 NPT", 0.339),
                    ("1/4 NPT", 0.438),
                    ("3/8 NPT", 0.578),
                    ("1/2 NPT", 0.719),
                    ("3/4 NPT", 0.922),
                    ("1 NPT", 1.156),
                    ("1-1/4 NPT", 1.5),
                    ("1-1/2 NPT", 1.734),
                    ("2 NPT", 2.219)):
        t.append([td, "{}".format(name), GN["NPT"]])
    for name, td in (("1/8 NPS", 0.348),
                    ("1/4 NPS", 0.453),
                    ("3/8 NPS", 0.594),
                    ("1/2 NPS", 0.734),
                    ("3/4 NPS", 0.938),
                    ("1 NPS", 1.188),
                    ("1-1/4 NPS", 1.516),
                    ("1-1/2 NPS", 1.75),
                    ("2 NPS", 2.219)):
        t.append([td, "{}".format(name), GN["NPS"]])
    # ----------------------------------------------------------------------
    # Metric threads
    T = { 
        "C": # Metric coarse threads
            ("M1×0.25 M1.2×0.25 M1.4×0.3 M1.6×0.35 M1.7×0.35 M1.8×0.35 "
            "M2×0.4 M2.2×0.45 M2.5×0.45 M3×0.5 M3.5×0.6 M4×0.7 M4.5×0.75 "
            "M5×0.8 M6×1 M7×1 M8×1.25 M9×1.25 M10×1.5 M11×1.5 M12×1.75 "
            "M14×2 M16×2 M18×2.5 M20×2.5 M22×2.5 M24×3"),
        "F": # Metric fine threads
            ("M1×0.2 M1.2×0.2 M1.4×0.2 M1.6×0.2 M1.8×0.2 M2×0.25 "
            "M2.5×0.35 M3×0.35 M3.5×0.35 "
            "M4×0.5 M5×0.5 M6×0.5 M6×0.75 M7×0.75 M8×0.75 M8×1 M10×1 "
            "M10×1.25 M12×1 M12×1.25 M14×1.5 M14×2 M16×1.5 M18×1.5 M18×2 "
            "M20×1 M20×1.5 M20×2 M22×1 M22×1.5 M22×2 M24×1.5 M24×2"),
    }
    for U in T:
        for i in T[U].split():
            sz, p = i.split("×")
            sz = round(float(sz.replace("M", ""))/25.4, 4)
            p = float(p)
            t.append([sz, "{}".format(i + U), GN["tap75"]])
    # Nut and wrench sizes
    T = ("#0,5/32 #1,5/32 #2,3/16 #3,3/16 #4,1/4 #5,5/16 #6,5/16 #8,11/32 "
        "#10,3/8 1/4,7/16 5/16,1/2 3/8,9/16 7/16,11/16 1/2,3/4 5/8,15/16 "
        "3/4,9/8 7/8,21/16 1,3/2")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(eval(wrench)), 4)
        t.append([d, "{} hex nut".format(size), GN["hexn"]])
    T = ("#1,1/8 #2,1/8 #3,3/16 #4,3/16 #5,3/16 #6,1/4 #8,1/4 "
        "#10,5/16 1/4,7/16 5/16,1/2 3/8,9/16 7/16,5/8 1/2,3/4 5/8,15/16 "
        "3/4,9/8 7/8,21/16 1,3/2")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(eval(wrench)), 4)
        t.append([d, "{} hex head".format(size), GN["hexh"]])
    T = ("#0,0.05 #1,1/16 #2,5/64 #3,5/64 #4,3/32 #5,3/32 #6,7/64 #8,9/64 "
        "#10,5/32 1/4,3/16 5/16,1/4 3/8,5/16 7/16,3/8 1/2,3/8 5/8,1/2 "
        "3/4,5/8 7/8,3/4 1,3/4")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(eval(wrench)), 4)
        t.append([d, "{} SHCS head".format(size), GN["shcs"]])
    # Metric screw head sizes
    # https://en.wikipedia.org/wiki/ISO_metric_screw_thread
    T = ("M2,4 M2.5,5 M3,5.5 M3.5,6 M4,7 M5,8 M6,10 M7,11 M8,13 M10,16 "
        "M12,18 M14,21 M16,24 M18,27 M20,30 M22,34 M24,36")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(wrench)/25.4, 4)
        t.append([d, "{} hex head".format(size), GN["hexh"]])
    T = ("M2,1.5 M2.5,2  M3,2.5 M4,3  M5,4  M6,5  M8,6  M10,8  M12,10 "
        "M14,10 M16,14 M18,14 M20,17 M22,17 M24,19")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(wrench)/25.4, 4)
        t.append([d, "{} SHCS head".format(size), GN["shcs"]])
    T = ("M2,1.25 M2.5,1.5 M3,2 M4,2.5 M5,3 M6,4 M8,5 M10,6 M12,8 M16,10 "
        "M18,12 M20,12 M22,14 M24,14")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(wrench)/25.4, 4)
        t.append([d, "{} FHCS head".format(size), GN["fhcs"]])
    T = ("M2,0.9 M2.5,1.3 M3,1.5 M4,2 M5,2.5 M6,3 M8,4 M10,5 M12,6 "
        "M16,8 M20,10 M24,12")
    for size, wrench in [i.split(",") for i in T.split()]:
        d = round(float(wrench)/25.4, 4)
        t.append([d, "{} set scr".format(size), GN["set"]])
    return t
def GetMetricSizes(d):
    '''Make a list of metric sizes.
    '''
    t = []
    # 0.5 mm resolution up to 13 mm (typical 25-piece drill set)
    for mm in frange("0", "13.1", "0.5"):
        t.append([round(mm/25.4, 8), "{} mm".format(mm), "mm"])
    # 1 mm resolution from 10 mm and above
    for mm in range(1, 300):
        t.append([round(mm/25.4, 8), "{} mm".format(mm), "mm"])
    return t
def BuildExtendedTable(args, d):
    '''Return a list with elements 
        (dia_inches, gauge, identifier)
    where 
        dia_inches is a float
        gauge identifies the name to show (e.g., 34 or 7/0)
        identifier is a string to identify the origin (e.g. "AWG")
    If args is not empty, search for the sizes that are within range of the
    stated size.
    '''
    t = MakeTable(sizes.number_drills, GN["#"])
    t.extend(MakeTable(sizes.letter_drills, GN["ltr"]))
    t.extend(Lathe(sizes.clausing_lathe_tpi))
    t.extend(MakeTable(sizes.AWG, GN["awg"]))
    if d["-a"]:
        t.extend(MakeTable(sizes.US_Standard, GN["US"]))
        t.extend(MakeTable(sizes.steel, GN["shtstl"]))
        t.extend(MakeTable(sizes.galvanized_steel, GN["galv"]))
        t.extend(MakeTable(sizes.stainless_steel, GN["sst"]))
        t.extend(MakeTable(sizes.aluminum, GN["al"]))
        t.extend(MakeTable(sizes.zinc, GN["zn"]))
        t.extend(MakeTable(sizes.hypodermic_needles, GN["hyp"]))
        t.extend(MakeTable(sizes.stubs_iron_wire, GN["siron"]))
        t.extend(MakeTable(sizes.Washburn_and_Moen_steel_wire, GN["wm"]))
        t.extend(MakeTable(sizes.music_wire, GN["music"]))
        t.extend(MakeTable(sizes.stubs_steel_wire, GN["sstl"]))
        t.extend(TapDrills(d))
    # Millimeter sizes
    MM = GetMetricSizes(d)
    t.extend(MM)
    # Fractions of an inch:  64ths to 1 inch, 16ths to 2 inches, 8ths to 12
    # inches.
    F = []
    for f in frange("1/64", "1", "1/64"):
        F.append([float(f), str(f), GN["frac"]])
    F.append([1, "1", GN["frac"]])
    for f in frange("17/16", "2", "1/16"):
        F.append([float(f), str(f), GN["frac"]])
    for f in frange("17/8", "97/8", "1/8"):
        F.append([float(f), str(f), GN["frac"]])
    t.extend(F)
    return t
def SortTable(table, column_number):
    if column_number == 0:
        return sorted(table)
    elif column_number == 1:
        t = sorted([(j, i, k) for i, j, k in table])
        return [(j, i, k) for i, j, k in t]
    elif column_number == 2:
        t = sorted([(k, i, j) for i, j, k in table])
        return [(j, k, i) for i, j, k in t]
    else:
        raise ValueError("Column number {} is bad".format(column_number))
def NumberSizeScrew(args):
    'Return dia in inches if args[0] begins with "#" else None'
    if len(args) != 1:
        return None
    if args[0] and args[0][0] != "#":
        return None
    try:
        n = int(args[0][1:])
        if not (0 <= n <= 20):
            raise Exception()
    except Exception:
        Error("'{args[0]}' is a bad number size")
    return round(0.06 + n*0.013, 4)
def PrintExtendedTable(args, d):
    # Build dictionary for colors to use.  Note:  at the moment, this isn't
    # used except for printing the matches.
    c = {}
    for key in GN:
        c[GN[key]] = None
    c["0dev"] = match
    # Construct data
    t = BuildExtendedTable(args, d)
    t = SortTable(t, 0)     # Sort by diameter in inches
    # If command line arguments were given, we need to reduce the table to
    # the relevant lines.
    if args:
        try:
            search = args[0]
            dia_search = NumberSizeScrew(args)
            if dia_search is None:
                dia_search = float(eval(args[0]))
                if not dia_search:
                    print("Diameter must be nonzero")
                    exit(1)
                if len(args) > 1:
                    unit = args[1]
                    try:
                        dia_search = dia_search*u(unit)/u("in")
                    except TypeError:
                        print("Bad length unit")
                        exit(1)
                    search += " " + args[1]
            print("Desired size =", search, "=", sig(dia_search), "inches")
            print()
            # dia_search is desired dimension in inches.  Find closest size
            # in table.  
            m = d["-n"] if d["-n"] else 1e8
            T = [i[0] for i in t]  # Just diameters in inches
            nleft = bisect_left(T, dia_search)
            nright = bisect_right(T, dia_search)
            lo, hi = max(nleft - m, 0), min(nright + m, len(t))
            t = t[lo:hi]
        except Exception as ex:
            print("Search for arguments on command line failed:")
            print("  ", ex)
            exit(1)
    # Print the results.  Note this is aimed at a screen 80 columns wide or
    # wider.
    t = SortTable(t, d["-s"])   # Sort order desired
    if args:
        print('''
    Size        Inches       mm          Category                      %dev
-----------     --------     -------     --------                      ----
'''[1:-1])
        fmt = "{{:^14s}}  {{:8s}}     {{:8s}}    {{:{}s}}  {{}}".format(maxlen)
    else:
        print('''
    Size        Inches       mm          Category
-----------     --------     -------     --------
'''[1:-1])
        fmt = "{:^14s}  {:8s}     {:8s}    {}"
    for dia, identifier, name in t:
            C = c[name]
            if C and d["-c"]:
                color.fg(C)
            if args:
                pct = 100*(dia - dia_search)/dia_search
                if abs(pct) <= 1e-3:
                    pct = 0
                dev = sig(pct, 2)
                if pct >= 0:
                    dev = " " + dev
                if not pct:
                    if d["-c"]:
                        color.fg(c["0dev"])
                    else:
                        dev += "    *"
                print(fmt.format(identifier, 
                                 sig(dia),
                                 sig(dia*25.4),
                                 name,
                                 dev))
                if d["-c"]:
                    color.normal()
            else:
                print(fmt.format(identifier, 
                                 sig(dia),
                                 sig(dia*25.4),
                                 name))
            if C and d["-c"]:
                color.normal()
def ParseCommandLine(d):
    d["-a"] = True      # If True, show all gauges
    d["-c"] = True      # Colorize output
    d["-d"] = 4         # Number of decimal places
    d["-f"] = False     # Convert command line fractions to Unicode
    d["-H"] = False     # Extended help
    d["-n"] = 10        # Number of lines before & after search item
    d["-s"] = 0         # Sorting of output
    d["-T"] = False     # Show fractions of an inch table in Unicode
    d["-t"] = False     # Show fractions of an inch table
    d["-x"] = False     # Use extended table
    try:
        opts, args = getopt.getopt(sys.argv[1:], "acd:fHhn:s:Ttwx")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o[1] in list("acfHTtx"):
            d[o] = not d[o]
        elif o in ("-d",):
            try:
                d["-d"] = n = int(a)
                if not (1 <= n <= 6):
                    raise Exception()
            except Exception:
                print("-d option must be an integer between 1 and 6")
                exit(1)
        elif o in ("-n",):
            try:
                d["-n"] = n = int(a)
                if n < 0:
                    raise Exception()
            except Exception:
                print("-n option must be an integer >= 0")
                exit(1)
        elif o in ("-s",):
            try:
                d["-s"] = n = int(a) - 1
                if not (0 <= n <= 2):
                    raise Exception()
            except Exception:
                print("-s option must be an integer between 1 and 3")
                exit(1)
        elif o in ("-w",):
            WrenchSizes(d)
        elif o in ("-h",):
            Usage(d, status=0)
    if d["-H"]:
        ExtendedHelp()
    sig.digits = d["-d"]
    if not args:
        Usage(d)
    return args
if __name__ == "__main__": 
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    if d["-f"]:
        for arg in args:
            f = ToFraction(arg)
            print(f"{arg}\t{FormatFraction(f)}")
    elif args or d["-x"]:
        PrintExtendedTable(args, d)
    elif d["-t"] or d["-T"]:
        PrintNormalTable(d)
