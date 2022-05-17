'''
Estimate number of significant figures in numbers
    SigFig()
        Returns the number of signifcant figures in an integer, float,
        flt, cpx, Fraction, decimal.Decimal, mpmath.mpf.
    SigFigFloat() 
        Returns the number of significant figures in a float.
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
    # <programming> Estimate number of significant figures in a number
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Standard imports
    from fractions import Fraction
    from decimal import Decimal, getcontext
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt, cpx
    try:
        import mpmath
        _have_mpmath = True
    except ImportError:
        _have_mpmath = false
if 1:   # Global variables
    ii = isinstance
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
        return getcontext().prec
    elif _have_mpmath and ii(x, mpmath.mpf):
        return mpmath.mp.dps
    else:
        raise TypeError("Type of x not supported")
def SigFigFloat(x, strict=False, maxsigfig=16):
    '''Return the estimated number of significant figures in the
    float x.  If x is an integer, it will be changed to a float if
    strict is not True.  Also works on a flt, but uses the actual float
    value, not the n attribute.
 
    Trailing zero digits are removed and are not considered significant.  
    '''
    ## Algorithm:  Change the float x to a significand with maxsigfig
    ## digits.  Remove trailing zeros to find the number of significant
    ## figures in the number; this assumes trailing zeros are not
    ## significant.  Secondly, remove the last digit and then remove all
    ## 9's or all 0's, rounding appropriately.
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
        # Works with a flt
        x = flt(1.234)
        Assert(f(x) == 4)
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
        ctx = getcontext()
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
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
