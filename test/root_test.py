'''

Todo
    - TestBracketRoots doesn't follow stated plan
    
'''
if 1:   # Imports
    if 1:   # Standard imports
        from decimal import Decimal, getcontext
        from random import uniform, seed
        import cmath
        import math
        import numbers
        import sys
    if 1:   # Custom imports
        from root import (Bisection, BracketRoots, FindRoots, Brent, NewtonRaphson,
            Ostrowski, Pound, Ridders, Crenshaw, SearchIntervalForRoots)
        from root import Cubic, Quadratic, Quartic
        from lwtest import run, assert_equal, raises, Assert
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
        try:
            import pylab as pl
            have_pylab = True
        except ImportError:
            have_pylab = False
        if 1:   # Drop into debugger on unhandled exception
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        tol = 2e-15  # For testing float equality
if 1:   # Test root-finding routines
    def TestCrenshaw():
        '''Here's a quick test of the routine.  The function is
        the polynomial x^8 - 2 = 0; we should get as an answer the
        8th root of 2.  You should see the following output if
        show is nonzero:
        
        Calculated root = 1.090507732665258
        Correct value   = 1.090507732665258
        Num iterations  = 9
        
        Calculated root = 1.090507732665257659207010655760707978993
        Correct value   = 1.090507732665258
        Num iterations  = 14
        
        The long answer can be checked with integer arithmetic.
        '''
        def f(x):
            return x**8 - 2
        tol = 1e-10
        itmax = 20
        x0 = 0.0
        x1 = 10.0
        root, numits = Crenshaw(x0, x1, f, tol=tol, itmax=itmax)
        assert_equal(root, 1.090507732665258, reltol=tol)
        # Now do the same, but with Decimal numbers
        getcontext().prec = 50
        tol = Decimal("1e-48")
        x0, x1 = Decimal(0), Decimal(10)
        root, numits = Crenshaw(x0, x1, f, tol=tol, itmax=itmax, fp=Decimal)
        assert_equal(root**8, 2, reltol=tol)
        # Call a function that uses extra arguments
        def f(x, a, **kw):
            b = kw.setdefault("b", 8)
            return x**b - a
        tol = 1e-10
        itmax = 20
        x0 = 0.0
        x1 = 10.0
        a, b = 2, 8
        root, numits = Crenshaw(x0, x1, f, tol=tol, itmax=itmax, args=[a])
        assert_equal(root, math.pow(a, 1 / b))
        # Use keyword argument
        a, b = 3, 7
        root, numits = Crenshaw(x0, x1, f, tol=tol, itmax=itmax, args=[a], kw={"b": b})
        assert_equal(root, math.pow(a, 1 / b), reltol=tol)
    def TestFindRoots():
        # Show that FindRoots can do a reasonable job for a
        # polynomial.  Note the particular results are sensitive to
        # n.
        f = lambda x: (x - 1) * (x - 2) * (x - 3) * (x - 4) * (x - 5)
        x1, x2, n = 0, 10, 10
        r = FindRoots(f, n, x1, x2, tol=tol)
        Assert(r == tuple([1.0 * i for i in range(1, 6)]))
        # Roots of sinc function
        f = lambda x: math.sin(x) / x
        x1, x2, n = 1, 10, 100
        r = FindRoots(f, n, x1, x2, tol=tol)
        assert_equal(r[0], 1 * math.pi)
        assert_equal(r[1], 2 * math.pi)
        assert_equal(r[2], 3 * math.pi)
        # Same as previous, but with an extra parameter
        f = lambda x, a: math.sin(a * x) / (a * x)
        r = FindRoots(f, n, x1, x2, args=[1], tol=tol)
        assert_equal(r[0], 1 * math.pi)
        assert_equal(r[1], 2 * math.pi)
        assert_equal(r[2], 3 * math.pi)
        r = FindRoots(f, n, x1, x2, args=[math.pi], tol=tol)
        assert_equal(r[0], 1)
        assert_equal(r[1], 2)
        assert_equal(r[2], 3)
        # Same as previous, but with a keyword parameter
        def f(x, a=1):
            return math.sin(a * x) / (a * x)
        r = FindRoots(f, n, x1, x2, kw={"a": 1}, tol=tol)
        assert_equal(r[0], 1 * math.pi)
        assert_equal(r[1], 2 * math.pi)
        assert_equal(r[2], 3 * math.pi)
        r = FindRoots(f, n, x1, x2, kw={"a": math.pi}, tol=tol)
        assert_equal(r[0], 1)
        assert_equal(r[1], 2)
        assert_equal(r[2], 3)
    def TestNewtonRaphson():
        # Find the root of f(x) = tan(x) - 1 for 0 < x < pi/2.
        f = lambda x: math.tan(x) - 1
        fd = lambda x: 1 / math.cos(x)**2
        x = NewtonRaphson(0.5, f, fd, tol=tol)
        assert_equal(x, math.atan(1), reltol=1e-15)
    def TestSearchIntervalForRoots():
        # Find an interval containing the root of f(x) = tan(x) -
        # 1 for 0 < x < pi/2.
        f = lambda x: math.tan(x) - 1
        answer = math.atan(1)
        x1, x2 = 0, math.pi / 2
        intervals = SearchIntervalForRoots(x1, x2, f, 10)
        for start, end in intervals:
            Assert(start <= answer <= end)
        intervals = SearchIntervalForRoots(x1, x2, f, 1000)
        for start, end in intervals:
            Assert(start <= answer <= end)
    def TestBracketRoots():
        '''The polynomial f(x) = (x-r1)*(x-r2)*(x+r3) has three roots of r1, r2, -r3.
        Use BracketRoots() to find one of the roots.  Also demonstrate that it will
        exceed the iteration limit if the interval doesn't include any of the roots.
        '''
        r1, r2, r3 = 1000, 500, -500
        f = lambda x: (x - r1)*(x - r2)*(x + r3)
        r = BracketRoots(f, -2, -1)
        Assert((r[0] <= r1 <= r[1]) or (r[0] <= r2 <= r[1]) or (r[0] <= r3 <= r[1]))
        # Demonstate iteration limit can be reached
        f = lambda x: x - 1000000
        raises(ValueError, BracketRoots, f, -2, -1, itmax=10)
    def TestBisection():
        # Root of x = cos(x); it's 0.739085133215161 as can be found easily
        # by iteration on a calculator.
        f = lambda x: x - math.cos(x)
        tol = 1e-14
        root, numit = Bisection(0.7, 0.8, f, tol=tol)
        Assert(abs(root - 0.739085133215161) <= tol)
        # Eighth root of 2:  root of x**8 = 2
        f = lambda x: x**8 - 2
        tol = 1e-14
        root, numit = Bisection(1, 2, f, tol=tol)
        Assert(abs(root - math.pow(2, 1 / 8)) <= tol)
        # Simple quadratic equation
        t = 100001
        f = lambda x: (x - t) * (x + 100)
        tol = 1e-10
        root, numit = Bisection(0, 2.1 * t, f, tol=tol)
        Assert(abs(root - t) <= tol)
        # Note setting switch to True will cause an exception for this
        # case.
        raises(ValueError, Bisection, 0, 2.1 * t, f, tol=tol, switch=True)
    def TestRidders():
        # Root of x = cos(x); it's 0.739085133215161 as can be found easily
        # by iteration on a calculator.
        f = lambda x: x - math.cos(x)
        tol = 1e-14
        root, numit = Ridders(0.7, 0.8, f, tol=tol)
        Assert(abs(root - 0.739085133215161) <= tol)
        # Eighth root of 2:  root of x**8 = 2
        f = lambda x: x**8 - 2
        tol = 1e-14
        root, numit = Ridders(1, 2, f, tol=tol)
        Assert(abs(root - math.pow(2, 1 / 8)) <= tol)
        # Simple quadratic equation
        t = 100001
        f = lambda x: (x - t) * (x + 100)
        tol = 1e-10
        root, numit = Ridders(0, 2.1 * t, f, tol=tol)
        Assert(abs(root - t) <= tol)
    def TestGeneralRootFinding(show=(len(sys.argv) > 1)):
        '''This test case uses each of the root finding functions to test a
        practical example of finding the square root of numbers over a wide
        floating point range.  The desire is to have convergence to the
        correct value within a relative tolerance of 1e-6, which should fit
        the needs for most any numerical calculation based on
        physically-measured data.
        '''
        tol = 1e-6
        fd = lambda x: 1/(2*x**0.5)
        # The stopping point is 10**(308//2) because this is about the square
        # root of largest floating point number.  Note some of the routines
        # won't converge over this full range.
        seed(0)
        e, bi, cr, rf, br, ri = [], [], [], [], [], []
        for i in range(308//2):
            e.append(i)
            val = float(10**i)
            sr0 = math.sqrt(val)
            a, b = sr0*(1 - uniform(0, 0.2)), sr0*(1 + uniform(0, 0.2))
            f = lambda x: x*x - val
            sr, n = Bisection(a, b, f, tol=tol)
            bi.append("%3d " % n)
            assert_equal(sr0, sr, reltol=tol)
            if 0:   # Crenshaw is commented out in root.py and probably will be removed
                sr, n = Crenshaw(a, b, f, tol=tol)
                cr.append("%3d " % n)
                assert_equal(sr0, sr, reltol=tol)
            try:
                sr, n = RootFinder(a, b, f, tol=tol)
                rf.append("%3d " % n)
                assert_equal(sr0, sr, reltol=tol)
            except Exception as E:
                pass
            try:
                sr, n = Brent(a, b, f, tol=tol)
                Br.append("%3d " % n)
                assert_equal(sr0, sr, reltol=tol)
            except Exception as E:
                pass
            try:
                sr, n = Brent(a, b, f, tol=tol)
                br.append("%3d " % n)
                assert_equal(sr0, sr, reltol=tol)
            except Exception as E:
                pass
            sr, n = Ridders(a, b, f, tol=tol)
            assert_equal(sr0, sr, reltol=tol)
            ri.append("%3d " % n)
        # Make a plot of the results
        if have_pylab:
            p = pl.semilogy
            p(e[: len(bi)], bi, ".-", label="Bisection")
            p(e[: len(cr)], cr, ".-", label="Crenshaw")
            p(e[: len(rf)], rf, ".-", label="RootFinder")
            p(e[: len(br)], br, ".-", label="Brent")
            p(e[: len(ri)], ri, ".-", label="Ridders")
            pl.title("Root-finding routine efficiency\n13 Oct 2014")
            pl.xlabel("n")
            pl.ylabel("Iterations to get sqrt(10**n)")
            pl.legend(loc="upper left")
            if 0:
                pl.show()
            else:
                pl.savefig("rootfinder_comparison.png")
    def TestOstrowski():
        from math import sin, cos, exp
        tol = 1e-14
        # Square root of 2
        x0 = 3
        f = lambda x: x**2 - 2
        deriv = lambda x: 2 * x
        root = 2**0.5
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=tol)
        # Shamir's first example
        x0 = 3
        f = lambda x: x**3 + 4 * x**2 - 15
        deriv = lambda x: 3 * x**2 + 8 * x
        root = 1.6319808055661
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=4e-14)
        # Shamir's 3rd example
        x0 = 1.1
        f = lambda x: sin(x) - x / 2
        deriv = lambda x: cos(x) - 1 / 2
        root = -1.8954942670340
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=2e-14)
        # Shamir's 5th example
        x0 = 10
        f = lambda x: cos(x) - x
        deriv = lambda x: -sin(x) - 1
        root = 0.73908513321516
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=tol)
        # Shamir's 6th example
        x0 = 0.1
        f = lambda x: sin(x) ** 2 - x**2 + 1
        deriv = lambda x: 2 * sin(x) * cos(x) - 2 * x
        root = 1.4044916482153
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=8e-13)
        # Shamir's 7th example
        x0 = 0.1
        f = lambda x: exp(-x) + cos(x)
        deriv = lambda x: -exp(-x) - sin(x)
        root = 1.7461395304080
        r, n = Ostrowski(x0, f, deriv, tol=tol)
        assert_equal(r, root, reltol=tol)
