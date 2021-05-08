'''
f.py
    This module is for routine calculations with real and complex numbers.
    The reals are of type flt and the complex numbers are of type cpx.
    These types should be handy for folks who do physical calculations with
    numbers derived from measurements because their str() form only shows a
    limited number of significant figures.  They also "infect" calculations
    with their types so that your results will be flt or cpx if you stick
    with int, float, complex, Fraction, and Decimal types in your
    calculations.

    All of the symbols in the math and cmath modules are in scope and they
    can take flt or cpx arguments where it makes sense.  They will return
    flt or cpx types appropriately, fitting the infection model.

    Example:

        >>> import f
        >>> from math import pi
        >>> pi
        3.141592653589793
        >>> type(pi)
        <class 'float'>
        >>> p = flt(pi)
        >>> type(p)
        <class 'f.flt'>
        >>> x, z = flt(p), cpx(p, 1/p)
        >>> x, z    # python uses repr() here, giving all the digits
        (3.141592653589793, (3.141592653589793+0.3183098861837907j))
        >>> x.f = True      # Interchange str() and repr() behavior
        >>> x, z
        (3.14, (3.14+0.318j))
        >>> sqrt(-1)        # A Delegator wrapper class calls cmath.sqrt
        (0.00+1.00j)

    This is the primary feature of using the module:  you won't see all
    those pesky extra digits.  The f attribute is handy for interactive
    sessions and in the debugger, but you don't need it for the print()
    command, which uses str() by default.

    If you use the h attribute for either a flt or cpx, you'll get a help
    message printed to stdout.  This should tell you enough to use the
    objects.  Also remember all math and cmath functions/constants are in
    scope.
'''

# TODO
'''
    * Color:  consider using color if the color module is present.

    * cpx attributes
        * ss:  (sign space) Defaults to ("", "").  Defaults to the empty
          string.  If they are both space characters, then you get '(1 +
          2j)' instead of '(1+2j)' or '1 + 2i' instead of '1+2i' if the
          i attribute is True.
'''
# Implementation
'''
    flt and cpx are derived from float and complex, so they can be used
    wherever float and complex can be used.  The Base class collects some
    common behavior.  The Formatter class in decimal_formatter.py will be
    used if it's available, but it's not mandatory (although the sci, eng,
    si, and sic attributes won't work).  Formatter is also nice because you
    can set the points where the fixed display changes to scientific
    notation.

    The "infection" model was gotten by implementing the numerical methods
    like __mul__ and __rmul__.  I'm currently (Apr 2021) using python 3.7.4
    as my standard python distribution and I'd been getting the strange
    behavior where 2j*cpx(3) would return a complex, but cpx(3)*2j would
    return a cpx.  I couldn't get both to return a cpx.  Then Windows did an
    OS update one night and the machine rebooted.  Then things worked fine
    after that with no code changes.

    The basic formatting strategy (with and without the Formatter class)
    is to use the scientific format of string interpolation f"{x:e}" with
    the proper number of decimal places to get the desired rounded string.
    The formatting is always done with Decimal objects to avoid float
    overflows or underflows.  I've testing the interpolation up to numbers
    with a million digits and things seem to work OK, so it should be
    robust.
'''

if 1:   # Imports
    # Standard library modules
    from collections.abc import Iterable
    from textwrap import dedent
    import cmath
    import decimal
    import locale
    import math
    import numbers
    import sys
    import time
if 1:   # Custom imports
    # Decimal formatter
    try:
        # This library, if present, is used to get the string form of flt
        # objects to a desired number of significant figures.  It also can
        # format in scientific and engineering forms.
        from decimal_formatter import Formatter
        _have_Formatter = True
    except ImportError:
        _have_Formatter = False
    # Debugging
    from pdb import set_trace as xx
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
    # Try to import the color.py module; if not available, the script
    # should still work (you'll just get uncolored output).
    try:
        import color as C
        _have_color = True
    except ImportError:
        # Make a dummy color object to swallow function calls
        class Dummy:
            def fg(self, *p, **kw): pass
            def normal(self, *p, **kw): pass
            def __getattr__(self, name): pass
        C = Dummy()
        _have_color = False

all = ["flt", "cpx"]
_no_color = (not sys.stdout.isatty()) or (not _have_color)

