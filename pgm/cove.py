"""
TODO:
    * -i option doesn't work

    Calculate the angle to set a table saw fence to cut a cove.  See
    cove.pdf for more details.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2009, 2014 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Cut a cove with a table saw
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import os
    import getopt
    from math import sqrt, acos, atan, pi, tan
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent
if 1:  # Global variables
    d2r = pi / 180
    r2d = 1 / d2r
    in2mm = 25.4
    mm2in = 1 / in2mm
    # For convenience, you can set the following global variables to the
    # dimensions of your table saw.  All internal calculations are done in
    # mm; use the in2mm and mm2in conversion factors as needed.
    Diameter = 10 * in2mm  # Diameter of saw blade
    Kerf_width = 0.093 * in2mm  # Width of blade's kerf
    X_width = 23.6 * in2mm  # X width of table saw top


def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)


def Usage(d, status=1):
    name = sys.argv[0]
    units = "mm" if d["-m"] else "inches"
    iunits = "inches" if d["-m"] else "mm"
    print(
        dedent(f"""
    Usage:  {name}  [options]  width  height
      Prints the fence angle (with respect to the blade rotation axis)
      needed for a table saw to cut a cove of specified dimensions.  The
      input units are {units} unless you use the -m option.
     
      width is the width of the cove at the surface of the workpiece.
      height is the depth of the cove (i.e., how high above the table
      you'll set the blade to make the deepest part of the cut).
     
    Options:
      -d diam                       [Default = {d["-d"] * mm2in:.2f} inches]
          Sets the diameter of the saw blade.  Since you'll probably use
          the program with one saw blade size, you can set the Diameter
          global variable to your saw blade's diameter for convenience.
      -i
          Include instructions for cutting the cove.
      -k kerf_width                 [Default = {d["-k"] * mm2in:.3f} inches]
          Set the kerf width of the blade.
      -m
          Set the input units to {iunits}.
      -x X_width                    [Default = {d["-x"] * mm2in:.2f} inches]
          Set the X dimension for your table saw.  See the cove.pdf
          document for an explanation.
    """)
    )
    exit(status)


def ParseCommandLine(d):
    d["-d"] = Diameter
    d["-i"] = False
    d["-k"] = Kerf_width
    d["-m"] = False  # Use metric dimensions by default if True
    d["-x"] = X_width
    try:
        optlist, args = getopt.getopt(sys.argv[1:], "d:ik:mx:")
    except getopt.GetoptError as str:
        msg, option = str
        print(msg)
        sys.exit(1)
    is_first = True
    for opt in optlist:
        if opt[0] == "-d":
            if d["-m"]:
                d["-d"] = float(opt[1])
            else:
                d["-d"] = float(opt[1]) * in2mm
            if d["-d"] <= 0:
                Error("Blade diameter must be > 0")
        elif opt[0] == "-k":
            if d["-m"]:
                d["-k"] = float(opt[1])
            else:
                d["-k"] = float(opt[1]) * in2mm
            if d["-k"] <= 0:
                Error("Kerf width must be > 0")
        elif opt[0] == "-m":
            d["-m"] = not d["-m"]
            if not is_first:
                Error("-m option must be the first argument if it is used")
        elif opt[0] == "-x":
            if d["-m"]:
                d["-x"] = float(opt[1])
            else:
                d["-x"] = float(opt[1]) * in2mm
            if d["-x"] <= 0:
                Error("X width must be > 0")
        is_first = False
    if len(args) != 2:
        Usage(d)
    return args


def Circle(x, D, L, delta, neg_threshold=1e-8):
    """Given the Cartesian x position, calculate the y value for a
    circle that fits through the three points
    P1  (D/2 - delta,  L/2)
    P2  (D/2 - delta, -L/2)
    P3  (D/2, 0)
    """
    # This formula was derived using sympy to expand the
    # Vandermonde-like determinant used to get the equation for a
    # circle through three non-collinear points.  See Schmall, C.,
    # "A First Course in Analytical Geometry", 2nd ed., van
    # Nostrand, 1921.
    assert 0 <= x <= D / 2
    y = (
        sqrt(
            -4 * D**2
            + 2 * D * L**2 / delta
            + 8 * D * delta
            + 16 * D * x
            - 4 * L**2 * x / delta
            - 16 * delta * x
            - 16 * x**2
        )
        / 4
    )
    if y < 0:
        # Probably caused by roundoff
        if abs(y) < neg_threshold:
            y = abs(y)
        else:
            raise ValueError("Circle:  complex for delta = {0}".format(delta))
    return y


def Ellipse(x, D, L, delta, neg_threshold=1e-8):
    """Given the Cartesian x position, calculate the y value for an
    ellipse with major diameter D that fits through the three points
    P1  (D/2 - delta,  L/2)
    P2  (D/2 - delta, -L/2)
    P3  (D/2, 0)
    """
    # Derived from the Cartesian equation for an ellipse (x/a)**2 +
    # (y/b)**2 = 1.  Insert the point P1 and solve for b (a is equal to
    # D/2).
    assert 0 <= x <= D / 2
    y = L / 4 * sqrt((D**2 - 4 * x**2) / (delta * (D - delta)))
    if y < 0:
        # Probably caused by roundoff
        if abs(y) < neg_threshold:
            y = abs(y)
        else:
            raise ValueError("Ellipse:  complex for delta = {0}".format(delta))
    return y


def GetFenceAngle(d):
    """Return the angle in radians of the fence needed to cut this cove
    approximation in the entry d["angle_rad"].  All variables are
    assumed to be in mm.
    """
    D, eps, L, delta = d["-d"], d["-k"], d["width_mm"], d["height_mm"]
    w = 2 * sqrt(delta * (D - delta))
    A = L / sqrt(w**2 + eps**2)
    if A > 1:
        Error("Problem not solvable for given dimensions")
    d["angle_rad"] = acos(A) + atan(eps / w)
    d["angle_deg"] = d["angle_rad"] * r2d


def GetProblemDimensions(args, d):
    msg = "{0} is a bad value for the width".format(args[0])
    try:
        d["width_mm"] = float(args[0])
    except Exception:
        Error(msg)
    else:
        if d["width_mm"] <= 0:
            Error(msg)
    msg = "{0} is a bad value for the height".format(args[1])
    try:
        d["height_mm"] = float(args[1])
    except Exception:
        Error(msg)
    else:
        if d["height_mm"] <= 0:
            Error(msg)
    if not d["-m"]:
        # Convert to mm
        d["width_mm"] *= in2mm
        d["height_mm"] *= in2mm


def MaximumDeviation(d, n=50):
    """Calculate the maximum deviation in mm between a cove made from a
    circle and the ellipse approximation produced on the table saw.
    """
    D, L, delta = d["-d"], d["width_mm"], d["height_mm"]
    x0, dx, diff = D / 2 - delta, delta / n, []
    for i in range(n):
        x = x0 + i * dx
        ycirc = Circle(x, D, L, delta)
        yell = Ellipse(x, D, L, delta)
        diff.append(abs(ycirc - yell))
    d["max_diff_mm"] = max(diff)


def Report(d):
    D_mm, D_in = d["-d"], d["-d"] * mm2in
    w_mm, w_in = d["width_mm"], d["width_mm"] * mm2in
    h_mm, h_in = d["height_mm"], d["height_mm"] * mm2in
    k_mm, k_in = d["-k"], d["-k"] * mm2in
    theta_rad, theta_deg = d["angle_rad"], d["angle_deg"]
    X_mm, X_in = d["-x"], d["-x"] * mm2in
    t = tan(theta_rad)
    Y_mm, Y_in = X_mm / t, X_in / t
    d_mm, d_in = d["max_diff_mm"], d["max_diff_mm"] * mm2in
    # Number of decimal places for inches and mm
    n, m = 3, 2
    w = 8  # Width of decimal number
    print(
        dedent(f"""
    Cutting a cove:
      Blade diameter       {D_in:{w}.{n}f} in {D_mm:{w}.{m}f} mm
      Cove width           {w_in:{w}.{n}f} in {w_mm:{w}.{m}f} mm
      Cove height          {h_in:{w}.{n}f} in {h_mm:{w}.{m}f} mm
      Kerf width           {k_in:{w}.{n}f} in {k_mm:{w}.{m}f} mm
      X dimension          {X_in:{w}.{n}f} in {X_mm:{w}.{m}f} mm
      Y dimension          {Y_in:{w}.{n}f} in {Y_mm:{w}.{m}f} mm
      Max diff from circle {d_in:{w}.{n}f} in {d_mm:{w}.{m}f} mm
      Fence angle (theta)  {theta_deg:{w}.2f}° = atan(X/Y)
                           {theta_rad:{w}.4f} radians
    """)
    )


if __name__ == "__main__":
    d = {}  # Options dictionary
    args = ParseCommandLine(d)
    GetProblemDimensions(args, d)
    GetFenceAngle(d)
    MaximumDeviation(d)
    Report(d)
if 0:
    # Manually-calculated test case for fence angle.  Dimensions in mm.
    d = {"-d": 250, "-k": 2, "height_mm": 5, "width_mm": 50}
    GetFenceAngle(d)
    assert abs(d["angle_deg"] - 46.075734) < 1e-6
    exit()
