'''

The Fmt class will format any number/string accepted by Decimal's
constructor into a string with the desired number of significant
figures.  Run the module as a script to see example output.

Use 'from fmt import fmt' to get fmt as a convenience instance of Fmt.

'''

# Copyright (C) 2008, 2012, 2021 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

import decimal
import collections 
import locale 

D = decimal.Decimal
all = [
    "Fmt",  # The Fmt class
    "D",    # decimal.Decimal abbreviation
    "fmt"   # Convenience instance of Fmt
]

class Fmt(object):
    _SI_prefixes = { # Key is exponent/3
        -8: "y", -7: "z", -6: "a", -5: "f", -4: "p", -3: "n", -2: "μ",
        -1: "m", 0: "", 1: "k", 2: "M",  3: "G", 4: "T", 5: "P", 6: "E",
        7: "Z", 8: "Y"}  
    _superscripts = {
        "-": "⁻", "+": "⁺", "0": "⁰", "1": "¹", "2": "²",  "3": "³",
        "4": "⁴", "5": "⁵", "6": "⁶", "7": "⁷", "8": "⁸", "9": "⁹"}  
    def __init__(self, n=3, low=1e-5, high=1e16):
        '''n is the number of significant figures to format to.  
        low is the point below which scientific notation is used.
        high is the point above which scientific notation is used.
        low and high can be None, which disables them; if disabled, then
        fixed point interpolation is used by default.
        '''
        self.n = n
        self.u = False
        self.low = D(str(low))
        self.high = D(str(high))
        # Implementation:  a number to format is first converted to a
        # Decimal object DO, then DO is converted to a string with the
        # desired number of significant figures using python's string
        # interpolation f"{x:e}" with appropriate parameters.  This
        # returns a string of the form sD.DDeD, which can be picked
        # apart into the sign, significand, radix, and exponent.  These
        # are then manipulated into the string form desired.  We assume
        # python's string interpolation works for numbers with an
        # arbitrary number of digits.  I've tested it up to numbers with
        # nearly a million digits and it appears to work.
    # ----------------------------------------------------------------------
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
    # ----------------------------------------------------------------------
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
        assert(isinstance(x, D))
        # Get scientific notation form
        N = int(n) if n is not None else self._n
        if N < 1:
            raise ValueError("n must be > 0")
        xs = f"{abs(x):.{N - 1}e}"
        sign = "-" if x < 0 else ""
        significand, e = xs.split("e")
        # The following is because f"{Decimal(0):.1e}" returns '0.0e+1'
        exponent = int(e) if x else 0
        other, dp = "", self.dp
        if dp not in significand:
            if len(significand) != 1:
                raise ValueError("'{significand}' was expected to be 1 character")
            ld = significand
        else:
            ld, other = significand.split(dp)
        assert(len(ld) + len(other) == N)     # n figures is an invariant
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
        x = D(str(value))
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

fmt = Fmt()     # Convenience instance

if __name__ == "__main__": 
    from math import pi
    from textwrap import dedent
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
    '''[1:].rstrip()))
    print(f"  f(D('1e999999')) = {f(D('1e999999'))}")
    print(f"  f(D('1e-999999')) = {f(D('1e-999999'))}")
    exit()
    try:
        f(D("1e1000000"))
    except decimal.Overflow:
        print('f(D("1e1000000"))', "results in overflow")
    print(f(D("1e-100000000")), "underflow that gives 0")