if 1:   # Test polynomial root-finding routines
    def TestQuadratic():
        # Exception if not quadratic
        raises(ValueError, Quadratic, *(0, 1, 1))
        # Real roots
        r1, r2 = Quadratic(1, 0, -2)
        assert_equal(r1, -r2)
        assert_equal(abs(r1), math.sqrt(2))
        # Complex roots
        r1, r2 = Quadratic(1, 0, 2)
        assert_equal(r1, -r2)
        assert_equal(r1, cmath.sqrt(-2))
        # Constant term 0
        r1, r2 = Quadratic(1, -1, 0)
        assert_equal(r1, 1)
        assert_equal(r2, 0j)
        # Real, distinct
        r1, r2 = Quadratic(1, 4, -21)
        Assert(r1 == 3)
        Assert(r2 == -7)
        # Real coefficients, complex roots
        r1, r2 = Quadratic(1, -4, 5)
        assert_equal(r1, 2 + 1j)
        assert_equal(r2, 2 - 1j)
        # Complex coefficients, complex roots
        r1, r2 = Quadratic(1, 3 - 3j, 10 - 54j)
        assert_equal(r1, (3 + 7j))
        assert_equal(r2, (-6 - 4j))
    def TestCubic():
        # Exception if not cubic
        raises(ValueError, Cubic, *(0, 1, 1, 1))
        # Basic equation
        r = Cubic(1, 0, 0, 0)
        Assert(r == (0, 0, 0))
        # Cube roots of 1
        for r in Cubic(1, 0, 0, -1):
            assert_equal(Pound(r**3, ratio=tol), 1, reltol=tol)
        # Cube roots of -1
        for r in Cubic(1, 0, 0, 1):
            assert_equal(Pound(r**3, ratio=tol), -1, reltol=tol)
        # Three real roots:  (x-1)*(x-2)*(x-3)
        for i, j in zip(Cubic(1, -6, 11, -6), (3, 1, 2)):
            assert_equal(i, j, reltol=tol)
        # One real root:  (x-1)*(x-j)*(x+j) = x**3 - x**2 + x - 1, roots = 1, -j, j
        for i, k in zip(Cubic(1, -1, 1, -1), (1, 1j, -1j)):
            # In the following, Assert is used instead of assert_equal
            # because one test case results in -0-1j vs. -1j, which results
            # in a failure -- but the numbers are numerically equal.
            Assert(i == k)
    def TestQuartic():
        # Exception if not cubic
        raises(ValueError, Quartic, *(0, 1, 1, 1, 1))
        # Basic equation
        r = Quartic(1, 0, 0, 0, 0)
        Assert(r == (0, 0, 0, 0))
        # Fourth roots of 1
        for r in Quartic(1, 0, 0, 0, -1):
            assert_equal(r**4, 1)
        # Fourth roots of -1
        for r in Quartic(1, 0, 0, 0, 1):
            assert_equal(Pound(r**4, ratio=tol), -1, reltol=tol)
        # The equation (x-1)*(x-2)*(x-3)*(x-4)
        for i, j in zip(Quartic(1, -10, 35, -50, 24), range(1, 5)):
            assert_equal(i, j, reltol=tol)
        # Two real roots: x*(x-1)*(x-j)*(x+j)
        for i, k in zip(Quartic(1, -1, 1, -1, 0), (-1j, 1j, 0j, 1)):
            assert_equal(i, k)
