''' 
 
TODO
    -flt
        - rlz doesn't remove 0 for negative numbers
    - cpx:
        - .t property:  tuple display.  z=cpx(1,1) --> "(1,1)".  Use wide
      attribute .w for "(1, 1)".  .w also gets "1 + i" form.
        - .w property:  wide display
        - Special forms:  1+i, i, -i, etc.
 
Module for calculations with real and complex numbers 

    The reals are of type flt (derived from float) and the complex numbers
    are of type cpx (derived from complex).

    Their primary feature is that you'll only see 3 digits when you print
    them as a string:
        
        from f import flt, cpx, asin
        a = 1/3
        b = flt(1/3)
        z = cpx(1/3, 2/3)
        print(a)
        print(b)
        print(z)
        print(asin(1))
        print(asin(1.1))

    results in

        0.3333333333333333      # Typical python float string interpolation
        0.333                   # flt shows 3 digits by default
        (0.333+0.667j)          # cpx is two flt instances
        1.57                    # math module function in scope
        (1.57+0.444j)           # cmath module function in scope

    Other flt/cpx features are
        
        - flt and cpx instances can contain arbitrary attributes
        - They are immutable and hashable.  They hash to the same values as
          their corresponding float and complex values.
        - Equality comparisons can be made to a chosen number of digits.
          This can be useful in decision-making contexts.
 
    The motivation for these types is doing calculations with numbers
    derived from physical measurements; it's rare to need more than a few
    digits in the results.  This module's string interpolations help you
    see the basic behavior of a calculation without seeing lots of digits
    that don't contain useful information.

    Behind the scenes the calculations are done with python's standard
    floats and complex numbers, so the usual 16 or so digits are there if
    you want them.  If you need calculation speed or minimum memory use,
    stick with python floats and complex numbers, as this module is slower
    and uses Decimal objects, which use substantially more memory.  

    The flt and cpx types are convenient for casual computations in e.g.
    the python REPL.

    - Interpolated digits

        Set the flt or cpx N attribute to the number of digits you wish to
        work with.  All instances then string interpolate to that number of
        digits.  When you want an instance to have a different number of
        digits, use the n attribute, which affects the instance only.  Set
        the instance's n attribute to zero to get the default behavior
        back.

        flt and cpx object are context managers, so you can change any
        class or instance attributes in a context manager block, then get
        back where you were after the block exits.

            z = cpx(3.45678, 8.76543)
            print(z)
            with z:
                z.N = 6
                z.i = True      # Use i as the complex unit
                print(z)
                z.p = True      # Polar coordinates with degrees
                print(z)
            print(z)            # Same as before the with block

        results in

            (3.46+8.77j)
            3.45678+8.76543i
            9.42242∠68.4775°
            (3.46+8.77j)

        A lock makes the context manager thread-safe, but can also cause
        deadlocks, so only use short chunks of code in with blocks.

    - Closure

        By design, binary operations with flt and cpx instances will return
        corresponding flt and cpx instances when used with other number
        types.  This fits the use case for these objects, which was to be
        used with numbers derived from physical measurements, letting you
        only see the relevant information in a problem.

        This behavior can give results you don't expect.  For example, a
        flt instance multiplied by a Decimal or Fraction instance will
        result in a flt instance.  Since Decimal and Fraction objects can
        contain more information than a flt, this closure behavior can lose
        information.  

    - Attributes common to flt and cpx
        - f:  The interactive python interpreter (REPL) and debugger use
          repr() for the default string interpolation of values.  When
          using these tools, set the flt or cpx instance's f attribute to
          True.  This interchanges the output of the repr() and str() functions,
          letting you see the limited digits string form in the interpreter and
          debugger.
        - c:  Set the c attribute to True and ANSI escape codes will be
          used to color the output to the terminal when str() or repr() are
          called, letting you use color to identify flt and cpx values.
          This works in typical UNIX terminals, but you'll need to modify
          the color.py module to get it to work in Windows.
        - eng:  Returns the engineering interpolation of the number.
        - h:  Returns a help string useful in the debugger and python REPL.
        - r:  Returns repr() regardless of the f attribute.
        - s:  Returns str() regardless of the f attribute.
        - sci:  Returns the number in scientific notation.
        - sigcomp:  Sets the number of digits to compare for equality.
          Each value is rounded to this value before comparison.
        - t:  Returns a date/time string.  While not a floating point
          computation tool, I often use this during computations.
        - rtz:  If True, remove trailing zeros in interpolated strings.
        - rtdp:  If True, remove a trailing radix (decimal point) if it is
          the last character in an interpolation.
        - rlz:  If True, remove a leading zero.  Thus, if x = flt(1/4) and
          x.rlz is True, then str(x) will be ".25".
        - u:  Use Unicode characters in eng/sci string interpolation.  If 
          x = flt(1e5*pi), then x.eng is "3.14✕10⁵" if x.u is True.

      - Attributes of cpx
        - rad:  If True, use radians for angle in polar form, degrees if
          False.
        - real:  Real part
        - imag:  Imaginary part
        - i:  If True, use "a+bi" str() form
        - p:  If True, use polar form
        - nz:  If True, don't show zero components
 
    - Factory behavior:  You can call a flt or cpx instance with an
      argument suitable for their constructors and you'll get another
      instance of that type.  If a flt has a nonzero n attribute, it is
      copied into the new instance.

    - Delegator:  A Delegator object ensures the proper math/cmath
      functions are called.  Thus, you can call sin(0.1) and sin(0.1j) and
      not get an exception.  Similarly, sqrt(2) and sqrt(-2) work.  

'''
 
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright © 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> This module provides the flt/cpx types for calculations
        # with numbers derived from measurements.  flt is derived from float
        # and cpx from complex.  Their most useful feature is to only show
        # a few digits in their string interpolations so that you don't see
        # lots of digits with no real information.
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard library modules
        from collections import deque
        from collections.abc import Iterable
        from fractions import Fraction
        import cmath
        import decimal
        import locale
        import math
        import numbers
        import operator
        import pathlib
        import re
        import sys
        import threading
        import time
        if 0:
            import debug
            debug.SetDebugger()
    # Custom imports
        from wrap import dedent
        from color import TRM as t
        import fmt
        try:
            import uncertainties
            have_unc = True
        except ImportError:
            have_unc = False
    # Global variables
        Lock = threading.Lock()
        D = decimal.Decimal
        P = pathlib.Path
        ii = isinstance
        __all__ = "Base flt cpx".split()
        # This can be True when a formatter class is written
        _have_Formatter = True

