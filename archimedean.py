'''
Length of an Archimedian spiral
 
Motivation:  How much toilet paper is on a roll?  One way to measure it
would be to roll it out.  This is perhaps the most accurate method.  But
it would be nice to be able to estimate it from the roll's dimensions.
The function ArchimedianSpiralArcLength below will help you do this.
 
The polar equation of this spiral is
 
    r = a*theta
 
where theta is the angle and a is a constant.  For a spiral with
multiple revolutions, the distance between the revolutions (pitch)
is 2*pi*a.
 
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
    # Program description string
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
 
import math
 
def SpiralArcLength(a, theta, degrees=False):
    '''Calculate the arc length of an Archimedian spiral from angle
    0 to theta.  theta is in radians unless degrees is True.  The number a
    is the constant in the polar equation for the spiral
 
        r = a*theta
 
    The formula is exact.
    '''
    if a <= 0:
        raise ValueError("a must be > 0")
    theta = math.radians(theta) if degrees else theta
    A = math.sqrt(theta*theta + 1)
    return a/2*(theta*A + math.log(theta + A))

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
        a, n_revolutions, twopi = 1, 10000, 2*math.pi
        theta = n_revolutions*2*math.pi
        arc_len = SpiralArcLength(a, theta) - SpiralArcLength(a, theta - 2*math.pi)
        L_D = SpiralArcLength(a, n_revolutions*twopi)
        L_d = SpiralArcLength(a, (n_revolutions - 1)*twopi)
        arc_length = L_D - L_d
        pitch = a*twopi
        D = (2*n_revolutions - 1)*pitch
        circumference = D*math.pi
        assert_equal(circumference, arc_len, reltol=1e-8)
    r = r"^Test_"
    failed, messages = run(globals(), regexp=r, quiet=0)
