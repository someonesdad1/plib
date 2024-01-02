'''

ToDo
    - Allow parameters to have uncertainty
    - Add -i option for interactive solution
        - Variables:
            - n = number of sides
            - θ = central angle
            - β = interior angle between sides
            - s = length of side
            - p = perimeter
            - A = area
            - r = radius for inscribed circle
            - R = radius for circumscribed circle
            - d = diameter for inscribed circle
            - D = diameter for circumscribed circle
        - Here are the functions given in the analytic geometry document
            - ρ means one of r, R, d, D
            - θ(n)
            - β(n)
            - s(ρ, n)
            - p(s, n)
            - A(s, n), A(ρ, n)
            - r(s, n), r(R, n)
            - d(s, n), d(D, n)

'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Calculate parameters of a regular polygon
        #∞what∞#
        #∞test∞# #∞test∞#
    # Standard imports
        from fractions import Fraction
        import sys
        import os
        import getopt
    # Custom imports
        from wrap import dedent
        from lwtest import Assert
        from color import TRM as t
        from f import flt, pi, sqrt, sin, cos, tan
        from uncertainties import ufloat, ufloat_fromstr, UFloat
    # Global variables
        class g:
            pass
        g.width = int(os.environ.get("COLUMNS", 80)) - 1
        ii = isinstance
        isatty = sys.stdout.isatty()
        t.ti = t("ornl") if isatty else ""
        t.hi = t("yell") if isatty else ""
        t.insc = t("purl") if isatty else ""
        t.circ = t("trq") if isatty else ""
        t.nn = t.n if isatty else ""
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] dia1 [dia2...]
          Print dimensions of regular polygons for given diameter(s) as either
          the inscribed or circumscribed circle diameter.  The diameters can
          be strings like '47', '4.7', '7/16', or '1-7/16'.
 
          You can also use words like 'triangle', 'hexagon', etc. to
          identify the polygon(s) you're interested in.  The first three
          letters of the word are what are used for identification.  Thus,
          '{sys.argv[0]} 1.3 tri' causes the script to print out results
          for a triangle only.
        Options:
          -a    Abbreviate numbers [{d['-a']}]
          -c l  Color highlight the sides in the list l [{d["-c"]}]
          -d n  Number of significant digits to print [{d["-d"]}]
          -n l  Which sides to print; must be a comma-separated list of
                integers or a range() call.  [{d["-n"]}]
          -t    Produce a table of useful factors allowing you to calculate
                various parameters of polygons given certain dimensions.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Abbreviate numbers
        d["-c"] = ""        # Which lines to highlight
        d["-d"] = 4         # Number of significant digits
        d["-n"] = ",".join(str(i) for i in range(3, 13))
        d["-t"] = False     # Print the table
        try:
            opts, diameters = getopt.getopt(sys.argv[1:], "ac:d:n:t")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, arg in opts:
            if o[1] in "at":
                d[o] = not d[o]
            elif o in ("-c",):
                d["-c"] = arg
            elif o in ("-d",):
                try:
                    d["-d"] = int(arg)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-n",):
                if "range" in arg:
                    d["-n"] = ','.join(str(i) for i in list(eval(arg)) if i > 2)
                else:
                    d["-n"] = arg
        x = flt(0)
        x.N = d["-d"]
        x.rtz = x.rtdp = False
        if d["-a"]:
            x.rtz = x.rtdp = True
        x.low = 1e-4
        x.high = 1e6
        if not d["-t"] and not diameters:
            Usage(d)
        # Convert d["-c"] to a set of integers
        if d["-c"]:
            s = d["-c"].split(",")
            d["-c"] = set([int(i) for i in s])
        else:
            d["-c"] = set([3, 6])
        return diameters
if 1:   # Core functionality
    def Convert(size):
        '''Convert the string size to a flt or ufloat.  Can be an integer, flt,
        or fraction of e.g. the forms 7/8 or 1-7/8.  A ufloat can be either
        '1+-.1' or '1.0(1)' forms.
        '''
        if "/" in size:
            ip = 0
            num, denom = size.split("/")
            if "-" in num:
                ip, num = num.split("-")
            num, denom, ip = [int(i) for i in (num, denom, ip)]
            return flt(Fraction(num + ip*denom, denom))
        elif "+-" in size:
            return ufloat_fromstr(size.replace("+-", "+/-"))
        elif "±" in size:
            return ufloat_fromstr(size)
        elif "(" in size and ")" in size:
            return ufloat_fromstr(size)
        else:
            return flt(size)
    def PrintFormulaTable():
        '''Print a table similar to the table on page 1-39 of Mark's
        "Standard Handbook for Mechanical Engineers", 7th ed., 1967.
        '''
        def F(x, w=None):
            '''str of flt x with leading 0 removed.  If w is not None, it's a
            width to center the string of x in.
            '''
            s = str(x)
            if s[0] == "0" and s[1] == ".":
                s = s[1:]
            if w is None:
                return s
            return f"{s:^{w}s}"
        # Check of formulas:  I drew a 6" diameter circle and used a
        # 30-60-90 triangle to draw a hexagon around it.  The measurements
        # agreed with the values calculated with the table to better than
        # 0.1%.
        print(dedent('''
        Regular polygons
        d = inscribed circle diameter, D = circumscribed circle diameter, A = area,
        s = perimeter, a = length of one side, T = angle subtended by side
        '''))
        # Width of printout:  the column for n is 2 wide and the remaining 9
        # columns are the width of a flt at current significance.  The smallest
        # number (and thus the longest) will be a/D for n=64.  This thus
        # defines the width w for each column.
        s = F(sin(pi/64))
        w = len(s)
        # Use new printing methods with flt and Unicode.  There are 9
        # columns for flt and we want to fit into g.width if possible.
        def f(x):
            return 4 + 9*x + 3
        while True:
            if f(w + 1) < g.width:
                w += 1
            else:
                break
        print(f"{'n':^2s}", end=" ")
        for s in "T(deg) A/d² A/D² A/a² d/a D/a a/d a/D D/d".split():
            print(f"{s:^{w}s}", end=" ")
        print()
        # Get which sizes to print
        if opts["-n"]:
            sizes = list(sorted(int(i) for i in opts["-n"].split(",")))
        else:
            sizes = list(range(3, 11)) + [12, 15, 16, 20, 24, 32, 48, 60, 64]
        for n in sizes:
            colorize = n in opts["-c"]
            res = []
            K = pi/n
            res.append("{0:^2d}".format(n))
            res.append(F(2*K*180/pi, w))         # T
            res.append(F(n*tan(K)/4, w))         # A/d^2
            res.append(F(n*sin(2*K)/8, w))       # A/D^2
            res.append(F(n/(tan(K)*4), w))       # A/a^2
            doa, Doa = 1/tan(K), 1/sin(K)
            res.append(F(doa, w))                # d/a
            res.append(F(Doa, w))                # D/a
            res.append(F(1/doa, w))              # a/d
            res.append(F(1/Doa, w))              # a/D
            res.append(F(Doa/doa, w))            # D/d
            if colorize:
                print(f"{t.hi}", end="")
            print(' '.join(res))
            if colorize:
                print(f"{t.nn}", end="")
        if 1:   # Print formulas
            print()
            print(dedent('''
            Formulas:
            k = π/n                           T = 360*k/π
            a/d = tan(k)                      A/d² = n*tan(k)/4
            a/D = sin(k)                      A/D² = n*sin(2*k)/8
            D/d = 1/cos(k)                    A/a² = 4*n/tan(k)
    
            a = d*tan(k) = D*sin(k)
            r = d/2 = sqrt(R² - a²/4) = a/(tan(k)*2) = R*cos(k)
            R = D/2 = sqrt(r² + a²/4) = a/(sin(k)*2) = r/cos(k)
            A = n*a*r/2 = n*a/2*sqrt((D² - a²)/4)
                = n*a²*cot(k)/4 = n*r²*tan(k) = n*R²*sin(2*k)/2
            s = 2*sqrt(R^2 - r^2) = 2*r*tan(k)
            ''', n=4))
        print('\nRef:  Marks, "Std Hdbk for Mech Engrs", pg 1-39, 7th ed., 1967')
        exit(0)
    def Title():
        print(dedent(f'''
        {t.ti}Properties of regular polygons to {opts["-d"]} figures{t.nn}
            d = inscribed diameter
            D = circumscribed diameter
            a = length of side
        '''))
    def Poly(s, n, circumscribed=False, leave_out=""):
        '''Given the diameter in the string s, number of sides n, and
        options dictionary opts, calculate the parameters and print the
        table.  Leave out the indicated column (only will be d or D).
        -----------------
        Definitions are:
            d = inscribed circle diameter
            D = circumscribed circle diameter
            s = perimeter
            A = area or surface area
            a = length of side
            r = radius of inscribed circle = d/2
            R = radius of circumscribed circle = D/2
            n = number of sides
        Equations are:
            theta = 2*pi/n = central angle subtended by side
            K = theta/2
            a = length of side = d*tan(K) = D*sin(K)
            r = sqrt(R^2 - a^2/4) = a*cot(K)/2 = R*cos(K)
            R = sqrt(r^2 + a^2/4) = a*csc(K)/2 = r*sec(K) = r/cos(K)
            A = n*a*r/2 = n*a/2*sqrt((D^2 - a^2)/4)
            = n*a^2*cot(K)/4 = n*r^2*tan(K) = n*R^2*sin(2*K)/2
            s = 2*sqrt(R^2 - r^2) = 2*r*tan(K)
        '''
        try:
            d = Convert(s)
        except Exception:
            Error(f"'{s}' is not a valid number")
        Assert(ii(d, (flt, int, Fraction, UFloat)))
        Assert(ii(n, int))
        Assert(n > 0)
        K = pi/n
        D = d/cos(K)
        if circumscribed:
            D = d
            d = D*cos(K)
        a = d*tan(K)
        A = n*a*d/4
        s = n*a
        colorize = n in opts["-c"]
        if colorize:
            print(f"{t.hi}", end="")
        if leave_out == "d":
            L = (n, D, a, A, s)
        elif leave_out == "D":
            L = (n, d, a, A, s)
        else:
            Error(f"Program bug: leave_out = {leave_out!r}")
        # Now print the line
        for x in L:
            w = opts["-d"] + 5
            if ii(x, UFloat):
                print(f"{x:^{w}.1uS}", end=" ")
            else:
                print(f"{x!s:^{w}s}", end=" ")
        if colorize:
            print(f"{t.nn}", end="")
        print()
    def Report(dstr):
        '''Print the calculated values assuming the diameter string in dstr
        is first an inscribed diameter, then the circumscribed diameter.
        '''
        def Header(circumscribed=False, leave_out=""):
            w = opts["-d"] + 5
            for s in "Sides d D a Area Perim".split():
                if s == leave_out:
                    continue
                print(f"{s:^{w}s}", end=" ")
            print()
            for n in number_of_sides:
                Poly(dstr, n, circumscribed, leave_out=leave_out)
        try:
            number_of_sides = [int(i) for i in opts["-n"].split(",")]
        except Exception:
            Error("'{0}' is bad -n option".format(opts["-n"]))
        try:
            dia = Convert(dstr)
        except Exception:
            breakpoint() #xx
            dia = flt(eval(dstr))
            pass
        if 1:   # Print inscribed diameter
            print(f"\n{t.insc}d = {dstr!r} = {dia} = inscribed diameter{t.nn}")
            print(f"    {t.insc}r = {dia/2} = inscribed radius{t.nn}")
            Header(circumscribed=False, leave_out="d")
        if 1:   # Print circumscribed diameter
            print(f"\n{t.circ}D = {dstr!r} = {dia} = circumscribed diameter (distance across points){t.nn}")
            print(f"    {t.circ}R = {dia/2} = circumscribed radius{t.nn}")
            Header(circumscribed=True, leave_out="D")
    def LookForWords(diameters):
        '''Look for strings like 'tri', 'quad', etc. in the list of
        diameters and set the appropriate values in the -n option.  Remove
        these words and return the resultant remaining diameters.
        '''
        words = "tri tet qua pen hex hep sep oct non dec dod".split()
        nums = {
            "tri": 3, "tet": 4, "qua": 4, "pen": 5, "hex": 6, "hep": 7,
            "sep": 7, "oct": 8, "non": 9, "dec": 10, "dod": 12,
        }
        found, dia = [], []
        for d in diameters:
            got_one = False
            for word in words:
                if d.startswith(word):
                    found.append(nums[word])
                    got_one = True
                    break
            if not got_one:
                dia.append(d)
        if 0:
            print(f"diameters = {diameters}")
            print(f"found = {found}")
            print(f"dia   = {dia}")
            exit()
        if found:
            opts["-n"] = ','.join(str(i) for i in found)
        return dia
        
if __name__ == "__main__":
    opts = {}
    diameters = ParseCommandLine(opts)
    diameters = LookForWords(diameters)
    # Make sure we can convert the diameters
    for dia in diameters:
        try:
            Convert(dia)
        except Exception:
            Error(f"'{dia}' is not a valid number")
    if opts["-t"]:
        PrintFormulaTable()
    Title()
    for d in diameters:
        Report(d)
        if len(diameters) > 1:
            print()
