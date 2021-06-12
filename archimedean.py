'''
Length of an Archimedian spiral
 
Motivation:  How much toilet paper is on a roll?  One way to measure it
would be to roll it out.  This is perhaps the most accurate method.  But
it would be nice to be able to estimate it from the roll's dimensions.
The function ArchimedianSpiralArcLength below will help you do this.
 
The polar equation of this spiral is
 
    r = a*theta
 
where theta is the angle and a is a constant.  For a spiral with
multiple revolutions, the distance between the revolutions (i.e., the
pitch) is 
        
    pitch = 2*pi*a = math.tau*a.
  
The arc length s is gotten from the integral from theta1 to theta2
of
 
    sqrt(r*r + (dr/dtheta)^2) dtheta
 
Substituting the equation for a spiral, we get
 
    A = sqrt(theta*theta + 1)
    s = a/2*[theta*A + ln(theta + A)]
 
This is the formula for the total arc length from an angle of 0 to an angle
of theta (remember theta is in radians).
 
To convert this to more practical formulas, let
 
    D = outside diameter of roll
    d = inside diameter of roll
    t = thickness of material on roll
    n = number of turns of material on roll = n1 - n0
    n0 = number of turns to make up ID
    n1 = number of turns to make up OD
 
Now, if t is reasonably thin, we have
 
    D = d + 2*n*t
 
because one wrap adds a thickness of 2*t on the diameter.  For thin t,
we can approximate the length by a finite sum:
 
    1st wrap:  circumference = pi*d
    2nd wrap:  circumference = pi*(d + 1*(2*t))
    3rd wrap:  circumference = pi*(d + 2*(2*t))
    4th wrap:  circumference = pi*(d + 3*(2*t))
    ...
    nth wrap:  circumference = pi*(d + (n-1)*(2*t))
 
Thus, the sum is
 
    S = pi*[d + (d + 1*(2*t)) + (d + 2*(2*t)) + ... + (d + (n-1)*(2*t))]
 
This is
 
    S = pi[n*d + 2*t*A(n - 1)]
 
where A(n - 1) is the sum of the integers 1 to (n - 1).  This is
0.5*(n - 1)*(n - 1 + 1) or n*(n - 1)/2.  Hence
 
    S/pi = n*d + 2*t*n*(n-1)/2 = n*d + t*n(n-1)
 
or, finally,
 
  +------------------------+
  |                        |
  | S = pi*n*[t*(n-1) + d] |
  |                        |
  +------------------------+
 
In terms of the constant in the polar equation for the spiral, we have
 
    t = 2*pi*a
    a = t/(2*pi)
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Functions to calculate the length of an Archimedian spiral.
    # Both exact and approximate formulas are given.  Example:
    # estimate the length of paper on a roll of toilet paper.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import math
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from frange import frange
    from f import flt, radians, log, sqrt
def SpiralArcLength(a, theta, degrees=False):
    '''Calculate the arc length of an Archimedian spiral from angle
    0 to theta.  theta is in radians unless degrees is True.  The number a
    is the constant in the polar equation for the spiral
 
        r = a*theta
 
    The formula is exact.
    '''
    if a <= 0:
        raise ValueError("a must be > 0")
    theta = radians(flt(theta)) if degrees else flt(theta)
    A = sqrt(theta*theta + 1)
    return flt(a)/2*(theta*A + log(theta + A))
def ApproximateSpiralArcLength(ID, OD, thickness):
    '''Given the inside and outside diameters of a spiral roll of
    material with uniform thickness, estimate the length of material on
    the roll.  The three parameters must be measured in the same units
    and the returned number will be in the same units.
 
    The smaller thickness(OD - ID) is, the better the approximation.
    '''
    # Approximation:  for a large diameter circle, one revolution of a
    # fine-pitch spiral should be nearly equal to the circumference.
    if ID < 0 or ID >= OD:
        raise ValueError("ID must be >= 0 and < OD")
    if OD <= 0:
        raise ValueError("OD must be > 0")
    if thickness <= 0:
        raise ValueError("thickness must be > 0")
    n = (OD - ID)/thickness
    if n < 1:
        raise ValueError("Number of turns is < 1")
    pitch = (OD - ID)/n
    length = 0
    for dia in frange(ID, OD, 2*pitch):
        dia += pitch    # Use in-between diameter
        length += 2*math.pi*(dia + pitch)
    return length

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal
    def Test_exact_formula():
        # a = 1, one revolution
        a, theta = 1, 2*math.pi
        A = math.sqrt(theta**2 + 1)
        exact = a/2*(theta*A + math.log(theta + A))
        formula = SpiralArcLength(a, theta)
        assert_equal(exact, formula)
        # Get ValueError for a < 0
        raises(ValueError, SpiralArcLength, -1, 1)
    def Test_approximation():
        # Approximation:  for a large diameter circle, one revolution of a
        # fine-pitch spiral should be nearly equal to the circumference.
        a, n_revolutions = 1, 10000
        theta = n_revolutions*math.tau
        arc_len = (SpiralArcLength(a, theta) -
                   SpiralArcLength(a, theta - math.tau))
        L_D = SpiralArcLength(a, n_revolutions*math.tau)
        L_d = SpiralArcLength(a, (n_revolutions - 1)*math.tau)
        arc_length = L_D - L_d
        pitch = a*math.tau
        D = (2*n_revolutions - 1)*pitch
        circumference = D*math.pi
        assert_equal(circumference, arc_len, reltol=1e-8)
    def Test_approximate_formula():
        ID, OD = 1, 2
        thickness = 0.001
        pitch = 2*thickness
        diameters = list(frange("1", "2", "0.001"))
        # Sum the circumferences
        estL1 = sum([dia*math.pi for dia in diameters])
        estL2 = ApproximateSpiralArcLength(ID, OD, thickness)
        assert_equal(estL1, estL2, reltol=0.002)
        # Now compare to exact formula
        a = pitch/math.tau
        # There are approximately ID/pitch circles from the spiral center
        # to the ID.  Since each is a revolution, multiplying by 2*pi
        # gives the total angle from 0 to the ID.  Similarly for OD.
        theta1 = math.tau*(ID/pitch)
        theta2 = math.tau*(OD/pitch)
        length1 = SpiralArcLength(a, theta1)
        length2 = SpiralArcLength(a, theta2)
        exact_length = length2 - length1
        tol = 0.001
        assert_equal(estL1, exact_length, reltol=tol)
        assert_equal(estL2, exact_length, reltol=tol)
        # In the above, L = 4710.8, estL = 4715.5, and the exact length
        # is 4712.4.  Note the exact length is between the two
        # estimates.
    def Test_toilet_paper_roll():
        '''A roll of toilet paper has an ID of 42 mm, an OD of 130 mm,
        and a thickness of about 0.125 mm.  Each sheet is 101x96 mm with
        the 101 mm dimension perpendicular to the perforations.  The
        manufacturer states there are 18 rolls in the package and the
        total area is 815.1 square feet.  Each roll is stated to have
        425 sheets on it, so that means the length of paper is 425(101
        mm) or 
        Check if this is approximately
        correct.  Use flt for calculations.
        '''
        from f import flt, tau
        from sys import argv
        num_rolls = 18
        mm = flt("1 mm")
        mm.n = 4
        ID, OD = mm(60), mm(130)
        fudge = 3.942
        width, thickness = mm(96), mm(0.125)*fudge
        pitch = 2*thickness
        length_actual = 425*mm(101)
        a = pitch/tau
        # Have to use ID.val because frange barfs on a flt
        f = lambda x:  float(x.val)
        # Since we know the stated length, use the approximate formula
        # to calculate what the thickness must be.
        length = mm(ApproximateSpiralArcLength(f(ID), f(OD),
                        f(thickness)))
        length_ft = length.to("ft")
        # The area per roll is the exact_length times the 101 mm
        # dimension
        area_per_roll = length*width
        area_per_roll_ft2 = area_per_roll.to("ft2")
        total_area = num_rolls*area_per_roll
        A_calc_ft2 = total_area.to('ft2')
        A_exact_ft2 = flt("815 ft2")
        assert_equal(A_calc_ft2, A_exact_ft2, reltol=0.01)
        if 0:   # Dump the variables
            d = locals()
            for i in sorted(d.keys()):
                if i in "flt tau mm f".split():
                    continue
                print(f"{i}: {d[i]}")
    exit(run(globals(), regexp="^Test_", quiet=0)[0])
