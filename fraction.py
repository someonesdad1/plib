'''
xx Move to fmt.py

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
#∞test∞# ignore #∞test∞#

import re
from fractions import Fraction

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

_super, _sub = "⁰¹²³⁴⁵⁶⁷⁸⁹", "₀₁₂₃₄₅₆₇₈₉"

def FormatFraction(f, improper=False):
    '''Return the string form of a fraction using Unicode subscript and
    superscript characters.  If improper is True, return an improper
    fraction.
    '''
    if not isinstance(f, Fraction):
        raise TypeError("f must be a Fraction")
    s, n, d = "", f.numerator, f.denominator
    if improper:
        rem = n
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
        assert(len(g) == 3)
        # Change denominator
        u = []
        for i in g[2]:
            u.append(_sub[int(i)])
        a, b = mo.span(3)
        t = t[:a] + ''.join(u) + t[b:]
        # Change numerator
        u = []
        for i in g[1]:
            u.append(_super[int(i)])
        a, b = mo.span(2)
        t = t[:a] + ''.join(u) + t[b:]
        # Change integer part
        ip = g[0]
        assert(len(ip) > 1)
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
    sup = {"⁰":0, "¹":1, "²":2, "³":3, "⁴":4, "⁵":5, "⁶":6, "⁷":7, "⁸":8, "⁹":9}
    sub = {"₀":0, "₁":1, "₂":2, "₃":3, "₄":4, "₅":5, "₆":6, "₇":7, "₈":8, "₉":9}
    # Mixed fractions
    t = r"(\d+)([" + ''.join(_super) + "]+)/([" + ''.join(_sub) + "]+)"
    r = re.compile(t)
    mo = r.search(s)
    if mo:
        g = mo.groups()
        assert(len(g) == 3)
        t = g[0] + sep
        for i in g[1]:
            t += str(sup[i])
        t += "/"
        for i in g[2]:
            t += str(sub[i])
        return t
    # Regular fractions with no integer part
    t = r"([" + ''.join(_super) + "]+)/([" + ''.join(_sub) + "]+)"
    r = re.compile(t)
    mo = r.search(s)
    if mo:
        g = mo.groups()
        assert(len(g) == 2)
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
        'Assumes a/b form where a and b are positive integers'
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
    if '+' in s:
        s = s.replace("+", "-")
    elif ' ' in s:
        s = s.replace(" ", "-")
    if "-" in s:
        # Mixed form I-a/b
        f = s.split("-")
        if len(f) != 2:
            raise ValueError(f"'{string}' not proper fractional form")
        I, frac = f
        return sign*(int(I) + ConvertFraction(frac))
    else:
        return sign*ConvertFraction(s)

if __name__ == "__main__": 
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