class Base(object):
    'Items common to flt and cpx classes'
    _digits = 3         # Number of digits for str()
    _sigcomp = None     # Number of digits for comparisons
    _dp = locale.localeconv()["decimal_point"]
    _flip = False       # If True, interchange str() and repr()
    _fmt = fmt.Fmt()    # Formatter for flt
    _color = False      # Allow ANSI color codes in str() & repr()
    _flt_color = t("yel")
    _cpx_color = t("sky")
    _rlz = False        # Remove leading zero if True
    _rtz = True         # Remove trailing zeros if True
    _rtdp = True        # Remove trailing decimal point
    _uni = False        # Use Unicode for sci/eng
    _lock = True        # Use lock for context management
    # The following values duplicate the default behavior of floats
    _low = 1e-5         # When to switch to scientific notation
    _high = 1e16        # When to switch to scientific notation
    if 1:   # Context manager methods
        def __enter__(self):
            # Save our important attributes in the base & cls dicts
            if Base._lock:
                Lock.acquire()
            du = "__"
            def Keep(s, A):
                'Return True if this attribute should be kept'
                if i.startswith(du) and i.endswith(du):
                    return False
                if "function" in str(A[i]) or "property" in str(A[i]):
                    return False
                if "staticmethod" in str(A[i]):
                    return False
                return True
            base, cls = {}, {}
            B = Base.__dict__
            for i in B:
                if Keep(i, B):
                    base[i] = B[i]
            S = flt.__dict__ if ii(self, flt) else cpx.__dict__
            for i in S:
                if Keep(i, S):
                    cls[i] = S[i]
            self.base = base
            self.cls = cls
        def __exit__(self, exc_type, exc_val, exc_tb):
            # Restore our important attributes
            B = Base.__dict__
            for i in self.base:
                exec(f"Base.{i} = self.base[i]")
            S = flt.__dict__ if ii(self, flt) else cpx.__dict__
            name = "flt" if ii(self, flt) else "cpx"
            for i in self.cls:
                exec(f"{name}.{i} = self.cls[i]")
            if Base._lock:
                Lock.release()
            return False
    if 1:   # Other methods
        def _reset(self):
            '''Set to a default state.  This is primarily aimed at setting
            things up for self tests.
            '''
            Base._digits = 3         # Number of digits for str()
            Base._sigcomp = None     # Number of digits for comparisons
            Base._dp = locale.localeconv()["decimal_point"]
            Base._flip = False       # If True, interchange str() and repr()
            Base._fmt = fmt.Fmt()    # Formatter for flt
            Base._fmt.n = Base._digits
            Base._color = False      # Allow ANSI color codes in str() & repr()
            Base._flt_color = t("yel")
            Base._cpx_color = t("lav")
            Base._rlz = False        # Remove leading zero if True
            Base._rtz = True         # Remove trailing zeros if True
            Base._rtdp = True        # Remove trailing decimal point
            Base._uni = False        # Use Unicode for eng/sci
            Base._lock = True        # Use lock for context management
            # The following values duplicate the default behavior of floats
            Base._low = 1e-5         # When to switch to scientific notation
            Base._high = 1e16        # When to switch to scientific notation
        def _check(self):
            'Make sure Base._digits is an integer >= 0 or None'
            if not ii(Base._digits, int):
                raise TypeError("Base._digits is not an integer")
            if Base._digits is not None:
                if Base._digits < 0:
                    raise TypeError("Base._digits must be None or an int >= 0")
        def _r(self):
            raise RuntimeError("Base class method should be overridden")
        def _s(self):
            raise RuntimeError("Base class method should be overridden")
        def __add__(self, other):
            return self._do_op(other, operator.add)
        def __sub__(self, other):
            return self._do_op(other, operator.sub)
        def __mul__(self, other):
            return self._do_op(other, operator.mul)
        def __truediv__(self, other):
            return self._do_op(other, operator.truediv)
        def __neg__(self):
            if ii(self, (flt, cpx)):
                return self(-float(self))
            else:
                raise RuntimeError("Bug in logic")
    if 1:   # Static methods
        @staticmethod
        def wrap(string, number, force=None):
            'Put ANSI color escape codes around the string'
            if not number.c:
                return string
            o = []
            use_flt = force is not None and force == flt
            use_cpx = force is not None and force == cpx
            if use_flt or ii(number, flt):
                o.append(Base._flt_color)
                o.append(string)
                o.append(t.n)
                return ''.join(o)
            elif use_cpx or ii(number, cpx):
                o.append(Base._cpx_color)
                o.append(string)
                o.append(t.n)
                return ''.join(o)
            else:
                return string
        @staticmethod
        def opname(op):
            "Return the short name of the operator module's function op"
            if not hasattr(Base.opname, "r"):
                Base.opname.r = re.compile(r"^<built-in function (.+)>$")
            mo = Base.opname.r.match(str(op))
            name = mo.groups()[0] if mo else str(op)
            return name
        @staticmethod
        def binary_op(a, b, op):
            '''Handle the binary operation op(a, b).  a and b can be any
            numerical type that operate with flt and cpx; one of them 
            must be a flt or cpx.
    
            Return either a flt or cpx.
            '''
            def GetResult(type_a, type_b, type_result):
                type_result(op(type_a(a), type_b(b)))
            if ii(a, flt):
                if ii(b, flt):
                    return GetResult(float, float, flt)
                elif ii(b, (complex, cpx)):
                    return GetResult(float, complex, cpx)
                else:
                    return GetResult(float, float, flt, promote=needs_promotion)
            elif ii(a, cpx):
                if ii(b, flt):
                    return GetResult(complex, float, cpx)
                elif ii(b, (complex, cpx)):
                    return GetResult(complex, complex, cpx)
                else:
                    return GetResult(complex, float, cpx, promote=needs_promotion)
            else:
                type_a = complex if ii(a, complex) else float
                if ii(b, flt):
                    if type_a == complex:
                        return GetResult(type_a, float, cpx)
                    else:
                        return GetResult(type_a, float, flt)
                elif ii(b, cpx):
                    return GetResult(type_a, complex, cpx)
                else:
                    raise RuntimeError("At least one of a or b must be flt or cpx")
        @staticmethod
        def sig_equal(a, b, n=None):
            '''Return True if objects a and b are equal to the indicated
            number of digits.  a and b must both be a flt or cpx.
            '''
            def Round(x):
                y = D(repr(float(x)))
                with decimal.localcontext() as ctx:
                    ctx.prec = n    # Round to n digits
                    y = +y
                return y
            n = a.N if n is None else n
            n = max(1, min(n, 15))  # Clamp n to [1, 15]
            if ii(a, flt) and ii(b, flt):
                return Round(a) == Round(b)
            elif ii(a, cpx) and ii(b, cpx):
                a_re, a_im = Round(a.real), Round(a.imag)
                b_re, b_im = Round(b.real), Round(b.imag)
                return (a_re == b_re) and (a_im == b_im)
            else:
                raise TypeError("a and b must both be flt or cpx")
    if 1:   # Read-only properties
        @property
        def h(self):
            'Return help string'
            return self.help()
        @property
        def r(self):    # Returns repr() regardless of self.f
            'Return the repr() string, regardless of self.f'
            return self._r()
        @property
        def s(self):    # Returns str() regardless of self.f
            'Return the str() string, regardless of self.f'
            return self._s()
        @property       # Returns date/time string
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
    if 1:   # Writable properties
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
        def high(self):
            'Switch to scientific notation when x > Base.high'
            return Base._high
        @high.setter
        def high(self, value):
            Base._high = D(abs(value)) if value is not None else D(0)
        @property
        def low(self):
            'Switch to scientific notation when x < Base.low'
            return Base._low
        @low.setter
        def low(self, value):
            Base._low = D(abs(value)) if value is not None else D(0)
        @property
        def N(self): 
            'How many digits to interpolate to'
            return Base._digits
        @N.setter
        def N(self, value):
            'The value is clamped to be between 1 and 15 digits'
            min_value, max_value = 1, 15
            if value is None:
                value = max_value
            elif not ii(value, int):
                raise ValueError("value must be an integer")
            if value < min_value:
                value = min_value
            elif value > max_value:
                value = max_value
            Base._digits = value
            assert(min_value <= Base._digits <= max_value)
        @property
        def rtdp(self):  # Remove trailing decimal point if True
            'Remove trailing decimal point if True'
            return Base._rtdp
        @rtdp.setter
        def rtdp(self, value):
            Base._rtdp = Base._fmt.rtdp = bool(value)
        @property
        def rlz(self):  # Remove leading zero if True
            'Remove leading zero if True'
            return Base._rlz
        @rlz.setter
        def rlz(self, value):
            Base._rlz = Base._fmt.rlz = bool(value)
        @property
        def rtz(self):  # Remove trailing zeros if True
            'Remove trailing zeros if True'
            return Base._rtz
        @rtz.setter
        def rtz(self, value):
            Base._rtz = Base._fmt.rtz = bool(value)
        @property
        def sigcomp(self):  # Num of digits for == and < comparisons
            '''Significant digits for '==' and '<' comparisons.  If it is
            None, then comparisons are made to full precision.  Otherwise,
            it must be an integer between 1 and 15.
            '''
            return Base._sigcomp
        @sigcomp.setter
        def sigcomp(self, value):
            if value is None:
                self._sigcomp = None
                return
            val = int(value)
            if not (1 <= val <= 15):
                raise ValueError("sigcomp must be between 1 and 15")
            Base._sigcomp = val
        @property
        def u(self):
            return Base._uni
        @u.setter
        def u(self, value):
            Base._uni = bool(value)

