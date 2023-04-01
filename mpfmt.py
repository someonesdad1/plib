'''
String interpolation for numbers when mpmath is available
'''

from lwtest import run, Assert
from collections import namedtuple, deque
import decimal
import fractions
from functools import partial
try:
    import mpmath
    have_mpmath = True
except ImportError:
    have_mpmath = False
ii = isinstance

# Namedtuple to hold the components of a real number that has been taken
# apart after being approximated by M.nstr().  The components are strings
# except for exp, which is an int.
#   sign is "-" or ""
#   ld is the leading digit
#   dp is the radix (decimal point character)
#   other is all digits except the leading one
#   exp is the power of 10 exponent
Apart = namedtuple("Apart", "sign ld dp other exp")

if 1:   # Classes
    class Fmt:
        def __init__(self, n=3):
            self.n = n          # Number of significant digits
            self.radix = "."    # Decimal point
            self.rtz = False    # Remove trailing zeros
            self.rtdp = False   # Remove trailing decimal point
            self.rlz = False    # Remove leading zero
            self.low = -4       # Below this exponent use sci
            self.high = 6       # Above this exponent use sci
            # Attributes for complex numbers
            self.imag_unit = "i"
            self.cuddled = ""
            self.polar = False
            self.deg = False
        def fix(self, apart):
            'Return the fixed decimal point form'
            sign, ld, dp, other, e = apart
            if e < 0:
                return "0" + dp + abs(e + 1)*"0" + ld + other
            else:
                dq, ne = deque(ld + other), e + 1
                while len(dq) < ne:
                    dq.append("0")
                dq.insert(ne, dp)
                return ''.join(dq)
        def __call__(self, x, fmt="fix", n=None) -> str:
            '''Return x as a formatted string.  fmt is the format to use:
                "fix" = fixed
                "sci" = scientific
                "eng" = engineering
                "engsi" = engineering with an SI prefix appended
                "engsic" = "engsi" with the prefix cuddled
            '''
            if ii(x, M.mpc): 
                r, i = x.real, x.imag
                assert(ii(r, M.mpf) and ii(i, M.mpf))
                sgn = "-" if i < 0 else "+"
                re = self(r, fmt=fmt, n=n)
                im = self(abs(i), fmt=fmt, n=n)
                u = " " if self.cuddled else ""
                s = f"{re}{u}{sgn}{u}{im}{self.imag_unit}"
                return s
            elif ii(x, (M.mpf, int)): 
                sgn, m, e = self.sigexp(x)
                s = str(m)
                u = sgn + s[0] + self.radix + s[1:]
                if fmt == "fix":
                    return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
                elif fmt == "sci":
                    return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
                elif fmt == "eng":
                    # xx Need to adjust exponent
                    return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
                elif fmt == "engsi":
                    return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
                elif fmt == "engsic":
                    return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
            elif ii(x, int): 
                pass
            else:
                raise TypeError("x must be int, mpmath.mpf, or mpmath.mpc")
if 1:   # Core methods
    def TakeApart(x, n=3):
        '''Return an Apart namedtuple for x, which is an instance
        representing a real number.  Allowed types for x are int,
        float, python Decimal, python Fraction, and mpmath.mpf.
        The number will be rounded to n digits.
 
        This is a fundamental routine for doing string interpolation on
        integers or floating point numbers.
 
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
            assert("." in s)    # mpmath seems to use only "."
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

def TestTakeApart():
    D = decimal.Decimal
    F = fractions.Fraction
    mpf = mpmath.mpf if have_mpmath else float
    if 1:   # Show supported types get the same string interpolation
        # Function to convert an Apart to a string
        g = lambda x: ''.join(x[:4]) + f"e{x[4]}"
        k, u = 5, "1.23456"
        for n in range(1, 10):
            TA = partial(TakeApart, n=n)
            for i in (-1, 0, 1, 2, 1234, -1234):
                expected = TA(i)
                for x in (float(i), mpf(i), D(i), F(i)):
                    Assert(TA(x) == expected)
                    Assert(g(TA(x)) == g(expected))
            # Large negative float
            expected, s = TA(int(-123456)*10**(300 - k)), f"-{u}e300"
            for typ in (float, mpf, D, F):
                y = TA(typ(s))
                Assert(y == expected)
                Assert(g(y) == g(expected))
            # Large positive float
            expected, s = TA(int(123456)*10**(300 - k)), f"{u}e300"
            for typ in (float, mpf, D, F):
                y = TA(typ(s))
                Assert(y == expected)
                Assert(g(y) == g(expected))
            # Small negative float
            expected, s = TA(int(-123456)/10**(300 + k)), f"-{u}e-300"
            for typ in (float, mpf, D, F):
                y = TA(typ(s))
                Assert(y == expected)
                Assert(g(y) == g(expected))
            # Small positive float
            expected, s = TA(int(123456)/10**(300 + k)), f"{u}e-300"
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

TestTakeApart()
exit()

if __name__ == "__main__": 
    fmt = Fmt()
    print(fmt.TakeApart(-39578574))
    print(fmt.TakeApart(1/mpmath.fac(100)))
    exit()

    for i in range(-10, 11):
        x = mpmath.mpf(f"4.56e{i}")
        a = fmt.TakeApart(x)
        print(fmt.fix(a), i)
    exit()

    fmt = Fmt()
    fmt.n = 2
    fmt.radix = "."
    fmt.imag_unit = "i"
    fmt.cuddled = ""
    fmt.polar = False
    fmt.deg = False
    def Test_complex():
        z = mpmath.mpc(1.2, -3.4)
        s = fmt(z)
        Assert(s == "1.2e0-3.4e0i")
        fmt.cuddled = " "
        s = fmt(z)
        Assert(s == "1.2e0 - 3.4e0i")
    exit(run(globals(), halt=True)[0])
