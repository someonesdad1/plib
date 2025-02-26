import sys
from fractions import Fraction
from lwtest import run, assert_equal, raises
from getnumber import GetNumber, ParseUnitString, GetWireDiameter
from getnumber import GetFraction
from format_numbers import FormatFraction
from uncertainties import ufloat_fromstr, UFloat
from pdb import set_trace as xx

if sys.version_info[0] == 3:
    import io

    sio = io.StringIO
else:
    from StringIO import StringIO as sio

err = sys.stderr


def TestExceptionalCases():
    "Check we get exceptions."
    # low > high
    raises(ValueError, GetNumber, "", low=1, high=0, instream=sio("0"))
    # Invert True without low or high
    raises(ValueError, GetNumber, "", invert=True, instream=sio("0"))


def TestAll():
    msg = "Error:  must have "
    # Note:  the test case comment is a picture of the allowed interval;
    # '(' and ')' mean open, '[' and ']' mean closed.
    #
    # [----...
    s_out = sio()
    GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("4"))
    assert s_out.getvalue() == msg + "number >= 5\n"
    s_out = sio()
    n = GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("5"))
    assert n == 5 and isinstance(n, int)
    s_out = sio()  # Test we can get a float like this too
    GetNumber("", numtype=float, low=5, outstream=s_out, instream=sio("4"))
    assert s_out.getvalue() == msg + "number >= 5\n"
    n = GetNumber("", numtype=float, low=5, outstream=sio(), instream=sio("5"))
    assert n == 5 and isinstance(n, float)
    # The remaining tests will be done implicitly with floats
    # (----...
    s_out = sio()
    GetNumber("", low=5, low_open=True, outstream=s_out, instream=sio("4"))
    assert s_out.getvalue() == msg + "number > 5\n"
    s_out = sio()
    n = GetNumber("", low=5, low_open=True, outstream=s_out, instream=sio("6"))
    assert n == 6 and isinstance(n, float)
    # ...----]
    s_out = sio()
    GetNumber("", high=5, outstream=s_out, instream=sio("6"))
    assert s_out.getvalue() == msg + "number <= 5\n"
    s_out = sio()
    n = GetNumber("", high=5, outstream=s_out, instream=sio("5"))
    assert n == 5 and isinstance(n, float)
    # ...----)
    s_out = sio()
    GetNumber("", high=5, high_open=True, outstream=s_out, instream=sio("5"))
    assert s_out.getvalue() == msg + "number < 5\n"
    s_out = sio()
    n = GetNumber("", high=5, high_open=True, outstream=s_out, instream=sio("4"))
    assert n == 4 and isinstance(n, float)
    # [----]
    s_out = sio()
    GetNumber("", low=2, high=5, outstream=s_out, instream=sio("6"))
    assert s_out.getvalue() == msg + "2 <= number <= 5\n"
    s_out = sio()
    GetNumber("", low=2, high=5, outstream=s_out, instream=sio("1"))
    assert s_out.getvalue() == msg + "2 <= number <= 5\n"
    # Also test at boundaries because this is probably the most important
    # case.
    s_out = sio()
    n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("5"))
    assert n == 5 and isinstance(n, float)
    s_out = sio()
    n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("2"))
    assert n == 2 and isinstance(n, float)
    # [----)
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, outstream=s_out, instream=sio("5"))
    assert s_out.getvalue() == msg + "2 <= number < 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        outstream=s_out,
        instream=sio("4.999999999999"),
    )
    assert n == 4.999999999999
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, outstream=s_out, instream=sio("1"))
    assert s_out.getvalue() == msg + "2 <= number < 5\n"
    # (----]
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, outstream=s_out, instream=sio("2"))
    assert s_out.getvalue() == msg + "2 < number <= 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        outstream=s_out,
        instream=sio("2.0000000000001"),
    )
    assert n == 2.0000000000001
    # (----)
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        outstream=s_out,
        instream=sio("5"),
    )
    assert s_out.getvalue() == msg + "2 < number < 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        outstream=s_out,
        instream=sio("4.999999999999"),
    )
    assert n == 4.999999999999
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        outstream=s_out,
        instream=sio("2"),
    )
    assert s_out.getvalue() == msg + "2 < number < 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        outstream=s_out,
        instream=sio("2.0000000000001"),
    )
    assert n == 2.0000000000001
    # ...---[  ]---...
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("2.0000000000001"),
    )
    assert s_out.getvalue() == msg + "number <= 2 or number >= 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("2"),
    )
    assert n == 2 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("5"),
    )
    assert n == 5 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("1"),
    )
    assert n == 1 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("6"),
    )
    assert n == 6 and isinstance(n, float)
    # ...---[  )---...
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("5"),
    )
    assert s_out.getvalue() == msg + "number <= 2 or number > 5\n"
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("4"),
    )
    assert s_out.getvalue() == msg + "number <= 2 or number > 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("2"),
    )
    assert n == 2 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        low_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("1"),
    )
    assert n == 1 and isinstance(n, float)
    # ...---(  ]---...
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("2"),
    )
    assert s_out.getvalue() == msg + "number < 2 or number >= 5\n"
    s_out = sio()
    GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("4"),
    )
    assert s_out.getvalue() == msg + "number < 2 or number >= 5\n"
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("1.999999"),
    )
    assert n == 1.999999 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("5"),
    )
    assert n == 5 and isinstance(n, float)
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        high_open=True,
        invert=True,
        outstream=s_out,
        instream=sio("6"),
    )
    assert n == 6 and isinstance(n, float)
    # ...---(  )---...
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out, instream=sio("2"))
    assert s_out.getvalue() == msg + "number < 2 or number > 5\n"
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out, instream=sio("5"))
    assert s_out.getvalue() == msg + "number < 2 or number > 5\n"
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out, instream=sio("3"))
    assert s_out.getvalue() == msg + "number < 2 or number > 5\n"
    s_out = sio()
    n = GetNumber("", low=2, high=5, invert=True, outstream=s_out, instream=sio("1"))
    assert n == 1 and isinstance(n, float)
    s_out = sio()
    n = GetNumber("", low=2, high=5, invert=True, outstream=s_out, instream=sio("6"))
    assert n == 6 and isinstance(n, float)
    # Show that we can evaluate things with a variables dictionary.
    from math import sin, pi

    v = {"sin": sin, "pi": pi}
    s_out = sio()
    n = GetNumber(
        "",
        low=2,
        high=5,
        invert=True,
        outstream=s_out,
        instream=sio("sin(pi/6)"),
        vars=v,
    )
    assert n == sin(pi / 6) and isinstance(n, float)