class flt(Base, float):
    '''The flt class is a float except that its str() representation is
    limited to the number of digits set in Base.N.  You can change the
    number of digits for a flt instance by changing the n attribute.  Set 
    it to 0 to return to the Base class behavior.
    '''
    def __new__(cls, value):
        if ii(value, str) and "∞" in value:
            value = value.replace("∞", "inf")
        instance = super().__new__(cls, value)
        instance._check()
        # Make sure formatter is set to current value of N
        Base._fmt.n = Base._digits
        # Local number of digits overrides Base.N if not zero
        instance._n = 0     # Instance's number of digits
        return instance
    def _s(self, fmt="fix", no_color=False):    # flt
        'Return the rounded string representation'
        if fmt not in set("fix eng sci engsi engsic".split()):
            raise ValueError("fmt must be one of:  fix, eng, sci, engsi, engsic")
        self._check()
        if not Base._digits:
            return str(float(self))
        def decorate(x):
            return x if no_color else Base.wrap(x, self)
        x = D(self)
        n = self._n if self._n else Base._digits 
        if n is None:
            n = 15
        if x == inf:
            return "∞"
        elif x == -inf:
            return "-∞"
        elif str(x) == "NaN":
            return "nan"
        if 1:
            # Set Base._fmt's state to our current state
            Base._fmt.dp = self._dp
            Base._fmt.high = self._high
            Base._fmt.low = self._low
            Base._fmt.n = self.n if self.n else self.N
            Base._fmt.rtz = self._rtz
            Base._fmt.rtdp = self._rtdp
            Base._fmt.rlz = self._rlz
            Base._fmt.u = self._uni
        if fmt == "fix":
            need_sci = ((x and self.low is not None and abs(x) < self.low) or 
                        (x and self.high is not None and abs(x) > self.high))
            if need_sci:
                s = self._fmt.sci(self, n=n)
            else:
                s = self._fmt.fix(self, n=n)
        elif fmt == "eng":
            s = self._fmt.eng(self, fmt="eng", n=n)
        elif fmt == "engsi":
            s = self._fmt.eng(self, fmt="engsi", n=n)
        elif fmt == "engsic":
            s = self._fmt.eng(self, fmt="engsic", n=n)
        elif fmt == "sci":
            s = self._fmt.sci(self, n=n)
        else:
            raise Exception("Software bug")
        return decorate(s)
    def _r(self, no_color=False):
        'Return the repr string representation'
        self._check()
        def f(x):
            return x if no_color else Base.wrap(x, self, force=flt)
        s = f"{repr(float(self))}"
        if no_color:
            return s
        return f(s)
    def __str__(self):
        return self._r() if Base._flip else self._s()
    def __repr__(self):
        return self._s() if Base._flip else self._r()
    def __hash__(self):
        return hash(float(self._r()))
    def rnd(self, n=None):
        '''Return a flt that is rounded to the current number of digits 
        or n digits if n is not None.
        '''
        with self:
            if n is not None:
                if not ii(n, int) and not (1 <= n <= 15):
                    raise ValueError("n must be an integer between 1 and 15")
                self.N = n
            return flt(self.s)
    def copy(self):
        'Returns a copy of self'
        cp = flt(float(self))
        return cp
    def help(self):
        print(dedent('''
        The flt class is derived from float and has the following attributes:
          c       * ANSI color escape codes in str() and repr()
          eng       Return engineering notation string
          f       * Exchange behavior of str() and repr()
          h         Print this help
          high    * Switch to scientific notation if x > high
          low     * Switch to scientific notation if x < low 
          N       * Number of interpolated digits
          n         Number of interpolated digits for one instance
          r         The repr() string, regardless of f attribute state
          rlz     * Don't print leading zero ("0.25" becomes ".25")
          rtz     * Don't print trailing zeros ("1.00" becomes "1.")
          rtdp    * Don't print trailing radix (decimal point) ("1." becomes "1")
          s         The str() string, regardless of f attribute state
          sci       Return scientific notation string
          sigcomp * Only compare this number of digits for == if not None
          t       * Date and time
          u       * Use Unicode characters in eng/sci string interpolation
             * means the attribute's state affects all flt and cps instances'''[1:]))
    if 1:   # Arithmetic functions
        def _do_op(self, other, op):
            if ii(other, complex):
                return cpx(op(float(self), other))
            return flt(op(float(self), float(other)))
        def __floordiv__(self, other):
            if ii(other, complex):
                raise TypeError("can't take floor of complex number")
            return self._do_op(other, operator.floordiv)
        def __mod__(self, other):
            if not ii(other, flt):
                raise TypeError("Second operand must be a flt")
            rem = abs(float(self) % float(other))
            assert(0 <= rem <= abs(other))
            rem *= -1 if other < 0 else 1
            return rem
        def __divmod__(self, other):
            '''Return (q, rem) where q is how many integer units of other are in
            self and rem is a flt giving the remainder.
            '''
            if not ii(other, flt):
                raise TypeError("Second operand must be a flt")
            # See python-3.7.4-docs-html/library/functions.html#divmod
            q = math.floor(float(self)/float(other))
            rem = self % other
            return q, flt(rem)
        def __pow__(self, other):
            'self**other'
            return self._do_op(other, operator.pow)
        def __radd__(self, other):
            'other + self'
            return self + other
        def __rsub__(self, other):
            'other - self'
            if ii(other, (flt, cpx)):
                return other.__add__(-self)
            return -self + other
        def __rmul__(self, other):
            'other*self'
            return self*other
        def __rtruediv__(self, other):
            'other/self'
            return operator.truediv(flt(1), self)*other
        def __rfloordiv__(self, other):
            'other//self'
            return flt(floor((flt(1)/self)*other))
        def __rmod__(self, other):
            'other % self'
            return self.__mod__(other, self)
        def __rdivmod__(self, other):
            'divmod(other, self)'
            return self.__divmod__(other, self)
        def __rpow__(self, other):
            'Calculate other**self'
            return pow(other, self)
        def __abs__(self):
            return flt(abs(float(self)))
        def __ne__(self, other):
            return not (self == other)
        def __eq__(self, other):
            '''To be equal, two flt objects must be numerically equal.
            If the sigcomp attribute is defined, it defines the number of
            digits involved in the comparison.
            '''
            n = self.sigcomp if self.sigcomp is not None else 15
            b = flt(float(other))
            return Base.sig_equal(self, b, n=n)
        def __lt__(self, other):
            if ii(other, complex):
                raise ValueError("Complex numbers are not ordered")
            return float(self) < float(other)
        def __call__(self, x):
            '''Factory function for a flt.  If x is a flt and has the n
            attribute set to nonzero, the returned flt has the same value
            of n.
            '''
            y = flt(x)
            if ii(x, flt) and self.n:
                y.n = self.n
            return y
    if 1:   # Properties
        @property
        def n(self):
            "This instance's number of digits"
            return self._n
        @n.setter
        def n(self, value):
            if not ii(value, int):
                raise TypeError(f"{value!r} must be an integer")
            if not (0 <= value <= 15):
                raise ValueError(f"value must be >= 0 and <= 15")
            self._n = value
    if 1:   # Formatting properties
        @property
        def eng(self):
            'Return a string formatted in engineering notation'
            return self._s(fmt="eng")
        @property
        def engsi(self):
            '''Return a string formatted in engineering notation with SI
            prefix appended with a space character.
            '''
            return self._s(fmt="engsi")
        @property
        def engsic(self):
            '''Return a string formatted in engineering notation with SI
            prefix appended with no space character.
            '''
            return self._s(fmt="engsic")
        @property
        def sci(self):
            'Return a string formatted in scientific notation'
            return self._s(fmt="sci")

class ParseComplex(object):
    '''Parses complex numbers in the ways humans like to write them.
    Instantiate the object, then call it with the string to parse; the
    real and imaginary parts are returned as a tuple.  You can pass in a
    number type to the constructor (you can also use fractions.Fraction)
    and the returned tuple will be composed of that type of number.
    '''
    _cre = r'''
        %s                          # Match at beginning
        ([+-])%s                    # Optional leading sign
        %s                          # Placeholder for imaginary unit
        (\.\d+|\d+\.?|\d+\.\d+)     # Required digits and opt. decimal point
        (e[+-]?\d+)?                # Optional exponent
        %s                          # Match at end
    '''
    # Pure imaginary, xi or ix
    _I1 = _cre % ("^", "?", "", "[ij]$")
    _I2 = _cre % ("^", "?", "[ij]", "$")
    # Reals
    _R = _cre % ("^", "?", "", "$")
    # Complex number:  x+iy
    _C1 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "", "[ij]$"))
    # Complex number:  x+yi
    _C2 = (_cre % ("^", "?", "", "")) + (_cre % ("", "", "[ij]", "$"))
    # Complex number:  iy+x
    _C3 = (_cre % ("^", "?", "[ij]", "")) + (_cre % ("", "?", "", "$"))
    # Complex number:  yi+x
    _C4 = (_cre % ("^", "?", "", "[ij]")) + (_cre % ("", "?", "", "$"))
    # Regular expressions (flags:  re.I ignores case, re.X allows verbose)
    _imag1 = re.compile(_I1, re.X | re.I)
    _imag2 = re.compile(_I2, re.X | re.I)
    _real = re.compile(_R, re.X | re.I)
    _complex1 = re.compile(_C1, re.X | re.I)
    _complex2 = re.compile(_C2, re.X | re.I)
    _complex3 = re.compile(_C3, re.X | re.I)
    _complex4 = re.compile(_C4, re.X | re.I)
    def __init__(self, number_type=flt):
        self.number_type = number_type
    def __call__(self, s):
        '''Return a tuple of two real numbers representing the real
        and imaginary parts of the complex number represented by
        the strings.  The allowed forms are (x and y are real 
        numbers):
            Real:               x
            Pure imaginary      iy, yi
            Complex             x+iy, x+yi
        Space characters are allowed in the s (they are removed before
        processing).
        '''
        nt = self.number_type
        # Remove any whitespace, use lowercase, and change 'j' to 'i'
        s = re.sub(r"\s+", "", s).lower().replace("j", "i")
        # Imaginary unit is a special case
        if s in ("i", "+i"):
            return nt(0), nt(1)
        elif s in ("-i",):
            return nt(0), nt(-1)
        # "-i+3", "i+3" are special cases
        if s.startswith("i") or s.startswith("-i") or s.startswith("+i"):
            li = s.find("i")
            if s[li + 1] == "+" or s[li + 1] == "-":
                rp = nt(s[li + 1:])
                ip = -nt(1) if s[0] == "-" else nt(1)
                return rp, ip
        # "n+i", "n-i" are special cases
        if s.endswith("+i") or s.endswith("-i"):
            if s.endswith("+i"):
                return nt(s[:-2]), 1
            else:
                return nt(s[:-2]), -1
        # Parse with regexps
        mo = ParseComplex._imag1.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._imag2.match(s)
        if mo:
            return nt(0), self._one(mo.groups())
        mo = ParseComplex._real.match(s)
        if mo:
            return self._one(mo.groups()), nt(0)
        mo = ParseComplex._complex1.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex2.match(s)
        if mo:
            return self._two(mo.groups())
        mo = ParseComplex._complex3.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        mo = ParseComplex._complex4.match(s)
        if mo:
            return self._two(mo.groups(), flip=True)
        raise ValueError("'%s' is not a proper complex number" % s)
    def _one(self, groups):
        s = ""
        for i in range(3):
            if groups[i]:
                s += groups[i]
        return self.number_type(s)
    def _two(self, groups, flip=False):
        nt = self.number_type
        s1 = self._one(groups)
        s2 = ""
        for i in range(3, 6):
            if groups[i]:
                s2 += groups[i]
        if flip:
            return nt(s2), nt(s1)
        else:
            return nt(s1), nt(s2)

