''' 
Provides dec(Decimal) objects with custom string interpolation

    Note:  The infection model was implemented by using the output of 
    the Signatures() function to determine which Decimal methods returned a
    Decimal object.  These were added to the class, calling the Decimal
    method and typecasting the result to a dec.  This was ultimately
    enabled by using the signatures gotten from help(Decimal).

    The Decimal module follows the "General Decimal Arithmetic
    Specification", version 1.70, 25 Mar 2009 by M. Cowlishaw.

Todo:
 
    * 
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
    if 1:   # Set to True to get color output
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
    g.o = C.lblu if C else ""
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
    # The following methods are implemented to allow dec to follow an
    # infection model.  They are the methods in Decimal that return a
    # Decimal.
    # --------------------------- 0 arguments ----------------------------
    def __abs__(self):
        return dec(super().__abs__())
    #def __copy__(...):
    #def __deepcopy__(...):
    def __neg__(self):
        return dec(super().__neg__())
    def __pos__(self):
        return dec(super().__pos__())
    def conjugate(self):
        return dec(super().conjugate())
    def copy_abs(self):
        return dec(super().copy_abs())
    def copy_negate(self):
        return dec(super().copy_negate())
    def exp(self, context=None):
        return dec(super().exp(context=context))
    def ln(self, context=None):
        return dec(super().ln(context=context))
    def log10(self, context=None):
        return dec(super().log10(context=context))
    def logb(self, context=None):
        return dec(super().logb(context=context))
    def logical_invert(self, context=None):
        return dec(super().logical_invert(context=context))
    def next_minus(self, context=None):
        return dec(super().next_minus(context=context))
    def next_plus(self, context=None):
        return dec(super().next_plus(context=context))
    def normalize(self, context=None):
        return dec(super().normalize(context=context))
    def radix(self):
        return dec(super().radix())
    def sqrt(self, context=None):
        return dec(super().sqrt(context=context))
    def to_integral(self, rounding=None, context=None):
        return dec(super().to_integral(context=context,
                                       rounding=rounding))
    def to_integral_exact(self, rounding=None, context=None):
        return dec(super().to_integral_exact(context=context,
                                             rounding=rounding))
    def to_integral_value(self, rounding=None, context=None):
        return dec(super().to_integral_value(context=context,
                                             rounding=rounding))
    # --------------------------- 1 argument -----------------------------
    def __add__(self, value):
        return dec(super().__add__(value))
    def __floordiv__(self, value):
        return dec(super().__floordiv__(value))
    def __mod__(self, value):
        return dec(super().__mod__(value))
    def __mul__(self, value):
        return dec(super().__mul__(value))
    def __pow__(self, value, mod=None):
        return dec(super().__pow__(value, mod=mod))
    def __radd__(self, value):
        return dec(super().__radd__(value))
    def __rfloordiv__(self, value):
        return dec(super().__rfloordiv__(value))
    def __rmod__(self, value):
        return dec(super().__rmod__(value))
    def __rmul__(self, value):
        return dec(super().__rmul__(value))
    def __rpow__(self, value, mod=None):
        return dec(super().__rpow__(value, mod=mod))
    def __rsub__(self, value):
        return dec(super().__rsub__(value))
    def __rtruediv__(self, value):
        return dec(super().__rtruediv__(value))
    def __sub__(self, value):
        return dec(super().__sub__(value))
    def __truediv__(self, value):
        return dec(super().__truediv__(value))
    def compare(self, value, context=None):
        return dec(super().compare(value, context=context))
    def compare_signal(self, value, context=None):
        return dec(super().compare_signal(value, context=context))
    def compare_total(self, value, context=None):
        return dec(super().compare_total(value, context=context))
    def compare_total_mag(self, value, context=None):
        return dec(super().compare_total_mag(value, context=context))
    def copy_sign(self, value, context=None):
        return dec(super().copy_sign(value, context=context))
    def logical_and(self, value, context=None):
        return dec(super().logical_and(value, context=context))
    def logical_or(self, value, context=None):
        return dec(super().logical_or(value, context=context))
    def logical_xor(self, value, context=None):
        return dec(super().logical_xor(value, context=context))
    def max(self, value, context=None):
        return dec(super().max(value, context=context))
    def max_mag(self, value, context=None):
        return dec(super().max_mag(value, context=context))
    def min(self, value, context=None):
        return dec(super().min(value, context=context))
    def min_mag(self, value, context=None):
        return dec(super().min_mag(value, context=context))
    def next_toward(self, value, context=None):
        return dec(super().next_toward(value, context=context))
    def quantize(self, exp, rounding=None, context=None):
        return dec(super().quantize(value, context=context))
    def remainder_near(self, value, context=None):
        return dec(super().remainder_near(value, context=context))
    def rotate(self, value, context=None):
        return dec(super().rotate(value, context=context))
    def scaleb(self, value, context=None):
        return dec(super().scaleb(value, context=context))
    def shift(self, value, context=None):
        return dec(super().shift(value, context=context))
def Signatures():
    'Print out the types of the return values of decimal.Decimal methods'
    x, y = D("1.234"), D("3.456")
    X, Y = D("11001"), D("11101")
    show = True
    seen = []
    w = 25
    t = "Error:  {n:{w}s}: {e}"
    def Type(z):
        global g
        s = str(type(z))[1:-1].replace("class", "").replace("'", "").strip()
        # Highlight the functions that return a Decimal, as these are ones
        # we need to implement
        if s == "decimal.Decimal":
            s = g.d + s + g.n
        else:
            s = g.o + s + g.n
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
    '''
    The following functions return a Decimal:

        No arguments:
            __abs__()           exp()               normalize()
            __copy__()          ln()                radix()
            __neg__()           log10()             sqrt()
            __pos__()           logb()              to_integral()
            conjugate()         logical_invert()    to_integral_exact()
            copy_abs()          next_minus()        to_integral_value()
            copy_negate()       next_plus()

        One argument:
            __add__(y)           __rsub__(y)          logical_xor(y)
            __deepcopy__(y)      __rtruediv__(y)      max(y)
            __floordiv__(y)      __sub__(y)           max_mag(y)
            __mod__(y)           __truediv__(y)       min(y)
            __mul__(y)           compare(y)           min_mag(y)
            __pow__(y)           compare_signal(y)    next_toward(y)
            __radd__(y)          compare_total(y)     quantize(y)
            __rfloordiv__(y)     compare_total_mag(y) remainder_near(y)
            __rmod__(y)          copy_sign(y)         rotate(y)
            __rmul__(y)          logical_and(y)       scaleb(y)
            __rpow__(y)          logical_or(y)        shift(y)
    '''
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
