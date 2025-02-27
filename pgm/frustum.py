if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2016, 2021 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Dimensions of a cylindrical frustum planar development
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import getopt
    import sys
if 1:  # Custom imports
    from wrap import dedent
    from f import flt, pi, atan, sqrt, cos, degrees
    from get import GetNumber


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    digits = d["-d"]
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] a b h
      Given a cylindrical frustum with end diameters a and b and height h,
      calculate the components of its planar development.  If you enter no
      parameters, you'll be prompted for the required data.
    Options:
      -d n      Set number of significant digits.  [{d["-d"]}]
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-d"] = 4  # Number of significant digits
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
                msg = "-d option's argument must be an integer between 1 and 15"
                Error(msg)
        elif o in ("-h",):
            Usage(0)
    flt(0).n = d["-d"]
    return args


def Calculate(d):
    r2d = 180 / pi
    a = d["large_dia"]
    b = d["small_dia"]
    h = d["h"]
    if a == b:
        Error("Not a frustum")
    # Make a be the large diameter
    if a < b:
        a, b = b, a
    if not (a > 0 and b > 0 and h > 0):
        raise ValueError("Parameters must be > 0")
    r = sqrt(b * b / 4 + (b * h / (a - b)) ** 2)
    R = sqrt(a * a / 4 + (a * h / (a - b)) ** 2)
    theta = atan((a - b) / h)
    phi = pi * a / R
    AB = pi * a
    CD = pi * b
    alpha = sqrt(2 * (1 - cos(phi)))
    # Print report
    print(
        dedent(f"""
    Given
        Diameter 1 = {a}
        Diameter 2 = {b}
        h = height of frustum = {h}
        Included angle = {degrees(2 * theta)}°
    Development:
        theta = frustum half-angle = {degrees(theta)}° = {theta} radians
        phi   = development angle  = {degrees(phi)}° = {phi} radians
        r = small radius = {r}            (arc length = {CD})
        R = large radius = {R}            (arc length = {AB})
        Divider setting for small arc = {r * alpha}
        Divider setting for large arc = {R * alpha}
    """)
    )
    exit(0)


def GetArgs(d):
    """Put the arguments into the options dictionary d."""
    print(
        dedent(f"""
    Print the planar development information for a conical frustum.

    Choose which problem to solve:
      1) Given height and both diameters
      2) Given height, small diameter, and included angle
      3) Given height, large diameter, and included angle""")
    )
    d["problem_type"] = GetNumber("Problem? ", default=1, numtype=int, low=1, high=3)
    d["h"] = flt(GetNumber("Height? ", default=1, low=0, low_open=True))
    if d["problem_type"] == 1:
        d["small_dia"] = flt(
            GetNumber("Small diameter? ", default=1, low=0, low_open=True)
        )
        d["large_dia"] = flt(
            GetNumber("Large diameter? ", default=d["small_dia"], low=0, low_open=True)
        )
    elif d["problem_type"] == 2:
        d["small_dia"] = flt(
            GetNumber("Small diameter? ", default=1, low=0, low_open=True)
        )
        d["theta_deg"] = flt(
            GetNumber("Included angle in degrees? ", default=10, low=0, low_open=True)
        )
    else:
        d["large_dia"] = flt(
            GetNumber("Large diameter? ", default=d["small_dia"], low=0, low_open=True)
        )
        d["theta_deg"] = flt(
            GetNumber("Included angle in degrees? ", default=10, low=0, low_open=True)
        )


if __name__ == "__main__":
    d = {}
    args = ParseCommandLine(d)
    if not args:
        args = GetArgs(d)
    else:
        a, b, h = [float(i) for i in args]
        d["h"] = h
        if a < b:
            d["small_dia"] = a
            d["large_dia"] = b
        else:
            d["small_dia"] = b
            d["large_dia"] = a
    Calculate(d)