class cpx(Base, complex):
    '''The cpx class is a complex except that its components are flt
    numbers.
    '''
    _i = False      # If True, use "i" instead of "j" in str()
    _p = False      # If True, use polar representation in str()
    _rad = False    # If True, use radians for angle measurement (degrees if False)
    _nz = False     # If True, don't print out zero components
    _PC = ParseComplex()
    _t = False      # If True, use tuple display:  1+2i -> "(1,2)"
    _w = False      # If True, use wide display:  1+2i -> "1 + 2i"
    def __new__(cls, real, imag=0):
        'real can be a number type, a cpx, or a complex.'
        def f(x):
            return D(x) if x else D(0)
        if ii(real, (int, float, flt, D)):
            imag = 0 if imag is None else imag
            re, im = float(real), float(imag)
            instance = super().__new__(cls, re, im)
        elif ii(real, cpx):
            re, im = real._real, real._imag
            instance = super().__new__(cls, re, im)
        elif ii(real, numbers.Complex):
            re, im = real.real, real.imag
            instance = super().__new__(cls, re, im)
        elif ii(real, str):
            if "i" in real:
                real = real.replace("i", "j")
            if "j" in real:
                if ii(imag, str):
                    raise ValueError("Can't use 'i' or 'j' and give imag number")
                else:
                    # Use ParseComplex to recognize the complex string
                    re, im = cpx._PC(real)
                    instance = super().__new__(cls, re, im)
            else:
                re, im = float(real), float(imag)
                instance = super().__new__(cls, re, im)
        else:
            raise TypeError("Unexpected type for real argument")
        # Make components flt instances
        instance._real = flt(f(re))
        instance._imag = flt(f(im))
        return instance
    def _reset(self):
        'Set things to a known state (primarily for self tests)'
        super()._reset()
        cpx._i = False
        cpx._nz = False
        cpx._p = False
        cpx._rad = False
        cpx._t = False
        cpx._w = False
    def _pol(self, repr=False):
        'Return polar form'
        def f(x):
            return Base.wrap(x, self)
        r, theta = [flt(i) for i in polar(self)]
        theta *= 1 if self.rad else 180/pi
        deg = "" if self.rad else "°"
        sp = " " if self.w else ""
        if repr:
            s = f"{r._r(no_color=True)}{sp}∠{sp}{theta._r(no_color=True)}{deg}"
        else:
            s = f"{r._s(no_color=True)}{sp}∠{sp}{theta._s(no_color=True)}{deg}"
        t = f(s) if self.i else f("(" + s + ")")
        return f(t)
    def _s(self, fmt="fix"):   
        '''Return the rounded string representation.  If cpx.i is True,
        then "i" is used as the unit imaginary and no parentheses are
        placed around the string.  If cpx.p is False, use rectangular;
        if True, use polar coordinates.
        '''
        if fmt not in set("fix eng sci engsi engsic".split()):
            raise ValueError("fmt must be one of:  fix, eng, sci, engsi, engsic")
        def f(x):
            return Base.wrap(x, self)
        if self.p:      # Polar coordinates
            return self._pol()
        elif self.t:    # Tuple form
            r, i = self._real, self._imag
            re = r._s(fmt=fmt, no_color=True)
            im = i._s(fmt=fmt, no_color=True)
            sp = " " if self.w else ""
            s = f"({re},{sp}{im})"
            return f(s)
        else:           # Rectangular coordinates
            r, i = self._real, self._imag
            re = r._s(fmt=fmt, no_color=True)
            im = i._s(fmt=fmt, no_color=True)
            if self.nz and ((r and not i) or (not r and i)):
                if r:
                    s = f"{re}" if cpx._i else f"({re})"
                else:
                    s = f"{im}i" if cpx._i else f"({im}j)"
            elif self.nz and not r and not i:
                s = "0"
            else:
                iu = "i" if cpx._i else "j"
                sp = " " if self.w else ""
                sgn = f"{sp}-{sp}" if i < 0 else f"{sp}+{sp}"
                im = abs(i)._s(fmt=fmt, no_color=True)
                if cpx._i:
                    s = f"{re}{sgn}{im}{iu}"
                else:
                    s = f"({re}{sgn}{im}{iu})"
            return f(s)
    def _r(self):  
        'Return the full representation string'
        def f(x):
            return Base.wrap(x, self, force=cpx)
        if self.p:
            s = self._pol(repr=True)
        else:
            re, im = float(self._real), float(self._imag)
            II = "i" if self.i else "j"
            if self.nz:
                s = []
                if re:
                    s.append(f"{re!r}")
                if im:
                    if s:
                        s.append("+" if im > 0 else "")
                    s.append(f"{im!r}")
                    s.append(II)
                t = f"{''.join(s)}"
                s = t
            else:
                r = f"{float(self._real)!r}"
                i = f"{float(self._imag)!r}"
                sgn = "+" if self._imag >= 0 else ""
                s = f"{r}{sgn}{i}{II}"
        return f(s)
    def __str__(self): 
        return self._r() if Base._flip else self._s()
    def __repr__(self):
        return self._s() if Base._flip else self._r()
    def __hash__(self):
        return hash(complex(self))
    def copy(self):
        'Return a copy of self'
        return cpx(complex(self))
    def help(self):
        return print(dedent('''
        The cpx class is derived from complex and has the following attributes in
        addition to those of flt:
          i       * Use 'i' instead of 'j' as the imaginary unit
          imag      Return the imaginary component
          nz      * Don't print zero components if True
          p       * Display in polar coordinates
          rad     * Display polar angle in radians
          real      Return the real component
             * means these attributes affect all cpx instances'''[1:]))
    def __call__(self, z):   
        'Factory function for a cpx'
        return cpx(z)
    if 1:   # Arithmetic functions
        def _do_op(self, other, op):   
            return cpx(op(complex(self), complex(other)))
        def __complex__(self): 
            return complex(self._real, self._imag)
        def __truediv__(self, other):  
            return self._do_op(other, operator.truediv)
        def __pow__(self, other):  
            return self._do_op(other, operator.pow)
        def __radd__(self, other): 
            return cpx(complex(other) + complex(self))
        def __rsub__(self, other): 
            return cpx(complex(other) - complex(self))
        def __rmul__(self, other): 
            return cpx(complex(other)*complex(self))
        def __rtruediv__(self, other): 
            return cpx(complex(other)/complex(self))
        def __rpow__(self, other): 
            return cpx(complex(other)**complex(self))
        def __neg__(self): 
            return cpx(-complex(self))
        def __pos__(self): 
            return cpx(complex(self))
        def __abs__(self): 
            return flt(abs(complex(self)))
        def __eq__(self, other):   
            '''If the sigcomp attribute is defined, it defines the number of
            digits involved in the comparison.
            '''
            n = self.sigcomp if self.sigcomp is not None else 15
            b = cpx(complex(other))
            return Base.sig_equal(self, b, n=n)
        def __ne__(self, other):   
            return not (self == other)
    if 1:   # Read-only properties
        @property
        def real(self):
            return self._real
        @property
        def imag(self):
            return self._imag
    if 1:   # Writable properties
        @property
        def i(self):   
            'Return boolean that indicates using "i" instead of "j"'
            return cpx._i
        @i.setter
        def i(self, value):
            'Set boolean that indicates using "i" instead of "j"'
            cpx._i = bool(value)
        @property
        def nz(self):  
            '''Return boolean that indicates don't print out zero components'''
            return cpx._nz
        @nz.setter
        def nz(self, value):   
            '''Set boolean that indicates don't print out zero components'''
            cpx._nz = bool(value)
        @property
        def p(self):   
            'If True, use polar coordinates; if False, use rectangular'
            return cpx._p
        @p.setter
        def p(self, value):
            cpx._p = bool(value)
        @property
        def rad(self): 
            'If True, use radians in polar form'
            return cpx._rad
        @rad.setter
        def rad(self, value):  
            cpx._rad = bool(value)
        @property
        def t(self): 
            'If True, use tuple display form 1+3i --> "(1,3)"'
            return cpx._t
        @t.setter
        def t(self, value):  
            cpx._t = bool(value)
        @property
        def w(self): 
            'If True, use wide display form 1+3i --> "1 + 3i"'
            return cpx._w
        @w.setter
        def w(self, value):  
            cpx._w = bool(value)
    if 1:   # Formatting properties
        @property
        def eng(self): 
            'Return a string formatted in engineering notation'
            return self._s(fmt="eng")
        @property
        def engsi(self):  
            '''Return a string formatted in engineering notation with SI
            prefix appended with a space character.
            '''
            return self._s(fmt="engsi")
        @property
        def engsic(self): 
            '''Return a string formatted in engineering notation with SI
            prefix appended with no space character.
            '''
            return self._s(fmt="engsic")
        @property
        def sci(self): 
            'Return a string formatted in scientific notation'
            return self._s(fmt="sci")
    
