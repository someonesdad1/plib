'''
SI prefixes
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#
import sys
import math
from fmt import fmt
from f import flt
from collections import deque

have_mpmath = False
try:
    import mpmath as M
    have_mpmath = True
except ImportError:
    pass
if 0:
    import debug
    debug.SetDebugger()
ii = isinstance

class SI(dict):
    '''Class to present a bidict behavior for both SI prefix strings
    and exponents.  Index as a dictionary with an SI prefix string and
    you'll have the corresponding base 10 logarithm returned.  Call as
    a function with an integer representing the base 10 logarithm of
    the prefix and you'll have the corresponding prefix returned.
 
    An incorrect string or integer will result in a KeyError
    exception.

    Use pure=True in constructor to avoid the 'd c, da h" prefixes.
    '''
    def __init__(self, pure=False):
        self.update({
            "m": -3,    # milli
            "μ": -6,    # micro
            "u": -6,    # micro
            "n": -9,    # nano
            "p": -12,   # pico
            "f": -15,   # femto
            "a": -18,   # atto
            "z": -21,   # zepto
            "y": -24,   # yocto
            "r": -27,   # ronto   Added 2022 27th CGPM
            "q": -30,   # quecto  Added 2022 27th CGPM
            "k": 3,     # kilo
            "M": 6,     # mega
            "G": 9,     # giga
            "T": 12,    # tera
            "P": 15,    # peta
            "E": 18,    # exa
            "Z": 21,    # zetta
            "Y": 24,    # yotta
            "R": 27,    # ronna   Added 2022 27th CGPM
            "Q": 30,    # quetta  Added 2022 27th CGPM
        })
        self.d = {
            -3: "m",
            -6: "μ",
            -9: "n",
            -12: "p",
            -15: "f",
            -18: "a",
            -21: "z",
            -24: "y",
            -27: "r",
            -30: "q",
            0: "",
            3: "k",
            6: "M",
            9: "G",
            12: "T",
            15: "P",
            18: "E",
            21: "Z",
            24: "Y",
            27: "R",
            30: "Q",
        }
        self.pure = pure
        if not self.pure:
            self.update({
                "d": -1,
                "c": -2,
                "da": 1,
                "h": 2,
            })
            self.d.update({
                -1: "d",
                -2: "c",
                1: "da",
                2: "h",
            })
    def __call__(self, x):
        return self.d[x]
# Convenience instance 
si = SI()
 
def GetSIExponent(e: int):
    '''Return None if not (-24 <= e <= 26).  Otherwise, return the nearest
    integer that is a suitable exponent division by 3.
    '''
    if not (-24 <= e <= 26):
        return None
    e = 24 if e > 24 else e
    while abs(e) % 3 != 0:
        e -= 1
    return e
def GetSI(x, eng=False):
    '''
    - Call with a single character string that is an SI prefix and
      you'll have the corresponding power of 10 returned.  An
      unrecognized SI string results in an exception.
 
    - Call with a number (integer or float) and a tuple (x, t, p) will
      be returned:
        x is the original number
        t is the number's significand (a number in the interval [1, 10)
        p is the appropriate SI prefix
      
      If x is 0, then (x, 0, "") is returned.
 
      If x is in (1/1000, 1000), then (x, x, "") is returned.
 
      If x is not within a factor of 1000 of
      the largest or smallest SI prefix, then None is returned for t
      and p.  The exception is when x is 0, in which case (x, 0, "")
      will be returned.  If x is in (1/1000, 1000), then (x, x, "") is
      returned if eng is True.
 
    If eng is True, then the prefixes d, c, da, and h are not allowed.
    '''
    if ii(x, str):
        if not x:
            return 1
        if len(x) > 2:
            raise ValueError("x must be string of length 1 or 2")
        if x in si:
            if eng and x in ("d", "c", "da", "h"):
                msg = "Prefixes that aren't a power of 3 not allowed"
                raise ValueError(msg)
            return 10**si[x]
        else:
            raise ValueError("'%s' is not a recognized SI prefix" % x)
    elif ii(x, (int, float)) or (have_mpmath and ii(x, M.mpf)):
        sgn = -1 if x < 0 else 1
        no_match = (x, None, None)
        if not x:
            return (x, 0, "")
        if ii(x, (int, float)):
            e = int(math.floor(math.log10(x)))
        else:
            e = int(M.floor(M.log10(x)))
        # See if exponent is in range
        e1 = GetSIExponent(e)
        if e1 is None:
            return no_match
        assert(e1 <= e)
        correction = e - e1
        assert(correction in (0, 1, 2))
        # Get significand
        t = fmt.significand(abs(x))
        t = M.mpf(t) if have_mpmath and ii(x, M.mpf) else float(t)
        # Adjust exponent to be a power of 3
        p = si(e1)
        t *= 10**correction
        return (x, t, p)
    else:
        raise ValueError("x must be string, float (mpmath.mpf OK too), or integer")
def Testing():
    from lwtest import Assert, raises
    # float
    a = 6.2
    for e in range(-25, 28):
        b = a*10**e
        e1 = GetSIExponent(e)
        expected_p = None
        if e1 in si.values():
            expected_p = si(e1)  # Yep, an incestuous test
            correction = e - e1
        if expected_p is not None:
            x, t, p = GetSI(b)
            Assert(p == expected_p)
            Assert(correction in (0, 1, 2))
            x1 = round(float(t), 2)
            b1 = 10**correction*round(float(fmt.significand(t)), 2)
            Assert(str(x1) == str(b1))
        else:
            if e < -24 or e > 25:
                Assert(GetSI(b) == (b, None, None))
            elif 0 <= e < 3:
                Assert(GetSI(b) == (b, b, ""))
            else:
                raise Exception("Bug")
    # mpmath
    a = M.mpf(6.2)
    for e in range(-25, 28):
        b = a*10**e
        e1 = GetSIExponent(e)
        expected_p = None
        if e1 in si.values():
            expected_p = si(e1)  # Yep, an incestuous test
            correction = e - e1
        if expected_p is not None:
            x, t, p = GetSI(b)
            Assert(p == expected_p)
            Assert(correction in (0, 1, 2))
            x1 = round(M.mpf(t), 2)
            b1 = 10**correction*round(M.mpf(fmt.significand(t)), 2)
            Assert(str(x1) == str(b1))
        else:
            if e < -24 or e > 25:
                Assert(GetSI(b) == (b, None, None))
            elif 0 <= e < 3:
                Assert(GetSI(b) == (b, b, ""))
            else:
                raise Exception("Bug")
    # Prefixes
    di = {
        "": 0,
        "d": -1,
        "c": -2,
        "m": -3,
        "μ": -6,
        "u": -6,
        "n": -9,
        "p": -12,
        "f": -15,
        "a": -18,
        "z": -21,
        "y": -24,
        "da": 1,
        "h": 2,
        "k": 3,
        "M": 6,
        "G": 9,
        "T": 12,
        "P": 15,
        "E": 18,
        "Z": 21,
        "Y": 24
    }
    for prefix in di:
        expected = 10**di[prefix]
        Assert(expected == GetSI(prefix))
    # Not allowed prefix when eng is True
    for i in ("d", "c", "da", "h"):
        raises(ValueError, GetSI, i, eng=True)
def PerformConversion(s):
    '''If the string s contains 'e', then convert to SI engineering notation.
    If it contains an SI prefix, convert it to 'e' notation.
 
    Examples:  '3.4e7' returns '34M'.  '34M' returns '3.4e7'.
    '''
    # Remove any trailing SI prefix
    n = GetSignificantFigures(s)
    if "e" in s:
        x = float(s)
        if 1e-24 <= x < 1e27:
            return fmt(x, fmt="engsic", n=n)
        else:
            return s
    else:
        found = ""
        for i in "yzafpnμmkMGTPEZY":
            if i in s:
                found = i
                break
        if found:
            if not s.endswith(found):
                raise ValueError(f"{s!r} doesn't end with {found!r}")
            x = float(s[:-1])*10**si[found]
            return fmt.sci(x, n=n)
        else:
            # Assume it's an integer 
            return fmt.engsic(float(s))
def GetSignificantFigures(s):
    '''Given a string s representing a floating point number, determine how
    many significant figures it has.
    '''
    def Fix(s):
        for i in "+- .,":
            s = s.replace(i, "")
        return s
    # Remove any SI prefix
    u = s
    for i in si:
        if s.endswith(i):
            n = len(i)
            u = u[:-n]
    u = u.lower()
    if "e" in u:
        t = Fix(u.split("e")[0])
    elif "×10" in u:
        t = Fix(u.split("×")[0])
    else:
        if "." in u or "," in u:
            t = Fix(u)
        else:
            # It's an integers.  Note an integer > 1e308 will cause an
            # exception.
            v = deque(repr(int(u)))
            # Get rid of trailing zeroes
            while v[-1] == "0":
                v.pop()
            return len(v)
    return len(t)
def ConvertSI(s):
    '''String s can end in an SI prefix and the remaining characters must
    represent a float.  Return a flt instance for the represented number.
    '''
    if s == "inf":
        return flt("inf")
    elif s == "-inf":
        return flt("-inf")
    if s.endswith("da"):
        raise ValueError(f"{s!r} cannot end in prefix 'da'")
    found = ""
    for prefix in si:
        if s.endswith(prefix):
            found = prefix
            break
    if not found:
        return flt(s)
    s = s[:-1]  # Remove prefix letter
    x = flt(s)*10**si[prefix]
    return x

if 0 and __name__ == "__main__":
    s = "342M"
    print(s, "-->", PerformConversion(s))
    exit()

if __name__ == "__main__": 
    Testing()
    if len(sys.argv) > 1:
        for input in sys.argv[1:]:
            output = PerformConversion(input)
            print(input, "-->", output)
    else:
        names = {
            -24: "yocto",
            -21: "zepto",
            -18: "atto",
            -15: "femto",
            -12: "pico",
            -9: "nano",
            -6: "micro",
            -3: "milli",
            -2: "centi",
            -1: "deci",
            1: "deca",
            2: "hecto",
            3: "kilo",
            6: "mega",
            9: "giga",
            12: "tera",
            15: "peta",
            18: "exa",
            21: "zetta",
            24: "yotta",
        }
        print("Symbol   Exponent    Prefix")
        print("------   --------    ------")
        for num in (-24, -21, -18, -15, -12, -9, -6, -3, -2, -1, 1, 2, 3, 6, 9,
                    12, 15, 18, 21, 24):
            if num:
                sym = si(num)
                name = names[num]
                print("  %2s      %4d       %s" % (sym, num, name))
