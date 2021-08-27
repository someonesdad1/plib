'''
Todo:

    * If x is a dec, then -x returns a Decimal.  Need to have all 
      such operations defined so that a dec is returned.
    * Similarly, all math operations need to be defined to allow infection
      to occur.  Maybe these can be defined as part of the script instead
      of having to write every one of them:

__repr__           __bool__           quantize           copy_sign
__hash__           __int__            remainder_near     same_quantum
__str__            __float__          fma                logical_and
__getattribute__   __floordiv__       is_canonical       logical_or
__lt__             __rfloordiv__      is_finite          logical_xor
__le__             __truediv__        is_infinite        rotate
__eq__             __rtruediv__       is_nan             scaleb
__ne__             __new__            is_qnan            shift
__gt__             exp                is_snan            from_float
__ge__             ln                 is_signed          as_tuple
__add__            log10              is_zero            as_integer_ratio
__radd__           next_minus         is_normal          __copy__
__sub__            next_plus          is_subnormal       __deepcopy__
__rsub__           normalize          adjusted           __format__
__mul__            to_integral        canonical          __reduce__
__rmul__           to_integral_exact  conjugate          __round__
__mod__            to_integral_value  radix              __ceil__
__rmod__           sqrt               copy_abs           __floor__
__divmod__         compare            copy_negate        __trunc__
__rdivmod__        compare_signal     logb               __complex__
__pow__            max                logical_invert     __sizeof__
__rpow__           max_mag            number_class       real
__neg__            min                to_eng_string      imag
__pos__            min_mag            compare_total      __doc__
__abs__            next_toward        compare_total_mag  __module__

Signatures:
 *  __abs__(self, /)
 *  __add__(self, value, /)
    __bool__(self, /)
    __ceil__(...)
    __complex__(...)
 *  __copy__(...)
 *  __deepcopy__(...)
    __divmod__(self, value, /)
    __eq__(self, value, /)
    __float__(self, /)
    __floor__(...)
 *  __floordiv__(self, value, /)
    __format__(...)
    __ge__(self, value, /)
    __getattribute__(self, name, /)
    __gt__(self, value, /)
    __hash__(self, /)
    __int__(self, /)
    __le__(self, value, /)
    __lt__(self, value, /)
 *  __mod__(self, value, /)
 *  __mul__(self, value, /)
    __ne__(self, value, /)
 *  __neg__(self, /)
 *  __pos__(self, /)
 *  __pow__(self, value, mod=None, /)
 *  __radd__(self, value, /)
 *  __rdivmod__(self, value, /)
    __reduce__(...)
 *  __repr__(self, /)
 *  __rfloordiv__(self, value, /)
    __rmod__(self, value, /)
 *  __rmul__(self, value, /)
    __round__(...)
 *  __rpow__(self, value, mod=None, /)
 *  __rsub__(self, value, /)
 *  __rtruediv__(self, value, /)
    __sizeof__(...)
 *  __str__(self, /)
 *  __sub__(self, value, /)
 *  __truediv__(self, value, /)
    __trunc__(...)
    compare(self, /, other, context=None)
    compare_signal(self, /, other, context=None)
    compare_total(self, /, other, context=None)
    compare_total_mag(self, /, other, context=None)
    conjugate(self, /)
    copy_abs(self, /)
    copy_negate(self, /)
    copy_sign(self, /, other, context=None)
 *  exp(self, /, context=None)
    fma(self, /, other, third, context=None)
 *  ln(self, /, context=None)
 *  log10(self, /, context=None)
 *  logb(self, /, context=None)
 *  logical_and(self, /, other, context=None)
 *  logical_invert(self, /, context=None)
 *  logical_or(self, /, other, context=None)
 *  logical_xor(self, /, other, context=None)
    max(self, /, other, context=None)
    max_mag(self, /, other, context=None)
    min(self, /, other, context=None)
    min_mag(self, /, other, context=None)
    next_minus(self, /, context=None)
    next_plus(self, /, context=None)
    next_toward(self, /, other, context=None)
    normalize(self, /, context=None)
    number_class(self, /, context=None)
    quantize(self, /, exp, rounding=None, context=None)
    radix(self, /)
    remainder_near(self, /, other, context=None)
    rotate(self, /, other, context=None)
    same_quantum(self, /, other, context=None)
    scaleb(self, /, other, context=None)
    shift(self, /, other, context=None)
    sqrt(self, /, context=None)
    to_eng_string(self, /, context=None)
    to_integral(self, /, rounding=None, context=None)
    to_integral_exact(self, /, rounding=None, context=None)
    to_integral_value(self, /, rounding=None, context=None)

    Class methods:
        from_float(f, /) from builtins.type

Provides Decimal objects with custom string interpolation
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
    # <math> Provides a dec object that is derived from
    # decimal.Decimal but has custom string interpolation.  It also
    # "infects" calculations with its type, providing a number class for
    # general-purpose calculations without the limitations of the float
    # type.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import locale
    from collections import deque
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    ii = isinstance
    D = decimal.Decimal
class dec(decimal.Decimal):
    '''Provides decimal.Decimal numbers with custom string interpolation.
    This class also "infects" calculations with integers, floats, and
    decimal.Decimal numbers by always returning a dec object.
    '''
    _digits = 3         # Number of significant digits for str()
    _sigcomp = None     # Number of sig digits for comparisons
    _dp = locale.localeconv()["decimal_point"]
    _rtz = False        # Remove trailing zeros if True
    _rtdp = False       # Remove trailing decimal point
    _low = 1e-5         # When to switch to scientific notation
    _high = 1e16        # When to switch to scientific notation
    _e = "e"            # Letter in scientific notation
    def __new__(cls, value="0", context=None):
        instance = super().__new__(cls, value, context)
        return instance
    def __str__(self):
        if self > dec._high or self < dec._low:
            return self.sci(dec._digits)
        return self.fix(dec._digits)
    def fix(self, n):
        'Return fixed-point form of x with n significant figures'
        dp = locale.localeconv()["decimal_point"]
        sign = "-" if self < 0 else ""
        # Get significand and exponent
        t = f"{abs(self):.{n - 1}{dec._e}}"
        s, e = t.split(dec._e)
        exponent = int(e)
        if not self:
            return s
        if not exponent:
            return sign + s.replace(".", dp)
        significand = s.replace(dp, "")
        # Generate the fixed-point representation
        sig, out, zero_digit = deque(significand), deque(), "0"
        out.append(sign + zero_digit + dp if exponent < 0 else sign)
        if exponent < 0:
            while exponent + 1:
                out.append(zero_digit)
                exponent += 1
            while sig:
                out.append(sig.popleft())
        else:
            while exponent + 1:
                out.append(sig.popleft()) if sig else out.append(zero_digit)
                exponent -= 1
            out.append(dp)
            while sig:
                out.append(sig.popleft())
        return f"{''.join(out)}"
    def sci(self, n):
        'Return self in scientific notation with n significant figures'
        dp = locale.localeconv()["decimal_point"]
        sign = "-" if self < 0 else ""
        # Get significand and exponent
        t = f"{abs(self):.{n - 1}{dec._e}}"
        s, e = t.split(dec._e)
        s.replace(".", dp)
        exponent = int(e)
        if not self:
            return s
        if not exponent:
            return sign + s
        # Generate the scientific notation representation
        return sign + s + dec._e + str(exponent)
    def __neg__(self):
        return dec(super().__neg__())
    def __add__(self, other):
        return dec(super().__add__(other))

def AddMethods():
    '''Routine to add the necessary methods so that dec objects infect
    routine calculations with their type.
    
    https://www.oreilly.com/library/view/python-cookbook/0596001673/ch05s13.html
    '''
    # No arguments
    def Add(name, *args):
        if not args:
            f = lambda: eval(f"dec(super().__{name}__())")
        elif len(args) ==  1:
            f = lambda x: eval(f"dec(super().__{name}__(x))")
        elif len(args) ==  2:
            f = lambda x, y: eval(f"dec(super().__{name}__(x, y))")
        elif len(args) ==  3:
            f = lambda x, y, z: eval(f"dec(super().__{name}__(x, y, z))")
        else:
            raise ValueError("Too many args")
        setattr(dec, name, f)
    for name in '''abs copy deepcopy neg pos'''.split():
        Add(name)
    for name in '''add'''.split():
        Add(name, "other")
AddMethods()

if 1:
    from lwtest import run, raises, assert_equal, Assert
    d = dec("1.2345")
    e = -d
    Assert(e == dec("-1.2345"))
    Assert(type(e) == type(dec("-1.2345")))
    # Addition
    e = d + d
    Assert(e == 2*dec("1.2345"))
    Assert(type(e) == type(d))
    exit()
if 0:
    d = decimal.Decimal.__dict__
    from columnize import Columnize
    for i in Columnize(d.keys()):
        print(i)
    exit()
if 0:
    a = dec(1.23)
    print(a)
    print(type(-a))
    exit(0)
if __name__ == "__main__": 
    # Use mpmath (http://mpmath.org/) to generate the numbers to test
    # against (i.e., assume mpmath's algorithms are correct).
    import mpmath as mp
    from pdb import set_trace as xx
    from wrap import wrap, dedent, indent, Wrap
    from lwtest import run, raises, assert_equal, Assert
    getcontext = decimal.getcontext
    localcontext = decimal.localcontext
    def Test_fix():
        d = dec("1.23456789")
        expected = '''
            1
            1.2
            1.23
            1.235
            1.2346
            1.23457
            1.234568
            1.2345679
            1.23456789
            1.234567890
            1.2345678900
            '''.split()
        for i in range(1, 12):
            Assert(d.fix(i) == expected[i - 1])
            Assert((-d).fix(i) == "-" + expected[i - 1])
    def Test_sci():
        d = dec("1.23456789e33")
        expected = '''
            1e33
            1.2e33
            1.23e33
            1.235e33
            1.2346e33
            1.23457e33
            1.234568e33
            1.2345679e33
            1.23456789e33
            1.234567890e33
            1.2345678900e33
            '''.split()
        for i in range(1, 12):
            Assert(d.sci(i) == expected[i - 1])
            Assert((-d).sci(i) == "-" + expected[i - 1])
        d = dec("1.23456789e-33")
        expected = '''
            1e-33
            1.2e-33
            1.23e-33
            1.235e-33
            1.2346e-33
            1.23457e-33
            1.234568e-33
            1.2345679e-33
            1.23456789e-33
            1.234567890e-33
            1.2345678900e-33
            '''.split()
        for i in range(1, 12):
            Assert(d.sci(i) == expected[i - 1])
            Assert((-d).sci(i) == "-" + expected[i - 1])
    def Test_add():
        d = dec("1.2345")
        x = d + 3
        Assert(x == dec("4.2345"))
        Assert(ii(x, dec))
    mp.mp.dps = getcontext().prec
    eps = 10*dec(10)**(-dec(getcontext().prec))
    exit(run(globals())[0])
