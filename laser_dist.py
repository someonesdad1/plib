'''
Routines to help with triangulation.  The uncertainties module is used
if it's available.
'''

# Copyright (C) 2010 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from math import cos, acos, sin, asin, tan, atan, sqrt, pi

try:
    from uncertainties import ufloat, UFloat
    from uncertainties.umath import (cos, acos, sin, asin, tan, atan,
                                     sqrt, pi)
except ImportError:
    pass

def DistAcrossRiver(AB, BD, AC, BC, AD, eps=1e-4):
    '''Returns a 5-tuple of (x, dx/d(AB), dx/d(BD), etc.).  dx/d(AB) is
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
    '''
    assert(AB > 0 and BD > 0 and AC > 0 and BC > 0 and AD > 0)
    def AngleViaCosLaw(c, a, b):
        'Finds the angle opposite c using the cosine law.'
        return acos((a*a + b*b - c*c)/(2*a*b))
    def f(AB, BD, AC, BC, AD):
        'Calculate CD given the five measurements.'
        ABD = AngleViaCosLaw(AD, AB, BD)
        ABC = AngleViaCosLaw(AC, AB, BC)
        CBD = ABD - ABC
        CD = BC*BC + BD*BD - 2*BC*BD*cos(CBD)
        return sqrt(CD)
    # Estimate the unknown distance
    CD_est = f(AB, BD, AC, BC, AD)
    # Estimate partial derivatives
    da = (f((1+eps)*AB, BD, AC, BC, AD) - CD_est)/(eps*AB)
    db = (f(AB, (1+eps)*BD, AC, BC, AD) - CD_est)/(eps*BD)
    dc = (f(AB, BD, (1+eps)*AC, BC, AD) - CD_est)/(eps*AC)
    dd = (f(AB, BD, AC, (1+eps)*BC, AD) - CD_est)/(eps*BC)
    de = (f(AB, BD, AC, BC, (1+eps)*AD) - CD_est)/(eps*AD)
    return CD_est, da, db, dc, dd, de

def CrownMoulding(wall_angle, crown_angle):
    '''Given a molding that must be fit to a given wall_angle, the
    crown_angle is the angle of the molding off the vertical to the wall.
    Returns (miter_angle, bevel_angle) in degrees where miter angle is what
    you need to set the table on your miter saw to and bevel angle is how
    much the blade needs to be tilted off the vertical.  Angles must be in
    degrees.
    '''
    s = pi/180
    miter_angle = atan(sin(crown_angle*s)/tan(wall_angle*s/2))
    bevel_angle = asin(cos(crown_angle*s)*cos(wall_angle*s/2))
    return miter_angle/s, bevel_angle/s
