from collections import deque
from decimal import localcontext
from fmt import Fmt, D
from fpformat import FPFormat
from lwtest import run, raises, assert_equal
from math import pi as p
from pdb import set_trace as xx
from sys import argv

def Assert(x):  # Because the assert statement can't be overridden
    'Drop into debugger if script has an argument'
    if len(argv) > 1 and not x:
        xx()
    else:
        assert(x)

def Init():
    'Make sure test environment is set up in a repeatable fashion'
    return Fmt(3)

def TestBasics():
    f = Init()
    s = f(p)
    for x, result in (
        (p, "3.14"),
        (-p, "-3.14"),
        (p*1e99, "3.14e99"),
        (-p*1e99, "-3.14e99"),
        (p*1e-99, "3.14e-99"),
        (-p*1e-99, "-3.14e-99"),
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

def TestFix():
    def TestHuge(n, digits=3):
        f = Init()
        f.n = digits
        x = D(str(p) + f"e{n}")
        f.high = None
        s = f(x, fmt="fix")
        Assert(s[:3] == "314")
        Assert(s[-1] == ".")
        Assert(s[3:-1] == "0"*(len(s) - 4))
    def TestTiny(n, digits=3):
        f = Init()
        f.n = digits
        x = D(str(p) + f"e-{n}")
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

def TestEng():
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

def TestSci():
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

if __name__ == "__main__":
    run(globals(), halt=1, verbose=0)