if 1:   # Get math/cmath functions into this namespace
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
        # The following strings can be used to decorate the names with
        # e.g. ANSI escape codes for color
        _left = "«"
        _right = "»"
        def __init__(self, name):
            self.name = name
        def __str__(self):
            return f"{Delegator._left}{self.name}{Delegator._right}"
        def __call__(self, *args, **kw):
            C = (complex, cpx)
            if hasattr(math, self.name) and not hasattr(cmath, self.name):
                # Forces a math call
                s = f"math.{self.name}(*args, **kw)"
            elif not hasattr(math, self.name) and hasattr(cmath, self.name):
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
            result = None
            try:
                result = eval(s)
            except AttributeError as err:
                raise TypeError(err) from None
            except TypeError as err:
                raise 
            except ValueError as err:
                if str(err) == "math domain error":
                    # This can happen with e.g. asin(2) where you need
                    # to use the cmath version to get a complex result.
                    # The argument is a float, but the result is a
                    # complex and this case won't be detected by the
                    # above tests.
                    if self.name in "asin acos".split():
                        # Try using cmath
                        result = eval("c" + s)
                    else:
                        raise
                else:
                    raise
            except OverflowError as err:
                raise
            except Exception as err:
                print(f"Unhandled exception in f.py's Delegator:\n  '{err!r}'")
                print("Dropping into debugger")
                breakpoint()
                pass
            if ii(result, int):
                return result
            elif ii(result, (float, flt)):
                return flt(result)
            elif ii(result, C):
                return cpx(result)
            else:
                if self.name == "polar":
                    result = tuple([flt(i) for i in result])
                elif self.name == "frexp":
                    result = flt(result[0]), result[1]
                elif self.name == "modf":
                    result = flt(result[0]), flt(result[1])
                return result
        @staticmethod
        def iscomplex(*args, **kw):
            '''Return True if any argument or keyword argument is
            complex.  If arg[0] is an iterator, also look for complex
            numbers in it.
            '''
            C = (complex, cpx)
            def cc(x):
                return any([ii(i, C) for i in x])
            if cc(list(args) + list(kw.values())):
                return True
            if len(args) == 1:
                if not ii(args[0], str) and ii(args[0], Iterable):
                    return cc(args[0])
            return False
    # All math/cmath function names for python version 3.9.4
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
            __all__.append(name)
    # Constants
    #   both:  e inf nan pi tau
    #   cmath: infj nanj 
    from math import e, inf, nan, pi, tau
    from cmath import infj, nanj
    # Change constants' type to flt
    constants = "e pi tau".split()
    for i in constants:
        exec(f"{i} = flt({i})")
    # Add these names to __all__
    __all__.extend("e inf nan pi tau infj nanj".split())
if 1:   # Other
    def GetNumDigits(s, inttzsig=False):
        '''Return the number of digits in the string s which represents
        either a base 10 integer or a floating point number.  If inttzsig
        is True and s represents an integer, then trailing zeros of s are
        not removed, meaning they contain real information.
        '''
        e = ValueError("'{}' is an illegal number form".format(s))
        dp = locale.localeconv()["decimal_point"]
        def RemoveSign(str):
            if str and str[0] in "+-":
                return str[1:]
            return str
        def rtz(s):     # Remove trailing zeros from string s
            dq = deque(s)
            while len(dq) > 1 and dq[-1] == "0":
                dq.pop()
            return ''.join(dq)
        def rlz(s):   # Remove leading zeros
            dq = deque(s)
            while len(dq) > 1 and dq[0] == "0" and not dq[-1] == dp:
                dq.popleft()
            return ''.join(dq)
        def Normalize(s):
            '''Remove any uncertainty, spaces, sign, and exponent and return
            the significand.
            '''
            t = s.replace(" ", "")
            # Remove any exponent portion
            if "e" in t:
                try:
                    left, right = s.split("e")
                except ValueError:
                    raise e
                t = left
            if not t:
                raise e
            t = RemoveSign(t)
            if t.count(dp) > 1:
                raise e
            return t
        #------------------------------------------------
        if not isinstance(s, str):
            raise ValueError("Argument must be a string")
        t = Normalize(s.lower().strip())
        if dp not in t:
            # It's an integer
            t = str(int(t))
            return len(t) if inttzsig else len(rtz(t))
        # It's a float
        try:
            # It's valid if it can be converted to a Decimal
            D(t)
        except Exception:
            raise e
        t = rlz(t)  # Remove leading zeros up to the first nonzero digit or "."
        t = t.replace(dp, "")  # Remove decimal point
        # Remove any leading zeros but only if the string is not all zeros
        if set(t) != set("0"):
            t = rlz(t)
        return len(t)

if 1:   # Classes derived from flt for physical data
    class Nothing(flt):
        '''Represent a 'None' number.  Can be initialized with None, 
        "None" (case insensitive), or "".
        '''
        def __new__(cls, arg):
            if ii(arg, str):
                assert(arg.lower() == "none" or not arg)
            else:
                assert(arg == None)
            instance = super().__new__(cls, 0)
            instance.arg = arg
            return instance
        def __str__(self):
            return "--"
        def __repr__(self):
            return f"Nothing({self.arg!r})"
    class Unk(flt):
        '''Represent an unknown number.  Always return '?' for str or repr.
        Constructor argument must be a single question mark or equivalent
        Unicode character.  The numerical value is deliberately NaN so that
        calculations with it won't succeed.
        '''
        def __new__(cls, arg):
            assert(ii(arg, str))
            c = arg.strip()
            if c:
                assert(len(c) == 1 and c in set("?¿⁇❓❔⸮︖﹖？"))
            instance = super().__new__(cls, "NaN")
            return instance
        def __str__(self):
            return "?"
        def __repr__(self):
            return "Unk('?')"
    class Approx(flt):
        '''Represent an approximate number.  Prepends "≈" to str.
        The first character must be one of '~≈≅'; the remainder is the
        number string.
        '''
        def __new__(cls, arg):
            first_char = arg[0]
            assert(first_char in set("~≈≅"))
            instance = super().__new__(cls, arg[1:])
            instance.arg = arg
            instance.fc = "≈"
            return instance
        def __str__(self):
            return self.fc + super().__str__()
        def __repr__(self):
            return f"Approx({self.arg!r})"
    class Rng(flt):
        'Represent a range'
        def __new__(cls, a, b):
            assert(ii(a, str) and ii(b, str))
            if a[0] in set("~≈≅"):
                # Is approximate, but ignore, as it's already approximate
                x, y = flt(a[1:]), flt(b)
            else:
                x, y = flt(a), flt(b)
            val = (x + y)/2     # Value is midpoint of interval
            instance = super().__new__(cls, val)
            instance.rng = (x, y) if x <= y else (y, x)
            return instance
        def __str__(self):
            a, b = self.rng
            return f"[{a},{b}]"
        def __repr__(self):
            a, b = self.rng
            return f"Rng({a}, {b})"
    class LessThan(flt):
        'Represent a number <x or ≤x'
        def __new__(cls, arg):
            chars = set("<≪⋘﹤＜≤≦⋜")
            assert(arg and arg[0] in chars)
            instance = super().__new__(cls, arg[1:].replace(" ", ""))
            instance.arg = arg
            instance.char = arg[0]
            return instance
        def __str__(self):
            return self.char + super().__str__()
        def __repr__(self):
            return f"LessThan({self.arg!r})"
    class GreaterThan(flt):
        'Represent a number >x or ≥x'
        def __new__(cls, arg):
            chars = set(">≫⋙﹥＞≥≧⋝")
            assert(arg and arg[0] in chars)
            instance = super().__new__(cls, arg[1:].replace(" ", ""))
            instance.arg = arg
            instance.char = arg[0]
            return instance
        def __str__(self):
            return self.char + super().__str__()
        def __repr__(self):
            return f"GreaterThan({self.arg!r})"
    class Unc(flt):
        '''Represent an uncertain number.  If the python uncertainties
        library is available, it is used for the convenient display of 
        uncertain numbers in the abbreviated 1.23(4) style.  Otherwise, the
        "nominal_value ± uncertainty" form is used.
 
        The property s is the uncertainty.
  
        Initialize the constructor with strings of the form 
            1) "3.4±0.1"
        If you have the python uncertainties library, you can also use:
            2) "3.4(1)"
            3) "3.4+/-0.1"
        '''
        def __new__(cls, u):
            'Our floating point value is the nominal value'
            r = u.replace(" ", "")
            if have_unc:
                v = uncertainties.ufloat_fromstr(r)
                instance = super().__new__(cls, v.n)
                instance.sd = float(v.s)
            else:
                n, s = [float(i) for i in r.split("±")]
                instance = super().__new__(cls, n)
                instance.sd = s
            instance.str = u
            return instance
        def __str__(self):
            if have_unc:
                u = uncertainties.ufloat(float(self), self.sd)
                return f"{u:uS}"
            else:
                return super().__str__() + "±" + str(self.sd)
        def __repr__(self):
            return f"Unc('{self.str}')"
        @property
        def s(self):
            return self.sd

