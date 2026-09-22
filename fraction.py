'''

FormatFraction
  Return the string form of a fraction using Unicode subscript and superscript
  characters.  Example:  Fraction(3, 16) returns '³/₁₆'.
  
FractionToUnicode
    Convert e.g. '3/16' will become '³/₁₆'.
    
FractionFromUnicode
    Convert e.g. '³/₁₆' will become '3/16'.
    
ToFraction
  Convert a string to a Fraction.  '19/16', '1 3/16', '1-3/16', and
  '1+3/16' all give the same fraction.
'''
##∞test∞# testdir #∞test∞#
if 1:   # Header
    _pgminfo = '''
        <oo gist ∞ Format fractions as Unicode oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2022 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 
        
            - ∞∞2 Move to fmt.py
        
        oo>
    '''
    if 1:   # Standard imports
        import re
        from fractions import Fraction
    if 1:   # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        _super, _sub = "⁰¹²³⁴⁵⁶⁷⁸⁹", "₀₁₂₃₄₅₆₇₈₉"
if 1:   # Core functionality
    def FormatFraction(f, improper=False, unicode=True):
        '''Return the string form of a fraction using Unicode subscript and
        superscript characters.  If improper is True, return an improper
        fraction.  If unicode is False, then return strings like '1-5/16'.
        '''
        if not isinstance(f, Fraction):
            raise TypeError("f must be a Fraction")
        s, n, d = "", f.numerator, f.denominator
        if unicode:
            if improper:
                rem = n  # rem is remainder
            else:
                ip, rem = divmod(n, d)
                if ip:
                    s += str(ip)
            if rem:
                for i in str(rem):
                    s += _super[int(i)]
                s += "/"
                for i in str(d):
                    s += _sub[int(i)]
            return s
        else:
            if improper or n < d:
                return f"{n}/{d}"
            else:
                ip, rem = divmod(n, d)
                if rem:
                    return f"{ip}-{rem}/{d}"
                else:
                    return f"{ip}"
    def FractionToUnicode(s):
        '''In the string s, convert 'a/b' expressions to the Unicode form
        where a and b are strings of ASCII digits.
        
        Example:  '3/16' will become '³/₁₆'.
        '''
        # Mixed fractions
        r = re.compile(r"(\d+[ +-])+(\d+)/(\d+)")
        mo = r.search(s)
        t = s
        if mo:
            g = mo.groups()
            assert len(g) == 3
            # Change denominator
            u = []
            for i in g[2]:
                u.append(_sub[int(i)])
            a, b = mo.span(3)
            t = t[:a] + "".join(u) + t[b:]
            # Change numerator
            u = []
            for i in g[1]:
                u.append(_super[int(i)])
            a, b = mo.span(2)
            t = t[:a] + "".join(u) + t[b:]
            # Change integer part
            ip = g[0]
            assert len(ip) > 1
            a, b = mo.span(1)
            t = t[:a] + str(int(ip[:-1])) + t[b:]
            return t
        # Regular fractions with no integer part
        r = re.compile(r"(\d+)/(\d+)")
        mo = r.search(s)
        if mo:
            g = mo.groups()
            return FormatFraction(Fraction(int(g[0]), int(g[1])))
    def FractionFromUnicode(s, sep="-"):
        '''In the string s, convert 'Ia/b' expressions where a and b are
        Unicode strings (superscripts for a and subscripts for b) to the
        usual form using ASCII digits.  I is an optional ASCII string of
        digits for the integer part.  sep is the character to separate the
        integer part and the fractional part.
        
        Example:  '1³/₁₆' will become '1-3/16'.
        '''
        sup = {"⁰": 0, "¹": 1, "²": 2, "³": 3, "⁴": 4, "⁵": 5, "⁶": 6, "⁷": 7, "⁸": 8, "⁹": 9}
        sub = {"₀": 0, "₁": 1, "₂": 2, "₃": 3, "₄": 4, "₅": 5, "₆": 6, "₇": 7, "₈": 8, "₉": 9}
        # Mixed fractions
        t = r"(\d+)([" + "".join(_super) + "]+)/([" + "".join(_sub) + "]+)"
        r = re.compile(t)
        mo = r.search(s)
        if mo:
            g = mo.groups()
            assert len(g) == 3
            t = g[0] + sep
            for i in g[1]:
                t += str(sup[i])
            t += "/"
            for i in g[2]:
                t += str(sub[i])
            return t
        # Regular fractions with no integer part
        t = r"([" + "".join(_super) + "]+)/([" + "".join(_sub) + "]+)"
        r = re.compile(t)
        mo = r.search(s)
        if mo:
            g = mo.groups()
            assert len(g) == 2
            t = ""
            for i in g[0]:
                t += str(sup[i])
            t += "/"
            for i in g[1]:
                t += str(sub[i])
            return t
    def ToFraction(string):
        '''Convert a string to a fractions.Fraction object.  '19/16',
        '1 3/16', '1-3/16', and '1+3/16' all give the same fraction.  Use
        FractionFromUnicode() if the string contains Unicode characters.
        '''
        def ConvertFraction(frac):
            "Assumes a/b form where a and b are positive integers"
            f = frac.split("/")
            if len(f) == 1:
                # It must be an integer
                return Fraction(int(f[0].strip()))
            if len(f) != 2:
                raise ValueError(f"'{string}' not proper fractional form")
            a, b = f
            return Fraction(int(a.strip()), int(b.strip()))
        s, sign = string.strip(), 1
        if not s:
            raise ValueError("Empty string")
        # Get sign
        if s[0] == "-":
            sign = -1
            s = s[1:]
        elif s[0] == "+":
            s = s[1:]
        # s is now of the form 'a/b', 'I-a/b', 'I+a/b', or 'I a/b'.  Convert
        # the mixed forms to the canonical 'I-a/b'.
        if "+" in s:
            s = s.replace("+", "-")
        elif " " in s:
            s = s.replace(" ", "-")
        if "-" in s:
            # Mixed form I-a/b
            f = s.split("-")
            if len(f) != 2:
                raise ValueError(f"'{string}' not proper fractional form")
            i, frac = f
            return sign * (int(i) + ConvertFraction(frac))
        else:
            return sign * ConvertFraction(s)

if __name__ == "__main__":
    import sys
    from fractions import Fraction
    from lwtest import run, assert_equal, raises
    from fraction import FormatFraction, FractionToUnicode
    from fraction import FractionFromUnicode, ToFraction, _sub, _super
    def Demo():
        # Print out fractions
        d = 16
        for n in range(1, d):
            print(FormatFraction(Fraction(n, d)), end=" ")
        print()
        d = 32
        for n in range(1, d, 2):
            print(FormatFraction(Fraction(n, d)), end=" ")
        print()
        d = 64
        for n in range(1, d, 2):
            print(FormatFraction(Fraction(n, d)), end=" ")
        print()
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
        for s in ("1  3/16", "1-+3/16", "1--3/16", "1++3/16", "1 3//16", "1 3/-16", "1 3/+16"):
            raises(ValueError, ToFraction, s)
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        exit(run(globals())[0])
    Demo()
