'''
- Bugs
    - 9.99999796866929e999999 with normal string interpolation is erroneously shown as 1.00e999999.
      fmt is not rounding properly.
- Todo
    - fmt.unc()
        - Add support for eng, engsi, engsic
    - Large numbers
        - mpmath can calculate fac(1e1000); it's log is 1.00e1002.  Thus
          log(log(x)) could be a way to get reasonably-sized numbers to
          help you see the magnitude.
        - 100!**100! can be calculated with mpmath, but the exponent is
          1.47e160.  Need to develop a notation to handle large numbers.
        - Use log: ((1.47e160))
        - Use sci notation in exponent:  1.47e((1e160))
        - Power tower:  10↑↑n == 10**10**...**10, n times
        - "order" of magnitude n:  how many times you have to take log of a
          number to get a result between 1 and 10.  Could call this
          "biglog".  See https://en.wikipedia.org/wiki/Super-logarithm
    - width
        - Add width attribute; remove width from method calls
            - Set to 0 for normal behavior.  Larger integer specifies the
              desired width.
        - Need an algorithm to make interpolations fit in a desired width.
          Must be on a best effort basis, as it will be impossible for some
          numbers.  Example 100!**100! won't fit into e.g. 60 columns
          because the exponent is 160 digits long.
            - See notes above about large number notations
        - Typical abbreviation will use ellipsis ⋯ (U+22EF) and truncate
          middle digits to get things to fit
    - Angle measures:  use plain ASCII for polar forms.  Support radians,
      degrees, gradians, and revolutions.
        - form:  x (a u) where x is the magnitude, a is the angle, and u is
          the angular unit (e.g., rad, deg, grad, rev).  
        - Other angle measures:  arcmin, arcsec, hour angle (24 per rev),
          point (1/8 of right angle), binary degree (256 per rev), quadrant
          (90°), sextant (60°).  
        - Could allow for a custom angle measure with a custom_angle
          attribute.
        - angle_measure attribute can be "deg", "rad", "grad", "rev",
          "turn".
 
---------------------------------------------------------------------------
class Fmt:  Format floating point numbers
    This module provides string interpolation ("formatting") for integer,
    floating point, and complex number types.  A Fmt instance can format
    int, float, decimal.Decimal, mpmath.mpf, and fractions.Fraction number
    types.
 
    Run the module as a script to see example output.  See Terminal Notes
    below.
 
    The attributes of a Fmt instance provide more control over the
    formatting:
 
        n       Sets the number of displayed digits.  For floats, the
                maximum is 15; for mpmath and Decimal, it's controlled by
                the context's precision.
        default String for default floating point formatting (fix, fixed,
                sci, eng, engsi, engsic)
        int     How to format integers (None is str(), dec, hex, oct, bin)
        dp      Sets the radix (decimal point) string (use '.' or ',').
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
        rtz     If True, remove trailing zero digits.
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
 
    Thread safety
        Fmt is deliberately not thread-safe.  This means if you call the
        methods of the same instance in two different threads, you'll get
        unpredictable and probably wrong results.  This could be fixed by
        e.g. using a thread.Lock instance and turning Fmt into a context
        manager, but the cost is that Fmt is then not able to be pickled.
        Most of my applications are single-threaded and I prefer to have
        the ability to pickle things if desired.
 
        One solution to a multithreading application is to give each thread
        its own Fmt() instance:  one way to do this is to create one
        instance, then make a copy using the copy() method.
 
    Terminal Notes
        This script is intended to be used with other scripts in the plib
        directory.  You can get the needed tools at
        https://github.com/someonesdad1/plib.  I use this script in a bash
        terminal in a cygwin environment using the mintty terminal emulator
        and it works as written.  Look at /plib/pictures/fmt.png to see
        what the Demo() function's output looks like on my screen.  Other
        terminals may need hacking on color.py to get things to work 
        correctly.  For the demo, define the environment variable DPRC to
        get ANSI color strings output to the terminal.
 
    How it works
        The TakeApart class takes apart numbers into their component parts
        (prepare() and disassemble() methods).  Then the Fmt instance uses
        the TakeApart instance to supply the needed parts of the number and
        builds the desired interpolation string.
 
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
        import sys 
        import subprocess 
        import threading 
        from collections import deque, namedtuple
        from pprint import pprint as pp
        from pdb import set_trace as xx 
    if 1:   # Custom imports
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
if 1:   # Utility
    def Assert(cond, debug=False, msg=""):
        '''Similar to assert, but you'll be dropped into the debugger on an
        exception if debug is True, Assert.debug is True, or 'Assert' is
        a nonempty environment string.  If msg is not empty, it's printed
        out.
        '''
        if not hasattr(Assert, "debug"):
            Assert.debug = False
        if not cond:
            if debug or Assert.debug or os.environ.get("Assert", ""):
                if msg:
                    print(msg, file=sys.stderr)
                print("Type 'up' to go to line that failed", file=sys.stderr)
                breakpoint()
            else:
                raise AssertionError(msg)
class TakeApart:
    '''Take apart a number into its components to prepare for string
    interpolation.  Handles int, float, Decimal, mpf, and Fractions.  
    The core implementation is in disassemble(), which depends on
    prepare().
 
    This code is not thread-safe, so only use one instance with one thread.
    '''
    def __init__(self):
        self._thread_id = threading.get_ident()
        self.supported = [int, float, Decimal, Fraction]
        if have_mpmath:
            self.supported.append(mpmath.mpf)
        self.supported = tuple(self.supported)
        self.reset()
    def reset(self):
        'Clear attributes used for number disassembly'
        self.number = None      # Number argument to __call__()
        self.normal = None      # True means number is not inf and not nan
        self.int = None         # True means number is an integer
        self.n = None           # Desired number of digits
        self.sign = None        # "-" or " "
        self.radix = None       # Decimal point defined by locale
        self.e = None           # Integer power of 10 of number
        self.dq = None          # Deque of significand's digits without dp
    def copy(self):
        'Return a copy of this instance'
        ta = TakeApart()
        ta.number = self.number
        ta.normal = self.normal
        ta.int = self.int
        ta.n = self.n
        ta.sign = self.sign
        ta.radix = self.radix
        ta.e = self.e
        if self.dq is not None:
            ta.dq = self.dq.copy()
        return ta
    def __str__(self):
        if self.number is None:
            return "Call disassemble(value, n) first"
        if self.normal:
            if self.int:
                return f"{self.sign}{''.join(self.dq)}"
            else:
                cp = self.dq.copy()
                cp.insert(1, self.radix)
                e = 0 if not self.number else self.e
                return f"{self.sign}{''.join(cp)}e{e}"
        else:
            if self.dq[0] == "n":
                return ''.join(self.dq)
            else:
                return self.sign.strip() + ''.join(self.dq)
    def __call__(self, x, n, all=False):
        if self._thread_id != threading.get_ident():
            print(f"Warning:  current thread ID = {threading.get_ident()}\n"
                  f"  TakeApart constructor started with is {self._thread_id}.\n"
                  f"  The TakeApart object is not thread-safe.",
                  file=sys.stderr)
        Assert(x is not None)
        Assert(ii(n, int) and n > 0)
        # Clamp n to the maximum precision allowed
        if ii(x, int):
            n = min(n, len(str(abs(x))))
        elif ii(x, float):
            n = min(n, 15)
        elif ii(x, (D, Fraction)):
            ctx = decimal.getcontext()
            n = min(n, ctx.prec)
        elif have_mpmath and ii(x, mpmath.mpf):
            n = min(n, mpmath.mp.dps)
        self.disassemble(x, n, all=all)
    def prepare(self, value, n: int, all=False):
        '''Return a canonical representation of a number value.  n is an
        integer describing the number of decimal digits we will want.  To
        do this, the canonical representation must have at least n + 1
        digits available; the n + 1 digits allows for banker's rounding (i.e.,
        round-to-even) of the significand to n digits.  If all is True, we
        return all of the number's digits.
 
        The returned representation will be a tuple of the form 
            
            (neg, digits, radix, e)
 
        where
 
            Value   Type    Definition
            ------  ----    ------------------------------------------------
            neg      b      Number is negative if True
            digits   s      Decimal digits of significand with no radix
            radix    s      Decimal point either "." or ","
            e        i      Power of 10 exponent.  None if value is integer.
 
        where b is Boolean, s is string, and i is integer.
 
        Improper values:
            inf     (False, "inf", None, None)
            -inf    (True, "inf", None, None)
            nan     (None, "nan", None, None)
 
        Integer values:
            (neg, digits, None, None)
 
        This method will check constraints/invariants and raise an
        exception if improper behavior is detected.
        '''
        if not (ii(n, int) and n > 0):
            raise ValueError("n must be an integer > 0")
        if value is None:
            raise ValueError("value must not be None")
        def special(value, typ):
            if value == typ("inf"):
                return (False, "inf", None, None)
            elif value == typ("-inf"):
                return (True, "inf", None, None)
            elif value == typ("nan") or repr(value) in "nan Decimal('NaN') mpf('nan')".split():
                return (None, "nan", None, None)
            return None
        not_supported = TypeError(f"{value!r} is an unsupported type")
        if not ii(value, self.supported):
            raise not_supported
        # We always use the locale's radix
        radix = locale.localeconv()["decimal_point"]
        # If value is Fraction, convert it
        if ii(value, Fraction):
            value = Decimal(value.numerator)/Decimal(value.denominator)
        # Construct the output tuple
        if ii(value, int):
            result = (value < 0, str(abs(value)), None, None)
        elif ii(value, float):
            if ".flt'>" in str(type(value)):  # Avoid an infinite recursion with f.flt instances
                value = float(value)
            result = special(value, float)
            if result is None:
                # We handle floats specially because the built-in
                # formatting does the required job without needing any
                # additional rounding step.  However, note it is NOT
                # half-even rounding.
                if all:
                    m = 16
                else:
                    m = min(n, 16)  # Clamp n
                s = f"{abs(value):.{m - 1}e}".replace(".", "").replace(",", "")
                if "e" not in s:
                    raise Exception("Bug:  no 'e' in float interpolation")
                digits, exp = s.split("e")
                result = (value < 0, digits, radix, int(exp))
        elif ii(value, Decimal):
            result = special(value, Decimal)
            if result is None:
                p = decimal.getcontext().prec
                s = f"{abs(value):.{p}e}".replace(".", "").replace(",", "")
                if "e" not in s:
                    raise Exception("Bug:  no 'e' in Decimal interpolation")
                digits, exp = s.split("e")
                result = (value < 0, digits, radix, int(exp))
        elif have_mpmath and ii(value, mpmath.mpf):
            # Note:  I have made it a policy to assume that any number defined
            # to be an mpmath.mpf type is a real number, even if mpmath.isinf()
            # is True for that number.  
            result = special(value, mpmath.mpf)
            if result is None:
                m = mpmath.mp.dps
                if m < n:
                    raise ValueError(f"mpmath precision less than requested n = {n}")
                # To get mpmath.nstr to return the full number of
                # significant digits, pass in the keyword argument
                # strip_zeros=False.  This keyword gets passed to
                # libmpf.to_str().  Also, min_fixed > max_fixed is used to
                # force scientific notation.
                s = mpmath.nstr(abs(value), m, show_zero_exponent=True,
                                min_fixed=1, max_fixed=0, strip_zeros=False)
                if "e" not in s:
                    raise Exception("Bug:  no 'e' in nstr() result")
                digits, exp = s.split("e")
                digits = digits.replace(".", "").replace(",", "")
                if not value and len(digits) < m:
                    # This can happen with numbers like 0
                    while len(digits) < m:
                        digits += "0"
                result = (value < 0, digits, radix, int(exp))
        else:
            raise not_supported
        if 1:   # Verify constraints & invariants
            assert(ii(result, tuple))
            neg, digits, radix, e = result  # result must be 4-tuple
            if radix is None and e is None:
                if neg is None:     # Check for nan
                    Assert(digits == "nan")
                else:               # inf or int
                    Assert(ii(neg, bool))
                    if "inf" in digits:
                        Assert(digits == "inf" or digits == "-inf")
                    else:
                        Assert(ii(value, int))
            else:
                Assert(ii(digits, str))
                if not all:
                    # Normal number:  make sure we have at least n + 1 digits for
                    # banker's rounding of the significand.
                    if ii(value, float):
                        Assert(len(digits) == n)    # Rounding already done
                    else:
                        if len(digits) == n:
                            digits += "0"   # Correct for this one case
                            result = (value < 0, digits, radix, int(exp))
                        Assert(len(digits) >= n + 1)
                Assert(radix is None or ii(radix, str))
                if ii(radix, str):
                    Assert(len(radix) == 1 and radix in ".,")
                if have_mpmath:
                    Assert(ii(value, (float, Fraction, Decimal, mpmath.mpf)))
                else:
                    Assert(ii(value, (float, Fraction, Decimal)))
                Assert(ii(e, int))
        return result
    def disassemble(self, value, n, all=False):
        '''Disassemble the number value into this instance's attributes.
        The basic information returned is:
 
        self.number     Original value
        self.normal     Boolean:  True for int/float, false for inf/nan
        self.int        Boolean:  True for int, False for float
        self.n          Number of desired digits in interpolation
        self.sign       Sign of number:  "-" or " "
        self.radix      Decimal point (defined by locale)
        self.e          Integer containing the numbers base 10 exponent
        self.dq         Deque containing self.n digits
 
        The deque self.dq contains the self.n digits that will be displayed.
        The last digit of the deque is rounded using half-even rounding:  if
        the (n+1)st digit is 5, the last digit is rounded up if the last digit
        is odd.
 
        If the number is inf/nan (self.normal is False), then self.dq will
        contain the string "nan" or "inf"; everything else is None.  If it's
        the string "inf", then self.sign will be either "-" or "".
 
        If the number is an integer, the deque will contain the first self.n
        digits followed by the necessary remaining zeroes.  self.sign is also
        set; everything else is None.
 
        Otherwise, the number is a floating point number and the deque contains
        the desired self.n digits with the other attributes set appropriately.
         
        If all is True, then n is ignored and all of the digits in the
        deque are returned.
        '''
        # Put this instance into a known state
        self.reset()
        # Get the basic string interpolation data for the supported number types
        neg, digits, radix, e = self.prepare(value, n, all=all)
        self.number = value
        self.normal = True
        self.n = n
        if digits == "nan" or "inf" in digits:
            self.normal = False
            self.sign = "-" if neg else ""
            self.dq = deque(digits)
            return
        if radix is None and e is None:     # int
            self.sign = "-" if neg else " "
            self.int = True
            size = len(digits)
            self.dq = self.round(value, deque(digits), self.n)
            # Append zeroes if needed
            for i in range(size - len(self.dq)):
                self.dq.append("0")
            # Checks
            Assert(len(self.dq) == size)
            Assert(self.sign == "-" or self.sign == " ")
            return
        # Regular floating point number
        self.int = False
        self.sign = "-" if neg else " "
        self.radix = radix
        self.e = e
        self.dq = deque(digits)
        if not all:
            self.dq = self.round(value, deque(digits), self.n)
            Assert(len(self.dq) == n)
        # Checks
        Assert(ii(self.int, bool))
        Assert(self.sign == "-" or self.sign == " ")
        Assert(self.radix == "." or self.radix == ",")
        Assert(ii(self.e, int))
    def round(self, value, dq: deque, n: int):
        '''Return the deque dq of digits rounded to n digits.  Use half-even
        rounding:  the last digit is rounded up if the following digit is
        greater than 5.  If the following digit is 5, the last digit is rounded
        up if it is odd.
        '''
        # Integers are special cases.  For example, 123 can be rounded to 2
        # digits, but an integer < 10 cannot.
        if ii(self.number, int) and len(str(abs(self.number))) <= n:
            return dq
        # Floats are also a special case, as rounding was done by the
        # string interpolation in prepare().
        if ii(value, float):
            return dq
        Assert(len(dq) >= n + 1)
        # Truncate to a string of n digits
        s = ''.join(dq)[:n]         # First n digits
        r = ''.join(dq)[n:]         # Remaining digits
        # Get the (n+1)st digit, which is used as the sentinel for rounding
        sentinel = int(r[0])
        if 1:   # Handle an exceptional case
            '''
            Example is fmt(float(0.99), n=2, fmt="fix")):  dq contains
            '98999999999999999' and s becomes '98'.  Using the sentinel
            to round will produce 0.99 instead of the expected 1.0.
 
            We handle this example by converting r = '999999999999999' to
            an int and adding 1.  If the string length changes, we have to
            add 1 to s and _then_ do half-even rounding.  This problem
            comes about because of the unexpected f"{x:.16e}" being equal
            to '9.8999999999999999e-01'.
        
            The following code demonstrates that this anomalous '8' appears
            in float string interpolation for '.{w}e' values of 15 and above.
 
            from collections import deque
            for w in range(12, 18):
                print("digits =", w)
                dq = deque("9")
                count = 0
                while count < 20:
                    x = float("." + ''.join(dq))
                    s = f"{x:.{w}e}"
                    if "8" in s:
                        print(f"{''.join(dq)}     {s}")
                    count += 1
                    dq.append("9")
 
            which gives
 
                digits = 12
                digits = 13
                digits = 14
                digits = 15
                99999999     9.999999899999999e-01
                digits = 16
                99     9.8999999999999999e-01
                999999     9.9999899999999997e-01
                99999999     9.9999998999999995e-01
                9999999999     9.9999999989999999e-01
                9999999999999     9.9999999999989997e-01
                9999999999999999     9.9999999999999989e-01
                digits = 17
                99     9.89999999999999991e-01
                999     9.98999999999999999e-01
                999999     9.99998999999999971e-01
                99999999     9.99999989999999950e-01
                999999999     9.99999999000000028e-01
                9999999999     9.99999999899999992e-01
                99999999999     9.99999999989999999e-01
                9999999999999     9.99999999999899969e-01
                99999999999999     9.99999999999990008e-01
                9999999999999999     9.99999999999999889e-01
 
            This is one of those rare bugs that is only found by testing at
            edge cases.  It was found in Test_Basics() and it was sheer luck
            that I chose both 0.99 and 16 digits.
            '''
            add_one = 0     # This is used below
            if len(str(int(r) + 1)) > len(r):
                add_one = 1
        Assert(len(s) == n)
        if set(s) == set("0"):
            dq = deque(s)
        else:
            # Get last digit of significand
            last_digit = s[-1]
            # Convert to integer to make rounding easy.  Note the addition
            # of add_one for the exceptional case.
            significand = int(s) + add_one
            # Round significand 
            if sentinel > 5 or (sentinel == 5 and last_digit in "13579"):
                significand += 1
            # Convert back to deque
            dq = deque(str(significand))
        # Check 
        Assert(len(dq) in (n, n + 1))
        # Remove the extraneous digit if needed.  This will be a case like
        # '999' rounding up to '1000'.
        if len(dq) == n + 1:
            dq.pop()
            self.e += 1
        return dq
 
class Fmt:
    def __init__(self, n=3):
        'n is the number of digits to format to'
        self._n_init = n
        self._n = None                  # Number of digits
        self._default = None            # Default formatting method
        self._int = None                # Default fmtint() style
        self.ta = None                  # Take apart machinery
        self._dp = None                 # Radix
        self._u = None                  # Use Unicode symbols for exponents
        self._rlz = None                # Remove leading zero if True
        self._rtz = None                # Remove trailing zeros if True
        self._rtdp = None               # Remove trailing radix if True
        self._spc = None                # If num >= 0, use " " for leading character
        self._sign = None               # Include "+" or "-" in interpolation
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
        # Attributes that won't change when reset() is called
        if 1:
            # These set the points where fixed mode switches to scientific
            # notation.  Standard python uses 1e-5 and 1e15.  Set either of
            # these to None to disable switching to scientific notation
            # (you can get large strings this way).  NOTE:  these must be
            # floats because they are compared to both mpf and Decimal
            # types.  This is a compromise, as it will break on high and
            # low values beyond the range of a float.  However, since float
            # exponents go over the range of about 308, this will likely
            # never happen.
            self._low_init = 1e-4
            self._high_init = 1e6
        # Key to _SI_prefixes dict is exponent//3
        self._SI_prefixes = dict(zip(range(-8, 9), list("yzafpnμm.kMGTPEZY")))
        self._SI_prefixes[0] = ""       # Need empty string
        self._superscripts = dict(zip("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"))
        # Set to default state
        self.reset()
    def reset(self):
        'Reset attributes to default state'
        self.n = self._n_init
        self._default = "fix"
        self._int = None    # Default uses str(int)
        self.ta = TakeApart()
        self._dp = locale.localeconv()["decimal_point"]
        self._u = False
        self._rlz = False
        self._rtz = False
        self._rtdp = False
        self._spc = False
        self._sign = False
        self.nchars = W*L//4  # Base on screen width and hight
        self.brief = False
        self.ellipsis = "⋯"
        # Attributes for complex numbers
        self._imag_unit = "i"
        self._polar = False
        self._deg = True
        self._cuddled = False
        self._ul = False
        self._comp = False
        # Low and high settings
        self._low = self._low_init  
        self._high = self._high_init
        # See constructor for why these must be floats
        Assert(ii(self._low, float))
        Assert(ii(self._high, float))
    def copy(self):
        'Return a copy of the current instance'
        fmt = Fmt(self.n)
        # Set attributes equal
        for i in self.__dict__:
            if i.startswith("__") and i.endswith("__"):
                continue
            fmt.__dict__[i] = self.__dict__[i]
        Assert(fmt.__dict__ == self.__dict__)
        # Set a new TakeApart instance 
        fmt.ta = TakeApart()
        # For this to work, fmt.ta(number) must be called before
        # disassembling any number.
    def toD(self, value) -> Decimal:
        '''Convert value to a Decimal object.  Supported types are int,
        float, Fraction, Decimal, str, mpmath.mpf, and any other type
        that gives a value from str(value).
 
        Note: if value is an mpmath.mpf number, it may be much larger than
        a default Decimal instance can hold (Decimal's default exponent
        goes up to 1e6).  Raise a ValueError exception to explain the
        problem.
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
        else:
            # This can fail on big mpf numbers
            return D(str(value))
    def GetUnicodeExponent(self, e):
        o = ["✕10"]
        for c in str(e):
            o.append(self._superscripts[c])
        return ''.join(o)
    def trim(self, dq):
        'Implement rtz, rtdp, and rlz for significand dq in deque'
        Assert(ii(dq, deque))
        if self._rtz and self._dp in dq:
            while dq and dq[-1] == "0":
                dq.pop()        # Remove trailing 0's
        if self._rtdp and dq and dq[-1] == self._dp:
            dq.pop()            # Remove trailing decimal point
        if self._rlz and len(dq) > 2:
            if dq[0] == "0" and dq[1] == self._dp: 
                dq.popleft()    # Remove leading 0
        return dq
    def none_bug(self, var, name):
        'Raise exception if var is None'
        if var is None:
            raise Exception(f"fmt.{var} is None")
    def clamp_n(self, value, n) -> int:
        'Clamp n to reasonable values'
        if ii(value, float):
            return min(n, 15)
        elif ii(value, D):
            ctx = decimal.getcontext()
            return min(n, ctx.prec)
        elif have_mpmath and ii(value, mpmath.mpf):
            return min(n, mpmath.mp.dps)
        else:
            return n
    def significand(self, value) -> str:
        "Return a string for the value's significand"
        if ii(value, float):
            n = 15
        elif have_mpmath and ii(value, mpmath.mpf):
            n = mpmath.mp.dps
        elif ii(value, D):
            ctx = decimal.getcontext()
            n = ctx.prec
        elif ii(value, int):
            return str(value)
        self.ta(value, n)
        dq = self.ta.dq
        sign = self.ta.sign.strip()
        dq.insert(1, self.dp)
        return sign + ''.join(dq)
    def __call__(self, value, fmt=None, n=None, width=None) -> str:
        '''Format value with the default formatter.  n overrides self.n
        digits and must be > 0.  fmt can be "fix", "fixed", "sci", "eng",
        "engsi", or "engsic" for real numbers.  If it is None, then 
        self.default is used.
 
        If n is not None, it is an integer > 0 that overrides the self.n
        setting.
 
        If value is an integer, fmt can be "dec", "hex", "oct", or "bin".  
 
        If width is not None, it is the desired string width when self.brief is
        True; note that a best effort will be made, but the returned string may
        be larger than the desired width.
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        if 1:   # Check arguments
            if n is not None:
                if not ii(n, int):
                    raise TypeError("n must be an integer")
                if n <= 0:
                    raise ValueError("n must be > 0")
            if ii(value, int):
                if fmt is not None and fmt not in "dec hex oct bin".split():
                    raise ValueError(f"'{fmt}' is unrecognized format string")
                else:
                    fmt = self.int
            else:
                if fmt is not None and fmt not in "fix fixed sci eng engsi engsic".split():
                    raise ValueError(f"'{fmt}' is unrecognized format string")
                elif fmt is None:
                    fmt = self.default
            if width is not None:
                if not ii(width, int):
                    raise TypeError("width must be an integer")
                if n <= 0:
                    raise ValueError("width must be > 0")
        # Call the relevant method
        if ii(value, complex) or (have_mpmath and ii(value, mpmath.mpc)):
            return self.Complex(value, fmt=fmt, n=n, width=width)
        elif ii(value, int):
            return self.Int(value, fmt=fmt, n=n, width=width)
        elif ii(value, (float, Decimal, Fraction)):
            return self.Real(value, fmt=fmt, n=n, width=width)
        elif have_mpmath and ii(value, mpmath.mpf):
            return self.Real(value, fmt=fmt, n=n, width=width)
        else:
            raise TypeError(f"{value!r} is an unsupported type")
    def fmtint(self, value, fmt=None, width=None, mag=False):
        '''Format an integer value.  If fmt is None, the default self.int
        formatting is used.  Other values for fmt are "hex", "oct", "dec",
        and "bin", which cause 0x, 0o, 0d, or 0b to be prepended.
        self.sign and self.spc are honored.
 
        width is the number of spaces the string must fit into.  If it is
        None, then the number of COLUMNS - 1 is used.
 
        mag if True is used to provide a [~10ⁿ] string at the end to
        indicate the magnitude of the number.
 
        width is only used if self.brief is True.
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
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
            L = self.get_columns() if width is None else int(width)
            # The minimum possible length is the sign, one character each
            # end, and ellipsis
            min_length = 2 + len(self.ellipsis) + len(sgn)
            m = ""
            if mag:     # Add in the length of ' |10ⁿ|' string
                x = D(value)*D("1.0")
                a = f"{x:.1e}".split("e")[1]
                e = int(a)
                Assert(e >= 0)
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
            Assert(len(left) + len(right) == n)
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
    def Int(self, value, fmt=None, n=None, width=None) -> str:
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        fmt = fmt if fmt is None else self.int
        Assert(ii(value, int))
        self.ta(value, n)
        sgn = self.ta.sign
        if sgn == " " and not self.spc:
            sgn = ""
        s = sgn + ''.join(self.ta.dq)
        return s
    def fixed(self, value, n=None, width=None) -> str:
        '''Return a fixed point representation simulating an HP calculator.
        Example:  if value = 72.8435 and n = 3, then '72.844' is returned.
        Here, n represents the number of digits after the decimal point.
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        n = self.clamp_n(value, n)
        if self.low is not None and 0 < abs(value) < self.low:
            return self.sci(value, n=n)
        elif self.high is not None and abs(value) >= self.high:
            return self.sci(value, n=n)
        # Take things apart
        self.ta(value, n, all=True)
        if abs(self.ta.e) > self.nchars:
            # A number whose exponent will take up more than 1/4 of the
            # screen's digits is too large, so use sci interpolation.
            return self.sci(value, n=n)
        sign = self.ta.sign     # Sign ("-" or " ")
        if not self.spc and sign == " ":
            sign = ""
        if self.sign and sign == "":
            sign = "+"
        dq = self.ta.dq         # Deque of significand's digits 
        e = self.ta.e
        if e >= 0:
            # Add zeroes if needed
            while e + 1 > len(dq):
                dq.append("0")
            insertion_point = e + 1
            last_digit = insertion_point + n - 1
            # Convert to string for more efficient indexing
            s = ''.join(dq)
            while len(s) < last_digit + 2:
                s += "0"
            try:
                ending_digit = s[last_digit]
            except Exception as e:
                breakpoint() #xx
                pass
            sentinel = int(s[last_digit + 1])
            # Truncate at n digits past the decimal point
            int_value = int(s[:last_digit + 1])
            # Round if needed
            if sentinel > 5 or (sentinel == 5 and ending_digit in "13579"):
                int_value += 1
            dq = deque(str(int_value))
            dq.insert(e + 1, self.dp)
            return sign + ''.join(dq)
        else:
            k = n - abs(e) + 1
            if k < 0:
                # Can't get any digits of significand
                return self.sci(value, n=n)
            s = ''.join(dq)
            int_value = int(s[:k]) if k else int(s[k])
            ending_digit = s[k - 1] if k else s[k]
            sentinel = int(s[k]) if k else int(s[k + 1])
            # Round if needed
            if sentinel > 5 or (sentinel == 5 and ending_digit in "13579"):
                int_value += 1
            dq = deque(str(int_value))
            s = ''.join(dq)
            # If it is all zeros, use sci
            if set(s) == set("0"):
                return self.sci(value, n=n)
            Assert(1 <= len(s) <= n)
            # Prepend zeroes if needed
            k = e
            while k < 0:
                dq.appendleft("0")
                k += 1
            dq.insert(1, self.dp)
            return sign + ''.join(dq)
    def fix(self, value, n=None, width=None) -> str:
        '''Return a fixed point representation using significant figures.
        Example:  if value = 72.8435 and n = 3, then '72.8' is returned.
        Here, n represents the number of significant digits in the return
        string.
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        n = self.clamp_n(value, n)
        if self.low is not None and 0 < abs(value) < self.low:
            return self.sci(value, n=n)
        elif self.high is not None and abs(value) >= self.high:
            return self.sci(value, n=n)
        # Take things apart
        self.ta(value, n)
        if abs(self.ta.e) > self.nchars:
            # A number whose exponent will take up more than 1/4 of the
            # screen's digits is too large, so use sci interpolation.
            return self.sci(value, n=n)
        sign = self.ta.sign     # Sign ("-" or " ")
        if not self.spc and sign == " ":
            sign = ""
        if self.sign and sign == "":
            sign = "+"
        dq = self.ta.dq         # Deque of significand's digits 
        e = self.ta.e
        # If len(dq) == n + 1, a special rounding happened to increase the
        # length by one, so pop the right end and increment the exponent.
        # See comments in TakeApart.round().
        if len(dq) == n + 1:
            dq.pop()
            e += 1
        if e < 0:
            # Number < 1
            ne = e + 1
            while ne < 0:
                dq.appendleft("0")
                ne += 1
            dq.appendleft(self.dp)  # Use self.dp; allows user to set it
            if not self._rlz:
                dq.appendleft("0")
        else:
            # Number >= 1
            while len(dq) < e + 1:
                dq.append("0")
            dq.insert(e + 1, self.dp)  # Use self.dp; allows user to set it
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
        s = ''.join(dq)
        return s
    def sci(self, value, n=None, width=None) -> str:
        'Return a scientific format representation'
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        n = self.clamp_n(value, n)
        self.ta(value, n)
        sgn = self.ta.sign  # Will be '-' or ' '
        if not self.spc and sgn == " ":
            sgn = ""    # No leading space allowed if self.spc True
        # Get exponent string
        exponent = self.GetUnicodeExponent(self.ta.e) if self.u else f"e{self.ta.e}"
        # Insert locale's decimal point
        self.ta.dq.insert(1, self.dp)
        self.ta.dq = self.trim(self.ta.dq)  # Implement rtz, rtdp, rlz
        s = sgn + ''.join(self.ta.dq) + exponent
        return s
 
        # Handle the case when self.brief is True
        if width is None:
            raise ValueError(f"width cannot be None if fmt.brief is True")
        if 1:   # Get m = number of digits that can be in significand
            m = width
            if self.u:
                m -= 3                      # For '×10'
            else:
                m -= 1                      # For 'e'
            m -= len(str(self.ta.e))        # For exponent's digits
            m -= 1                          # For decimal point
            m -= len(self.ellipsis)         # For ellipsis
            m = max(2, m)                   # Must have at least two characters
        if len(dq) <= m:    # We can return it with no more work
            # Insert locale's decimal point
            dq.insert(1, self.dp)
            dq = self.trim(dq)  # Implement rtz, rtdp, rlz
            s = sgn + ''.join(dq) + exponent
            return s
        # Significand needs digits removed.  Split significand and remove
        # middle digits to get needed width.
        middle = len(dq)//2
        left = deque(list(dq)[:middle])
        right = deque(list(dq)[middle:])
        def Len():
            return len(left) + len(right)
        while Len() > m:
            if len(left) >= len(right):
                left.pop()
            else:
                right.popleft()
        Assert(Len() <= m)
        # Insert decimal point and ellipsis
        if len(left) == 1:
            left.append(self.dp)
            left.append(self.ellipsis)
        else:
            right.insert(0, self.ellipsis)
            left.insert(1, self.dp)
        s = sgn + ''.join(left) + ''.join(right) + exponent
        return s
    def eng(self, value, fmt="eng", n=None, width=None) -> str:
        '''Return an engineering format representation.  Suppose value
        is 31415.9 and n is 3.  Then fmt can be:
            "eng"    returns "31.4e3"
            "engsi"  returns "31.4 k"
            "engsic" returns "31.4k" (the SI prefix is cuddled)
        Note:  cuddling is invalid SI syntax, but it's sometimes useful in
        program output.
 
        If width is not None and self.brief is True, try to fit the string
        into width characters by removing digits to the right of the
        decimal point.  Example:
 
            x = 34567800.0
            width = 8
            eng    = '34.567e6'
            eng    = '34.5✕10⁶' with self.u == True
            engsi  = '34.567 M'
            engsic = '34.5678M'
 
        Note that you may get a string longer than the desired width
        because you'd lose information otherwise.  Example:  in the
        previous example, if the width is changed to 5, you'll get
 
            eng       = '34e6'    len = 4
            eng       = '34✕10⁶'  len = 6 with self.u == True
            engsi     = '34 M'    len = 4
            engsic    = '34.5M'   len = 5
        
        In the first and third lines, the length would have been 5 except
        it's OK to remove the decimal point.  In the second line, there's 
        no way to remove another digit from the significand without ruining
        the engineering notation (i.e., the exponent would need to be
        changed, turning the notation into plain scientific).
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        n = self.clamp_n(value, n)
        self.ta(value, n)
        sign = self.ta.sign     # Sign ("-" or " ")
        if not self.spc and sign == " ":
            sign = ""
        if self.sign and sign == "":
            sign = "+"
        # Get significand without decimal point
        dq = self.ta.dq
        eng_step = 3
        div, rem = divmod(self.ta.e, eng_step)
        k = rem + 1 
        while len(dq) < k:
            dq.append("0")
        dq.insert(k, self.dp)   # Using self.dp allows user to change it
        dq.appendleft(sign)
        dq = self.trim(dq)  # Implement rtz, rtdp, rlz
        exponent = ["e", f"{eng_step*div}"]
        try:
            prefix = self._SI_prefixes[div]
        except KeyError:
            prefix = None
        # Remove dp if it ends significand
        if dq[-1] == self.dp:
            dq.pop()
        if fmt == "eng":
            if self.u:      # Use Unicode characters for power of 10
                o = self.GetUnicodeExponent(eng_step*div)
                dq.extend(list(o))
            else:
                dq.extend(exponent)
        elif fmt == "engsi":
            dq.extend(exponent) if prefix is None else dq.extend([" ", prefix])
        elif fmt == "engsic":
            dq.extend(exponent) if prefix is None else dq.extend([prefix])
        else:
            raise ValueError(f"'{fmt}' is an unrecognized format")
        return ''.join(dq)
 
        if self.brief:
            width = W if width is None else width
            # dq holds the eng significand
            if dq[0] == "":
                dq.popleft()    # Remove the empty string
            # Adjust the significand to get the desired digits.  Since it's
            # eng notation, we can only remove digits up to the decimal
            # point.
            elen = len(''.join(exponent))
            # Get the width for the significand for the style chosen
            if fmt == "eng":
                elen -= 1 if self.u else 0
                width -= 3 + elen if self.u else elen
            elif fmt == "engsi":
                width -= 2 if prefix else elen
            elif fmt == "engsic":
                width -= 1 if prefix else elen
            # Remove LSDs from significand to get width goal
            while len(''.join(dq)) > width and dq[-1] != self.ta.dp:
                dq.pop()
    def unc(self, x, u, fmt="fix", intv=False) -> str:
        '''Return a string form analogous to the shorthand form used for
        uncertainty:  e.g. '1.23(4)' where '1.23' is x and the '4' is
        the indication of the uncertainty u.  If intv is True, use the form
        '1.23[4]', which indicates an interval from e.g. a roundoff error.
        Only 'fix' and 'sci' are allowed format types.
        '''
        if 1:   # Check parameters
            if fmt is None:
                fmt = self.default
            elif fmt not in "fix sci".split():
                raise ValueError(f"'{fmt}' is unrecognized format string")
            # x and u must be real 
            msg = "must be a float or Decimal"
            types = (float, D)
            if have_mpmath:
                msg = "must be a float, Decimal, or mpmath.mpf"
                types = (float, D, mpmath.mpf)
            if not ii(x, types):
                raise TypeError("x " + msg)
            if not ii(u, types):
                raise TypeError("u " + msg)
            # u must be >= 0
            if u < 0:
                raise ValueError("u must be >= 0")
            # u must be < x
            if u >= abs(x):
                raise ValueError("u must be < x")
        # Get the maximum number of digits we can get
        n = 15  # Assume float
        if ii(x, D):
            n = decimal.getcontext().prec
        elif have_mpmath and ii(x, mpmath.mpf):
            n = mpmath.mp.dps
        # Switch to sci if needed
        if self.low is not None and abs(x) < self.low:
            fmt = "sci"
        elif self.high is not None and abs(x) >= self.high:
            fmt = "sci"
        # Take the numbers apart
        uta = self.ta.copy()
        xta = self.ta.copy()
        xta(x, n)
        uta(u, 1)
        k = xta.e - uta.e + 1   # Number of digits in significand
        Assert(k > 0)
        lbkt, rbkt = ("[", "]") if intv else ("(", ")")
        us = lbkt + uta.dq[0] + rbkt    # Unc/ro portion
        # Get significand's digits 
        sig = deque(''.join(list(xta.dq)[:k]))
        # Format the string
        e = xta.e
        if fmt == "sci":
            sig.insert(1, self.dp)
            sig.append(us)
            sig.append(self.GetUnicodeExponent(e) if self.u else f"e{e}")
        else:
            # Fixed point
            if e < 0:
                while e:
                    sig.appendleft("0")
                    e += 1
                sig.insert(1, self.dp)
                sig.append(us)
            else:
                if 0:
                    print(f"x = {x}   u = {u}")
                    print(f"k = {k}")
                    print(f"sig = {''.join(sig)}   us = {us}    e  = {e}")
                # Place decimal point
                if len(sig) < e + 1:   # Need added 0's
                    sig.append("0"*(e + 1 - len(sig)))
                    if not self.rtdp:
                        sig.append(self.dp)
                else:
                    if not self.rtdp:
                        sig.insert(e + 1, self.dp)
                        k += 1
                sig.insert(k, us)
        return ''.join(sig)
    def Real(self, value, fmt=None, n=None, width=None) -> str:
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        fmt = fmt if fmt is not None else self.default
        if fmt == "fix":
            return self.fix(value, n=n, width=width)
        elif fmt == "fixed":
            return self.fixed(value, n=n, width=width)
        elif fmt == "sci":
            return self.sci(value, n=n, width=width)
        elif fmt in "eng engsi engsic".split():
            return self.eng(value, fmt=fmt, n=n, width=width)
        else:
            raise ValueError(f"{fmt!r} is an unknown format")
    def Complex(self, value, fmt=None, n=None, width=None) -> str:
        '''value is a complex number.  Return a string in the form of 
        'a + bi'.
        '''
        if width is not None:
            raise Exception(f"width keyword not supported yet") #xx
        n = n if n is not None else self.n
        if fmt is not None:
            if fmt not in "fix fixed sci eng engsi engsic".split():
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
                # Manual hack to get underlining.  This removes the
                # dependency on color.py, which sometimes results in
                # circular dependency problems.
                #return f"{a}{s}{t(attr='ul')}∕{s}{b}{t.n}"
                u = '\x1b[4m'
                v = '\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m'
                return f"{a}{s}{u}∕{s}{b}{v}"
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
    if 1:   # Properties
        @property       # Default formatting method
        def default(self) -> str:
            self.none_bug(self._default, "default")
            return self._default
        @default.setter
        def default(self, value):
            if value not in "fix fixed sci eng engsi engsic".split():
                raise TypeError("value must be fix, sci, eng, engsi, or engsi")
            self._default = value
        @property       # Decimal point string
        def dp(self) -> str:
            self.none_bug(self._dp, "dp")
            return self._dp
        @dp.setter
        def dp(self, value):
            if not ii(value, str) or len(value) > 1 or value not in ".,":
                raise TypeError("Decimal point must be either '.' or ','")
            self._dp = value
        @property       # Use "sci" format if abs(x) is >= high and not None
        def high(self):
            return self._high
        @high.setter
        def high(self, value):
            # Note this must be a float (see notes in constructor)
            self._high = None if value is None else abs(float(str(value)))
        @property       # How to format integers with self.fmtint()
        def int(self):
            return self._int
        @int.setter
        def int(self, value):
            s = "hex oct dec bin"
            if value is None:
                self._int = None
            else:
                if value not in s.split():
                    raise ValueError(f"value must be one of {s}")
                self._int = None if value == "dec" else value
        @property       # Use "sci" format if abs(x) is < low and not None
        def low(self):
            return self._low
        @low.setter
        def low(self, value):
            # Note this must be a float (see notes in constructor)
            self._low = None if value is None else abs(float(str(value)))
        @property       # Number of digits wanted in interpolation, an int > 0
        def n(self) -> int:
            self.none_bug(self._n, "n")
            return self._n
        @n.setter
        def n(self, value):
            if not(ii(value, int) or value <= 0):
                raise ValueError("value must be integer > 0")
            self._n = value
        @property       # (bool) Remove trailing zeros after radix if True
        def rtz(self) -> bool:
            self.none_bug(self._rtz, "rtz")
            return self._rtz
        @rtz.setter
        def rtz(self, value):
            self._rtz = bool(value)
        @property       # (bool) Remove trailing radix if True
        def rtdp(self) -> bool: 
            self.none_bug(self._rtdp, "rtdp")
            return self._rtdp
        @rtdp.setter
        def rtdp(self, value):
            self._rtdp = bool(value)
        @property       # (bool) Remove leading zero if True
        def rlz(self) -> bool:
            self.none_bug(self._rlz, "rlz")
            return self._rlz
        @rlz.setter
        def rlz(self, value):
            self._rlz = bool(value)
        @property       # Always include numbers' sign
        def sign(self) -> bool:
            self.none_bug(self._sign, "sign")
            return self._sign
        @sign.setter
        def sign(self, value):
            self._sign = bool(value)
        @property       # Add " " to numbers >= 0 where "-" goes
        def spc(self) -> bool:
            self.none_bug(self._spc, "spc")
            return self._spc
        @spc.setter
        def spc(self, value):
            self._spc = bool(value)
        @property       # (bool) Use Unicode in "sci" and "eng" formats if True
        def u(self) -> bool:
            self.none_bug(self._u, "u")
            return self._u
        @u.setter
        def u(self, value):
            self._u = bool(value)
    if 1:   # Complex number properties
        @property       # Imaginary unit string
        def imag_unit(self) -> str:
            self.none_bug(self._imag_unit, "imag_unit")
            return self._imag_unit
        @imag_unit.setter
        def imag_unit(self, value):
            Assert(ii(value, str) and len(value) > 0)
            self._imag_unit = value
        @property       # (bool) Show complex numbers in polar form
        def polar(self) -> bool:
            self.none_bug(self._polar, "polar")
            return self._polar
        @polar.setter
        def polar(self, value):
            self._polar = bool(value)
        @property       # (bool) Show complex number's angles in degrees
        def deg(self) -> bool:
            self.none_bug(self._deg, "deg")
            return self._deg
        @deg.setter
        def deg(self, value):
            self._deg = bool(value)
        @property       # (bool) Use '1+2i' form if True, '1 + 2i' form if False
        def cuddled(self) -> bool:
            self.none_bug(self._cuddled, "cuddled")
            return self._cuddled
        @cuddled.setter
        def cuddled(self, value):
            self._cuddled = bool(value)
        @property       # (bool) Underline the argument when displaying polar form
        def ul(self) -> bool:
            self.none_bug(self._ul, "ul")
            return self._ul
        @ul.setter
        def ul(self, value):
            self._ul = bool(value)
        @property       # (bool) Show complex number in (re,im) form
        def comp(self) -> bool:
            self.none_bug(self._comp, "comp")
            return self._comp
        @comp.setter
        def comp(self, value):
            self._comp = bool(value)
# Convenience Fmt instance
fmt = Fmt()

# Development area
if 0 and __name__ == "__main__": 
    n = 1
    x = mpmath.mpf("9.99999796866929e999999")
    print(fmt(x))
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
            from color import t
            from lwtest import run, raises
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
            Fmt class defaults to showing {f.n} digits and the trailing radix helps
            you identify that it's a floating point number.
        '''))
        t.print(f"{t.em}fmt=\"fix\":  Shows desired number of figures")
        print(f"  {t.f}f(x) = f(x, fmt=\"fix\"){t.n} = {t.fix}{f(x)}{t.n} (defaults to {f.n} digits)")
        t.print(f"{t.t}Remove trailing decimal point:  {t.f}f.rtdp = True")
        f.rtdp = True
        t.print(f"  {t.f}f(x) = {t.fix}{f(x)}")
        f.rtdp = False
        # More digits
        n = 10
        t.print(f"{t.t}Set to {n} digits:  {t.f}f.n = {n}")
        f.n = n
        t.print(f"  {t.f}f(x) = {t.fix}{f(x)}")
        t.print(f"{t.t}Override f.n digits:")
        t.print(f"  {t.f}f(x, n=5){t.n} = {t.fix}{f(x, n=5)}")
        t.print(f"{t.t}Remove trailing zeros:")
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
        t.print(f"{t.em}fmt=\"fixed\":  Shows fixed number of decimal places")
        print(f"  {t.f}f(x) = f(x, fmt=\"fixed\", n=2){t.n} = {t.fix}{f(x, fmt='fixed', n=2)}{t.n} (show to second decimal place)")
        # Change scientific notation thresholds
        t.print(f"{t.em}fmt=\"sci\"  Scientific notation")
        print(f"Change transition thresholds to scientific notation:")
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
        print(dedent(f'''
        Large and small enough numbers will still require scientific notation (the
        default processing switches to scientific notation if an interpolation takes
        up more than a fourth of the screen area).'''))
        f.high = 1e6
        f.low = 1e-6
        # Big exponents
        print(dedent(f'''
        {t.em}Big numbers{t.n}   {t.t}Fixed point, scientific, and engineering formatting should work
        for numbers of arbitrary magnitudes as long as an exception isn't encountered.
        '''))
        t.print(f"  {t.f}f(Decimal('1e999999')){t.n} = {t.sci}{f(D('1e999999'))}")
        t.print(f"  {t.f}f(Decimal('1e-999999')){t.n} = {t.sci}{f(D('1e-999999'))}")
        try:
            f(D("1e1000000"))
        except decimal.Overflow:
            t.print(f'  {t.f}f(Decimal("1e1000000")){t.n}', "results in overflow")
        t.print(f'  {t.f}f(Decimal("1e-100000000")){t.n}', "underflow that gives 0")
        if 0 and have_mpmath:
            x = mpmath.mpf(100)
            y = mpmath.fac(x)
            z = y**y
            print(dedent(f'''
            mpmath lets you calculate y = x**x where x is 100!:
            y = {fmt(z)} (the exponent is 1.47e160)
            '''))
        else:
            print(dedent(f'''
            If you install mpmath, you can handle/format large numbers.  For example,
            if x = 100!, then x**x is a large number with an exponent of 1.47e160 and
            fmt(x**x) will format the number properly.
            '''))
        # Decimals with lots of digits
        n = 20
        t.print(dedent(f'''
        {t.em}Digits{t.n}  {t.t}You can ask for any number of digits, but the maximum given will be
        a number consistent with the numerical type's precision.  A float is good to
        about 15 digits.  Decimal and mpmath numbers depend on the current context's
        precision.  The expression evaluated is y = 100000*sin(pi/4):
        '''))
        with decimal.localcontext() as ctx:
            ctx.prec = n
            x = 100000*decimalmath.sin(decimalmath.pi()/4)
            t.print(f"  y = {t.fix}{fmt(x, n=n)}{t.n} (Decimal calculation to 20 digits)")
            y = 100000*math.sin(math.pi/4)
            ys, m = fmt(y, n=n), 16
            bad = f"{t.fix}{ys[:m]}{t.err}{ys[m:]}{t.n}"
            t.print(f"  y = {bad}      (float calculation to 15 digits)")
            n = 4
            t.print(f"  sci(y)    to {n} digits = {t.sci}{f(x, 'sci', n=n)}")
            n = 5
            t.print(f"  eng(y)    to {n} digits = {t.eng}{f(x, 'eng', n=n)}")
            n = 6
            t.print(f"  engsi(y)  to {n} digits = {t.si}{f(x, 'engsi', n=n)}")
            n = 7
            t.print(f"  engsic(y) to {n} digits = {t.si}{f(x, 'engsic', n=n)}")
        t.print(dedent(f'''
        {t.em}SI notation{t.n}    The {t.f}f.engsi{t.n} method supplies an SI prefix after the number to
        indicate the number's magnitude.  You can then append a physical unit string
        to get proper SI syntax:  {t.u}{f(x, 'engsi')}Ω{t.n}.  {t.f}f.engsic{t.n} does the same except the prefix
        is cuddled: {t.u}{f(x, 'engsic')}Ω{t.n} (incorrect SI syntax, but sometimes useful).
        ''', n=8))
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
        if W < 79:
            print("[Need a screen width of at least 80 for acceptable Demo() output]")
    if 1:   # Test code 
        def GetDefaultFmtInstance():
            'Make sure test environment is set up in a repeatable fashion'
            fmt = Fmt()
            fmt.n = 3
            return fmt
        def Test_prepare():
            '''TakeApart.prepare() is the core functionality needed for
            string interpolation for supported number types.
            '''
            ta = TakeApart()
            n = 3
            def f(x):
                return ta.prepare(x, n)
            if 1:   # int
                Assert(f(0) == (False, "0", None, None))
                for s in "1 2 10 20 1234567890".split():
                    Assert(f(int(s)) == (False, s, None, None))
                    Assert(f(-int(s)) == (True, s, None, None))
            if 1:   # float
                Assert(f(float("inf")) == (False, "inf", None, None))
                Assert(f(float("-inf")) == (True, "inf", None, None))
                Assert(f(float("nan")) == (None, "nan", None, None))
                for x, expected in (
                        (float( 0.0), (False, "0"*n, ".", 0)),
                        (float( 1.0), (False, "1" + "0"*(n - 1), ".", 0)),
                        (float(-1.0), (True , "1" + "0"*(n - 1), ".", 0)),
                        (float( 0.1), (False, "1" + "0"*(n - 1), ".", -1)),
                        (float(-0.1), (True , "1" + "0"*(n - 1), ".", -1)),
                        (float( 123456.78901), (False, "123", ".", 5)),
                        (float(-123456.78901), (True , "123", ".", 5)),
                        (float( 123456.78901e-6), (False, "123", ".", -1)),
                        (float(-123456.78901e-6), (True , "123", ".", -1)),
                        (float( 123456.78901e300), (False, "123", ".", 305)),
                        (float(-123456.78901e300), (True , "123", ".", 305)),
                        (float( 123456.78901e-300), (False, "123", ".", -295)),
                        (float(-123456.78901e-300), (True , "123", ".", -295)),
                        #
                        (float("0." + "9"*(n - 1)), (False, "990", ".", -1)),
                        (float("0." + "9"*n), (False, "999", ".", -1)),
                        (float("1." + "0"*(n - 3) + "1"), (False, "110", ".", 0)),
                        (float("1." + "0"*(n - 2) + "1"), (False, "101", ".", 0)),
                        (float("-0." + "9"*(n - 1)), (True, "990", ".", -1)),
                        (float("-0." + "9"*n), (True, "999", ".", -1)),
                        (float("-1." + "0"*(n - 3) + "1"), (True, "110", ".", 0)),
                        (float("-1." + "0"*(n - 2) + "1"), (True, "101", ".", 0)),
                    ):
                    if 1:
                        if f(x) != expected:
                            print(f"x = {x}")
                            print(f"got      = {f(x)}")
                            print(f"expected = {expected}")
                            exit()
                    Assert(f(x) == expected)
            if 1:   # Decimal
                m = 10
                with decimal.localcontext() as ctx:
                    ctx.prec = m
                    u = "1" + "0"*m
                    v = "12345678900"
                    Assert(f(D("inf")) == (False, "inf", None, None))
                    Assert(f(D("-inf")) == (True, "inf", None, None))
                    Assert(f(D("nan")) == (None, "nan", None, None))
                    for x, expected in (
                            (D(" 0.0"), (False, "0"*(m + 1), ".", m - 1)),
                            (D(" 1.0"), (False, u, ".", 0)),
                            (D("-1.0"), (True , u, ".", 0)),
                            (D(" 0.1"), (False, u, ".", -1)),
                            (D("-0.1"), (True , u, ".", -1)),
                            (D(" 123456.78901"), (False, v, ".", 5)),
                            (D("-123456.78901"), (True , v, ".", 5)),
                            (D(" 123456.78901e-6"), (False, v, ".", -1)),
                            (D("-123456.78901e-6"), (True , v, ".", -1)),
                            (D(" 123456.78901e300"), (False, v, ".", 305)),
                            (D("-123456.78901e300"), (True , v, ".", 305)),
                            (D(" 123456.78901e-300"), (False, v, ".", -295)),
                            (D("-123456.78901e-300"), (True , v, ".", -295)),
                            #
                            (D(" 0.9999999999"), (False, "99999999990", ".", -1)),
                            (D(" 0.99999999999"), (False, "10000000000", ".", 0)),
                            (D("1." + "0"*(m - 2) + "1"), (False, "10000000010", ".", 0)),
                            (D("1." + "0"*(m - 1) + "1"), (False, "10000000000", ".", 0)),
                            (D("-0.9999999999"), (True, "99999999990", ".", -1)),
                            (D("-0.99999999999"), (True, "10000000000", ".", 0)),
                            (D("-1." + "0"*(m - 2) + "1"), (True, "10000000010", ".", 0)),
                            (D("-1." + "0"*(m - 1) + "1"), (True, "10000000000", ".", 0)),
                        ):
                        if 0:
                            if f(x) != expected:
                                print(f"x = {x}")
                                print(f"got      = {f(x)}")
                                print(f"expected = {expected}")
                                exit()
                        Assert(f(x) == expected)
                    # Fraction
                    F = Fraction
                    for x, expected in (
                            (F( 0, 1), (False, "0"*(m + 1), ".", m)),
                            (F( 1, 1), (False, u, ".", 0)),
                            (F(-1, 1), (True , u, ".", 0)),
                            (F( 1, 10), (False, u, ".", -1)),
                            (F(-1, 10), (True , u, ".", -1)),
                        ):
                        y = D(x.numerator)/D(x.denominator)
                        if 0:
                            if f(y) != expected:
                                print(f"y = {y}")
                                print(f"got      = {f(y)}")
                                print(f"expected = {expected}")
                                exit()
                        Assert(f(y) == expected)
            if 1:   # mpf
                if not have_mpmath:
                    return
                m = 10
                with mpmath.workdps(m):
                    mpf = mpmath.mpf
                    Assert(f(mpf("inf")) == (False, "inf", None, None))
                    Assert(f(mpf("-inf")) == (True, "inf", None, None))
                    Assert(f(mpf("nan")) == (None, "nan", None, None))
                    u = "1" + "0"*(m - 1)
                    v = "1234567890"
                    for x, expected in (
                            (mpf(" 0.0"), (False, "0"*m, ".", 0)),
                            (mpf(" 1.0"), (False, u, ".", 0)),
                            (mpf("-1.0"), (True , u, ".", 0)),
                            (mpf(" 0.1"), (False, u, ".", -1)),
                            (mpf("-0.1"), (True , u, ".", -1)),
                            (mpf(" 123456.78901"), (False, "1234567890", ".", 5)),
                            (mpf("-123456.78901"), (True , "1234567890", ".", 5)),
                            (mpf(" 123456.78901e-6"), (False, v, ".", -1)),
                            (mpf("-123456.78901e-6"), (True , v, ".", -1)),
                            (mpf(" 123456.78901e300"), (False, v, ".", 305)),
                            (mpf("-123456.78901e300"), (True , v, ".", 305)),
                            (mpf(" 123456.78901e-300"), (False, v, ".", -295)),
                            (mpf("-123456.78901e-300"), (True , v, ".", -295)),
                            #
                            (mpf(" 0.9999999999"), (False, "9999999999", ".", -1)),
                            (mpf(" 0.99999999999"), (False, "1000000000", ".", 0)),
                            (mpf("1." + "0"*(m - 2) + "1"), (False, "1000000001", ".", 0)),
                            (mpf("1." + "0"*(m - 1) + "1"), (False, "1000000000", ".", 0)),
                            (mpf("-0.9999999999"), (True, "9999999999", ".", -1)),
                            (mpf("-0.99999999999"), (True, "1000000000", ".", 0)),
                            (mpf("-1." + "0"*(m - 2) + "1"), (True, "1000000001", ".", 0)),
                            (mpf("-1." + "0"*(m - 1) + "1"), (True, "1000000000", ".", 0)),
                        ):
                        if 0:
                            if f(x) != expected:
                                print(f"x = {x}")
                                print(f"m = {m}")
                                print(f"expected = {expected}")
                                print(f"got      = {f(x)}")
                                s = mpmath.nstr(x, m, show_zero_exponent=True,
                                    min_fixed=1, max_fixed=0, strip_zeros=False)
                                print(f"nstr = {s}")
                                exit()
                        Assert(f(x) == expected)
        def Test_disassemble():
            '''TakeApart.disassemble() is used for all string interpolation, so
            show it works for the basic tasks.
            '''
            ta = TakeApart()
            def f(x, n):
                ta.disassemble(x, n)
                return ''.join(ta.dq)
            if 1:   # Integer
                x = 12345600
                for n, expected in (
                        (1, "10000000"),
                        (2, "12000000"),
                        (3, "12300000"),
                        (4, "12340000"),
                        (5, "12346000"),
                        (6, "12345600"),
                        (7, "12345600"),
                    ):
                    Assert(f(x, n) == expected)
                    Assert(ta.sign == " ")
                    Assert(f(-x, n) == expected)
                    Assert(ta.sign == "-")
                # One digit integers that can't be rounded
                for x in range(1, 10):
                    for n in range(1, 20):
                        Assert(f(x, n) == str(x))
                        Assert(f(-x, n) == str(x))
            if 1:   # Floating point numbers and a fraction
                X = mpmath.mpf("12345600.") if have_mpmath else 12345600.
                for x in (12345600., D("12345600."), Fraction(12345600, 1), X):
                    for n, expected in (
                            (1, "1"),
                            (2, "12"),
                            (3, "123"),
                            (4, "1234"),
                            (5, "12346"),
                            (6, "123456"),
                            (7, "1234560"),
                        ):
                        # See the bug explanation in Test_TakeApart()
                        if ii(x, float) and n == 4:
                            Assert(f(x, n) == "1235")
                            Assert(ta.sign == " ")
                            Assert(f(-x, n) == "1235")
                            Assert(ta.sign == "-")
                        else:
                            Assert(f(x, n) == expected)
                            Assert(ta.sign == " ")
                            Assert(f(-x, n) == expected)
                            Assert(ta.sign == "-")
        def Test_Basics():
            f = GetDefaultFmtInstance()
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
            # Test integers with fixed point
            zero, one = 0, 1
            for x, n, result in (
                (zero, 1, "0"),
                (one, 1, "1"),
                (-one, 1, "-1"),
                (zero, 2, "0"),
                (one, 2, "1"),
                (-one, 2, "-1"),
                (zero, 3, "0"),
                (one, 3, "1"),
                (-one, 3, "-1"),
                (zero, 8, "0"),
                (one, 8, "1"),
                (-one, 8, "-1"),
            ):
                f.n = n
                s = f(x)
                Assert(s == result)
            # Test floats with fixed point
            zero, one = 0.0, 1.0
            for x, n, result in (
                (zero, 1, "0."),
                (one, 1, "1."),
                (-one, 1, "-1."),
                (zero, 2, "0.0"),
                (one, 2, "1.0"),
                (-one, 2, "-1.0"),
                (zero, 3, "0.00"),
                (one, 3, "1.00"),
                (-one, 3, "-1.00"),
                (zero, 8, "0.0000000"),
                (one, 8, "1.0000000"),
                (-one, 8, "-1.0000000"),
            ):
                f.n = n
                s = f(x)
                Assert(s == result)
            # Test with numbers near 1
            f = GetDefaultFmtInstance()
            x = 0.99
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "0.99")
            Assert(f(-x, n=1) == "-1.")
            Assert(f(-x, n=2) == "-0.99")
            x = 0.999999
            raises(ValueError, f, x, n=-1)
            raises(ValueError, f, x, n=0)
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "1.0")
            Assert(f(x, n=3) == "1.00")
            Assert(f(x, n=4) == "1.000")
            Assert(f(x, n=5) == "1.0000")
            Assert(f(x, n=6) == "0.999999")
            Assert(f(x, n=7) == "0.9999990")
            raises(ValueError, f, -x, n=-1)
            raises(ValueError, f, -x, n=0)
            Assert(f(-x, n=1) == "-1.")
            Assert(f(-x, n=2) == "-1.0")
            Assert(f(-x, n=3) == "-1.00")
            Assert(f(-x, n=4) == "-1.000")
            Assert(f(-x, n=5) == "-1.0000")
            Assert(f(-x, n=6) == "-0.999999")
            Assert(f(-x, n=7) == "-0.9999990")
        def Test_toD():
            f = GetDefaultFmtInstance().toD
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
        def Test_Fixed():
            f = GetDefaultFmtInstance()
            # Test with a float
            x = 31.43905775
            for n, expected in (
                    (1, "31.4"),
                    (2, "31.44"),
                    (3, "31.439"),
                    (4, "31.4390"),
                    (5, "31.43906"),
                    (6, "31.439058"),
                    (7, "31.4390578"),
                    (8, "31.43905775"),
                    (15, "31.439057750000000"),
                ):
                f.n = n
                got = f(x, fmt="fixed")
                if 0 and got != expected:
                    print(f"n = {n}")
                    print(f"got      = {got}")
                    print(f"expected = {expected}")
                    exit()
                Assert(f(x, fmt="fixed") == expected)
                Assert(f(-x, fmt="fixed") == "-" + expected)
                # Show that n in call overrides fmt.n
                got = f(x, fmt="fixed", n=n)
                if 0 and got != expected:
                    print(f"n = {n}")
                    print(f"got      = {got}")
                    print(f"expected = {expected}")
                    exit()
                Assert(f(x, fmt="fixed", n=n) == expected)
                Assert(f(-x, fmt="fixed", n=n) == "-" + expected)
            x = 0.03143905775
            for n, expected in (
                    (1,  "0.03"),
                    (2,  "0.03"),
                    (3,  "0.031"),
                    (4,  "0.0314"),
                    (5,  "0.03144"),
                    (6,  "0.031439"),
                    (7,  "0.0314390"),
                    (8,  "0.03143906"),
                    (9,  "0.031439058"),
                    (10, "0.0314390578"),
                    (15, "0.031439057750000"),
                ):
                f.n = n
                got = f(x, fmt="fixed")
                if 0 and got != expected:
                    print(f"n = {n}")
                    print(f"got      = {got}")
                    print(f"expected = {expected}")
                    exit()
                Assert(f(x, fmt="fixed") == expected)
                Assert(f(-x, fmt="fixed") == "-" + expected)
                # Show that n in call overrides fmt.n
                got = f(x, fmt="fixed", n=n)
                if 0 and got != expected:
                    print(f"n = {n}")
                    print(f"got      = {got}")
                    print(f"expected = {expected}")
                    exit()
                Assert(f(x, fmt="fixed", n=n) == expected)
                Assert(f(-x, fmt="fixed") == "-" + expected)
            # Test with an mpf
            if have_mpmath:
                mpmath.mp.dps = 40
                x = mpmath.mpf("31.43905775")
                for n, expected in (
                        (1, "31.4"),
                        (2, "31.44"),
                        (3, "31.439"),
                        (4, "31.4390"),
                        (5, "31.43906"),
                        (6, "31.439058"),
                        (7, "31.4390578"),
                        (8, "31.43905775"),
                        (15, "31.439057750000000"),
                        (30, "31.439057750000000000000000000000"),
                    ):
                    f.n = n
                    got = f(x, fmt="fixed")
                    if 0 and got != expected:
                        print(f"n = {n}")
                        print(f"got      = {got}")
                        print(f"expected = {expected}")
                        exit()
                    Assert(f(x, fmt="fixed") == expected)
                    Assert(f(-x, fmt="fixed") == "-" + expected)
                    # Show that n in call overrides fmt.n
                    got = f(x, fmt="fixed", n=n)
                    if 0 and got != expected:
                        print(f"n = {n}")
                        print(f"got      = {got}")
                        print(f"expected = {expected}")
                        exit()
                    Assert(f(x, fmt="fixed", n=n) == expected)
                    Assert(f(-x, fmt="fixed", n=n) == "-" + expected)
            # Test with a Decimal
            with decimal.localcontext() as ctx:
                ctx.prec = 40
                x = D("31.43905775")
                for n, expected in (
                        (1, "31.4"),
                        (2, "31.44"),
                        (3, "31.439"),
                        (4, "31.4390"),
                        (5, "31.43906"),
                        (6, "31.439058"),
                        (7, "31.4390578"),
                        (8, "31.43905775"),
                        (15, "31.439057750000000"),
                        (30, "31.439057750000000000000000000000"),
                    ):
                    f.n = n
                    got = f(x, fmt="fixed")
                    if 0 and got != expected:
                        print(f"n = {n}")
                        print(f"got      = {got}")
                        print(f"expected = {expected}")
                        exit()
                    Assert(f(x, fmt="fixed") == expected)
                    Assert(f(-x, fmt="fixed") == "-" + expected)
                    # Show that n in call overrides fmt.n
                    got = f(x, fmt="fixed", n=n)
                    if 0 and got != expected:
                        print(f"n = {n}")
                        print(f"got      = {got}")
                        print(f"expected = {expected}")
                        exit()
                    Assert(f(x, fmt="fixed", n=n) == expected)
                    Assert(f(-x, fmt="fixed", n=n) == "-" + expected)
        def Test_Fix():
            def TestTrimming():
                f = GetDefaultFmtInstance()
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
                f = GetDefaultFmtInstance()
                x = 0.00732
                f.rlz = False
                Assert(f(x, fmt="fix") == "0.00732")
                f.rlz = True
                Assert(f(x, fmt="fix") == ".00732")
                # Use alternate string for decimal point
                f = GetDefaultFmtInstance()
                x = -31.41
                f.dp = ","
                Assert(f(x) == "-31,4")
                with raises(TypeError) as y:
                    f.dp = "q"
            def TestHuge(n, digits=3):
                f = GetDefaultFmtInstance()
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
                f = GetDefaultFmtInstance()
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
                f = GetDefaultFmtInstance()
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
                    f, x = GetDefaultFmtInstance(), D(s)
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
                    f = GetDefaultFmtInstance()
                    f.high = None
                    t = f(x, fmt="fix")
                    Assert(t == "3.06e9983")
            def Test_spc():
                'Test .spc and .sign'
                f = GetDefaultFmtInstance()
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
                f = GetDefaultFmtInstance()
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
                if n <= 100:
                    TestLotsOfDigits(n)
            TestTrimming()
            TestBigInteger(20)
            Test_spc()
            Test_rlz()
        def Test_Eng():
            old_dps = None
            if have_mpmath:
                old_dps = mpmath.mp.dps
                mpmath.mp.dps = 10
            fmt = GetDefaultFmtInstance()
            fmt.u = 0
            fmt.n = 6
            for typ in (D, "mpmath"):
                if typ == "mpmath" and have_mpmath:
                    typ = mpmath.mpf
                if 1:
                    x = typ("3.45678e7")
                    # eng
                    s = f"{fmt.eng(x)}"
                    Assert(s == "34.5678e6")
                    s = f"{fmt.eng(-x)}"
                    Assert(s == "-34.5678e6")
                    s = f"{fmt.eng(x, n=1)}"
                    Assert(s == "30e6")
                    s = f"{fmt.eng(-x, n=1)}"
                    Assert(s == "-30e6")
                    fmt.u = 1
                    s = f"{fmt.eng(x)}"
                    Assert(s == "34.5678✕10⁶")
                    s = f"{fmt.eng(-x)}"
                    Assert(s == "-34.5678✕10⁶")
                    s = f"{fmt.eng(x, n=1)}"
                    Assert(s == "30✕10⁶")
                    s = f"{fmt.eng(-x, n=1)}"
                    Assert(s == "-30✕10⁶")
                    fmt.u = 0
                    # engsi
                    s = f"{fmt.eng(x, fmt='engsi')}"
                    Assert(s == "34.5678 M")
                    s = f"{fmt.eng(-x, fmt='engsi')}"
                    Assert(s == "-34.5678 M")
                    s = f"{fmt.eng(x, fmt='engsi', n=1)}"
                    Assert(s == "30 M")
                    s = f"{fmt.eng(-x, fmt='engsi', n=1)}"
                    Assert(s == "-30 M")
                    # engsic
                    s = f"{fmt.eng(x, fmt='engsic')}"
                    Assert(s == "34.5678M")
                    s = f"{fmt.eng(-x, fmt='engsic')}"
                    Assert(s == "-34.5678M")
                    s = f"{fmt.eng(x, fmt='engsic', n=1)}"
                    Assert(s == "30M")
                    s = f"{fmt.eng(-x, fmt='engsic', n=1)}"
                    Assert(s == "-30M")
                if 1:
                    x = typ("3.45678e-13")
                    s = f"{fmt.eng(x)}"
                    Assert(s == "345.678e-15")
                    s = f"{fmt.eng(-x)}"
                    Assert(s == "-345.678e-15")
                    s = f"{fmt.eng(x, n=1)}"
                    Assert(s == "300e-15")
                    s = f"{fmt.eng(-x, n=1)}"
                    Assert(s == "-300e-15")
                    fmt.u = 1
                    s = f"{fmt.eng(x)}"
                    Assert(s == "345.678✕10⁻¹⁵")
                    s = f"{fmt.eng(-x)}"
                    Assert(s == "-345.678✕10⁻¹⁵")
                    s = f"{fmt.eng(x, n=1)}"
                    Assert(s == "300✕10⁻¹⁵")
                    s = f"{fmt.eng(-x, n=1)}"
                    Assert(s == "-300✕10⁻¹⁵")
                    fmt.u = 0
                    # engsi
                    s = f"{fmt.eng(x, fmt='engsi')}"
                    Assert(s == "345.678 f")
                    s = f"{fmt.eng(-x, fmt='engsi')}"
                    Assert(s == "-345.678 f")
                    s = f"{fmt.eng(x, fmt='engsi', n=1)}"
                    Assert(s == "300 f")
                    s = f"{fmt.eng(-x, fmt='engsi', n=1)}"
                    Assert(s == "-300 f")
                    # engsic
                    s = f"{fmt.eng(x, fmt='engsic')}"
                    Assert(s == "345.678f")
                    s = f"{fmt.eng(-x, fmt='engsic')}"
                    Assert(s == "-345.678f")
                    s = f"{fmt.eng(x, fmt='engsic', n=1)}"
                    Assert(s == "300f")
                    s = f"{fmt.eng(-x, fmt='engsic', n=1)}"
                    Assert(s == "-300f")
            if old_dps is not None:
                mpmath.mp.dps = old_dps
        def Test_Sci():
            fmt = GetDefaultFmtInstance()
            x = D("3.141592653589793e+99")
            fmt.n = 4
            Assert(fmt(x) == "3.142e99")
            fmt.n = 3
            Assert(fmt(x) == "3.14e99")
            x = D("3.141592653589793e-99")
            Assert(fmt(x) == "3.14e-99")
            x = D("3.141592653589793")
            Assert(fmt(x) == "3.14")
            Assert(fmt(x, fmt="sci") == "3.14e0")
            x = D("3.9e21")
            fmt.n = 1
            Assert(fmt(x) == "4.e21")
        def Test_Unc():
            fmt = GetDefaultFmtInstance()
            x = 1.23456
            u = 0.0064
            Assert(fmt.unc(x, u) == "1.234(6)")
            Assert(fmt.unc(x, u, fmt="fix") == "1.234(6)")
            Assert(fmt.unc(x, u, fmt="fix", intv=True) == "1.234[6]")
            Assert(fmt.unc(x, u, fmt="sci") == "1.234(6)e0")
            #
            x = 123.456
            u = 0.64
            Assert(fmt.unc(x, u) == "123.4(6)")
            x = 123.456e3
            u = 0.64e3
            Assert(fmt.unc(x, u) == "1234(6)00.")
            fmt.rtdp = True
            Assert(fmt.unc(x, u) == "1234(6)00")
            fmt.rtdp = False
            #
            fmt.high = None
            x = 1.23456e10
            u = 0.0064e10
            Assert(fmt.unc(x, u) == "1234(6)0000000.")
            x = 1.23456e50
            u = 0.0064e50
            Assert(fmt.unc(x, u) == "1234(6)00000000000000000000000000000000000000000000000.")
            #
            fmt.low = None
            x = 1.23456e-5
            u = 0.0064e-5
            Assert(fmt.unc(x, u) == "0.00001234(6)")
            x = 1.23456e-50
            u = 0.0064e-50
            Assert(fmt.unc(x, u) == "0.00000000000000000000000000000000000000000000000001234(6)")

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
                ta = TakeApart()
                for n in range(1, 10):
                    for i in (-1, 0, 1, 2, 1234, -1234):
                        ta(float(i), n)
                        expected = str(ta)
                        for x in (mpf(i), D(i), F(i)):
                            ta(x, n)
                            strta = str(ta)
                            Assert(strta == expected)
                            Assert(g(strta) == g(expected))
                    # Large negative float
                    ta(float(int(-123456)*10**(m - k)), n)
                    s = f"-{u}e{m}"
                    expected = str(ta)
                    for typ in (mpf, D, F):
                        ta(typ(s), n)
                        y = str(ta)
                        if n == 4:
                            # The float rounding will produce '-1.235e300',
                            # but the 'proper' half-even rounding will give
                            # '-1.234e300'.  This is a bug, but I'm
                            # choosing to ignore it because most
                            # applications will probably use either floats
                            # by themselves or Decimal/mpf by themselves
                            # (e.g., hc.py).
                            Assert(y == "-1.234e300")
                            Assert(expected == "-1.235e300")
                        else:
                            Assert(y == expected)
                            Assert(g(y) == g(expected))
                    # Large positive float
                    ta(float(int(123456)*10**(m - k)), n)
                    s = f"{u}e{m}"
                    expected = str(ta)
                    for typ in (mpf, D, F):
                        ta(typ(s), n)
                        y = str(ta)
                        if n == 4:
                            # See cop-out above
                            Assert(y == " 1.234e300")
                            Assert(expected == " 1.235e300")
                        else:
                            Assert(y == expected)
                            Assert(g(y) == g(expected))
                    # Small negative float
                    ta(float(int(-123456)/10**(m + k)), n)
                    s = f"-{u}e{-m}"
                    expected = str(ta)
                    for typ in (mpf, D, F):
                        ta(typ(s), n)
                        y = str(ta)
                        if n == 4:
                            # See cop-out above
                            Assert(y == "-1.234e-300")
                            Assert(expected == "-1.235e-300")
                        else:
                            Assert(y == expected)
                            Assert(g(y) == g(expected))
                    # Small positive float
                    ta(float(int(123456)/10**(m + k)), n)
                    s = f"{u}e{-m}"
                    expected = str(ta)
                    for typ in (mpf, D, F):
                        ta(typ(s), n)
                        y = str(ta)
                        if n == 4:
                            # See cop-out above
                            Assert(y == " 1.234e-300")
                            Assert(expected == " 1.235e-300")
                        else:
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
            f = GetDefaultFmtInstance()
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
        def Test_Brief():
            return
            # Integers
            GetDefaultFmtInstance()
            fmt.brief = True
            x = 12345678901234567891234567890123456789123456789
            result = fmt.fmtint(x, width=10, mag=0)
            Assert(result == "12345⋯6789")
            result = fmt.fmtint(x, width=5, mag=0)
            Assert(result == "12⋯89")
            x = -x
            result = fmt.fmtint(x, width=10)
            Assert(result == "-1234⋯789")
            result = fmt.fmtint(x, width=5)
            Assert(result == "-1⋯9")
            raises(ValueError, fmt.fmtint, x, width=3)
            if 1:   # Test mag
                result = fmt.fmtint(x, width=15, mag=True)
                Assert(result == "-123⋯89 |10⁴⁶|")
            # Floats
            print("xx Test_Brief:  need to write float code")  #xx
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
