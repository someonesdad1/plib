'''
 
Todo
    - Refactor to get rid of old method and use new TakeApart instance.
    - The brief keyword was added to Fmt attributes.  When it is True,
      string interpolation output is truncated to fit into a user-defined
      width.  Need to implement in fix sci eng __call__.
        - Behavior:  if fmt.brief is True, then a width is gotten and a 
          number's interpolation string is adusted to fit into the desired
          width.  This defaults to COLUMNS - 1 if it is not specified.

    - fix(), sci(), etc. should use two new keywords:  unc and err.  unc
      will be interpreted as an uncertainty and use the standard
      uncertainty interpolation such as 3.14(3).  err is the same but uses
      3.14[3] to imply an interval number, such as from a roundoff error.
        - This also gives the ability to handle ufloats.

    - Why doesn't fix() use significand()?
    - Lock
        - The threading.Lock used for context management is a PITA in some
          use cases because it means this object can't be pickled.  Try
          using a global variable that allows the lock to not be used.
        - One use case is hc.py, which is a single threaded app.  It would
          be easier to persist its state if pickling could be used.
    - Get rid of the color.py dependency in the module (OK in test code).
      The only needed change is to put an ANSI escape sequence in for
      underlining for polar complex number display.
    - Angle measures:  deg rad grad rev
    - Note mpmath.nstr() has keywords to control low & high for fixed point
      strings.  You can also use it to get a floating point interpolation.
        - An x = mpf(i) where i is an integer appears to have the property
          int(x) == i, at least if the integer can be expressed at the
          current precision exactly.  Checked up to 2**1000000.
 
class Fmt:  Format floating point numbers
    Run the module as a script to see example output.  See Terminal Notes
    below.
 
    This module provides string interpolation ("formatting") for floating
    point and complex number types.  str(float(math.pi)) returns
    '3.141592653589793', which contains too many digits for
    casual interpretation.  This module's convenience instance fmt will
    format pi as fmt(math.pi) = '3.14', which allows easier interpretation.
 
    A Fmt instance can format int, float, decimal.Decimal, mpmath.mpf, and
    fraction.Fraction number types.
 
    Fmt is also a context manager so you can change formatting
    characteristics in a with block.  See Locking notes below for 
    a complication detail about the context manager.
 
    Methods
        - reset() to put instance in default state
        - fmtint() to format an integer
 
    The attributes of a Fmt instance provide more control over the
    formatting:
 
        n       Sets the number of significant digits.
        default String for default formatting (fix, sci, eng, engsi,
                engsic)
        int     How to format integers (None is str(), dec, hex, oct, bin)
        brief   If True, fit string on one line if possible.
        dp      Sets the radix (decimal point) string.
        low     Numbers below this value are displayed with scientific
                notation.  None means all small numbers are displayed
                in fixed point.
        high    Numbers above this value are displayed with scientific
                notation.  None means all large numbers are displayed
                in fixed point.
        u       If True, display scientific and engineering notations with
                Unicode such as 3.14✕10⁶.
        rlz     If True, remove leading zero digit in fixed point strings.
                Example:  -0.284 is "-0.284" if False, "-.284" if True.
        rtz     If True, remove trailing significant zero digits.
        rtdp    If True, remove the trailing radix if it ends the string.
        spc     If True, use " " as leading character if number >= 0
        sign    If True, always include the number's sign
 
    Complex number attributes:
 
        imag_unit   String to use for the imaginary unit.
        polar       If True, use polar coordinates.
        deg         If True, output degrees in polar coordinates.
        cuddled     If True, use '2+3i' form; if False, use '2 + 3i' form.
        ul          If True, underline the argument in polar form.
        comp        If True, display as (re,im) form, (re, im) if cuddled
                    False.
 
    Terminal Notes
        This script is intended to be used with other scripts in the plib
        directory.  You can get the needed tools at
        https://github.com/someonesdad1/plib.  I use this script in a bash
        terminal in a cygwin environment using the mintty terminal emulator
        and it works as written.  Look at /plib/pictures/fmt.png to see
        what the Demo() function's output looks like on my screen.  Other
        terminals may need hacking on color.py to get things to work 
        correctly.  Define the environment variable DPRC to get ANSI color
        strings output to the terminal.
 
    Locking notes 
        The context manager uses a threading.Lock object to keep things
        sane in multi-threaded environments.  However, there's a fairly
        steep cost of doing this:  you cannot pickle a Fmt instance to 
        e.g. persist its state.  If you wish to persist a Fmt instance
        state, you can set the self.lock attribute to None before pickling.
 
'''
if 1:   # Header
    if 1:   # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2008, 2012, 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Format numbers with the Fmt class.  Provides
        # fixed point, scientific, and engineering formats.  Run as a
        # script to see a demo.
        #∞what∞#
        #∞test∞# --test #∞test∞#
        pass
    if 1:   # Standard imports
        import decimal
        import fractions
        import locale 
        import math 
        import os 
        import string 
        import subprocess 
        import threading 
        from collections import deque, namedtuple
        from pprint import pprint as pp
        from pdb import set_trace as xx 
    if 1:   # Custom imports
        from color import t
        from wrap import dedent
        try:
            # Note:  mpmath is optional, but I suggest you use it because
            # it handles numbers much larger and smaller than standard
            # python tools and it has numerous special functions defined
            # over the complex plane.
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    if 1:   # Global variables
        W = int(os.environ.get("COLUMNS", "80")) - 1
        L = int(os.environ.get("LINES", "50"))
        D = Decimal = decimal.Decimal
        F = Fraction = fractions.Fraction
        ii = isinstance
        __all__ = "Fmt TakeApart fmt ta".split()
