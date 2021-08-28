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
    __abs__(self, /)
    __add__(self, value, /)
    __bool__(self, /)
    __ceil__(...)
    __complex__(...)
    __copy__(...)
    __deepcopy__(...)
    __divmod__(self, value, /)
    __eq__(self, value, /)
    __float__(self, /)
    __floor__(...)
    __floordiv__(self, value, /)
    __format__(...)
    __ge__(self, value, /)
    __getattribute__(self, name, /)
    __gt__(self, value, /)
    __hash__(self, /)
    __int__(self, /)
    __le__(self, value, /)
    __lt__(self, value, /)
    __mod__(self, value, /)
    __mul__(self, value, /)
    __ne__(self, value, /)
    __neg__(self, /)
    __pos__(self, /)
    __pow__(self, value, mod=None, /)
    __radd__(self, value, /)
    __rdivmod__(self, value, /)
    __reduce__(...)
    __repr__(self, /)
    __rfloordiv__(self, value, /)
    __rmod__(self, value, /)
    __rmul__(self, value, /)
    __round__(...)
    __rpow__(self, value, mod=None, /)
    __rsub__(self, value, /)
    __rtruediv__(self, value, /)
    __sizeof__(...)
    __str__(self, /)
    __sub__(self, value, /)
    __truediv__(self, value, /)
    __trunc__(...)

    compare(self, /, other, context=None)
    compare_signal(self, /, other, context=None)
    compare_total(self, /, other, context=None)
    compare_total_mag(self, /, other, context=None)
    conjugate(self, /)
    copy_abs(self, /)
    copy_negate(self, /)
    copy_sign(self, /, other, context=None)
    exp(self, /, context=None)
    fma(self, /, other, third, context=None)
    ln(self, /, context=None)
    log10(self, /, context=None)
    logb(self, /, context=None)
    logical_and(self, /, other, context=None)
    logical_invert(self, /, context=None)
    logical_or(self, /, other, context=None)
    logical_xor(self, /, other, context=None)
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
    from functools import partial
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from columnize import Columnize
    if 0:
        from color import C
    else:
        C = None
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    ii = isinstance
    D = decimal.Decimal
    class g: pass
    g.d = C.lgrn if C else ""
    g.o = C.lyel if C else ""
    g.n = C.norm if C else ""

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
def Signatures():
    'Print out the types of the return values of decimal.Decimal methods'
    x, y = D("1.234"), D("3.456")
    X, Y = D("11001"), D("11101")
    show = True
    seen = []
    w = 25
    t = "Error:  {n:{w}s}: {e}"
    def Type(z):
        s = str(type(z))[1:-1].replace("class", "").replace("'", "").strip()
        # Highlight the functions that return a Decimal, as these are ones
        # we need to implement
        if s == "decimal.Decimal":
            s = g.d + s + g.n
        return s
    def ZeroArgs(name, x, us=""):
        n = f"x.{us}{name}{us}()"
        seen.append(n)
        try:
            z = eval(n)
            if show:
                print(f"{n:{w}s}   {Type(z)}")
        except Exception as e:
            print(t.format(**locals()))
    def OneArg(name, x, y, us=""):
        n = f"x.{us}{name}{us}(y)"
        seen.append(n)
        try:
            z = eval(n)
            if show:
                print(f"{n:{w}s}   {Type(z)}")
        except Exception as e:
            print(t.format(**locals()))
    def TwoArgs(name, x, y, z, us=""):
        n = f"x.{us}{name}{us}(y, z)"
        seen.append(n)
        try:
            t = eval(n)
            if show:
                print(f"{n:{w}s}   {Type(z)}")
        except Exception as e:
            print(t.format(**locals()))
    print("Missing stuff:  format getattribute")
    if 1:   # Functions with double underscores
        f = partial(ZeroArgs, us="__")
        for name in '''abs bool ceil complex copy neg pos float floor 
            hash int reduce repr round sizeof str trunc
            neg pos
            '''.split():
            f(name, x)
        #
        f = partial(OneArg, us="__")
        for name in '''add deepcopy divmod eq floordiv ge gt
            le lt mod mul ne pow radd rdivmod rfloordiv rmod rmul rpow
            rsub rtruediv sub truediv
            '''.split():
            f(name, x, y)
        #
        f = partial(TwoArgs, us="__")
        for name in '''
            '''.split():
            f(name, x, y, 2)
    if 1:   # Regular functions
        f = ZeroArgs
        for name in '''conjugate copy_abs copy_abs copy_negate exp ln log10
            logb logical_invert next_minus next_plus normalize
            number_class radix sqrt to_eng_string to_integral to_integral_exact
            to_integral_value
            '''.split():
            if name in "logical_invert".split():
                f(name, X)
            else:
                f(name, x)
        #
        f = OneArg
        for name in '''compare compare_signal compare_total compare_total_mag
            copy_sign logical_and logical_or logical_xor max max_mag min
            min_mag next_toward quantize remainder_near rotate same_quantum
            scaleb shift
            '''.split():
            if name in '''logical_and logical_or logical_xor rotate scaleb
                          shift'''.split():
                if name in "rotate scaleb shift".split():
                    f(name, X, D(1))
                else:
                    f(name, X, Y)
            else:
                f(name, x, y)
        #
        f = TwoArgs
        for name in '''fma
            '''.split():
            f(name, x, y, 2)
    if 1:   # List the functions we've seen
        print(f"\nList of {len(seen)} functions examined:")
        seen = [i[2:] for i in sorted(seen)]
        for i in Columnize(seen, indent=" "*2):
            print(i)
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

if 1:
    # Show the return types of decimal.Decimal's methods
    Signatures()
    exit()
if 0:
    AddMethods()
    exit()
if 0:
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
