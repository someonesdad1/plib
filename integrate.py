'''
Various pure-python numerical integration routines.
'''

# Copyright (C) 2011, 2017 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
from __future__ import print_function, division
import sys

py3 = sys.version_info[0] >= 3
Int = (int,) if py3 else (int, long)

def Simpson(f, a, b, n):
    '''Integrate f over the interval [a, b] with n points via Simpson's
    rule.  f is a univariate function.
    '''
    _CheckParameters(f, a, b, n, neven=True)
    h = (b - a)/float(n)
    sum = 0.0
    for i in range(1, n):
        if i % 2 == 0:
            sum += 2.0*f(a + i*h)
        else:
            sum += 4.0*f(a + i*h)
    return h/3.0*(f(a) + sum + f(b))

def Trapezoidal(f, a, b, n):
    '''Integrate f over the interval [a, b] with n points via the
    trapezoidal rule.  From Bartsch, "Handbook of Mathematical Formulas",
    Academic Press, 1974, page 361.
    '''
    _CheckParameters(f, a, b, n)
    h = (b - a)/float(n)
    sum = 0.0
    for i in range(n):
        sum += 2.0*f(a + i*h)
    return (f(a) + sum + f(b))*h/2.0

def Trapezoid_nme(f, a, b, integral_old, n):
    '''Returns an estimate of the integral of f(x) from a to b using 2^n
    points and given that integral_old is the estimate from 2^(n-1) points.

    From "Numerical Methods in Engineering with Python", 2nd ed. by Jaan
    Kiusalaas, 2010, ISBN: 9780521191326.
    '''
    _CheckParameters(f, a, b, n)
    if n == 1:
        integral_new = (f(a) + f(b))*(b - a)/2.0
    else:
        n = 2**(n - 2)      # Number of new points
        h = (b - a)/n       # Spacing of new points
        x = a + h/2.0       # Coord. of 1st new point
        sum = 0.0
        for i in range(n):
            sum, x = sum + f(x), x + h
        integral_new = (integral_old + h*sum)/2.0
    return integral_new

def Trapezoid_nr(f, a, b, n, s=[0]):
    '''trapzd routine from Numerical Recipes in C, pg 137, sec. 4.2.
    Note they use a static variable s to contain the values of the previous
    call; we emulate that with the parameter s -- you don't need to pass in
    anything for s.
    '''
    if n == 1:
        s[0] = 0.5*(b - a)*(f(a) + f(b))
    else:
        it = 1
        for i in range(1, n-1):
            it <<= 1
        tnm = it
        delta = (b - a)/tnm
        x = a + 0.5*delta
        sum = 0
        for i in range(1, it + 1):
            sum += f(x)
            x += delta
        s[0] = 0.5*(s[0] + (b - a)*sum/tnm)
    return s[0]

def Trapezoid(f, a, b, eps=1e-6, itmax=50):
    '''Driver to use the Trapezoid_nr routine to calculate the integral of
    f(x) from a to b to within less than relative error eps.
    '''
    # Any number that is unlikely to be the average of the function at
    # its endpoints will do here.
    olds = -1e-30
    for i in range(1, itmax+1):
        s = Trapezoid_nr(f, a, b, i)
        if i > 5:
            if abs(s - olds) < eps*abs(olds) or (s == 0 and olds == 0):
                return s
        olds = s
    raise ValueError("Too many iterations")

def _CheckParameters(f, a, b, n, neven=False):
    if not callable(f):
        raise ValueError("f must be a univariate function")
    if not isinstance(n, Int):
        raise TypeError(msg)
    if neven:
        if n < 2 or n % 2 != 0:
            raise ValueError("n must be an even integer >= 2")
    else:
        if n <= 1:
            raise ValueError("n must be an integer > 1")
    if a >= b:
        raise ValueError("Must have a < b")
