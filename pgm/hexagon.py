'''
Give information on hexagon dimensions
    For each dimension given on command line:

    Assume it's either the diameter of the inscribed circle d or the
    circumscribed circle diameter D; calculate the other dimensions of
    the hexagon.

    A = area = sqrt(3)/2*d^2
    a = length of side = D/2 = d/sqrt(3)
    D = 2*a = 2*(length of side) = 2*d/sqrt(3)
    d = D*sqrt(3)/2
    s = perimeter = 6*a

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
    # Calculate hexagon dimensions from distance across flats & points
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    from fractions import Fraction
    import sys
if 1:   # Custom imports
    from wrap import dedent
    import sigfig
    from f import flt
if 1:   # Global variables
    sr3 = flt(3**0.5)
    sr3.N = 5
    sr3.rtz = sr3.rtdp = False
def Convert(size):
    'Convert the string size to a flt'
    if "/" in size:
        ip = 0
        num, denom = size.split("/")
        if "-" in num:
            ip, num = num.split("-")
        num, denom, ip = [int(i) for i in (num, denom, ip)]
        x = Fraction(num + ip*denom, denom)
        n = max(3, sigfig.SigFig(x))
        y = flt(x)
        y.n = n
        return y
    else:
        n = max(3, sigfig.SigFigFloat(float(size)))
        x = flt(size)
        x.n = n
        return x
def Hexagon(size):
    def P(dia, inscribed=True):
        if inscribed:
            msg = "Size is inscribed circle (measurement across flats):"
        else:
            msg = "Size is circumscribed circle (measurement over points):"
        a = dia/sr3
        A = sr3/2*dia**2
        D = 2*a
        s = 6*a
        print(dedent(f'''
        {msg}
          d = across flats   = {dia}
          D = across points  = {D}
          a = length of side = {a}
          A = area           = {A}
          s = perimeter      = {s}
        '''))
    # Inscribed circle
    D = Convert(size)
    P(D, inscribed=True)
    # Circumscribed circle
    P(D*sr3/2, inscribed=False)
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print(dedent(f'''
        Usage:  {sys.argv[0]} diam1 [diam2...]
            Prints dimensions of a hexagon given the inscribed or circumscribed
            circle diameter.'''))
        exit(1)
    for i in sys.argv[1:]:
        Hexagon(i)
