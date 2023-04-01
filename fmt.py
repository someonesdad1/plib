'''
Format floating point numbers
    Run the module as a script to see example output.
 
    This module provides string interpolation ("formatting") for floating
    point number types.  If x is float(math.pi), str(x) or repr(x) return
    '3.141592653589793', which contains too many digits for casual
    interpretation.  This module's convenience instance fmt will format pi
    as fmt(math.pi) = '3.14', which allows easier interpretation.
 
    The Fmt class will format any number/string accepted by Decimal's
    constructor into a string with the desired number of digits.
 
    The read-write attributes of a Fmt instance provide more control over
    the formatting:
 
    n       Sets the number of digits to use.
 
    dp      Sets the radix (decimal point) to either "." or ",".
 
    low     Numbers below this value are displayed with scientific
            notation.  Set to None to always have small numbers displayed
            in fixed point.
 
    high    Numbers above this value are displayed with scientific
            notation.  Set to None to always have large numbers displayed
            in fixed point.
 
    u       If True, display scientific and engineering notations with
            Unicode exponents.
 
    rlz     If True, remove leading zero digit in fixed point strings.
            Example:  -0.284 is "-0.284" if False, "-.284" if True.
 
    rtz     If True, remove trailing zero digits.
 
    rtdp    If True, remove the trailing radix if it ends the string.
 
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2008, 2012, 2021 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Format Decimal numbers with the Fmt class.  Provides
        # fixed point, scientific, and engineering formats.  You can control
        # the points at which fixed point switches to scientific notation
        # (or set them to None, which means you always get fixed point
        # notation).  Scientific and engineering notation can use Unicode
        # characters for exponents, such as 3.14✕10⁶ and 314✕10⁻⁹.  Since
        # the implementation is in Decimal numbers, you can work with
        # arbitrarily large numbers and arbitrary number of decimal places.
        #∞what∞#
        #∞test∞# --test #∞test∞#
    # Standard imports
        import decimal
        import collections 
        import locale 
        import math 
        from fraction import Fraction
        from pdb import set_trace as xx 
    # Custom imports
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    # Global variables
        D = Decimal = decimal.Decimal
        ii = isinstance
        __all__ = "D Fmt fmt".split()

class Fmt:
    # Key to _SI_prefixes dict is exponent//3
    _SI_prefixes = dict(zip(range(-8, 9), list("yzafpnμm.kMGTPEZY")))
    _superscripts = dict(zip("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"))
    def __init__(self, n=3, low=D("1e-5"), high=D("1e16")):
        '''n is the number of digits to format to.  
        low is the point below which scientific notation is used.
        high is the point above which scientific notation is used.
        low and high can be None, which disables them; if disabled, then
        fixed point interpolation is used by default.
        '''
        Fmt._SI_prefixes[0] = ""    # Need empty string
        self._dp = locale.localeconv()["decimal_point"]  # Radix
        self._n = n                     # Number of digits
        self._u = False                 # Use Unicode symbols for exponents
        self._low = self.toD(low)       # Use sci if x < this value
        self._high = self.toD(high)     # Use sci if x > this value
        self._rtz = False               # Remove trailing zeros if True
        self._rtdp = False              # Remove trailing radix if True
        self._rlz = False               # Remove leading zero if True
        # Attributes for complex numbers
        self._imag_unit = "i"           # Imaginary unit
        self._polar = False             # Use polar coord for complex
        self._deg = True                # Use degrees for angles
        self._cuddled = False           # Use 'a+bi' if True
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
    def _trim(self, dq):
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
        x = self.toD(value)
        parts, dq, z = self._get_data(x, n)
        ne = parts.e + 1
        if parts.e >= 0:
            xx()
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
        dq = self._trim(dq)
        return ''.join(dq)
    def sci(self, value, n=None) -> str:
        'Return a scientific format representation'
        x = self.toD(value)
        parts, dq, z = self._get_data(x, n)
        dq.insert(1, self.dp)
        dq.appendleft(parts.sign)
        if dq[-1] == self.dp:
            del dq[-1]
        dq = self._trim(dq)
        if self.u:
            # Use Unicode characters for power of 10
            o = ["✕10"]
            for c in str(parts.e):
                o.append(Fmt._superscripts[c])
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
        dq = self._trim(dq)
        exponent = ["e", f"{eng_step*div}"]
        try:
            prefix = Fmt._SI_prefixes[div]
        except KeyError:
            prefix = None
        if fmt == "eng":
            if self.u:      # Use Unicode characters for power of 10
                o = ["✕10"]
                for c in str(eng_step*div):
                    o.append(Fmt._superscripts[c])
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
            if have_mpmath:
                mag = (r*r + i*i)**(0.5)
                angle = mpmath.atan2(i, r)
                if self._deg:
                    angle *= 180/mpmath.pi
                a = self(mag, fmt=fmt, n=n)
                b = self(angle, fmt=fmt, n=n)
                if self._deg:
                    b += "°"
                return f"{a}{s}∠{s}{b}"
            else:
                mag = (r*r + i*i)**(0.5)
                angle = math.atan2(i, r)
                if self._deg:
                    angle *= 180/math.pi
                a = self(mag, fmt=fmt, n=n)
                b = self(angle, fmt=fmt, n=n)
                if self._deg:
                    b += "°"
                return f"{a}{s}∠{s}{b}"
        else:
            sr = self(value.real)
            si = self(value.imag)
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
                    o.append(Fmt._superscripts[c])
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
            "(bool) Show complex number's angles in degrees"
            return self._cuddled
        @cuddled.setter
        def cuddled(self, value):
            self._cuddled = bool(value)
fmt = Fmt()     # Convenience instance

if 0:
    # Checking a value
    print(fmt.fix(3.14e1))
    exit()
    
if 0:
    # Develop handling of complex numbers
    fmt.u = 0
    fmt.rtz = 1
    fmt.rtdp = 1
    fmt.imag_unit="j"
    fmt.cuddled = 0
    fmt.polar = 1
    x = mpmath.mpc(1, 2)
    z = complex(1, 2)
    print(fmt(z, n=2))
    exit()

if __name__ == "__main__": 
    if 1:   # Header
        # Standard imports
            from collections import deque
            from decimal import localcontext
            from math import pi
            from pdb import set_trace as xx
            import getopt
            import os
            import pathlib
            import sys
        # Custom imports
            from fpformat import FPFormat
            from lwtest import run, raises, Assert
            from wrap import dedent
            import decimalmath
            from color import Color, TRM as t
        # Global variables
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
    def Demo():
        f = fmt
        t.print(dedent(f'''
        {t.t}Demonstration of Fmt class features:  f = Fmt()
            Formatting (string interpolation) is gotten by calling the Fmt instance
            as a function:  {t.f}f(number){t.n}.  number can be anything that can be converted
            to a python Decimal instance, such as integer, float, Fraction, string,
            mpmath mpf type, etc.  Support for complex numbers is included.
 
        '''))
        s = "pi*1e5"
        x = eval(s)
        # Standard formatting
        print(dedent(f'''
        {t.t}Usual float formatting:{t.n}  x = {s}
            repr(x) = {t.u}{x!r}{t.n}, str(x) = {t.u}{x!s}{t.n}
            Though accurate, we're overwhelmed with too many digits.  The Fmt class
            defaults to showing {f.n} significant figures:  {t.f}f(x){t.n} = {t.fix}{f(x)}{t.n}  The trailing
            radix helps you identify that it's a floating point number.
 
        '''))
        t.print(f"{t.t}Fmt fixed point formatting:")
        print(f"  {t.f}f(x){t.n} = {t.fix}{f(x)}{t.n} (defaults to {f.n} significant figures)")
        # 2 figures
        t.print(f"{t.t}Set to 2 significant figures:  {t.f}f.n = 2")
        f.n = 2
        t.print(f"  f(x) = {t.fix}{f(x)}")
        t.print(f"{t.t}Override f.n significant figures:")
        t.print(f"  {t.f}f(x, n=5){t.n} = {t.fix}{f(x, n=5)}")
        f.n = 3
        # Change scientific notation thresholds
        t.print(f"{t.t}Change transition thresholds to scientific notation")
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
        t.print(f"{t.t}Set f.u to True to use Unicode characters in sci and eng exponents:")
        t.print(f"  {t.f}f.sci(pi*1e6)){t.n} = {t.sci}{f.sci(pi*1e6)}")
        t.print(f"  {t.f}f.eng(pi*1e-7){t.n} = {t.eng}{f.eng(pi*1e-7)}")
        f.u = False
        # Set low & high to None to always get fixed point
        f.low = f.high = None
        t.print(f"{t.t}Setting f.low and f.high to None always results in fixed point:")
        t.print(f"  {t.f}f(pi*1e-27){t.n} = {t.fix}{f(pi*1e-27)}")
        t.print(f"  {t.f}f(pi*1e57){t.n} = {t.fix}{f(pi*1e57)}")
        f.high = 1e6
        f.low = 1e-6
        # Big exponents
        print(dedent(f'''
        {t.t}Fixed point, scientific, and engineering formatting should work for numbers of
        arbitrary magnitudes as long as a Decimal exception isn't encountered.  The
        default Decimal context allows exponents up to an absolute value of (1e6 - 1).
        '''))
        t.print(f"  {t.f}f(D('1e999999')){t.n} = {t.sci}{f(D('1e999999'))}")
        t.print(f"  {t.f}f(D('1e-999999')){t.n} = {t.sci}{f(D('1e-999999'))}")
        try:
            f(D("1e1000000"))
        except decimal.Overflow:
            t.print(f'  {t.f}f(D("1e1000000")){t.n}', "results in overflow")
        t.print(f'  {t.f}f(D("1e-100000000")){t.n}', "underflow that gives 0")
        # Decimals with lots of digits
        t.print(dedent(f'''
        {t.t}Arguments of the formatting functions can be Decimal numbers or any number
        type that can be converted to Decimal.  This means you can format with an
        arbitrary number of significant digits up to the capacity of the Decimal
        context.
        '''))
        with decimal.localcontext() as ctx:
            ctx.prec = 30
            x = 100000*decimalmath.sin(decimalmath.pi()/4)
            t.print(f"  x = 100000*sin(pi/4) to 30 digits = {t.fix}{x}")
            n = 4
            t.print(f"  sci    to {n} digits = {t.sci}{f(x, 'sci', n=n)}")
            n = 5
            t.print(f"  eng    to {n} digits = {t.eng}{f(x, 'eng', n=n)}")
            n = 6
            t.print(f"  engsi  to {n} digits = {t.si}{f(x, 'engsi', n=n)}")
            n = 7
            t.print(f"  engsic to {n} digits = {t.si}{f(x, 'engsic', n=n)}")
        t.print(dedent(f'''
        {t.t}Engineering SI notation means to append an SI prefix to indicate the number's
        magnitude.  This lets you append a physical unit string to get proper SI
        syntax:  {t.u}{f(x, 'engsi')}Ω{t.n}.
        ''', n=8))
        # Complex numbers
        s = "complex(3.45, -6.78)"
        t.print(dedent(f'''
        Complex numbers are also handled by formatting each component separately.  
            'z = {s}' formats to {fmt(eval(s))}
        You can use Fmt attributes of {t.f}imag_unit{t.n}, {t.f}polar{t.n}, {t.f}deg{t.n}, and {t.f}cuddled{t.n} to control the
        number's appearance and change to polar coordinates.
        ''', n=8))
    # Test code 
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
            x = 31.41
            f.dp = ","
            Assert(f(x) == "31,4")
            with raises(TypeError) as y:
                f.dp = "q"
        def TestHuge(n, digits=3):
            f = Init()
            f.n = digits
            x = D(str(pi) + f"e{n}")
            f.high = None
            s = f(x, fmt="fix")
            Assert(s[:3] == "314")
            Assert(s[-1] == ".")
            Assert(s[3:-1] == "0"*(len(s) - 4))
        def TestTiny(n, digits=3):
            f = Init()
            f.n = digits
            x = D(str(pi) + f"e-{n}")
            f.low = None
            s = f(x, fmt="fix")
            Assert(s[:2] == "0.")
            Assert(s[-3:] == "314")
            Assert(s[2:-3] == "0"*(len(s) - 5))
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
            # Here's a second test with somewhat more random digits.
            s = "305834907503304830840485408347390568489537430834"
            n = int(1e6/len(s))  # How many before we reach a million digits
            x = D(s*n)
            f = Init()
            f.high = None
            t = f(x, fmt="fix")
            Assert(len(t) == n*len(s) + 1)
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
        TestBigInteger(100)
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
            '''Compare to fpformat's results.  Only go up to 15 digits because
            fpformat uses floats
            '''
            s, numdigits = "1.2345678901234567890", 15
            fp = FPFormat()
            fp.expdigits = 1
            fp.expsign = False
            f = Init()
            for e in range(10):
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
    def Test_ReallyBig():
        '''The Fmt object uses Decimal numbers to do the formatting.  This
        works for most stuff, but will fail when dealing with exponents
        beyond around a million, the default for Decimal.  This should only
        happend for mpmath.mpf numbers.  In this case, simple sci
        formatting is done.
        '''
        if not have_mpmath:
            return
        mpmath.mp.dps = 50
        x = mpmath.mpf(mpmath.pi)**(10**100)
        s = ("3.76e4971498726941338543512682882908988736516783243804425858"
             "528617907843433628490660912792300428115847331")
        Assert(fmt(x, 3) == s)
    # Module's base code
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
        exit(run(globals(), regexp=r"Test_", halt=1)[0])
    else:
        Demo()
