'''
Routines to help with triangulation.  The uncertainties module is used
if it's available.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # <math> Routines to help with triangulation.  Will use the
    # uncertainties module if it's available.
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    pass
if 1:  # Imports
    from math import cos, acos, sin, asin, tan, atan, sqrt, radians, degrees
if 1:  # Custom imports
    from f import flt
    try:
        from uncertainties import ufloat
        from uncertainties.core import Variable as ufloat_t
        from uncertainties.core import AffineScalarFunc as ufloat_f
        # Note the following imports overshadow the math module's functions, but this is
        # OK because they also take floating point arguments
        from uncertainties.umath import cos, acos, sin, asin, tan, atan, sqrt
    except ImportError:
        pass
    ii = isinstance
def DistAcrossRiver(AB, BD, AC, BC, AD, eps=1e-4):
    '''Returns a 5-tuple of (x, ∂x/∂(AB), ∂x/∂(BD), etc.).  ∂x/∂(AB) is an estimate of
    the partial derivative of x with respect to AB.  Any of the five arguments can be
    integers/floats or uncertainties.ufloats.
    
    Given a linear distance from C to D (i.e., x) across a river you want to measure.
    You can e.g. measure only from the side of AB with a laser distance meter.  You lay
    out a baseline from A to B and measure the five distances AB, BD, AC, BC, AD.  eps
    is a small number used to help estimate partial derivatives.
    
    All these distances must lie in the same plane.
                  +--- river
                  |
                  V
        A---------------------C
        |     ||||||||||      |
        |     ||||||||||      |
        |     ||||||||||      | x
        |     ||||||||||      |
        |     vvvvvvvvvv      |
        B---------------------D
        
    (Of course, it won't be a square in general).  A coordinate system is put on the image
    such that AB is in the +y direction and B is at the origin.

    '''
    assert AB > 0 and BD > 0 and AC > 0 and BC > 0 and AD > 0
    def AngleViaCosLaw(c, a, b):
        'Finds the angle opposite c using the cosine law.'
        return acos((a*a + b*b - c*c)/(2*a*b))
    def CD(AB, BD, AC, BC, AD):
        '''Calculate CD given the five measurements.  Note we average the results from the
        two triangles CBD and CAD and return a flt.
        '''
        if 1:   # Triangle CBD
            ABD = AngleViaCosLaw(AD, AB, BD)
            ABC = AngleViaCosLaw(AC, AB, BC)
            CBD = ABD - ABC
            CD1 = sqrt(BC*BC + BD*BD - 2*BC*BD*cos(CBD))
        if 1:   # Triangle CAD
            CAB = AngleViaCosLaw(BC, AB, AC)
            BAD = AngleViaCosLaw(BD, AB, AD)
            CAD = CAB - BAD
            CD2 = sqrt(AC*AC + AD*AD - 2*AC*AD*cos(CAD))
        if ii(AB, (ufloat_t, ufloat_f)):
            return (CD1 + CD2)/2
        else:
            return flt((CD1 + CD2)/2)
    def ToUnc(x):
        if ii(x, ufloat_t):
            return x
        return ufloat(x, 0)
    if any(ii(i, ufloat_t) for i in (AB, BD, AC, BC, AD)):
        # Make them all ufloats
        AB, BD, AC, BC, AD = [ToUnc(i) for i in (AB, BD, AC, BC, AD)]
        if 1:
            CD_est = CD(AB, BD, AC, BC, AD)
            Eps = ToUnc(eps)
            # Estimate partial derivatives
            da = (CD((1 + Eps)*AB, BD, AC, BC, AD) - CD_est)/(Eps*AB)
            db = (CD(AB, (1 + Eps) * BD, AC, BC, AD) - CD_est)/(Eps*BD)
            dc = (CD(AB, BD, (1 + Eps) * AC, BC, AD) - CD_est)/(Eps*AC)
            dd = (CD(AB, BD, AC, (1 + Eps) * BC, AD) - CD_est)/(Eps*BC)
            de = (CD(AB, BD, AC, BC, (1 + Eps) * AD) - CD_est)/(Eps*AD)
    CD_est = CD(AB, BD, AC, BC, AD)
    # Estimate partial derivatives
    da = (CD((1 + eps)*AB, BD, AC, BC, AD) - CD_est)/(eps*AB)
    db = (CD(AB, (1 + eps) * BD, AC, BC, AD) - CD_est)/(eps*BD)
    dc = (CD(AB, BD, (1 + eps) * AC, BC, AD) - CD_est)/(eps*AC)
    dd = (CD(AB, BD, AC, (1 + eps) * BC, AD) - CD_est)/(eps*BC)
    de = (CD(AB, BD, AC, BC, (1 + eps) * AD) - CD_est)/(eps*AD)
    return CD_est, da, db, dc, dd, de
def CrownMolding(wall_angle, crown_angle):
    '''Given a molding that must be fit to a given wall_angle, the
    crown_angle is the angle of the molding off the vertical to the wall.
    Returns (miter_angle, bevel_angle) in degrees where miter angle is what
    you need to set the table on your miter saw to and bevel angle is how
    much the blade needs to be tilted off the vertical.  Angles must be in
    degrees.
    '''
    miter_angle = atan(sin(radians(crown_angle)/tan(radians(wall_angle)/2)))
    bevel_angle = asin(cos(radians(crown_angle))*cos(radians(wall_angle)/2))
    return degrees(miter_angle), degrees(bevel_angle)

if 0:
    AB, BD, AC, BC, AD = 58.5, 87, 74, 109, 103.5
    x = DistAcrossRiver(AB, BD, AC, BC, AD)
    print(float(x[0]))
    exit()

if __name__ == "__main__":
    from lwtest import run, assert_equal, Assert
    from sig import sig
    try:
        from uncertainties import ufloat
        from uncertainties.umath import cos, acos, sin, asin, tan, atan, sqrt
        have_unc = True
    except ImportError:
        have_unc = False
    def TestDistAcrossRiverUnc():
        if not have_unc:
            return
        if 1:   # Unit square test case
            unc = 0.05
            AB = ufloat(1, unc)
            BD = ufloat(1, unc)
            AC = ufloat(1, unc)
            BC = ufloat(sqrt(2), unc)
            AD = ufloat(sqrt(2), unc)
            x = DistAcrossRiver(AB, BD, AC, BC, AD)
            assert_equal(x[0].nominal_value, 1, reltol=1e-15)
        if 1:   # Test case from pencil sketch on paper
            # Letter paper, measurements in inches
            # Should give result of 9 units for CD
            unc = 0.05
            AB = ufloat(5, unc)
            BD = ufloat(7.28, unc)
            AC = ufloat(5.96, unc)
            BC = ufloat(8.98, unc)
            AD = ufloat(9.84, unc)
            x = DistAcrossRiver(AB, BD, AC, BC, AD)
            Assert(x[0].nominal_value == 9.007579356544376)
    def TestDistAcrossRiver():
        if 1:   # Simplest case:  unit square
            AB, BD, AC, BC, AD, eps = 1, 1, 1, sqrt(2), sqrt(2), 1e-5
            x = DistAcrossRiver(AB, BD, AC, BC, AD, eps=eps)
            assert_equal(x[0], 1, reltol=eps)
            assert_equal(x[1], -1, reltol=eps)
            assert_equal(x[2], -1, reltol=eps)
            assert_equal(x[3], -1, reltol=eps)
            assert_equal(x[4], sqrt(2), reltol=eps)
            assert_equal(x[5], sqrt(2), reltol=eps)
        if 1:   # Test case from pencil sketch on paper
            # Small notepad, measurements in mm
            # Measured side CD was 83.3 mm
            AB, BD, AC, BC, AD = 58.5, 87, 74, 109, 103.5
            x = DistAcrossRiver(AB, BD, AC, BC, AD)
            X = (83.4636548807707, -1.4798379807160942, -1.2529759620744159,
                 -1.5574415442470095, 1.9653558672403655, 1.7401403871848773)
            Assert(x == X)
        if 1:   # Test case from pencil sketch on paper
            # Letter paper, measurements in inches
            # Should give result of 9 units for CD
            AB, BD, AC, BC, AD = 5, 7.28, 5.96, 8.98, 9.84
            x = DistAcrossRiver(AB, BD, AC, BC, AD)
            assert abs(x[0] - 9) < 0.01
    def TestCrownMolding():
        # The easiest test case is where crown angle is zero and where the wall
        # angle is a right angle.
        miter, bevel = CrownMolding(90, 0)
        eps = 1e-15
        assert_equal(miter, 0, reltol=eps)
        assert_equal(bevel, 45, reltol=eps)
        # http://www.installcrown.com/Crown_angle_generator.html
        miter, bevel = CrownMolding(90, 45)
        assert_equal(miter, 35.264389682754654, reltol=eps)
        assert_equal(bevel, 30, reltol=eps)
        # Some oddball numbers using above calculator
        miter, bevel = CrownMolding(68.37, 33.77)
        assert_equal(miter, 39.29636516267699, reltol=eps)
        assert_equal(bevel, 43.444706297407485, reltol=eps)
    exit(run(globals(), halt=1)[0])
