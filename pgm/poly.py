if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Calculate parameters of a regular polygon given the inscribed or
    # circumscribed circle diameter.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from fractions import Fraction
    use_sig = False
    if use_sig:
        from math import pi, sqrt, sin, cos, tan
    import sys
    import os
    import getopt
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    if use_sig:
        from sig import sig
    else:
        from f import flt, pi, sqrt, sin, cos, tan
    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import color
        have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw):
                pass
            def normal(self, *p, **kw):
                pass
            def __getattr__(self, name):
                pass
        color = Dummy()
        have_color = False
if 1:   # Global variables
    class g: pass
    g.width = int(os.environ.get("COLUMNS", 80)) - 1
    ii = isinstance
    highlight = color.lred
    if use_sig:
        sig.lead_zero = False
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] dia1 [dia2...]
      Print dimensions of regular polygons for given diameter(s) as either
      the inscribed or circumscribed circle diameter.  The diameters can
      be strings like '47', '4.7', '7/16', or '1-7/16'.
    Options:
      -c l  Color highlight the sides in the list l.  Needs optional color.py
            module.  [{d["-c"]}]
      -d n  Number of significant digits to print in report [{d["-d"]}]
      -n l  Define the number of sides to print; list l must be a
            comma-separated list of integers.  [{d["-n"]}]
      -t    Produce a table of useful factors allowing you to calculate
            various parameters of polygons given certain dimensions.
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-c"] = ""        # Which lines to highlight
    d["-d"] = 4         # Number of significant digits
    d["-n"] = "3,4,5,6,7,8,9,10"
    d["-t"] = False     # Print the table
    try:
        opts, diameters = getopt.getopt(sys.argv[1:], "c:d:n:t")
    except getopt.GetoptError as e:
        print(str(e))
        exit(1)
    for o, arg in opts:
        if o in ("-c",):
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
            d["-n"] = arg
        elif o in ("-t",):
            d["-t"] = not d["-t"]
    if use_sig:
        sig.digits = d["-d"]
    else:
        flt(0).n = d["-d"]
    if not d["-t"] and not diameters:
        Usage(d)
    # Convert d["-c"] to a set of integers
    s = d["-c"].split(",")
    d["-c"] = set([int(i) for i in s]) if s != [""] else set([])
    return diameters
def Convert(size):
    '''Convert the string size to a flt.  Can be an integer, flt,
    or fraction of e.g. the forms 7/8 or 1-7/8.
    '''
    if "/" in size:
        ip = 0
        num, denom = size.split("/")
        if "-" in num:
            ip, num = num.split("-")
        num, denom, ip = [int(i) for i in (num, denom, ip)]
        return flt(Fraction(num + ip*denom, denom))
    else:
        return flt(size)
def PrintTable(opts):
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
    if use_sig:
        # Use old printing method with sig
        fmt = "{{0:^{0}}}".format(3 + opts["-d"])
        print("{0:^2s}".format("n"), end=" ")
        for s in "T(deg) A/d^2 A/D^2 A/a^2 d/a D/a a/d a/D D/d".split():
            print(fmt.format(s), end=" ")
    else:
        # Use new printing methods with flt and Unicode.  There are 9
        # columns for flt and we want to fit into g.width if possible.
        f = lambda x: 4 + 9*x + 3
        while True:
            if f(w + 1) < g.width:
                w += 1
            else:
                break
        print(f"{'n':^2s}", end=" ")
        for s in "T(deg) A/d² A/D² A/a² d/a D/a a/d a/D D/d".split():
            print(f"{s:^{w}s}", end=" ")
    print()
    sizes = list(range(3, 11)) + [12, 15, 16, 20, 24, 32, 48, 60, 64]
    for n in sizes:
        escapes = have_color and n in opts["-c"]
        res = []
        K = pi/n
        res.append("{0:^2d}".format(n))
        if use_sig:
            res.append(fmt.format(sig(2*K*180/pi)))         # T
            res.append(fmt.format(sig(n*tan(K)/4)))         # A/d^2
            res.append(fmt.format(sig(n*sin(2*K)/8)))       # A/D^2
            res.append(fmt.format(sig(n/(tan(K)*4))))       # A/a^2
            doa, Doa = 1/tan(K), 1/sin(K)
            res.append(fmt.format(sig(doa)))                # d/a
            res.append(fmt.format(sig(Doa)))                # D/a
            res.append(fmt.format(sig(1/doa)))              # a/d
            res.append(fmt.format(sig(1/Doa)))              # a/D
            res.append(fmt.format(sig(Doa/doa)))            # D/d
        else:
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
        if escapes:
            color.fg(highlight)
        print(' '.join(res))
        if escapes:
            color.normal()
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
    exit(0)
def Poly(s, n, opts, circumscribed=False):
    '''Given the diameter in the string s, number of sides n, and
    options dictionary opts, calculate the parameters and print the
    table.
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
    assert ii(d, (flt, int, Fraction))
    assert ii(n, int)
    assert n > 0
    K = pi/n
    D = d/cos(K)
    if circumscribed:
        D = d
        d = D*cos(K)
    a = d*tan(K)
    A = n*a*d/4
    s = n*a
    escapes = have_color and n in opts["-c"]
    if escapes:
        color.fg(highlight)
    if use_sig:
        # The magic number 7 allows numbers such as 1.23e-100 to fit on
        # the line (i.e., you need more room than you think).
        fmt = "{{0:^{0}}}".format(7 + opts["-d"])
    for x in (n, d, D, a, A, s):
        if use_sig:
            print(fmt.format(sig(x)), end=" ")
        else:
            w = opts["-d"] + 3
            print(f"{x!s:^{w}s}", end=" ")
    if escapes:
        color.normal()
    print()
def Report(d, opts):
    '''Print the calculated values assuming the diameter string in d
    is first an inscribed diameter, then the circumscribed diameter.
    '''
    def Print(circumscribed=False):
        if use_sig:
            fmt = "{{0:^{0}}}".format(7 + opts["-d"])
        else:
            fmt = "{{0:^{0}}}".format(3 + opts["-d"])
        w = 3 + opts["-d"]
        for s in "Sides d D a Area Perim".split():
            print(f"{s:^{w}s}", end=" ")
        print()
        for n in number_of_sides:
            Poly(d, n, opts, circumscribed)
    try:
        number_of_sides = [int(i) for i in opts["-n"].split(",")]
    except Exception:
        Error("'{0}' is bad -n option".format(opts["-n"]))
    print("Size =", d, "[inscribed diameter]")
    Print(circumscribed=False)
    print("Size =", d, "[circumscribed diameter (distance across points)]")
    Print(circumscribed=True)
def Title():
    print(dedent('''
    Properties of regular polygons
      d = inscribed dia., D = circumscribed dia., a = length of side
    '''))
if __name__ == "__main__":
    opts = {}
    diameters = ParseCommandLine(opts)
    if opts["-t"]:
        PrintTable(opts)
    Title()
    for d in diameters:
        Report(d, opts)
        if len(diameters) > 1:
            print()