class Base(object):
    '''This class will contain the common things between the flt and cpx
    classes.
    '''
    _digits = 3         # Number of significant digits
    _dp = locale.localeconv()["decimal_point"]
    _flip = False       # If True, interchange str() and repr()
    _fmt = None         # Formatter for flt
    _color = False      # Allow ANSI color codes in str() & repr()
    _flt_color = C.lgreen
    _cpx_color = C.yellow
    def _check(self):
        'Make sure Base._digits is an integer >= 0 or None'
        if not isinstance(Base._digits, int):
            raise TypeError("Base._digits is not an integer")
        if Base._digits is not None:
            if Base._digits < 0:
                raise TypeError("Base._digits must be None or an int >= 0")
    def _r(self):
        raise RuntimeError("Base class method should be overridden")
    def _s(self):
        raise RuntimeError("Base class method should be overridden")
    # Properties
    @property
    def c(self):
        'If True, allow ANSI escape codes to color the output'
        return Base._color
    @c.setter
    def c(self, value):
        Base._color = bool(value)
    @property
    def f(self):
        'Flip the behavior of str() and repr() if value is True'
        return Base._flip
    @f.setter
    def f(self, value):
        Base._flip = bool(value)
    @property
    def h(self):
        'Print help to stdout'
        self.help()
    @property
    def n(self):
        'Return/set how many digits to round to'
        if not isinstance(Base._digits, int):
            raise TypeError("Base._digits is not an integer")
        return Base._digits
    @n.setter
    def n(self, value):
        if value is None:
            value = 0
        if not isinstance(value, int) or value < 0:
            raise ValueError("value must be an integer >= 0 or None")
        Base._digits = value
        if _have_Formatter:
            # Note Formatter won't allow 0 digits, so we let it be the
            # maximum number of digits in a float.
            from sys import float_info
            Base._fmt.n = value if value else float_info.dig
            Base._digits = Base._fmt.n
    @property
    def r(self):
        'Return the repr() string, regardless of self.f'
        return self._r()
    @property
    def s(self):
        'Return the str() string, regardless of self.f'
        return self._s()
    @property
    def t(self):
        'Return date/time string'
        f = time.strftime
        d = int(f("%d"))
        dt = f"{d}{f('%b%Y')}"
        h = f("%H")
        if h[0] == "0":
            h = h[1:]
        t = f"{h}:{f('%M:%S')} {f('%p').lower()}"
        return f"{dt} {t}"
    # These properties will work if the Formatter object is present
    @property
    def eng(self):
        'Return a string formatted in engineering notation'
        return Base._fmt(self, fmt="eng") if _have_Formatter else ""
    @property
    def si(self):
        '''Return a string formatted in engineering notation with SI
        prefix appended with a space character.
        '''
        return self._s(fmt="engsi")
    @property
    def sic(self):
        '''Return a string formatted in engineering notation with SI
        prefix appended with no space character.
        '''
        return self._s(fmt="engsic")
    @property
    def sci(self):
        'Return a string formatted in scientific notation'
        return self._s(fmt="sci")
    @staticmethod
    def wrap(string, number):
        'Provide ANSI escape codes around the string'
        if _no_color or not number.c:
            return string
        o = []
        if isinstance(number, flt):
            o.append(C.fg(Base._flt_color, s=True))
            o.append(string)
            o.append(C.normal(s=True))
            return ''.join(o)
        elif isinstance(number, cpx):
            o.append(C.fg(Base._cpx_color, s=True))
            o.append(string)
            o.append(C.normal(s=True))
            return ''.join(o)
        else:
            return string

