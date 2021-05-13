import math
from frange import frange
from lngamma import lngamma
from lwtest import run, assert_equal, raises
import sys

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
        print("Warning:  TestComplex in lngamma_test.py not run")
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

if __name__ == "__main__":
    exit(run(globals())[0])
