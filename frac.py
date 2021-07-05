'''
Find a rational approximation to a real number

    RationalApprox()
        Uses a method of the fractions module and handles integers,
        floats, flt, Fraction, decimal.Decimal, and mpmath.mpf types.

    RationalCF()
        Uses a continued fraction representation based on some C code by
        B. Epstein.  You need to pass it the maximum denominator.

    SigFigFloat() 
        Returns the number of significant figures in a float.

    SigFig()
        Returns the number of signifcant figures in an integer, float,
        flt, cpx, Fraction, decimal.Decimal

'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Find a rational approximation to a real number
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import math
    import os
    import pathlib
    import sys
    from fractions import Fraction
    import decimal
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt, cpx
    from decorators import TraceExecution
    try:
        import mpmath
        _have_mpmath = True
    except ImportError:
        _have_mpmath = false
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    Decimal = decimal.Decimal
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(d, status=1):
        name = sys.argv[0]
        print(dedent(f'''
        Usage:  {name} [options] etc.
        Explanations...
    
        Options:
            -h
                Print a manpage.
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False
        d["-d"] = 3         # Number of significant digits
        if len(sys.argv) < 2:
            Usage(d)
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ad:h")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("a"):
                d[o] = not d[o]
            elif o in ("-d",):
                try:
                    d["-d"] = int(a)
                    if not (1 <= d["-d"] <= 15):
                        raise ValueError()
                except ValueError:
                    msg = ("-d option's argument must be an integer between "
                        "1 and 15")
                    Error(msg)
            elif o in ("-h", "--help"):
                Usage(d, status=0)
        return args
