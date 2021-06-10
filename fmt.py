'''
Format Decimal numbers
    The Fmt class will format any number/string accepted by Decimal's
    constructor into a string with the desired number of significant
    figures.  Run the module as a script to see example output.

    Use 'from fmt import fmt' to get fmt as a convenience instance of
    Fmt.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2008, 2012, 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Format Decimal numbers
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import collections 
    import locale 
if 1:   # Global variables
    D = decimal.Decimal
    ii = isinstance
    __all__ = [
        "Fmt",  # The Fmt class
        "D",    # decimal.Decimal abbreviation
        "fmt"   # Convenience instance of Fmt
    ]
class Fmt(object):
    # Key to _SI_prefixes is exponent/3
    _SI_prefixes = dict(zip(range(-8, 9), list("yzafpnμm.kMGTPEZY")))
    _superscripts = dict(zip("-+0123456789", "⁻⁺⁰¹²³⁴⁵⁶⁷⁸⁹"))
    def __init__(self, n=3, low=D("1e-5"), high=D("1e16")):
        '''n is the number of significant figures to format to.  
        low is the point below which scientific notation is used.
        high is the point above which scientific notation is used.
        low and high can be None, which disables them; if disabled, then
        fixed point interpolation is used by default.
        '''
        '''Implementation:  a number to format is first converted to a
        Decimal object D, then D is converted to a string with the
        desired number of significant figures using python's string
        interpolation f"{x:e}" with appropriate parameters.  This
        returns a string of the form sD.DDeD, which can be picked apart
        into the sign, significand, radix, and exponent.  These are then
        manipulated into the string form desired.  We assume python's
        string interpolation works for numbers with an arbitrary number
        of digits.  I've tested it up to numbers with nearly a million
        digits and it appears to work.
        '''
        Fmt._SI_prefixes[0] = ""    # Need empty string
        self._n = n
        self._u = False
        self._low = low if ii(low, D) else D(str(low))
        self._high = high if ii(high, D) else D(str(high))
    # Methods
    def _take_apart(self, x, n=None):
        '''Take the Decimal number x apart into its sign, digits,
        decimal point, and exponent.  Return the named tuple 
        Apart(sign, ld, dp, other, e) where:
            ld + dp + other is the significand: 
            ld is the leading digit
            dp is the locale's decimal point
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
    def _get_data(self, value, n=None):
        x = D(str(value))
        parts = self._take_apart(x, n)
        return (parts, collections.deque(parts.ld) + 
            collections.deque(parts.other), "0")
    def fix(self, value, n=None):
        'Return a fixed point representation'
        x = D(str(value))
        parts, d, z = self._get_data(x, n)
        ne = parts.e + 1
        if parts.e >= 0:
            while len(d) < ne:
                d.append(z)
            d.insert(ne, self.dp)
        else:
            while ne < 0:
                d.appendleft(z)
                ne += 1
            d.appendleft(self.dp)
            d.appendleft(z)
        d.appendleft(parts.sign)
        return ''.join(d)
    def sci(self, value, n=None):
        'Return a scientific format representation'
        x = D(str(value))
        parts, d, z = self._get_data(x, n)
        d.insert(1, self.dp)
        d.appendleft(parts.sign)
        if d[-1] == self.dp:
            del d[-1]
        if self.u:
            # Use Unicode characters for power of 10
            o = ["✕10"]
            for c in str(parts.e):
                o.append(Fmt._superscripts[c])
            d.extend(o)
        else:
            d.extend(["e", str(parts.e)])
        return ''.join(d)
    def eng(self, x, fmt="eng", n=None):
        '''Return an engineering format representation.  Suppose x is
        31415.9 and n is 3.  Then fmt can be:
            "eng"    returns "31.4e3"
            "engsi"  returns "31.4 k"
            "engsic" returns "31.4k" (the SI prefix is cuddled)
        '''
        fmt = fmt.strip().lower()
        parts, d, z = self._get_data(x, n)
        eng_step = 3
        div, rem = divmod(parts.e, eng_step)
        k = rem + 1 
        while len(d) < k:
            d.append(z)
        d.insert(k, self.dp)
        if d[-1] == self.dp:
            del d[-1]
        d.appendleft(parts.sign)
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
                d.extend(o)
            else:
                d.extend(exponent)
        elif fmt == "engsi":
            d.extend(exponent) if prefix is None else d.extend([" ", prefix])
        elif fmt == "engsic":
            d.extend(exponent) if prefix is None else d.extend([prefix])
        else:
            raise ValueError(f"'{fmt}' is an unrecognized format")
        return ''.join(d)
    def __call__(self, value, fmt="fix", n=None):
        '''Format value with the default "fix" formatter.  n overrides
        self.n significant figures.  fmt can be "fix", "sci", "eng", 
        "engsi", or "engsic".
        '''
        x = value if ii(value, D) else D(str(value))
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
    # Properties
    @property
    def dp(self):
        'Read-only decimal point string'
        return locale.localeconv()["decimal_point"]
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
    def n(self):
        'Number of significant figures (integer > 0)'
        return self._n
    @n.setter
    def n(self, value):
        self._n = int(value)
        assert(self._n > 0)
    @property
    def u(self):
        '(bool) Use Unicode in "sci" and "eng" formats if True'
        return self._u
    @u.setter
    def u(self, value):
        self._u = bool(value)
