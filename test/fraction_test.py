from fractions import Fraction
from lwtest import run, assert_equal, raises
from fraction import FormatFraction, FractionToUnicode
from fraction import FractionFromUnicode, ToFraction, _sub, _super
from pdb import set_trace as xx


def TestFunctions():
    for ip in range(0, 11):
        for d in range(2, 11):
            for n in range(1, d):
                # Test FormatFraction
                f = Fraction(n, d)
                s = FormatFraction(f)
                N = ""
                for i in str(f.numerator):
                    N += _super[int(i)]
                D = ""
                for i in str(f.denominator):
                    D += _sub[int(i)]
                t = N + "/" + D
                assert s == t
                u = FractionToUnicode(str(n) + "/" + str(d))
                assert s == u
                v = FractionFromUnicode(u)
                ff = str(f.numerator) + "/" + str(f.denominator)
                assert v == ff
                # Add integer part
                if ip:
                    s = FormatFraction(ip + f)
                    t = str(ip) + N + "/" + D
                    assert s == t
                    s = FractionToUnicode(str(ip) + "-" + ff)
                    assert s == t
                    w = FractionFromUnicode(t)
                    u = str(ip) + "-" + v
                    assert w == str(ip) + "-" + v


def TestToFraction():
    f = Fraction(19, 16)
    for s in ("19/16", "1 3/16", "1-3/16", "1+3/16"):
        assert ToFraction(s) == f
    for s in (
        "1  3/16",
        "1-+3/16",
        "1--3/16",
        "1++3/16",
        "1 3//16",
        "1 3/-16",
        "1 3/+16",
    ):
        raises(ValueError, ToFraction, s)


if __name__ == "__main__":
    exit(run(globals())[0])