class TakeApart:
    'Handles int, float, Decimal, mpf, and Fractions'
    def __init__(self, n=3):
        # Note self.n won't be changed in a reset()
        self._n = n
        self.lock = threading.Lock()    # For context management
        self.reset()
    def reset(self):
        'Set attributes to default'
        self._supported = set((int, float, Decimal, Fraction))
        if have_mpmath:
            self.supported.add(mpmath.mpf)
        self._number = None     # Number argument to __call__()
        self._sign = None       # "-" or " "
        self._ld = None         # Leading digit of number
        self._dp = None         # Decimal point string
        self._other = None      # Remaining digits of number
        self._e = None          # Integer exponent of 10
        self._dq = None         # Deque of significand's digits
        self._strict = False    # If True, n must be <= precision
    def __enter__(self):
        self.lock.acquire()  # Stay locked through context execution
        self.my_attributes = {}
        for a in self.__dict__:
            if a.startswith("__"):
                continue
            if not a.startswith("_"):
                continue
            if a in "_supported _superscripts".split():
                continue
            self.my_attributes[a] = eval(f"self.{a}")
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore our attributes
        d = self.my_attributes
        for i in d:
            exec(f"self.{i} = d['{i}']")
        self.lock.release()
        del self.my_attributes
        return False
    def __str__(self):
        if self._ld is None:
            return None
        return (self.sign + self._ld + self._dp +
                self.other + "e" + str(self._e))
    def __call__(self, x):
        assert(x is not None)
        self._number = x
        self.disassemble()
        return str(self)
    def disassemble(self):
        "Disassemble the number self._number into this instance's attributes"
        n, x = self._n, self._number
        assert(ii(n, int) and n >= 0)
        # Handle int, float, Decimal, mpf, and Fractions
        if ii(x, (int, float, decimal.Decimal)):
            # The following avoids an infinite recursion with f.flt
            # instances
            if ".flt'>" in str(type(x)):
                x = float(x)
            y = decimal.Decimal(str(x))
            ctx = decimal.getcontext()
            n = min(ctx.prec, n) if self.strict else n
            if not n:
                n = ctx.prec
            if self._strict:
                assert(1 <= n <= ctx.prec)
        elif ii(x, fractions.Fraction):
            y = decimal.Decimal(x.numerator)/decimal.Decimal(x.denominator)
        elif have_mpmath and ii(x, mpmath.mpf):
            y = x
            n = min(mpmath.mp.dps, n) if self.strict else n
            if not n:
                n = mpmath.mp.dps
            if self._strict:
                assert(1 <= n <= mpmath.mp.dps)
        else:
            raise TypeError(f"{x!r} is not a supported number type")
        # Now disassemble the number
        sign, yabs = " ", y
        if y < 0:
            sign = "-"
            yabs = -y
        if have_mpmath and ii(yabs, mpmath.mpf):
            # mpmath
            lg, ten = mpmath.chop(mpmath.log10(yabs)), mpmath.mpf(10)
            e = int(mpmath.floor(lg)) if yabs else 0
            # Get the significand string
            a = yabs*ten**(-e)
            assert(ii(a, mpmath.mpf))
            s = mpmath.nstr(a, n)
            a = mpmath.mpf(s)
            if a >= 10:
                # This can happen when e.g. the number is 9.999999 and we
                # are rounding to 3 figures
                s = mpmath.nstr(a/ten, n)
                e += 1
            assert("." in s and len(s) > 1)    # mpmath seems to use only "."
            dp = s[1]
            t = s.replace(".", "").replace(",", "")     # Remove radix
            while len(t) < n:   # nstr() returns 1.0 for 1 whatever n is
                t += "0"
            if len(t) > n: # nstr(1, 1) returns 1.0 for n = 1
                t = t[:n]
            assert(len(t) == n if yabs else 1)
            ld, other = t[0], t[1:]
        else:
            # Decimal
            yabs = abs(y)
            assert(ii(y, decimal.Decimal))
            ys = f"{yabs:.{n - 1}e}".lower()    # Get sci form to n digits
            s, e = ys.split("e")
            dp = "," if "," in s else "."
            ld, other = (s, "") if len(s) == 1 else s.split(dp)
            # For zero, Decimal formats an exponent to n - 1; we want 0
            e = int(e) if y else 0
        self._sign = sign
        self._ld = ld
        self._dp = dp
        self._other = other
        self._e = e
        self._dq = deque(ld + other)
        if 1:
            # Check invariants
            assert(self._sign in ("-", " "))
            assert(ii(self._ld, str) and len(self._ld) == 1)
            assert(self._dp in (".", ","))
            assert(len(self._dp) == 1)
            assert(ii(self._other, str))
            assert(ii(self._e, int))
            # Deque has length of strings ld and other
            assert(ii(self._dq, deque) and 
                (len(self._dq) == len(self._ld) + len(self._other)))
            assert("." not in self._dq and "," not in self._dq)
            assert(len(self._ld + self._other) == n)
    if 1:   # Properties
        @property
        def dp(self):
            'Decimal point string'
            assert(ii(self._dp, str) and len(self._dp) == 1)
            return self._dp
        @property
        def dq(self):
            "Deque of significand's digits"
            assert(ii(self._dq, deque) and len(self._dq))
            return self._dq
        @property
        def e(self):
            'Integer exponent of 10'
            assert(ii(self._e, int))
            return self._e
        @property
        def exp(self):
            'String form of self.e'
            return str(self.e)
        @property
        def ld(self):
            'Leading digit of significand'
            assert(ii(self._ld, str) and len(self._ld) == 1)
            return self._ld
        @property
        def other(self):
            'Non-leading digits of significand'
            assert(ii(self._ld, str))
            return self._other
        @property
        def n(self):
            'Number of digits in significand'
            return self._n
        @n.setter
        def n(self, value):
            assert(ii(value, int) and value >= 0)
            redo = True if self._n != value else False
            self._n = value
            if redo and self._number is not None:
                self(self._number)
        @property
        def number(self):
            'Last argument to __call__()'
            assert(self._number is not None)
            return self._number
        @property
        def sign(self) -> str:
            '"-" or " ", sign of self.number'
            assert(ii(self._sign, str) and self._sign in ("-", " ", ""))
            return self._sign
        @property
        def strict(self):
            'If True, n must be <= precision'
            return self._strict
        @strict.setter
        def strict(self, value):
            self._strict = bool(value)
        @property
        def supported(self):
            'Set of supported types'
            return self._supported
        @supported.setter
        def supported(self, myset):
            assert(ii(myset, set) and myset)
            self._supported = myset
