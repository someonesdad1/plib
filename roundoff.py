'''
Roundoff()
    Rounds off floating point values so that printed forms are easier to
    read.  Examples:
        745.6998719999999               --> 745.699872
        4046.8726100000003              --> 4046.87261
        0.0254*12 = 0.30479999999999996 --> 0.3048
 
TemplateRound()
    Used to round a number to a template.  Examples:
        TemplateRound(123.48, 0.1, up=True)  --> 123.5
        TemplateRound(123.48, 0.1, up=False) --> 123.4
    You can think of this example as "round $123.48 to the nearest dime".
 
SigFig()
    Returns the number of significant figures in the argument as long as it
    can be converted to a float.  Trailing zeros are not significant.  Only
    works up to 12 significant figures.
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
    ii = isinstance
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
    if ii(number, (int, Fraction)):
        return number
    if _have_unc and ii(number, UFloat):
        return number
    if ii(number, complex):
        re = RoundOff(number.real, digits=digits)
        im = RoundOff(number.imag, digits=digits)
        return type(number)(re, im)     # Handles classes derived from complex
    can_convert = False
    if convert and not ii(number, Decimal):
        try:
            float(number)
            can_convert = True
        except ValueError:
            pass
    if ii(number, float) or (convert and can_convert):
        # Convert to a decimal, then back to a float
        x = Decimal(number)
        with localcontext() as ctx:
            ctx.prec = digits
            x = +x
        return type(number)(x)  # Handles classes derived from floats
    elif ii(number, complex):
        return type(number)(
            RoundOff(number.real, digits=digits, convert=True),
            RoundOff(number.imag, digits=digits, convert=True)
            )
    elif ii(number, Decimal):
        with localcontext() as ctx:
            ctx.prec = digits
            number = +number
            return number
    elif _have_mpmath and ii(number, mpmath.mpf):
        x = Decimal(mpmath.nstr(number, mpmath.mp.dps))
        with localcontext() as ctx:
            ctx.prec = digits
            x = +x
            s = str(x)
            return mpmath.mpf(s)
    elif _have_mpmath and ii(number, mpmath.mpc):
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
def SigFig(x, clamp=True):
    '''Return the number of significant figures in the float x (x must
    be anything that can be converted to a float).  This is done by
    rounding to 12 figures, the default for RoundOff().  Note you won't
    get more than 12 figures, even if the number has them.  The reason for
    this is that essentially no practical measured data ever has 12
    figures.  If you do want more than 12, set clamp to False.
 
    Note that trailing '0' digits are removed, so a number like 30000
    will have 1 significant figure, as will 30000.00.  If you're
    chronologically-gifted, you may have been taught that '30000.00' has
    seven significant figures.  Today, I recommend you use the notation
    '3.000000e4' instead to denote this.
    '''
    if x == 0:
        return 1
    radix = ".,"
    def RemoveTrailingZeroes(s):
        while s[-1] == "0":
            s = s[:-1]
        return s
    def RemoveRadix(s):
        for i in radix:
            s = s.replace(i, "")
        return s
    y = RoundOff(float(x))
    # Algorithm is to convert to scientific notation, parse out the
    # significand, remove the radix, and counts its digits.
    s = f"{y:.12e}"
    m, e = s.split("e")
    t = str(float(m))
    t = RemoveRadix(t)
    t = RemoveTrailingZeroes(t)
    return len(t)
def TemplateRound(x, template, up=True):
    '''Round a number x to a template number.  The basic algorithm is to
    determine how many template values are in x.  You can choose to
    round up (the default) or down.  This should work with x and template
    being any numerical types with floating point semantics.  The absolute
    value of template is used.
 
    The algorithm is derive from pg 435 of the 31 Oct 1988 issue of "PC
    Magazine" written in BASIC:
        DEF FNRound(Amount, Template) =
            SGN(Amount)*INT(0.5 + ABS(Amount)/Template)*Template
    '''
    if not template:
        raise ValueError("template must not be zero")
    if not x:
        return x
    sign = 1 if x >= 0 else -1
    if sign < 0:
        up = not up
    nt = type(x) if type(x) != int else float
    # Find out how many template "units" there are in x
    y = int(abs(x/template) + nt("0.5"))*abs(template)
    # Do rounding as needed
    if up and y < abs(x):
        y += template
    elif not up and y > abs(x):
        y -= template
    # Check that y is within one template of x
    assert abs(abs(x) - abs(y)) <= abs(template)
    return sign*y

if __name__ == "__main__":
    from math import pi
    from wrap import dedent
    from lwtest import run, raises, assert_equal, Assert
    def Test_TemplateRound():
        # Routine floating point rounding
        a, t = 463.77, 0.1
        Assert(TemplateRound(-a, t, up=True) == -463.7)
        Assert(TemplateRound(-a, t, up=False) == -463.8)
        Assert(TemplateRound(a, t, up=True) == 463.8)
        Assert(TemplateRound(a, t, up=False) == 463.7)
        a, t = 463.77, 1
        Assert(TemplateRound(-a, t, up=True) == -463)
        Assert(TemplateRound(-a, t, up=False) == -464)
        Assert(TemplateRound( a, t, up=True) == 464)
        Assert(TemplateRound( a, t, up=False) == 463)
        a, t = 463.77, 10
        Assert(TemplateRound(-a, t, up=True) == -460)
        Assert(TemplateRound(-a, t, up=False) == -470)
        Assert(TemplateRound( a, t, up=True) == 470)
        Assert(TemplateRound( a, t, up=False) == 460)
        Assert(TemplateRound(123.48, 0.1, up=True) == 123.5)
        Assert(TemplateRound(123.48, 0.1, up=False) == 123.4)
        # Integer rounding
        a, t = 463, 1
        Assert(TemplateRound(-a, t, up=True) == -463)
        Assert(TemplateRound(-a, t, up=False) == -463)
        Assert(TemplateRound( a, t, up=True) == 463)
        Assert(TemplateRound( a, t, up=False) == 463)
        a, t = 463, 10
        Assert(TemplateRound(-a, t, up=True) == -460)
        Assert(TemplateRound(-a, t, up=False) == -470)
        Assert(TemplateRound( a, t, up=True) == 470)
        Assert(TemplateRound( a, t, up=False) == 460)
        # Decimal rounding
        a, t = Decimal("123.48"), Decimal("0.1")
        Assert(TemplateRound(a, t, up=True) == Decimal("123.5"))
        Assert(TemplateRound(a, t, up=False) == Decimal("123.4"))
        # Fraction rounding:  a will be 123+31/64, t will be 1/8
        a, t = 123 + Fraction(31, 64), Fraction(1, 8)
        Assert(TemplateRound(a, t, up=True) == Fraction(247, 2))
        Assert(TemplateRound(a, t, up=False) == Fraction(987, 8))
        # mpmath
        if _have_mpmath:
            mpf = mpmath.mpf
            a, t = mpf("123.48"), mpf("0.1")
            Assert(TemplateRound(a, t, up=True) == mpf("123.5"))
            Assert(TemplateRound(a, t, up=False) == mpf("123.4"))
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
        x = 0.00081
        Assert(SigFig(x) == 2)
        x = 0.0001
        Assert(SigFig(x) == 1)
        x = 0.0000
        Assert(SigFig(x) == 1)

    Test_TemplateRound();exit() #xx

    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals(), halt=True)[0])
    else:
        print("Examples of RoundOff() and SigFig() use:")
        for i in (745.6998719999999, 4046.8726100000003, -0.0254*12):
            print("  RoundOff({}) = {}".format(i, RoundOff(i)))
        x = pi*1e8
        print("pi*1e8 rounded to indicated number of digits:")
        print(f"pi*1e8 = {x}")
        for i in range(1, 17):
            y = RoundOff(x, digits=i)
            print("  {:2d} {} [sigfig = {}]".format(i, y, SigFig(y)))
        print(dedent('''
        sigfig is reported as 12, but the number printed has more digits.
        This is deliberate and is based on the assumption that these
        numbers represent a physical quantity.
 
        Ignore the old convention of e.g. stating that 310000000.0 has 10 
        significant figures.  It has the number of significant figures that
        you rounded it to.  If you want to properly show the number of
        significant figures in a floating point number, give its interpolated
        string in scientific notation.
        '''))