fmt = Fmt()     # Convenience instance
if __name__ == "__main__": 
    if 1:   # Imports
        from collections import deque
        from decimal import localcontext
        from math import pi
        from pdb import set_trace as xx
        import getopt
        import os
        import pathlib
        import sys
    if 1:   # Custom modules
        from fpformat import FPFormat
        from lwtest import run, raises, Assert
        from wrap import dedent
        import decimalmath
    if 1:   # Global variables
        P = pathlib.Path
        d = {}      # Options dictionary
    if 1:   # Example code 
        def Demo():
            f = fmt
            print("Demonstration of Fmt class features:  f = Fmt()\n")
            s = "pi*1e5"
            x = eval(s)
            # Standard formatting
            print(f"x = {s} = {repr(x)}")
            print(f"Standard fixed point formatting:")
            print(f"  f(x) = {f(x)} (defaults to {f.n} significant figures)")
            # 2 figures
            print(f"Set to 2 significant figures:  f.n = 2")
            f.n = 2
            print(f"  f(x) = {f(x)}")
            print(f"Override f.n significant figures:")
            print(f"  f(x, n=5) = {f(x, n=5)}")
            f.n = 3
            # Change where we switch to scientific notation
            print(f"Change transition thresholds to scientific notation")
            f.high = 1e6
            f.low = 1e-6
            print(f"  f.high = {f.sci(f.high, n=1)}")
            print(f"  f.low  = {f.sci(f.low, n=1)}")
            print(" ", f(pi*1e5), "  < f.high so use fix")
            print(" ", f(pi*1e6), "    > f.high so use sci")
            print(" ", f(pi*1e-6), "> f.low so use fix")
            print(" ", f(pi*1e-7), "   < f.low so use sci")
            # Get scientific and engineering notations
            print("Force use of scientific and engineering notation")
            print(f"  sci:  f.sci(pi*1e-7)        = {f.sci(pi*1e-7)}")
            print(f"        f(pi*1e-7, fmt='sci') = {f(pi*1e-7, fmt='sci')}")
            print(f"  eng:  f.eng(pi*1e-7)        = {f.eng(pi*1e-7)}")
            print(f"        f(pi*1e-7, fmt='eng') = {f(pi*1e-7, fmt='eng')}")
            # Use Unicode characters for scientific notation
            f.u = True
            print("Set f.u to True to use Unicode characters in sci and eng")
            print(f"  f.sci(pi*1e6)) = {f.sci(pi*1e6)}")
            print(f"  f.eng(pi*1e-7) = {f.eng(pi*1e-7)}")
            f.u = False
            # Set low & high to None to always get fixed point
            f.low = f.high = None
            print("Setting f.low and f.high to None gets fixed point always:")
            print(f"  f(pi*1e-27) = {f(pi*1e-27)}")
            print(f"  f(pi*1e57) = {f(pi*1e57)}")
            f.high = 1e6
            f.low = 1e-6
            # Big exponents
            print(dedent('''
            Fixed point, scientific, and engineering formatting should work for
            numbers of arbitrary magnitudes as long as a Decimal exception isn't 
            encountered.  The default Decimal context allows exponents up to an
            absolute value of (1e6 - 1).
            '''))
            print(f"  f(D('1e999999')) = {f(D('1e999999'))}")
            print(f"  f(D('1e-999999')) = {f(D('1e-999999'))}")
            try:
                f(D("1e1000000"))
            except decimal.Overflow:
                print('  f(D("1e1000000"))', "results in overflow")
            print('  f(D("1e-100000000"))', "underflow that gives 0")
            # Decimals with lots of digits
            print(dedent('''
            Arguments of the formatting functions can be Decimal numbers or any
            number type that can be converted to Decimal.  This means you can
            format with arbitrary numbers of significant digits up to the
            capacity of the Decimal context.
            '''))
            with decimal.localcontext() as ctx:
                ctx.prec = 30
                x = 100000*decimalmath.sin(decimalmath.pi()/4)
                print(f"  x = 100000*sin(pi/4) to 30 places = {x}")
                print(f"  sci    to 20 places = {f(x, 'sci', n=20)}")
                print(f"  eng    to 20 places = {f(x, 'eng', n=20)}")
                print(f"  engsi  to 20 places = {f(x, 'engsi', n=20)}")
                print(f"  engsic to 20 places = {f(x, 'engsic', n=20)}")
    if 1:   # Test code 
        def Init():
            'Make sure test environment is set up in a repeatable fashion'
            return Fmt(3)
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
            Assert(f(x, n=1) == "1.")
            Assert(f(x, n=2) == "1.0")
            Assert(f(x, n=3) == "1.00")
            Assert(f(x, n=4) == "1.000")
            Assert(f(x, n=5) == "1.0000")
            Assert(f(x, n=6) == "0.999999")
            Assert(f(x, n=7) == "0.9999990")
            raises(ValueError, f, -x, n=0)
            Assert(f(-x, n=1) == "-1.")
            Assert(f(-x, n=2) == "-1.0")
            Assert(f(-x, n=3) == "-1.00")
            Assert(f(-x, n=4) == "-1.000")
            Assert(f(-x, n=5) == "-1.0000")
            Assert(f(-x, n=6) == "-0.999999")
            Assert(f(-x, n=7) == "-0.9999990")
        def Test_Fix():
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
                n = int(1e6/len(s)) # How many before we reach a million digits
                x = D(s*n)
                f = Init()
                f.high = None
                t = f(x, fmt="fix")
                Assert(len(t) == n*len(s) + 1)
            for n in (999999,  # Largest exponent allowed by default Decimal context
                100, 20, 3):
                TestTiny(n)
                TestHuge(n)
                TestLotsOfDigits(n)
            TestBigInteger(100)
        def Test_Eng():
            '''Compare to fpformat's results.  Only go up to 15 digits because
            fpformat uses floats
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
        r = r"^Test_"
        exit(run(globals(), regexp=r, halt=1)[0])
    else:
        Demo()
