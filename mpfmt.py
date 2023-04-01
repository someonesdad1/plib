'''
String interpolation for numbers when mpmath is available
'''

import mpmath as M
from lwtest import run, Assert
from collections import namedtuple, deque
ii = isinstance
Apart = namedtuple("Apart", "sign leaddigit dp otherdigits exp")

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
        def TakeApart(self, x, n=None):
            '''Return an Apart namedtuple for x, which is an mpmath.mpf
            instance or an integer; all components are strings except exp
            is an integer.  If x is inf or nan you'll get a ValueError
            exception.  Use self.n if n is None.
            '''
            if n is None:
                n = self.n
            assert(ii(x, (M.mpf, int)))
            assert(ii(n, int) and n > 0)
            sign = "-" if x < 0 else ""
            a = abs(x)
            e = int(M.floor(M.log10(a))) if x else 0
            s = M.nstr(a/10**e, n)
            dp = s[1]
            s = s.replace(".", "").replace(",", "")     # Remove radix
            while len(s) < n:
                # Special case:  nstr() returns 1.0 for 1 whatever n is
                s += "0"
            assert(len(s) == n if x else 1)
            leaddigit = s[0]
            otherdigits = s[1:]
            return Apart(sign, leaddigit, dp, otherdigits, e)
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

if __name__ == "__main__": 
    fmt = Fmt()
    for i in range(-10, 11):
        x = M.mpf(f"4.56e{i}")
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
        z = M.mpc(1.2, -3.4)
        s = fmt(z)
        Assert(s == "1.2e0-3.4e0i")
        fmt.cuddled = " "
        s = fmt(z)
        Assert(s == "1.2e0 - 3.4e0i")
    exit(run(globals(), halt=True)[0])
