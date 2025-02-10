'''
Generate a temperature table
'''
if 1:  # Header
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
        from color import t
        from temperature import ConvertTemperature
        from frange import frange
        from sig import sig
        from f import flt
if 1:   # Global variables
    ii = isinstance
if 1:   # Utility
    def GetColors():
        t.k = t.roy if d["-c"] else ""
        t.c = t.yel if d["-c"] else ""
        t.f = t.grn if d["-c"] else ""
        t.r = t.viol if d["-c"] else ""
        t.N = t.n if d["-c"] else ""
    def Error(msg, status=1):
        print(msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        n, unit = d["-d"], d["-u"]
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] start end increment [column1]
          Generate a temperature conversion table.  If column1 is included, it must be one of C, F,
          K, R (defaults to {unit}, case not important) and is the first column's temperature unit.
        Example:  '{sys.argv[0]} 0 100 50 c' produces
            °C       °F        K       °R       
              0       32      273      492      
             50      122      323      582      
            100      212      373      672      
        Options:
          -c    Don't print in color
          -d n  Set number of significant digits.  [{n}]
        '''))
        exit(status)
    def GetTemp(s):
        try:
            return int(s)
        except ValueError:
            return float(s)
    def ParseCommandLine(d):
        d["-c"] = True          # Print colors
        d["-u"] = "C"           # Primary unit (C, F, R, K)
        d["-d"] = 3             # Number of significant digits
        d["units"] = tuple("CFRK")
        d["range"] = frange     # Iterator for input temperatures
        if len(sys.argv) < 2:
                Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cd:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("c"):
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
        GetColors()
if 1:   # Core functionality
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
    x = flt(0)
    x.rtz = x.rtdp = True
    x.N = d["-d"]
    cu = {  # Output column units
        "C": "°C °F K °R".split(),
        "F": "°F °C K °R".split(),
        "R": "°R K °C °F".split(),
        "K": "K °C °F °R".split(),
    }
    clr = { # Column colors
        "C": [t.c, t.f, t.k, t.r],
        "F": [t.f, t.c, t.k, t.r],
        "R": [t.r, t.k, t.c, t.f],
        "K": [t.k, t.c, t.f, t.r],
    }
    out = [cu[d["-u"]]]
    iu, ou1, ou2, ou3 = [i.replace("°", "") for i in out[0]]
    # Calculate the temperature table's units
    for T in d["range"](*d["specs"]):
        if 0:
            t1 = sig(ConvertTemperature(T, iu, ou1))
            t2 = sig(ConvertTemperature(T, iu, ou2))
            t3 = sig(ConvertTemperature(T, iu, ou3))
            out.append((rdp(sig(T)), rdp(t1), rdp(t2), rdp(t3)))
        else:
            t1 = ConvertTemperature(T, iu, ou1)
            t2 = ConvertTemperature(T, iu, ou2)
            t3 = ConvertTemperature(T, iu, ou3)
            out.append((flt(T), t1, t2, t3))
    # Get maximum string width in any of the columns so we know the maximum column width
    w = 0
    for i in out:
        w = max(w, *[len(str(j)) for j in i])
    # Dump contents of out sequence
    if 0:
        from pprint import pprint as pp
        pp(out)
        exit()
    # Print report
    sep = " "*4     # Space between columns
    c = clr[iu]     # Color for each column
    def Header1():
        for i, letter in enumerate((iu, ou1, ou2, ou3)):
            print(f"{c[i]}{deg(letter):^{w}s}{t.N}{sep}", end="")
        print()
    def Header2():
        for i, letter in enumerate((iu, ou1, ou2, ou3)):
            print(f"{c[i]}{'─'*w:^{w}s}{t.N}{sep}", end="")
        print()
    Header1()
    Header2()
    if 0:
        fr = "{{:>{}s}}".format(w)
        fc = "{{:^{}s}}".format(w)
        for i, items in enumerate(out):
            if i:
                for j in items:
                    print(fr.format(j), sep, end=" ")
            else:
                for j in items:
                    print(fc.format(deg(j)), sep, end=" ")
            print()
    else:
        for i, items in enumerate(out):
            if i:   # First row already printed in Header()
                for j, k in enumerate(items):
                    print(f"{c[j]}{k!s:^{w}s}{sep}", end="")
                print()
    Header2()
    Header1()
