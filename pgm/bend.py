'''
ToDo
    - Use the material in MH to validate the formula and refine the
      printout

Bend allowance computation for sheet metal
    Based on bend.c by M. Klotz.  Klotz lost the attribution, but thought
    it was probably one of Hoffman's articles in "Home Shop Machinist".
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Bend allowance computation for sheet metal
        #∞what∞#
        #∞test∞# #∞test∞#
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
    t = flt(g("t = thickness of material? "))
    r = flt(g("r = radius of bend?        "))
    θ = flt(g("θ = angle of bend in °?    "))
    θ = radians(θ)
    x = t/3 if r < 2*t else 2*t/10
    if r > 4*t:
        x = t/2
    t.N = 4
    print(dedent(f'''
    
    Length of bend exterior          {θ*(r + t)}
    Length of bend interior          {θ*r}
    Length of material to form bend  {θ*(r + x)}

    Formulas:
        if r < 2*t:
            x = t/3
        elif 2*t <= r <= 4*t:
            x = t/5
        else:
            x = t/2
        and
            Length of bend exterior          = θ*(r + t)
            Length of bend interior          = θ*r
            Length of material to form bend  = θ*(r + x)
    '''))
if __name__ == "__main__": 
    BendAllowance()
