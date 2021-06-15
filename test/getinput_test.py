import sys
import os
from lwtest import run, raises, assert_equal
from getinput import *
from uncertainties import ufloat_fromstr, UFloat
from io import StringIO
from pdb import set_trace as xx 

err = sys.stderr
def sio(*s):
    'Allows StringIO to be used for input or output'
    if not s:
        return StringIO()
    return StringIO(s[0])
def TestGetNumberExceptionalCases():
    # low > high
    raises(ValueError, GetNumber, "", low=1, high=0, instream=sio("0"))
    # Invert True without low or high
    raises(ValueError, GetNumber, "", invert=True, instream=sio("0"))
def TestGetNumberAll():
    msg = "Error:  must have "
    # Note:  the test case comment is a picture of the allowed interval;
    # '(' and ')' mean open, '[' and ']' mean closed.
    #
    # [----...
    s_out = sio()
    GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("4"))
    assert(s_out.getvalue() == msg + "number >= 5\n")
    s_out = sio()
    n = GetNumber("", numtype=int, low=5, outstream=s_out, instream=sio("5"))
    assert(n == 5 and isinstance(n, int))
    s_out = sio()  # Test we can get a float like this too
    GetNumber("", numtype=float, low=5, outstream=s_out, instream=sio("4"))
    assert(s_out.getvalue() == msg + "number >= 5\n")
    n = GetNumber("", numtype=float, low=5, outstream=sio(), instream=sio("5"))
    assert(n == 5 and isinstance(n, float))
    # The remaining tests will be done implicitly with floats
    # (----...
    s_out = sio()
    GetNumber("", low=5, low_open=True, outstream=s_out,
           instream=sio("4"))
    assert(s_out.getvalue() == msg + "number > 5\n")
    s_out = sio()
    n = GetNumber("", low=5, low_open=True, outstream=s_out,
               instream=sio("6"))
    assert(n == 6 and isinstance(n, float))
    # ...----]
    s_out = sio()
    GetNumber("", high=5, outstream=s_out, instream=sio("6"))
    assert(s_out.getvalue() == msg + "number <= 5\n")
    s_out = sio()
    n = GetNumber("", high=5, outstream=s_out, instream=sio("5"))
    assert(n == 5 and isinstance(n, float))
    # ...----)
    s_out = sio()
    GetNumber("", high=5, high_open=True, outstream=s_out,
           instream=sio("5"))
    assert(s_out.getvalue() == msg + "number < 5\n")
    s_out = sio()
    n = GetNumber("", high=5, high_open=True, outstream=s_out,
               instream=sio("4"))
    assert(n == 4 and isinstance(n, float))
    # [----]
    s_out = sio()
    GetNumber("", low=2, high=5, outstream=s_out, instream=sio("6"))
    assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
    s_out = sio()
    GetNumber("", low=2, high=5, outstream=s_out, instream=sio("1"))
    assert(s_out.getvalue() == msg + "2 <= number <= 5\n")
    # Also test at boundaries because this is probably the most important
    # case.
    s_out = sio()
    n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("5"))
    assert(n == 5 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, outstream=s_out, instream=sio("2"))
    assert(n == 2 and isinstance(n, float))
    # [----)
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
           instream=sio("5"))
    assert(s_out.getvalue() == msg + "2 <= number < 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
               instream=sio("4.999999999999"))
    assert(n == 4.999999999999)
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, outstream=s_out,
           instream=sio("1"))
    assert(s_out.getvalue() == msg + "2 <= number < 5\n")
    # (----]
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
           instream=sio("2"))
    assert(s_out.getvalue() == msg + "2 < number <= 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, outstream=s_out,
               instream=sio("2.0000000000001"))
    assert(n == 2.0000000000001)
    # (----)
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, high_open=True,
           outstream=s_out, instream=sio("5"))
    assert(s_out.getvalue() == msg + "2 < number < 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
               outstream=s_out, instream=sio("4.999999999999"))
    assert(n == 4.999999999999 )
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, high_open=True,
           outstream=s_out, instream=sio("2"))
    assert(s_out.getvalue() == msg + "2 < number < 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True,
               outstream=s_out, instream=sio("2.0000000000001"))
    assert(n == 2.0000000000001)
    # ...---[  ]---...
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
           outstream=s_out, instream=sio("2.0000000000001"))
    assert(s_out.getvalue() == msg + "number <= 2 or number >= 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
           outstream=s_out, instream=sio("2"))
    assert(n == 2 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
           outstream=s_out, instream=sio("5"))
    assert(n == 5 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
               outstream=s_out, instream=sio("1"))
    assert(n == 1 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, high_open=True, invert=True,
               outstream=s_out, instream=sio("6"))
    assert(n == 6 and isinstance(n, float))
    # ...---[  )---...
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, invert=True,
           outstream=s_out, instream=sio("5"))
    assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
    s_out = sio()
    GetNumber("", low=2, high=5, low_open=True, invert=True,
           outstream=s_out, instream=sio("4"))
    assert(s_out.getvalue() == msg + "number <= 2 or number > 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, invert=True,
           outstream=s_out, instream=sio("2"))
    assert(n == 2 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, low_open=True, invert=True,
           outstream=s_out, instream=sio("1"))
    assert(n == 1 and isinstance(n, float))
    # ...---(  ]---...
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, invert=True,
           outstream=s_out, instream=sio("2"))
    assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
    s_out = sio()
    GetNumber("", low=2, high=5, high_open=True, invert=True,
           outstream=s_out, instream=sio("4"))
    assert(s_out.getvalue() == msg + "number < 2 or number >= 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, high_open=True, invert=True,
           outstream=s_out, instream=sio("1.999999"))
    assert(n == 1.999999 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, high_open=True, invert=True,
           outstream=s_out, instream=sio("5"))
    assert(n == 5 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, high_open=True, invert=True,
           outstream=s_out, instream=sio("6"))
    assert(n == 6 and isinstance(n, float))
    # ...---(  )---...
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("2"))
    assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("5"))
    assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
    s_out = sio()
    GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("3"))
    assert(s_out.getvalue() == msg + "number < 2 or number > 5\n")
    s_out = sio()
    n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("1"))
    assert(n == 1 and isinstance(n, float))
    s_out = sio()
    n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("6"))
    assert(n == 6 and isinstance(n, float))
    # Show that we can evaluate things with a variables dictionary.
    from math import sin, pi
    v = {"sin":sin, "pi":pi}
    s_out = sio()
    n = GetNumber("", low=2, high=5, invert=True, outstream=s_out,
           instream=sio("sin(pi/6)"), vars=v)
    assert(n == sin(pi/6) and isinstance(n, float))
