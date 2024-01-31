'''
Provides the function PP which returns a form of the pprint.pprint function
with a width argument set to the desired width.  Also includes the utility 
Clear() which will clear the screen on UNIX type systems.
'''
if 1:  # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # <programming> Provides pp, a pprint aware of the screen width
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        import os
        import subprocess
        import sys
        from functools import partial
        from fractions import Fraction
        from decimal import Decimal
        from pprint import pprint
    # Custom imports
        have_mpmath = False
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            pass
    # Global variables 
        __all__ = ["Clear", "PP"]
        ii = isinstance
def Int(s):
    'Convert s into a positive integer'
    n = int(os.environ.get("COLUMNS", 80)) - 1
    if ii(s, str):
        if s.startswith("0x"):
            n = int(s, 16)
        elif s.startswith("0o"):
            n = int(s, 8)
        elif s.startswith("0b"):
            n = int(s, 2)
        elif "." in s or "e" in s:
            n = int(float(s))
        else:
            n = int(s)
    elif ii(s, int):
        n = s
    elif ii(s, (float, Decimal, Fraction)):
        n = int(s)
    elif have_mpmath and ii(s, mpmath.mpf):
        n = int(s)
    else:
        print(f"{__file__}:Int(s):  unrecognized type of argument", file=sys.stderr)
    n = abs(n)
    if n <= 0:
        raise ValueError("Integer value of s must be > 0")
    return n
def PP(width=None):
    '''Returns pprint.pprint with a width parameter set to one less than
    the current screen width if the parameter width is None.  Otherwise,
    it's a number converted to a positive integer that must be nonzero.
    '''
    columns = int(os.environ.get("COLUMNS", 80)) - 1
    if width is not None:
        try:
            columns = int(abs(width))
            if not columns:
                raise ValueError("PP():  width parameter must not be zero")
        except Exception as e:
            print(e)
            exit(1)
    return partial(pprint, width=columns)
def Clear():
    subprocess.run("clear", shell=True)

if __name__ == "__main__": 
    from lwtest import run, Assert, raises
    from io import StringIO
    from f import flt
    def TestInt():
        # Integer forms
        Assert(Int(1) == 1)
        Assert(Int(0o1) == 1)
        Assert(Int(0x1) == 1)
        Assert(Int(0b1) == 1)
        Assert(Int("1") == 1)
        Assert(Int("01") == 1)
        Assert(Int("0x1") == 1)
        # Float
        Assert(Int("1e2") == 100)
        Assert(Int("1.2") == 1)
        Assert(Int(flt("1.2")) == 1)
        # Decimal
        Assert(Int(Decimal("1.2")) == 1)
        # Fraction
        Assert(Fraction(1, 1) == 1)
        # mpmath.mpf
        if have_mpmath:
            Assert(Int(mpmath.mpf("1")) == 1)
            Assert(Int(mpmath.mpf("1.2")) == 1)
            Assert(Int(mpmath.mpf("1e2")) == 100)
    def Test_pp():
        pp = PP(5)
        buf = StringIO()
        s = "1234567890"
        pp(s, stream=buf)
        u = buf.getvalue()
        assert(u == f"{s!r}\n")

    exit(run(globals(), halt=True)[0])
