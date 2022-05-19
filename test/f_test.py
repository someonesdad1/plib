from fractions import Fraction
import cmath
import decimal
import f
import io
import math
import operator as op
import sys

# Custom libraries
from lwtest import run, raises, assert_equal
from color import TRM as t
t.r = t("redl")
try:
    import numpy
    _have_numpy = True
except ImportError:
    _have_numpy = False
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()

flt, cpx, Base = f.flt, f.cpx, f.Base
filename = __file__
pi = f.pi    # Handy constant
ii = isinstance

def Assert(x):  # Because the assert statement can't be overridden
    'Drop into debugger if script has an argument'
    if len(sys.argv) > 1 and not x:
        xx()
    else:
        assert(x)

def Init(n=1):
    '''Make sure test environment is set up and return convenience
    instances.
    '''
    x = flt(pi)
    if n == 2:
        z = cpx(pi, 1/pi)
    # Set attributes of flt and cpx to known values
    x.f = False
    x.n = 3
    x.x = False
    cpx.i = False
    return x if n == 1 else (x, z)

def TestBasics():
    x = Init()
    Assert(x == pi)
    x.n = 3
    Assert(str(x) == "3.14")
    x.n = 4
    Assert(str(x) == "3.142")
    Assert(repr(x) == repr(math.pi))
    # Check flipped behavior
    x.f = True
    x.n = 3
    Assert(repr(x) == "3.14")
    x.n = 4
    Assert(repr(x) == "3.142")
    Assert(str(x) == repr(math.pi))

def TestAttributes():
    def Test_f():   # Flips str() and repr()
        x, z = Init(2)
        x.f = False
        P, Z = float(pi), complex(z)
        Assert(str(x) == x.s)
        Assert(repr(x) == repr(P) == x.r)
        Assert(str(z) == z.s)
        rz =     '3.141592653589793+0.3183098861837907j'
        rZ =    '(3.141592653589793+0.3183098861837907j)'
        zdotr = "'3.141592653589793+0.3183098861837907j'"
        Assert(repr(z) == rz)
        Assert(repr(Z) == rZ)
        Assert(repr(z.r) == zdotr)
        x.f = True
        Assert(str(x) == x.r)
        Assert(repr(x) == x.s)
        Assert(str(z) == z.r)
        Assert(repr(z) == z.s)
    def Test_h():   # Returns the help string
        x, z = Init(2)
        for i in (x, z):
            so = sys.stdout
            sys.stdout = io.StringIO()
            i.h     # Prints to stdout
            got = sys.stdout.getvalue()
            sys.stdout = so
            Assert(len(got.split("\n")) > 3)
    def Test_n():   # Sets number of significant figures
        'Note n can be 0 or None (both imply 15 digits)'
        x = Init()
        x.n = None
        Assert(str(x) == str(pi))
        x.n = 0
        Assert(str(x) == str(pi))
        for i, expected in ((4, "3.142"), (8, "3.1415927")):
            x.n = i
            Assert(str(x) == expected == x.s)
            Assert(repr(x) == repr(pi) == x.r)
        # Get expected exceptions
        for i in ("3", "0.1", "0.0", 1j):
            with raises(ValueError):
                x.n = i
    def Test_r():   # Returns repr() of the number, regardles of f attribute
        x, z = Init(2)
        expected = repr(x)
        x.f = False
        Assert(x.r == expected)
        x.f = True
        Assert(x.r == expected)
        x.f = False
        # The cpx repr doesn't have parentheses like complex does
        expected = repr(z).replace("(", "").replace(")", "")
        z.f = False
        Assert(z.r == expected)
        z.f = True
        Assert(z.r == expected)
        z.f = False
    def Test_s():   # Returns str() of the number, regardles of f attribute
        x, z = Init(2)
        x.f = False
        xs, xr, zs, zr = x.s, x.r, z.s, z.r
        for I, Is, Ir in ((x, xs, xr), (z, zs, zr)):
            I.f = False
            Assert(I.s == Is)
            Assert(str(I) == Is)
            Assert(repr(I) == Ir)
            I.f = True
            Assert(I.s == Is)
            Assert(str(I) == Ir)    # str() --> repr() (flipped)
            Assert(repr(I) == Is)   # repr() --> str() (flipped)
    def Test_formatting():
        from f import _have_Formatter
        if _have_Formatter:
            x = Init()*1e4
            Assert(x.sci == "3.14e4")
            Assert(x.eng == "31.4e3")
            Assert(x.si == "31.4 k")
            Assert(x.sic == "31.4k")
    Test_f()
    Test_h()
    Test_n()
    Test_r()
    Test_s()
    Test_formatting()
    # Use to get list of attributes
    if 0:
        x = Init()
        for i in dir(x):
            if i.startswith("_"):
                continue
            print(i)
            exit()
        # Gives attributes: f h n r s
        # Gives formatting attributes: eng sci si sic 