if __name__ == "__main__": 
    from lwtest import run, raises, assert_equal, Assert
    eps = 1e-15
    def Equal(a, b, reltol=eps):
        'Return True if a == b within the indicated tolerance'
        if not a and not b:
            return True
        if ii(a, flt) and ii(b, flt):
            diff = abs(float(a) - float(b))
            if float(a):
                reldiff = abs(diff/float(a))
            elif float(b):
                reldiff = abs(diff/float(b))
            return reldiff <= reltol
        elif ii(a, cpx) and ii(b, cpx):
            # Real part
            realdiff = abs(float(a.real) - float(b.real))
            if float(a.real):
                reldiff = abs(realdiff/float(a.real))
            elif float(b):
                reldiff = abs(realdiff/float(b.real))
            else:
                reldiff = realdiff
            if reldiff > reltol:
                return False
            # Imaginary part
            imagdiff = abs(float(a.imag) - float(b.imag))
            if float(a.imag):
                reldiff = abs(imagdiff/float(a.imag))
            elif float(b.imag):
                reldiff = abs(imagdiff/float(b.imag))
            else:
                reldiff = imagdiff
            if reldiff > reltol:
                return False
            return True
        else:
            raise TypeError("Both a and b must be flt or cpx")
    def Test_flt_derivatives():
        # Nothing
        x = Nothing("")
        Assert(str(x) == "--")
        Assert(repr(x) == "Nothing('')")
        x = Nothing("nOnE")
        Assert(str(x) == "--")
        Assert(repr(x) == "Nothing('nOnE')")
        x = Nothing(None)
        Assert(str(x) == "--")
        Assert(repr(x) == "Nothing(None)")
        # Unk
        x = Unk("")
        Assert(str(x) == "?")
        Assert(repr(x) == "Unk('?')")
        # Approx
        x = Approx("~1.2")
        Assert(x == 1.2)
        Assert(str(x) == "≈1.2")
        Assert(repr(x) == "Approx('~1.2')")
        x = Approx("≈1.2")
        Assert(x == 1.2)
        Assert(str(x) == "≈1.2")
        Assert(repr(x) == "Approx('≈1.2')")
        x = Approx("≅1.2")
        Assert(x == 1.2)
        Assert(str(x) == "≈1.2")
        Assert(repr(x) == "Approx('≅1.2')")
        # Rng
        x = Rng("1", "2")
        Assert(x == 1.5)
        Assert(str(x) == "[1,2]")
        Assert(repr(x) == "Rng(1, 2)")
        x = Rng("2", "1")
        Assert(x == 1.5)
        Assert(str(x) == "[1,2]")
        Assert(repr(x) == "Rng(1, 2)")
        # LessThan
        x = LessThan("<3.5")
        Assert(x == 3.5)
        Assert(str(x) == "<3.5")
        Assert(repr(x) == "LessThan('<3.5')")
        x = LessThan("≤3.5")
        Assert(x == 3.5)
        Assert(str(x) == "≤3.5")
        Assert(repr(x) == "LessThan('≤3.5')")
        # GreaterThan
        x = GreaterThan(">3.5")
        Assert(x == 3.5)
        Assert(str(x) == ">3.5")
        Assert(repr(x) == "GreaterThan('>3.5')")
        x = GreaterThan("≥3.5")
        Assert(x == 3.5)
        Assert(str(x) == "≥3.5")
        Assert(repr(x) == "GreaterThan('≥3.5')")
        # Unc
        s = "3.456 ± 0.0036"
        x = Unc(s)
        Assert(x == 3.456)
        Assert(x.s == 0.0036)
        Assert(str(x) == "3.456(4)")
        Assert(repr(x) == f"Unc('{s}')")

    def Test_sig_equal():
        '''Base.sig_equal compares two numbers to a specified number of
        digits and returns True if they are equal.
        
        The choice of this number for p means there will be no spurious
        rounding of the last digit.  If you choose p == pi, you'll see
        the following tests fail for n = 2, 6, and 9.  For example, for 
        n == 2, you'll see x = 3.14... and y = 3.17...  In the 
        Base.sig_equal function, the two numbers compared will be 
        Decimal('3.1') and Decimal('3.2'), leading to an inequality.
        '''
        p = 1.111111111111111
        for n in range(1, 15):
            eps = 10**-n
            a = 1 + eps
            x = flt(p)
            y = flt(p*a)
            Assert(Base.sig_equal(x, y, n=n))
            Assert(not Base.sig_equal(x, y, n=n + 1))
            x = cpx(p, p)
            y = cpx(p*a, p*a)
            Assert(Base.sig_equal(x, y, n=n))
            Assert(not Base.sig_equal(x, y, n=n + 1))
    def Test_flt_constructor():
        with flt(0):
            # flt(X) 
            for i in (1, 1.0, flt(1), Fraction(1, 1), D("1")):
                Assert(flt(i) == float(i))
                x = flt(i)
                # Factory works
                Assert(x(i) == x)
            with raises(TypeError):
                flt(cpx(1))
        # inf and nan
        x = flt("inf")
        Assert(x == inf)
        x = flt("∞")
        Assert(x == inf)
        x = flt("-inf")
        Assert(x == -inf)
        x = flt("-∞")
        Assert(x == -inf)
        x = flt("nan")
        Assert(str(x) == "nan")
        # Test factory feature
        x = flt(pi)
        y = x(1/pi)
        Assert(ii(y, flt) and y == 1/pi)
        x.n = 5
        y = x(1/pi)
        Assert(y.n == 5)
    def Test_hash():
        # flt and cpx should have same hashes as float and complex
        a = 39573.38593
        x = flt(a)
        Assert(hash(x) == hash(a))
        z = cpx(a, 1/a)
        Assert(hash(z) == hash(complex(a, 1/a)))
        x = flt("∞")
        Assert(hash(x) == hash(float("inf")))
    def Test_cpx_constructor():
        with cpx(0):
            z = cpx(1)
            # Simple
            Assert(z == cpx(1))
            Assert(z == cpx(1, imag=None))
            # Two components
            z = cpx(1, 2)
            Assert(z == cpx(1, 2))
            Assert(z == cpx("1", 2))
            Assert(z == cpx(1, "2"))
            Assert(z == cpx("1", "2"))
            # String
            Assert(z == cpx("1+2j"))
            Assert(z == cpx("1+2i"))
    def Test_copy():
        a = 1.1
        # flt
        with flt(0):
            x = flt(a)
            Assert(x == x.copy())
            Assert(x(x) == x.copy())
            Assert(x(a) == x.copy())
        # cpx
        with cpx(0):
            z = cpx(a)
            zcopy = z.copy()
            Assert(z == zcopy)
            Assert(z(z) == zcopy)
            Assert(z(a) == zcopy)
    def Test_sigcomp_flt():
        '''The flt/cpx sigcomp attribute is an integer that forces
        comparisons to be made to the indicated number of digits.
        '''
        # Note:  if you use a number like pi, some digits will round up,
        # some won't and the test won't pass for some values of i.
        o = 1.1111111111111111
        for i in range(2, 14):
            x = flt(o)
            y = flt(o*(1 + 10**-i))
            with x:
                x.sigcomp = i 
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
        # Check sigcomp = None
        with x:
            x.sigcomp = None
            x = flt(pi)
            y = flt(pi*(1 + 10**-16))
            Assert(x == y)
    def Test_sigcomp_cpx():
        # Note:  if you use a number like pi, some digits will round up,
        # some won't and the test won't pass for some values of i.
        o = 1.1111111111111111
        for i in range(2, 14):
            x = cpx(o, o)
            t = o*(1 + 10**-i)
            y = cpx(t, o)
            with x:
                x.sigcomp = i
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
            y = cpx(o, t)
            with x:
                x.sigcomp = i
                Assert(x == y)
                x.sigcomp = i + 1
                Assert(x != y)
        # Check sigcomp = None
        with x:
            x.sigcomp = None
            x = cpx(pi, pi)
            t = pi*(1 + 10**-16)
            y = cpx(t, pi)
            Assert(x == y)
            y = cpx(pi, t)
            Assert(x == y)
    def Test_polar():
        z = cpx(1, 1)
        with z:
            z.N = 3
            z.p = 1
            Assert(z.s == "(1.41∠45.0°)")
            z.i = 1
            Assert(z.s == "1.41∠45.0°")
            z.rad = 1
            Assert(z.s == "1.41∠0.785")
    def Test_low_and_high():
        'Also tests flt._sci()'
        x = flt(1)
        x.rtz = x.rtdp = False
        with x:
            x.N = 2
            x.low = 0.01
            x.high = 100
            Assert(x(1).s == "1.0")
            Assert(x(10).s == "10.")
            Assert(x(100).s == "100.")
            Assert(x(99.9).s == "100.")
            Assert(x(100.9).s == "1.0e2")
            Assert(x(101).s == "1.0e2")
            Assert(x(0.1).s == "0.10")
            Assert(x(0.01).s == "0.010")
            Assert(x(0.00999).s == "1.0e-2")
            Assert(x(0.0099).s == "9.9e-3")
            Assert(x(0.001).s == "1.0e-3")
        z = cpx(1, 1)
        with z:
            z.N = 2
            z.low = 0.01
            Assert(z(1).s == "(1.0+0.0j)")
            Assert(z(0.1).s == "(0.10+0.0j)")
            Assert(z(0.01).s == "(0.010+0.0j)")
            Assert(z(0.001).s == "(1.0e-3+0.0j)")
            Assert(z(1j).s == "(0.0+1.0j)")
            Assert(z(0.1j).s == "(0.0+0.10j)")
            Assert(z(0.01j).s == "(0.0+0.010j)")
            Assert(z(0.001j).s == "(0.0+1.0e-3j)")
            Assert(z(1+1j).s == "(1.0+1.0j)")
            Assert(z(0.1+0.1j).s == "(0.10+0.10j)")
            Assert(z(0.01+0.01j).s == "(0.010+0.010j)")
            Assert(z(0.001+0.001j).s == "(1.0e-3+1.0e-3j)")
    def Test_eng():
        Expected = '''
            3.14e-9 31.4e-9 314e-9 3.14e-6 31.4e-6 314e-6 3.14e-3
            31.4e-3 314e-3 3.14e0 31.4e0 314e0 3.14e3 31.4e3 314e3
            3.14e6 31.4e6 314e6 3.14e9'''.split()
        x = flt(0)
        x._reset()
        with x:
            for i in range(-9, 10):
                e = Expected[i + 9]
                x = flt(pi*10**i)
                s = x.eng
                Assert(s == e)
            x.rtz = x.rtdp = False
            Assert(x(0).eng == "0.00e0")
            x.rtz = x.rtdp = True
            Assert(x(0).eng == "0e0")
    def Test_GetNumDigits():
        data = '''
            # Various forms of 0
            0 1
            +0 1
            -0 1
            0. 1
            0.0 1
            00 1
            000000 1
            .0 1
            .00 2
            0.00 2
            00.00 2
            .000000 6
            0.000000 6
            00.000000 6
        #
            1 1
            +1 1
            -1 1
            1. 1
            .000001 1
            0.1 1
            .1 1
            +.1 1
            -.1 1
            1.0 2
            10 1
            100000 1
            12300 3
            123.456 6
            +123.456 6
            -123.456 6
            123.45600 8
            012300 3
            0123.456 6
            0123.45600 8
            0.00000000000000000000000000001 1
            0.000000000000000000000000000010 2
            1e4 1
            1E4 1
            01e4 1
            01E4 1
            1.e4 1
            1.E4 1
            01.e4 1
            01.E4 1
            1.0e4 2
            1.0E4 2
            01.0e4 2
            01.0E4 2
            123.456e444444 6
            123.45600e444444 8
            000000123.456e444444 6
            000000123.45600e444444 8
        '''
        for i in data.strip().split("\n"):
            i = i.strip()
            if not i or i.startswith("#"):
                continue
            try:
                s, expected = i.split()
            except Exception as e:
                print(f"Unhandled exception:  '{e}'")
                print(f"Dropping into debugger")
                breakpoint()
                pass
            got = GetNumDigits(s)
            expected = int(expected)
            assert_equal(got, expected)
        # Test with inttzsig
        assert_equal(GetNumDigits("123", inttzsig=False), 3)
        assert_equal(GetNumDigits("123", inttzsig=True), 3)
        assert_equal(GetNumDigits("12300", inttzsig=False), 3)
        assert_equal(GetNumDigits("12300", inttzsig=True), 5)
        # Forms that raise exceptions
        raises(ValueError, GetNumDigits, 1)
        raises(ValueError, GetNumDigits, 1.0)
        raises(ValueError, GetNumDigits, "a")
        raises(ValueError, GetNumDigits, "e2")
        raises(ValueError, GetNumDigits, "1..e2")
        # Show that GetNumDigits works with strings from Decimal objects
        n = 50
        x = D("1." + "1"*n)
        assert_equal(GetNumDigits(str(x)), n + 1)
    def Test_rnd():
        x = flt(pi)
        for n, s in (
                (1, "3.0"),
                (2, "3.1"),
                (3, "3.14"),
                (4, "3.142"),
                (5, "3.1416"),
                (6, "3.14159"),
                (7, "3.141593"),
                (8, "3.1415927"),
                (9, "3.14159265"),
                (10, "3.141592654"),
                (11, "3.1415926536"),
                (12, "3.14159265359"),
                (13, "3.14159265359"),
                (14, "3.1415926535898"),
                (15, "3.14159265358979"),
                ):
            Assert(repr(x.rnd(n)) == s)
            y = flt(s)
            Assert(repr(y) == s)
    def Test_fmt():
        if 1:   # flt
            x = flt(10*pi)
            x._reset()
            y = flt(10*pi)
            Assert(str(x) == str(y) == "31.4")
            # Show context manager works to allow a change to Base.N; also show
            # that an instance's change to self.n isn't affected by the context
            # manager.
            with x:
                x.N = 8
                Assert(str(x) == str(y) == "31.415927")
                y.n = 8
            Assert(str(x) == "31.4")
            # y still uses 8 digits but x doesn't
            Assert(str(y) == "31.415927")
            # Test eng, sci, etc.
            x = flt(1e5*pi)
            Assert(x.s == "314000")
            Assert(x.eng == "314e3")
            Assert(x.engsi == "314 k")
            Assert(x.engsic == "314k")
            Assert(x.sci == "3.14e5")
            x.u = True
            Assert(x.eng == "314✕10³")
            Assert(x.sci == "3.14✕10⁵")
            # Eng/sci with Unicode
            # rtz, rtdp, rlz
            x = flt(1.1)
            x._reset()
            with x:
                x.N = 4
                Assert(x.s == "1.1")
                x.rtz = False
                Assert(x.s == "1.100")
            x = flt(31)
            x.rtz = x.rtdp = False
            Assert(x.s == "31.0")
            x.rtz = True
            Assert(x.s == "31.")
            x.rtdp = True
            Assert(x.s == "31")
            x = flt(1/4)
            x._reset()
            Assert(x.s == "0.25")
            x.rlz = True
            Assert(x.s == ".25")
        if 1:   # cpx
            # Quadrant 1
            z = cpx(1.234, 7.654)
            z._reset()
            Assert(z.s == "(1.23+7.65j)")
            z.p = True
            Assert(z.s == "(7.75∠80.8°)")
            z.i = True
            Assert(z.s == "7.75∠80.8°")
            z.rad = True
            Assert(z.s == "7.75∠1.41")
            z.rad = False
            z.p = False
            Assert(z.s == "1.23+7.65i")
            z.t = True
            Assert(z.s == "(1.23,7.65)")
            z.w = True
            Assert(z.s == "(1.23, 7.65)")
            z = cpx(0, 7.654)
            Assert(z.s == "(0, 7.65)")
            z.t = False
            Assert(z.s == "0 + 7.65i")
            z.nz = True
            Assert(z.s == "7.65i")
            # Quadrant 2
            z = cpx(-1.234, 7.654)
            z._reset()
            Assert(z.s == "(-1.23+7.65j)")
            z.i = True
            Assert(z.s == "-1.23+7.65i")
            z.p = True
            Assert(z.s == "7.75∠99.2°")
            z.i = False
            Assert(z.s == "(7.75∠99.2°)")
            z.rad = True
            Assert(z.s == "(7.75∠1.73)")
            z.rad = False
            z.p = False
            z.i = True
            Assert(z.s == "-1.23+7.65i")
            z = cpx(-1.234, 0)
            Assert(z.s == "-1.23+0i")
            z.nz = True
            Assert(z.s == "-1.23")
            # Quadrant 3
            z = cpx(-1.234, -7.654)
            z._reset()
            Assert(z.s == "(-1.23-7.65j)")
            z.i = True
            Assert(z.s == "-1.23-7.65i")
            z.p = True
            Assert(z.s == "7.75∠-99.2°")
            z.i = False
            Assert(z.s == "(7.75∠-99.2°)")
            z.rad = True
            Assert(z.s == "(7.75∠-1.73)")
            z.rad = False
            z.p = False
            z.i = True
            Assert(z.s == "-1.23-7.65i")
            # Spcial case of 0
            z = cpx(-0, -0)
            Assert(z.s == "0+0i")
            z.nz = True
            Assert(z.s == "0")
            z._reset()
    def Test_functions():
        '''Test the functions using python 3.7.12.  The focus is that the
        correct types are returned, as the numerical values will have been
        tested well with python's tests.
        '''
        x = flt(3.389) 
        y = flt(1.412) 
        a, i = 0.8813735870195429, cpx(0, 1)
        tf, tc, ti = type(x), type(i), type(1)
        if 1:   # acos
            Assert(type(acos(0)) == tf)
            Assert(type(acos(i)) == tc)
        if 1:   # acosh
            raises(ValueError, acosh, 0.1)
            Assert(type(acosh(1)) == tf)
            Assert(type(acosh(i)) == tc)
        if 1:   # asin
            Assert(type(asin(0)) == tf)
            Assert(type(asin(i)) == tc)
        if 1:   # asinh
            Assert(type(asinh(0)) == tf)
            Assert(type(asinh(i)) == tc)
        if 1:   # atan
            Assert(type(atan(0)) == tf)
            raises(ValueError, atan, i)
        if 1:   # atan2
            Assert(type(atan2(0, 0)) == tf)
        if 1:   # atanh
            Assert(type(atanh(0)) == tf)
            Assert(type(atanh(i)) == tc)
            raises(ValueError, atanh, 1)
        if 1:   # ceil
            Assert(type(ceil(x)) == ti)
            raises(TypeError, ceil, i)
        if 1:   # copysign
            Assert(type(copysign(x, 1)) == tf)
            Assert(type(copysign(x, -1)) == tf)
        if 1:   # cos
            Assert(type(cos(0)) == tf)
            Assert(type(cos(i)) == tc)
        if 1:   # cosh
            Assert(type(cosh(0)) == tf)
            Assert(type(cosh(i)) == tc)
        if 1:   # degrees
            Assert(type(degrees(pi)) == tf)
            raises(TypeError, degrees, i)
        if 1:   # divmod
            q, rem = divmod(x, y)
            Assert(q == 2 and ii(q, int))
            Assert(rem == x - 2*y and type(rem) == tf)
            Assert(q*y + x % y == x)
        if 1:   # erf
            Assert(type(erf(x)) == tf)
            raises(TypeError, erf, i)
        if 1:   # erfc
            Assert(type(erfc(x)) == tf)
            raises(TypeError, erfc, i)
        if 1:   # exp
            Assert(type(exp(0)) == tf)
            Assert(type(exp(i)) == tc)
        if 1:   # expm1
            Assert(type(expm1(0)) == tf)
            raises(TypeError, expm1, i)
        if 1:   # fabs
            Assert(type(fabs(x)) == tf)
            raises(TypeError, fabs, i)
        if 1:   # factorial
            Assert(factorial(3) == 6)
            raises(ValueError, factorial, -1)
            # The following line is commented out because using factorial()
            # with floats is deprecated.
            # raises(ValueError, factorial, x)
            raises(TypeError, factorial, i)
        if 1:   # floor
            Assert(type(floor(x)) == ti)
            raises(TypeError, floor, i)
        if 1:   # fmod
            Assert(type(fmod(x, y)) == tf)
            raises(TypeError, fmod, i, y)
        if 1:   # frexp
            a, b = frexp(x)
            Assert(type(a) == tf)
            Assert(type(b) == ti)
            raises(TypeError, frexp, i)
        if 1:   # fsum
            Assert(type(fsum([x, y])) == tf)
            raises(TypeError, fsum, [i, y])
        if 1:   # gamma
            Assert(type(gamma(x)) == tf)
            raises(TypeError, gamma, i)
        if 1:   # hypot
            Assert(type(hypot(x, y)) == tf)
            raises(TypeError, hypot, i, x)
        if 1:   # isclose
            Assert(type(isclose(x, y)) == bool)
            Assert(type(isclose(i, y)) == bool)
        if 1:   # isfinite
            Assert(type(isfinite(x)) == bool)
        if 1:   # isinf
            Assert(isinf(flt("inf")))
        if 1:   # isnan
            Assert(isnan(flt("nan")))
        if 1:   # ldexp
            Assert(ldexp(x, 4) == x*2**4)
        if 1:   # lgamma
            Assert(type(lgamma(x)) == tf)
            raises(TypeError, lgamma, i)
        if 1:   # log
            Assert(type(log(x)) == tf)
            Assert(type(log(i)) == tc)
        if 1:   # log10
            Assert(type(log10(x)) == tf)
            Assert(type(log10(i)) == tc)
        if 1:   # log1p
            Assert(type(log1p(x)) == tf)
            raises(TypeError, log1p, i)
        if 1:   # log2
            Assert(type(log2(x)) == tf)
            raises(TypeError, log2, i)
        if 1:   # modf
            a, b = modf(x)
            Assert(type(a) == tf and type(b) == tf)
            raises(TypeError, modf, i)
        if 1:   # phase
            Assert(type(phase(x)) == tf)
            Assert(type(phase(i)) == tf)
        if 1:   # polar
            a, b = polar(i)
            Assert(type(a) == tf and type(b) == tf)
        if 1:   # pow
            Assert(type(pow(x, y)) == tf)
            raises(TypeError, pow, i, x)
            raises(TypeError, pow, x, i)
        if 1:   # radians
            Assert(type(radians(x)) == tf)
            raises(TypeError, radians, i)
        if 1:   # rect
            Assert(type(rect(x, y)) == tc)
        if 1:   # remainder
            Assert(type(remainder(x, y)) == tf)
        if 1:   # sin
            Assert(type(sin(x)) == tf)
            Assert(type(sin(i)) == tc)
        if 1:   # sinh
            Assert(type(sinh(x)) == tf)
            Assert(type(sinh(i)) == tc)
        if 1:   # sqrt
            Assert(type(sqrt(x)) == tf)
            Assert(type(sqrt(-x)) == tc)
            Assert(type(sqrt(i)) == tc)
        if 1:   # tan
            Assert(type(tan(x)) == tf)
            Assert(type(tan(i)) == tc)
        if 1:   # tanh
            Assert(type(tanh(x)) == tf)
            Assert(type(tanh(i)) == tc)
        if 1:   # trunc
            Assert(type(trunc(x)) == ti)
            raises(TypeError, trunc, i)
    def Test_ParseComplex():
        test_cases = {
            # Pure imaginaries
            1j: (
                "i", "j", "1i", "i1", "1j", "j1", "1 j", "j 1",
                "I", "J", "1I", "I1", "1J", "J1", "1 i", "i 1",
            ),
            -1j: (
                "-i", "-j", " - \t\n\r\v\f j",
                "-I", "-J", " - \t\n\r\v\f J",
            ),
            3j: (
                "3i", "+3i", "3.i", "+3.i", "3.0i", "+3.0i", "3.0e0i", "+3.0e0i",
                "i3", "+i3", "i3.", "+i3.", "i3.0", "+i3.0", "i3.0e0", "+i3.0e0",
                "3.000i", "i3.000", "3.000E0i", "i3.000E0",
                "3.000e-0i", "i3.000e-0", "3.000e+0i", "i3.000e+0",
    
                "3I", "+3I", "3.I", "+3.I", "3.0I", "+3.0I", "3.0e0I", "+3.0e0I",
                "I3", "+I3", "I3.", "+I3.", "I3.0", "+I3.0", "I3.0e0", "+I3.0e0",
                "3.000I", "I3.000", "3.000E0I", "I3.000E0",
                "3.000e-0I", "I3.000e-0", "3.000e+0I", "I3.000e+0",
    
                "3j", "+3j", "3.j", "+3.j", "3.0j", "+3.0j", "3.0e0j", "+3.0e0j",
                "j3", "+j3", "j3.", "+j3.", "j3.0", "+j3.0", "j3.0e0", "+j3.0e0",
                "3.000j", "j3.000", "3.000E0j", "j3.000E0",
                "3.000e-0j", "j3.000e-0", "3.000e+0j", "j3.000e+0",
    
                "3J", "+3J", "3.J", "+3.J", "3.0J", "+3.0J", "3.0e0J", "+3.0e0J",
                "J3", "+J3", "J3.", "+J3.", "J3.0", "+J3.0", "J3.0e0", "+J3.0e0",
                "3.000J", "J3.000", "3.000E0J", "J3.000E0",
                "3.000e-0J", "J3.000e-0", "3.000e+0J", "J3.000e+0",
            ),
            -8j: (
                "-8i", "-8.i", "-8.0i", "-8.0e0i",
                "-i8", "-i8.", "-i8.0", "-i8.0E0",
    
                "-8I", "-8.I", "-8.0I", "-8.0e0I",
                "-I8", "-I8.", "-I8.0", "-I8.0E0",
    
                "-8j", "-8.j", "-8.0j", "-8.0e0j",
                "-j8", "-j8.", "-j8.0", "-j8.0E0",
    
                "-8J", "-8.J", "-8.0J", "-8.0e0J",
                "-J8", "-J8.", "-J8.0", "-J8.0E0",
            ),
            # Reals
            0: (
                "0", "+0", "-0", "0.0", "+0.0", "-0.0"
                "000", "+000", "-000", "000.000", "+000.000", "-000.000",
                "0+0i", "0-0i", "0i+0", "0i-0", "+0i+0", "+0i-0", "i0+0",
                "i0-0", "+i0+0", "+i0-0", "-i0+0", "-i0-0",
            ),
            1: (
                "1", "+1", "1.", "+1.", "1.0", "+1.0", "1.0e0", "+1.0e0",
                                                    "1.0E0", "+1.0E0",
                "1+0i", "1-0i",
                "0i+1", "+0i+1", "-0i+1", "i0+1", "+i0+1", "-i0+1",
            ),
            -1: (
                "-1", "-1+0i", "-1-0i", "0i-1", "+0i-1", "-0i-1",
                "i0-1", "+i0-1", "-i0-1",
            ),
            -2: (
                "-2", "-2.", "-2.0", "-2.0e0",
            ),
            -2.3: (
                "-2.3", "-2.30", "-2.3000", "-2.3e0", "-2300e-3", "-0.0023e3",
                "-.23E1",
            ),
            2.345e-7: (
                "2.345e-7", "2345e-10", "0.00000002345E+1", "0.0000002345",
            ),
            # Complex numbers
            1+1j: ("1+i", "1+1i", "i+1", "1i+1", "i1+1"),
            1-1j: ("1-i", "1-1i", "-i+1", "-1i+1", "-i1+1"),
            -1-1j: ("-1-i", "-1-1i", "-i-1", "-1i-1", "-i1-1"),
            1-2j: (
                "1-2i", "1-2.i", "1.-2i", "1.-2.i",
                "1-j2", "1-j2.", "1.-j2", "1.-j2.",
                "1.00-2.00I", "1.00-I2.00", "1000e-3-200000e-5I",
                "1.00-J2.00", "1000E-3-J200000E-5",
                "-2i+1", "-i2 + \n1",
                "-i2+1",
            ),
            -1+2j: (
                "2i-1", "i2-1",
                "+2i-1", "+i2-1",
            ),
            -12.3+4.56e-7j: (
                "-12.3+4.56e-7j",
                "-12.3 + 4.56e-7j",
                "- 1 2 . 3 + 4 . 5 6 e - 7 j",
                "-1.23e1+456e-9i",
                "-0.123e2+0.000000456i",
            ),
        }
        PC = ParseComplex()
        for number in test_cases:
            for numstr in test_cases[number]:
                real, imag = PC(numstr)
                num = cpx(real, imag)
                assert_equal(num, number)
        # Test that we can get Decimal == D types back
        PC = ParseComplex(D)
        a, b = PC("1+3i")
        Assert(isinstance(a, D) and isinstance(b, D))
        Assert(a == 1 and b == 3)
        a, b = PC("-1.2-3.4i")
        Assert(isinstance(a, D) and isinstance(b, D))
        Assert(a == D("-1.2") and b == D("-3.4"))
        # Test that we can get rational number components back
        PC = ParseComplex(Fraction)
        a, b = PC("-1.2-3.4i")
        Assert(isinstance(a, Fraction) and isinstance(b, Fraction))
        Assert(a == Fraction(-6, 5) and b == Fraction(-17, 5))
        # Show that numbers with higher resolutions than floats can be used
        PC = ParseComplex(D)
        rp = "0.333333333333333333333333333333333"
        ip = "3.44444444444444444444444444444"
        r, i = PC(rp + "\n-i" + ip)  # Note inclusion of a newline
        Assert(r == D(rp))
        Assert(i == D("-" + ip))
        # Test that mpmath mpf numbers can be used
        try:
            from mpmath import mpf
            PC = ParseComplex(mpf)
            a, b = PC("1.1 - 3.2i")
            Assert(isinstance(a, mpf) and isinstance(b, mpf))
            Assert(a == mpf("1.1") and b == mpf("-3.2"))
        except ImportError:
            pass
    failed, messages = run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)
