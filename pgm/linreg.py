"""
Produces a linear regression on a stream of data from stdin.
The input data format is two real numbers per line; the first
number is the x value and the second number is the y value.

The output gives the regression statistics and the residuals.  The
section with the residuals is output in a form suitable for input
into xgraph.
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # 2D linear regression tool
    ##∞what∞#
    ##∞test∞# #∞test∞#
    pass
if 1:  # Imports
    import sys
    import getopt

    # from math import sqrt
    from pdb import set_trace as xx
if 1:  # Custom imports
    from wrap import dedent

    # from sig import sig
    from f import sqrt, flt
if 1:  # Global variables
    # Sums and sums of squares
    sx = sxx = sy = syy = sxy = 0.0
    n, m = 0, sys.float_info.max
    xmin, ymin = m, m
    xmax, ymax = -m, -m
    # The input arrays for data
    X, Y = [], []


def ProcessData():
    "Calculate the needed sums"
    global sx, sxx, sy, syy, sxy, n
    global xmin, ymin, xmax, ymax
    if n < 2:
        raise ValueError("Not enough data points")
    if len(X) != len(Y):
        raise ValueError("Unequal arrays")
    for i in range(n):
        x, y = X[i], Y[i]
        sx += x
        sxx += x * x
        sy += y
        syy += y * y
        sxy += x * y
        xmin = min(x, xmin)
        ymin = min(y, ymin)
        xmax = max(x, xmax)
        ymax = max(y, ymax)


def CalculateRegression():
    """Calculate regression statistics and return them in a dictionary."""
    dict = {}
    slope = (n * sxy - sx * sy) / (n * sxx - sx * sx)
    dict["slope"] = slope
    dict["intercept"] = (sy - slope * sx) / n
    dict["r"] = slope * sqrt((n * sxx - sx * sx) / (n * syy - sy * sy))
    return dict


def ProcessLine(line, line_count, file):
    """Split the line into two tokens and return them as an (x, y) tuple."""
    nums = line.strip().split()
    if len(nums) != 2:
        print("Line %d of file '%s' not of proper form:" % (line_count, file))
        print("  '%s'" % line.strip())
        sys.exit(1)
    return [flt(i) for i in nums]


def ReadStream(fp, filename):
    global X, Y, n
    lines = fp.readlines()
    line_count = 0
    for line in lines:
        line_count += 1
        line = line.strip()
        if not line or line[0] == "#":
            continue
        x, y = ProcessLine(line, line_count, filename)
        X.append(x)
        Y.append(y)
        n = n + 1


def GetData(files):
    "Read in the data and put it into the data arrays X and Y"
    for file in files:
        fp = sys.stdin if file == "-" else open(file)
        ReadStream(fp, file)
        fp.close()
    if not X or not Y:
        print("No data read in")
        exit(1)


def PrintResiduals(d):
    print(
        dedent(f"""
    Residuals
         i                y                    ŷ                  %dev
    ----------    -----------------    -----------------    ------------------
    """)
    )
    slope = d["slope"]
    intercept = d["intercept"]
    w = 20
    for i in range(n):
        x, y = X[i], Y[i]
        ŷ = slope * x + intercept  # Predicted value
        residual = ŷ - y
        print(f"{i + 1:^12d} ", end="")
        print(f"{y!s:^{w}s} ", end="")
        print(f"{ŷ!s:^{w}s} ", end="")
        if y:
            pct = str(100 * residual / y) + "%"
            print(f"{pct:^{w}s}")
        else:
            print(f"{'--':^{w}s}")


def Usage(status=1):
    name = sys.argv[0]
    print(
        dedent(f"""
    Usage:  {sys.argv[0]} [options] [file1 [file2...]]
      Calculate the simple linear regression on the data given in the
      files (use "-" for stdin).  There must be two numbers separated
      by spaces on each line; comments beginning with '#' as the first
      non-space characters are ignored, as are empty lines.
    Options:
      -d n      Number of significant figures to use [{d["-d"]}]
      -h        Print this help
    """)
    )
    exit(status)


def PrintData():
    v, w = 13, 19
    print(
        dedent(f"""
    Data:
          i                  x                   y
    {"-" * v:^{v}s}    {"-" * w:^{w}s} {"-" * w:^{w}s}
    """)
    )
    for i in range(n):
        x, y = X[i], Y[i]
        print(f"{i:^{v}d}    {x!s:^{w}s}{y!s:^{w}s}")


def PrintResults(reg):
    if d["-v"]:
        print()
    slope, intercept, r = reg["slope"], reg["intercept"], reg["r"]
    x_mean = sx / n
    y_mean = sy / n
    xs = sqrt((sxx - n * (sx / n) ** 2) / (n - 1))
    ys = sqrt((syy - n * (sy / n) ** 2) / (n - 1))
    w = 18
    print(
        dedent(f"""
    Linear regression results:
      {n} points
      Slope     = {slope}
      Intercept = {intercept}
      R         = {r}
                           x                    y
      {"Mean":4s}         {sx / n!s:^{w}s}  {sy / n!s:^{w}s}
      {"s":4s}         {xs!s:^{w}s}  {ys!s:^{w}s}
      {"min":4s}         {xmin!s:^{w}s}  {ymin!s:^{w}s}
      {"max":4s}         {xmax!s:^{w}s}  {ymax!s:^{w}s}

    """)
    )


def ParseCommandLine(d):
    d["-d"] = 3  # Significant figures
    d["-v"] = False  # Print data
    try:
        optlist, files = getopt.getopt(sys.argv[1:], "d:hv")
    except getopt.GetoptError as e:
        msg, option = e
        print(msg)
        exit(1)
    for o, a in optlist:
        if o == "-d":
            d["-d"] = int(a)
        elif o == "-h":
            Usage(status=0)
        elif o == "-v":
            d["-v"] = not d["-v"]
    flt(0).n = d["-d"]
    # flt(0).rtz = True
    if not files:
        Usage(status=1)
    return files


if __name__ == "__main__":
    d = {}  # Options dictionary
    files = ParseCommandLine(d)
    GetData(files)
    ProcessData()
    r = CalculateRegression()
    if d["-v"]:
        PrintData()
    PrintResults(r)
    PrintResiduals(r)
