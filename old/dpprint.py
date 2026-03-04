'''
Provides the function PP which returns a form of the pprint.pprint function
with a width argument set to the desired width.  Also includes the utility
Clear() which will clear the screen on UNIX type systems.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Provides screenwidth-aware form of pprint.pprint function oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2024 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:   # Standard imports
        import os
        import subprocess
        import sys
        from functools import partial
        from fractions import Fraction
        from decimal import Decimal
        from pprint import pprint
    if 1:   # Custom imports
        have_mpmath = False
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            pass
    if 1:   # Global variables
        __all__ = ["Clear", "PP"]
if 1:   # Core functionality
    def Int(s):
        "Convert s into a positive integer"
        n = int(os.environ.get("COLUMNS", 80)) - 1
        if isinstance(s, str):
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
        elif isinstance(s, int):
            n = s
        elif isinstance(s, (float, Decimal, Fraction)):
            n = int(s)
        elif have_mpmath and isinstance(s, mpmath.mpf):
            n = int(s)
        else:
            print(f"{__file__}:Int(s):  unrecognized type of argument", file=sys.stderr)
        n = abs(n)
        if n <= 0:
            raise ValueError("Integer value of s must be > 0")
        return n
    def PP(width=None, compact=False):
        '''Returns pprint.pprint with a width parameter set to one less than
        the current screen width if the parameter width is None.  Otherwise,
        it's a number converted to a positive integer that must be nonzero.
        If compact is True, multiple items will be printed on one line.
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
        return partial(pprint, width=columns, compact=compact)
    def Clear():
        subprocess.run("clear", shell=True)

if __name__ == "__main__":
    from lwtest import run, Assert
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
        assert u == f"{s!r}\n"
    exit(run(globals(), halt=True)[0])