def Test_flt_arithmetic():
    '''Make sure that the flt class "infects" calculations by returning
    a flt for arithmetic operations.
 
    This won't happen for e.g. x = flt(1), y = mpmath.mpf(1) because y*x
    returns an mpmath.mpf type since mpmath's code intercepts the
    operation.  However, x*y returns a flt.
    '''
    def Real():
        x = Init()
        y = flt(1/pi)
        a = 2
        # First "direction"
        Assert(x*a == flt(a*pi))
        Assert(x/a == flt(pi/a))
        Assert(x + a == flt(pi + a))
        Assert(x - a == flt(pi - a))
        # Second "direction"
        Assert(a*x == flt(a*pi))
        Assert(a/x == flt(a/pi))
        Assert(a + x == flt(a + pi))
        Assert(a - x == flt(a - pi))
        # Check for type "infection"
        for o in (op.mul, op.truediv, op.floordiv, op.add, op.sub):
            b = o(a, x)
            Assert(isinstance(b, flt))
            b = o(x, a)
            Assert(isinstance(b, flt))
        # divmod and mod
        z = divmod(x, y)
        a = flt(0.2768036779356769)
        Assert(z == ((flt(9), a)))
        Assert(isinstance(z[0], flt))
        Assert(isinstance(z[1], flt))
        z = x % y
        Assert(z == a)
        Assert(isinstance(z, flt))
        # pow
        z = x**y
        assert(z == flt(pi**(1/pi)))
        Assert(isinstance(z, flt))
        # iadd, etc.
        z = x
        z *= y
        Assert(z == x*y)
        z = x
        z /= y
        Assert(z == x/y)
        z = x
        z //= y
        Assert(z == x//y)
        z = x
        z += y
        Assert(z == x + y)
        z = x
        z -= y
        Assert(z == x - y)
    def Complex():
        # flt with python complex numbers on the right-hand side
        x = Init()
        c = 2j
        z = cpx(c)
        for o in (op.mul, op.truediv, op.add, op.sub):
            y = o(x, c)
            expected = o(float(x), c)
            Assert(isinstance(y, cpx))
            Assert(y == expected)
            y = o(x, z)
            expected = o(float(x), c)
            Assert(isinstance(y, cpx))
            Assert(y == expected)
    Real()
    Complex()

def Test_cpx_arithmetic():
    '''Make sure that the cpx class "infects" calculations by returning
    a cpx for all arithmetic operations.
    '''
    Init()
    X, Y = complex(pi, 1/pi), complex(1/pi, pi)
    x, y = cpx(X), cpx(Y)
    d = decimal.Decimal("0.5")
    # Check operations wint int, float, flt, complex, cpx, Fraction, and
    # Decimal numbers.
    W = (2, 2.0, flt(2), 2j, 2-2j, cpx(2-2j), Fraction(1, 2), d)
    for w in (2, 2.0, flt(2), 2j, 2-2j, cpx(2-2j)):
        # Check we get the correct values
        # cpx on left
        Assert(x*w == X*w)
        Assert(x/w == X/w)
        Assert(x + w == X + w)
        Assert(x - w == X - w)
        # cpx on right
        Assert(w*x == w*X)
        Assert(w/x == w/X)
        Assert(w + x == w + X)
        Assert(w - x == w - X)
        # Return type must always be cpx
        ops = (op.mul, op.truediv, op.add, op.sub)
        for o in ops:
            b = o(w, x)
            Assert(isinstance(b, cpx))
            b = o(x, w)
            Assert(isinstance(b, cpx))
    # pow:  both x**y (typically used for ints) and built-in pow()
    z = x**y
    Z = X**Y
    assert(z == Z)
    Assert(isinstance(z, cpx))
    z = pow(x, y)
    assert(z == Z)
    Assert(isinstance(z, cpx))
    # Augmented arithmetic e.g. a *= b, etc.
    z = Z
    z *= y
    Assert(z == Z*y)
    z = Z
    z /= y
    Assert(z == Z/y)
    z = Z
    z += y
    Assert(z == Z + y)
    z = Z
    z -= y
    Assert(z == Z - y)

def TestRound():
    n = 6
    def Real():
        x = Init()
        # Use python's built-in round
        y = round(x, n)
        expected = 3.141593
        Assert(isinstance(y, float))
        Assert(y == expected)
        # Use flt's round method
        y = x.round(n)
        expected = 3.14159
        Assert(isinstance(y, flt))
        Assert(y == expected)
    def Complex():
        x = Init()
        z = cpx(x, 1/x)
        raises(TypeError, round, z, n)
        # Use flt's method
        y = z.round(n)
        expected = cpx(x.round(n), (1/x).round(n))
        Assert(isinstance(y, cpx))
        Assert(y == expected)
        # Use no argument
        y = x.round()
        Assert(isinstance(y, flt))
        # Note the following statement depends on us knowing that the
        # value of x is pi and that the built-in with one less than x.n
        # will work.  It may not work in general.
        Assert(y == round(pi, x.n - 1))
    Real()
    Complex()

def TestInfection():
    'Show flt & cpx infect commutatively'
    x, z = Init(), cpx(pi, -pi)
    f, d = Fraction(87, 232), decimal.Decimal("-87.232")
    for y in (2, 2.0, f, d):
        for o in (op.mul, op.truediv, op.add, op.sub):
            Assert(isinstance(o(y, x), flt))
            Assert(isinstance(o(x, y), flt))
            Assert(isinstance(o(y, z), cpx))
            Assert(isinstance(o(z, y), cpx))

def Test_numpy():
    if not _have_numpy:
        print(f"{t.r}{filename}:  ** Did not test flt/cpx with numpy **{t.n}")
        return
    Init()
    x = flt(pi)
    s = 3.3
    a = numpy.array((s,))
    y = x*a[0]
    Assert(y == x*s)
    x *= a[0]
    Assert(x == s*pi)

def TestDelegator():
    # Test that Delegator.iscomplex returns True when any argument or
    # part of an Iterable argument is complex.
    F = f.Delegator.iscomplex
    for i in (1j, [1j], (1j,), [1, 1j], (1, 1j)):
        assert(F(i))
    for i in (1, [1], (1,), [1, 1], (1, 1)):
        assert(not F(i))
    assert(not F(a=1))
    assert(F(a=1j))
    assert(F(a=1, b=1j))

def TestMathFunctions1():
    'Spot checks'
    tol = 1e-14     # Tolerance for isclose() tests
    Init()
    x, y = flt(pi/4), flt(42.3*pi)
    s, c, srt = f.sin(x), f.cos(x), f.sqrt(2)/2
    Assert(f.isclose(s, c, abs_tol=tol))
    Assert(f.isclose(s, srt, abs_tol=tol))
    Assert(f.isclose(c, srt, abs_tol=tol))
    Assert(f.atan2(1, 1) == x)
    Assert(f.factorial(6) == 720)
    a = f.fmod(y, x)
    b = math.fmod(y, x)
    Assert(a == b)
    a = f.remainder(y, x)
    b = math.remainder(y, x)
    Assert(a == b)
    # Iterator
    s = [0.1]*10
    Assert(f.fsum(s) == 1)
    Assert(f.fsum(s) == flt(1))
    # Boolean
    Assert(f.isfinite(x))
    Assert(f.isinf(f.inf))
    Assert(f.isnan(f.nan))
    a = 1e-5
    Assert(f.expm1(a) == math.expm1(a))
    Assert(f.log10(a) == math.log10(a))
    Assert(f.degrees(pi/4) == 45)
    Assert(f.radians(45) == pi/4)
    Assert(f.erf(1) + f.erfc(1) == 1)
    Assert(f.isclose(f.lgamma(7), f.log(720), abs_tol=tol))
    # Complex
    w, z = cpx(pi, -pi), cpx(-23.17, 18)
    Assert(f.cos(z) == cmath.cos(z))
    Assert(f.isclose(z, f.rect(*f.polar(z)), abs_tol=tol))
    Assert(f.log(w, z) == cmath.log(w, z))
    Assert(f.acosh(z) == cmath.acosh(z))
    Assert(f.isinf(f.inf))
    Assert(f.isinf(f.infj))
    Assert(f.isnan(f.nan))
    Assert(f.isnan(f.nanj))
    Assert(f.tau == math.tau == cmath.tau)
    # Check that a few functions work and return flt
    for x in (1, 10, -99, 9e99):
        y = f.sqrt(x)
        if x >= 0:
            Assert(isinstance(y, f.flt))
            Assert(y == math.sqrt(x))
        else:
            Assert(isinstance(y, f.cpx))
            Assert(y == cmath.sqrt(x))
        try:
            y = f.sin(x)
            Assert(isinstance(y, f.flt))
            Assert(y == math.sin(x))
        except OverflowError:
            if x != 9e99:
                raise
        try:
            y = flt(x)**flt(x)
            Assert(isinstance(y, f.flt))
            Assert(y == float(x)**float(x))
        except OverflowError:
            if x != 9e99:
                raise
    # Check that a few functions work and return cpx
    y = f.sqrt(-1)
    Assert(isinstance(y, f.cpx))
    Assert(y == cmath.sqrt(-1))
    for x in (1j, 1+1j, -99-99j, 9e99-9e99j):
        y = f.sqrt(x)
        Assert(isinstance(y, f.cpx))
        Assert(y == cmath.sqrt(x))
        try:
            y = f.sin(x)
            Assert(isinstance(y, f.cpx))
            Assert(y == cmath.sin(x))
        except OverflowError:
            if x != 9e99-9e99j:
                raise
        if x != 9e99-9e99j:
            y = x**cpx(x)
            Assert(isinstance(y, f.cpx))
            Assert(y == complex(x)**complex(x))

def TestMathFunctions2():
    '''The functions to be tested here are from python 3.9.4.  The list
    was produced by the /pylib/listmath.py script.
 
    These tests will be a little more systematic than the previous
    function.  The objectives are:
        * See that the function is available
        * See that its output matches the math or cmath version
        * The right type is returned (flt or cpx)
    '''
    not_tested = []     # For message about functions not tested
    def TestBoth():
        '''
        Both in math and cmath
          1:
            cmath.acos(x)       math.acos(x)
            cmath.acosh(x)      math.acosh(x)
            cmath.asin(x)       math.asin(x)
            cmath.asinh(x)      math.asinh(x)
            cmath.atan(x)       math.atan(x)
            cmath.atanh(x)      math.atanh(x)
            cmath.cos(x)        math.cos(x)
            cmath.cosh(x)       math.cosh(x)
            cmath.exp(x)        math.exp(x)
            cmath.isfinite(x)   math.isfinite(x)
            cmath.isinf(x)      math.isinf(x)
            cmath.isnan(x)      math.isnan(x)
            cmath.log10(x)      math.log10(x)
            cmath.sin(x)        math.sin(x)
            cmath.sinh(x)       math.sinh(x)
            cmath.sqrt(x)       math.sqrt(x)
            cmath.tan(x)        math.tan(x)
            cmath.tanh(x)       math.tanh(x)
          2:
            cmath.log(x[, base])    math.log(x[, base])
          4:
            cmath.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0) math.isclose(a, b, *, rel_tol=1e-09, abs_tol=0.0)
        '''
        x, x1, z = flt(0.821), flt(1.821), cpx(0.9112, -2.3)
        for fn in '''
            acos       acosh      asin       asinh      atan       atanh
            cos        cosh       exp        log10      sin        sinh
            sqrt       tan        tanh       
        '''.split():
            # Real test
            s = f"f.{fn}(x)"
            m = f"math.{fn}(x)"
            try:
                y1 = eval(s)
                y2 = eval(m)
            except ValueError:
                # Probably acosh
                s = f"f.{fn}(x1)"
                m = f"math.{fn}(x1)"
                y1 = eval(s)
                y2 = eval(m)
            except Exception as e:
                print(f"Unhandled exception:  '{e}'")
                print(f"Dropping into debugger")
                raise
                breakpoint() #xx
            Assert(y1 == y2)
            Assert(ii(y1, flt))
            Assert(ii(y2, float))
            # Complex test
            s = f"f.{fn}(z)"
            m = f"cmath.{fn}(z)"
            try:
                y1 = eval(s)
                y2 = eval(m)
            except ValueError:
                # Probably acosh
                s = f"f.{fn}(x1)"
                m = f"math.{fn}(x1)"
                y1 = eval(s)
                y2 = eval(m)
            Assert(y1 == y2)
            Assert(ii(y1, cpx))
            Assert(ii(y2, complex))
    def TestMathOnly():
        '''
        Only in math
          1:
            math.ceil(x)
            math.degrees(x)
            math.erf(x)
            math.erfc(x)
            math.expm1(x)
            math.fabs(x)
            math.factorial(x)
            math.floor(x)
            math.frexp(x)
            math.gamma(x)
            math.isqrt(n)
            math.lgamma(x)
            math.log1p(x)
            math.log2(x)
            math.modf(x)
            math.radians(x)
            math.trunc(x)
            math.ulp(x)
          2:
            math.atan2(y, x)
            math.comb(n, k)
            math.copysign(x, y)
            math.dist(pi, q)
            math.fmod(x, y)
            math.ldexp(x, i)
            math.nextafter(x, y)
            math.perm(n, k=None)
            math.pow(x, y)
            math.remainder(x, y)
          i:
            math.fsum(iterable)
            math.prod(iterable, *, start=1)
          *:
            math.gcd(*integers)
            math.hypot(*coordinates)
            math.lcm(*integers)
        '''
        # Univariate
        x, x1, i = flt(0.821), flt(1.821), 10
        for fn in '''
            ceil degrees erf erfc expm1 fabs factorial floor frexp gamma
            isqrt lgamma log1p log2 modf radians trunc ulp'''.split():
            if not hasattr(math, fn):
                not_tested.append(f"math.{fn}")
                continue
            s = f"f.{fn}(x)"
            m = f"math.{fn}(x)"
            try:
                y1 = eval(s)
                y2 = eval(m)
            except ValueError:
                # factorial needs an integer
                s = f"f.{fn}(i)"
                m = f"math.{fn}(i)"
                y1 = eval(s)
                y2 = eval(m)
            Assert(y1 == y2)
            if ii(y1, flt):
                Assert(ii(y2, float))
            else:
                Assert(type(y1) == type(y2))
        # Bivariate
        for fn in '''
            atan2 comb copysign dist fmod ldexp nextafter perm pow
            remainder'''.split():
            if not hasattr(math, fn):
                not_tested.append(f"math.{fn}")
                continue
            s = f"f.{fn}(x, x1)"
            m = f"math.{fn}(x, x1)"
            try:
                y1 = eval(s)
                y2 = eval(m)
            except TypeError:
                # ldexp
                s = f"f.{fn}(x, i)"
                m = f"math.{fn}(x, i)"
                y1 = eval(s)
                y2 = eval(m)
            except ValueError:
                # factorial needs an integer
                s = f"f.{fn}(i)"
                m = f"math.{fn}(i)"
                y1 = eval(s)
                y2 = eval(m)
            Assert(y1 == y2)
            if ii(y1, flt):
                Assert(ii(y2, float))
            else:
                Assert(type(y1) == type(y2))
        # Iterable
        arg = [x, x1]
        y1 = f.fsum(arg)
        y2 = math.fsum(arg)
        Assert(y1 == y2)
        Assert(ii(y1, flt))
        Assert(ii(y2, float))
        if hasattr(math, "prod"):  # Needs testing with python 3.9
            y1 = f.prod(arg)
            y2 = math.prod(arg)
            Assert(y1 == y2)
            Assert(ii(y1, flt))
            Assert(ii(y2, float))
        else:
            not_tested.append(f"math.prod")
        # Argument list
        # gcd
        arg = [10, 12]  # python 3.9 lets len(arg) > 2
        y1 = f.gcd(*arg)
        y2 = math.gcd(*arg)
        Assert(y1 == y2)
        Assert(ii(y1, int))
        Assert(ii(y2, int))
        # lcm
        if hasattr(math, "lcm"):  # Needs testing with python 3.9
            y1 = f.lcm(*arg)
            y2 = math.lcm(*arg)
            Assert(y1 == y2)
            Assert(ii(y1, int))
            Assert(ii(y2, int))
        else:
            not_tested.append(f"math.lcm")
        # hypot
        y1 = f.hypot(*arg)
        y2 = math.hypot(*arg)
        Assert(y1 == y2)
        Assert(ii(y1, flt))
        Assert(ii(y2, float))
    def TestCMathOnly():
        '''
        Only in cmath
          1:
            cmath.phase(x)
            cmath.polar(x)
          2:
            cmath.rect(r, phi)
        '''
        # phase
        z = cpx(1, 1)
        y1 = f.phase(z)
        y2 = cmath.phase(z)
        Assert(y1 == y2)
        Assert(ii(y1, flt))
        Assert(ii(y2, float))
        # polar
        y1 = f.polar(z)
        y2 = cmath.polar(z)
        r, theta = y2
        Assert(y1 == y2)
        Assert(ii(y1, tuple))
        Assert(ii(y2, tuple))
        Assert(ii(y1[0], flt))
        Assert(ii(y1[1], flt))
        Assert(ii(y2[0], float))
        Assert(ii(y2[1], float))
        # rect
        y1 = f.rect(r, theta)
        y2 = cmath.rect(r, theta)
        Assert(y1 == y2 == z)
        Assert(ii(y1, cpx))
        Assert(ii(y2, complex))
    def TestBooleans():
        a = 1.6
        x, z = flt(a), cpx(a, a)
        rnan, cnan = math.nan, cmath.nan
        rinf, cinf, cinfj = math.inf, cmath.inf, cmath.infj
        # isfinite
        Assert(f.isfinite(x) is True)
        Assert(f.isfinite(z) is True)
        # isinf
        Assert(f.isinf(rinf) is True)
        Assert(f.isinf(cinf) is True)
        Assert(f.isinf(cinfj) is True)
        # isnan
        Assert(f.isnan(rnan) is True)
        Assert(f.isnan(cnan) is True)
    TestBoth()
    TestMathOnly()
    TestCMathOnly()
    TestBooleans()
    if not_tested:
        s = [i.replace("math.", "") for i in not_tested]
        print(f"{t.r}{__file__}:  math/cmath stuff not in this python version:\n"
              f"    {' '.join(s)}{t.n}")
if __name__ == "__main__":
    exit(run(globals(), halt=1)[0])
