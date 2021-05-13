# Use mpmath (http://mpmath.org/) to generate the numbers to test
# against (i.e., assume mpmath's algorithms are correct).

import sys
import mpmath as mp
import decimal
from decimalmath import acos, asin, atan, decimal, half, log10, sqrt
from decimalmath import zero, one, two, three, pi, ln

from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

getcontext = decimal.getcontext
localcontext = decimal.localcontext
Dec = decimal.Decimal

def Test_pi():
    s = repr(mp.pi())
    x = eval(s.replace("mpf", "Dec"))
    assert_equal(pi(), x, reltol=eps)
    with localcontext() as ctx:
        # Value from wikipedia page on pi
        ctx.prec = 52
        # Truncate instead of round to second to last digit
        s_calc = str(pi())[:-1]
        s_exact = "3.14159265358979323846264338327950288419716939937510"
        assert_equal(s_calc, s_exact)

def Test_atan():
    assert_equal(atan(zero),            zero, reltol=eps)
    assert_equal(atan(Dec(3).sqrt()),   Pi/3, reltol=eps)
    assert_equal(atan(one),             Pi/4, reltol=eps)
    assert_equal(atan(-one),           -Pi/4, reltol=eps)
    assert_equal(atan(-Dec(3).sqrt()), -Pi/3, reltol=eps)

def Test_asin():
    assert_equal(asin(half),              Pi/6, reltol=eps)
    assert_equal(asin(-half),            -Pi/6, reltol=eps)
    assert_equal(asin(Dec(3).sqrt()/2),   Pi/3, reltol=eps)
    assert_equal(asin(-Dec(3).sqrt()/2), -Pi/3, reltol=eps)
    assert_equal(asin(zero),              zero, reltol=eps)
    assert_equal(asin(one),               Pi/2, reltol=eps)
    assert_equal(asin(-one),             -Pi/2, reltol=eps)
    raises(ValueError, asin, Dec(2))

def Test_acos():
    assert_equal(acos(zero),             Pi/2, reltol=eps)
    assert_equal(acos(half),             Pi/3, reltol=eps)
    assert_equal(acos(-half),            Pi/6 + Pi/2, reltol=eps)
    assert_equal(acos(Dec(3).sqrt()/2),  Pi/6, reltol=eps)
    assert_equal(acos(-Dec(3).sqrt()/2), Pi - Pi/6, reltol=eps)
    assert_equal(acos(one),              zero, reltol=eps)
    assert_equal(acos(-one),             Pi, reltol=eps)
    raises(ValueError, acos, Dec(2))

def Test_ln():
    s = repr(mp.log("0.5"))
    x = eval(s.replace("mpf", "decimal.Decimal"))
    assert_equal(ln(half), x, reltol=eps)
    assert_equal(ln(one),     zero, reltol=eps)
    s = repr(mp.log(mp.pi()/2))
    x = eval(s.replace("mpf", "decimal.Decimal"))
    assert_equal(ln(Pi/2), x, reltol=eps)
    s = repr(mp.log(10))
    x = eval(s.replace("mpf", "decimal.Decimal"))
    assert_equal(ln(Dec(10)), x, reltol=eps)
    raises(ValueError, ln, Dec(-1))

def Test_log10():
    assert_equal(log10(half), mp.log10("0.5"), reltol=eps)
    assert_equal(log10(one), zero, reltol=eps)
    assert_equal(log10(Pi/2), mp.log10(mp.pi()/2), reltol=eps)
    assert_equal(log10(Dec(10)), mp.log10(10), reltol=eps)
    raises(ValueError, log10, Dec(-1))

def Test_pow():
    assert_equal(pow(Dec(4), half),    two, reltol=eps)
    assert_equal(pow(two, -two),       one/Dec(4), reltol=eps)
    assert_equal(pow(-two, two),       Dec(4), reltol=eps)
    assert_equal(pow(-three, two),     Dec(9), reltol=eps)
    assert_equal(pow(-three, -two),    one/Dec(9), reltol=eps)
    assert_equal(pow(-three, three),   Dec(-27), reltol=eps)
    assert_equal(pow(-three, -three), -one/Dec(27), reltol=eps)
    raises(decimal.InvalidOperation, pow, Dec(-2), 1/Dec(3))

def Test_sqrt():
    assert_equal(sqrt(Dec(0)), zero, reltol=eps)
    assert_equal(sqrt(Dec(1)), one, reltol=eps)
    assert_equal(sqrt(Dec(4)), two, reltol=eps)
    assert_equal(sqrt(Dec(9)), three, reltol=eps)
    x = "88.325"
    assert_equal(sqrt(Dec(x)), mp.sqrt(mp.mpf(x)), reltol=eps)
    raises(ValueError, sqrt, -two)

mp.mp.dps = getcontext().prec
Pi = Dec(str(mp.pi()))  # Reference value of pi at current precision
eps = 10*Dec(10)**(-Dec(getcontext().prec))

if __name__ == "__main__":
    exit(run(globals())[0])
