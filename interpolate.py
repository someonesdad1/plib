'''
Interpolation routines
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
    # Interpolation routines
    #∞what∞#
    #∞test∞# Put test file information here (see 0test.py) #∞test∞#
    pass
if 1:  # Imports
    import bisect
def LagrangeInterpolation(x, X, Y, strict=False):
    '''Page 32 of Meeus, "Astronomical Algorithms", 2nd ed.  Given x, an
    abscissa, calculates the interpolated value y = f(x) where f(x) is
    Lagrange's interpolating polynomial.  X and Y are expected to be
    sequences of the same size such that Y[i] = f(X[i]).  If strict is
    true, then you'll get an exception if you try to interpolate outside
    the range of abscissas given in X.
    '''
    n = len(X)
    if len(Y) != n:
        raise ValueError("len(X) != len(Y)")
    if len(set(X)) != n:
        raise ValueError("X's values are not unique")
    if strict:
        if x < min(X) or x > max(X):
            raise ValueError("x value is outside of interpolation range")
    y = 0
    for i in range(n):
        terms = 1
        for j in range(n):
            if i == j:
                continue
            terms *= (x - X[j])/(X[i] - X[j])
        y += terms*Y[i]
    return y
def LinearInterp(x, X, Y, inv=False, check=False):
    '''Given two sequences X and Y, use linear interpolation to find the y
    value corresponding to x.  If inv is True, find the abscissa
    corresponding to the y value = x.  X and Y must have an equal number of
    elements and X must be in sorted order.  A ValueError exception will be
    raised if there's no associated value or x is out of range.
 
    If check is True, verify that X and Y are sorted and have an equal
    number of elements.
    '''
    def find_le(a, x):
        'Return index of rightmost value less than or equal to x'
        i = bisect.bisect_right(a, x)   # From bisect manpage
        if i:
            return i - 1
        raise ValueError("{} not found in sequence".format(str(x)))
    if check:
        if len(X) != len(Y) or not X:
            raise ValueError("Arrays not same size or are empty")
        n = len(X)
        for i in range(n - 1):
            if X[i] > X[i + 1]:
                raise ValueError("X[{}] > X[{}] (X isn't sorted)".format(i, i + 1))
    if inv:
        if x < Y[0] or x > Y[-1]:
            raise ValueError("{} not found in sequence Y".format(str(x)))
        i = find_le(Y, x)
        if i == len(Y) - 1:
            return X[-1]
        x0, y0 = Y[i], X[i]
        x1, y1 = Y[i + 1], X[i + 1]
    else:
        if x < X[0] or x > X[-1]:
            raise ValueError("{} not found in sequence X".format(str(x)))
        i = find_le(X, x)
        if i == len(X) - 1:
            return Y[-1]
        x0, y0 = X[i], Y[i]
        x1, y1 = X[i + 1], Y[i + 1]
    assert(x0 <= x < x1)
    frac = (x - x0)/(x1 - x0)
    return y0 + frac*(y1 - y0)
if __name__ == "__main__": 
    from math import pi, sin
    from lwtest import run, raises, assert_equal
    from frange import frange
    def eq(x, y, relative_error=1e-12):
        if x == y:
            return True
        try:
            z = abs((x - y)/float(y))
        except ZeroDivisionError:
            try:
                z = abs((y - x)/float(x))
            except ZeroDivisionError:
                raise ValueError("Both arguments are zero")
        return True if z < relative_error else False
    def TestLagrange():
        li, X0, tol = LagrangeInterpolation, 10, 1e-12
        # Try a simple fit to a quadratic
        X = range(X0)
        Y, offsets = [i*i for i in X], frange("0", 1, "0.1")
        for i in X:
            for offset in offsets:
                x = i + offset
                y = li(x, X, Y)
                assert_equal(y, x**2, reltol=tol)
        # Interpolation for a sinusoid
        X = list(frange(0, 2*pi, 0.1))
        Y, offsets = [sin(i) for i in X], frange(0, 1, 0.1)
        for i in range(5):
            for offset in offsets:
                x = i + offset
                y = li(x, X, Y)
                assert_equal(y, sin(x), reltol=tol)
    def TestLinearInterp():
        X = [0, 1, 2]
        Y = [1, 2, 3]
        # Test normal interpolation
        assert_equal(LinearInterp(0.0, X, Y, inv=0, check=1), 1)
        assert_equal(LinearInterp(0.5, X, Y, inv=0), 1.5)
        assert_equal(LinearInterp(1.5, X, Y, inv=0), 2.5)
        assert_equal(LinearInterp(2.0, X, Y, inv=0), 3)
        # Test inverse interpolation
        assert_equal(LinearInterp(1.0, X, Y, inv=1), 0)
        assert_equal(LinearInterp(1.5, X, Y, inv=1), 0.5)
        assert_equal(LinearInterp(2.5, X, Y, inv=1), 1.5)
        assert_equal(LinearInterp(3.0, X, Y, inv=1), 2)
        # Normal out-of-bounds
        raises(ValueError, LinearInterp, -1, X, Y)
        raises(ValueError, LinearInterp, 2.01, X, Y)
        # Inverse out-of-bounds
        raises(ValueError, LinearInterp, 0.99, X, Y, inv=1)
        raises(ValueError, LinearInterp, 3.01, X, Y, inv=1)
        # Empty sequences
        X = []
        Y = []
        raises(ValueError, LinearInterp, 0.5, X, Y, inv=0, check=1)
        raises(ValueError, LinearInterp, 0.5, X, Y, inv=1, check=1)
        # Unequal sequence lengths
        X = [0, 1]
        Y = [1, 2, 3]
        raises(ValueError, LinearInterp, 0.5, X, Y, inv=0, check=1)
        raises(ValueError, LinearInterp, 0.5, X, Y, inv=1, check=1)
    exit(run(globals(), halt=1)[0])
