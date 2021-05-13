import os
from lwtest import run, raises
from get import GetText, GetLines, GetNumberedLines, GetWords, GetBinary
from get import GetNumbers, _have_unc, _have_f, Fraction
from io import StringIO
from pdb import set_trace as xx 
if _have_f:
    from get import flt, cpx

S = "Some\ntext\n"
text_file = "get.a"
open(text_file, "w").write(S)
ii = isinstance

def Assert(cond):
    '''Same as assert, but you'll be dropped into the debugger on an
    exception if you include a command line argument.
    '''
    if not cond:
        if len(sys.argv) > 1:
            print("Assert error:  entering debugger")
            xx()
        else:
            raise AssertionError

def TestGetText():
    sio = StringIO(S)
    t = GetText(sio)
    Assert(t == S)
    t = GetText(S)
    Assert(t == S)
    t = GetText(text_file)
    Assert(t == S)
    # Test with bytes
    b = b"Some\ntext\n"
    t = GetText(b)
    Assert(t == S)
    t = GetText(b, enc="ISO-8859-1")
    Assert(t == S)
    t = GetText(b"\xb5", enc="ISO-8859-1")
    Assert(t == "µ")
    # Test with regexp
    s = """# Comment
    ## Another comment
Line 1
    Line 2
    """
    r = ("^ *##", "^ *#")
    lines, meta = GetLines(s, regex=r)
    Assert(lines == ['Line 1', '    Line 2', '    '])
    Assert(meta[r[0]] == ['    ## Another comment'])
    Assert(meta[r[1]] == ['# Comment'])

def TestGetLines():
    sio = StringIO(S)
    l = S.split() + [""]
    t = GetLines(sio)
    Assert(t == l)
    t = GetLines(S)
    Assert(t == l)
    t = GetLines(text_file)
    Assert(t == l)

def TestGetWords():
    sio = StringIO(S)
    l = S.split()
    t = GetWords(sio)
    Assert(t == l)
    t = GetWords(S)
    Assert(t == l)
    t = GetWords(text_file)
    Assert(t == l)

def TestGetBinary():
    enc = "iso-8859-1"
    open(text_file, "wb").write(S.encode(enc))
    t = GetBinary(text_file)
    Assert(t == S.encode("ascii"))

def TestGetNumberedLines():
    expected = ((1, "Some"), (2, "text"), (3, ""))
    sio = StringIO(S)
    t = GetNumberedLines(sio)
    Assert(t == expected)
    t = GetNumberedLines(S)
    Assert(t == expected)
    t = GetNumberedLines(text_file)
    Assert(t == expected)

def TestGetNumbers():
    # Check general python numerical types
    s = "1 1.2 3/4 3+1j"
    l = GetNumbers(s)
    Assert(l == [1, 1.2, Fraction(3, 4), (3+1j)])
    # Check f.py types flt and cpx
    if _have_f:
        s = "1.2 3+1j"
        x, z = GetNumbers(s)
        Assert(ii(x, flt) and ii(z, cpx))
    # Check uncertainties library forms
    if _have_unc:
        s = "3±4 3+-4 3+/-4 3(4)"
        for u in GetNumbers(s):
            Assert(u.nominal_value == 3)
            Assert(u.std_dev == 4)
    # Test with a single type
    s = "1 1.2"
    l = GetNumbers(s, numtype=float)
    Assert(l == [1.0, 1.2])
    Assert(all([isinstance(i, float) for i in l]))
    s = "1 1.2 3+4j"
    l = GetNumbers(s, numtype=complex)
    Assert(l == [1+0j, 1.2+0j, 3+4j])

if __name__ == "__main__":
    exit(run(globals(), halt=True)[0])