class flt(Base, float):
    '''The flt class is a float except that its str() representation is
    limited to the number of significant figures set in the attribute n.
    Changing n for an instance changes all flt objects' behavior.  Set
    it to None or 0 to return to normal float behavior.
    '''
    def __new__(cls, value):
        instance = super().__new__(cls, value)
        instance._check()
        if _have_Formatter and Base._fmt is None:
            Base._fmt = Formatter(Base._digits)
        return instance
    def _s(self, fmt="fix", no_color=False):
        '''Return the rounded string representation.  The fmt keyword only
        works if the Formatter class is present.
        '''
        self._check()
        if not Base._digits:
            return str(float(self))
        f = lambda x: x if no_color else Base.wrap(x, self)
        x = decimal.Decimal(self)
        if _have_Formatter:
            return f(Base._fmt(x, fmt=fmt))
        else:
            with decimal.localcontext() as ctx:
                ctx.prec = abs(Base._digits)
                x = +x  # Update x to stated precision
                s = str(float(x))
                while "e" not in s and "E" not in s and s[-1] == "0":
                    s = s[:-1] # Remove trailing zero
                return f(s)
    def _r(self, no_color=False):
        'Return the repr string representation'
        self._check()
        f = lambda x: x if no_color else Base.wrap(x, self)
        s = repr(float(self))
        if no_color:
            return s
        return f(s)
    def __str__(self):
        return self._r() if Base._flip else self._s()
    def __repr__(self):
        return self._s() if Base._flip else self._r()
    # Public methods
    def round(self, n=None):
        'Return flt rounded to n places or Base._digits if n is None'
        if n is None:
            n = Base._digits
        if not isinstance(n, int) or n < 0:
            raise ValueError("n must be an integer >= 0 or None")
        if n:
            x = decimal.Decimal(self)
            with decimal.localcontext() as ctx:
                ctx.prec = abs(n)
                x = +x
                return flt(x)
        else:
            return self
    def help(self):
        print(dedent('''
        The flt class is derived from float and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          eng       Format in engineering notation
          si        Format in engineering notation with SI prefix
          sic       Format in engineering notation with SI prefix cuddled
          f       * Flip behavior of str() and repr()
          h         Print this help
          n       * Set/read the number of significant figures
          r         The repr() string, regardless of f attribute state
          s         The str() string, regardless of f attribute state
          t       * Date and time
          sci       Format in scientific notation
             * means the attribute affects all flt and cps instances'''[1:]))
    # Define the arithmetic functions so that we get a flt back when
    # doing arithmetic with floats and integers.  If other is a complex,
    # we'll return a cpx.
    def __add__(self, other):
        if isinstance(other, complex):
            return cpx(float(self) + other)
        return flt(float(self) + float(other))
    def __sub__(self, other):
        if isinstance(other, complex):
            return cpx(float(self) - other)
        return flt(float(self) - float(other))
    def __mul__(self, other):
        if isinstance(other, complex):
            return cpx(float(self)*other)
        return flt(float(self)*float(other))
    def __truediv__(self, other):
        if isinstance(other, complex):
            return cpx(float(self)/other)
        return flt(float(self)/float(other))
    def __floordiv__(self, other):
        return flt(float(self)//float(other))
    def __mod__(self, other):
        return flt(float(self) % float(other))
    def __divmod__(self, other):
        a, b = divmod(float(self), float(other))
        return (flt(a), flt(b))
    def __pow__(self, other):
        return flt(pow(float(self), float(other)))
    def __radd__(self, other):
        return flt(float(other) + float(self))
    def __rsub__(self, other):
        return flt(float(other) - float(self))
    def __rmul__(self, other):
        return flt(float(other)*float(self))
    def __rtruediv__(self, other):
        return flt(float(other)/float(self))
    def __rfloordiv__(self, other):
        return flt(float(other)//float(self))
    def __rmod__(self, other):
        return flt(float(other) % float(self))
    def __rdivmod__(self, other):
        a, b = divmod(float(other), float(self))
        return (flt(a), flt(b))
    def __rpow__(self, other):
        return flt(self.pow(float(other), float(self)))
    def __abs__(self):
        return flt(abs(self))

class cpx(Base, complex):
    '''The cpx class is a complex except that its components are flt
    numbers.
    '''
    _i = False      # If True, use "i" instead of "j" in str()
    _p = False      # If True, use polar representation in str()
    _z = False      # If True, don't print out zero components
    def __new__(cls, real, imag=0):
        'real can be a number type, a cpx, or a complex.'
        if isinstance(real, cpx):
            instance = super().__new__(cls, real._real, real._imag)
            instance._real = flt(real._real)
            instance._imag = flt(real._imag)
        elif isinstance(real, numbers.Real):
            instance = super().__new__(cls, real, imag)
            instance._real = flt(real)
            instance._imag = flt(imag)
        elif isinstance(real, numbers.Complex):
            instance = super().__new__(cls, real.real, real.imag)
            instance._real = flt(real.real)
            instance._imag = flt(real.imag)
        else:
            if isinstance(real, str):
                z = complex(real)
                instance = cpx(z)
            else:
                instance = super().__new__(cls, real, imag)
                instance._real = flt(real)
                instance._imag = flt(imag)
        return instance
    def _pol(self, rep=False):
        'Return polar form'
        f = lambda x:  Base.wrap(x, self)
        r, θ = [flt(i) for i in polar(self)]
        θ *= 180/pi if self.p == 1 else 1
        d = "°" if self.p == 1 else ""
        if rep:
            s = f"{r._r(no_color=True)}∠{θ._r(no_color=True)}{d}"
        else:
            s = f"{r._s(no_color=True)}∠{θ._s(no_color=True)}{d}"
        t = f(s) if self.i else f("(" + s + ")")
        return f(t)
    def _s(self, fmt="fix"):
        '''Return the rounded string representation.  If cpx.i is True,
        then "i" is used as the unit imaginary and no parentheses are
        placed around the string.  If cpx.p is 0, use rect; 1 is polar
        in degrees, 2 is polar in radians.
        '''
        f = lambda x:  Base.wrap(x, self)
        if cpx._p:
            # Polar
            return self._pol()
        else:
            # Rectangular
            r, i = self._real, self._imag
            re, im = r._s(fmt=fmt, no_color=True), i._s(fmt=fmt, no_color=True)
            if self.z and ((r and not i) or (not r and i)):
                if r:
                    s = f"{re}" if cpx._i else f"({re})"
                else:
                    s = f"{im}i" if cpx._i else f"({im}j)"
            else:
                im = "+" + im if im[0] != "-" else im
                s = f"{re}{im}i" if cpx._i else f"({re}{im}j)"
            return f(s)
    def _r(self):
        'Return the full representation string'
        s = repr(complex(self))
        if self.p:
            s = self._pol(rep=True)
        elif self.i:
            s = s.replace("(", "").replace(")", "").replace("j", "i")
        return Base.wrap(s, self)
    def __str__(self):
        return self._r() if Base._flip else self._s()
    def __repr__(self):
        return self._s() if Base._flip else self._r()
    def round(self, n=None):
        'Return a cpx with components rounded to n decimal places'
        return cpx(self.real.round(n), self.imag.round(n))
    def help(self):
        print(dedent('''
        The cpx class is derived from complex and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          eng       Format in engineering notation
          si        Format in engineering notation with SI prefix
          sic       Format in engineering notation with SI prefix cuddled
          f       * Flip behavior of str() and repr()
          h         Print this help
          i       * Use 'i' instead of 'j' as the imaginary unit
          imag      Return the imaginary component
          n       * Set/read the number of significant figures
          p       * 0=rect, 1=polar degrees, 2=polar radians
          r         The repr() string, regardless of f attribute state
          real      Return the real component
          s         The str() string, regardless of f attribute state
          t       * Date and time
          sci       Format in scientific notation
          z       * Don't print zero components if True
             * means these attributes affect all cpx instances'''[1:]))
    # Define the arithmetic functions so that we get a cpx back when
    # doing arithmetic with other numbers.
    def __complex__(self):
        return complex(self._real, self._imag)
    def __add__(self, other):
        return cpx(complex(self) + complex(other))
    def __sub__(self, other):
        return cpx(complex(self) - complex(other))
    def __mul__(self, other):
        return cpx(complex(self)*complex(other))
    def __truediv__(self, other):
        return cpx(complex(self)/complex(other))
    def __pow__(self, other):
        return cpx(complex(self)**complex(other))
    def __radd__(self, other):
        return cpx(complex(other) + complex(self))
    def __rsub__(self, other):
        return cpx(complex(other) - complex(self))
    def __rmul__(self, other):
        return cpx(complex(other)*complex(self))
    def __rtruediv__(self, other):
        return cpx(complex(other)/complex(self))
    def __rpow__(self, other):
        #return cpx(pow(complex(other), complex(self)))
        return cpx(complex(other)**complex(self))
    def __neg__(self):
        return cpx(-complex(self))
    def __pos__(self):
        return cpx(complex(self))
    def __abs__(self):
        return flt(abs(complex(self)))
    # Properties
    @property
    def real(self):
        return self._real
    @property
    def imag(self):
        return self._imag
    @property
    def i(self):
        'Return boolean that indicates using "i" instead of "j"'
        return cpx._i
    @i.setter
    def i(self, value):
        'Set boolean that indicates using "i" instead of "j"'
        cpx._i = bool(value)
    @property
    def p(self):
        'If 0, use rectangular coordinates, if != 0, use polar.'
        return cpx._p
    @p.setter
    def p(self, value):
        '''If 0, display complex numbers in rectangular form.  If 1,
        display in polar form using degrees.  If 2, display in polar
        using radians.
        '''
        cpx._p = int(value)
    @property
    def z(self):
        '''Return boolean that indicates don't print out zero components'''
        return cpx._z
    @z.setter
    def z(self, value):
        '''Set boolean that indicates don't print out zero components'''
        cpx._z = bool(value)

if 1:   # Get math/cmath functions into our namespace
    '''Put all math symbols into this namespace.  We use an object with
    the same name as the function and let it have a __call__ method.
    When called, it calls the relevant math or cmath function and
    returns the result if it doesn't get an exception.  It also allows for
    special handling where needed (e.g., see how sqrt of a negative number
    is handled to give a cpx instead of an exception).
    '''
    class Delegator(object):
        '''A delegator object is used to encapsulate the math and cmath
        functions and allow them to be put in this module's namespace.  When
        the Delegator instance.__call__ is called, the cmath routine is
        called if any of the arguments are complex; otherwise, the math
        routine is called.
        '''
        def __init__(self, name):
            self.name = name
        def __call__(self, *args, **kw):
            C, ii = (complex, cpx), isinstance
            if hasattr(math, name) and not hasattr(cmath, name):
                # Forces a math call
                s = f"math.{self.name}(*args, **kw)"
            elif not hasattr(math, name) and hasattr(cmath, name):
                # Forces a cmath call
                s = f"cmath.{self.name}(*args, **kw)"
            else:
                if self.iscomplex(*args, **kw):
                    s = f"cmath.{self.name}(*args, **kw)"
                else:
                    if self.name == "sqrt" and len(args) == 1 and args[0] < 0:
                        s = f"cmath.{self.name}(*args, **kw)"
                    elif self.name == "rect" and len(args) == 2:
                        s = f"cmath.{self.name}(*args, **kw)"
                    elif self.name == "pow" and len(args) == 2:
                        s = f"math.{self.name}(*args, **kw)"
                    else:
                        s = f"math.{self.name}(*args, **kw)"
            # Now execute the function.  You'll get a TypeError if you do
            # something like erf(1j), just what you'll get from
            # math.erf(1j).  However, the Delegator's exception message will
            # tell you that "module 'cmath' has no attribute 'erf'".  The
            # TypeError from math.erf will tell you "can't convert complex
            # to float".  The complex argument forced the Delegator to
            # search for a complex function, which doesn't exist.  This
            # could be fixed with more code (e.g., knowing erf is only in
            # math), but I don't think it's worth the extra effort.
            try:
                result = eval(s)
            except AttributeError as err:
                raise TypeError(err) from None
            if ii(result, int):
                return result
            elif ii(result, (float, flt)):
                return flt(result)
            elif ii(result, C):
                return cpx(result)
            else:
                if self.name == "polar":
                    result = tuple([flt(i) for i in result])
                return result
        @staticmethod
        def iscomplex(*args, **kw):
            '''Return True if any argument or keyword argument is
            complex.  If arg[0] is an iterator, also look for complex
            numbers in it.
            '''
            C, ii = (complex, cpx), isinstance
            cc = lambda x: any([ii(i, C) for i in x])
            if cc(list(args) + list(kw.values())):
                return True
            if len(args) == 1:
                if not ii(args[0], str) and ii(args[0], Iterable):
                    return cc(args[0])
            return False
    # All math/cmath function names for Version 3.9.4
    functions = '''
    acos      comb      exp       gamma     lcm       nextafter remainder
    acosh     copysign  expm1     gcd       ldexp     perm      sin
    asin      cos       fabs      hypot     lgamma    phase     sinh
    asinh     cosh      factorial isclose   log       polar     sqrt
    atan      degrees   floor     isfinite  log10     pow       tan
    atan2     dist      fmod      isinf     log1p     prod      tanh
    atanh     erf       frexp     isnan     log2      radians   trunc
    ceil      erfc      fsum      isqrt     modf      rect      ulp
    '''
    for name in functions.split():
        if hasattr(math, name) or hasattr(cmath, name):
            s = f"{name} = Delegator('{name}')"
            exec(s)
    # Constants
    #   both:  e inf nan pi tau
    #   cmath: infj nanj 
    from math import e, inf, nan, pi, tau
    from cmath import infj, nanj
    # Change constants' type to flt
    constants = "e pi tau".split()
    for i in constants:
        exec(f"{i} = flt({i})")

if __name__ == "__main__": 
    x, z = flt(3.4), cpx(-pi, 1/pi)
    z.i = 1
    print(x, z)
    x.c = True
    print(x, z)
    z.p = 1
    print(z)
    print(z.r)
    print(z.t)
