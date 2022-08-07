'''
Cartesian coordinates of bolt holes on a circle
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
    # Cartesian coordinates of bolt holes on a circle
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
if 1:   # Custom imports
    from f import flt, sin, cos, pi, degrees, radians
    from get import GetNumber
    from wrap import dedent
def Error(*msg, status=1):
    print(*msg, file=sys.stderr)
    exit(status)
def GetParameters():
    print("Print a table of the Cartesian coordinates of holes on a circle.")
    digits = GetNumber("How many significant digits?", numtype=int, default=6,
                       low=1, high=15)
    n = GetNumber("How many holes to place?", numtype=int, default=6,
                  low=0, low_open=True)
    dia = flt(GetNumber("Bolt circle diameter? ", low=0, low_open=True,
                        default=1))
    theta_offset = flt(GetNumber("Angle offset of first hole (degrees)? ",
                                default=0))
    x0 = flt(GetNumber("x position of origin? ", default=0))
    y0 = flt(GetNumber("y position of origin? ", default=0))
    return n, dia, theta_offset, x0, y0, digits
def BoltCircle():
    if 0:
        N, Diameter, theta_offset, X0, Y0, digits = GetParameters()
    else:
        N, Diameter, theta_offset, X0, Y0, digits = (1, flt(10),
                flt(0), flt(1), flt(-1), 6)
    X0.n, w = digits, 25
    print(dedent(f'''
    Bolt circle placement
    ---------------------
      {'Number of holes':{w}s} {N}
      {'Bolt circle diameter':{w}s} {Diameter}   radius = {Diameter/2}
      {'Angle offset':{w}s} {theta_offset} degrees
      {'Origin':{w}s} ({X0}, {Y0})
    '''))
    s = "Table of hole positions"
    print()
    print(s)
    print("-"*len(s))
    print()
    w, eps, r = 15, 1e-14, Diameter/2
    s = "-"*(w - 4)
    print(f"Hole {'x':^{w}} {'y':^{w}} {'theta, deg':^{w}}")
    print(f"---- {s:^{w}} {s:^{w}} {s:^{w}}")
    def g(x):
        return f"{x!s:^{w}}" if abs(x) >= eps else f"{flt(0)!s:{w}}"
    for i in range(N):
        theta = 2*pi*i/N + radians(theta_offset)
        X, Y = r*cos(theta) + X0, r*sin(theta) + Y0
        x, y, t = g(X), g(Y), degrees(theta)
        print(f"{i + 1:^4} {x:^{w}} {y:^{w}} {t:^{w}}")
if __name__ == "__main__": 
    BoltCircle()
