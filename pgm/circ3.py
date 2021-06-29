'''
Find the radius of a circle given three points
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2013 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Find the radius of a circle given three points
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import string
    import sys
    import getopt
    from math import sqrt, cos, acos, sin
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from sig import sig
    from wrap import dedent
    try:
        from uncertainties import ufloat, ufloat_fromstr, UFloat
        from uncertainties.umath import sqrt, cos, acos, sin
        have_unc = True
    except ImportError:
        have_unc = False
if 1:   # Global variables
    ii = isinstance
def Det(a, b, c, d, e, f, g, h, i):
    '''Calculate a 3x3 determinant:
        | a b c |
        | d e f |
        | g h i |
    '''
    return a*(e*i - h*f) - b*(d*i - g*f) + c*(d*h - g*e)
def Circ3Points(x1, y1, x2, y2, x3, y3):
    '''Returns the radius of the circle that passes through the three
    points (x1, y1), (x2, y2), and (x3, y3).
    This is equations 30-34 from
    http://mathworld.wolfram.com/Circle.html.
    '''
    h1 = x1**2 + y1**2
    h2 = x2**2 + y2**2
    h3 = x3**2 + y3**2
    a = Det(x1, y1, 1, x2, y2, 1, x3, y3, 1)
    d = -Det(h1, y1, 1, h2, y2, 1, h3, y3, 1)
    e = Det(h1, x1, 1, h2, x2, 1, h3, x3, 1)
    f = -Det(h1, x1, y1, h2, x2, y2, h3, x3, y3)
    if not a:
        raise ValueError("Collinear points")
    if have_unc:
        if isinstance(a, UFloat) and not a.nominal_value:
            msg = "Collinearity:  an uncertain divisor is %s" % sig(a)
            raise ValueError(msg)
    r = sqrt((d**2 + e**2)/(4*a*a) - f/a)
    return r
def Circ3Dist(a, b, c):
    '''Given a triangle with sides a, b, c, returns the radius of the
    circle which passes through the three points.  This is turned into
    the circle from 3 points problem by putting the longest side on
    the x axis with one point at the origin.  Then use the cosine law
    to find the coordinates of the third point.
    '''
    c, b, a = sorted([a, b, c])
    # Now a is longest, b next, and c shortest
    x1, y1 = 0, 0
    x2, y2 = a, 0
    try:
        B = acos((a*a + c*c - b*b)/(2*a*c))
    except ValueError:
        raise ValueError("The three distances don't make a triangle")
    x3, y3 = c*cos(B), c*sin(B)
    return Circ3Points(x1, y1, x2, y2, x3, y3)
def Error(msg, status=1):
    print(msg, file=sys.stderr)
    exit(status)
def Usage(d, status=1):
    print(dedent(f'''
    Usage:  {sys.argv[0]} [options] [datafile]
      Print the radius of a circle given three points.  You can either
      give the distances between the three points or their Cartesian
      coordinates.  The points will be taken from the datafile given on
      the command line.  If you prefer, use the -i option and you'll be
      prompted for the input data.
     
      Lines allowed in the datafile must be:
        x, y            Defines a point in Cartesian coordinates
        a               Defines a distance
     
      If you use a line with a comma, then the program assumes that it and
      the following lines are Cartesian coordinates; there must be three
      such lines.
     
      Blank lines and lines that begin with a '#' after leading whitespace
      is removed are ignored.
    
      If you have the python uncertainties library (see
      http://packages.python.org/uncertainties), the entered numbers can have
      an associated uncertainty.  A number with uncertainty can then be entered
      with one of the equivalent notations:  3.2+-0.1,  3.2+/-0.1, 3.2±0.1, or
      3.2(1).
     
    Options:
        -d digits
            Set the number of significant digits for the report; this is used
            only if there are no uncertainties in the problem.  [{d["-d"]}]
        -i
            Prompt interactively for the input data.
    
    Examples/checks:
    
      1.  Enter the three sides 2, 1.41421356237, and 1.41421356237.  You
          should get a circle of radius 1.
    
      2.  Enter the points
            1.0(1), 0.0(1)
            -1.0(1), 0.0(1)
            0.0(1), 1.0(1)
          You should get a circle of radius 1.00(7); this means the
          circle's radius is 1 with a standard uncertainty of 0.07.
    '''))
    exit(status)
def ParseCommandLine(d):
    d["-d"] = 6
    d["-i"] = False
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:i")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for opt in optlist:
        if opt[0] == "-d":
            d["-d"] = int(opt[1])
            if d["-d"] < 1:
                Error("-d option must be integer > 0")
        if opt[0] == "-i":
            d["-i"] = True
            return None
    if len(args) != 1:
        Usage(d)
    sig.digits = d["-d"]
    return args[0]
def GetNumber(prompt):
    '''Return a float or ufloat, depending on what the user types in.
    '''
    while True:
        s = input(prompt)
        t = s.replace("+-", "+/-")
        t = s.replace("\xb1", "+/-")
        try:
            if "+/-" in t or ("(" in t and ")" in t):
                x = ufloat_fromstr(t)
            else:
                x = float(t)
            return x
        except Exception:
            print("'{}' is not a proper number".format(s))
def GetDataInteractively(d):
    order = ["first", "second", "third"]
    while True:
        s = input("Enter distances [d] or points (p)?  ").strip().lower()
        if not s:
            s = "d"
            break
        elif s in set("dpq"):
            break
    if s == "q":
        exit(0)
    if s == "d":
        # Distances
        dist = [0, 0, 0]
        for i in range(3):
            x = GetNumber("Enter the {} distance:  ".format(order[i]))
            dist[i] = x
        d["distances"] = dist
    else:
        # Points
        coord = [0, 0, 0]
        print("  Note:  enter points as two numbers 'x, y' separated "
              "by a comma")
        for i in range(3):
            while True:
                s = input("Enter the {} point:  ".format(order[i]))
                if s == "q":
                    exit(0)
                try:
                    f = s.split(",")
                    if len(f) != 2:
                        print("Your input must have only one comma")
                    else:
                        x = InterpretNum(f[0])
                        y = InterpretNum(f[1])
                        coord[i] = (x, y)
                        break
                except Exception:
                    pass
        d["coordinates"] = coord
    print()
def InterpretNum(s):
    '''Return a float or ufloat from the string s.
    '''
    t = s.replace("+-", "+/-")
    t = t.replace("\xb1", "+/-")
    t = t.replace("\xc2", "")    # Hack for python 2.7
    if "+/-" in t or ("(" in t and ")" in t):
        return ufloat_fromstr(t)
    return float(t)
def ReadDatafile(datafile, d):
    lines = [i.strip() for i in open(datafile).readlines()]
    dist, coord = [], []
    e = Exception("Can't mix distances and coordinates")
    try:
        for i, line in enumerate(lines):
            linenum = i + 1
            if not line or line[0] == "#":
                continue
            if "," in line:
                # Coordinate
                f = line.split(",")
                if len(f) != 2:
                    msg = "Line {} in datafile '{}' doesn't have 2 coordinates"
                    Error(msg.format(linenum, datafile))
                x = InterpretNum(f[0])
                y = InterpretNum(f[1])
                coord.append((x, y))
                if dist:
                    raise e
            else:
                dist.append(InterpretNum(line))
                if coord:
                    raise e
        if coord:
            d["coordinates"] = coord
        elif dist:
            d["distances"] = dist
    except Exception as e:
        msg = "Line %d is bad in datafile '%s'\n" % (linenum, datafile)
        msg += "  Line:  '%s'\n" % line
        msg += "  Error:  %s" % str(e)
        Error(msg)
def Coordinates(d):
    (x1, y1), (x2, y2), (x3, y3) = d["coordinates"]
    try:
        r = Circ3Points(x1, y1, x2, y2, x3, y3)
        s = [(x1, y1), (x2, y2), (x3, y3)]
        return r, s
    except Exception as e:
        X1, Y1 = sig(x1), sig(y1)
        X2, Y2 = sig(x2), sig(y2)
        X3, Y3 = sig(x3), sig(y3)
        err = str(e)
        msg = dedent(f'''
        Couldn't calculate radius from coordinates:
            {X1}, {Y1}
            {X2}, {Y2}
            {X3}, {Y3}
        Error:  {err}''')
        Error(msg)
def Distances(d):
    a, b, c = d["distances"]
    try:
        return Circ3Dist(a, b, c), (a, b, c)
    except Exception as e:
        Error(str(e))
def Report(r, s, d):
    prob_type = "three distances" if isinstance(s, tuple) else "three points"
    print("Circle from {prob_type}:".format(**locals()))
    if isinstance(s, tuple):
        print("  Distances:")
        for i in s:
            print("    ", sig(i))
    else:
        indent, w = " "*4, 16
        print(indent, "{0:^{1}}".format("x", w), "{0:^{1}}".format("y", w))
        h = "{0:>{1}}".format("-"*w, w)
        print(indent, h, h)
        for x, y in s:
            X = "{:.1fS}".format(x) if ii(x, UFloat) else sig(x)
            Y = "{:.1fS}".format(y) if ii(y, UFloat) else sig(y)
            sx = "{:>{}s}".format(X, w)
            sy = "{:>{}s}".format(Y, w)
            print("    ", sx, sy)
    print("\nRadius of circle   =", sig(r))
    print("Diameter of circle =", sig(2*r))
if __name__ == "__main__":
    d = {}      # Options dictionary
    datafile = ParseCommandLine(d)
    if d["-i"]:
        GetDataInteractively(d)
    else:
        ReadDatafile(datafile, d)
    if "coordinates" in d:
        r, s = Coordinates(d)
    else:
        r, s = Distances(d)
    Report(r, s, d)