class Fmt:
    def __init__(self, n=3, low=D("1e-5"), high=D("1e16")):
        '''n is the number of digits to format to.  
        low is the point below which scientific notation is used.
        high is the point above which scientific notation is used.
        low and high can be None, which disables them; if disabled, then
        fixed point interpolation is used by default except for very
        large or small numbers where there are too many digits to
        display on the screen.
        '''
        self._n_init = n
        self._n = None                  # Number of digits
        self._default = None            # Default formatting method
        self.ta = None                  # Take apart machinery
        self._dp = None                 # Radix
        self._u = None                  # Use Unicode symbols for exponents
        self._rlz = None                # Remove leading zero if True
        self._rtz = None                # Remove trailing zeros if True
        self._rtdp = None               # Remove trailing radix if True
        self._spc = None                # If num >= 0, use " " for leading character
        self._sign = None               # Include "+" or "-" in interpolation
        self._int = None                # Default fmtint() style
        self._strict = None             # If True, n must be <= precision
        # If in fix mode, very large/small numbers can result in too
        # many digits to display on the screen.  When abs(exponent) is
        # greater than self.nchars (here, about 1/4 of the terminal
        # window's capacity), use sci.
        self.nchars = None              # If in fix mode, use sci if n > this number
        self.brief = None               # Fit string on one line 
        self.ellipsis = None            # Ellipsis for brief mode
        # Attributes for complex numbers
        self._imag_unit = None          # Imaginary unit
        self._polar = None              # Use polar coord for complex
        self._deg = None                # Use degrees for angles
        self._cuddled = None            # Use 'a+bi' if True
        self._ul = None                 # Underline argument in polar form
        self._comp = None               # (re,im) form 
        # Other attributes that won't change when reset() is called
        # Key to _SI_prefixes dict is exponent//3
        self._low_init = self.toD(low)
        self._high_init = self.toD(high)
        self._SI_prefixes = dict(zip(range(-8, 9), list("yzafpnμm.kMGTPEZY")))
        self._SI_prefixes[0] = ""       # Need empty string
        self._superscripts = dict(zip("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"))
        # For context manager behavior, we'll use a lock to avoid another
        # thread messing with our attributes.  You can set this to None if
        # you don't want a lock used.
        self.lock = threading.Lock()
        # Set to default state
        self.reset()
    def reset(self):
        'Reset attributes to default state'
        n = self._n_init
        self._n = n
        self._default = "fix"
        self._int = None    # Default uses str(int)
        self.ta = TakeApart()
        self.ta.n = n  # Synchronize number of digits
        self._dp = locale.localeconv()["decimal_point"]
        self._low = self._low_init  
        self._high = self._high_init
        self._u = False
        self._rlz = False
        self._rtz = False
        self._rtdp = False
        self._spc = False
        self._sign = False
        self.nchars = W*L//4  # Base on screen width and hight
        self.brief = False
        self.ellipsis = "·"*3
        self._strict = False
        # Attributes for complex numbers
        self._imag_unit = "i"
        self._polar = False
        self._deg = True
        self._cuddled = False
        self._ul = False
        self._comp = False
    def __getstate__(self):
        state = self.__dict__.copy()
        # Remove things that are unpicklable
        del state["lock"]
    def __setstate__(self, state):
        self.__dict__.update(state)
        self.lock = threading.Lock()
    def __enter__(self):
        # Store our attributes (note only those that start with '_' are
        # saved)
        if self.lock is not None:
            self.lock.acquire()  # Stay locked through context execution
        self.my_attributes = {}
        for a in self.__dict__:
            if a.startswith("__"):
                continue
            if not a.startswith("_"):
                continue
            if a in "_SI_prefixes _superscripts".split():
                continue
            self.my_attributes[a] = eval(f"self.{a}")
    def __exit__(self, exc_type, exc_val, exc_tb):
        # Restore our attributes
        d = self.my_attributes
        for i in d:
            exec(f"self.{i} = d['{i}']")
        if self.lock is not None:
            self.lock.release()
        del self.my_attributes
        return False
    def toD(self, value) -> Decimal:
        '''Convert value to a Decimal object.  Supported types are int,
        float, Fraction, Decimal, str, mpmath.mpf, and any other type
        that gives a value from str(value)
        '''
        if ii(value, (int, float)):
            return D(value)
        elif ii(value, D):
            return value
        elif ii(value, Fraction):
            return D(value.numerator)/D(value.denominator)
        elif ii(value, str):
            if "/" in value:
                f = Fraction(value)
                return D(f.numerator)/D(f.denominator)
            else:
                return D(value)
        elif have_mpmath and ii(value, mpmath.mpf):
                return D(str(value))
        else:
            return D(str(value))
    def _take_apart(self, x, n=None) -> namedtuple:
        '''Take the Decimal number x apart into its sign, digits,
        decimal point, and exponent.  Return the named tuple 
        Apart(sign, ld, dp, other, e) where:
            ld + dp + other is the significand: 
            ld is the leading digit
            dp is the locale's radix (decimal point)
            other is the string of digits after the decimal point
            e is the integer exponent
        n overrides self.n if it is not None.
        '''
        Apart = namedtuple("Apart", "sign ld dp other e")
        if not ii(x, D):
            raise TypeError("x must be a Decimal number")
        # Get scientific notation form
        N = int(n) if n is not None else self._n
        if not N:
            ctx = decimal.getcontext()
            N = ctx.prec
        xs = f"{abs(x):.{N - 1}e}"
        if self.dp == ",":
            xs = xs.replace(".", ",")
        sign = "-" if x < 0 else ""
        significand, e = xs.split("e")
        exponent = int(e) if x else 0
        other, dp = "", self.dp
        if dp not in significand:
            if len(significand) != 1:
                raise ValueError("'{significand}' was expected to be 1 character")
            ld = significand
        else:
            ld, other = significand.split(dp)
        assert(len(ld) + len(other) == N)     # N figures is an invariant
        return Apart(sign, ld, dp, other, int(exponent))
    def _get_data(self, value, n=None) -> tuple:
        x = D(str(value))
        parts = self._take_apart(x, n)
        return (parts, deque(parts.ld) + deque(parts.other), "0")
    def get_columns(self):
        'Return the number of columns on the screen'
        return int(os.environ.get("COLUMNS", 80)) - 1
    def get_colums1(self):
        '''Returns the current number of columns on the screen.  It's not
        called by default because it's slow since it has to create another
        process.  Use it if the user may have resized a window after your 
        app has started.
        '''
        # This only works on UNIX/cygwin type systems
        try:
            r = subprocess.run(["stty", "size"], capture_output=True)
            lines, columns = tuple(int(i) for i in r.stdout.strip().split())
            return lines
        except CalledProcessError:
            return self.get_columns()
    def fmtint(self, value, fmt=None, width=None, offset=0, mag=False):
        '''Format an integer value.  If fmt is None, the default self.int
        formatting is used.  Other values for fmt are "hex", "oct", "dec",
        and "bin", which cause 0x, 0o, 0d, or 0b to be prepended.
        self.sign and self.spc are honored.
 
        width is the number of spaces the string must fit into.  If it is
        None, then the number of COLUMNS - 1 is used.
 
        offset is subtracted from width to allow for other string elements
        to be used with the returned string.
        
        mag if True is used to provide a [~10ⁿ] string at the end to
        indicate the magnitude of the number.
 
        width and offset are only used if self.brief is True.
        '''
        if not ii(value, int):
            raise TypeError("value must be an int")
        if value < 0:
            sgn = "-"
            value = abs(value)
        else:
            sgn = "+" if self.sign else " " if self.spc else ""
        if fmt is None:
            fmt = self.int
        s = f"{sgn}{value}"
        if not self.brief:
            if fmt == "hex":
                s = f"{sgn}{hex(value)}"
            elif fmt == "oct":
                s = f"{sgn}{oct(value)}"
            elif fmt == "dec":
                s = f"{sgn}0d{value}"
            elif fmt == "bin":
                s = f"{sgn}{bin(value)}"
            elif fmt is None:
                pass
            else:
                raise ValueError(f"fmt = {fmt!r} must be None, hex, oct, dec, or bin")
            return s
        else:
            # Get L = what will fit on one line
            L = self.get_columns() - offset if width is None else int(width) - offset
            # The minimum possible length is the sign, one character each
            # end, and ellipsis
            min_length = 2 + len(self.ellipsis) + len(sgn)
            m = ""
            if mag:     # Add in the length of ' |10ⁿ|' string
                x = D(value)*D("1.0")
                a = f"{x:.1e}".split("e")[1]
                e = int(a)
                assert(e >= 0)
                m = " |10"
                for i in str(e):
                    m += self._superscripts[i]
                m += "|"
            L0 = min_length + len(m)
            if L < L0:
                raise ValueError(f"Resulting width of {L} is < minimum of {L0}")
            n = len(s)
            if n <= L and not mag:
                return s
            if s[0] in "+- ":
                s = s[1:]
                n = len(s)
            # Limit the width.  The algorithm is to change s to two deques,
            # split in the middle.  Then remove one digit at a time,
            # alternating deques, until the resulting string will fit the
            # current string width.
            lst = list(s)
            split = n//2
            left, right = deque(lst[:split]), deque(lst[split:])
            assert(len(left) + len(right) == n)
            def dqlen():
                return len(left) + len(right) + len(self.ellipsis) + len(sgn)
            while True:
                # Remove a character from the larger of the two deques
                if len(left) > len(right):
                    if len(left) > 1:
                        left.pop()
                        if dqlen() <= L - len(m) - len(sgn):
                            break
                        #print(f"a: {''.join(left)!r} {''.join(right)!r}")
                else:
                    if len(right) > 1:
                        right.popleft()
                        if dqlen() <= L - len(m) - len(sgn):
                            break
                        #print(f"b: {''.join(left)!r} {''.join(right)!r}")
                if len(left) == 1 and len(right) == 1:
                    break
            u = sgn + ''.join(left) + self.ellipsis + ''.join(right) + m
            if len(u) > L:
                msg = dedent(f'''
                Bug in algorithm:
                  L = {L}
                  result = {u!r}
                  len(result) = {len(u)}
                  min_length = {min_length}
                  m = {m!r}  (len = {len(m)})
                ''')
                raise Exception(msg)
            return u
    def trim(self, dq):
        'Implement rtz, rtdp, and rlz for significand dq in deque'
        assert(ii(dq, deque))
        if self._rtz and self._dp in dq:
            while dq and dq[-1] == "0":
                dq.pop()        # Remove trailing 0's
        if self._rtdp and dq and dq[-1] == self._dp:
            dq.pop()            # Remove trailing decimal point
        if self._rlz and len(dq) > 2:
            if dq[0] == "0" and dq[1] == self._dp: 
                dq.popleft()    # Remove leading 0
        return dq
    def significand(self, value, n=None) -> str:
        'Return the signifcand of abs(value) as a string'
        with self.ta:
            self.ta.n = n if n is not None else self.n
            self.ta(abs(value))
            dq = self.ta.dq         # Deque of significand's digits (no dp)
        dq.insert(1, self.dp)
        return ''.join(dq)
    def fix(self, value, n=None, width=None, offset=0) -> str:
        'Return a fixed point representation'
        # Get the exponent e
        if self.ta._number is None or value != self.ta._number:
            self.ta(value)  # Needs disassembling into parts
        if abs(self.ta.e) > self.nchars:
            # I've arbitrarily decided that a number whose exponent will
            # take up more than 1/4 of the screen's digits is too large, so 
            # use sci interpolation.
            return self.sci(value, n=n)
        if 0:   # Old method using Decimal numbers
            x = self.toD(value)
            parts, dq, z = self._get_data(x, n)
            ne = parts.e + 1
            if parts.e >= 0:
                while len(dq) < ne:
                    dq.append(z)
                dq.insert(ne, self.dp)
            else:
                while ne < 0:
                    dq.appendleft(z)
                    ne += 1
                dq.appendleft(self.dp)
                if not self._rlz:
                    dq.appendleft(z)
            if parts.sign:
                dq.appendleft(parts.sign)
            dq = self.trim(dq)
            retval_old = ''.join(dq)
        if 1:   # Use new method with TakeApart implementation
            with self.ta:
                self.ta.n = n if n is not None else self.n
                self.ta(value)  # Disassemble into parts
                sign = self.ta.sign     # Sign ("-" or " ")
                if not self.spc and sign == " ":
                    sign = ""
                if self.sign and sign == "":
                    sign = "+"
                # Note we use fmt instance's decimal point, which is
                # gotten from the locale, not from the number parsed by
                # TakeApart()
                dp = self.dp            # Decimal point
                dq = self.ta.dq         # Deque of significand's digits 
                # Remove any decimal point in dq
                s = ''.join(dq).replace(dp, "")     # Remove dp
                dq = deque(s)
                # Check we only have digits in dq
                if not set(dq).issubset(set(string.digits)):
                    raise Exception("Bug in dq's characters")
                e = self.ta.e           # Integer exponent
                if e < 0:
                    # Number < 1
                    ne = e + 1
                    while ne < 0:
                        dq.appendleft("0")
                        ne += 1
                    dq.appendleft(dp)
                    if not self._rlz:
                        dq.appendleft("0")
                else:
                    # Number >= 1
                    while len(dq) < e + 1:
                        dq.append("0")
                    dq.insert(e + 1, dp)
                # Handle the sign
                if self.sign:   # Always use a sign
                    if sign == " ":
                        sign = "+"
                    dq.appendleft(sign)
                else:
                    if self.spc:  # Use ' ' if positive
                        if sign == "-":
                            dq.appendleft(sign)
                        else:
                            dq.appendleft(" ")
                    else:           # Only use sign if negative
                        if sign == "-":
                            dq.appendleft(sign)
                dq = self.trim(dq)
                retval_new = ''.join(dq)
            assert(set(retval_new).issubset(set("0123456789.,-+ ")))
        if 0:
            # Ensure new and old method get same results (prepend space to
            # old results if >= 0 and self.spc)
            if retval_old[0] != "-" and self.spc:
                retval_old = f" {retval_old}"
            assert retval_new == retval_old, f"{retval_new!r} != {retval_old!r}"
        return retval_new
    def sci(self, value, n=None, width=None, offset=0) -> str:
        'Return a scientific format representation'
        if 0:   # Old method
            x = self.toD(value)
            parts, dq, z = self._get_data(x, n)
            dq.insert(1, self.dp)
            dq.appendleft(parts.sign)
            if dq[-1] == self.dp:
                del dq[-1]
            dq = self.trim(dq)
            if self.u:
                # Use Unicode characters for power of 10
                o = ["✕10"]
                for c in str(parts.e):
                    o.append(self._superscripts[c])
                dq.extend(o)
            else:
                dq.extend(["e", str(parts.e)])
            return ''.join(dq)
        else:
            n = n if n is not None else self.n
            ta = self.ta
            with ta:
                ta.n = n
                ta(value)
                sgn = ta.sign
                if not self.spc and sgn == " ":
                    sgn = ""
                # Get significand
                dq = deque(list(ta.ld + ta.dp + ta.other))
                dq = self.trim(dq)
                sig = [sgn, ''.join(dq), "e", str(ta.e)]
                return ''.join(sig)
    def eng(self, value, fmt="eng", n=None, width=None, offset=0) -> str:
        '''Return an engineering format representation.  Suppose value
        is 31415.9 and n is 3.  Then fmt can be:
            "eng"    returns "31.4e3"
            "engsi"  returns "31.4 k"
            "engsic" returns "31.4k" (the SI prefix is cuddled)
        Note:  cuddling is illegal SI syntax, but it's sometimes useful in
        program output.
        '''
        x = self.toD(value)
        fmt = fmt.strip().lower()
        parts, dq, z = self._get_data(x, n)
        eng_step = 3
        div, rem = divmod(parts.e, eng_step)
        k = rem + 1 
        while len(dq) < k:
            dq.append(z)
        dq.insert(k, self.dp)
        if dq[-1] == self.dp:
            del dq[-1]
        dq.appendleft(parts.sign)
        dq = self.trim(dq)
        exponent = ["e", f"{eng_step*div}"]
        try:
            prefix = self._SI_prefixes[div]
        except KeyError:
            prefix = None
        if fmt == "eng":
            if self.u:      # Use Unicode characters for power of 10
                o = ["✕10"]
                for c in str(eng_step*div):
                    o.append(self._superscripts[c])
                dq.extend(o)
            else:
                dq.extend(exponent)
        elif fmt == "engsi":
            dq.extend(exponent) if prefix is None else dq.extend([" ", prefix])
        elif fmt == "engsic":
            dq.extend(exponent) if prefix is None else dq.extend([prefix])
        else:
            raise ValueError(f"'{fmt}' is an unrecognized format")
        return ''.join(dq)
    def Complex(self, value, fmt=None, n=None) -> str:
        '''value is a complex number.  Return a string in the form of 
        'a + bi'.
        '''
        if fmt is not None:
            if fmt not in "fix sci eng engsi engsic".split():
                raise ValueError(f"'{fmt}' is unrecognized format string")
        else:
            fmt = self.default
        e = TypeError(f"value {value!r} must be complex")
        if have_mpmath:
            if not ii(value, (complex, mpmath.mpc)):
                raise e
        else:
            if not ii(value, complex):
                raise e
        if self.polar:
            r = value.real
            i = value.imag
            s = "" if self.cuddled else " "
            mag = (r*r + i*i)**(0.5)
            if have_mpmath:
                angle = mpmath.atan2(i, r)
                if self._deg:
                    angle *= 180/mpmath.pi
            else:
                mag = (r*r + i*i)**(0.5)
                angle = math.atan2(i, r)
                if self._deg:
                    angle *= 180/math.pi
            a = self(mag, fmt=fmt, n=n)
            b = self(angle, fmt=fmt, n=n)
            if self._deg:
                b += "°"
            if self.ul:
                return f"{a}{s}{t(attr='ul')}∕{s}{b}{t.n}"
            else:
                return f"{a}{s}∠{s}{b}"
        else:
            sr = self(value.real)
            si = self(value.imag)
            if self.comp:
                s = "" if self.cuddled else " "
                return f"({sr},{s}{si})"
            # Get imaginary sign
            sign = "+"
            if si[0] == "-":
                sign = "-"
                si = si[1:]
            s = "" if self.cuddled else " "
            ret = f"{sr}{s}{sign}{s}{si}{self._imag_unit}"
            return ret
    def __call__(self, value, fmt: str=None, n: int=None, width=None, offset=0) -> str:
        '''Format value with the default "fix" formatter.  n overrides
        self.n digits.  fmt can be "fix", "sci", "eng", "engsi", or
        "engsic".  If it is None, then self.default is used.
        '''
        if fmt is not None:
            if fmt not in "fix sci eng engsi engsic".split():
                raise ValueError(f"'{fmt}' is unrecognized format string")
        else:
            fmt = self.default
        if n is None:
            n = self._n
        else:
            if not ii(n, int):
                raise TypeError("n must be an integer")
            if n < 0:
                raise ValueError("n must be >= 0")
        if ii(value, complex):
            return self.Complex(value, fmt=fmt, n=n)
        elif have_mpmath and ii(value, mpmath.mpc):
            return self.Complex(value, fmt=fmt, n=n)
        assert(n is not None)
        x = value
        if ii(value, (int, float, Decimal)):
            return self.call_Decimal(value, fmt=fmt, n=n)
        else:
            return self.call_mpmath(value, fmt=fmt, n=n)
    def call_Decimal(self, value, fmt: str="fix", n: int=None) -> str:
        'Handle formatting with the Decimal type'
 
        assert(ii(value, (int, float, Decimal)))
        try:
            x = self.toD(value)
            abs(x)
        except (decimal.InvalidOperation, decimal.Overflow) as e:
            # If we get here, we likely have a value number that has an
            # exponent too large or small for the default Decimal context.
            # We'll return a sci formatted value.
            s = str(value).lower()
            # Remove minus or plus signs
            minus = ""
            if s[0] == "+":
                s = s[1:]
            elif s[0] == "-":
                s = s[1:]
                minus = "-"
            try:
                # m will be the significand, e will be the exponent
                m, e = s.split("e")
            except Exception:
                raise ValueError(f"{value!r} can't be formatted")
            radix = "."
            if "," in m:
                radix = ","
            m = m.replace(radix, "")
            m = m[:self.n]
            if len(m) > 1:
                m = minus + m[0] + radix + m[1:]
            if e[0] == "+":
                e = e[1:]
            if self.u:
                # Use Unicode characters for power of 10
                o = ["✕10"]
                for c in e:
                    o.append(self._superscripts[c])
                return m + ''.join(o)
            return m + "e" + e
        if fmt == "fix":
            if value:
                if x and self.high is not None and abs(x) > self.high:
                    return self.sci(x, n)
                elif x and self.low is not None and abs(x) < self.low:
                    return self.sci(x, n)
                return self.fix(x, n)
            else:
                return self.fix(x, n)
        elif fmt == "sci":
            return self.sci(x, n)
        else:
            return self.eng(x, n=n, fmt=fmt)
    def call_mpmath(self, value, fmt: str="fix", n: int=None) -> str:
        assert(ii(value, mpmath.mpf))
        low, high = mpmath.mpf(str(self.low)), mpmath.mpf(str(self.high))
        if fmt == "fix":
            if value:
                if abs(value) > high:
                    return self.sci(value, n)
                if abs(value) < low:
                    return self.sci(value, n)
                return self.fix(value, n)
            else:
                return self.fix(value, n)
        elif fmt == "sci":
            return self.sci(value, n)
        else:
            return self.eng(value, n=n, fmt=fmt)
    if 1:   # Properties
        @property
        def default(self) -> str:
            'Default formatting method'
            return self._default
        @default.setter
        def default(self, value):
            'Default formatting method'
            if value not in "fix sci eng engsi engsic".split():
                raise TypeError("value must be fix, sci, eng, engsi, or engsi")
            self._default = value
        @property
        def dp(self) -> str:
            'Decimal point string'
            return self._dp
        @dp.setter
        def dp(self, value):
            'Only "." or "," allowed for decimal point'
            if not ii(value, str) or len(value) > 1 or value not in ".,":
                raise TypeError("value must be either '.' or ','")
            self._dp = value
        @property
        def high(self):
            'Use "sci" format if abs(x) is > high and not None'
            return self._high
        @high.setter
        def high(self, value):
            self._high = None if value is None else abs(D(str(value)))
        @property
        def int(self):
            'How to format integers with self.fmtint()'
            return self._int
        @int.setter
        def int(self, value):
            s = "None hex oct dec bin"
            if value not in s.split():
                raise ValueError(f"value must be one of {' '.join(s)}")
            self._int = value
        @property
        def low(self):
            'Use "sci" format if abs(x) is < low and not None'
            return self._low
        @low.setter
        def low(self, value):
            self._low = None if value is None else abs(D(str(value)))
        @property
        def n(self) -> int:
            'Number of digits (integer >0 0)'
            return self._n
        @n.setter
        def n(self, value):
            if not(ii(value, int) or value < 0):
                raise ValueError("value must be integer >= 0")
            self._n = value
            self.ta._n = value
        @property
        def rtz(self) -> bool:
            '(bool) Remove trailing zeros after radix if True'
            return self._rtz
        @rtz.setter
        def rtz(self, value):
            self._rtz = bool(value)
        @property
        def rtdp(self) -> bool:
            '(bool) Remove trailing radix if True'
            return self._rtdp
        @rtdp.setter
        def rtdp(self, value):
            self._rtdp = bool(value)
        @property
        def rlz(self) -> bool:
            '(bool) Remove leading zero if True'
            return self._rlz
        @rlz.setter
        def rlz(self, value):
            self._rlz = bool(value)
        @property
        def sign(self) -> bool:
            "Always include numbers' sign"
            return self._sign
        @sign.setter
        def sign(self, value):
            self._sign = bool(value)
        @property
        def spc(self) -> bool:
            'Add " " to numbers >= 0 where "-" goes'
            return self._spc
        @spc.setter
        def spc(self, value):
            self._spc = bool(value)
        @property
        def strict(self):
            'If True, n must be <= precision'
            return self._strict
        @strict.setter
        def strict(self, value):
            self._strict = self.ta.strict = bool(value)
        @property
        def u(self) -> bool:
            '(bool) Use Unicode in "sci" and "eng" formats if True'
            return self._u
        @u.setter
        def u(self, value):
            self._u = bool(value)
    if 1:   # Complex number properties
        @property
        def imag_unit(self) -> str:
            'Imaginary unit string'
            return self._imag_unit
        @imag_unit.setter
        def imag_unit(self, value):
            assert(ii(value, str) and len(value) > 0)
            self._imag_unit = value
        @property
        def polar(self) -> bool:
            '(bool) Show complex numbers in polar form'
            return self._polar
        @polar.setter
        def polar(self, value):
            self._polar = bool(value)
        @property
        def deg(self) -> bool:
            "(bool) Show complex number's angles in degrees"
            return self._polar
        @deg.setter
        def deg(self, value):
            self._deg = bool(value)
        @property
        def cuddled(self) -> bool:
            "(bool) Use '1+2i' form if True, '1 + 2i' form if False"
            return self._cuddled
        @cuddled.setter
        def cuddled(self, value):
            self._cuddled = bool(value)
        @property
        def ul(self) -> bool:
            "(bool) Underline the argument when displaying polar form"
            return self._ul
        @ul.setter
        def ul(self, value):
            self._ul = bool(value)
        @property
        def comp(self) -> bool:
            "(bool) Show complex number in (re,im) form"
            return self._comp
        @comp.setter
        def comp(self, value):
            self._comp = bool(value)
