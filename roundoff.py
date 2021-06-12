'''
The function RoundOff() allows for rounding off floating point values so
that printed forms are easier to read.  Examples:
        745.6998719999999               --> 745.699872
        4046.8726100000003              --> 4046.87261
        0.0254*12 = 0.30479999999999996 --> 0.3048

The function SigFig() returns the number of significant figures in the
argument as long as it can be converted to a float.  Trailing zeros are 
not significant.  Only works up to 12 significant figures.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2015 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Round off floating point values.  By default, floats
    # are rounded to 12 figures.  This means numbers like 0.0254*12 =
    # 0.30479999999999996 will become 0.3048, which is easier to read.
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import sys
    import re
    from decimal import Decimal, localcontext
    from fractions import Fraction
    from pdb import set_trace as xx
if 1:   # Custom imports
    try:
        from uncertainties import ufloat, UFloat
        _have_unc = True
    except ImportError:
        _have_unc = False
    try:
        import mpmath
        _have_mpmath = True
    except ImportError:
        _have_mpmath = False
if 1:   # Global variables
    __all__ = [
        "RoundOff",
    ]
def RoundOff(number, digits=12, convert=False):
    '''Round the significand of number to the indicated number of digits
    and return the rounded number (integers and Fractions are returned
    untransformed).  number can be an int, float, Decimal, Fraction or
    complex number.
 
    If you have the mpmath library, mpf and mpc types can be rounded.
    If you have the uncertainties library, UFloats can be passed in, but
    they will be returned unchanged.
    
    Rounding can get rid of trailing 0's and 9's:
            745.6998719999999               --> 745.699872
            4046.8726100000003              --> 4046.87261
            0.0254*12 = 0.30479999999999996 --> 0.3048
    so that printing the floating point representation is easier to read.
 
    If convert is True, then use float() to convert number to a floating
    point form.
 
    The digits keyword can be any integer greater than zero.  Arbitrary
    precisions with Decimal and mpmath mpf and mpc numbers are supported.
 
    The digits keyword defaults to 12 digits.  This is deliberate
    because few practical problems need more digits if they're based on
    physical measurements (mathematical calculations are the exception
    where numerical accuracy may need to be assessed).  12 was chosen
    because it gives proper rounding in a number of practical test cases
    where 13 doesn't.  For example,
        x = math.pi/6
        math.sin(x) = 0.49999999999999994
        RoundOff(math.sin(x)) = 0.5
    '''
    if isinstance(number, (int, Fraction)):
        return number
    if _have_unc and isinstance(number, UFloat):
        return number
    if isinstance(number, complex):
        re = RoundOff(number.real, digits=digits)
        im = RoundOff(number.imag, digits=digits)
        return type(number)(re, im) # Handles classes derived from complex
    can_convert = False
    if convert and not isinstance(number, Decimal):
        try:
            float(number)
            can_convert = True
        except ValueError:
            pass
    if isinstance(number, float) or (convert and can_convert):
        # Convert to a decimal, then back to a float
        x = Decimal(number)
        with localcontext() as ctx:
            ctx.prec = digits
            x = +x
        return type(number)(x)  # Handles classes derived from floats
    elif isinstance(number, complex):
        return type(number)(
            RoundOff(number.real, digits=digits, convert=True),
            RoundOff(number.imag, digits=digits, convert=True)
            )
    elif isinstance(number, Decimal):
        with localcontext() as ctx:
            ctx.prec = digits
            number = +number
            return number
    elif _have_mpmath and isinstance(number, mpmath.mpf):
        x = Decimal(mpmath.nstr(number, mpmath.mp.dps))
        with localcontext() as ctx:
            ctx.prec = digits
            x = +x
            s = str(x)
            return mpmath.mpf(s)
    elif _have_mpmath and isinstance(number, mpmath.mpc):
        re = Decimal(mpmath.nstr(number.real, mpmath.mp.dps))
        im = Decimal(mpmath.nstr(number.imag, mpmath.mp.dps))
        old_dps = mpmath.mp.dps
        with localcontext() as ctx:
            ctx.prec = digits
            re = +re
            im = +im
            sre, sim = str(re), str(im)
            with mpmath.workdps(digits):
                z = mpmath.mpc(sre, sim)
                return z
    else:
        raise TypeError("Unrecognized floating point type")
def SigFig(x):
    '''Return the number of significant figures in the float x (x must
    be anything that can be converted to a float).  This is done by
    rounding to 12 figures, the default for RoundOff().  Note you won't
    get more than 12 figures, even if the number has them.
 
    Note that trailing '0' digits are removed, so a number like 30000
    will have 1 significant figure, as will 30000.00.
    '''
    radix = ".,"
    def RemoveTrailingZeroes(s):
        while s[-1] == "0" and s[-1] not in radix:
            s = s[:-1]
        return s
    def RemoveRadix(s):
        for i in radix:
            s = s.replace(i, "")
        return s
    y = RoundOff(float(x))
    s = str(y)
    if "e" in s:
        s = s.split("e")[0]
    s = RemoveRadix(s)
    s = RemoveTrailingZeroes(s)
    return len(s)
if __name__ == "__main__":
    from math import pi
    from lwtest import run, raises, assert_equal, Assert
    def Test_RoundOff():
        Assert(RoundOff(745.6998719999999) == 745.699872)
        Assert(RoundOff(745.6998719999999, 5) == 745.70)
        Assert(RoundOff(745.6998719999999, 4) == 745.7)
        Assert(RoundOff(745.6998719999999, 3) == 746)
        Assert(RoundOff(745.6998719999999, 2) == 750)
        Assert(RoundOff(745.6998719999999, 1) == 700)
        Assert(RoundOff(4046.8726100000003) == 4046.87261)
        Assert(RoundOff(-0.30479999999999996) == -0.3048)
    def Test_SigFig():
        x = pi*1e8
        for n in range(1, 14):
            y = RoundOff(x, n)
            Assert(SigFig(y) == min(n, 12))
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals(), halt=True)[0])
    else:
        print("Examples of RoundOff() and SigFig() use:")
        for i in (745.6998719999999, 4046.8726100000003, -0.0254*12):
            print("  RoundOff({}) = {}".format(i, RoundOff(i)))
        x = pi*1e8
        print("pi*1e8 rounded to indicated number of digits:")
        for i in range(1, 15):
            y = RoundOff(x, digits=i)
            print("  {:2d} {} [sigfig = {}]".format(i, y, SigFig(y)))
