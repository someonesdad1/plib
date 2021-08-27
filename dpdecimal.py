'''
Todo:

    * If x is a dpDecimal, then -x returns a Decimal.  Need to have all 
      such operations defined so that a dpDecimal is returned.
    * Similarly, all math operations need to be defined to allow infection
      to occur.

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
    # <math> Provides a dpDecimal object that is derived from
    # decimal.Decimal but has custom string interpolation.
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import decimal
    import locale
    from collections import deque
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    ii = isinstance
class dpDecimal(decimal.Decimal):
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
        if self > dpDecimal._high or self < dpDecimal._low:
            return self.sci(dpDecimal._digits)
        return self.fix(dpDecimal._digits)
    def __neg__(self):
        return dpDecimal(-decimal.Decimal(self))
    def fix(self, n):
        'Return fixed-point form of x with n significant figures'
        dp = locale.localeconv()["decimal_point"]
        sign = "-" if self < 0 else ""
        # Get significand and exponent
        t = f"{abs(self):.{n - 1}{dpDecimal._e}}"
        s, e = t.split(dpDecimal._e)
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
        t = f"{abs(self):.{n - 1}{dpDecimal._e}}"
        s, e = t.split(dpDecimal._e)
        s.replace(".", dp)
        exponent = int(e)
        if not self:
            return s
        if not exponent:
            return sign + s
        # Generate the scientific notation representation
        return sign + s + dpDecimal._e + str(exponent)

if 0:
    a = dpDecimal(1.23)
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
    D = dpDecimal
    def Test_fix():
        d = D("1.23456789")
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
        d = D("1.23456789e33")
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
        d = D("1.23456789e-33")
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
    mp.mp.dps = getcontext().prec
    eps = 10*D(10)**(-D(getcontext().prec))
    exit(run(globals())[0])
