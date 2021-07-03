'''
Print out a table of drill sizes

    If an argument was given, print out the nearest drill sizes.  Use
    color to indicate it's a size I have and what series:

        Red         Fractional
        Yellow      Numbered
        Magenta     Letter
        Blue        Metric

    I don't have a metric set, but typical sets go from 1 to 13 mm by 0.5
    mm steps.
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
    # Print out drill sizes
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    import getopt
    import color as c
    #from math import *
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
if 1:   # Global variables
    DrillSizes = '''
        # Name:(diameter in inches)
        # Letter sizes
        A:0.234 B:0.238 C:0.242 D:0.246 E:0.250 F:0.257 G:0.261 H:0.266
        I:0.272 J:0.277 K:0.281 L:0.290 M:0.295 N:0.302 O:0.316 P:0.323
        Q:0.332 R:0.339 S:0.348 T:0.358 U:0.368 V:0.377 W:0.386 X:0.397
        Y:0.404 Z:0.413
        # Number sizes
        1:0.2280 2:0.2210 3:0.2130 4:0.2090 5:0.2055 6:0.2040 7:0.2010
        8:0.1990 9:0.1960 10:0.1935 11:0.1910 12:0.1890 13:0.1850
        14:0.1820 15:0.1800 16:0.1770 17:0.1730 18:0.1695 19:0.1660
        20:0.1610 21:0.1590 22:0.1570 23:0.1540 24:0.1520 25:0.1495
        26:0.1470 27:0.1440 28:0.1405 29:0.1360 30:0.1285 31:0.1200
        32:0.1160 33:0.1130 34:0.1110 35:0.1100 36:0.1065 37:0.1040
        38:0.1015 39:0.0995 40:0.0980 41:0.0960 42:0.0935 43:0.0890
        44:0.0860 45:0.0820 46:0.0810 47:0.0785 48:0.0760 49:0.0730
        50:0.0700 51:0.0670 52:0.0635 53:0.0595 54:0.0550 55:0.0520
        56:0.0465 57:0.0430 58:0.0420 59:0.0410 60:0.0400 61:0.0390
        62:0.0380 63:0.0370 64:0.0360 65:0.0350 66:0.0330 67:0.0320
        68:0.0310 69:0.0293 70:0.0280 71:0.0260 72:0.0250 73:0.0240
        74:0.0225 75:0.0210 76:0.0200 77:0.0180 78:0.0160 79:0.0145
        80:0.0135
    '''
def GetDictFromString(string):
    d = {}
    for line in string.split("\n"):
        s = line.strip()
        if not s or s[0] == "#":
            continue
        for item in s.split():
            f = item.split(":")
            size, dia_inches = f
            d[size] = float(dia_inches)
    return d
def Str(x):
    '''If x is equal to an integer, return its string value.  Otherwise,
    return it with one decimal place.
    '''
    if int(x) == x:
        return str(int(x))
    else:
        return f"{x:.1f}"
def GetDrillSizes(metric=False):
    '''Return a dictionary relating drill name (a string or number) to
    drill diameter in inches.  The keys will be:
        Ends in 'mm'       Metric size in mm
        Capital letters    Letter drills
        Number strings     Number drills
        Contains '/'       Fractional
    If metric is True, return the dictionary values in mm.
    '''
    sz, denominator, in2mm, mm2in = {}, 64, 25.4, 1/25.4
    # Fractions of an inch
    for numerator in range(1, denominator + 1):
        f = Fraction(numerator, denominator)
        sz[f"{f.numerator}/{f.denominator}"] = f
    # Metric (integer steps in units of 0.1 mm)
    min, max, step = 1, 13, 0.5
    for i in range(min*10, int(max + step)*10 + 1, int(10*step)):
        sz[Str(i/10) + " mm"] = (i/10)*mm2in
    sz.update(GetDictFromString(DrillSizes))
    if metric:
        for i in sz:
            sz[i] = round(sz[i]*in2mm, 2)
    return sz
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    name = sys.argv[0]
    tol = d["-t"]
    metric = bool(d["-m"])
    print(dedent(f'''
    Usage:  {name} [options] [size1 [size2...]]
      Prints out a table of drill sizes if no arguments given.  For each
      size in inches, print out nearest standard drill sizes.  Append 'mm'
      to the size to specify it in mm.  size can be an expression (the
      math library's symbols are in scope).
     
    Example:    python {name} pi/10
      will print out drill sizes that are near one-tenth of pi inches.
     
    Options [default]:
        -c
            Don't print in color (i.e., don't output escape sequences).
        -m
            Output the drill diameters in mm. [{metric}]
        -t pct
            When printing a list of matching sizes, use pct as the
            tolerance in percent.  [{tol}%]
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = True      # Output in color
    d["-m"] = False     # Output in mm
    d["-t"] = "10"      # Tolerance in %
    try:
        opts, sizes = getopt.getopt(sys.argv[1:], "chmt:")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, a in opts:
        if o in ("-c",):
            d["-c"] = not d["-c"]
        elif o in ("-h",):
            Usage(d, status=0)
        elif o in ("-m",):
            d["-m"] = not d["-m"]
        elif o in ("-t",):
            d["-t"] = a
            try:
                pct = float(d["-t"])
                if pct < 0:
                    raise Exception
            except Exception:
                Error("'{0}' is a bad percentage (use -h for help)".format(a))
    return sizes
