if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Bend allowance computation
    #∞what∞#
    #∞test∞# #∞test∞#
    #
    # Patterned after bend.c by Marv Klotz.  Klotz lost the attribution,
    # but thought it was probably in one of Hoffman's articles in "Home
    # Shop Machinist".
    pass
if 1:   # Imports
    import sys
    from functools import partial
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumber
    from f import flt, radians
def BendAllowance():
    g = partial(GetNumber, low_open=True, low=0)
    print("Bend Allowance Computation (length units are arbitrary)\n")
    t = flt(g("Thickness of material? "))
    r = flt(g("Radius of bend? "))
    θ = flt(g("Angle of bend in degrees? "))
    θ = radians(θ)
    x = t/3 if r < 2*t else 2*t/10
    if r > 4*t:
        x = t/2
    t.n = 4
    print(dedent(f'''
    
    Length of bend exterior                   {θ*(r + t)}
    Length of bend interior                   {θ*r}
    Length of material required to form bend  {θ*(r + x)}
    '''))
if __name__ == "__main__": 
    BendAllowance()
