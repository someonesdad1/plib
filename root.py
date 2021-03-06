'''
Root Finding Routines
    The following functions find real roots of functions.  You can
    call them using e.g. mpmath numbers and find roots to arbitrary
    precision.  The functions QuadraticEquation, CubicEquation, and
    QuarticEquation use functions from the math and cmath library, so they
    can't be used with other floating point implementations.
 
    The fp keyword arguments let you perform these root-finding
    calculations with any floating point type that can convert strings like
    "1.5" to a floating point number.  Python's float type is the default.
 
    The following "prototypes" may be abbreviated; see the actual function
    definitions for details.
 
    Bisection(x1, x2, f)
        Finds a root by bisection.  Slow, but guaranteed to find the root
        if the root is bracketed in [x1, x2].
 
    Note:  Crenshaw, RootFinder, Brent, and kbrent are all forms of Brent's
    algorithm, but have different source code.  From my testing they behave
    quite similarly, but Jack Crenshaw's routine sometimes is a tad bit more
    efficient because of the more carefully thought out convergence criteria
    Jack used.
 
    Crenshaw(x1, x3, f)
        This is a slightly updated form of the translation of Jack
        Crenshaw's C code in the RootFinder routine.  It includes a keyword
        to show progress to a stream so you can watch convergence and it
        uses slightly better convergence criteria on both x and y so that
        sometimes it takes one less iteration.  
 
    RootFinder(x0, x2, f)
        Finds a root with quadratic convergence that lies between x0 and
        x2.  x0 and x2 must bracket the root.  The function whose root is
        being found is f(x).  The root is found when successive estimates
        differ by less than eps.  The routine will throw an exception if
        the number of iterations exceeds itmax.  The returned value is the
        root.
 
    Brent(x1, x2, f)
        Brent's method.  The root must be bracketed in [x1, x2].  Uses a
        combination of bisection and inverse quadratic interpolation.
        Translated from the C algorithm in "Numerical Recipes".
 
    kbrent(a, b, f)
        Another form of Brent's method from Kiusalaas, "Numerical Methods
        in Engineering with Python".
 
    Ostrowski(x0, f, deriv)
        An improved form of Newton's method which uses another evaluation of
        the function f(x) in each iteration to get fourth-order convergence.
 
    FindRoots(f, n, x1, x2)
        This is a general-purpose root finding routine.  It uses
        SearchIntervalForRoots to divide the interval [x1, x2] into n
        intervals and look for roots in each subinterval by sign changes.
        If a subinterval has a root, the RootFinder routine is used to find
        the root to precision eps.  If more than itmax iterations are used
        in any interval, an exception is raised.  Returns a tuple of the
        roots found.
 
    Pound(x)
        Utility function to reduce complex numbers with small real or
        imaginary components to pure imaginary or pure real numbers,
        respectively.
 
    Ridders(f, a, b)
        Finds a root via Ridder's method if the root is bracketed.
        Converges quadratically with two function evaluations per
        iteration.
 
    NewtonRaphson(f, fd, x)
        Quadratically-converging root-finding method; you need to supply the
        function f, its derivative fd, and an initial guess x.
 
    SearchIntervalForRoots(f, n, x1, x2)
        Given a function f of one variable, divide the interval [x1, x2]
        into n subintervals and determine if the function crosses the x
        axis in each subinterval.  Return a tuple of the intervals where
        there is a zero crossing (i.e., there's at least one root in each
        intervale in the tuple).
 
    BracketRoots(f, x1, x2):
        Expands an interval geometrically until a root is bracketed or the
        number of iterations exceed itmax.  Returns (a, b) where a and b
        bracket the root.  An exception is raised if too many iterations
        are used.
 
    The following functions find real and complex roots and use the math
    library, so are only for calculations with floats.  If adjust is True,
    any root where Im/Re < epsilon is converted to a real root.  epsilon is a
    global variable.  Set adjust to False, to have the roots returned as
    complex numbers.
 
    QuadraticEquation(a, b, c, adjust=True)
        Returns the two roots of a*x^2 + b*x + c = 0.  If adjust is true,
        any root where Im/Re < eps is converted to a real root.  Set
        adjust to zero to have all roots returned as complex numbers.
 
    CubicEquation(a, b, c, d, adjust=True)
        Returns the three roots of a*x^3 + b*x^2 + c*x + d = 0.  If adjust
        is true, any root where Im/Re < eps is converted to a real root.
        Set adjust to zero to have all roots returned as complex numbers.
 
    QuarticEquation(a, b, c, d, e, adjust=True)
        Returns the four roots of a*x^4 + b*x^3 + c*x^2 + d*x + e = 0.
        If adjust is true, any root where Im/Re < eps is converted to a
        real root.  Set adjust to zero to have all roots returned as
        complex numbers.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #???copyright???# Copyright (C) 2006, 2010 Don Peterson #???copyright???#
    #???contact???# gmail.com@someonesdad1 #???contact???#
    #???license???#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #???license???#
    #???what???#
    # <math> Root finding routines
    #???what???#
    #???test???# ["test/root_test.py"] #???test???#
    pass
if 1:   # Imports
    import sys
    import math
    import cmath
    import numbers
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    __all__ = [
        "ITMAX",
        "NoConvergence",
        "FindRoots",
        "RootFinder",
        "NewtonRaphson",
        "BracketRoots",
        "SearchIntervalForRoots",
        "Bisection",
        "Ridders",
        "Pound",
        "QuadraticEquation",
        "CubicEquation",
        "QuarticEquation",
        "Brent",
        "kbrent",
        "Crenshaw",
    ]
    ITMAX = 100     # Default maximum number of iterations
 
    # Ratio of imag/real to decide when something is a real root (or
    # real/imag to decide when something is pure imaginary).  Also used as
    # the default tolerance for root finding.  It's a string because
    # it will be converted to a floating point type inside the function
    # it's used in (some of the functions can allow other numerical types
    # besides floating point).
    epsilon = "2.5e-15"
     
    # Default relative tolerance for root finding.  I've set it to 1e-6.
    # It is rare in working with practical stuff to need higher precisions
    # because the problem's solution is probably limited by the
    # uncertainties in measured parameters -- and it's rare to have more
    # than 6 figures for measurements.
    eps0 = 1e-6
class NoConvergence(Exception):
    pass
def FindRoots(f, n, x1, x2, eps=eps0, itmax=ITMAX, fp=float,
              args=[], kw={}):
    '''This is a general-purpose root finding routine that returns a
    tuple of the roots found of the function f on the interval
    [x1, x2].
 
    It uses SearchIntervalForRoots to divide the interval into n
    intervals and look for roots in each subinterval.  If a
    subinterval has a root, the RootFinder routine is used to find the
    root to precision eps.  If more than itmax iterations are used in
    any interval, an exception is raised.
 
    Parameters
        f       Function to search for roots
        n       Number of subintervals
        x1      Start of overall interval to search
        x2      End of overall interval to search
        eps     Precision to find roots
        itmax   Maximum number of iterations
        fp      Floating point type to use for calculations
        args    Extra parameters for f()
        kw      Extra keyword arguments for f()
 
    Example:  Find the roots of sin(x)/x = 0 on the interval [1, 10]:
        import math
        for i in FindRoots(lambda x: math.sin(x)/x, 1000, 1, 10):
            print(i)
    which prints
        3.14159265359
        6.28318530718
        9.42477796077
    '''
    if not f:
        raise ValueError("f must be defined")
    if not isinstance(n, numbers.Integral):
        raise TypeError("n must be integer")
    if x1 >= x2:
        raise ValueError("Must have x1 < x2")
    intervals = SearchIntervalForRoots(f, n, x1, x2, fp=fp, args=args, kw=kw)
    if not intervals:
        return tuple()
    roots = []
    for x1, x2 in intervals:
        try:
            x, numits = RootFinder(x1, x2, f, eps=eps, itmax=itmax,
                                   args=args, kw=kw)
        except NoConvergence:
            pass
        else:
            roots.append(x)
    return tuple(roots)
def RootFinder(x0, x2, f, eps=eps0, itmax=ITMAX, fp=float, args=[], kw={}):
    '''Return (root, num_iterations) where root is a root of the function
    f() that lies in the interval [x0, x2] and num_iterations is the number
    of iterations taken.
 
    f() takes one parameter and returns a number.  eps is the precision to
    find the root to (it will be larger than the difference between the
    last two iterations) and itmax is the maximum number of iterations
    allowed.  fp is the number type to use in the calculation.  args is a
    sequence of any extra arguments that need to be passed to f; kw is a
    dictionary of keywords that will be passed to f.
 
    The routine will throw an exception if it receives bad input data or it
    doesn't converge.
 
    ----------------------------------------------------------------
 
    A root finding routine.  See "All Problems Are Simple" by Jack
    Crenshaw, Embedded Systems Programming, May, 2002, pg 7-14,
    jcrens@earthlink.com.  Originally, it could be downloaded from
    http://www.embedded.com/code.htm, but this address appears to be 
    defunct as of 2018. 
 
    I originally got Crenshaw's C code from this site and modified it in
    20 May 2003.
 
    In 2014, Jack sent me some of the files he could find related to this
    root finding method.  One of these files was titled "The IBM Algorithm
    for Inverse Parabolic Interpolation"; it was a FORTRAN function called
    RTMI.  It explains that the algorithm is due to an unknown author at
    IBM, probably in the 1960's.  I've associated it with Jack's name
    because he has studied it and done much to draw attention to the
    algorithm.
 
    The method is called "inverse parabolic interpolation" and will
    converge rapidly as it's a 4th order algorithm.  The routine works by
    starting with x0, x2, and finding a third x1 by bisection.  The
    ordinates are gotten, then a horizontally-opening parabola is fitted to
    the points.  The abscissa to the parabola's root is gotten, and the
    iteration is repeated.
    '''
    zero, one, two, eps = fp("0"), fp("1"), fp("2"), fp(eps)
    assert(x0 != x2 and eps > 0 and itmax > 0)
    if x2 < x0:
        x0, x2 = x2, x0
    x1 = y0 = y1 = y2 = b = c = y10 = y20 = y21 = xm = ym = 0
    xmlast = x0
    if args:
        y0, y2 = ((f(x0, *args, **kw), f(x2, *args, **kw)) if kw else
                  (f(x0, *args), f(x2, *args)))
    else:
        y0, y2 = (f(x0, **kw), f(x2, **kw)) if kw else (f(x0), f(x2))
    if not y0:
        return x0, 0
    if not y2:
        return x2, 0
    if y2*y0 > zero:
        msg = "Root not bracketed: y0 = {0}, y2 = {1}".format(y0, y2)
        raise ValueError(msg)
    for i in range(itmax):
        x1 = (x2 + x0)/2    # Bisection step
        if args:
            y1 = f(x1, *args, **kw) if kw else f(x1, *args)
        else:
            y1 = f(x1, **kw) if kw else f(x1)
        # 13 Oct 2014:  added 'abs(x1 - xmlast) < eps' test because
        # routine was not converging on sqrt(1e108), when it actually
        # only took 5 iterations.
        if not y1 or (abs(x1 - x0) < eps) or (abs(x1 - xmlast) < eps):
            return x1, i + 1
        if y1*y0 > zero:
            x0, x2, y0, y2 = x2, x0, y2, y0
        # Attempt inverse quadratic interpolation
        y10, y21, y20 = y1 - y0, y2 - y1, y2 - y0
        if y2*y20 < two*y1*y10:     # Do another bisection
            x2, y2 = x1, y1
        else:       # Inverse quadratic interpolation
            b, c = (x1 - x0)/y10, (y10 - y21)/(y21*y20)
            xm = x0 - b*y0*(one - c*y1)
            if args:
                ym = f(xm, *args, **kw) if kw else f(xm, *args)
            else:
                ym = f(xm, **kw) if kw else f(xm)
            if not ym or abs(xm - xmlast) < eps:
                return xm, i + 1
            xmlast = xm
            if ym*y0 < zero:
                x2, y2 = xm, ym
            else:
                x0, y0, x2, y2 = xm, ym, x1, y1
    raise NoConvergence("No convergence in RootFinder()")
def NewtonRaphson(f, fd, x, eps=eps0, itmax=ITMAX, show=False,
                  fp=float, args=[], kw={}):
    '''Returns the root using Newton-Raphson algorithm for solving
    f(x) = 0.
        f     = the function (must be a function object)
        fd    = the function's derivative (must be a function object)
        x     = initial guess of the root's location
        eps   = number used to determine when to quit
        itmax = the maximum number of iterations allowed
        fp    = type of numbers to calculate with
        args  = extra arguments for f
        kw    = keyword arguments for f
        show  = print intermediate values
 
    The iteration is
 
        xnew = x - f(x)/f'(x)
 
    until
 
        |dx|/(1+|x|) < eps
 
    is achieved.  Here, dx = f(x)/fd(x).  This termination condition is
    a compromise between |dx| < eps, if x is small and |dx|/|x| < eps,
    if x is large.
 
    Newton-Raphson converges quadratically near the root; however, its
    downfalls are well-known:  i) near-zero derivatives can send it into
    the next county; ii) ogive-shaped curves can make it oscillate and not
    converge; iii) you need to have an expression for both the function and
    its derivative.
 
    Adapted from
    http://www.phys.uu.nl/~haque/computing/WPark_recipes_in_python.html
    (is a defunct link as of Sep 2014).
    '''
    count, one = 0, fp("1.0")
    while True:
        if args:
            dx = f(x, *args, **kw)/fd(x) if kw else f(x, *args)/fd(x)
        else:
            dx = f(x, **kw)/fd(x) if kw else f(x)/fd(x)
        if abs(dx) < eps*(one + abs(x)):
            return x - dx
        x = x - dx
        count += 1
        if count > itmax:
            msg = "Too many iterations ({0}) in NewtonRaphson()".format(count)
            raise NoConvergence(msg)
        if show:
            print("NewtonRaphson[%d]: x = %s" % (count, x))
def BracketRoots(f, x1, x2, itmax=ITMAX, fp=float, args=[], kw={}):
    '''Given a function f and an initial interval [x1, x2], expand the
    interval geometrically until a root is bracketed or the number of
    iterations exceeds itmax.  Return (x3, x4), where the interval
    definitely brackets a root.  If the maximum number of iterations
    is exceeded, an exception is raised.
 
    fp      Floating point type to use
    args    Sequence of extra arguments to be passed to f
    kw      Dictionary of keywords that will be passed to f
 
    Adapted from zbrac in chapter 9.1 of Numerical Recipes in C, page 352.
    '''
    assert(f and x1 != x2)
    zero = fp("0")
    if x1 > x2:
        x1, x2 = x2, x1
    if args:
        f1, f2 = ((f(x1, *args, **kw), f(x2, *args, **kw)) if kw else
                  (f(x1, *args), f(x2, *args)))
    else:
        f1, f2 = (f(x1, **kw), f(x2, **kw)) if kw else (f(x1), f(x2))
    factor, count = fp("1.6"), 0
    while True:
        if f1*f2 < zero:
            return (x1, x2)
        if abs(f1) < abs(f2):
            x1 += factor*(x1 - x2)
            if args:
                f1 = f(x1, *args, **kw) if kw else f(x1, *args)
            else:
                f1 = f(x1, **kw) if kw else f(x1)
        else:
            x2 += factor*(x2 - x1)
            if args:
                f2 = f(x2, *args, **kw) if kw else f(x2, *args)
            else:
                f2 = f(x2, **kw) if kw else f(x2)
        count += 1
        if count > itmax:
            raise NoConvergence("No convergence in BracketRoots()")
def SearchIntervalForRoots(f, n, x1, x2, fp=float, args=[], kw={}):
    '''Given a function f of one variable, divide the interval [x1, x2]
    into n subintervals and determine if the function crosses the x axis
    in any subinterval; return a tuple of the intervals where there is a
    zero crossing.  fp is the floating point type to use.  args is a
    sequence of any extra parameters needed by f; kw is a dictionary of
    any keyword parameters needed by f.
 
    Idea from Numerical Recipes in C, zbrak, chapter 9, page 352.
    '''
    assert(f and n > 0 and x1 < x2)
    if args:
        y0 = f(x1, *args, **kw) if kw else f(x1, *args)
    else:
        y0 = f(x1, **kw) if kw else f(x1)
    x0, delta, intervals = x1, (x2 - x1)/(n + fp("1.")), []
    for i in range(1, n + 1):
        x = x1 + i*delta
        if args:
            y = f(x, *args, **kw) if kw else f(x, *args)
        else:
            y = f(x, **kw) if kw else f(x)
        if y0*y < 0:
            intervals.append((x0, x))
        x0, y0 = x, y
    return tuple(intervals)
def Bisection(x1, x2, f, eps=eps0, switch=False):
    '''Returns (root, num_it) (the root and number of iterations) by
    finding a root of f(x) = 0 by bisection.  The root must be
    bracketed in [x1,x2].
 
    If switch is True, an exception will be raised if the function
    appears to be increasing during bisection.  Be careful with this,
    as the polynomial test case converges just fine with bisection,
    but will cause an exception if switch is True.
 
    If the root is bracketed, bisection is guaranteed to converge,
    either on some root in the interval or a singularity within the
    interval.  It's also conceptually simple to understand:  draw a
    line between the two bracketing points and look at the midpoint.
    Choose the new interval containing the midpoint and the other
    point that evaluates to the opposite sign.  Repeat until you find
    the root to the required accuracy.  Each iteration adds a
    significant digit to the answer.
 
    The number of iterations and function evaluations will be
    log2(abs(x2 - x1)/eps).
 
    Adapted slightly from the book "Numerical Methods in Engineering
    with Python" by Jaan Kiusalaas, 2nd ed.  You can get the book's
    algorithms from http://www.cambridge.org/us/download_file/202203/.
 
    scipy has a bisection routine; it is probably in C/C++ and will
    be faster.
    '''
    f1, f2, d = f(x1), f(x2), abs(x2 - x1)
    if not f1:
        return x1, 0
    if not f2:
        return x2, 0
    if f1*f2 > 0:
        raise ValueError("Root is not bracketed")
    # Get the number of iterations we'll need
    n = int(math.ceil(math.log(abs(x2 - x1)/eps)/math.log(2)))
    for i in range(n):
        x3 = (x1 + x2)/2    # Abscissa of interval midpoint
        f3 = f(x3)          # Ordinate of interval midpoint
        if not f3:
            return x3, i + 1
        if switch and abs(f3) > abs(f1) and abs(f3) > abs(f2):
            msg = "f(x) increasing on interval bisection (i.e., a singularity)"
            raise ValueError(msg)
        # Choose which half-interval to use based on which one continues to
        # bracket the root.
        if f2*f3 < 0:
            x1, f1 = x3, f3  # Right half-interval contains the root
        else:
            x2, f2 = x3, f3  # Left half-interval contains the root
    x = (x1 + x2)/2
    assert(d/2**n <= eps)
    return x, n
def Ridders(a, b, f, eps=eps0, itmax=ITMAX):
    '''Returns (root, num_it) (root and the number of iterations) using
    Ridders' method to find a root of f(x) = 0 to the specified relative
    tolerance eps.  The root must be bracketed in [a, b].  If the number of
    iterations exceeds itmax, an exception will be raised.
 
    Wikipedia states:  Ridders' method is a root-finding algorithm based on
    the false position method and the use of an exponential function to
    successively approximate a root of a function f.
 
    Ridders' method is simpler than Brent's method but Press et. al. (1988)
    claim that it usually performs about as well.  It converges
    quadratically, which implies that the number of additional significant
    digits doubles at each step; but the function has to be evaluated twice
    for each step so the order of the method is 2**(1/2). The method is due
    to Ridders (1979).
 
    Adapted slightly from the book "Numerical Methods in Engineering with
    Python" by Jaan Kiusalaas, 2nd ed.  You can get the book's algorithms
    from http://www.cambridge.org/us/download_file/202203/.
    '''
    fa, fb = f(a), f(b)
    if not fa:
        return a, 0
    if not fb:
        return b, 0
    if fa*fb > 0:
        raise ValueError("Root is not bracketed")
    for i in range(itmax):
        # Compute the improved root x from Ridder's formula
        c = (a + b)/2
        fc = f(c)
        s = (fc**2 - fa*fb)**(1/2)
        if not s:
            if not fc:
                return c, i + 1
            raise ValueError("No root")
        dx = (c - a)*fc/s
        if (fa - fb) < 0:
            dx = -dx
        x = c + dx
        fx = f(x)
        # Test for convergence
        if i > 0 and abs(x - x_old) < eps*max(abs(x), 1.0):
            return x, i + 1
        x_old = x
        # Re-bracket the root as tightly as possible
        if fc*fx > 0:
            if fa*fx < 0:
                b, fb = x, fx
            else:
                a, fa = x, fx
        else:
            a, b, fa, fb = c, x, fc, fx
    raise NoConvergence("Too many iterations ({0}) in Ridders()".format(i))
def Brent(x1, x2, f, args=[], kw={}, eps=eps0, itmax=ITMAX):
    '''Return (r, numits) where r is the root of the function f that
    is known to lie in the interval [x1, x2].  The root will be found
    within the absolute tolerance eps.  numits is the number of
    iterations it took.
 
    args is a sequence of extra arguments for f(); kw is a dictionary
    of keyword arguments for f().
 
    The is essentially the zbrent routine from "Numerical Recipes in
    C", translated into python.
    '''
    def F(x):
        if args:
            return f(x, *args, kw=kw) if kw else f(x, *args)
        else:
            return f(x, kw=kw) if kw else f(x)
    a, b, c = x1, x2, x2
    i, EPS = 0, 3.0e-8
    fa, fb = F(a), F(b)
    fc = fb
    if (fa > 0.0 and fb > 0.0) or (fa < 0.0 and fb < 0.0):
        raise ValueError("Root must be bracketed")
    while i < itmax:
        i += 1
        if (fb > 0.0 and fc > 0.0) or (fb < 0.0 and fc < 0.0):
            c, fc = a, fa
            e = d = b - a
        if abs(fc) < abs(fb):
            a = b
            b = c
            c = a
            fa = fb
            fb = fc
            fc = fa
        tol1 = 2.0*EPS*abs(b) + 0.5*eps
        xm = 0.5*(c - b)
        if abs(xm) <= tol1 or fb == 0.0:
            return (b, i)       # *** Found the root ***
        if abs(e) >= tol1 and abs(fa) > abs(fb):
            s = fb/fa
            if a == c:
                p, q = 2.0*xm*s, 1.0 - s
            else:
                q, r = fa/fc, fb/fc
                p = s*(2.0*xm*q*(q - r) - (b - a)*(r - 1.0))
                q = (q - 1.0)*(r - 1.0)*(s - 1.0)
            if p > 0.0:
                q = -q
            p = abs(p)
            min1 = 3.0*xm*q - abs(tol1*q)
            min2 = abs(e*q)
            if 2.0*p < (min1 if min1 < min2 else min2):
                e = d
                d = p/q
            else:
                d = xm
                e = d
        else:
            d = xm      # Bounds decreasing too slowly, use bisection.
            e = d
        a, fa = b, fb
        if abs(d) > tol1:   # Evaluate new trial root.
            b += d
        else:
            b += tol1 if xm >= 0 else -tol1
        fb = F(b)
    raise NoConvergence("No convergence in Brent()")
def kbrent(a, b, f, eps=eps0, itmax=ITMAX):
    '''Finds root of f(x) = 0 by combining quadratic interpolation
    with bisection (simplified Brent's method).  The root must be
    bracketed in (a, b).  Calls user-supplied function f(x).
 
    The method is defined to converge at x if:
        1.  f(x) < eps
        2.  The interval [a, b] width < eps*max(abs(b), 1)
 
    This algorithm (slightly modified) is from page 150 in the book
    J. Kiusalaas, "Numerical Methods in Engineering with Python".
    '''
    x1, x2 = a, b
    f1 = f(x1)
    if not f1:
        return x1
    f2 = f(x2)
    if not f2:
        return x2
    if f1*f2 > 0:
        raise ValueError("Root is not bracketed")
    x3 = (a + b)/2  # Midpoint for bisection
    for i in range(itmax):
        f3 = f(x3)
        if abs(f3) < eps:
            return x3, i + 1
        #print("i = {0}  x3 = {1:.8g}  f3 = {2:.8g}".format(i + 1, x3, f3))
        # Tighten the brackets on the root
        if f1*f3 < 0:
            b = x3  # New interval is left-hand half
        else:
            a = x3  # New interval is right-hand half
        if (b - a) < eps*max(abs(b), 1):
            return (a + b)/2, i + 1
        # Try quadratic interpolation
        denom = (f2 - f1)*(f3 - f1)*(f2 - f3)
        numer = (x3*(f1 - f2)*(f2 - f3 + f1) +
                 f2*x1*(f2 - f3) + f1*x2*(f3 - f1))
        # If division by zero, push x out of bounds
        x = x3 + (f3*numer/denom if denom else b - a)
        # If interpolation goes out of bounds, use bisection.  This test
        # is equivalent to (a < x < b) if a < b or (b < x < a) if b < a.
        # 13 Oct 2014:  added inf test because was getting
        # nonconvergence for simple test case (sqrt(1e108)) because x
        # was NaN.
        if denom == float("inf") or (b - x)*(x - a) < 0:
            x = a + (b - a)/2
        # Let x3 be x & choose new x1 and x2 so that x1 < x3 < x2
        if x < x3:
            x2, f2 = x3, f3
        else:
            x1, f1 = x3, f3
        x3 = x
    raise NoConvergence("No convergence in kbrent()")
def Crenshaw(x1, x3, f, eps=eps0, itmax=ITMAX, dbg=None, p=4):
    '''Returns (root, number_of_iterations).
      x1, x3        Initial estimates of the root and must bracket it.
      f             Function f(x) to call to evaluate.
      eps           Relative change used to determine when the algorithm
                    has converged.
      itmax         Maximum number of iterations to use.
      dbg           If not None, it must be a stream; the function prints
                    intermediate values to this stream so you can watch
                    convergence.
      p             Number of significant digits to print to dbg stream.
    '''
    d = {
        "p"     : p,
        "xlast" : None,
        "ymin"  : 1e308,
        "ymax"  : -1e308,
        "eps"   : eps,
    }
    def Dbg(s, end="\n"):
        if dbg:
            for i in s.split("\n"):
                dbg.write("+ {0}{1}".format(i, end))
    def F(*args, **kw):
        '''Parameters args:  the first element is x and is mandatory.
        The following parameters are passed to the function f.  The
        keyword dictionary must contain a dictionary named opts; it is
        used in this function, the opts key is removed, and the
        remaining dictionary is passed to the function f.
 
        This is a wrapper function that calls f(x) given a dictionary d
        that contains the following keys:
          ymin        Minimum y value encountered
          ymax        Maximum y value encountered
          eps         Desired convergence radius, relative
          converged   Will be True when the current y value is less than
                      eps*(ymax - ymin).
        This is per Jack Crenshaw's follow-up article on 13 Apr 2004
        entitled "A root-finding algorithm" in "Embedded Systems
        Development".  Jack's realization was that the original algorithm
        he published in May 2002 ("All Problems Are Simple" in "Embedded
        Systems Programming", pg 7-14) often converged to a value better
        than requested by the user (I've noticed the same behavior).
        Jack's insight was to look at successive y values and base
        convergence on getting a y value that was less in absolute value
        than eps*(ymax - ymin).  This function, F(x) does the bookkeeping
        so that a) the minimum and maximum y values are remembered and b)
        the convergence status is returned in a Boolean variable.  You'll
        find this method gets the root to the desired precision and does it
        in fewer steps than the original algorithm.
 
        Note:  Jack has mentioned numerous times that this algorithm was
        from some unknown genius at IBM in the 1960's and was part of their
        FORTRAN library code.  Jack studied the algorithm and wrote
        articles in "Embedded Systems Development" to popularize it.  The
        method is inverse parabolic interpolation with bisection and it
        converges quadratically.
        '''
        args = list(args)
        x = args[0]
        del args[0]
        d = kw["opts"]  # Options dictionary
        p = d["p"]  # Number of digits in debug printing
        del kw["opts"]
        def dx(x):
            diff = abs(x - d["xlast"])
            if d["xlast"]:
                return diff/d["xlast"]
            elif x:
                return diff/x
            else:
                return 0
        if args:
            y = f(x, *p, **kw) if kw else f(x, *p)
        else:
            y = f(x, **kw) if kw else f(x)
        d["xlast"] = x
        d["ymin"] = ymin = min(y, d["ymin"])
        d["ymax"] = ymax = max(y, d["ymax"])
        Dbg("f(x): x = {x:.{p}g}, y = {y:.{p}g}, Y min/max: "
            "[{ymin:.{p}g}, {ymax:.{p}g}]".format(**locals()))
        d["converged"] = abs(y) < d["eps"]*(ymax - ymin) and dx(x) < eps
        return y
    Dbg('''Crenshaw() called with:
    Starting interval = [{x1:.{p}g}, {x3:.{p}g}]
    eps   = {eps}
    itmax = {itmax}'''.format(**locals()))
    # Local variables
    x2 = y2 = 0     # Middle point in bisections
    xm = ym = 0     # Estimated root in interpolations
    y1 = y3 = y21 = y31 = y32 = 0
    b = c = 0       # Temporary variables
    # Set up values at initial points.
    # Test each just in case we luck out.
    Dbg("Get function values at both ends")
    y1, y3 = F(x1, opts=d), F(x3, opts=d)
    if not y1 or d["converged"]:
        Dbg("--> Converged to " + str((x1, 0)))
        return (x1, 0)
    if not y3 or d["converged"]:
        Dbg("--> Converged to " + str((x3, 0)))
        return (x3, 0)
    # If the signs are the same, we were given
    # bad initial values of x1, x3
    if y3*y1 > 0.0:
        raise ValueError("Root not bracketed")
    for i in range(itmax):
        x2 = (x3 + x1)/2  # Bisection step
        y2 = F(x2, opts=d)
        Dbg("Bisection x2 = {x2:.{p}g}, y2 = {y2:.{p}g}".format(**locals()))
        if not y2 or d["converged"]:
            Dbg("--> Converged to " + str((x2, i + 1)))
            return (x2, i + 1)
        if y2*y1 > 0:  # Relabel to keep the root between x1 and x2.
            x1, x3, y1, y3 = x3, x1, y3, y1
        # Attempt a parabolic interpolation.
        y21, y32, y31 = y2 - y1, y3 - y2, y3 - y1
        if y3*y31 < 2*y2*y21:
            # Do another bisection
            x3, y3 = x2, y2
            Dbg("Can't use parabolic; x3 now {x3:.{p}g}".format(**locals()))
        else:
            # Parabolic interpolation
            try:
                # y21 and y31 cannot be zero, but y32 might.
                b, c = (x2 - x1)/y21, (y21 - y32)/(y32*y31)
                xm = x1 - b*y1*(1 - c*y2)
                ym = F(xm, opts=d)
                Dbg("Parabolic xm = {xm:.{p}g}, ym = {ym:.{p}g}".
                    format(**locals()))
                if not ym or d["converged"]:
                    Dbg("--> Converged to " + str((xm, i + 1)))
                    return (xm, i + 1)
                # Relabel to keep root between x1 and x2.
                if(ym*y1 < 0):
                    x3, y3 = xm, ym
                else:
                    x1, y1, x3, y3 = xm, ym, x2, y2
            except ZeroDivisionError:
                f = sys.stderr
                print("Division by zero in RootFinder:", file=f)
                print("  x1  =", x1, file=f)
                print("  x2  =", x2, file=f)
                print("  y21 =", y21, file=f)
                print("  y31 =", y31, file=f)
                print("  y32 =", y32, file=f)
                # Do another bisection
                x3, y3 = x2, y2
    raise NoConvergence("No convergence in Crenshaw()")
def Ostrowski(x0, f, deriv, eps=eps0, itmax=ITMAX, dbg=None):
    '''Returns (root, num_iterations) for the root of the function f(x).
    
    x0 is the initial guess for the root, f is f(x), the univariate
    function whose root we want, deriv is the first derivative function of
    f(x), and eps is the relative change in successive root iterations to
    use as a convergence criterion.  If dbg is not None, it must be a
    stream object to which the successive iterations will be dumped.
 
    Ostrowski's method is based on Newton's method with a follow-on
    evaluation to refine the root:
 
        y_n = x_n - f(x_n)/f'(x_n)
        x_(n+1) = y_n - f(y_n)*(x_n - y_n)/(f(x_n) - 2*f(y_n))
 
    For each iteration step, there are three function evaluations: f(x_n),
    f'(x_n), and f(y_n).
 
    Reference:  "Ostrowski's Method for Finding Roots" by Namir Shammas in 
    "HP Solve", issue 28, July 2012, page 8.
    '''
    x = x0
    if dbg:
        dbg.write("+ Starting value of x = {}\n".format(x0))
    xn = x0
    for i in range(1, itmax):
        a = f(xn) 
        yn = xn - a/deriv(xn)
        b = f(yn)
        c = a - 2*b
        if not c:
            if b:
                raise ZeroDivisionError("(a - 2*b) is zero")
            else:
                return (yn, i)    # yn is a root of f
        xn1 = yn - b*(xn - yn)/c
        # Dump to debug stream
        if dbg:
            dbg.write("+ i = {}  xnew = {}, ynew = {}\n".format(i, sig(xn1), sig(yn)))
        # Check for convergence
        if xn1 == xn:
            return (xn, i)
        if xn:
            rel = (xn1 - xn)/xn
            if abs(rel) <= eps:
                return (xn, i)
        else:
            # The following may not be an exact interpretation, but it
            # allows for the case where x was zero and avoids a divide by
            # zero error.
            rel = (xn - xn1)/xn1
            if abs(rel) <= eps:
                return (xn1, i)
        # Set up for next iteration
        xn = xn1
    raise NoConvergence("No convergence in Ostrowski()")
def Pound(x, adjust=True, eps=float(epsilon)):
    '''Turn x into a real if the imaginary part is small enough
    relative to the real part and adjust is True.  The analogous thing
    is done for a nearly pure imaginary number.
 
    The name comes from imagining the complex number is a nail which a
    light tap from a hammer makes it lie parallel to either the real or
    imaginary axis.
 
    Set adjust to False so that only pure real or imaginary numbers are
    converted.  If adjust is True, then the conversion is done if the
    ratio of the real to imaginary part is small enough.
    '''
    # Handle the "pure" cases first.
    if not x.real and not x.imag:
        return 0
    elif x.real and not x.imag:
        return x.real
    elif not x.real and x.imag:
        return x.imag*1j
    # Adjust if the Re/Im or Im/Re ratio is small enough; otherwise
    # return unchanged.
    if adjust and x.real and abs(x.imag/x.real) < eps:
        return x.real
    elif adjust and x.imag and abs(x.real/x.imag) < eps:
        return x.imag*1j
    return x
def QuadraticEquation(a, b, c, adjust=True, force_real=False):
    '''Return the two roots of a quadratic equation.  The equation is a*x^2
    + b*x + c = 0; the coefficients can be complex.  Note this works with
    float types only.  Set force_real to True to force the returned values
    to be real.
 
    Here's a derivation of the method used.  Multiply by 4*a and
    complete the square to get
 
        (2*a*x + b)**2 = (b**2 - 4*a*c)
        x = (-b +/- sqrt(b**2 - 4*a*c))/(2*a)           (1)
 
    Next, multiply the equation by 1/x**2 to get
 
        a + b*(1/x) + c*(1/x**2) = 0
 
    Complete the square to find
 
        1/x = (-b -/+ sqrt(b**2 - 4*a*c))/(2*c)
 
    or
 
        x = 2*c/(-b -/+ sqrt(b**2 - 4*a*c))             (2)
 
    Equations 1 or 2 may provide more accuracy for a particular root.
    There can be loss of precision in the discriminant when a*c is small
    compared to b**2.  This happens when the roots vary greatly in absolute
    magnitude.  Suppose they are x1 and x2; then (x - x1)*(x - x2) = x**2 -
    (x1 + x2)*x + x1*x2 = 0.  Here,
 
        a = 1
        b = -(x1 + x2)
        c = x1*x2
 
    Suppose x1 = 1000 and x2 = 0.001.  Then b = -1000.001 and c = 1.  The
    square root of the discriminant is 999.999 and the subtraction b -
    sqrt(D) results in 0.0001, with a loss of around 6 significant figures.
 
    The algorithm is to use these two equations depending on the sign
    of b (D = b**2 - 4*a*c):
 
    b >= 0:
        x1 = -b - sqrt(D))/(2*a)    and     x2 = 2*c/(-b - sqrt(D))
    b < 0:
        x1 = 2*c/(-b + sqrt(D))     and     x2 = -b + sqrt(D))/(2*a)
    '''
    if not a:
        raise ValueError("a cannot be zero")
    if isinstance(b, numbers.Complex):
        p = b/a
        q = c/a
        d = cmath.sqrt(p*p/4 - q)
        if force_real:
            return tuple([i.real for i in (-p/2 + d, -p/2 - d)])
        return Pound(-p/2 + d, adjust), Pound(-p/2 - d, adjust)
    else:
        # More stable numerical method
        D = cmath.sqrt(b*b - 4*a*c)
        if b >= 0:
            x1, x2 = (-b - D)/(2*a), 2*c/(-b - D)
        else:
            x1, x2 = 2*c/(-b + D), (-b + D)/(2*a)
        if force_real:
            return tuple([i.real for i in (x1, x2)])
        return Pound(x1, adjust), Pound(x2, adjust)
def CubicEquation(a, b, c, d, adjust=True, force_real=False):
    '''Returns the roots of a cubic with complex coefficients: a*z**3
    + b*z**2 + c*z + d.
 
    You can set force_real to True to make all the returned roots be
    real (this causes the real part of the calculated roots to be
    returned).  This may be of use e.g. when solving cubic equations
    of state like the Peng-Robinson or Redlich-Kwong equations.  You
    must exercise caution, as you might be throwing a true complex
    root away.
 
    If adjust is True and the roots have imaginary parts small enough
    relative to the real part, they are converted to real numbers.
 
    Example:
        for i in CubicEquation(1, 1, 1, 1):
            print(i)
    prints
        -1.0
        (-6.93889390391e-17+1j)
        (-6.93889390391e-17-1j)
    However,
        for i in CubicEquation(1, 1, 1, 1, adjust=True):
            print(i)
    prints
        -1.0
        1j
        -1j
    Note
        for i in CubicEquation(1, 1, 1, 1, force_real=True):
            print(i)
    prints
        -1.0
        -6.93889390391e-17
        -6.93889390391e-17
    which is probably *not* what you want because it throws important
    information away.
 
    ----------------------------------------------------------------------
    The following Mathematica commands were used to generate the code for
    the cubic and quartic routines.
 
    (* Cubic *)
      f = a*x^3 + b*x^2 + c*x + d;
      g = Solve[f == 0, x];
      FortranForm[g]
 
    (* Quartic *)
      f = a*x^4 + b*x^3 + c*x^2 + d*x + e;
      g = Solve[f == 0, x];
      FortranForm[g]
 
    The output was edited with the following changes:
 
      1. Change (0,1) to 1j
      2. Remove extra parentheses and comma at end of expression
      3. Substitute (1/3.) for 0.3333333333333333
      4. Substitute (2/3.) for 0.6666666666666666
      5. Put backslashes on lines as appropriate
 
    After this manipulation, common terms were looked for and set up as
    single variables to avoid recalculation.  This removed a lot of
    duplication.
 
    The special case where we're finding the third or fourth root of a
    real or complex number, we use De Moivre's theorem:  Let z be a
    complex number written in polar form z = r*(cos(x) + i*sin(x)).
    Then
 
      z^(1/n) = r^(1/n)*(cos((x + 2*k*pi)/n) + i*sin((x + 2*k*pi)/n))
 
    where k varies from 0 to n-1 to give the n roots of z.
    '''
    if not a:
        raise ValueError("a must not be zero")
    if b == 0 and c == 0 and d == 0:
        return 0, 0, 0
    if b == 0 and c == 0:
        # Find the three cube roots of (-d) using De Moivre's theorem.
        r = abs(-d)  # Magnitude
        # Get the argument
        if isinstance(-d, numbers.Complex):
            x = math.atan2((-d).imag, (-d).real)
        else:
            x = 0
            if (-d) < 0:
                x = math.pi
        n = 3
        rn = r**(1./n)
        def f(x, k):
            return (rn*(math.cos((x + 2*k*math.pi)/n) +
                    1j*math.sin((x + 2*k*math.pi)/n)))
        roots = f(x, 0), f(x, 1), f(x, 2)
        if force_real:
            return tuple(i.real for i in roots)
        return tuple(Pound(i, adjust) for i in roots)
    u = -2*b**3 + 9*a*b*c - 27*a**2*d
    D = -b**2 + 3*a*c
    v = cmath.sqrt(4*D**3 + u**2)
    w = 2**(1./3)
    y = (u + v)**(1./3)
    st = 1j*math.sqrt(3)
    z = -b/(3.*a)
    t = 3*2**(2./3)*a*y
    x = 6*w*a
    x1 = z - w*D/(3.*a*y) + y/(3.*w*a)
    x2 = z + ((1 + st)*D)/t - ((1 - st)*y)/x
    x3 = z + ((1 - st)*D)/t - ((1 + st)*y)/x
    if force_real:
        return tuple(i.real for i in (x1, x2, x3))
    return tuple(Pound(i, adjust) for i in (x1, x2, x3))
def QuarticEquation(a, b, c, d, e, adjust=True, force_real=False):
    '''Returns the roots of a quartic with complex coefficients:
    a*x**4 + b*x**3 + c*x**2 + d*x + e.  Note this works with float
    types only.  Set force_real to make all the returned roots be
    real.
 
    You can set force_real to True to make all the returned roots be
    real (this causes the real part of the calculated roots to be
    returned).  You must exercise caution, as you might be throwing a
    true complex root away.
 
    If adjust is True and a root has an imaginary part small enough
    relative to the real part, it is converted to a real number.
    Analogously, if the real parts are small enough relative to the
    imaginary parts, the root is converted to a pure imaginary.
 
    Example 1:
        for i in QuarticEquation(1, 1, 1, 1, 1):
            print(i)
    prints
        (-0.809016994375-0.587785252292j)
        (-0.809016994375+0.587785252292j)
        (0.309016994375-0.951056516295j)
        (0.309016994375+0.951056516295j)
 
    Example 2:  (x-1)*(x-2)*(x-3)*(x-4) is a quartic polynomial with
    a = 1, b = -10, c = 35, d = -50, and e = 24.  Then
        for i in QuarticEquation(1, -10, 35, -50, 24):
            print(i)
    prints
        0.9999999999999992
        2.0000000000000004
        2.9999999999999996
        4.000000000000001
 
    See the docstring for CubicEquation to find out how the equations were
    generated.
    '''
    if not a:
        raise ValueError("a must not be zero")
    if b == 0 and c == 0 and d == 0 and e == 0:
        return 0, 0, 0, 0
    if b == 0 and c == 0 and d == 0:
        # Find the four fourth roots of (-e) using De Moivre's theorem.
        r = abs(-e)  # Magnitude
        # Get the argument
        if isinstance(-e, numbers.Complex):
            x = math.atan2((-e).imag, (-e).real)
        else:
            x = 0
            if (-e) < 0:
                x = math.pi
        n = 4
        rn = r**(1./n)
        def f(x, k):
            return (rn*(math.cos((x + 2*k*math.pi)/n) +
                    1j*math.sin((x + 2*k*math.pi)/n)))
        roots = f(x, 0), f(x, 1), f(x, 2), f(x, 3)
        if force_real:
            return tuple([i.real for i in roots])
        return tuple([Pound(i, adjust) for i in roots])
    cr3 = 2**(1./3)
    p = -b/(4.*a)
    q = (c**2 - 3*b*d + 12*a*e)
    r = 2*c**3 - 9*b*c*d + 27*a*d**2 + 27*b**2*e - 72*a*c*e
    s = cmath.sqrt(-4*q**3 + r**2)
    t = (3*a*(r + s)**(1./3))
    u = (r + s)**(1./3)/(3.*cr3*a)
    v = (-(b**3./a**3) + (4.*b*c)/a**2 - (8.*d)/a)
    w = cmath.sqrt(b**2/(4.*a**2) - (2*c)/(3.*a) + (cr3*q)/t + u)
    x = b**2/(2.*a**2) - (4*c)/(3.*a) - (cr3*q)/t - u
    y = cmath.sqrt(x - v/(4.*w))/2
    z = cmath.sqrt(x + v/(4.*w))/2
    roots = p - w/2. - y, p - w/2. + y, p + w/2. - z, p + w/2. + z
    if force_real:
        return tuple([i.real for i in roots])
    return tuple(Pound(i, adjust) for i in roots)
