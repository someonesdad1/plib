'''

TODO
    - Remove args & kw from everything except Crenshaw and Bisection
        - These are used for more complicated cases
        - Ridders, Brent, ITP for speedy evaluations & single-argument functions
    - Add fp=float, dbg=None, args=[], kw={} to each call
        - Modify each line to make sure each number is type fp
        - If dbg is not None, it's a stream to send debugging messages to
        - Put in the necessary Dbg calls
        - Equip function calls with args & kw
    - Primary routines
        - Ridders, Brent, and Rootfinder are the fastest on the cos(x)-x example.  All
          things being equal, the simplest and shortest code should be preferred.
    - The beginning root bracketing of each method could be a separate function called
      RootIsBracketed(a, b, f) which raises an exception if it's not bracketed
    - Standardization
        - (a, b) brackets root, f for function name
        - Functions should have same args & kw
        - Rename epsilon to something that is specific to complex numbers
        - dbg should be a boolean that causes debugging output to stderr so that you can
          see convergence
    - Debugging
        - Use dbg == stream in function calls to turn it on
        - Colorized output goes to stream
        - Done with Dbg()
    - Jack's convergence observation
        - Figure out the slightly better criterion used in Crenshaw and add it to both
          RootFinder and kbrent.
    - fp argument
        - See if every routine can be given an fp keyword argument; this would be the
          floating point type to use for the calculations.  Default to flt.  Does this
          change by virtue of e.g. needing a math module inside the functions?  If so,
          then float may be the only real choice.
        - No, math module not used in root finding modules (except ceil in bisect())

    - Change printing stuff to use f-strings, as they are easier to read
    - Each routine should make use of a debug stream passed into the function.  Watching
      an algorithm converge or diverge is helpful to understand what's going on.
        - Use some standardized color names in the module for debugging output
            - grnl abscissa
            - yell ordinate
            - ornl for convergence quality
    - Quadratic, etc.
        - It's possible that this code will work without modifications on both
          floats/complex and mpf/mpc numbers.  If so, point this out.
        - Consider converting the routines to use Decimal numbers
    - Write a test routine that sets up a number of different problems and reports on
      the time each method uses, number of iterations, and goodness of answer.  This
      could obviously uncover some things that might not work right, as they should give
      the same answers.  This would make a good addition to the testing strategy.
    - Ostrokowksi
        - Uses tol as a relative convergence number rather than absolute like the other
          methods.  This probably should be standardized to an absolute number.
        - Include fp, args, kw

    - Recommendations
        - Many of us probably work with problems whose information comes from physical
          measurements.  Such data are likely to only have a few digits of relevance.
          Since today's computers are so fast, you can probably find your root
          adequately with the simple bisection algorithm.
        - Start with bisection because it's reliable.  Switch to other methods when you
          run into problems.  Brent and RootFinder and the same basic algorith; Ridders
          is similar but uses a different interpolation function.  
        - https://www.cs.princeton.edu/courses/archive/fall12/cos323/notes/cos323_f12_lecture02_rootfinding.pdf
          is a good overview of the basics.  The three pictures on page 9 show some of
          the things that can go wrong:  1) a root at a tangent point, 2) a singularity,
          and 3) a pathological case.  Construct some test cases using these cases.

---------------------------------------------------------------------------

Root Finding Routines

    - Ridders, Brent, ITP are for single argument functions and are intended to be fast
      general purpose routines
    - Extra arguments & keyword arguments for the function whose root is to be found
        - Crenshaw (is Brent's method)
        - Bisection
    - fp argument lets you use float, flt, mpmath.mpf, or Decimal math types

    Features
        - dbg stream argument to send debugging information to watch convergence
        - args, kw for extra parameters in the function f
        - fp type to use float, flt, mpmath.mpf, or Decimal math types
        - itmax to control maximum number of iterations

References ([x:y:z] means page y in reference x or page z in the PDF form)
    
    [1] Various emails with Jack Crenshaw around 2014
    
    [2] J. Kiusalaas, "Numerical Methods in Engineering with Python", Cambridge
        University Press, 2005.  You can download the book's algorithms from
        http://www.cambridge.org/us/download_file/202203/.
    
    [3] W. Press, et. al., "Numerical Recipes in C", 2nd ed., Cambridge University
        Press, 1992.
    
---------------------------------------------------------------------------
    
Notes
    
Division by multiplication & subtraction

    https://www.cs.princeton.edu/courses/archive/fall12/cos323/notes/cos323_f12_lecture02_rootfinding.pdf
    notes that in some computers a hardware divide is not available, so division can be
    simulated in software by using Newton-Raphson iteration using only multiplication
    and subtraction:
    
        a/b = a*(1/b)
        f(x) = 1/x - b = 0  Solve f(x) = 0 to get reciprocal of b
        f'(x) = -1/x**2
        x[n+1] = x - (1/x - b)/(-1/x**2)   (Here x = x[n])
               = x*(2 - b*x)
    
    Example:  calculate 3/5.  a = 3 and b = 5.  Start with x = 0.1.  Some python code
    for this iteration is (this calculates 1/b)
    
        x, b = 0.1, 5
        tol = 1e-15     # Roughly floating point precision
        for i in range(20):
            xnew = x*(2 - b*x)
            print(f"{i:2d} {xnew:.15f}")
            if abs(x - xnew) < tol:
                break
            x = xnew
    
    which prints out the calculation of 1/5 as
    
        0 0.150000000000000
        1 0.187500000000000
        2 0.199218750000000
        3 0.199996948242188
        4 0.199999999953434
        5 0.200000000000000
        6 0.200000000000000
    
    Here's another example:  calculate 42.7/6.2.  Use 0.1 as a starting value to get an
    iterative calculation of 1/6.2:
    
        0 0.138000000000000
        1 0.157927200000000
        2 0.161220196900992
        3 0.161290292091457
        4 0.161290322580639
        5 0.161290322580645
        6 0.161290322580645
    
    But the starting value is important:  try the same problem but start with x = 7.
    The algorithm diverges and results in -∞.  This is a well-known weakness of
    Newton-Raphson root-finding, as it is unstable when the function's derivative is a
    small number.  Here, f'(7) is about -0.02.
    
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2006, 2010 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # <math> Root finding routines
        ##∞what∞#
        ##∞test∞# ["test/root_test.py"] #∞test∞#
        pass
    if 1:  # Imports
        import decimal
        import math
        import numbers
        import sys
    if 1:  # Custom imports
        from color import t
        from lwtest import Assert
        from wrap import dedent
        from timer import Timer
        from f import flt
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        t.dbg = t.skyl   # Color for debugging output
if 1:  # Root finders
    def Crenshaw(a, b, f, tol=1e-6, itmax=50, fp=float, dbg=None, args=[], kw={}):
        '''Return (root, num_iterations) where root is a root of the function f() that
        lies in the interval [a, b] and num_iterations is the number of iterations it
        took to find the root.

        a       Start of bracketing interval
        b       End of bracketing interval
        f       Function to evaluate.  If it needs more than one argument or keyword
                arguments, add the extra arguments to the sequence args and kw.
        tol     The routine has converged when the last two function values differ by
                less than tol.
        itmax   Maximum number of iterations; if exceeded, a ValueError will be raised
        fp      Number type to do the calculations with
        args    Sequence of extra arguments for the function f
        kw      Keyword arguments for the function f
        dbg     If not None, send debugging messages to this stream
    
        The routine will raise an exception if it receives bad input data or it doesn't converge.
    
        ----------------------------------------------------------------
    
        A root finding routine.  See "All Problems Are Simple" by Jack Crenshaw,
        Embedded Systems Programming, May, 2002, pg 7-14, jcrens@earthlink.com.
        Originally, it could be downloaded from http://www.embedded.com/code.htm, but
        this URL is defunct as of 2018.  I originally got Crenshaw's C code from this
        site and modified it in 20 May 2003.
    
        In 2014, Jack sent me some of the files he could find related to this root
        finding method.  One of these files was titled "The IBM Algorithm for Inverse
        Parabolic Interpolation"; it was a FORTRAN function called RTMI.  It explains
        that the algorithm is due to an unknown author at IBM.  Jack remembered coming
        across it in the 1960's.  I've associated it with Jack's name because he has
        studied it and done much to draw attention to the algorithm, but it's basically
        Brent's algorithm.
    
        The method is called "inverse parabolic interpolation" and will converge rapidly
        as it's a 4th order algorithm.  The routine works by starting with a, b, and
        finding a third x1 by bisection.  The ordinates are gotten, then a
        horizontally-opening parabola is fitted to the points.  The abscissa to the
        parabola's root is gotten, and the iteration is repeated.
    
        Sad news:  on 25 Feb 2025 I got an email from a friend of Jack's that Jack died
        on 24 Dec 2024.  I originally contacted Jack about this algorithm and it led to
        an email friendship over a decade with many hundreds of emails on a bewildering
        variety of topics.  I never got to meet him (we lived on opposite coasts of the
        US), but we connected over many things.  I miss his lively mind.
        '''
        fnname = "Crenshaw"
        # Check function arguments
        if a == b:
            raise ValueError("a and b cannot be equal")
        if tol <= 0:
            raise ValueError("tol must be > 0")
        if not isinstance(itmax, int) and itmax <= 0:
            raise ValueError("itmax must be an integer > 0")
        # Convert a and b to fp type
        a, b = fp(a), fp(b)
        zero, one, two, tol = fp("0"), fp("1"), fp("2"), fp(tol)
        if b < a:
            a, b = b, a
        x1 = y0 = y1 = y2 = B = C = y10 = y20 = y21 = xm = ym = zero
        xmlast = fp(a)
        if args:
            y0, y2 = ((f(a, *args, **kw), f(b, *args, **kw)) if kw else (f(a, *args), f(b, *args)))
        else:
            y0, y2 = (f(a, **kw), f(b, **kw)) if kw else (f(a), f(b))
        y0, y2 = fp(y0), fp(y2)
        # Check for a zero at the endpoints
        if not y0:
            Dbg(f"{fnname}: a is root", file=dbg)
            return a, 0 
        if not y2:
            Dbg(f"{fnname}: b is root", file=dbg)
            return b, 0
        if y2*y0 > zero:
            msg = f"Root not bracketed: f(a) = {y0}, f(b) = {y2}"
            raise ValueError(msg)
        for i in range(itmax):
            x1 = (b + a)/2  # Bisection step
            Dbg(f"{fnname}:  {fp(x1)}, count = {i + 1}", file=dbg)
            if args:
                y1 = fp(f(x1, *args, **kw) if kw else f(x1, *args))
            else:
                y1 = fp(f(x1, **kw) if kw else f(x1))
            # 13 Oct 2014:  added 'abs(x1 - xmlast) < tol' test because routine was not converging on
            # sqrt(1e108), when it actually only took 5 iterations.
            if not y1 or (abs(x1 - a) < tol) or (abs(x1 - xmlast) < tol):
                Dbg(f"{fnname} done", file=dbg)
                return fp(x1), i + 1
            if y1*y0 > zero:
                a, b, y0, y2 = b, a, y2, y0
            # Attempt inverse quadratic interpolation
            y10, y21, y20 = fp(y1 - y0), fp(y2 - y1), fp(y2 - y0)
            if y2*y20 < two*y1*y10:  # Do another bisection
                b, y2 = x1, y1
            else:  # Inverse quadratic interpolation
                B, C = fp((x1 - a)/y10), fp((y10 - y21)/(y21*y20))
                xm = fp(a - B*y0*(one - C*y1))
                if args:
                    ym = fp(f(xm, *args, **kw) if kw else f(xm, *args))
                else:
                    ym = fp(f(xm, **kw) if kw else f(xm))
                if not ym or abs(xm - xmlast) < tol:
                    Dbg(f"{fnname} done", file=dbg)
                    return fp(xm), i + 1
                xmlast = xm
                if ym*y0 < zero:
                    b, y2 = xm, ym
                else:
                    a, y0, b, y2 = xm, ym, x1, y1
        raise ValueError(f"Number of iterations exceeded {itmax}")
    def Bisection(a, b, f, tol=1e-6, itmax=None, switch=False, fp=float, dbg=None, args=[], kw={}):
        '''Returns (root, num_it) (the root and number of iterations) by finding a root
        of f(x) = 0 by bisection.  The root must be bracketed in [a, b].  Adapted from
        [2:145:154].

        switch      If True, an exception will be raised if the function appears to be
                    increasing during bisection.  Be careful with this, as the
                    polynomial test case converges just fine with bisection, but will
                    cause an exception if switch is True.  It is intended to handle the
                    case where the number being converged on is a singularity.

        itmax       Limit the number of iterations to this value if not None.  Since the
                    number of iterations is N = log2(|a - b|/tol), setting itmax to less
                    than N will lose precision.  
        
        fp          Type of number evaluated by f and the type of the returned root
        
        dbg         If not None, send debugging information to this stream
        
        args        Extra arguments for f (will be evaluated as f(x, *args)
        
        kw          Keyword dictionary for f (will be evaluated as f(x, **kw)
        
        Example
        -------

        The function cos(x) - x can be shown to have a root at 0.739 radians by
        continuously pressing the cos key on a calculator, which finds the root by
        iteration (see Whittaker & Robinson, "The Calculus of Observations", p. 81,
        1924).

            from math import pi, cos
            Bisection(0, pi/2, lambda x: cos(x) - x) --> (0.7390855007577259, 21)

        Method
        ------

        If the root is bracketed and the function is continuous, bisection is guaranteed
        to converge because of the intermediate value theorem.  It may also try to
        converge on a singularity.  

        The method is conceptually simple to understand: draw a line between the two
        bracketing points and look at the midpoint.  Choose the new interval containing
        the midpoint and the other point that evaluates to the opposite sign.  Repeat
        until you find the root to the required accuracy.  Each iteration adds a
        significant digit to the answer and is equivalent to a binary search, which is
        called linear convergence.
        '''
        fnname = "Bisection"
        a, b = [fp(i) for i in (a, b)]
        fa, fb = IsBracketed(a, b, f, fp=fp)
        diff = abs(b - a)
        if not fa:
            Dbg(f"{fnname}: a is root", file=dbg)
            return a, 0
        if not fb:
            Dbg(f"{fnname}: b is root", file=dbg)
            return b, 0
        # Get number of iterations we need to calculate
        n = Ceil(Log2(abs(b - a)/tol, fp), fp)
        if itmax is not None:
            n = itmax
        for count in range(n):
            x = (a + b)/2   # Abscissa of interval midpoint
            Dbg(f"{fnname}:  {fp(x)}, count = {count + 1}", file=dbg)
            y = fp(f(x))    # Ordinate of interval midpoint
            if not y:
                Dbg(f"{fnname} done", file=dbg)
                return x, count + 1
            if switch and abs(y) > abs(fa) and abs(y) > abs(fb):
                msg = "f(x) increasing on interval bisection (i.e., a singularity)"
                raise ValueError(msg)
            # Choose which half-interval to use based on which one continues to
            # bracket the root.
            if fb*y < 0:
                a, fa = x, y  # Right half-interval contains the root
            else:
                b, fb = x, y  # Left half-interval contains the root
        x = fp((a + b)/2)
        Dbg(f"{fnname} done, {x}, count = {count + 1}", file=dbg)
        assert diff/2**n <= tol
        return x, n
    def Ridders(a, b, f, tol=1e-6, itmax=50, fp=float, dbg=None, args=[], kw={}):
        '''Returns (root, num_it), the root and the number of iterations using Ridders'
        method to find a root of f(x) = 0 to the specified tolerance tol.  The
        root must be bracketed on [a, b].  If the number of iterations exceeds itmax, an
        exception will be raised.
        
        Wikipedia states:  Ridders' method is a root-finding algorithm based on the
        false position method and the use of an exponential function to successively
        approximate a root of a function f.
        
        Ridders' method is simpler than Brent's method but Press et. al. (1988) claim
        that it usually performs about as well.  It converges quadratically, which
        implies that the number of additional significant digits doubles at each step;
        but the function has to be evaluated twice for each step so the order of the
        method is 2**(1/2). The method is due to Ridders (1979).
        
        Adapted from [3:358:382].
        '''
        fnname = "Ridders"
        a, b = [fp(i) for i in (a, b)]
        fa, fb = IsBracketed(a, b, f, fp=fp)
        if not fa:
            Dbg(f"{fnname}: a is root", file=dbg)
            return a, 0
        if not fb:
            Dbg(f"{fnname}: b is root", file=dbg)
            return b, 0
        for i in range(itmax):
            # Compute the improved root x from Ridder's formula
            c = (a + b)/2
            Dbg(f"{fnname}:  {fp(c)}, count = {i + 1}", file=dbg)
            fc = fp(f(c))
            sr = (fc*fc - fa*fb)**0.5
            if not sr:
                if not fc:
                    Dbg(f"{fnname} done", file=dbg)
                    return c, i + 1
                raise ValueError("No root")
            dx = (c - a)*fc/sr
            if (fa - fb) < 0:
                dx = -dx
            x = fp(c + dx)
            fx = fp(f(x))
            # Test for convergence.  Note:  a linter will complain that x_old is undefined
            # or assigned and never used, but in fact it works OK because i is 0 the first
            # pass through.
            if i > 0:
                if abs(x - x_old) < tol*max(abs(x), 1):   # noqa
                    Dbg(f"{fnname} done", file=dbg)
                    return x, i + 1
            x_old = x   # noqa
            # Re-bracket the root as tightly as possible
            if fc*fx > 0:
                if fa*fx < 0:
                    b, fb = x, fx
                else:
                    a, fa = x, fx
            else:
                a, b, fa, fb = c, x, fc, fx
        raise ValueError(f"Number of iterations exceeded {itmax}")
    def Brent(a, b, f, tol=1e-6, itmax=50, fp=float, dbg=None, args=[], kw={}):
        '''Return (root, number of iterations) where root is the root of f(x) = 0 by
        combining quadratic interpolation with bisection (simplified Brent's method).
        The root must be bracketed in (a, b).  Calls user-supplied function f(x).  From
        [2:148:157].
        
        The method is defined to converge at x if:
            1.  f(x) < tol
            2.  The interval [a, b] width < tol*max(abs(b), 1)
        '''
        fnname = "Brent"
        a, b = [fp(i) for i in (a, b)]
        fa, fb = IsBracketed(a, b, f, fp=fp)
        x1, x2 = a, b
        if not fa:
            Dbg(f"{fnname}: a is root", file=dbg)
            return a, 0
        if not fb:
            Dbg(f"{fnname}: b is root", file=dbg)
            return b, 0
        f1, f2 = fa, fb     # Renaming for algorithm's notation
        x3 = fp((a + b)/2)  # Midpoint for bisection
        for count in range(itmax):
            f3 = fp(f(x3))
            Dbg(f"{fnname}:  {fp(f3)}, count = {count + 1}", file=dbg)
            if abs(f3) < tol:
                Dbg(f"{fnname} done", file=dbg)
                return x3, count + 1
            # Tighten the brackets on the root
            if f1*f3 < 0:
                b = x3  # New interval is left-hand half
            else:
                a = x3  # New interval is right-hand half
            if (b - a) < tol*max(abs(b), 1):
                Dbg(f"{fnname}:  {fp((a + b)/2)}, count = {count + 1}", file=dbg)
                Dbg(f"{fnname} done", file=dbg)
                return (a + b)/2, count + 1
            # Try quadratic interpolation (Lagrange's 3-point formula)
            numer = fp(x3*(f1 - f2)*(f2 - f3 + f1) + f2*x1*(f2 - f3) + f1*x2*(f3 - f1))
            denom = fp((f2 - f1)*(f3 - f1)*(f2 - f3))
            # If division by zero, push x out of bounds
            x = x3 + (f3*numer/denom if denom else b - a)
            # If interpolation goes out of bounds, use bisection.  This test is equivalent to
            # (a < x < b) if a < b or (b < x < a) if b < a.
            # 13 Oct 2014:  added inf test because was getting nonconvergence for simple
            # test case (sqrt(1e108)) because x was NaN.
            if denom == float("inf") or (b - x)*(x - a) < 0:
                x = a + (b - a)/2
            # Let x3 be x & choose new x1 and x2 so that x1 < x3 < x2
            if x < x3:
                x2, f2 = x3, f3
            else:
                x1, f1 = x3, f3
            x3 = x
        raise ValueError(f"Number of iterations exceeded {itmax}")
if 1:  # Other
    def ITP(a, b, f, tol=1e-6, itmax=50, k1=None, k2=2, n0=1, fp=float):
        '''Return (root, num_iterations) for the root of the function f.

        a       Start of bracketing interval
        b       End of bracketing interval
        f       Function (univariate) to evaluate
        tol     The routine has converged when the last two function values differ by
                less than tol
        itmax   Maximum number of iterations; if exceeded, a ValueError will be raised
        fp      Number type to do the calculations with (float, Decimal, mpmath.mpf
                supported)

        Translation into python of John Burkardt's C routine (see
        https://people.sc.fsu.edu/~jburkardt/f_src/zero_itp/zero_itp.html, last modified
        2 Mar 2024).  All variables are C doubles except nh and nmax, which are integer.
        
        math symbols used:  ceil, log2
        
        Note:
            - ceil can be gotten with ROUND_CEIL
            - pow can be gotten with Decimal.power()
            - log2 can be gotten with ln
            - Thus, this could be written with a Decimal implementation.  It would be
              interesting to do this; fp could be set to Decimal and you'd get this
              impl.  Interesting to see how much slower it is than float.
                - This may give the general pattern for all the rootfinders to let them
                  support float, Decimal, and mpf.
                  
        Constants:
            - k1 is on [0,∞], suggested value 0.2/(b - a)
            - k2 is on [1, 1+ϕ] == [1, 2.618], ϕ = (1 + sqrt(5))/2, suggested value 2
            - n0 on [0,∞] = max number of iterations over bisection.  It can be set to 0
              for difficult problems, but is usually set to 1, to take advantage of the
              secant method.
        
        From https://docs.rs/kurbo/0.8.1/kurbo/common/fn.solve_itp.html
            - ITP paper https://dl.acm.org/doi/10.1145/3423597
                - Oliveira, I. F. D.; Takahashi, R. H. C. (2020-12-06). "An Enhancement
                  of the Bisection Method Average Performance Preserving Minmax
                  Optimality".  ACM Transactions on Mathematical Software.  47 (1):
                  5:1–5:24.  doi:10.1145/3423597. ISSN 0098-3500. S2CID 230586635.
            - The assumption is that ya < 0 and yb > 0, otherwise unexpected results may
              occur
            - a and b must bracket the root and represent the search lower/upper bounds
            - Must have tol > 2**(-63)(b - a), otherwise integer overflow may occur.
              This is probably specific to kurbo, which appears to be a 64-bit floating
              point R implementation
            - kurbo hardwires k2 = 2, both because it avoids a floating point
              exponentiation and the value has been tested to work well with curve
              fitting problems
            - The n0 parameter controls the relative impact of the bisection and secant
              components.  When it is 0, the number of iterations is guaranteed to be no
              more than the number required by bisection (thus, this method is strictly
              superior to bisection). However, when the function is smooth, a value of 1
              gives the secant method more of a chance to engage, so the average number
              of iterations is likely lower, though there can be one more iteration than
              bisection in the worst case.
            - The k1 parameter is harder to characterize, and interested users are
              referred to the paper, as well as encouraged to do empirical testing. To
              match the paper, a value of 0.2/(b-a) is suggested, and this is confirmed
              to give good results.
            - When the function is monotonic, the returned result is guaranteed to be
              within tol of the zero crossing.
              
        Here's the algorithm from https://www.wikiwand.com/en/articles/ITP_Method
            - Given interval [a0, b0], f, ϵ
                - f is the function to find its root
                - f(a0)*f(b0) < 0 (required) (i.e., a0 and b0 bracket the root)
                - ϵ > 0 is the target precision
            - Problem definition:  Find xᵦ such that |xᵦ - q| <= ϵ and f(q) = 0.
            - noh = ln2((b0 - a0)/(2ϵ)) = guaranteed number of iterations to terminate
            - Step 1:  Interpolation [Calculate bisection & regula falsi points]
                - x_b = (a + b)/2
                - x_f = (b*f(a) - a*f(b))/(f(a) - f(b))
            - Step 2:  Truncation [perturb the estimator towards the center]
                - x_t = x_f + σ*ρ where
                    - σ = sign(x_b - x_f)
                    - ρ = min(k1*abs(b - a)**k2, abs(x_b - x_f))
            - Step 3:  Projection [Project the estimator to minmax interval]
                - x_itp = x_b - σ*βₖ where
                    - βₖ = min(ϵ*2**(noh + n0 - j) - (b - a)/2, abs(x_t - x_b))
                - (j not defined, but used in the pseudocode)

        '''
        a, b, tol = fp(a), fp(b), fp(tol)
        if a == b:
            raise ValueError("a and b are equal")
        if b < a:
            a, b = b, a
        if k1 is None:
            k1 = fp("0.2")/(b - a)
        else:
            k1 = fp(k1)
        k2 = fp(k2)
        ya, yb = IsBracketed(a, b, f, fp=fp)
        # Modify f(x) so that y(a) < 0, 0 < y(b);
        if 0 < ya:
            s, ya, yb = -1, -ya, -yb
        else:
            s = 1
        nh = Ceil(Log2((b - a)/(2*tol), fp), fp)
        nmax, count = nh + n0, 0
        while 2*tol < (b - a):
            count += 1
            if count > itmax:
                raise ValueError(f"Number of iterations exceeded {itmax}")
            # Calculate parameters
            xh, r, delta = (a + b)/2, tol*2**(nmax - count) - (b - a)/2, fp(k1*(b - a)**k2)
            # Interpolation
            xf = (yb*a - ya*b)/(yb - ya)
            # Truncation
            sigma = 1 if 0 <= xh - xf else -1
            xt = fp(xf + sigma*delta if delta < abs(xh - xf) else xh)
            # Projection
            xitp = xt if abs(xt - xh) <= r else fp(xh - sigma*r)
            # Update the interval
            yitp = fp(s*f(xitp))
            if 0 < yitp:
                b, yb = xitp, yitp
            elif yitp < 0:
                a, ya = xitp, yitp
            else:
                a, b = xitp, xitp
                break
        return fp((a + b)/2), count
    def NewtonRaphson(x, f, fderiv, tol=1e-6, itmax=50, fp=float):
        '''Returns the root using Newton-Raphson algorithm for solving f(x) = 0.
            f       The function 
            fderiv  f's derivative
            x       Initial guess of the root's location
            tol     Number used to determine when to quit
            itmax   Maximum number of iterations allowed
            fp      Type of numbers to calculate with
            
        The iteration is xnew = x - f(x)/f'(x) until |dx|/(1+|x|) < tol is achieved.
        Here, dx = f(x)/fderiv(x).  This termination condition is a compromise between
        |dx| < tol if x is small and |dx|/|x| < tol if x is large.
        
        - Advantages
            - Simple code and easy to understand what's going on
            - Fast
            - Converges quadratically near the root
        - Disadvantages
            - Near-zero derivatives can send it far from the root
            - Curves with ogive shapes can make it oscillate and not converge
            - You need to have an expression for both the function and its derivative
        
        Adapted from http://www.phys.uu.nl/~haque/computing/WPark_recipes_in_python.html
        (defunct URL as of Sep 2014).
        '''
        count, one, x = 0, fp(1), fp(x)
        while True:
            dx = fp(f(x)/fderiv(x))
            if abs(dx) < tol*(one + abs(x)):
                return x - dx
            x, count = x - dx, count + 1
            if count > itmax:
                raise ValueError(f"Number of iterations exceeded {itmax}")
    def Ostrowski(x, f, fderiv, tol=1e-6, itmax=50, fp=float):
        '''Returns (root, num_iterations) for the root of the function f(x).

        x           Initial guess for the root
        f           The function f(x)
        fderiv      The first derivative of f
        tol         Convergence tolerance
        itmax       Maximum number of iterations
        fp          Floating point type to do calculations with
        
        Ostrowski's method is based on Newton's method with a follow-on evaluation to refine the root:
        
            y_n = x_n - f(x_n)/f'(x_n)
            x_(n+1) = y_n - f(y_n)*(x_n - y_n)/(f(x_n) - 2*f(y_n))
            
        For each iteration step, there are three function evaluations: f(x_n), f'(x_n), and f(y_n).
        
        Reference:  "Ostrowski's Method for Finding Roots" by Namir Shammas in "HP Solve", issue 28,
        July 2012, page 8.
        '''
        xn = fp(x)
        for count in range(itmax):
            ya = fp(f(xn))
            if not ya:
                return (xn, count + 1)
            yn = fp(xn - ya/fderiv(xn))
            yb = fp(f(yn))
            c = ya - 2*yb
            if not c:
                if yb:
                    raise ZeroDivisionError("(ya - 2*yb) is zero")
                else:
                    return (yn, count + 1)
            xn1 = fp(yn - yb*(xn - yn)/c)
            # Check for convergence
            if xn1 == xn:
                return (xn, count + 1)
            diff = abs(xn1 - xn)
            if diff < tol:
                return (xn, count + 1)
            xn = xn1
        raise ValueError(f"Number of iterations exceeded {itmax}")
    def SearchIntervalForRoots(a, b, f, n, fp=float, args=[], kw={}):
        '''Return a tuple of subintervals of [a, b] where f has roots.
        
        a       Start of interval
        b       End of interval
        f       Function whose roots we want
        fp      Floating point type to do calculations with
        args    Extra arguments for f
        kw      Extra keyword arguments for f

        Divide [a, b] into n subintervals and examine each one for a zero crossing.
        Idea from [3:352].
        '''
        if a == b:
            raise ValueError("a and b are equal")
        if n < 1 or not isinstance(n, int):
            raise ValueError("n must be an integer > 0")
        a, b = fp(a), fp(b)
        if a > b:
            raise ValueError("a must be < b")
        if args:
            y0 = fp(f(a, *args, **kw)) if kw else fp(f(a, *args))
        else:
            y0 = fp(f(a, **kw)) if kw else fp(f(a))
        x0, delta, intervals = a, fp((b - a)/(n + fp("1"))), []
        for count in range(1, n + 1):
            x = a + count*delta
            if args:
                y = f(x, *args, **kw) if kw else f(x, *args)
            else:
                y = f(x, **kw) if kw else f(x)
            # See if this interval has a root (check endpoints too)
            if y0*y < 0 or not y0 or not y:
                intervals.append((x0, x))
            x0, y0 = x, y
        return tuple(intervals)
    def FindRoots(f, n, x1, x2, tol=1e-6, itmax=50, fp=float, args=[], kw={}):
        '''This is a general-purpose root finding routine that returns a tuple of the
        roots found of the function f on the interval [x1, x2].
        
        It uses SearchIntervalForRoots to divide the interval into n intervals and look
        for roots in each subinterval.  If a subinterval has a root, the Crenshaw
        routine is used to find the root to precision tol.  If more than itmax
        iterations are used in any interval, an exception is raised.
        
        Parameters
            f       Function to search for roots
            n       Number of subintervals
            x1      Start of overall interval to search
            x2      End of overall interval to search
            tol  Precision to find roots
            itmax   Maximum number of iterations
            fp      Floating point type to use for calculations
            args    Extra parameters for f()
            kw      Extra keyword arguments for f()
            
        Example:  Find the roots of sin(x)/x = 0 on the interval [1, 10]:
            import math
            for i in FindRoots(lambda x: math.sin(x)/x, 1000, 1, 10):
                print(i)
        which prints
            3.141592653589784
            6.283185307179587
            9.424777960769378
        '''
        if not f:
            raise ValueError("f must be defined")
        if not isinstance(n, numbers.Integral):
            raise TypeError("n must be integer")
        if x1 >= x2:
            raise ValueError("Must have x1 < x2")
        intervals = SearchIntervalForRoots(x1, x2, f, n, fp=fp, args=args, kw=kw)
        if not intervals:
            return tuple()
        roots = []
        for x1, x2 in intervals:
            try:
                x, numits = Crenshaw(x1, x2, f, tol=tol, itmax=itmax, args=args, kw=kw)
            except StopIteration:
                pass
            else:
                roots.append(x)
        return tuple(roots)
    def BracketRoots(f, x1, x2, itmax=50, fp=float, args=[], kw={}):
        '''Given a function f and an initial interval [x1, x2], expand the interval
        geometrically until a root is bracketed or the number of iterations exceeds
        itmax.  Return (a, b), where the interval [a, b]  brackets a root.  If the
        maximum number of iterations is exceeded, an exception is raised.
        
        fp      Floating point type to use
        args    Sequence of extra arguments to be passed to f
        kw      Dictionary of keywords that will be passed to f
        
        Adapted from zbrac in [3:352].
        '''
        assert f and x1 != x2
        zero = fp("0")
        if x1 > x2:
            x1, x2 = x2, x1
        if args:
            f1, f2 = (
                (f(x1, *args, **kw), f(x2, *args, **kw))
                if kw
                else (f(x1, *args), f(x2, *args))
            )
        else:
            f1, f2 = (f(x1, **kw), f(x2, **kw)) if kw else (f(x1), f(x2))
        factor, count = fp("1.6"), 0
        while True:
            if f1 * f2 < zero:
                return (x1, x2)
            if abs(f1) < abs(f2):
                x1 += factor * (x1 - x2)
                if args:
                    f1 = f(x1, *args, **kw) if kw else f(x1, *args)
                else:
                    f1 = f(x1, **kw) if kw else f(x1)
            else:
                x2 += factor * (x2 - x1)
                if args:
                    f2 = f(x2, *args, **kw) if kw else f(x2, *args)
                else:
                    f2 = f(x2, **kw) if kw else f(x2)
            count += 1
            if count > itmax:
                raise ValueError(f"Number of iterations exceeded {itmax}")
if 0:  # Crenshaw
    '''
    
    This routine is commented out because it takes too much time.  However, it uses
    Jack's realization that the routine often did better than the user requested,
    shaving one iteration off the computation.
    
    I suspect it's not worth the bookkeeping needed to eliminate the extra step,
    particularly since e.g. Brent() converges quickly and is usually the fastest.
    
    '''
    def CrenshawOld(x1, x3, f, eps=1e-6, itmax=50, p=4, dbgstream=None):
        '''Returns (root, number_of_iterations).
        x1, x3        Initial estimates of the root and must bracket it.
        f             Function f(x) to call to evaluate.
        eps           Relative change used to determine when the algorithm
                      has converged.
        itmax         Maximum number of iterations to use.
        '''
        d = {
            "p": p,
            "xlast": None,
            "ymin": 1e308,
            "ymax": -1e308,
            "eps": eps,
        }
        def Dbg(s, end="\n"):
            if dbgstream:
                for i in s.split("\n"):
                    g.dbgstream.write("+ {0}{1}".format(i, end))
        def F(*args, **kw):
            '''Parameters args:  the first element is x and is mandatory.  The following parameters are
            passed to the function f.  The keyword dictionary must contain a dictionary named opts; it
            is used in this function, the opts key is removed, and the remaining dictionary is passed
            to the function f.
            
            This is a wrapper function that calls f(x) given a dictionary d that contains the following
            keys:
              ymin        Minimum y value encountered
              ymax        Maximum y value encountered
              eps         Desired convergence radius, relative
              converged   Will be True when the current y value is less than
                          eps*(ymax - ymin).
                          
            This is per Jack Crenshaw's follow-up article on 13 Apr 2004 entitled "A root-finding
            algorithm" in "Embedded Systems Development".  Jack's realization was that the original
            algorithm he published in May 2002 ("All Problems Are Simple" in "Embedded Systems
            Programming", pg 7-14) often converged to a value better than requested by the user (I've
            noticed the same behavior).  Jack's insight was to look at successive y values and base
            convergence on getting a y value that was less in absolute value than eps*(ymax - ymin).
            This function, F(x) does the bookkeeping so that a) the minimum and maximum y values are
            remembered and b) the convergence status is returned in a Boolean variable.  You'll find
            this method gets the root to the desired precision and does it in fewer steps than the
            original algorithm.
            
            Note:  Jack has mentioned numerous times that this algorithm was from some unknown genius
            at IBM in the 1960's and was part of their FORTRAN library code.  Jack studied the
            algorithm and wrote articles in "Embedded Systems Development" to popularize it.  The
            method is inverse parabolic interpolation with bisection and it converges quadratically
            (converging quadratically means the error in the current step is the square of the error
            in the previous step).
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
                    return diff / d["xlast"]
                elif x:
                    return diff / x
                else:
                    return 0
            if args:
                y = f(x, *p, **kw) if kw else f(x, *p)
            else:
                y = f(x, **kw) if kw else f(x)
            d["xlast"] = x
            d["ymin"] = ymin = min(y, d["ymin"])
            d["ymax"] = ymax = max(y, d["ymax"])
            Dbg(
                "f(x): x = {x:.{p}g}, y = {y:.{p}g}, Y min/max: "
                "[{ymin:.{p}g}, {ymax:.{p}g}]".format(**locals())
            )
            d["converged"] = abs(y) < d["eps"] * (ymax - ymin) and dx(x) < eps
            return y
        Dbg(
            '''Crenshaw() called with:
            Starting interval = [{x1:.{p}g}, {x3:.{p}g}]
            eps   = {eps}
            itmax = {itmax}'''.format(**locals())
        )
        # Local variables
        x2 = y2 = 0  # Middle point in bisections
        xm = ym = 0  # Estimated root in interpolations
        y1 = y3 = y21 = y31 = y32 = 0
        b = c = 0  # Temporary variables
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
        # If the signs are the same, we were given bad initial values of x1, x3
        if y3 * y1 > 0.0:
            raise ValueError("Root not bracketed")
        for i in range(itmax):
            x2 = (x3 + x1)/2  # Bisection step
            y2 = F(x2, opts=d)
            Dbg("Bisection x2 = {x2:.{p}g}, y2 = {y2:.{p}g}".format(**locals()))
            if not y2 or d["converged"]:
                Dbg("--> Converged to " + str((x2, i + 1)))
                return (x2, i + 1)
            if y2 * y1 > 0:  # Relabel to keep the root between x1 and x2.
                x1, x3, y1, y3 = x3, x1, y3, y1
            # Attempt a parabolic interpolation.
            y21, y32, y31 = y2 - y1, y3 - y2, y3 - y1
            if y3 * y31 < 2 * y2 * y21:
                # Do another bisection
                x3, y3 = x2, y2
                Dbg("Can't use parabolic; x3 now {x3:.{p}g}".format(**locals()))
            else:
                # Parabolic interpolation
                try:
                    # y21 and y31 cannot be zero, but y32 might.
                    b, c = (x2 - x1)/y21, (y21 - y32)/(y32 * y31)
                    xm = x1 - b * y1 * (1 - c * y2)
                    ym = F(xm, opts=d)
                    Dbg("Parabolic xm = {xm:.{p}g}, ym = {ym:.{p}g}".format(**locals()))
                    if not ym or d["converged"]:
                        Dbg("--> Converged to " + str((xm, i + 1)))
                        return (xm, i + 1)
                    # Relabel to keep root between x1 and x2.
                    if ym * y1 < 0:
                        x3, y3 = xm, ym
                    else:
                        x1, y1, x3, y3 = xm, ym, x2, y2
                except ZeroDivisionError:
                    print("Division by zero in Crenshaw:", file=sys.stderr)
                    print("  x1  =", x1, file=sys.stderr)
                    print("  x2  =", x2, file=sys.stderr)
                    print("  y21 =", y21, file=sys.stderr)
                    print("  y31 =", y31, file=sys.stderr)
                    print("  y32 =", y32, file=sys.stderr)
                    # Do another bisection
                    x3, y3 = x2, y2
        raise StopIteration("No convergence in Crenshaw()")
