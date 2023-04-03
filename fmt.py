'''
Todo
    - Test_Big produces a number with an exponent of 1e49.  In pure fixed
      mode, this would take forever to print out.  Thus, if low or high are
      None, there should still be limits to what will be printed.  A
      guide would be half the number of characters that will fit on the
      screen at once.
 
class Fmt:  Format floating point numbers
    Run the module as a script to see example output.  See Terminal Notes
    below.
 
    This module provides string interpolation ("formatting") for floating
    point and complex number types.  str(float(math.pi)) returns
    '3.141592653589793', which contains too many digits for
    casual interpretation.  This module's convenience instance fmt will
    format pi as fmt(math.pi) = '3.14', which allows easier interpretation.
 
    Fmt is also a context manager so you can change formatting
    characteristics in a with block.
 
    The attributes of a Fmt instance provide more control over the
    formatting:
 
        n       Sets the number of significant digits.
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
        terminals will likely need hacking on color.py to get things to
        work correctly.  Define the environment variable DPRC to get ANSI
        color strings output to the terminal.
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
        import collections 
        import locale 
        import math 
        import os 
        import threading 
        from pprint import pprint as pp
        from pdb import set_trace as xx 
    if 1:   # Custom imports
        from color import t
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
if 1:   # Classes
    class TakeApart:
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
            self._number = x
            self.disassemble()
            return str(self)
        def disassemble(self):
            "Disassemble the number self._number into this instance's attributes"
            n, x = self._n, self._number
            assert(x is not None)
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
                lg, ten = mpmath.log10(yabs), mpmath.mpf(10)
                e = int(mpmath.floor(lg)) if yabs else 0
                s = mpmath.nstr(mpmath.mpf(yabs/ten**e), n)
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
            self._dq = collections.deque(ld + other)
            # Check invariants
            assert(self._sign in ("-", " "))
            assert(ii(self._ld, str) and len(self._ld) == 1)
            assert(self._dp in (".", ","))
            assert(ii(self._other, str))
            assert(ii(self._e, int))
            assert(ii(self._dq, collections.deque) and 
                   (len(self._dq) == len(self._ld) + len(self._other)))
        if 1:   # Properties
            @property
            def dp(self):
                'Decimal point string'
                assert(ii(self._dp, str) and len(self._dp) == 1)
                return self._dp
            @property
            def dq(self):
                "Deque of significand's digits"
                assert(ii(self._dq, collections.deque) and len(self._dq))
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
                assert(ii(self._ld, str) and len(self._ld == 1))
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
                assert(ii(value, int))
                assert(value > 0)
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
            def supported(self):
                'Set of supported types'
                return self._supported
            @supported.setter
            def supported(self, myset):
                assert(ii(myset, set) and myset)
                self._supported = myset
    new_method = True
    class Fmt:
        def __init__(self, n=3, low=D("1e-5"), high=D("1e16")):
            '''n is the number of digits to format to.  
            low is the point below which scientific notation is used.
            high is the point above which scientific notation is used.
            low and high can be None, which disables them; if disabled, then
            fixed point interpolation is used by default.
            '''
            self._n = n                     # Number of digits
            if new_method:
                self.ta = TakeApart()       # Take apart machinery
                self.ta.n = n               # Synchronize number of digits
            self._dp = locale.localeconv()["decimal_point"]  # Radix
            self._low = self.toD(low)       # Use sci if x < this value
            self._high = self.toD(high)     # Use sci if x > this value
            self._u = False                 # Use Unicode symbols for exponents
            self._rlz = False               # Remove leading zero if True
            self._rtz = False               # Remove trailing zeros if True
            self._rtdp = False              # Remove trailing radix if True
            self._spc = False               # If num >= 0, use " " for leading character
            # Attributes for complex numbers
            self._imag_unit = "i"           # Imaginary unit
            self._polar = False             # Use polar coord for complex
            self._deg = True                # Use degrees for angles
            self._cuddled = False           # Use 'a+bi' if True
            self._ul = False                # Underline argument in polar form
            self._comp = False              # (re,im) form 
            # Key to _SI_prefixes dict is exponent//3
            self._SI_prefixes = dict(zip(range(-8, 9), list("yzafpnμm.kMGTPEZY")))
            self._SI_prefixes[0] = ""       # Need empty string
            self._superscripts = dict(zip("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"))
            # For context manager behavior, we'll use a lock to avoid another
            # thread messing with our attributes
            self.lock = threading.Lock()
        def __enter__(self):
            # Store our attributes (note only those that start with '_' are
            # saved)
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
        def _take_apart(self, x, n=None) -> collections.namedtuple:
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
            Apart = collections.namedtuple("Apart", "sign ld dp other e")
            if not ii(x, D):
                raise TypeError("x must be a Decimal number")
            # Get scientific notation form
            N = int(n) if n is not None else self._n
            if N < 1:
                raise ValueError("n must be > 0")
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
            return (parts, collections.deque(parts.ld) + 
                collections.deque(parts.other), "0")
        def trim(self, dq):
            'Implement rtz, rtdp, and rlz for significand dq in deque'
            assert(ii(dq, collections.deque))
            if self._rtz and self._dp in dq:
                while dq and dq[-1] == "0":
                    dq.pop()        # Remove trailing 0's
            if self._rtdp and dq and dq[-1] == self._dp:
                dq.pop()            # Remove trailing decimal point
            if self._rlz and len(dq) > 2:
                if dq[0] == "0" and dq[1] == self._dp: 
                    dq.popleft()    # Remove leading 0
            return dq
        def fix(self, value, n=None) -> str:
            'Return a fixed point representation'
            # We first need to check that this number isn't too large to
            # use fixed point formatting.  Example:  pi**100000 has an
            # exponent of 49714 and its fixed point expression will involve
            # tens of thousands of digits.  I've arbitrarily chosen that a
            # number that will take up more than about 1/4 of the screen's
            # space is too big for fixed formatting, so go over to
            # scientific in this case.
            #
            # First get the exponent e
            self.ta(value)
            e = abs(self.ta.e)
            nmax = W*L//4    # 1/4 of the number of characters that fit on screen
            if e > nmax:
                return self.sci(value, n=n)
            if 1:   # Use old method
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
                    self.ta(value)
                    self.ta.n = n if n is not None else self.n
                    sign = self.ta.sign     # Sign ("-" or " ")
                    # Note we use fmt instance's decimal point
                    dp = self.dp            # Decimal point
                    dq = self.ta.dq         # Deque of significand's digits (no dp)
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
                    if sign == "-" or (sign == " " and self.spc):
                        dq.appendleft(sign)
                    dq = self.trim(dq)
                    retval_new = ''.join(dq)
                assert(set(retval_new).issubset(set("0123456789.,- ")))
            # Ensure new and old method get same results (prepend space to
            # old results if >= 0 and self.spc)
            if retval_old[0] != "-" and self.spc:
                retval_old = f" {retval_old}"
            assert retval_new == retval_old, f"{retval_new!r} != {retval_old!r}"
            return retval_new
        def sci(self, value, n=None) -> str:
            'Return a scientific format representation'
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
        def eng(self, value, fmt="eng", n=None) -> str:
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
        def Complex(self, value, fmt="fix", n=None) -> str:
            '''value is a complex number.  Return a string in the form of 
            'a + bi'.
            '''
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
        def __call__(self, value, fmt="fix", n=None) -> str:
            '''Format value with the default "fix" formatter.  n overrides
            self.n digits.  fmt can be "fix", "sci", "eng", "engsi", or "engsic".
            '''
            if ii(value, complex):
                return self.Complex(value, fmt=fmt, n=n)
            elif have_mpmath and ii(value, mpmath.mpc):
                return self.Complex(value, fmt=fmt, n=n)
            x = 0
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
            if fmt not in "fix sci eng engsi engsic".split():
                raise ValueError(f"'{fmt}' is unrecognized format string")
            if fmt == "fix":
                if x and self.high is not None and abs(x) > self.high:
                    return self.sci(x, n)
                elif x and self.low is not None and abs(x) < self.low:
                    return self.sci(x, n)
                return self.fix(x, n)
            elif fmt == "sci":
                return self.sci(x, n)
            else:
                return self.eng(x, n=n, fmt=fmt)
        if 1:   # Properties
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
            def low(self):
                'Use "sci" format if abs(x) is < low and not None'
                return self._low
            @low.setter
            def low(self, value):
                self._low = None if value is None else abs(D(str(value)))
            @property
            def n(self) -> int:
                'Number of digits (integer > 0)'
                return self._n
            @n.setter
            def n(self, value):
                n = abs(int(value))
                self._n = max(n, 1)
                self.ta.n = self._n
            @property
            def spc(self) -> bool:
                'Add " " to numbers >= 0 where "-" goes'
                return self._spc
            @spc.setter
            def spc(self, value):
                self._spc = bool(value)
            @property
            def u(self) -> bool:
                '(bool) Use Unicode in "sci" and "eng" formats if True'
                return self._u
            @u.setter
            def u(self, value):
                self._u = bool(value)
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
if 0 and __name__ == "__main__": 
    x = mpmath.mpf("1e8")
    print(fmt.fix(x))
    exit()

if __name__ == "__main__": 
    if 1:
        import debug
        debug.SetDebugger()
    if 1:   # Header
        # Standard imports
            from collections import deque
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
        t.print(f"The f.ul underlining won't work unless your terminal supports it.")
        if not use_colors:
            print(f"Set the environment variable DPRC to true to see colorized output.")
    if 1:   # Test code 
        def Init():
            'Make sure test environment is set up in a repeatable fashion'
            f = Fmt(3)
            f.rlz = f.rtz = f.rtdp = False
            return f
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
            raises(ValueError, f, x, n=0)
            raises(ValueError, f, x, n=-1)
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "1.0")
            Assert(f(x, n=3) == "1.00")
            Assert(f(x, n=4) == "1.000")
            Assert(f(x, n=5) == "1.0000")
            Assert(f(x, n=6) == "0.999999")
            Assert(f(x, n=7) == "0.9999990")
            raises(ValueError, f, -x, n=0)
            raises(ValueError, f, -x, n=-1)
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
            Assert(fmt(x, 3) == s)
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
