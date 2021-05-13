import sys
from cuncertainties import *
from lwtest import run, assert_equal, raises
from pdb import set_trace as xx

eps = 1e-15
ii = isinstance

def cufloat_rel_eq(a, b, eps=eps):
    '''a and b are cufloats.  Return True if they are less than
    eps apart in the complex plane.
    '''
    assert(ii(a, cufloat))
    assert(ii(b, cufloat))
    if a:
        return True if abs(abs(b - a)/a) < eps else False
    elif b:
        return True if abs(abs(b - a)/b) < eps else False
    else:
        return True
def float_rel_eq(a, b, eps=eps):
    assert(ii(a, (int, long, float)))
    assert(ii(b, (int, long, float)))
    if a:
        return True if abs(b - a)/a < eps else False
    elif b:
        return True if abs(b - a)/b < eps else False
    else:
        return True
def non_rv_equal(a, b, eps=eps):
    '''a is a cufloat object and b is a regular python complex
    number.  Ensure that their real and imaginary parts are equal
    within a relative amount of eps.
    '''
    assert ii(a, cufloat) and ii(b, complex)
    a_re = a.real.nominal_value
    a_im = a.imag.nominal_value
    assert a.real.std_dev == 0
    assert a.imag.std_dev == 0
    return (float_rel_eq(a_re, b.real) and 
        float_rel_eq(a_im, b.imag))
def Test_functions():
    '''Use the corresponding methods of cmath to check basic
    behavior on numbers that have no uncertainty.  We should have
    identical results.
    '''
    x, y = -1.3, 2.7
    z = complex(x, y)
    zu = cufloat(x, 0, y, 0)
    non_rv_equal(zu, z)
    float_rel_eq(phase(zu).nominal_value, cmath.phase(z))
    r1, t1 = polar(zu)
    r2, t2 = cmath.polar(z)
    float_rel_eq(r1.nominal_value, r2)
    float_rel_eq(t1.nominal_value, t2)
    x1, y1 = rect(r1, t1)
    z2 = cmath.rect(r2, t2)
    float_rel_eq(x1.nominal_value, z2.real)
    float_rel_eq(y1.nominal_value, z2.imag)
    for f in (
        (exp, cmath.exp),
        (log, cmath.log),
        (log10, cmath.log10),
        (sqrt, cmath.sqrt),
        (acos, cmath.acos),
        (asin, cmath.asin),
        (atan, cmath.atan),
        (cos, cmath.cos),
        (sin, cmath.sin),
        (tan, cmath.tan),
        (acosh, cmath.acosh),
        (asinh, cmath.asinh),
        (atanh, cmath.atanh),
        (cosh, cmath.cosh),
        (sinh, cmath.sinh),
        (tanh, cmath.tanh),
    ):
        non_rv_equal(f[0](zu), f[1](z))
def Test_trig():
    '''Check with some real values via the math module.
    '''
    for x in (0.01, 0.1, 0.5, 0.99, 1, 1.01, math.pi/2):
        assert(abs(sin(x) - cufloat(math.sin(x))) < eps)
        assert(abs(cos(x) - cufloat(math.cos(x))) < eps)
        assert(abs(tan(x) - cufloat(math.tan(x))) < eps)
        assert(abs(sinh(x) - cufloat(math.sinh(x))) < eps)
        assert(abs(cosh(x) - cufloat(math.cosh(x))) < eps)
        assert(abs(tanh(x) - cufloat(math.tanh(x))) < eps)
    # Check with some complex values via the cmath module
    for y in (0.01, 0.1, 0.5, 0.99, 1, 1.01, math.pi/2):
        x = complex(y, 1)
        z = cmath.sin(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(sin(x) - v) < eps)
        z = cmath.cos(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(cos(x) - v) < eps)
        z = cmath.tan(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(tan(x) - v) < eps)
        z = cmath.sinh(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(sinh(x) - v) < eps)
        z = cmath.cosh(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(cosh(x) - v) < eps)
        z = cmath.tanh(x)
        v = cufloat(z.real, 0, z.imag)
        assert(abs(tanh(x) - v) < eps)
