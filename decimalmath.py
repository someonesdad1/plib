'''
Elementary functions for the python Decimal library
    TODO

    * Needs to handle inf and nan in arguments.  Decimal supports
      methods is_nan() and is_infinite().  If strict, then results in
      exception if arg is one of these values; otherwise return
      something appropriate.  If not strict, then out-of-domain
      arguments can return nan.
    * Add strict bool.  If True, then all arguments must be decimal.  If
      False, then will try to convert from mpmath, float, or string.
    * Add atan2
    * Add hyperbolic functions?
    * Add other trig functions (sec, csc, versine, haversine, etc.)?
    * All loops should have counters to avoid having the program hang.
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
    # Elementary functions for the python Decimal library
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import math
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    __all__ = '''acos asin atan atan2 cos exp ln log10 pi
        pow sin sqrt tan'''.split()
    Dec = decimal.Decimal
    zero, one, two, three = Dec(0), Dec(1), Dec(2), Dec(3)
    half = Dec("0.5")
    precision_increment = 4
    inf = float("inf")
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
    
    mpmath (http://code.google.com/p/mpmath/) is not needed for normal
    use; it is used to provide reference values for testing.
    ''')
def pi():
    '''Returns pi to the current precision.
    '''
    with decimal.localcontext() as ctx:
        ctx.prec += precision_increment
        lasts, t, s, n, na, d, da = 0, three, 3, 1, 0, 0, 24
        while s != lasts:
            lasts = s
            n, na = n + na, na + 8
            d, da = d + da, da + 32
            t = (t*n)/d
            s += t
    return +s  # Force rounding to current precision
def exp(x):
    '''Returns e raised to the power of x.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    with decimal.localcontext() as ctx:
        ctx.prec += precision_increment
        i, lasts, s, fact, num = 0, 0, 1, 1, 1
        while s != lasts:
            lasts = s
            i += 1
            fact *= i
            num *= x
            s += num/fact
    return +s  # Force rounding to current precision
def sin(x):
    '''Returns the sine of x; x is in radians.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    i, lasts, s, fact, num, sign = 1, 0, x, 1, x, 1
    with decimal.localcontext() as ctx:
        ctx.prec += precision_increment
        while s != lasts:
            lasts = s
            i += 2
            fact *= i*(i-1)
            num *= x*x
            sign *= -1
            s += num/fact*sign
    return +s  # Force rounding to current precision
def cos(x):
    '''Returns the cosine of x; x is in radians.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
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
    return +s  # Force rounding to current precision
def tan(x):
    '''Returns the tangent of x; x is in radians.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    if x == zero:
        return zero
    elif x == one:
        return pi()/4
    elif x == -one:
        return -pi()/4
    with decimal.localcontext() as ctx:
        ctx.prec += 2
        s = sin(x)/cos(x)
    return +s  # Force rounding to current precision
def acos(x):
    '''Returns the inverse cosine (in radians) of x.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
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
    '''Returns the inverse tangent (in radians) of x.
    '''
    # The algorithm uses the root finder with the tangent function as
    # an argument.
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    if x == zero:
        return zero
    elif float(x) == inf:
        return pi()/2
    elif float(-x) == -inf:
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
    if not isinstance(x, Dec):
        raise ValueError("x argument is not Decimal type")
    if not isinstance(y, Dec):
        raise ValueError("y argument is not Decimal type")
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
def asin(x):
    '''Returns the inverse sine (in radians) of x.
    '''
    # The algorithm uses the root finder with the sine function as
    # an argument.
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
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
def log10(x):
    '''Returns the base 10 logarithm of x.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    if x <= zero:
        raise ValueError("Argument must be > 0")
    return ln(x)/ln(Dec(10))