def TestGetNumber_mpmath():
    # Import mpmath and use for testing if available.
    # Demonstrates that GetNumber works with ordered number types
    # other than int and float.
    try:
        import mpmath
    except ImportError:
        print("** mpmath not tested in getnumber_test.py", file=err)
    else:
        # [----
        n = GetNumber("", numtype=mpmath.mpf, low=2, outstream=sio(),
                   instream=sio("4"))
        assert(n == 4 and isinstance(n, mpmath.mpf))
def TestGetNumberDefaultValue():
    # See that we get an exception when the default is not between low and
    # high.
    with raises(ValueError):
        GetNumber("", low=2, high=5, invert=True, outstream=sio(), default=1,
               instream=sio(""))
    # Test default value with int
    default = 2
    num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                 numtype=int, default=default, instream=sio(""))
    assert(num == default)
    # Test default value with float
    default = 3.77
    num = GetNumber("", low=2, high=5, invert=True, outstream=sio(),
                 default=default, instream=sio(""))
    assert(num == default)
def TestGetNumberNumberWithUnit():
    # Show that we can return numbers with units
    # 5 with no unit string
    n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5"),
        use_unit=True)
    assert(n == (5, "") and isinstance(n[0], float))
    # 5 meters, cuddled
    n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5m"),
        use_unit=True)
    assert(n == (5, "m") and isinstance(n[0], float))
    # 5 meters
    n = GetNumber("", low=0, high=10, outstream=sio(), instream=sio("5 m"),
        use_unit=True)
    assert(n == (5, "m") and isinstance(n[0], float))
    # millimeters, cuddled
    n = GetNumber("", low=0, high=1e100, outstream=sio(),
        instream=sio("123.456e7mm"), use_unit=True)
    assert(n == (123.456e7, "mm") and isinstance(n[0], float))
    # millimeters
    n = GetNumber("", low=0, high=1e100, outstream=sio(),
        instream=sio("123.456e7   mm"), use_unit=True)
    assert(n == (123.456e7, "mm") and isinstance(n[0], float))
    # millimeters, negative number
    n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
        instream=sio("-123.456e7   mm"), use_unit=True)
    assert(n == (-123.456e7, "mm") and isinstance(n[0], float))
    #--------------------
    # Uncertainties
    #--------------------
    for t in ("8 mm", "8+-1 mm", "8+/-1 mm", "8(1) mm"):
        n = GetNumber("", low=-1e100, high=1e100, outstream=sio(),
            instream=sio(t), use_unit=True, use_unc=True)
        assert(isinstance(n[0], UFloat))
        assert(n[0].nominal_value == 8)
        assert(n[0].std_dev == 1)
        assert(n[1] == "mm")
