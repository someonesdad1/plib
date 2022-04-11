'''
Elementary functions for the python Decimal library
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2006, 2012 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Elementary math functions for the python Decimal library.
    # Provides a number of the real-valued functions that are in the math
    # module.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import math
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from kolor import C
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    ii = isinstance
    __all__ = '''
        acos acosh asin asinh atan atan2 atanh ceil copysign cos cosh
        degrees e exp expm1 f2d fabs FindRoot floor fmod hypot isclose
        IsDecimal isfinite isinf isnan log log10 log1p log2 modf pi pow
        radians remainder sin sinh sqrt tan tanh tau trunc
        inf ninf nan
        '''.split()
    Dec = decimal.Decimal
    zero, one, two, three, four, nine, ten = [Dec(i) for i in (0, 1, 2, 3,
        4, 9, 10)]
    half = Dec("0.5")
    inf, ninf, nan = Dec("inf"), Dec("-inf"), Dec("nan")
    precision_increment = 4
    class g: pass
    g.e = C.lcyn
    g.n = C.norm
    __doc__ = dedent('''
    Elementary functions for the python Decimal library.
    
    Function      Domain            Range
    --------      ------            -----
    acos        -1 to 1           0 to pi
    asin        -1 to 1           -pi/2 to pi/2
    atan        -oo to oo         -pi/2 to pi/2
    atan2       Two arguments     -pi to pi
    cos         Any real          -1 to 1
    exp         Any real          (0, oo]
    ln          Any real > 0      -oo to oo
    log10       Any real > 0      -oo to oo
    pi          --                --
    pow         Two arguments     -oo to oo
    sin         Any real          -1 to 1
    sqrt        Any real > 0      Real > 0
    tan         Any real          -oo to oo
    
    The calculation strategy of this module is to calculate pi, exp, sin,
    and cos by power series; the code for these is taken from examples in
    the Decimal documentation.  The remaining functions can be calculated
    from these core functions using a root-finding function.
    
    This module has been tested with:
    
        python 2.6.5 with mpmath 0.12
        python 3.2.2 with mpmath 0.17
        Python 2.7.16 cygwin with mpmath 1.0.0
        Python 3.7.4 cygwin with mpmath 1.1.0
        Python 3.7.10 cygwin with mpmath 1.1.0
    
    mpmath (http://code.google.com/p/mpmath/) is not needed for normal
    use; it is used to provide reference values for testing.
    ''')
if 1:   # Utility functions
    def IsDecimal(*x):
        for i, val in enumerate(x):
            if not ii(val, Dec):
                msg = f"Argument {i + 1} '{val}' is not Decimal type"
                raise ValueError(msg)
if 1:   # Constants
    def pi():
        'Returns pi to the current precision'
        # Algorithm from Decimal documentation's recipes
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            lasts, t, s, n, na, d, da = 0, three, three, one, zero, zero, 24
            while s != lasts:
                lasts = s
                n, na = n + na, na + 8
                d, da = d + da, da + 32
                t = (t*n)/d
                s += t
        return +s  # Force rounding to current precision
    def tau():
        return two*pi()
    def e():
        return exp(one)
if 1:   # Trigonometric
    def sin(x):
        'Returns the sine of x; x is in radians'
        IsDecimal(x)
        if not x:
            return zero
        # Check for an argument proportional to pi/2
        p = pi()/two
        ratio = abs(x/p)
        fp = ratio - int(ratio)
        eps = ten**-(decimal.getcontext().prec - 1)
        if not fp or abs(fp - 1) < eps:
            return one
        i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            # Algorithm is Maclaurin series expansion
            while s != lasts:
                lasts = s
                i += 2
                fact *= i*(i-1)
                num *= x*x
                sign *= -1
                s += num/fact*sign
        return +s  # Force rounding to current precision
    def cos(x):
        'Returns the cosine of x; x is in radians'
        '''
        Implementation note:  an argument proportional to pi/2 is
        problematic because the cosine of such an angle is zero.  However,
        for the default precision of 28 digits, the power series below will
        give about -3.6e-28 for pi/2 and -9.2e-28 for 3*pi/2 instead of
        zero.  When a tangent of pi/2 is calculated, the sine will be zero
        but the cosine will cause the tangent to be a large negative number
        near 10**28.  This gets the sign wrong for pi/2.  Thus, we'll set
        the cosine to zero in such cases.
 
        A further problem is that a large integer multiplied by pi/2 should
        also have a cosine that is zero, but this gets harder to detect
        because the fractional part has fewer digits.
        '''
        IsDecimal(x)
        if not x:
            return one
        # Check for an argument proportional to pi/2
        p = pi()/two
        ratio = abs(x/p)
        fp = ratio - int(ratio)
        eps = ten**-(decimal.getcontext().prec - 1)
        if not fp or abs(fp - 1) < eps:
            return zero
        # Calculate Maclaurin series
        i, lasts, s, fact, num, sign = 0, 0, 1, 1, 1, 1
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            while s != lasts:
                lasts = s
                i += 2
                fact *= i*(i-1)
                num *= x*x
                sign *= -1
                s += num/fact*sign
        # If s is about eps or less, then it's also likely that the
        # argument was a multiple of pi/2
        if abs(s) < eps:
            return 0
        return +s
    def tan(x):
        'Returns the tangent of x; x is in radians'
        IsDecimal(x)
        if x == zero:
            return zero
        return sin(x)/cos(x)
    def asin(x):
        'Returns the inverse sine (in radians) of x'
        # The algorithm uses the root finder with the sine function as
        # an argument.
        IsDecimal(x)
        if not (-one <= x <= one):
            raise ValueError("Absolute value of Argument must be <= 1")
        if x == zero:
            return zero
        elif x == one:
            return pi()/2
        elif x == -one:
            return -pi()/2
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            if abs(x) > 1:
                raise ValueError("asin(x) with abs(x) > 1: " + str(x))
            # Get a close starting value
            starting_value = f2d(math.asin(float(x)))
            delta = Dec("1e-4")
            if starting_value > 0:
                low = starting_value*(1 - delta)
                high = min(starting_value*(1 + delta), f2d(math.pi/2))
            else:
                high = starting_value*(1 - delta)
                low = min(starting_value*(1 + delta), -f2d(math.pi/2))
            # Make sure we bracket the root
            assert((math.sin(low) - float(x))*(math.sin(high) - float(x)) < 0)
            root = FindRoot(low, high, lambda t: sin(t) - x)[0]
        return +root  # Force rounding to current precision
    def acos(x):
        'Returns the inverse cosine (in radians) of x'
        # The algorithm uses the root finder with the cosine function as
        # an argument.
        IsDecimal(x)
        if abs(x) > 1:
            raise ValueError("Absolute value of argument must be <= 1")
        if x == zero:
            return pi()/2
        elif x == one:
            return zero
        elif x == -one:
            return pi()
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            # Get a close starting value
            starting_value = f2d(math.acos(float(x)))
            delta = Dec("1e-4")
            low = starting_value*(1 - delta)
            high = min(starting_value*(1 + delta), f2d(math.pi))
            # Make sure we bracket the root
            assert((math.cos(low) - float(x))*(math.cos(high) - float(x)) < 0)
            root = FindRoot(low, high, lambda t: cos(t) - x)[0]
        return +root  # Force rounding to current precision
    def atan(x):
        'Returns the inverse tangent (in radians) of x'
        # The algorithm uses the root finder with the tangent function as
        # an argument.
        IsDecimal(x)
        if x == zero:
            return zero
        elif x == inf:
            return pi()/2
        elif x == ninf:
            return -pi()/2
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            starting_value = f2d(math.atan(float(x)))
            delta = Dec("1e-4")
            if starting_value > 0:
                low = starting_value*(1 - delta)
                high = min(starting_value*(1 + delta), f2d(math.pi/2))
            else:
                high = starting_value*(1 - delta)
                low = max(starting_value*(1 + delta), f2d(-math.pi/2))
            # Make sure we bracket the root
            assert((math.tan(low) - float(x))*(math.tan(high) - float(x)) < 0)
            root = FindRoot(low, high, lambda t: tan(t) - x)[0]
        return +root  # Force rounding to current precision
    def atan2(y, x):
        '''Returns the inverse tangent of y/x (in radians) and gets the
        correct quadrant.
        '''
        IsDecimal(x, y)
        Pi = pi()
        if x == zero:
            if y == zero:
                raise ValueError("Both arguments zero:  indeterminate angle")
            elif y < zero:
                return -Pi/2
            else:
                return Pi/2
        elif y == zero:
            if x > zero:
                return zero
            else:
                return -Pi
        theta = atan(y/abs(x))
        if x < zero:
            s = 1 if y > zero else -1
            theta = s*Pi - theta
        return +theta
    def degrees(x):
        IsDecimal(x)
        return x*180/pi()
    def radians(x):
        IsDecimal(x)
        return x*pi()/180
    def hypot(x, y):
        IsDecimal(x, y)
        return sqrt(x*x + y*y)
if 1:   # Exponential and logarithmic
    def exp(x):
        'Returns e raised to the power of x'
        IsDecimal(x)
        return x.exp()
    def expm1(x):
        'exp(x) - 1, avoiding loss of significance for small x'
        IsDecimal(x)
        if not x:
            return zero
        i, lasts, s, fact, term = 1, 0, x, 1, x
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            # Algorithm is Maclaurin series expansion
            while s != lasts:
                lasts = s
                i += 1
                fact *= i
                term *= x
                s += term/fact
        return +s  # Force rounding to current precision
    def log10(x):
        'Returns the base 10 logarithm of x'
        IsDecimal(x)
        if x <= zero:
            raise ValueError("Argument must be > 0")
        return x.log10()
    def log(x, base=None):
        'Returns the logarithm of x to the indicated base (e if base is None)'
        # Use the native method, as the old method was to use a root finder
        # and evaluating exp(x) for large numbers like 2e100000 takes
        # excessive time.
        IsDecimal(x)
        if x == one:
            return zero
        elif x <= zero:
            raise ValueError("x must be > 0")
        if base is not None and base <= 0:
            raise ValueError("base must be > 0")
        ln = x.ln()
        if base is None:
            return ln
        else:
            return ln/log(base)
    def log2(x):
        IsDecimal(x)
        return log(x, base=two)
    def log1p(x):
        '''Returns log(1 + x) and is accurate when x << 1.  If x > 0.1, will
        raise an exception because convergence is very slow.
        '''
        # The Maclaurin expansion is
        #     x - x**2/2 + x**3/3 - x**4/4 + x**5/5 - x**6/6 + ...
        IsDecimal(x)
        if x > Dec("0.1"):
            raise ValueError("Unacceptable convergence if x > 0.1")
        i, lasts, s, num, sign = 1, 0, x, x, 1
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            # Algorithm is Maclaurin series expansion
            while s != lasts:
                lasts = s
                i += 1
                num *= x
                sign *= -1
                term = num*sign/i
                s += term
                print(s)
        return +s  # Force rounding to current precision
    def pow(y, x):
        'Returns y raised to the power x'
        if not ii(x, (Dec, int)):
            raise ValueError("Argument is not Decimal or integer type")
        if not ii(y, (Dec, int)):
            raise ValueError("Argument is not Decimal or integer type")
        if not y:
            raise ValueError("Base must not be zero")
        if x == zero:
            return one
        if x == one:
            return y
        if x == -one:
            return 1/y
        with decimal.localcontext() as ctx:
            ctx.prec += precision_increment
            if y < 0:
                if ii(x, int) or int(x) == x:
                    y = abs(y)
                    if x % 2 == 0:
                        # Even power
                        if x < 0:
                            retval = 1/exp(-x*log(y))
                        else:
                            retval = exp(x*log(y))
                    else:
                        # Odd power
                        if x < 0:
                            retval = -1/exp(-x*log(y))
                        else:
                            retval = -exp(x*log(y))
                else:
                    raise ValueError("Negative base with noninteger exponent")
            else:
                retval = exp(x*log(y))
        return +retval  # Force rounding to current precision
if 1:   # Hyperbolic
    def cosh(x):
        IsDecimal(x)
        y = exp(x)
        return (y + one/y)/two
    def acosh(x):
        IsDecimal(x)
        return log(x + sqrt(x*x - one))
    def sinh(x):
        IsDecimal(x)
        y = exp(x)
        return (y - one/y)/two
    def asinh(x):
        IsDecimal(x)
        return log(x + sqrt(x*x + one))
    def tanh(x):
        IsDecimal(x)
        y = exp(x)
        a = one/y
        return (y - a)/(y + a)
    def atanh(x):
        IsDecimal(x)
        return log((one + x)/(one - x))/two
if 1:   # Miscellaneous
    def sqrt(x):
        'Returns the square root of x'
        IsDecimal(x)
        if x < zero:
            raise ValueError("Can't take square root of negative argument")
        if x == zero:
            return zero
        if x == one:
            return one
        return x.sqrt()
    def ceil(x):
        'Smallest integer > x'
        IsDecimal(x)
        return 0 if x == zero else -int(-x) if x < 0 else int(x) + 1
    def floor(x):
        'Largest integer < x'
        IsDecimal(x)
        return 0 if x == zero else -int(-x) - 1 if x < 0 else int(x)
    def copysign(x, y):
        IsDecimal(x)
        return x.copy_sign(y)
    def f2d(x):
        '''Convert a floating point number x to a Decimal.  See the
        decimal module's documentation for warnings about doing such
        things.
        '''
        if not ii(x, (float, str)):
            raise ValueError("x needs to be a float or string")
        if ii(x, float):
            return Dec("0").from_float(x)
        else:
            return Dec(x)
    def FindRoot(x0, x2, f, maxit=50, show=False):
        '''Returns a tuple (root, number_of_iterations, eps) where root is the
        root of f(x) == 0.  The root must be bracketed by x0 and x2.  f is the
        function to evaluate; it takes one Decimal argument and returns a
        Decimal.  If your f(x) has more arguments, use functools.partial.  
        If show is True, print out intermediate values.
    
        The iteration will terminate when two consecutive calculations differ
        by eps (see below) or less.
    
        The routine will raise a ValueError exception if the number of
        iterations is greater than maxit.
    
        Reference:  "All Problems Are Simple" by Jack Crenshaw, Embedded
        Systems Programming, May, 2002, pg 7-14.  Translated from Jack's C
        code by myself on 20 May 2003.
    
        Inverse parabolic interpolation algorithm to find the roots.  Jack
        states this routine will converge rapidly on most functions, typically
        adding 4 digits to the solution on each iteration.  The routine works
        by starting with x0, x2, and finding a third x1 by bisection.  The
        ordinates are gotten, then a horizontally-opening parabola is fitted to
        the points.  The parabola's root's abscissa is gotten, and the
        iteration is repeated.
    
        Note:  Jack commented that this routine was written by some unknown
        genius at IBM and was in IBM's FORTRAN library code in the 1960's.
        Jack has done quite a bit of work to popularize it.
        '''
        # We'll find the value to a precision that is 10**(-n + 1) where
        # n is the current number of Decimal digits.  Note:  we add 1
        # because there are two guard digits and, if 1 wasn't added, some
        # of the iterations won't converge (e.g., asin(-0.5)).
        eps = Dec(10)**(-Dec(decimal.getcontext().prec) + 1)
        # Check arithmetic
        if 1/2 != 0.5:
            raise ValueError("Inadequate arithmetic")
        # Set up constants
        xmlast = x0
        x1 = y0 = y1 = y2 = b = c = temp = y10 = y20 = y21 = xm = ym = zero
        # Check input
        if not ii(x0, Dec):
            raise ValueError("Argument x0 is not Decimal type")
        if not ii(x2, Dec):
            raise ValueError("Argument x2 is not Decimal type")
        if x0 >= x2:
            raise ValueError("x0 must be strictly less than x2")
        if eps <= zero:
            raise ValueError("eps must be > 0")
        if not ii(maxit, int) or maxit < one:
            raise ValueError("maxit must be integer > 0")
        # Handle special cases
        y0 = f(x0)
        if not y0:
            return x0, 0, eps
        y2 = f(x2)
        if not y2:
            return x2, 0, eps
        # Make sure root is bracketed
        if y2*y0 > zero:
            raise ValueError("x0 and x2 don't bracket a root")
        # Iterate for root
        for i in range(maxit):
            x1 = (x2 + x0)/two
            y1 = f(x1)
            if not y1 or abs(x1 - x0) < eps:
                return x1, i + 1, eps
            if y1*y0 > zero:
                temp = x0
                x0 = x2
                x2 = temp
                temp = y0
                y0 = y2
                y2 = temp
            y10 = y1 - y0
            y21 = y2 - y1
            y20 = y2 - y0
            if y2*y20 < two*y1*y10:
                x2 = x1
                y2 = y1
                if abs(xm - xmlast) < eps:
                    return xm, i + 1, eps
            else:
                b = (x1 - x0)/y10
                c = (y10 - y21)/(y21*y20)
                xm = x0 - b*y0*(one - c*y1)
                ym = f(xm)
                if not ym or abs(xm - xmlast) < eps:
                    return xm, i + 1, eps
                xmlast = xm
                if ym*y0 < zero:
                    x2 = xm
                    y2 = ym
                else:
                    x0 = xm
                    y0 = ym
                    x2 = x1
                    y2 = y1
            if show:
                print(xm)
        raise ValueError(f"FindRoot:  no convergence after {maxit} iterations")
    def fabs(x):
        IsDecimal(x)
        return -x if x < zero else x if x > zero else zero
    def fmod(x, y):
        '''fmod is the floating point analog of x % y.  It tells you the
        remainder after subtracting an integer number of y's from x.
        '''
        IsDecimal(x, y)
        return (-1 if x < 0 else 1)*(abs(x) - int(abs(x/y))*abs(y))
    def isinf(x):
        IsDecimal(x)
        return x == inf or x == ninf
    def isnan(x):
        IsDecimal(x)
        ctx = getcontext()
        return ctx.is_qnan(x) or ctx.is_snan(x)
    def isfinite(x):
        IsDecimal(x)
        return not isinf(x) and not isnan(x)
    def isclose(a, b, rel_tol=zero, abs_tol=zero):
        '''Returns True of a and b are close to each other.  Note this used
        different keyword defaults than math.isclose().
        '''
        IsDecimal(a, b, rel_tol, abs_tol)
        abmax = max(abs(a), abs(b))
        return abs(a - b) <= max(rel_tol*abmax, abs_tol)
    def modf(x):
        'Return (fractional_part, integer_part)'
        IsDecimal(x)
        ip = Dec(floor(abs(x)))
        fp = abs(x) - ip
        return (fp.copy_sign(x), ip.copy_sign(x))
    def remainder(x, y):
        '''Returns x - n*y where n is the closest integer to x/y.  If x/y is
        halfway between two integers, it's rounded to the nearest even integer.
        The sign is the same as the original dividend.
 
        remainder() produces a number on the closed interval [-y/2, y/2].  See 
        https://stackoverflow.com/questions/26671975/why-do-we-need-ieee-754-remainder#27378075
        for a trigonometric example.
        '''
        IsDecimal(x)
        IsDecimal(y)
        fp, ip = modf(abs(x/y))
        sign = -one if x < zero else one if x > zero else zero
        if fp == half:
            if int(ip) % 2:
                ip += one
        elif fp > half:
            ip += 1
        return sign*(abs(x) - ip*abs(y))
    def trunc(x):
        IsDecimal(x)
        sign = -1 if x < 0 else 1 if x > 0 else 0
        return sign*int(abs(x))

if __name__ == "__main__": 
    # Use mpmath (http://mpmath.org/) to generate the numbers to test
    # against (i.e., assume mpmath's algorithms are correct).
    import mpmath as mp
    import math
    from random import uniform, seed
    from pdb import set_trace as xx
    from wrap import wrap, dedent, indent, Wrap
    from lwtest import run, raises, assert_equal, Assert
    from functools import partial
    getcontext = decimal.getcontext
    localcontext = decimal.localcontext
    mp.mp.dps = getcontext().prec
    Pi = Dec(str(mp.pi()))  # Reference value of pi at current precision
    pio2, pio3, pio4, pio6 = Pi/two, Pi/three, Pi/four, Pi/Dec(6)
    eps = ten*ten**(-Dec(getcontext().prec))
    AssertNearlyEqual = partial(assert_equal, reltol=eps)
    def Test_pi():
        s = repr(mp.pi())
        x = eval(s.replace("mpf", "Dec"))
        AssertNearlyEqual(pi(), x)
        with localcontext() as ctx:
            # Value from wikipedia page on pi
            ctx.prec = 52
            # Truncate instead of round to second to last digit
            s_calc = str(pi())[:-1]
            s_exact = "3.14159265358979323846264338327950288419716939937510"
            assert_equal(s_calc, s_exact)
    def Test_trig():
        if 1:   # Regular functions
            # sin
            AssertNearlyEqual(sin(zero), zero)
            AssertNearlyEqual(sin(pio4), one/sqrt(two))
            AssertNearlyEqual(sin(pio2), one)
            # cos
            AssertNearlyEqual(cos(zero), one)
            AssertNearlyEqual(cos(pio4), one/sqrt(two))
            Assert(cos(pio2) == zero)
            # tan
            AssertNearlyEqual(tan(zero), zero)
            AssertNearlyEqual(tan(pio4), one)
            raises(decimal.DivisionByZero, tan, pio2)
        if 1:   # Inverse functions
            # asin
            AssertNearlyEqual(asin(half),               pio6)
            AssertNearlyEqual(asin(-half),             -pio6)
            AssertNearlyEqual(asin(three.sqrt()/two),   pio3)
            AssertNearlyEqual(asin(-three.sqrt()/two), -pio3)
            AssertNearlyEqual(asin(zero),               zero)
            AssertNearlyEqual(asin(one),                pio2)
            AssertNearlyEqual(asin(-one),              -pio2)
            raises(ValueError, asin, two)
            # acos
            AssertNearlyEqual(acos(zero),               pio2)
            AssertNearlyEqual(acos(half),               pio3)
            AssertNearlyEqual(acos(-half),              pio6 + pio2)
            AssertNearlyEqual(acos(three.sqrt()/two),   pio6)
            AssertNearlyEqual(acos(-three.sqrt()/two),  Pi - pio6)
            AssertNearlyEqual(acos(one),                zero)
            AssertNearlyEqual(acos(-one),               Pi)
            raises(ValueError, acos, two)
            # atan
            AssertNearlyEqual(atan(zero),               zero)
            AssertNearlyEqual(atan(three.sqrt()),       pio3)
            AssertNearlyEqual(atan(one),                pio4)
            AssertNearlyEqual(atan(-one),              -pio4)
            AssertNearlyEqual(atan(-three.sqrt()),     -pio3)
            # atan2
            AssertNearlyEqual(atan2(one, one),          pio4)
            AssertNearlyEqual(atan2(one, -one),         three*pio4)
            AssertNearlyEqual(atan2(-one, one),        -pio4)
            AssertNearlyEqual(atan2(-one, -one),       -three*pio4)
    def Test_log():
        s = repr(mp.log("0.5"))
        x = eval(s.replace("mpf", "decimal.Decimal"))
        AssertNearlyEqual(log(half), x)
        AssertNearlyEqual(log(one),     zero)
        s = repr(mp.log(mp.pi()/2))
        x = eval(s.replace("mpf", "decimal.Decimal"))
        AssertNearlyEqual(log(pio2), x)
        s = repr(mp.log(10))
        x = eval(s.replace("mpf", "decimal.Decimal"))
        AssertNearlyEqual(log(ten), x)
        raises(ValueError, log, -one)
        # Use the Decimal instance's method
        AssertNearlyEqual(log(half), half.ln())
    def Test_log10():
        AssertNearlyEqual(log10(half), mp.log10("0.5"))
        AssertNearlyEqual(log10(one), zero)
        AssertNearlyEqual(log10(pio2), mp.log10(mp.pi()/2))
        AssertNearlyEqual(log10(ten), mp.log10(10))
        raises(ValueError, log10, -one)
        # Use the Decimal instance's method
        AssertNearlyEqual(log10(half), half.log10())
    def Test_pow():
        AssertNearlyEqual(pow(four, half),    two)
        AssertNearlyEqual(pow(two, -two),       one/four)
        AssertNearlyEqual(pow(-two, two),       four)
        AssertNearlyEqual(pow(-three, two),     nine)
        AssertNearlyEqual(pow(-three, -two),    one/nine)
        AssertNearlyEqual(pow(-three, three),   Dec(-27))
        AssertNearlyEqual(pow(-three, -three), -one/Dec(27))
        raises(ValueError, pow, -two, 1/three)
    def Test_sqrt():
        AssertNearlyEqual(sqrt(zero), zero)
        AssertNearlyEqual(sqrt(one), one)
        AssertNearlyEqual(sqrt(four), two)
        AssertNearlyEqual(sqrt(nine), three)
        x = "88.325"
        AssertNearlyEqual(sqrt(Dec(x)), mp.sqrt(mp.mpf(x)))
        raises(ValueError, sqrt, -two)
        # Use the Decimal instance's method
        AssertNearlyEqual(sqrt(half), half.sqrt())
    def Test_hyperbolic():
        if 1:   # Regular functions
            # sinh
            AssertNearlyEqual(sinh(zero), zero)
            AssertNearlyEqual(sinh(one), -sinh(-one))
            Assert(str(sinh(Pi)) == str(mp.sinh(str(Pi))))
            # cosh
            AssertNearlyEqual(cosh(zero), one)
            AssertNearlyEqual(cosh(one), cosh(-one))
            Assert(str(cosh(Pi)) == str(mp.cosh(str(Pi))))
            # tanh
            AssertNearlyEqual(tanh(zero), zero)
            AssertNearlyEqual(tanh(one), -tanh(-one))
            AssertNearlyEqual(tanh(Pi), Dec(str(mp.tanh(str(Pi)))))
        if 1:   # Inverse functions
            # asinh
            AssertNearlyEqual(asinh(zero), zero)
            Assert(str(asinh(Pi)) == str(mp.asinh(str(Pi))))
            Assert(str(asinh(-Pi)) == str(mp.asinh(str(-Pi))))
            # acosh
            AssertNearlyEqual(acosh(one), zero)
            Assert(str(acosh(Pi)) == str(mp.acosh(str(Pi))))
            raises(ValueError, acosh, half)
            # atanh
            AssertNearlyEqual(atanh(zero), zero)
            AssertNearlyEqual(atanh(one/Pi), Dec(str(mp.atanh(str(one/Pi)))))
            raises(decimal.DivisionByZero, atanh, one)
    def Test_floor_ceil():
        # Zero
        Assert(floor(zero) == 0)
        Assert(ceil(zero) == 0)
        # Positive numbers
        Assert(floor(Pi) == math.floor(math.pi))
        Assert(ceil(Pi) == math.floor(math.pi) + 1)
        x = Pi*Dec('1e20')
        Assert(floor(x) == int(x))
        Assert(ceil(x) == int(x) + 1)
        # Negative numbers
        Assert(floor(-Pi) == math.floor(-math.pi))
        Assert(ceil(-Pi) == math.ceil(-math.pi))
        x = -Pi*Dec('1e20')
        Assert(floor(x) == int(x) - 1)
        Assert(ceil(x) == int(x))
    def Test_copysign():
        # Check with integers
        Assert(copysign(one, 1) == one)
        Assert(copysign(-one, 1) == one)
        Assert(copysign(one, -1) == -one)
        Assert(copysign(-one, -1) == -one)
        Assert(copysign(zero, 1) == zero)
        Assert(copysign(zero, -1) == -zero)
        # Check with Decimal
        Assert(copysign(one, one) == one)
        Assert(copysign(-one, one) == one)
        Assert(copysign(one, -one) == -one)
        Assert(copysign(-one, -one) == -one)
        Assert(copysign(zero, one) == zero)
        Assert(copysign(zero, -one) == -zero)
    def Test_fabs():
        Assert(fabs(zero) == zero)
        Assert(fabs(one) == one)
        Assert(fabs(-one) == one)
    def Test_fmod():
        'Compare to results from math.fmod'
        def test(a, b):
            x, y = Dec(a), Dec(b)
            dr = fmod(x, y)
            X, Y = float(a), float(b)
            fr = f2d(math.fmod(X, Y))
            Assert(isclose(dr, fr, rel_tol=Dec("1e-9")))
            Assert(isclose(dr, x % y, rel_tol=Dec("1e-9")))
        test(*"98.61 7.73".split())
        test(*"98.61 -7.73".split())
        test(*"-98.61 7.73".split())
        test(*"-98.61 -7.73".split())
        # Also works on integers
        Assert(fmod(three, two) == one)
        Assert(three % two == one)
        # Requires Decimals
        raises(ValueError, fmod, one, 2)
        raises(ValueError, fmod, 1, two)
    def Test_isinf_isnan_isfinite():
        # isinf
        Assert(isinf(inf))
        Assert(isinf(ninf))
        Assert(not isinf(nan))
        Assert(not isinf(nan))
        # isnan
        Assert(isnan(nan))
        Assert(not isnan(inf))
        # isfinite
        Assert(isfinite(zero))
        Assert(isfinite(one))
        Assert(isfinite(-one))
        Assert(not isfinite(inf))
        Assert(not isfinite(ninf))
        Assert(not isfinite(nan))
    def Test_isclose():
        a, b = one, one + Dec("1e-10")
        # Using default values
        Assert(isclose(a, a))
        Assert(not isclose(a, b))
        # Using rel_tol
        Assert(isclose(a, b, rel_tol=Dec("1e-9")))
        Assert(isclose(a, b, rel_tol=Dec("1e-10")))
        Assert(not isclose(a, b, rel_tol=Dec("1e-11")))
        # Using abs_tol
        Assert(isclose(a, b, abs_tol=Dec("1e-10")))
        Assert(not isclose(a, b, abs_tol=Dec("1e-11")))
    def Test_modf():
        with decimal.localcontext() as ctx:
            ctx.prec = 15
            for s in (pi(), -pi()):
                ffp, fip = math.modf(float(s))
                fp, ip = modf(s)
                Assert(fp == +f2d(ffp))
                Assert(ip == +f2d(fip))
    def Test_remainder():
        'Use randomly-generated numbers'
        n, x = 100, 1000
        reltol = Dec("1e-12")
        seed(x)
        f = partial(uniform, -x, x)
        for i in range(n):
            x = f()
            y = f()
            while not y:    # Make sure y isn't zero
                y = f()
            fresult = f2d(math.remainder(x, y))
            dresult = remainder(f2d(x), f2d(y))
            if 1 and not isclose(fresult, dresult, rel_tol=reltol):
                print("x, y", x, y)
                print("math module: ", fresult)
                print("this module: ", dresult)
                exit(1)
            else:
                Assert(isclose(fresult, dresult, rel_tol=reltol))
    def Test_trunc():
        for i in range(100):
            x = Dec("0.1") + Dec(i)
            t = trunc(x)
            Assert(t == i)
            x = -x
            t = trunc(x)
            Assert(t == -i)
    exit(run(globals())[0])