def ln(x):
    '''Returns the natural logarithm of x.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    if x == one:
        return zero
    elif x <= zero:
        raise ValueError("Argument must be > 0")
    with decimal.localcontext() as ctx:
        ctx.prec += precision_increment
        # If x is less than 1, we'll calculate the log of its inverse,
        # then negate it before returning.
        inverse = one
        if x < one:
            x = 1/x
            inverse = -one
        # Get a starting value
        starting_value = f2d(math.log(float(x)))
        delta = Dec("1e-4")
        low = starting_value*(1 - delta)
        assert low > zero
        high = starting_value*(1 + delta)
        # Make sure we bracket the root
        assert((math.exp(low) - float(x))*(math.exp(high) - float(x)) < 0)
        root = inverse*FindRoot(low, high, lambda t: exp(t) - x)[0]
    return +root  # Force rounding to current precision
def pow(y, x):
    '''Returns y raised to the power x.
    '''
    if not isinstance(x, (Dec, int)):
        raise ValueError("Argument is not Decimal or integer type")
    if not isinstance(y, (Dec, int)):
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
            if isinstance(x, int) or int(x) == x:
                y = abs(y)
                if x % 2 == 0:
                    # Even power
                    if x < 0:
                        retval = 1/exp(-x*ln(y))
                    else:
                        retval = exp(x*ln(y))
                else:
                    # Odd power
                    if x < 0:
                        retval = -1/exp(-x*ln(y))
                    else:
                        retval = -exp(x*ln(y))
            else:
                raise ValueError("Negative base with noninteger exponent")
        else:
            retval = exp(x*ln(y))
    return +retval  # Force rounding to current precision
def sqrt(x):
    '''Returns the square root of x.
    '''
    if not isinstance(x, Dec):
        raise ValueError("Argument is not Decimal type")
    if x < 0:
        raise ValueError("Can't take square root of negative argument")
    if x == 0:
        return Dec(0)
    if x == 1:
        return Dec(1)
    return pow(x, 1/Dec(2))
def f2d(x):
    '''Convert a floating point number x to a Decimal.  See the
    decimal module's documentation for warnings about doing such
    things.
    '''
    if not isinstance(x, (float, str)):
        raise ValueError("x needs to be a float or string")
    return Dec(repr(float(x)))
def FindRoot(x0, x2, f, maxit=50):
    '''Inverse parabolic interpolation algorithm to find roots.  The
    root must be bracketed by x0 and x2.  f is the function to
    evaluate; it takes one Decimal argument and returns a Decimal.  If
    your f has more arguments, use functools.partial.  The iteration
    will terminate when two consecutive calculations differ by eps (see
    below) or less.
 
    Returns a tuple (root, number_of_iterations, eps)
 
    The routine will raise a ValueError exception if the number of
    iterations is greater than maxit.
 
    Reference:  "All Problems Are Simple" by Jack Crenshaw, Embedded
    Systems Programming, May, 2002, pg 7-14.  Translated from
    Crenshaw's C code modified by Don Peterson 20 May 2003.
 
    Crenshaw states this routine will converge rapidly on most
    functions, typically adding 4 digits to the solution on each
    iteration.  The routine works by starting with x0, x2, and finding
    a third x1 by bisection.  The ordinates are gotten, then a
    horizontally-opening parabola is fitted to the points.  The
    parabola's root's abscissa is gotten, and the iteration is
    repeated.
    '''
    # We'll find the value to a precision that is 10**(-n + 1) where
    # n is the current number of Decimal digits.  Note:  we add 1
    # because there are two guard digits and, if 1 wasn't added, some
    # of the iterations won't converge (e.g., asin(-0.5)).
    eps = Dec(10)**(-Dec(decimal.getcontext().prec) + 1)
    # Set up constants
    xmlast = x0
    x1 = y0 = y1 = y2 = b = c = temp = y10 = y20 = y21 = xm = ym = zero
    # Check input
    if not isinstance(x0, Dec):
        raise ValueError("Argument is not Decimal type")
    if not isinstance(x2, Dec):
        raise ValueError("Argument is not Decimal type")
    if x0 >= x2:
        raise ValueError("x0 must be strictly less than x2")
    if eps <= zero:
        raise ValueError("eps must be > 0")
    if maxit < one or not isinstance(maxit, int):
        raise ValueError("maxit must be integer > 0")
    # Handle special cases
    y0 = f(x0)
    if not y0:
        return x0, 0, eps
    y2 = f(x2)
    if not y2:
        return x2, 0, eps
    if y2*y0 > zero:
        raise ValueError("x0 and x2 don't bracket a root")
    # Iterate for root
    for ix in range(maxit):
        x1 = (x2 + x0)/two
        y1 = f(x1)
        if not y1 or abs(x1 - x0) < eps:
            return x1, ix+1, eps
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
                return xm, ix+1, eps
        else:
            b = (x1 - x0)/y10
            c = (y10 - y21)/(y21*y20)
            xm = x0 - b*y0*(one - c*y1)
            ym = f(xm)
            if not ym or abs(xm - xmlast) < eps:
                return xm, ix+1, eps
            xmlast = xm
            if ym*y0 < zero:
                x2 = xm
                y2 = ym
            else:
                x0 = xm
                y0 = ym
                x2 = x1
                y2 = y1
    msg = "FindRoot:  no convergence after {0} iterations".format(maxit)
    raise ValueError(msg)
if __name__ == "__main__": 
    # Use mpmath (http://mpmath.org/) to generate the numbers to test
    # against (i.e., assume mpmath's algorithms are correct).
    import mpmath as mp
    from pdb import set_trace as xx
    from wrap import wrap, dedent, indent, Wrap
    from lwtest import run, raises, assert_equal, Assert
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
        raises(ValueError, pow, Dec(-2), 1/Dec(3))
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
    exit(run(globals())[0])