if 1:  # Polynomials
    def Quadratic(a, b, c, adjust=True, force_real=False):
        '''Return the two roots of a quadratic equation.  The equation is a*x**2 + b*x +
        c = 0; where the coefficients can be floats or complex numbers (including
        mpmath's mpf and mpc numbers).  
        
        adjust      Use Pound() to cause roots with small real or imaginary parts to be
                    adjusted to be pure real or imaginary.
        force_real  If true, forces the returned values to be real numbers by returning
                    the real parts.
        
        Here's a derivation of the method used.  Multiply by 4*a and complete the square to get
        
            (2*a*x + b)**2 = (b**2 - 4*a*c)
            x = (-b +/- sqrt(b**2 - 4*a*c))/(2*a)           (1)
            
        Next, multiply the equation by 1/x**2 to get
        
            a + b*(1/x) + c*(1/x**2) = 0
            
        Complete the square to find
        
            1/x = (-b -/+ sqrt(b**2 - 4*a*c))/(2*c)
            
        or
        
            x = 2*c/(-b -/+ sqrt(b**2 - 4*a*c))             (2)
            
        Equations 1 or 2 may provide more accuracy for a particular root.  There can be loss of
        precision in the discriminant when a*c is small compared to b**2.  This happens when the roots
        vary greatly in absolute magnitude.  Suppose they are x1 and x2; then (x - x1)*(x - x2) = x**2
        - (x1 + x2)*x + x1*x2 = 0.  Here,
        
            a = 1
            b = -(x1 + x2)
            c = x1*x2
            
        Suppose x1 = 1000 and x2 = 0.001.  Then b = -1000.001 and c = 1.  The square root of the
        discriminant is 999.999 and the subtraction b - sqrt(D) results in 0.0001, with a loss of
        around 6 significant figures.
        
        The algorithm is to use these two equations depending on the sign of b (D = b**2 - 4*a*c):
        
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
            d = (p*p/4 - q)**0.5
            if force_real:
                return tuple([i.real for i in (-p/2 + d, -p/2 - d)])
            return Pound(-p/2 + d, adjust), Pound(-p/2 - d, adjust)
        else:
            # More stable numerical method
            D = (b*b - 4*a*c)**0.5
            if b >= 0:
                x1, x2 = (-b - D)/(2*a), 2*c/(-b - D)
            else:
                x1, x2 = 2*c/(-b + D), (-b + D)/(2*a)
            if force_real:
                return tuple([i.real for i in (x1, x2)])
            return Pound(x1, adjust), Pound(x2, adjust)
    def Cubic(a, b, c, d, adjust=True, force_real=False):
        '''Returns the roots of a cubic with complex coefficients: a*z**3 + b*z**2 + c*z
        + d.  The coefficients can also be mpmath's mpf and mpc numbers.
        
        adjust      Use Pound() to cause roots with small real or imaginary parts to be
                    adjusted to be pure real or imaginary.
        force_real  If true, forces the returned values to be real numbers by returning
                    the real parts.
        
        Using force_real might be of service when e.g. solving cubic equations of state
        like the Peng-Robinson or Redlich-Kwong equations.  You must exercise caution,
        as you might be throwing a true complex root away.
        
        Example
        -------
            The cubic equation x**3 + x**2 + x + 1 = 0 has the roots -1, i, and -i, as
            can be shown from expanding (x + 1)(x + i)(x - i).

            for i in Cubic(1, 1, 1, 1):
                print(i)
            prints
                -1.0
                (-6.93889390391e-17+1j)
                (-6.93889390391e-17-1j)
            
            for i in Cubic(1, 1, 1, 1, adjust=True):
                print(i)
            prints
                -1.0
                1j
                -1j
            showing how the Pound() function eliminates the small real parts.

            Note
                for i in Cubic(1, 1, 1, 1, force_real=True):
                    print(i)
            prints
                -1.0
                -6.93889390391e-17
                -6.93889390391e-17
            which is probably *not* what you want because it throws important information
            away.

        ----------------------------------------------------------------------

        The following Mathematica commands were used to generate the code for the cubic
        and quartic routines.
        
        (* Cubic *)
          f = a*x**3 + b*x**2 + c*x + d;
          g = Solve[f == 0, x];
          FortranForm[g]
          
        (* Quartic *)
          f = a*x**4 + b*x**3 + c*x**2 + d*x + e;
          g = Solve[f == 0, x];
          FortranForm[g]
          
        The output was edited with the following changes:
        
            1. Change (0,1) to 1j
            2. Remove extra parentheses and comma at end of expression
            3. Substitute 1/3 for 0.3333333333333333
            4. Substitute 2/3 for 0.6666666666666666
            
        After this manipulation, common terms were looked for and set up as single
        variables to avoid recalculation.
        
        The special case where we're finding the third or fourth root of a real or
        complex number, we use De Moivre's theorem:  Let z be a complex number written
        in polar form z = r*(cos(x) + i*sin(x)).  Then
        
          z**(1/n) = r**(1/n)*(cos((x + 2*k*pi)/n) + i*sin((x + 2*k*pi)/n))
          
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
                x = math.atan2(-d.imag, -d.real)
            else:
                x = math.pi if -d < 0 else 0
            def f(x, k):
                return r**(1/3)*(math.cos((x + 2*k*math.pi)/3) + 1j*math.sin((x + 2*k*math.pi)/3))
            roots = f(x, 0), f(x, 1), f(x, 2)
            if force_real:
                return tuple(i.real for i in roots)
            return tuple(Pound(i, adjust) for i in roots)
        u = -2*b**3 + 9*a*b*c - 27*a**2*d
        D = -(b**2) + 3*a*c
        v = (4*D**3 + u**2)**0.5
        w = 2**(1/3)
        y = (u + v)**(1/3)
        st = 1j*3**0.5
        z = -b/(3*a)
        u = 3*2**(2/3)*a*y
        x = 6*w*a
        x1 = z - w*D/(3*a*y) + y/(3*w*a)
        x2 = z + ((1 + st)*D)/u - ((1 - st)*y)/x
        x3 = z + ((1 - st)*D)/u - ((1 + st)*y)/x
        if force_real:
            return tuple(i.real for i in (x1, x2, x3))
        return tuple(Pound(i, adjust) for i in (x1, x2, x3))
    def Quartic(a, b, c, d, e, adjust=True, force_real=False):
        '''Returns the roots of a quartic with complex coefficients: a*x**4 + b*x**3 + c*x**2 + d*x +
        e.  Note this works with float types only.  Set force_real to make all the returned roots be
        real.
        
        You can set force_real to True to make all the returned roots be real (this causes the real
        part of the calculated roots to be returned).  You must exercise caution, as you might be
        throwing a true complex root away.
        
        If adjust is True and a root has an imaginary part small enough relative to the real part, it
        is converted to a real number.  Analogously, if the real parts are small enough relative to the
        imaginary parts, the root is converted to a pure imaginary.
        
        Example 1:
            for i in Quartic(1, 1, 1, 1, 1):
                print(i)
        prints
            (-0.809016994375-0.587785252292j)
            (-0.809016994375+0.587785252292j)
            (0.309016994375-0.951056516295j)
            (0.309016994375+0.951056516295j)
            
        Example 2:  (x-1)*(x-2)*(x-3)*(x-4) is a quartic polynomial with a = 1, b = -10, c = 35, d =
        -50, and e = 24.  Then
            for i in Quartic(1, -10, 35, -50, 24):
                print(i)
        prints
            0.9999999999999992
            2.0000000000000004
            2.9999999999999996
            4.000000000000001
            
        See the docstring for Cubic to find out how the equations were generated.
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
                if -e < 0:
                    x = math.pi
            n = 4
            rn = r**(1/n)
            def f(x, k):
                return rn*(math.cos((x + 2*k*math.pi)/n) + 1j * math.sin((x + 2*k*math.pi)/n))
            roots = f(x, 0), f(x, 1), f(x, 2), f(x, 3)
            if force_real:
                return tuple([i.real for i in roots])
            return tuple([Pound(i, adjust) for i in roots])
        cr3 = 2**(1/3)
        p = -b/(4*a)
        q = c**2 - 3*b*d + 12*a*e
        r = 2*c**3 - 9*b*c*d + 27*a*d**2 + 27*b**2*e - 72*a*c*e
        s = (-4*q**3 + r**2)**0.5
        T = 3*a*(r + s)**(1/3)
        u = (r + s)**(1/3)/(3*cr3*a)
        v = -(b**3/a**3) + (4*b*c)/a**2 - (8*d)/a
        w = (b**2/(4*a**2) - (2*c)/(3*a) + (cr3*q)/T + u)**0.5
        x = b**2/(2*a**2) - (4*c)/(3*a) - (cr3*q)/T - u
        y = (x - v/(4*w))**0.5/2
        z = (x + v/(4*w))**0.5/2
        roots = p - w/2 - y, p - w/2 + y, p + w/2 - z, p + w/2 + z
        if force_real:
            return tuple([i.real for i in roots])
        return tuple(Pound(i, adjust) for i in roots)
if 1:  # Utility
    def Ceil(x, fp):
        'Ceiling function for type fp:  float, flt, mpf, Decimal'
        if fp is float or fp is flt:
            return math.ceil(x)
        elif have_mpmath and fp is mpmath.mpf:
            return mpmath.ceil(x)
        elif fp is decimal.Decimal and x is decimal.Decimal:
            return x.to_integral_exact(rounding=decimal.ROUND_CEILING) 
        else:
            raise TypeError(f"Type {fp} not supported")
    def Log2(x, fp):
        'Base 2 logarithm function for type fp:  float, flt, mpf, Decimal'
        if fp is float or fp is flt:
            return math.log2(x)
        elif have_mpmath and fp is mpmath.mpf:
            return mpmath.log2(x)
        elif fp is decimal.Decimal:
            assert x is decimal.Decimal
            return x.ln(x)/x.ln(2)
        else:
            raise TypeError(f"Type {fp} not supported")
    def IsBracketed(a, b, f, fp=float):
        '''Check that a and b bracket a root of f(x); raise ValueError if not.  Return
        the values (fp(f(a)), fp(f(b))) for convenience and to avoid recalculating them.
        '''
        fa, fb = fp(f(a)), fp(f(b))
        if fa*fb > 0:
            raise ValueError(f"a = {a} and b = {b} do not bracket a root of f")
        return (fa, fb)
    def Pound(z, adjust=True, ratio=2.5e-15):
        '''Turn z into a real if z.imag is small enough relative to the z.real and
        adjust is True.  Do the analogous thing for a nearly pure imaginary number.
        
        The name comes from imagining the complex number is a nail which a light tap
        from a hammer makes it lie parallel to either the real or imaginary axis.
        
        Set adjust to False so that only pure real or imaginary numbers are converted.
        
        Examples
            Pound(-6.9e-17+1j) --> 1j
            Pound(1-6.9e-17j) --> 1.0
            Pound(-6.9e-17+1j, ratio=1e-20) --> (-6.9e-17+1j)
            Pound(-6.9e-14+1j) --> (-6.9e-14+1j)
        '''
        if not isinstance(z, complex):
            if have_mpmath and not isinstance(z, mpmath.mpc):
                return z
            else:
                return z
        if z.real and not z.imag:
            return z.real
        elif not z.real and z.imag:
            return 1j*z.imag
        # Adjust if the z.real/z.imag or z.imag/z.real ratio is small enough, otherwise
        # return z unchanged
        if adjust and z.real and abs(z.imag/z.real) <= ratio:
            return z.real
        elif adjust and z.imag and abs(z.real/z.imag) <= ratio:
            return 1j*z.imag
        else:
            return z
    def Dbg(*p, **kw):
        'Used to print colorized debugging information to stream'
        file = kw.get("file", None)
        if file is None:
            return
        # file must be a suitable stream
        print(f"{t.dbg}", end="", file=file)
        print(*p, **kw)
        print(f"{t.n}", end="", file=file)
if 1:  # Demo code
    def Check():
        '''This function runs each routine to find the solution of f(x) = 0 where the
        function f(x) is cos(x) - x.  If it completes without an exception, this shows
        the routines got the same numerical value.  It's not intended to be the unit
        test code (see test/root_test.py for that), but rather to be a tool to detect
        when accidental changes have occurred to this file.
        '''
        def myfunc(x):
            return x - math.cos(x)
        tol = 1e-16
        x0, x1 = 0, math.pi/2
        methods = (
            (Bisection, "Bisection"), 
            (Crenshaw, "Crenshaw"),
            (Ridders, "Ridders"),
            (Brent, "Brent"),
            (ITP, "ITP"),
        )
        expected = "0.739085133215161"
        for func, name in methods:
            x, m = func(x0, x1, myfunc, tol=tol)
            Assert(f"{x:.15f}" == expected)
        # FindRoots has a different calling pattern and it returns a tuple of roots
        # found
        x = FindRoots(myfunc, 10, x0, x1, tol=tol)
        Assert(f"{x[0]:.15f}" == expected)
    def MpmathCheck():
        'This checks that mpmath numbers can be used with the routines'
        def myfunc(x):
            return x - math.cos(x)
        tol = mpmath.mpf("1e-16")
        methods = (
            (Bisection, "Bisection"), 
            (Crenshaw, "Crenshaw"),
            (Ridders, "Ridders"),
            (Brent, "Brent"),
            (ITP, "ITP"),
        )
        expected = mpmath.mpf("0.739085133215161")
        for func, name in methods:
            a, b = mpmath.mpf(0), mpmath.pi
            x, m = func(a, b, myfunc, tol=tol)
            Assert(abs(x - expected) < 1e-15)
        # FindRoots has a different calling pattern and it returns a tuple of roots found
        x = FindRoots(myfunc, 10, a, b, tol=tol)[0]
        Assert(abs(x - expected) < 1e-15)
        if 1:   # Prints out a comparison of float/mpf for polynomial routines
            from mpmath import mpf, mpc, mp
            from color import t
            t.print(f"{t.whtl}Demo that Quadratic, Cubic, Quartic work for mpmath numbers")
            a, b, c, d, e = 1, 1, 1, 1, 1
            mp.dps = 16
            A, B, C, D, E = mpf(1), mpf(1), mpf(1), mpf(1), mpf(1)
            if 1:
                t.print(f"{t.ornl}Quadratic")
                for i in Quadratic(a, b, c):
                    print(i)
                print(f"{t.lill}", end="")
                for i in Quadratic(A, B, C):
                    print(i)
                t.print()
            if 1:
                t.print(f"{t.ornl}Cubic")
                for i in Cubic(a, b, c, d):
                    print(i)
                print(f"{t.lill}", end="")
                for i in Cubic(A, B, C, D):
                    print(i)
                t.print()
            if 1:
                t.print(f"{t.ornl}Quartic")
                for i in Quartic(a, b, c, d, e):
                    print(i)
                print(f"{t.lill}", end="")
                for i in Quartic(A, B, C, D, E):
                    print(i)
                t.print()
    def Demo():
        if 0:
            MpmathCheck()
        Check()
        print(dedent('''
        Print out the results of calculating the root to cos(x) - x = 0; both the number of 
        iterations and timing are printed.
        '''))
        tm = Timer()
        tm.u = 1e6  # Set timer's units to μs
        x0, x1 = 0, math.pi/2
        tol, n, fmt, tfmt, ind = 1e-16, 1000, ".15f", ".2g", " "*4
        def myfunc(x):
            return x - math.cos(x)
        print(f"{ind}Relative error = {tol}, number of evaluations for timing = {n}")
        for func, name, fp, nfp in (
                (Bisection, "Bisection", float, "float"), 
                (Crenshaw, "Crenshaw", float, "float"),
                (Crenshaw, "Crenshaw", mpmath.mpf, "mpf"),
                (Ridders, "Ridders", float, "float"),
                (Brent, "Brent", float, "float"),
                (ITP, "ITP", float, "float"),
                ):
            count = 0
            tm.start
            for i in range(n):
                x, m = func(x0, x1, myfunc, tol=tol, fp=fp)
                count += m
            tm.stop
            print(f"{ind}{name:10s}:  Got {float(x):{fmt}} in {count//n:3d} steps, {tm.et/n:{tfmt}} μs {fp}")
        # FindRoots uses a different syntax
        tm.start
        for i in range(n):
            x = FindRoots(myfunc, 10, x0, x1, tol=tol)
        tm.stop
        print(f"{ind}FindRoots :  Got {x[0]:{fmt}} in  ?  steps, {tm.et/n:{tfmt}} μs")

if __name__ == "__main__":
    Demo()
