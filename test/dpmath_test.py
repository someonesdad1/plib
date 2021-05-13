import math
from lwtest import run, assert_equal
from dpmath import polyeval, polyderiv, polyreduce, rect, polar
from dpmath import isqrt, AlmostEqual

eps = 1e-15

def test_polyeval():
    assert(polyeval((3, 2, 1), 6) == 51)

def test_polyderiv():
    assert(polyderiv((3, 2, 1)) == [2, 2])

def test_polyreduce():
    # Use (x - 1)*(x - 2) = 2 - 3*x + x**2
    p = (2, -3, 1)
    assert(polyreduce(p, 1) == [-2, 1])

def test_rect():
    assert(rect(0, 0) == (0, 0))
    assert(rect(0, 180, deg=True) == (0, 0))
    x, y = rect(1, 45, deg=True)
    s = math.sin(math.pi/4)
    assert_equal(x, s, abstol=eps)
    assert_equal(y, s, abstol=eps)

def test_polar():
    assert(polar(0, 0) == (0, 0))
    assert(polar(0, 1) == (1, math.pi/2))
    assert(polar(0, -1) == (1, -math.pi/2))
    assert(polar(-1, 0) == (1, math.pi))
    s = math.sin(math.pi/4)
    r, theta = polar(s, s, deg=True)
    assert_equal(r, 1, abstol=eps)
    assert_equal(theta, 45, abstol=eps)

def test_isqrt():
    n0 = 123456789
    n = n0
    while n < n0**8:
        assert(isqrt(n*n) == n)
        n = 3*n//2

if __name__ == "__main__":
    exit(run(globals())[0])