if 1:   # Test utility
    def TestPound():
        '''Pound(z) returns a pure real or imaginary if z is close enough to
        the real or imaginary axis.
        '''
        def test1():
            Assert(Pound(0, True) == 0)
            Assert(Pound(1 + 1j, True) == 1 + 1j)
            for z, expected, t in (
                (1 + 0j, 1, numbers.Real),
                (1 - 0j, 1, numbers.Real),
                (-1 + 0j, -1, numbers.Real),
                (-1 - 0j, -1, numbers.Real),
                #
                (1 + 1e-16j, 1, numbers.Real),
                (1 - 1e-16j, 1, numbers.Real),
                (-1 + 1e-16j, -1, numbers.Real),
                (-1 - 1e-16j, -1, numbers.Real),
                #
                (1e-16 + 1e-32j, 1e-16, numbers.Real),
                (1e-16 - 1e-32j, 1e-16, numbers.Real),
                (-1e-16 + 1e-32j, -1e-16, numbers.Real),
                (-1e-16 - 1e-32j, -1e-16, numbers.Real),
                #
                (0 + 1j, 1j, numbers.Complex),
                (0 - 1j, -1j, numbers.Complex),
                (-0 + 1j, 1j, numbers.Complex),
                (-0 - 1j, -1j, numbers.Complex),
                #
                (1e-16 + 1j, 1j, numbers.Complex),
                (1e-16 - 1j, -1j, numbers.Complex),
                (-1e-16 + 1j, 1j, numbers.Complex),
                (-1e-16 - 1j, -1j, numbers.Complex),
            ):
                b = Pound(z)
                Assert(b == expected)
                Assert(isinstance(b, t))
        def test2():
            epsilon = 2.5e-15
            tol = 0.99 * float(epsilon)
            # Zero
            Assert(Pound(0, 0) == 0)
            Assert(Pound(0j, 1) == 0)
            Assert(Pound(0 + 0j, 1) == 0)
            # Pure real
            Assert(Pound(1, 0) == 1)
            Assert(Pound(1, 1) == 1)
            Assert(Pound(1 + tol, 1) == 1 + tol)
            # Pure imaginary
            Assert(Pound(1j, 0) == 1j)
            Assert(Pound(1j, 1) == 1j)
            x = (1 + tol) * 1j
            Assert(Pound(x, 1) == x)
            # Real with small imaginary part
            x = 1
            y = x + tol * 1j
            Assert(Pound(y, 0) == y)
            Assert(Pound(y, 1) == x)
            # Imaginary with small real part
            y = tol + x * 1j
            Assert(Pound(y, 0) == y)
            Assert(Pound(y, 1) == x * 1j)
            # Number that shouldn't be changed
            x = 1 + 1j
            Assert(Pound(x, 0) == x)
            Assert(Pound(x, 1) == x)
        test1()
        test2()

if __name__ == "__main__":
    exit(run(globals(), halt=True)[0])
