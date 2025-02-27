"""
Routines to help with triangulation.  The uncertainties module is used
if it's available.
"""

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
    from math import cos, acos, sin, asin, tan, atan, sqrt, pi
if 1:  # Custom imports
    try:
        from uncertainties import ufloat, UFloat
        from uncertainties.umath import cos, acos, sin, asin, tan, atan, sqrt, pi
    except ImportError:
        pass


def DistAcrossRiver(AB, BD, AC, BC, AD, eps=1e-4):
    """Returns a 5-tuple of (x, dx/d(AB), dx/d(BD), etc.).  dx/d(AB) is
    an estimate of the partial derivative of x with respect to AB.

    Given a linear distance from C to D (i.e., x) across a river you
    want to measure.  You can e.g. measure only from the side of AB
    with a laser distance meter.  You lay out a baseline from A to B
    and measure the five distances AB, BD, AC, BC, AD.  eps is a small
    number used to help estimate partial derivatives.

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

    (Of course, it won't be square in general).  A coordinate system
    is put on the image such that AB is in the +y direction and B is
    at the origin.
    """
    assert AB > 0 and BD > 0 and AC > 0 and BC > 0 and AD > 0

    def AngleViaCosLaw(c, a, b):
        "Finds the angle opposite c using the cosine law."
        return acos((a * a + b * b - c * c) / (2 * a * b))

    def f(AB, BD, AC, BC, AD):
        "Calculate CD given the five measurements."
        ABD = AngleViaCosLaw(AD, AB, BD)
        ABC = AngleViaCosLaw(AC, AB, BC)
        CBD = ABD - ABC
        CD = BC * BC + BD * BD - 2 * BC * BD * cos(CBD)
        return sqrt(CD)

    # Estimate the unknown distance
    CD_est = f(AB, BD, AC, BC, AD)
    # Estimate partial derivatives
    da = (f((1 + eps) * AB, BD, AC, BC, AD) - CD_est) / (eps * AB)
    db = (f(AB, (1 + eps) * BD, AC, BC, AD) - CD_est) / (eps * BD)
    dc = (f(AB, BD, (1 + eps) * AC, BC, AD) - CD_est) / (eps * AC)
    dd = (f(AB, BD, AC, (1 + eps) * BC, AD) - CD_est) / (eps * BC)
    de = (f(AB, BD, AC, BC, (1 + eps) * AD) - CD_est) / (eps * AD)
    return CD_est, da, db, dc, dd, de


def CrownMoulding(wall_angle, crown_angle):
    """Given a molding that must be fit to a given wall_angle, the
    crown_angle is the angle of the molding off the vertical to the wall.
    Returns (miter_angle, bevel_angle) in degrees where miter angle is what
    you need to set the table on your miter saw to and bevel angle is how
    much the blade needs to be tilted off the vertical.  Angles must be in
    degrees.
    """
    s = pi / 180
    miter_angle = atan(sin(crown_angle * s) / tan(wall_angle * s / 2))
    bevel_angle = asin(cos(crown_angle * s) * cos(wall_angle * s / 2))
    return miter_angle / s, bevel_angle / s


if __name__ == "__main__":
    from lwtest import run, assert_equal
    from sig import sig

    try:
        from uncertainties import ufloat, UFloat
        from uncertainties.umath import cos, acos, sin, asin, tan, atan
        from uncertainties.umath import sqrt, pi

        have_unc = True
    except ImportError:
        have_unc = False

    def TestDistAcrossRiver():
        # Should give result of 9 units for CD
        AB, BD, AC, BC, AD = 5, 7.28, 5.96, 8.98, 9.84
        x = DistAcrossRiver(AB, BD, AC, BC, AD)
        assert abs(x[0] - 9) < 0.01
        x_no_unc = x[0]
        # Same test, but with uncertainties
        if have_unc:
            unc = 0.05
            AB = ufloat(5, unc)
            BD = ufloat(7.28, unc)
            AC = ufloat(5.96, unc)
            BC = ufloat(8.98, unc)
            AD = ufloat(9.84, unc)
            x = DistAcrossRiver(AB, BD, AC, BC, AD)
            assert abs(x_no_unc - x[0]) < 0.01
            assert abs(x[0] - 9) < 0.01
            assert sig(x[0]) == "9.0(2)"

    def TestCrownMoulding():
        # The easiest test case is where crown angle is zero and where the wall
        # angle is a right angle.
        miter, bevel = CrownMoulding(90, 0)
        eps = 1e-15
        assert_equal(miter, 0, reltol=eps)
        assert_equal(bevel, 45, reltol=eps)
        # http://www.installcrown.com/Crown_angle_generator.html
        miter, bevel = CrownMoulding(90, 45)
        assert_equal(miter, 35.264389682754654, reltol=eps)
        assert_equal(bevel, 30, reltol=eps)
        # Some oddball numbers using above calculator
        miter, bevel = CrownMoulding(68.37, 33.77)
        assert_equal(miter, 39.29636516267699, reltol=eps)
        assert_equal(bevel, 43.444706297407485, reltol=eps)

    exit(run(globals(), halt=1)[0])