def Test_mpmath():
    """Import mpmath and use for testing if available.  Demonstrates that
    GetNumber works with ordered number types other than int and float.
    """
    try:
        import mpmath
    except ImportError:
        print("** mpmath not tested in getnumber_test.py", file=err)
    else:
        # [----
        n = GetNumber("", numtype=mpmath.mpf, low=2, outstream=sio(), instream=sio("4"))
        assert n == 4 and isinstance(n, mpmath.mpf)


def TestDefaultValue():
    """See that we get an exception when the default is not between low
    and high.
    """
    with raises(ValueError):
        GetNumber(
            "", low=2, high=5, invert=True, outstream=sio(), default=1, instream=sio("")
        )
    # Test default value with int
    default = 2
    num = GetNumber(
        "",
        low=2,
        high=5,
        invert=True,
        outstream=sio(),
        numtype=int,
        default=default,
        instream=sio(""),
    )
    assert num == default
    # Test default value with float
    default = 3.77
    num = GetNumber(
        "",
        low=2,
        high=5,
        invert=True,
        outstream=sio(),
        default=default,
        instream=sio(""),
    )
    assert num == default


def TestNumberWithUnit():
    "Show that we can return numbers with units"
    # 5 with no unit string
    n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5"), use_unit=True)
    assert n == (5, "") and isinstance(n[0], float)
    # 5 meters, cuddled
    n = GetNumber(
        "", low=0, high=10, outstream=sio(), instream=sio("5m"), use_unit=True
    )
    assert n == (5, "m") and isinstance(n[0], float)
    # 5 meters
    n = GetNumber(
        "", low=0, high=10, outstream=sio(), instream=sio("5 m"), use_unit=True
    )
    assert n == (5, "m") and isinstance(n[0], float)
    # millimeters, cuddled
    n = GetNumber(
        "",
        low=0,
        high=1e100,
        outstream=sio(),
        instream=sio("123.456e7mm"),
        use_unit=True,
    )
    assert n == (123.456e7, "mm") and isinstance(n[0], float)
    # millimeters
    n = GetNumber(
        "",
        low=0,
        high=1e100,
        outstream=sio(),
        instream=sio("123.456e7   mm"),
        use_unit=True,
    )
    assert n == (123.456e7, "mm") and isinstance(n[0], float)
    # millimeters, negative number
    n = GetNumber(
        "",
        low=-1e100,
        high=1e100,
        outstream=sio(),
        instream=sio("-123.456e7   mm"),
        use_unit=True,
    )
    assert n == (-123.456e7, "mm") and isinstance(n[0], float)
    # --------------------
    # Uncertainties
    # --------------------
    for t in ("8 mm", "8+-1 mm", "8+/-1 mm", "8(1) mm"):
        n = GetNumber(
            "",
            low=-1e100,
            high=1e100,
            outstream=sio(),
            instream=sio(t),
            use_unit=True,
            use_unc=True,
        )
        assert isinstance(n[0], UFloat)
        assert n[0].nominal_value == 8
        assert n[0].std_dev == 1
        assert n[1] == "mm"


def TestParseUnitString():
    allowed = ("kg", "m")
    v, u = ParseUnitString("kg", allowed)
    assert v == 1 and u == "kg"
    # 'kkg' is allowed by ParseUnitString, but is not allowed by formal SI
    # rules.
    v, u = ParseUnitString("kkg", allowed)
    assert v == 1000 and u == "kg"
    v, u = ParseUnitString("ym", allowed)
    assert v == 1e-24 and u == "m"
    # Allow for a default unit if strict is False
    v, u = ParseUnitString("xyz", allowed, strict=False)
    assert v == 1 and u == ""
    # Must have unit in the allowed container
    raises(ValueError, ParseUnitString, "kz", allowed, strict=True)


def TestInspect():
    """Test that 2 isn't in the first interval, but is in the second."""
    assert GetNumber("", low=0, high=1, inspect="2") == False
    assert GetNumber("", low=0, high=3, inspect="2") == True
    # If inspect is not a string, get exception
    raises(ValueError, GetNumber, "", inspect=1)


def TestGetFraction():
    e = Fraction(5, 4)
    for i in (
        "5/4",
        "+5/4",
        " -5/4",
        "1   1/4",
        "+1 1/4",
        "  -1 1/4",
        "1-1/4",
        "+1-1/4",
        "-1-1/4",
        "1+1/4",
        "+1+1/4",
        "-1+1/4",
    ):
        i = i.strip()
        neg = -1 if i[0] == "-" else 1
        assert GetFraction(i) == neg * e


def TestFormatFraction():
    f = Fraction(5, 4)
    s = FormatFraction(f)
    assert s == "1¹/₄"
    s = FormatFraction(f, improper=True)
    assert s == "⁵/₄"


if __name__ == "__main__":
    exit(run(globals())[0])