if 0:   # Core methods
    def _TakeApart(x, n=3):
        '''Take apart a real number into digits, decimal point, and
        exponent for further string interpolation processing.  Returns an
        Apart namedtuple instance.  Supports integer, common floating point
        types and python fractions.
 
        Examples:
            TakeApart(-39578574)
                Apart(sign='-', ld='3', dp='.', other='96', exp=7)
            TakeApart(1/mpmath.fac(100))
                Apart(sign='', ld='1', dp='.', other='07', exp=-158)
        '''
        assert(ii(n, int) and n > 0)
        # Convert either to a Decimal or mpf
        if ii(x, (int, float, decimal.Decimal)):
            y = decimal.Decimal(str(x))
        elif ii(x, fractions.Fraction):
            y = decimal.Decimal(x.numerator)/decimal.Decimal(x.denominator)
        elif have_mpmath and ii(x, mpmath.mpf):
            y = x
        else:
            raise TypeError(f"{x!r} is not a supported number type")
        # Process
        sign, yabs = " ", y
        if y < 0:
            sign = "-"
            yabs = -y
        if have_mpmath and ii(yabs, mpmath.mpf):
            e = int(mpmath.floor(mpmath.log10(yabs))) if yabs else 0
            s = mpmath.nstr(mpmath.mpf(yabs/10**e), n)
            assert("." in s and len(s) > 1)    # mpmath seems to use only "."
            dp = s[1]
            t = s.replace(".", "").replace(",", "")     # Remove radix
            while len(t) < n:   # nstr() returns 1.0 for 1 whatever n is
                t += "0"
            if len(t) > n: # nstr(1, 1) returns 1.0 for n = 1
                t = t[:n]
            assert(len(t) == n if yabs else 1)
            leaddigit, otherdigits = t[0], t[1:]
            return Apart(sign, leaddigit, dp, otherdigits, e)
        else:
            yabs = abs(y)
            assert(ii(y, decimal.Decimal))
            ys = f"{yabs:.{n - 1}e}".lower()    # Get sci form to n digits
            s, e = ys.split("e")
            dp = "," if "," in s else "."
            ld, other = (s, "") if len(s) == 1 else s.split(dp)
            # For zero, Decimal formats an exponent to n - 1; we want 0
            e = int(e) if y else 0
            return Apart(sign, ld, dp, other, e)
