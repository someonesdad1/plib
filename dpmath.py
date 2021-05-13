'''
General-purpose math-related functions.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import math
import sys

def AlmostEqual(a, b, rel_err=2e-15, abs_err=5e-323):
    '''Determine whether floating-point values a and b are equal to
    within a (small) rounding error; return True if almost equal and
    False otherwise.  The default values for rel_err and abs_err are
    chosen to be suitable for platforms where a float is represented
    by an IEEE 754 double.  They allow an error of between 9 and 19
    ulps.
 
    This routine comes from the Lib/test/test_cmath.py in the python
    distribution; the function was called almostEqualF.
    '''
    # Special values testing
    if math.isnan(a):
        return math.isnan(b)
    if math.isinf(a):
        return a == b
    # If both a and b are zero, check whether they have the same sign
    # (in theory there are examples where it would be legitimate for a
    # and b to have opposite signs; in practice these hardly ever
    # occur).
    if not a and not b:
        return math.copysign(float(1), a) == math.copysign(float(1), b)
    # If a - b overflows, or b is infinite, return False.  Again, in
    # theory there are examples where a is within a few ulps of the
    # max representable float, and then b could legitimately be
    # infinite.  In practice these examples are rare.
    try:
        absolute_error = abs(b - a)
    except OverflowError:
        return False
    else:
        return absolute_error <= max(abs_err, rel_err*abs(a))

def polar(x, y, deg=False):
    '''Return the polar coordinates for the given rectangular
    coordinates.  If deg is True, angle measure is in degrees;
    otherwise, angles are in radians.
    '''
    r2d = 180/math.pi if deg else 1
    return (math.hypot(x, y), math.atan2(y, x)*r2d)

def rect(r, theta, deg=False):
    '''Return the rectangular coordinates for the given polar
    coordinates.  If deg is True, angle measure is in degrees;
    otherwise, angles are in radians.
    '''
    d2r = math.pi/180 if deg else 1
    return (r*math.cos(theta*d2r), r*math.sin(theta*d2r))

if 1:   # Polynomial utilities
    # These routines were originally from 
    # http://www.physics.rutgers.edu/~masud/computing/
    # in the file WPark_recipes_in_python.html.  This URL is now defunct.

    # coef is a sequence of the polynomial's coefficients; coef[0] is the
    # constant term and coef[-1] is the highest term; x is a number.

    def polyeval(coef, x):
        '''Evaluate a polynomial with the stated coefficients.  Returns 
        coef[0] + x(coef[1] + x(coef[2] +...+ x(coef[n-1] + coef[n]x)...)
     
        Example: polyeval((3, 2, 1), 6) = 3 + 2(6) + 1(6)**2 = 51
        '''
        p = 0
        for i in reversed(coef):
            p = p*x + i
        return p

    def polyderiv(coef):
        '''Returns the coefficients of the derivative of a polynomial with
        coefficients in coef.
 
        Example: polyderiv((3, 2, 1)) = [2, 2]
        '''
        b = []
        for i in range(1, len(coef)):
            b.append(i*coef[i])
        return b

    def polyreduce(coef, root):
        '''Given a root of a polynomial, factor out the (x - root) term, then
        return the coefficients of the factored polynomial.
 
        Example: polyreduce((-12, -1, 1), -3) = [-4, 1]
        '''
        c, p = [], 0
        for i in reversed(coef):
            p = p*root + i
            c.append(p)
        c.reverse()
        return c[1:]

def bitlength(n):
    '''This emulates the n.bit_count() function of integers in python 2.7
    and 3.  This returns the number of bits needed to represent the
    integer n; n can be any integer.
 
    A naive implementation is to take the base two logarithm of the
    integer, but this will fail if abs(n) is larger than the largest
    floating point number.
    '''
    try:
        return n.bit_count()
    except Exception:
        return len(bin(abs(n))) - 2

def isqrt(x):
    '''Integer square root.  This calculation is done with integers, so it
    can calculate square roots for large numbers that would overflow the
    normal square root function.
    
    From
    http://code.activestate.com/recipes/577821-integer-square-root-function/
    '''
    if x < 0:
        raise ValueError("Square root not defined for negative numbers")
    n = int(x)
    if n == 0:
        return 0
    a, b = divmod(bitlength(n), 2)
    x = 2**(a+b)
    while True:
        y = (x + n//x)//2
        if y >= x:
            return x
        x = y
