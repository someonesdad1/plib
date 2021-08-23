'''
Generate a temperature table
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2017 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Generate a temperature table
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import getopt
    import os
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from temperature import ConvertTemperature
    from frange import frange
    from sig import sig
if 1:   # Global variables
    ii = isinstance
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    n, unit = d["-d"], d["-u"]
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] start end increment [unit]
      Generate a temperature conversion table.  If unit is included, it must
      be one of C, F, K, R (defaults to {unit}).
    Example:  '{sys.argv[0]} 0 100 50 c' produces
        °C       °F        K       °R       
          0       32      273      492      
         50      122      323      582      
        100      212      373      672      
    Options:
      -d n  Set number of significant digits.  [{n}]
    '''))
    exit(status)
def GetTemp(s):
    try:
        return int(s)
    except ValueError:
        return float(s)
def ParseCommandLine(d):
    d["-u"] = "C"       # Primary unit (C, F, R, K)
    d["-d"] = 3         # Number of significant digits
    d["units"] = frozenset("CFRK")
    d["range"] = frange # Iterator for input temperatures
    if len(sys.argv) < 2:
            Usage(d)
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d:h")
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
        elif o in ("-h", "--help"):
            Usage(d, status=0)
    sig.digits = d["-d"]
    if len(args) not in (3, 4):
        Usage(d)
    if len(args) == 4:
        if args[3].upper() not in set("CFRK"):
            Error("Unit option must be C, F, R, or K")
        d["-u"] = args[3].upper()
    # Get the specifier for the sequence of temperatures
    d["specs"] = [GetTemp(i) for i in args[:3]]
    # Force inclusion of the endpoint by adding the increment to end
    d["specs"][1] += d["specs"][2]
    if all([ii(i, int) for i in d["specs"]]):
        d["range"] = range
def rdp(s):
    if s[-1] == ".":
        return s[:-1]
    return s
def deg(s):
    if s != "K":
        return "°" + s
    return s
if __name__ == "__main__":
    d = {}      # Options dictionary
    sig.idp = False
    sig.rtz = True
    ParseCommandLine(d)
    # Get the output column units
    if d["-u"] == "C":
        out = [["C", "F", "K", "R"]]
    elif d["-u"] == "F":
        out = [["F", "C", "K", "R"]]
    elif d["-u"] == "R":
        out = [["R", "K", "C", "F"]]
    else:
        out = [["K", "C", "F", "R"]]
    iu, ou1, ou2, ou3 = out[0]
    for t in d["range"](*d["specs"]):
        t1 = sig(ConvertTemperature(t, iu, ou1))
        t2 = sig(ConvertTemperature(t, iu, ou2))
        t3 = sig(ConvertTemperature(t, iu, ou3))
        out.append((rdp(sig(t)), rdp(t1), rdp(t2), rdp(t3)))
    # Get maximum string size
    size = 0
    for i in out:
        size = max(size, *[len(j) for j in i])
    # Print report
    fr = "{{:>{}s}}".format(size)
    fc = "{{:^{}s}}".format(size)
    if 0:
        from pprint import pprint as pp
        pp(out)
        exit()
    sep = " "*4
    for i, items in enumerate(out):
        if i:
            for j in items:
                print(fr.format(j), sep, end=" ")
        else:
            for j in items:
                print(fc.format(deg(j)), sep, end=" ")
        print()