def TestGetNumberInspect():
    # Test that 2 isn't in the first interval, but is in the second.
    assert(GetNumber("", low=0, high=1, inspect="2") == False)
    assert(GetNumber("", low=0, high=3, inspect="2") == True)
    # If inspect is not a string, get exception
    raises(ValueError, GetNumber, "", inspect=1)

def TestParseUnitString():
    allowed = ("kg", "m")
    v, u = ParseUnitString("kg", allowed)
    assert(v == 1 and u == "kg")
    # 'kkg' is allowed by ParseUnitString, but is not allowed by formal SI
    # rules.
    v, u = ParseUnitString("kkg", allowed)
    assert(v == 1000 and u == "kg")
    v, u = ParseUnitString("ym", allowed)
    assert(v == 1e-24 and u == "m")
    # Allow for a default unit if strict is False
    v, u = ParseUnitString("xyz", allowed, strict=False)
    assert(v == 1 and u == "")
    # Must have unit in the allowed container
    raises(ValueError, ParseUnitString, "kz", allowed,
                      strict=True)
def TestGetWireDiameter():
    GetWireDiameter.input = sio("12 ga")
    awg, d_mm = GetWireDiameter()
    assert(awg == "12 ga")
    assert_equal(d_mm, 2.05232)
    # Same, but in inches
    GetWireDiameter.input = sio("12 ga")
    awg, d_in = GetWireDiameter(default_unit="in")
    assert(awg == "12 ga")
    assert_equal(d_in, 0.0808)
    # Large diameter
    GetWireDiameter.input = sio("12 ly")
    awg, d_ly = GetWireDiameter(default_unit="ly")
    assert(awg == "12 ly")
    assert_equal(d_ly, 12)
    # Test at boundaries
    GetWireDiameter.input = sio("-3 ga")
    s, d = GetWireDiameter()
    assert_equal(d, 11.684)
    GetWireDiameter.input = sio("56 ga")
    s, d = GetWireDiameter()
    assert_equal(d, 0.012446, reltol=1e-5)
    # Note we can't test outside of proper bounds with a StringIO stream
    # because an infinite loop will occur.
    GetWireDiameter.input = None
