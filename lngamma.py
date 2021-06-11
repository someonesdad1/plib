if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2008 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Lanczos' formula to calculate ln of gamma function
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import math
    import cmath
def lngamma(z):
    '''Routine to calculate the logarithm of the gamma function.
    Translated from C.  See page 160 of "Numerical Recipes".  This is
    Lanczos' remarkable formula.  |error| < 2e-10 everywhere Re x > 0.
    '''
    stp = 2.50662827465
    if isinstance(z, complex):
        if z.real <= 0:
            raise ValueError("Argument's real part must be > 0")
        x = z - 1
        tmp = x + 5.5
        tmp = (x + 0.5)*cmath.log(tmp) - tmp
        ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) +
               24.01409822/(x + 3) - 1.231739516/(x + 4) +
               0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
        return tmp + cmath.log(stp*ser)
    else:
        if z <= 0:
            raise ValueError("Argument must be > 0")
        x = z - 1
        tmp = x + 5.5
        tmp = (x + 0.5)*math.log(tmp) - tmp
        ser = (1 + 76.18009173/(x + 1) - 86.50532033/(x + 2) +
               24.01409822/(x + 3) - 1.231739516/(x + 4) +
               0.120858003e-2/(x + 5) - 0.536382e-5/(x + 6))
        return tmp + math.log(stp*ser)
if __name__ == "__main__": 
    from frange import frange
    from lwtest import run, assert_equal, raises
    import sys
    import color as C
    # Color for warnings
    yel, norm = C.fg(C.yellow, s=1), C.normal(s=1)
    def TestReal():
        tol = 1e-10
        for x, value in ((1, 1),
                        (1.1, 0.9513507699),
                        (1.61, 0.8946806085)):
            assert(math.fabs(math.exp(lngamma(x)) - value) < tol)
        assert(math.fabs(lngamma(100) - 359.13420537) < 1e-7)
        # If we are running under python 3, then the math library has lgamma
        # which we can test against.
        tol = 2e-9
        for x in frange("0.1", "10", "0.1"):
            y = lngamma(x)
            y0 = math.lgamma(x)
            if not y0:
                assert(y < tol)
            else:
                assert_equal(lngamma(x), math.lgamma(x), reltol=tol)
    def TestComplex():
        # Use mpmath for complex value standards
        try:
            from mpmath import ln, gamma
        except ImportError:
            print(f"{yel}Warning:  TestComplex in lngamma_test.py not run{norm}")
            return
        start, stop, step = 0, 10, 1
        eps = 3e-10
        for r in frange(start + step, stop, step):
            for i in frange(start + step, stop, step):
                z = complex(r, i)
                got = lngamma(z)
                expected = ln(gamma(z))
                diff = abs(got-expected)
                if diff > 1:    # Correct for phase difference of n*pi
                    diff -= round(diff/math.pi, 6)*math.pi
                assert(diff <= eps)
    exit(run(globals(), halt=1)[0])