def Test_inv_trig():
    '''Check with some real values via the math/cmath modules.
    '''
    for x in (0.01, 0.1, 0.5, 0.99, 1):
        assert(abs(asin(x) - cufloat(math.asin(x))) < eps)
        assert(abs(acos(x) - cufloat(math.acos(x))) < eps)
        assert(abs(atan(x) - cufloat(math.atan(x))) < eps)
        assert(abs(asinh(x) - cufloat(math.asinh(x))) < eps)
        if x != 1:
            assert(abs(atanh(x) - cufloat(math.atanh(x))) < eps)
        z = cmath.acosh(x)
        assert(abs(acosh(x) - cufloat(z.real, 0, z.imag)) < eps)
def Test_properties():
    '''Check that we can read the properties.
    '''
    r, i, f = 1, 2, 3.0
    x = cufloat(r, 0, i, 0)
    assert(x.real == r)
    assert(x.imag == i)
    # Show we can also set the property value
    # int
    x.imag = i*i
    assert(x.imag == i*i)
    # float
    x.imag = f
    assert(x.imag == f)
    # ufloat
    y = ufloat(3, 8)
    x.imag = y
    assert(x.imag == y)
def Test_identities():
    '''Show that finv(f(x)) is x.
    '''
    # Note:  limit the maximum value, as the roundoff error for
    # the cosine increases as this maximum value increases.
    for z in (
        cufloat(0.1),
        cufloat(0.5),
        cufloat(1),
        cufloat(2),
    ):
        assert(abs(z - sin(asin(z))) <= eps)
        assert(abs(z - cos(acos(z))) <= eps)
        assert(abs(z - tan(atan(z))) <= eps)
        assert(abs(z - sinh(asinh(z))) <= eps)
        assert(abs(z - cosh(acosh(z))) <= eps)
        if z != one:
            assert(abs(z - tanh(atanh(z))) <= eps)
def Test_equality():
    '''Integer and float initialization should result in the same
    numbers.
    '''
    x = cufloat(1, 2, 3, 4)
    y = cufloat(1.0, 2.0, 3.0, 4.0)
    z = cufloat(1.0, 2.0, 3.0, 4.0 + eps)
    assert(x == x.copy())
    assert(x == y)
    assert(x != z)
def Test_arithmetic():
    x = cufloat(1, 0, 2, 0)
    y = cufloat(3, 0, 4, 0)
    assert_equal(x + y, cufloat(4, 0, 6, 0))
    assert_equal(y - x, cufloat(2, 0, 2, 0))
    assert_equal(x*y, cufloat(-5, 0, 10, 0))
    assert_equal(x/y, cufloat(0.44, 0, 0.08, 0))
    # Now with small but nonzero uncertainties
    a = 1000
    x = cufloat(1, 1/a, 2, 2/a)
    y = cufloat(3, 3/a, 4, 4/a)
    sx, sy = 0.0031622776601683794, 0.004472135954999579
    assert_equal(x + y, cufloat(4, sx, 6, sy))
    assert_equal(y - x, cufloat(2, sx, 2, sy))
    #
    sx = 0.012083045973594572
    sy = 0.01019803902718557 
    prod = x*y
    ans = cufloat(-5, sx, 10, sy)
    # This comparison is needed for python 2.7 (4th one fails if not
    # done this way).
    assert_equal(prod.real.nominal_value, ans.real.nominal_value)
    assert_equal(prod.real.std_dev, ans.real.std_dev)
    assert_equal(prod.imag.nominal_value, ans.imag.nominal_value)
    assert_equal(prod.imag.std_dev, ans.imag.std_dev, abstol=1e-15)
    #
    sx, sy = 0.0004633319328516005, 0.000430492183436587
    assert_equal(x/y, cufloat(0.44, sx, 0.08, sy))
def Test_init():
    z = cufloat(0)
    z = cufloat(long(0))
    z = cufloat(0.0)
    z = cufloat(1)
    z = cufloat(long(1))
    z = cufloat(1.0)
    z = cufloat(1, 2)
    z = cufloat(1, 2, 3)
    z = cufloat(1, 2, 3, 4)
    raises(TypeError, cufloat, 1j)
    raises(TypeError, cufloat, ufloat(1, 1))
    raises(TypeError, cufloat, cufloat(1))

if __name__ == "__main__":
    exit(run(globals())[0])