if 1:   # Core functionality
    def SigFigFloat(x, strict=False, maxsigfig=16):
        '''Return the estimated number of significant figures in the
        float x.  If x is an integer, it will be changed to a float if
        strict is not True.
        '''
        '''
        Algorithm:  Change the float x to a significand with maxsigfig
        digits.  Remove trailing zeros to find the number of significant
        figures in the number; this assumes trailing zeros are not
        significant.  Secondly, remove the last digit and then remove
        all 9's or all 0's, rounding appropriately.
        '''
        def RemoveTrailingDigit(i, digit="0"):
            assert(ii(i, int) and i >= 0)
            s = str(i)
            while s and s[-1] == digit:
                s = s[:-1]
            return int(s)
        def CheckLimits(n):
            if not (1 <= n <= maxsigfig):
                raise ValueError(f"n = {n} is improper")
        if not ii(x, float) and strict:
            raise TypeError("x must be a float")
        if not x:
            return 1
        y = float(x) if ii(x, int) else x
        Len = lambda x:  len(str(x))
        # Turn significand into an integer
        s = int(f"{abs(y):.{maxsigfig}e}".split("e")[0].replace(".", ""))
        ns = Len(s)
        t = RemoveTrailingDigit(s)  # Remove zeros
        nt = Len(t)
        if ns != nt:
            CheckLimits(nt)
            return nt
        # See if it rounds by removing the last digit
        assert(Len(s) > 1)
        t = int(str(s)[:-1])
        u = RemoveTrailingDigit(t)
        nu, nt = Len(u), Len(t)
        if nu != nt:
            CheckLimits(nu)
            return nu
        u = RemoveTrailingDigit(t, "9")
        nu = Len(u)
        if nu != nt:
            v = RemoveTrailingDigit(t + 1)
            nv = Len(v)
            CheckLimits(nv)
            return Len(v)
        # It's full precision
        CheckLimits(ns)
        return ns
    def SigFig(x, rtz=False):
        '''Return the number of significant figures in the number x.  If
        rtz is zero, then integers are processed by first removing trailing
        zero digits.  Note this means all trailing zeros are significant
        or none are.
        '''
        if not x:
            return 1
        if ii(x, (flt, cpx)):
            return x.n
        elif ii(x, float):
            return SigFigFloat(x)
        elif ii(x, int):
            s = str(abs(x))
            if rtz:
                while s[-1] == "0":
                    s = s[:-1]
            return len(s)
        elif ii(x, Fraction):
            return len(str(abs(x.denominator)))
        elif ii(x, Decimal):
            return decimal.getcontext().prec
        elif _have_mpmath and ii(x, mpmath.mpf):
            return mpmath.mp.dps
        else:
            raise TypeError("Type of x not supported")
    def RationalApprox(x, reltol=None, check=True):
        '''Returns a fractions.Fraction that is equal to or less than
        the given relative tolerance of x.  If reltol is None, then the
        relative tolerance is given by the (estimated) number of
        significant figures of x.
  
        The algorithm uses the limit_denominator() method of a
        fractions.Fraction instance.
        '''
        if ii(x, int):
            return Fraction(x, 1)
        elif ii(x, Fraction):
            return x
        if not x:
            return Fraction(0, 1)
        if reltol is not None and not (0 < reltol <= 1):
            raise ValueError(f"reltol must be > 0 and <= 1")
        S = [flt, float, int, Fraction]
        S += [mpmath.mpf] if _have_mpmath else []
        if not ii(x, tuple(S)):
            raise TypeError("Type of x not supported")
        X = Decimal(str(x))
        max_denom = int(1/reltol) if reltol else int(10**SigFig(x)) 
        f = Fraction(0, 1).from_decimal(X)
        result = f.limit_denominator(max_denominator=max_denom)
        if check and reltol:
            y = Decimal(result.numerator)/Decimal(result.denominator)
            if not (abs((y - X)/X) <= reltol):
                raise ValueError("Relative tolerance incorrect")
        return result
    def RationalCF(x, max_denom):
        '''Return a Fraction which represents float x the best with the
        indicated maximum denominator.  The algorithm is based on a
        continued fraction expansion.
        '''
        # Based on the following C code by D. Eppstein
        '''
        // From https://www.ics.uci.edu/~eppstein/numth/frap.c
        // Downloaded Mon 05 Jul 2021 07:48:55 AM
        /*
        ** find rational approximation to given real number
        ** David Eppstein / UC Irvine / 8 Aug 1993
        **
        ** With corrections from Arno Formella, May 2008
        **
        ** usage: a.out r d
        **   r is real number to approx
        **   d is the maximum denominator allowed
        **
        ** based on the theory of continued fractions
        ** if x = a1 + 1/(a2 + 1/(a3 + 1/(a4 + ...)))
        ** then best approximation is found by truncating this series
        ** (with some adjustments in the last term).
        **
        ** Note the fraction can be recovered as the first column of the matrix
        **  ( a1 1 ) ( a2 1 ) ( a3 1 ) ...
        **  ( 1  0 ) ( 1  0 ) ( 1  0 )
        ** Instead of keeping the sequence of continued fraction terms,
        ** we just keep the last partial product of these matrices.
        */
        #include <stdio.h>
        main(ac, av)
        int ac;
        char ** av;
        {
            double atof();
            int atoi();
            void exit();
            long m[2][2];
            double x, startx;
            long maxden;
            long ai;
            /* read command line arguments */
            if (ac != 3) {
            fprintf(stderr, "usage: %s r d\n",av[0]);  // AF: argument missing
            exit(1);
            }
            startx = x = atof(av[1]);
            maxden = atoi(av[2]);
            /* initialize matrix */
            m[0][0] = m[1][1] = 1;
            m[0][1] = m[1][0] = 0;
            /* loop finding terms until denom gets too big */
            while (m[1][0] *  ( ai = (long)x ) + m[1][1] <= maxden) {
            long t;
            t = m[0][0] * ai + m[0][1];
            m[0][1] = m[0][0];
            m[0][0] = t;
            t = m[1][0] * ai + m[1][1];
            m[1][1] = m[1][0];
            m[1][0] = t;
                if(x==(double)ai) break;     // AF: division by zero
            x = 1/(x - (double) ai);
                if(x>(double)0x7FFFFFFF) break;  // AF: representation failure
            } 
            /* now remaining x is between 0 and 1/ai */
            /* approx as either 0 or 1/m where m is max that will fit in maxden */
            /* first try zero */
            printf("%ld/%ld, error = %e\n", m[0][0], m[1][0],
            startx - ((double) m[0][0] / (double) m[1][0]));
            /* now try other possibility */
            ai = (maxden - m[1][1]) / m[1][0];
            m[0][0] = m[0][0] * ai + m[0][1];
            m[1][0] = m[1][0] * ai + m[1][1];
            printf("%ld/%ld, error = %e\n", m[0][0], m[1][0],
            startx - ((double) m[0][0] / (double) m[1][0]));
        }
        '''
        if not ii(x, (float, flt)):
            raise TypeError("x must be a float or flt")
        if not ii(max_denom, int) and max_denom < 1:
            raise TypeError("max_denom must be an integer > 0")
        if x == 0:
            return Fraction(0, 1)
        m00, m01 = 1, 0     # Initialize the matrix
        m10, m11 = 0, 1
        y, sign = abs(x), -1 if x < 0 else 1
        ai = int(y)
        while (m10*ai + m11) <= max_denom: # Loop until denom gets too big
            # Multiply these matrices:
            #    (m00 m01) and (ai 1)
            #    (m10 m11)     (1  0)
            tmp = m00*ai + m01
            m01, m00 = m00, tmp
            tmp = m10*ai + m11
            m11, m10 = m10, tmp
            if y == float(ai):
                break
            y = 1/(y - ai)
            ai = int(y)
        # Remaining y is between 0 and 1/ai.  Approximate as either 0 or 1/m
        # where m is max that will fit in max_denom.
        # First try zero
        n1 = m00
        d1 = m10
        err1 = x - n1/d1
        # Try the other possibility
        ai = int((max_denom - m11)/m10)
        n2 = m00*ai + m01
        d2 = m10*ai + m11
        err2 = x - n2/d2
        if abs(err1) <= abs(err2):
            return Fraction(sign*n1, d1)
        else:
            return Fraction(sign*n2, d2)
