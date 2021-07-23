'''
Print rational approximations of common constants
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
    # Print rational approximations of common constants
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
    from fractions import Fraction
    from rational import RatApp
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    #from sig import sig
    #from math import sqrt, pi, exp, log, log10
    from f import flt, sqrt, pi, exp, log, log10
if 1:   # Global variables
    e = exp(1)
    numbers = [
        ("pi", pi),
        ("sqrt(pi)", sqrt(pi)),
        ("pi^2", pi**2),
        ("e", e),
        ("sqrt(e)", sqrt(e)),
        ("e^2", e**2),
        ("e^pi", e**pi),
        ("ln(pi)", log(pi)),
        ("ln(2)", log(2)),
        ("ln(3)", log(3)),
        ("ln(4)", log(4)),
        ("ln(5)", log(5)),
        ("ln(6)", log(6)),
        ("ln(7)", log(7)),
        ("ln(8)", log(8)),
        ("ln(9)", log(9)),
        ("ln(10)", log(10)),
        ("log(pi)", log10(pi)),
        ("log(2*pi)", log10(2*pi)),
        ("log(e)", log10(e)),
        ("log(2)", log10(2)),
        ("log(3)", log10(3)),
        ("180/pi", 180/pi),
        ("2**(1/3)", flt(2)**(1/3)),
        ("sqrt(3)/2", sqrt(3)/2),
        ("1/sqrt(2*pi)", 1/sqrt(2*pi)),
    ]
def FmtFrac(f):
    return f"{f.numerator}/{f.denominator}"
def PrintRatApprox(name, value):
    '''Print the rational approximation for the given value at the
    chosen precision points.
    '''
    if int(value) == value:     # Ignore integers
        return
    print(f"{name:13s} {value!s:13s}", end=" ")
    p = (1, 0.1, 0.01, 0.001)
    for pct in p:
        f = RatApp(float(value), reltol=pct/100)
        print("{:10s}".format(FmtFrac(f)), end=" ")
    print()
if __name__ == "__main__":
    s = " "*14 
    flt(0).n = 8
    print("Rational approximations", s, "Relative % error")
    print("-----------------------", end="")
    print(" "*6, "1         0.1        0.01       0.001")
    print(" "*27, "-----      ------     ------     -------")
    for name, value in numbers:
        PrintRatApprox(name, value)
    print()
    print("Square roots:")
    numbers = [
        ("pi", sqrt(pi)),
        ("e", sqrt(e)),
    ]
    n = 20
    for i in range(2, n + 1):
        numbers.append(("{}".format(i), sqrt(i)))
    for name, value in numbers:
        PrintRatApprox(name, value)
