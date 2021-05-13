'''
Code for the complete elliptic functions.

From Robert Weaver's website:
    http://electronbunker.sasktelwebsite.net/CalcMethods2c.html

Bob commented in an email that it's more efficient to calculate these
functions using the arithmetic-geometric mean as used in the Nagaoka
function in calculating the inductance of coils.  He sent me his javascript
implementations of those, so I've included them too (they are used by
default).  Change use_series to True to use the series calculation method.

The series algorithm comes from
http://electronbunker.sasktelwebsite.net/DL/KelvinEllipticCalcs.pdf
'''

# Copyright (C) 2010, 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import math

debug = False
use_series = False

if use_series:
    def EllipticK(k, eps=1e-15):
        '''Calculate the complete elliptic integral of the first kind with
        modulus k.  Uses series expansion; based on Dwight's formulas 773.2
        & 773.3.  Translated from Basic code by Robert Weaver, 2009-10-26.
        '''
        kp2 = 1-k*k
        kp = math.sqrt(kp2)     # complementary modulus
        count, value = 1, 0
        if k <= 0.91:
            # if k <= .91 use formula 773.2
            m = (1-kp)/(1+kp)
            m2 = m*m
            term = 1.0      # the zeroth term is 1.0
            sum = term
            for n in range(2, 101, 2):
                # calc nth coefficient
                termi = ((n-1)/(n))**2*m2
                term = term*termi
                sum = sum+term
                if (term/sum) < eps:
                    break
                count += 1
            value = math.pi*sum/2*(m+1)
        else:
            # if k > .91 use formula 773.3
            term = math.log(4/kp)
            coeff = 1.0
            sum = term
            for n in range(2, 101, 2):
                coeff = coeff*((n-1)/n)**2*kp2
                termi = 2/((n-1)*n)
                term = term-termi
                sum = sum+coeff*term
                if (coeff*term/sum) < eps:
                    break
                count += 1
            value = sum
        if debug:
            print("EllipticK(%.6f) =" % k, value, "in", count, "steps")
        return value

    def EllipticE(k, eps=1e-15):
        '''Calculate the complete elliptic integral of the second kind with
        modulus k.  Uses series expansion.  Based on H. B. Dwight's formulae
        774.2 & 774.3.  Adapted from Basic code by Robert Weaver, 2009-10-26
        '''
        kp2 = 1-k*k
        kp = math.sqrt(kp2)     # complementary modulus
        m, count = (1-kp)/(1+kp), 1
        if k == 1:
            # This prevents a divide by zero problem
            value = 1
        elif k < 0.93:
            # formula 774.2
            term = 1.0      # the zeroth term is 1.0
            sum = term
            coeff = 1.0     # the zeroth coefficient is 1
            for n in range(2, 101, 2):
                termi = m*(n-3)/n
                term = term*termi*termi
                sum = sum+term
                if (term/sum) < eps:
                    break
                count += 1
            value = math.pi*sum/(2*m+2)
        else:
            # formula 774.3
            tio = 0
            cio = 1
            coeff = 1
            term = math.log(4/kp)
            sum = 1
            for n in range(2, 101, 2):
                cin = (n-1)/n
                coeff = coeff*cio*cin*kp2
                cio = cin
                tin = 1/((n-1)*n)
                term = term-tio-tin
                tio = tin
                sum = sum+term*coeff
                if (term*coeff/sum) < eps:
                    break
                count += 1
            value = sum
        if debug:
            print("EllipticE(%.6f) =" % k, sum, "in", count, "steps")
        return value
else:
    def EllipticK(k):
        '''Returns the complete elliptic integral of the 1st kind for
        modulus k.
        '''
        m, a = k*k, 1
        b = math.sqrt(1 - m)
        c, co = a - b, 2*(a - b)
        while c < co:
            co = c
            c = (a - b)/2
            ao = (a + b)/2
            b = math.sqrt(a*b)
            a = ao
        return math.pi/(a + a)

    def EllipticE(k):
        '''Returns the complete elliptic integral of the 2nd kind for
        modulus k.
        '''
        if k == 1:
            return 1
        else:
            kk, c, a, ci, co = k*k, 1, 1, 1, 2
            b = math.sqrt(1-kk)
            E = 1 - kk/2
            while c < co:
                co = c
                c = (a - b)/2
                E = E - ci*c*c
                ao = (a + b)/2
                b = math.sqrt(a*b)
                ci *= 2
                a = ao
            return E*math.pi/(a + a)

def EllipseCircumference(a, b):
    '''Calculate the circumference of an ellipse with major
    diameter a and minor diameter b.  Relative accuracy is about
    0.5^53 (~ 1e-16).  Downloaded Mon 26 May 2014 from
    http://paulbourke.net/geometry/ellipsecirc/python.code

    Note that the formula for the circumference of an ellipse is
    2*a*E(e) where a is the major diameter, e is the eccentricity,
    and E is the complete elliptic integral of the second kind.  Thus,
    this function an also be used to calculate E.

    A quick check showed that Bourke's formula iterates about half as
    much as Weaver's EllipticE.  Since they agree in the tests to
    floating point precision, Bourke's is preferred -- it converges
    quadratically.
    '''
    assert a >= 0 and b >= 0
    # Note the original formula is in terms of the 'semi-axes';
    # hence the division by 2.
    a, b = a/2, b/2
    x, y = max(a, b), min(a, b)
    digits = 53
    tol = math.sqrt(math.pow(0.5, digits))
    if digits*y < tol*x:
        return 4*x
    s, m = 0, 1
    while x - y > tol*y:
        x, y = 0.5*(x + y), math.sqrt(x*y)
        m *= 2
        s += m*math.pow(x - y, 2)
    return math.pi*(math.pow(a + b, 2) - s)/(x + y)