if __name__ == "__main__":
    from wrap import dedent
    from lwtest import run, raises, assert_equal, Assert
    def Test_SigFigFloat():
        x, f = 0, SigFigFloat
        with raises(TypeError):
            f(0, strict=True)
        Assert(f(0, strict=False) == 1)
        Assert(f(0.0) == 1)
        # Simple truncation
        t = 1.111111111111111
        for i in range(1, 15):
            x = round(t, i)    
            Assert(f(x) == i + 1)
        # Where digits need to be removed.  Note these tests depend on
        # the value of the maxsigfig keyword parameter.
        for i in range(1, 10):
            x = float("123.4599999999999" + str(i))
            Assert(f(x) == 5)
            x = float("123.4500000000000" + str(i))
            Assert(f(x) == 5)
        # Integers
        for x, n in ((1, 1), (10, 1), (11, 2), (10000, 1), (10001, 5)):
            Assert(f(x, strict=False) == n)
    def Test_SigFig():
        # flt
        f = SigFig
        x = flt(1)
        for i in range(1, 15):
            x.n = i
            Assert(f(x) == i)
        x.n = 3
        # float (no testing needed, as it's delegated to SigFigFloat)
        # int
        for x in (0, 1, 10, 100, 1000, 10000, 100000, 1000000):
            Assert(f(x, rtz=False) == len(str(x)))
            Assert(f(-x, rtz=False) == len(str(x)))
            Assert(f(x, rtz=True) == 1)
            Assert(f(-x, rtz=True) == 1)
        for x in (8, 88, 888, 8888, 88888, 888888, 8888888):
            Assert(f(x, rtz=False) == len(str(x)))
            Assert(f(-x, rtz=False) == len(str(x)))
            Assert(f(x, rtz=True) == len(str(x)))
            Assert(f(-x, rtz=True) == len(str(x)))
        # Fraction
        for x in (1, 10, 100, 1000, 10000, 100000, 1000000):
            Assert(f(Fraction(1, x)) == len(str(x)))
        # Decimal
        ctx = decimal.getcontext()
        for i in range(1, 100):
            ctx.prec = i
            x = Decimal(1)
            Assert(f(x) == i)
        # mpf
        if _have_mpmath:
            for i in range(1, 100):
                x = mpmath.mpf(1)
                mpmath.mp.dps = i
                Assert(f(x) == i)
    def Test_RationalApprox():
        f, pi = RationalApprox, math.pi
        # Simple forms
        Assert(f(0) == Fraction(0, 1))
        Assert(f(0.0) == Fraction(0, 1))
        Assert(f(flt(0.0)) == Fraction(0, 1))
        Assert(f(0.000000) == Fraction(0, 1))
        Assert(f(1) == Fraction(1, 1))
        Assert(f(1.0) == Fraction(1, 1))
        Assert(f(flt(1.0)) == Fraction(1, 1))
        Assert(f(1.000000) == Fraction(1, 1))
        Assert(f(-1) == Fraction(-1, 1))
        Assert(f(-1.0) == Fraction(-1, 1))
        Assert(f(flt(-1.0)) == Fraction(-1, 1))
        Assert(f(-1.000000) == Fraction(-1, 1))
        # Use reltol
        for r, p in (
                (1, (3, 1)),
                (0.5, (3, 1)),
                (0.1, (22, 7)),
                (0.01, (311, 99)),
                (0.009, (333, 106)),
                (0.001, (355, 113)),
                (7e-5, (355, 113)),
                (6e-5, (52163, 16604)),
                (5e-5, (62813, 19994)),
                (4e-5, (78433, 24966)),
                (2e-5, (104348, 33215)),
                (1e-5, (312689, 99532)),
                (1e-6, (3126535, 995207)),
                (1e-10, (28558622536, 9090491889)),
                (1e-14, (310742154100396, 98912299704203)),
            ):
            Assert(f(pi, reltol=r) == Fraction(*p))
        # Use significant figures
        for i, expected in (
                (1, Fraction(31, 10)),
                (2, Fraction(157, 50)),
                (3, Fraction(1571, 500)),
                (4, Fraction(3927, 1250)),
                (5, Fraction(314159, 100000)),
                (6, Fraction(3141593, 1000000)),
                (7, Fraction(31415927, 10000000)),
                (8, Fraction(62831853, 20000000)),
                (9, Fraction(1570796327, 500000000)),
                (10, Fraction(3926990817, 1250000000)),
                (11, Fraction(314159265359, 100000000000)),
                (12, Fraction(314159265359, 100000000000)),
                (13, Fraction(15707963267949, 5000000000000)),
                (14, Fraction(314159265358979, 100000000000000)),
            ):
            t = f(round(pi, i))
            Assert(t == expected)
            t = f(round(-pi, i))
            Assert(t == -expected)
    def Test_RationalCF():
        f, pi = RationalCF, math.pi
        for r, p in (
                (1, (3, 1)),
                (0.5, (3, 1)),
                (0.1, (22, 7)),
                (0.01, (311, 99)),
                (0.009, (333, 106)),
                (0.001, (355, 113)),
                (7e-5, (355, 113)),
                (6e-5, (52163, 16604)),
                (5e-5, (62813, 19994)),
                (4e-5, (78433, 24966)),
                (2e-5, (104348, 33215)),
                (1e-5, (312689, 99532)),
                (1e-6, (3126535, 995207)),
                (1e-10, (19870569874, 6324998835)),         # **
                (1e-14, (130161051938194, 41431549628009)), # **
                # ** better (smaller denom) approximation than RationalApprox
            ):
            g = f(pi, max_denom=p[1])
            Assert(f(pi, max_denom=p[1]) == Fraction(*p))
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
