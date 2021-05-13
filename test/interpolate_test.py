from interpolate import LagrangeInterpolation, LinearInterp
from math import pi, sin
from lwtest import run, raises, assert_equal
from frange import frange

# Run some tests
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

if __name__ == "__main__":
    exit(run(globals())[0])