if 1:   # Convenience instances
    fmt = Fmt()
    ta = TakeApart()
# Development area
if 1 and __name__ == "__main__": 
    '''
    Need fix sci eng __call__
    '''
    M = mpmath
    fmt.brief = 1
    M.mp.dps = 20
    x = M.mpf("3.45678901234567890")
    print(f"x = {x}")
    print(f"fmt(x) = {fmt(x)}")
    exit()

if __name__ == "__main__": 
    if 1:   # Header
        # Standard imports
            from functools import partial
            from decimal import localcontext
            from math import pi
            import getopt
            import os
            import pathlib
            import sys
        # Custom imports
            from fpformat import FPFormat
            from lwtest import run, raises, Assert
            from wrap import dedent
            import decimalmath
        # Global variables
            Fraction = fractions.Fraction
            P = pathlib.Path
            d = {}      # Options dictionary
            # Set up colors for demo
            u = use_colors = bool(os.environ.get("DPRC", False))
            t.t = t() if u else ""          # Title
            t.u = t("ornl") if u else ""    # Normal float formatting
            t.f = t("sky") if u else ""     # Feature being demonstrated
            t.fix = t("whtl") if u else ""  # Fixed point
            t.sci = t("yell") if u else ""  # Scientific notation
            t.eng = t("grnl") if u else ""  # Engineering notation
            t.si = t("magl") if u else ""   # Engsi notation
            t.em = t("purl") if u else ""   # Emphasis
            t.err = t("redl") if u else ""  # Error in digits
    def Demo():
        f = fmt
        t.print(dedent(f'''
        {t.t}Demonstration of Fmt class features:  {t.em}f = Fmt(){t.n}
            Formatting (string interpolation) is gotten by calling the Fmt instance
            as a function:  {t.f}f(x){t.n}.  x can be an integer, real, or complex number.
        '''))
        s = "pi*1e5"
        x = eval(s)
        # Standard formatting
        print(dedent(f'''
        {t.t}Usual python float formatting:{t.n}  x = {s}
            repr(x) = str(x) = {t.u}{x!s}{t.n}
            Though accurate, there are too many digits for easy comprehension.  The
            Fmt class defaults to showing {f.n} significant figures and the trailing
            radix helps you identify that it's a floating point number.
        '''))
        t.print(f"{t.em}Fixed point formatting")
        print(f"  {t.f}f(x){t.n} = {t.fix}{f(x)}{t.n} (defaults to {f.n} significant figures)")
        t.print(f"{t.t}Remove trailing decimal point:  {t.f}f.rtdp = True")
        f.rtdp = True
        t.print(f"  {t.f}f(x) = {t.fix}{f(x)}")
        f.rtdp = False
        # More figures
        n = 10
        t.print(f"{t.t}Set to {n} significant figures:  {t.f}f.n = {n}")
        f.n = n
        t.print(f"  {t.f}f(x) = {t.fix}{f(x)}")
        t.print(f"{t.t}Override f.n significant figures:")
        t.print(f"  {t.f}f(x, n=5){t.n} = {t.fix}{f(x, n=5)}")
        t.print(f"{t.t}Remove trailing significant zeros:")
        t.print(f"  {t.f}f(1/4) = {t.fix}{f(1/4)} f.rtz = False")
        f.rtz = True
        t.print(f"  {t.f}f(1/4) = {t.fix}{f(1/4)} {' '*8}f.rtz = True")
        f.rtz = False
        t.print(f"{t.t}Remove leading zero of decimal fraction:")
        t.print(f"  {t.f}f(1/4) = {t.fix}{f(1/4)} f.rlz = False")
        f.rlz = True
        t.print(f"  {t.f}f(1/4) = {t.fix}{f(1/4)} {' '*1}f.rlz = True")
        f.rlz = False
        f.n = 3
        # Change scientific notation thresholds
        t.print(f"{t.em}Scientific notation{t.n}    {t.t}Change transition thresholds to scientific notation:")
        f.high = 1e6
        f.low = 1e-6
        t.print(f"  {t.f}f.high{t.n} = {t.sci}{f.sci(f.high, n=1)}")
        t.print(f"  {t.f}f.low{t.n}  = {t.sci}{f.sci(f.low, n=1)}")
        print(f"  {t.fix}{f(pi*1e5)}{t.n} < f.high so use fix")
        print(f"  {t.sci}{f(pi*1e6)}{t.n} > f.high so use sci")
        print(f"  {t.fix}{f(pi*1e-6)}{t.n} > f.low so use fix")
        print(f"  {t.sci}{f(pi*1e-7)}{t.n} < f.low so use sci")
        # Get scientific and engineering notations
        t.print(f"{t.t}Force use of scientific and engineering notation")
        t.print(f"  sci:  {t.f}f.sci(pi*1e-7){t.n}        = {t.sci}{f.sci(pi*1e-7)}")
        t.print(f"        {t.f}f(pi*1e-7, fmt='sci'){t.n} = {t.sci}{f(pi*1e-7, fmt='sci')}")
        t.print(f"  eng:  {t.f}f.eng(pi*1e-7){t.n}        = {t.eng}{f.eng(pi*1e-7)}")
        t.print(f"        {t.f}f(pi*1e-7, fmt='eng'){t.n} = {t.eng}{f(pi*1e-7, fmt='eng')}")
        # Use Unicode characters for scientific notation
        f.u = True
        t.print(f"{t.em}Unicode    {t.n}{t.t}Set f.u to True to use Unicode characters in sci and eng exponents:")
        t.print(f"  {t.f}f.sci(pi*1e6)){t.n} = {t.sci}{f.sci(pi*1e6)}{t.n}   f.u = True")
        t.print(f"  {t.f}f.eng(pi*1e-7){t.n} = {t.eng}{f.eng(pi*1e-7)}{t.n}   f.u = True")
        f.u = False
        # Set low & high to None to always get fixed point
        t.print(f"{t.em}Always use fixed point")
        f.low = f.high = None
        t.print(f"  {t.t}Set {t.f}f.low{t.n} and {t.f}f.high{t.n} to None always use fixed point:")
        t.print(f"  {t.f}f(pi*1e-27){t.n} = {t.fix}{f(pi*1e-27)}")
        t.print(f"  {t.f}f(pi*1e57){t.n} = {t.fix}{f(pi*1e57)}")
        print(f"  Large and small enough numbers will still require scientific notation.")
        f.high = 1e6
        f.low = 1e-6
        # Big exponents
        print(dedent(f'''
        {t.em}Big numbers{t.n}   {t.t}Fixed point, scientific, and engineering formatting should work
        for numbers of arbitrary magnitudes as long as an exception isn't encountered.
        For very large or small numbers, install the optional mpmath library.
        '''))
        t.print(f"  {t.f}f(Decimal('1e999999')){t.n} = {t.sci}{f(D('1e999999'))}")
        t.print(f"  {t.f}f(Decimal('1e-999999')){t.n} = {t.sci}{f(D('1e-999999'))}")
        try:
            f(D("1e1000000"))
        except decimal.Overflow:
            t.print(f'  {t.f}f(Decimal("1e1000000")){t.n}', "results in overflow")
        t.print(f'  {t.f}f(Decimal("1e-100000000")){t.n}', "underflow that gives 0")
        # Decimals with lots of digits
        n = 20
        t.print(dedent(f'''
        {t.em}Significant figures{t.n}    {t.t}You can ask for any number of significant figures, but
        some displayed digits can be meaningless if they are beyond the number's
        allowed precision.  Below, digits in error are shown in red, as a python float
        is only good to about 15 digits.  The expression evaluated is
        100000*sin(pi/4) to {n} digits.
        '''))
        with decimal.localcontext() as ctx:
            ctx.prec = n
            x = 100000*decimalmath.sin(decimalmath.pi()/4)
            # mpmath's result to 30 significant figures
            mp = "70710.6781186547524400844362104822"
            #    "70710.678118654745049"    float to 20 figures
            #                     ^ Incorrect digits
            t.print(f"  x = {t.fix}{fmt(x, n=n)}{t.n} (Decimal calculation)")
            y = 100000*math.sin(math.pi/4)
            ys, m = fmt(y, n=n), 16
            bad = f"{t.fix}{ys[:m]}{t.err}{ys[m:]}{t.n}"
            t.print(f"  x = {bad} (float calculation)")
            n = 4
            t.print(f"  sci(x)    to {n} digits = {t.sci}{f(x, 'sci', n=n)}")
            n = 5
            t.print(f"  eng(x)    to {n} digits = {t.eng}{f(x, 'eng', n=n)}")
            n = 6
            t.print(f"  engsi(x)  to {n} digits = {t.si}{f(x, 'engsi', n=n)}")
            n = 7
            t.print(f"  engsic(x) to {n} digits = {t.si}{f(x, 'engsic', n=n)}")
        t.print(dedent(f'''
        {t.em}SI notation{t.n}    The {t.f}f.engsi{t.n} method supplies an SI prefix after the number to
        indicate the number's magnitude.  You can then append a physical unit string
        to get proper SI syntax:  {t.u}{f(x, 'engsi')}Ω{t.n}.  {t.f}f.engsic{t.n} does the same except the prefix
        is cuddled: {t.u}{f(x, 'engsic')}Ω{t.n}.
        ''', n=8))
        # Context manager
        x = 2**0.5
        t.print(dedent(f'''
        {t.em}Context manager{t.n}    A Fmt class instance is a context manager that lets you
        change attributes in a with statement and have them restored when the with
        block is over:
            x = 2**0.5
            print(fmt(x))        -->  {t.f}{fmt(x)}{t.n}
            with fmt:
                fmt.n = 8
        ''', n=8))
        with fmt:
            fmt.n = 8
            t.print(f"        print(fmt(x))    -->  {t.f}{fmt(x)}{t.n}")
        t.print(f"    print(fmt(x))        -->  {t.f}{fmt(x)}{t.n}")
        # Complex numbers
        z = complex(3.45678, -6.78901)
        fmt.imag_unit = "j"
        t.print(dedent(f'''
        {t.em}Complex numbers{t.n}    These are handled by formatting each floating point
        component separately.  Let z = complex(3.45678, -6.78901):
            str(z) = {t.f}{str(z)}{t.n}
            fmt(z) = {t.f}{fmt(z)}{t.n}
        Use the Fmt object's attributes to change the formatted form:
        ''', n=8))
        w, sp = 25, " "*4
        fmt.imag_unit = "i"
        s = 'fmt.imag_unit = "i"'
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n}")
        fmt.cuddled = True
        s = "fmt.cuddled = True"
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n}")
        fmt.polar = True
        fmt.deg = False
        s = "fmt.polar = True"
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n} (in radians)")
        fmt.deg = True
        s = "fmt.deg = True"
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n} (in degrees)")
        fmt.ul = True
        s = "fmt.ul = True"
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n}")
        fmt.polar = False
        fmt.comp = True
        fmt.cuddled = True
        s = "fmt.comp = True"
        t.print(f"{sp}{s:{w}s} {t.f}{fmt(z)}{t.n}  (fmt.cuddled True)")
        fmt.cuddled = False
        t.print(f"{sp}{'':{w}s} {t.f}{fmt(z)}{t.n} (fmt.cuddled False)")
        t.print(f"The fmt.ul underlining won't work unless your terminal supports it.")
        if not use_colors:
            print(f"Set the environment variable DPRC to true to see colorized output.")
    if 1:   # Test code 
        def Init():
            'Make sure test environment is set up in a repeatable fashion'
            fmt = Fmt()
            fmt.n = 3
            return fmt
        def Test_Basics():
            f = Init()
            s = f(pi)
            for x, result in (
                (pi, "3.14"),
                (-pi, "-3.14"),
                (pi*1e99, "3.14e99"),
                (-pi*1e99, "-3.14e99"),
                (pi*1e-99, "3.14e-99"),
                (-pi*1e-99, "-3.14e-99"),
            ):
                s = f(x)
                Assert(s == result)
            # Test simple numbers with fixed point
            for x, n, result in (
                (0, 1, "0."),
                (1, 1, "1."),
                (-1, 1, "-1."),
                (0, 2, "0.0"),
                (1, 2, "1.0"),
                (-1, 2, "-1.0"),
                (0, 3, "0.00"),
                (1, 3, "1.00"),
                (-1, 3, "-1.00"),
                (0, 8, "0.0000000"),
                (1, 8, "1.0000000"),
                (-1, 8, "-1.0000000"),
            ):
                f.n = n
                s = f(x)
                Assert(s == result)
            # Test with numbers near 1
            f = Init()
            x = 0.99
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "0.99")
            Assert(f(-x, n=1) == "-1.")
            Assert(f(-x, n=2) == "-0.99")
            x = 0.999999
            raises(ValueError, f, x, n=-1)
            s = "0.9999989999999999712443354838"
            Assert(f(x, n=0) == s)
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "1.0")
            Assert(f(x, n=3) == "1.00")
            Assert(f(x, n=4) == "1.000")
            Assert(f(x, n=5) == "1.0000")
            Assert(f(x, n=6) == "0.999999")
            Assert(f(x, n=7) == "0.9999990")
            raises(ValueError, f, -x, n=-1)
            Assert(f(-x, n=0) == "-" + s)
            Assert(f(-x, n=1) == "-1.")
            Assert(f(-x, n=2) == "-1.0")
            Assert(f(-x, n=3) == "-1.00")
            Assert(f(-x, n=4) == "-1.000")
            Assert(f(-x, n=5) == "-1.0000")
            Assert(f(-x, n=6) == "-0.999999")
            Assert(f(-x, n=7) == "-0.9999990")
        def Test_toD():
            f = Init().toD
            # int and str
            for i in (-1, 0, 1, "-1", "0", "1", "inf", "-inf"): 
                Assert(f(i) == D(i))
                Assert(f(D(i)) == D(i))
            for i in (-1_000, 1_000, "-1_000", "1_000"): 
                Assert(f(i) == D(i))
                Assert(f(D(i)) == D(i))
            # float and str
            for i in (-1., 0., 1., "-1.", "0.", "1."): 
                Assert(f(i) == D(i))
                Assert(f(D(i)) == D(i))
            for i in (-0.00_1, 0.00_1, 
                        -1_000., 1_000.,
                        "-0.00_1", "0.00_1",
                        "-1_000.", "1_000."): 
                Assert(f(i) == D(i))
                Assert(f(D(i)) == D(i))
            # Fraction
            n, d = 3, 8
            x = Fraction(n, d)
            Assert(f(x) == D(n/d))
            # Fraction string
            Assert(f(f"{n}/{d}") == D(n/d))
            # mpmath 
            if have_mpmath:
                mpf = mpmath.mpf
                n = 50
                mpmath.mp.dps = n
                x = mpf(2)**mpf(1/2)
                with decimal.localcontext() as ctx:
                    ctx.prec = n
                    Assert(f(x) == D(2)**D(1/2))
        def Test_Fix():
            'This is where the majority of execution time is'
            def TestTrimming():
                f = Init()
                x = 31.41
                f.n = 6
                f.rtz = 0
                Assert(f(x, fmt="fix") == "31.4100")
                Assert(f(x, fmt="sci") == "3.14100e1")
                Assert(f(x, fmt="eng") == "31.4100e0")
                # Remove trailing zeros
                f.rtz = 1
                Assert(f(x, fmt="fix") == "31.41")
                Assert(f(x, fmt="sci") == "3.141e1")
                Assert(f(x, fmt="eng") == "31.41e0")
                # Remove decimal point
                f.rtdp = 1
                f.n = 2
                Assert(f(x, fmt="fix") == "31")
                Assert(f(x, fmt="sci") == "3.1e1")
                Assert(f(x, fmt="eng") == "31e0")
                # Remove leading zero
                f = Init()
                x = 0.00732
                f.rlz = False
                Assert(f(x, fmt="fix") == "0.00732")
                f.rlz = True
                Assert(f(x, fmt="fix") == ".00732")
                # Use alternate string for decimal point
                f = Init()
                x = -31.41
                f.dp = ","
                Assert(f(x) == "-31,4")
                with raises(TypeError) as y:
                    f.dp = "q"
            def TestHuge(n, digits=3):
                f = Init()
                f.n = digits
                x = D(str(pi) + f"e{n}")
                f.high = None
                s = f(x, fmt="fix")
                if n == 999999:
                    # Note sci is used
                    Assert(s == "3.14e999999")
                else:
                    Assert(s.startswith("3140"))
            def TestTiny(n, digits=3):
                f = Init()
                f.n = digits
                x = D(str(pi) + f"e-{n}")
                f.low = None
                s = f(x, fmt="fix")
                if n == 999999:
                    # Note sci is used
                    Assert(s == "3.14e-999999")
                else:
                    Assert(s.endswith("0314"))
            def TestLotsOfDigits(n, digits=3):
                f = Init()
                f.n = digits
                with localcontext() as ctx:
                    ctx.prec = n
                    t = "0." + "1"*n
                    x = D(t)
                    f.n = n
                    s = f(x)
                    Assert(s == t)
                    s = f(x, n=n)
                    Assert(s == t)
            def TestBigInteger(n):
                d = ["1234567890"]*n
                s = ''.join(d)
                with localcontext() as ctx:
                    ctx.prec = len(s) + 1
                    f, x = Init(), D(s)
                    f.high = None
                    for m in range(1, len(s)):
                        t = f(x, n=m)
                        begin = t[:m]
                        end = ("0"*(len(s) - m)) + "."
                        Assert(t == begin + end)
                if 1:
                    # Here's a second test with somewhat more random digits.
                    s = "305834907503304830840485408347390568489537430834"
                    n = int(1e4/len(s))  # How many digits
                    x = D(s*n)
                    f = Init()
                    f.high = None
                    t = f(x, fmt="fix")
                    Assert(t == "3.06e9983")
            def Test_spc():
                'Test .spc and .sign'
                f = Init()
                x = 0.2846
                s = f(x)
                Assert(s == "0.285")
                f.spc = True
                s = f(x)
                Assert(s == " 0.285")
                f.sign = True
                s = f(x)
                Assert(s == "+0.285")
                f.spc = False
                s = f(x)
                Assert(s == "+0.285")
                x = -0.2846
                s = f(x)
                Assert(s == "-0.285")
            def Test_rlz():
                f = Init()
                x = 0.2846
                s = f.fix(x)
                Assert(s == "0.285")
                x *= -1
                s = f.fix(x)
                Assert(s == "-0.285")
                x *= -1
                # Turn on rlz
                f.rlz = True
                s = f.fix(x)
                Assert(s == ".285")
                x *= -1
                s = f.fix(x)
                Assert(s == "-.285")
            for n in (999999,  # Largest exponent allowed by default Decimal context
                    100, 20, 3):
                TestTiny(n)
                TestHuge(n)
                TestLotsOfDigits(n)
            TestTrimming()
            TestBigInteger(20)
            Test_spc()
            Test_rlz()
        def Test_Eng():
            '''Compare to fpformat's results.  Only go up to 15 digits because
            fpformat uses floats.
            '''
            s, numdigits = "1.2345678901234567890", 15
            x = D(s)
            fp = FPFormat()
            fp.expdigits = 1
            fp.expsign = False
            def Test_eng():
                f = Init()
                for n in range(1, numdigits + 1):
                    t = f.eng(x, n=n)
                    fp.digits(n)
                    expected = fp.eng(x)
                    if n == 1:
                        expected = expected.replace(".", "")
                    Assert(t == expected)
            def Test_engsi():
                f = Init()
                for n in range(1, numdigits + 1):
                    t = f.eng(x, n=n, fmt="engsi")
                    fp.digits(n)
                    expected = fp.engsi(x)
                    if n == 1:
                        expected = expected.replace(".", "")
                    Assert(t == expected)
            def Test_engsic():
                f = Init()
                for n in range(1, numdigits + 1):
                    t = f.eng(x, n=n, fmt="engsic")
                    fp.digits(n)
                    expected = fp.engsic(x)
                    if n == 1:
                        expected = expected.replace(".", "")
                    Assert(t == expected)
            Test_eng()
            Test_engsi()
            Test_engsic()
        def Test_Sci():
            def CompareToFPFormat():
                "Compare to fpformat's results"
                s, numdigits = "1.2345678901234567890", 10
                fp = FPFormat()
                fp.expdigits = 1
                fp.expsign = False
                f = Init()
                f.rtdp = 1
                for e in range(6):
                    for n in range(1, numdigits + 1):
                        x = D(s + f"e{e}")
                        t = f.sci(x, n=n)
                        fp.digits(n)
                        expected = fp.sci(x)
                        if n == 1:
                            expected = expected.replace(".", "")
                        Assert(t == expected)
            def Other():
                f = Init()
            CompareToFPFormat()
            Other()
        def Test_Big():
            '''The Fmt object uses Decimal numbers to do the formatting.  This
            works for most stuff, but will fail when dealing with exponents
            beyond around a million, the default for Decimal.  This should only
            happend for mpmath.mpf numbers.  In this case, simple sci
            formatting is done.
            '''
            if not have_mpmath:
                return
            mpmath.mp.dps = 50
            x = mpmath.mpf(mpmath.pi)**(10**50)
            s = "1.81e49714987269413385435126828829089887365167832438044"
            Assert(fmt(x, n=3) == s)
        def Test_Default():
            'Verify the default formatting attribute works'
            fmt = Fmt()
            fmt.n = 3
            x = math.pi*1e4
            Assert(fmt(x) == "31400.")
            fmt.default = "sci"
            Assert(fmt(x) == "3.14e4")
            fmt.default = "eng"
            Assert(fmt(x) == "31.4e3")
            fmt.default = "engsi"
            Assert(fmt(x) == "31.4 k")
            fmt.default = "engsic"
            Assert(fmt(x) == "31.4k")
        def Test_TakeApart():
            mpf = mpmath.mpf if have_mpmath else float
            if 1:   # Show supported types get the same string interpolation
                # Function to convert an Apart to a string
                g = lambda x: ''.join(x[:4]) + f"e{x[4]}"
                k, u, m = 5, "1.23456", 300
                TA = TakeApart()
                for n in range(1, 10):
                    TA.n = n
                    for i in (-1, 0, 1, 2, 1234, -1234):
                        expected = TA(i)
                        for x in (float(i), mpf(i), D(i), F(i)):
                            Assert(TA(x) == expected)
                            Assert(g(TA(x)) == g(expected))
                    # Large negative float
                    expected, s = TA(int(-123456)*10**(m - k)), f"-{u}e{m}"
                    for typ in (float, mpf, D, F):
                        y = TA(typ(s))
                        Assert(y == expected)
                        Assert(g(y) == g(expected))
                    # Large positive float
                    expected, s = TA(int(123456)*10**(m - k)), f"{u}e{m}"
                    for typ in (float, mpf, D, F):
                        y = TA(typ(s))
                        Assert(y == expected)
                        Assert(g(y) == g(expected))
                    # Small negative float
                    expected, s = TA(int(-123456)/10**(m + k)), f"-{u}e-{m}"
                    for typ in (float, mpf, D, F):
                        y = TA(typ(s))
                        Assert(y == expected)
                        Assert(g(y) == g(expected))
                    # Small positive float
                    expected, s = TA(int(123456)/10**(m + k)), f"{u}e-{m}"
                    for typ in (float, mpf, D, F):
                        y = TA(typ(s))
                        Assert(y == expected)
                        Assert(g(y) == g(expected))
            if 0:
                n, w, s, sp, f = 5, 20, "-123.456e300", " "*2, F(1, 1)
                TA = partial(TakeApart, n=n)
                # This printout is handy to compare things for equality
                print("0")
                print(f"{sp}{'int(0)':{w}s} {TA(0)}")
                print(f"{sp}{'float(0)':{w}s} {TA(float(0))}")
                print(f"{sp}{'mpf(0)':{w}s} {TA(mpf(0))}")
                print(f"{sp}{'Decimal(0)':{w}s} {TA(D(0))}")
                print(f"{sp}{'Fraction(0)':{w}s} {TA(F(0, 1))}")
                #
                print("1")
                print(f"{sp}{'int(1)':{w}s} {TA(1)}")
                print(f"{sp}{'float(1)':{w}s} {TA(float(1))}")
                print(f"{sp}{'mpf(1)':{w}s} {TA(mpf(1))}")
                print(f"{sp}{'Decimal(1)':{w}s} {TA(D(1))}")
                print(f"{sp}{'Fraction(1, 1)':{w}s} {TA(F(1, 1))}")
                #
                print("-1")
                print(f"{sp}{'int(-1)':{w}s} {TA(-1)}")
                print(f"{sp}{'float(-1)':{w}s} {TA(float(-1))}")
                print(f"{sp}{'mpf(-1)':{w}s} {TA(mpf(-1))}")
                print(f"{sp}{'Decimal(-1)':{w}s} {TA(D(-1))}")
                print(f"{sp}{'Fraction(-1, 1)':{w}s} {TA(F(-1, 1))}")
                #
                print("-123.456e300")
                print(f"{sp}{'int':{w}s} {TA(int(-123456)*10**297)}")
                print(f"{sp}{'float':{w}s} {TA(float(s))}")
                print(f"{sp}{'mpf':{w}s} {TA(mpf(s))}")
                print(f"{sp}{'Decimal':{w}s} {TA(D(s))}")
                print(f"{sp}{'Fraction':{w}s} {TA(f.from_decimal(D(s)))}")
                #
                print("123.456e300")
                print(f"{sp}{'int':{w}s} {TA(int(123456)*10**297)}")
                print(f"{sp}{'float':{w}s} {TA(float(s[1:]))}")
                print(f"{sp}{'mpf':{w}s} {TA(mpf(s[1:]))}")
                print(f"{sp}{'Decimal':{w}s} {TA(D(s[1:]))}")
                print(f"{sp}{'Fraction':{w}s} {TA(f.fromdecimal(D(s[1:])))}")
        def Test_Int():
            f = Init()
            x = 32768
            Assert(f.fmtint(x) == "32768")
            Assert(f.fmtint(x, fmt=None) == f"{x}")
            Assert(f.fmtint(x, fmt="hex") == hex(x))
            Assert(f.fmtint(x, fmt="oct") == oct(x))
            Assert(f.fmtint(x, fmt="dec") == "0d32768")
            Assert(f.fmtint(x, fmt="bin") == bin(x))
            raises(TypeError, f.fmtint, "kdjfkdj")
            raises(ValueError, f.fmtint, x, fmt="kdjfkdj")
            # Setting default works
            f.int = "hex"
            Assert(f.fmtint(x) == hex(x))
        def Test_Strict():
            'Also slightly checks significand'
            f = Init()
            prec = 15
            n = 100
            mpmath.mp.dps = prec
            x = +mpmath.pi
            fmt.strict = False
            s1 = fmt.significand(x, n=n)
            Assert(len(s1) == n + 1)
            fmt.strict = True
            s1 = fmt.significand(x, n=n)
            Assert(len(s1) == prec + 1)
        def Test_Brief():
            # Integers
            Init()
            fmt.brief = True
            x = 12345678901234567891234567890123456789123456789
            result = fmt.fmtint(x, width=10, offset=0, mag=0)
            Assert(result == "1234···789")
            result = fmt.fmtint(x, width=5, offset=0, mag=0)
            Assert(result == "1···9")
            x = -x
            result = fmt.fmtint(x, width=10)
            Assert(result == "-123···89")
            raises(ValueError, fmt.fmtint, x, width=5)
            result = fmt.fmtint(x, width=6, offset=0, mag=0)
            Assert(result == "-1···9")
            if 1:   # Test offset
                result = fmt.fmtint(x, width=10, offset=4)
                Assert(result == "-1···9")
                raises(ValueError, fmt.fmtint, x, width=9, offset=4)
            if 1:   # Test mag
                result = fmt.fmtint(x, width=15, mag=True)
                Assert(result == "-12···9 |10⁴⁶|")
            # Floats
            print("Test_Brief:  need to write float code")  #xx
    if 1:   # Module's base code
        def Error(msg, status=1):
            print(msg, file=sys.stderr)
            exit(status)
        def ParseCommandLine(d):
            d["--test"] = False         # Run self tests
            try:
                opts, args = getopt.getopt(sys.argv[1:], "h", 
                    "test".split())
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o in ("-h", "--help"):
                    Usage(d, status=0)
                elif o == "--test":
                    d["--test"] = True
            return args
    args = ParseCommandLine(d)
    if d["--test"]:
        exit(run(globals(), regexp=r"Test_", halt=1, verbose=0)[0])
    else:
        Demo()
