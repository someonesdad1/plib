'''
String interpolation for numbers when mpmath is available
'''

import mpmath as M
from lwtest import run, Assert
ii = isinstance

if 1:   # Classes
    class Fmt:
        def __init__(self, n=3):
            self.n = n
            self.radix = "."
            # Attributes for complex numbers
            self.imag_unit = "i"
            self.cuddled = False
            self.polar = False
            self.deg = False
        def sigexp(self, x, n=None):
            '''Return (sign, significand, exponent) for x, which is an
            mpmath.mpf instance or an integer.  Both significand and
            exponent are integers.  sign is a string that is "-" or "".
            The implied radix is after the first digit of the significand.
            n is the number of significant digits in the significand and
            must be an integer > 0.  Note if x is inf or nan you'll get a
            ValueError exception.  Use self.n if n is None.
            '''
            if n is None:
                n = self.n
            assert(ii(x, (M.mpf, int)))
            assert(ii(n, int) and n > 0)
            sign = "-" if x < 0 else ""
            a = abs(x)
            e = int(M.floor(M.log10(a))) if x else 0
            s = M.nstr(a/10**e, n)
            s = s.replace(".", "").replace(",", "")     # Remove radix
            while len(s) < n:
                # Special case:  nstr() returns 1.0 for 1 whatever n is
                s += "0"
            assert(len(s) == n if x else 1)
            return sign, int(s), e
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
                s = f"{re}{u}{sgn}{u}{im}"
                return s
            elif ii(x, M.mpf): 
                sgn, m, e = self.sigexp(x)
                s = str(m)
                return f"{sgn}{s[0] + self.radix + s[1:]}e{e}"
            elif ii(x, int): 
                pass
            else:
                raise TypeError("x must be int, mpmath.mpf, or mpmath.mpc")

if __name__ == "__main__": 
    fmt = Fmt()
    fmt.n = 2
    def Test_complex():
        z = M.mpc(1, 2)
        s = fmt(z)
        Assert(s == "1.0e0+2.0e0")
    exit(run(globals(), halt=True)[0])
