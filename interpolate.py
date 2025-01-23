'''
Interpolation routines
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <math> Lagrange and linear interpolation routines
        #∞what∞#
        #∞test∞# run #∞test∞#
        pass
    if 1:  # Imports
        import bisect
    if 1:  # Local imports
        from f import flt
if 1:  # Core functionality
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
    def LinearInterp(x, X, Y, inv=False, check=False, ret_type=flt):
        '''Given two sequences X and Y, use linear interpolation to find the y
        value corresponding to x.  If inv is True, find the abscissa
        corresponding to the y value = x.  X and Y must have an equal number of
        elements and X must be in sorted order.  
        
        A ValueError exception will be raised if there's no associated value or x
        is out of range.
        
        If check is True, verify that X is sorted and that X and Y have an
        equal number of elements.
        
        ret_type is the number type to return.  It must be initializable from a float.
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
                return ret_type(X[-1])
            x0, y0 = Y[i], X[i]
            x1, y1 = Y[i + 1], X[i + 1]
        else:
            if x < X[0] or x > X[-1]:
                raise ValueError("{} not found in sequence X".format(str(x)))
            i = find_le(X, x)
            if i == len(X) - 1:
                return ret_type(Y[-1])
            x0, y0 = X[i], Y[i]
            x1, y1 = X[i + 1], Y[i + 1]
        assert(x0 <= x < x1)
        frac = (x - x0)/(x1 - x0)
        return ret_type(y0 + frac*(y1 - y0))
    def LinearInterpFunction(X, Y, ret_type=flt):
        '''Return a function that returns the linearly-interpolated value for
        the function Y(X).  X does not need to be sorted.
        '''
        # Make sure X is sorted
        x, y = zip(*sorted(zip(X, Y)))
        a = LinearInterp(x[0], x, y, check=True, ret_type=ret_type)
        def Func(arg):
            return LinearInterp(arg, x, y, ret_type=ret_type)
        return Func

if __name__ == "__main__": 
    from math import pi, sin, fabs
    from lwtest import run, raises, assert_equal
    from frange import frange
    ii = isinstance
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
        # Page 34 of Meeus:  Lagrangian interpolation
        X = [29.43, 30.97, 27.69, 28.11, 31.58, 33.05]
        Y = [0.4913598528, 0.5145891926, 0.4646875083, 0.4711658342,
            0.5236885653, 0.5453707057]
        d = LagrangeInterpolation(30, X, Y)
        assert(fabs(d - 1/2.) < 1e-9)
        d = LagrangeInterpolation(0, X, Y)
        assert(fabs(d - 0.0000482) < 1e-5)
        d = LagrangeInterpolation(90, X, Y)
        assert(fabs(d - 1.00007) < 2e-4)
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
    def TestLinearInterpWithType():
        X = [0, 1, 2]
        Y = [1, 2, 3]
        # Test with integers
        x = LinearInterp(2.0, X, Y, ret_type=int)
        assert(x == 3)
        assert(ii(x, int))
    def TestLinearInterpFunction():
        X = (0, 1)
        Y = (0.5, 1.5)
        f = LinearInterpFunction(X, Y)
        assert_equal(f(0), 0.5)
        assert_equal(f(0.5), 1)
        assert_equal(f(1), 1.5)
        raises(ValueError, f, 1.01)
        # Test you can get an integer
        f = LinearInterpFunction(X, Y, ret_type=int)
        assert(f(0.5) == 1)
        assert(ii(f(0.5), int))
        assert(f(1) == 1)
        assert(ii(f(1), int))
    exit(run(globals(), halt=1)[0])