#----------------------------------------------------------------------
# GetLines tests
def TestGetLines():
    file = "test_GetLines"
    try:
        open(file, "w").write("one\ntwo three\nfour\n")
        lines = list(GetLines(file))
        assert(lines == ["one\n", "two three\n", "four\n"])
        # ignore kw:  Ignore lines that contain 'four'
        ignore = lambda line:  True if "four" in line else False
        lines = list(GetLines(file, ignore=ignore))
        assert(lines == ["one\n", "two three\n"])
        # xfm kw:  Transform to uppercase
        lines = list(GetLines(file, xfm=str.upper))
        assert(lines == ["ONE\n", "TWO THREE\n", "FOUR\n"])
        # nonl kw:  Remove the newline
        lines = list(GetLines(file, nonl=True))
        assert(lines == ["one", "two three", "four"])
    finally:
        try:
            os.remove(file)
        except Exception:
            pass
#----------------------------------------------------------------------
# GetTokens tests
def TestGetTokens():
    file = "test_GetTokens"
    try:
        open(file, "w").write("one\ntwo three\nfour\n")
        # Canonical usage
        gt = GetTokens(file)
        for got in "one two three four".split():
            assert(next(gt) == got) 
        raises(StopIteration, next, gt)
        # Transform tokens to uppercase with convert
        fp = open(file)
        gt = GetTokens(fp, convert=str.upper)
        for got in "ONE TWO THREE FOUR".split():
            assert(next(gt) == got) 
        fp.close()
        # Transform line to uppercase with fltr
        fp = open(file)
        gt = GetTokens(fp, fltr=str.upper)
        for got in "ONE TWO THREE FOUR".split():
            assert(next(gt) == got) 
        fp.close()
        # Transform line to uppercase and append "x" to token (use both convert and
        # fltr)
        fp = open(file)
        gt = GetTokens(fp, fltr=str.upper, convert=lambda x: x + "x")
        for got in "ONEx TWOx THREEx FOURx".split():
            assert(next(gt) == got) 
        fp.close()
        # Works with file and stream simultaneously
        open(file, "w").write("one\ntwo three\n")
        stream = sio("four\n")
        gt = GetTokens(file, stream)
        for got in "one two three four".split():
            assert(next(gt) == got) 
        fp.close()
        # Reverse file & stream changes order
        stream = sio("four\n")
        gt = GetTokens(stream, file)
        for got in "four one two three".split():
            assert(next(gt) == got) 
        fp.close()
    finally:
        try:
            os.remove(file)
        except Exception:
            pass
def TestChoice():
    try:
        instream, outstream = sio("2"), sio()
        Choice.test = True
        Choice.instream = instream
        Choice.outstream = outstream
        num, item = Choice(["a", "b", "c"])
        assert(num == 1)
        assert(item == "b")
    finally:
        del Choice.instream, Choice.outstream
        Choice.test = False
def TestTokenizeString():
    x = '''
        and as 
        or other
    '''
    y = '''
        and furthermore
    '''
    s = list(TokenizeString(x, y, linesep=" ", sep="\n"))
    assert(s == ["and", "as", "or", "other", "and", "furthermore"])
    # Filter fourth token and beyond
    def F(token):
        F.n += 1
        return token.upper() if F.n >= 4 else token
    F.n = 0
    s = list(TokenizeString(x, y, linesep=" ", sep="\n", token_filter=[F]))
    assert(s == ["and", "as", "or", "OTHER", "AND", "FURTHERMORE"])
    # No arguments
    assert(list(TokenizeString()) == [])
    # Simple string
    assert(list(TokenizeString("a;b", sep=";")) == ["a", "b"])
    # Show function composition works
    if have_toolz:
        assert(list(TokenizeString("a;b", sep=";", token_filter=[str.lower,
                                   str.upper])) == ["a", "b"])
        assert(list(TokenizeString("A;B", sep=";", token_filter=[str.lower,
                                   str.upper])) == ["a", "b"])
if __name__ == "__main__":
    exit(run(globals())[0])