def GetFormat(max_length, d):
    metric = d["-m"]
    rnd = 2 if metric else 4
    return "{{0:^{0}s}}  {{1:.{1}f}}".format(max_length, rnd)
def PrintTable(d):
    metric = d["-m"]
    sz = [(size, name) for name, size in GetDrillSizes(metric=d["-m"]).items()]
    sz.sort()
    out, rnd = [], 2 if metric else 4
    # Get maximum length of name strings
    max_length = max([len(name) for size, name in sz])
    fmt = GetFormat(max_length, d)
    for size, name in sz:
        out.append(fmt.format(name, float(size)))
    print("Drill sizes in", "mm" if metric else "inches")
    for i in Columnize(out):
        print(i)
def PrintSize(size, d):
    size = size.strip()
    metric, indent = d["-m"], 4
    s, convert_size = size, 1
    try:
        if size.endswith("mm"):
            s = size.replace("mm", "")
            convert_size = 1/25.4
        sz_inches = convert_size*float(eval(s))
        if sz_inches <= 0:
            raise Exception
    except Exception:
        Error("'{0}' is a bad size (use -h for help)".format(size))
    tol = float(d["-t"])/100
    # Find sizes that are within +/- tol of the indicated size.
    print("Drills within {0}% of size '{1}':".format(d["-t"], size))
    if metric:
        print(" "*indent, "Target size = ",
              "{0:.2f} mm".format(sz_inches*25.4), sep="")
    else:
        print(" "*indent, "Target size = ",
              "{0:.4f} inches".format(sz_inches), sep="")
    sz = [(size, name) for name, size in GetDrillSizes(metric=d["-m"]).items()]
    sz.sort()
    s = []
    for size, name in sz:
        if (1 - tol)*sz_inches <= size <= (1 + tol)*sz_inches:
            s.append((size, name))
    max_length = max([len(name) for size, name in sz])
    # Get the best match
    t = []
    for size, name in s:
        pct = 100*(float(size) - sz_inches)/sz_inches
        t.append((abs(pct), name))
    t.sort()
    best = t[0][1]
    fmt = " "*4 + GetFormat(max_length, d)
    fmt += " "*indent + "{2: .2g}%    {3}"
    for size, name in s:
        if d["-c"]:
            flag = ""
            if name == best:
                c.fg(c.lred)
            else:
                c.normal()
        else:
            flag = "*" if name == best else ""
        pct = 100*(float(size) - sz_inches)/sz_inches
        print(fmt.format(name, float(size), pct, flag))
    c.normal()
if __name__ == "__main__": 
    d = {}  # Options dictionary
    sizes = ParseCommandLine(d)
    if sizes:
        for size in sizes:
            PrintSize(size, d)
    else:
        PrintTable(d)
