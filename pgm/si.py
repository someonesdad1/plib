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
from math import log10 as _log10

if sys.version_info[0] == 3:
    long = int

class _si(dict):
    '''Class to present a bidict behavior for both SI prefix strings
    and exponents.  Index as a dictionary with an SI prefix string and
    you'll have the corresponding base 10 logarithm returned.  Call as
    a function with an integer representing the base 10 logarithm of
    the prefix and you'll have the corresponding prefix returned.

    An incorrect string or integer will result in a KeyError
    exception.
    '''
    def __init__(self):
        self.update({
            "d" : -1,
            "c" : -2,
            "m" : -3,
            "μ" : -6,
            "n" : -9,
            "p" : -12,
            "f" : -15,
            "a" : -18,
            "z" : -21,
            "y" : -24,
            "da" :  1,
            "h" :  2,
            "k" :  3,
            "M" :  6,
            "G" :  9,
            "T" :  12,
            "P" :  15,
            "E" :  18,
            "Z" :  21,
            "Y" :  24
        })
    def __call__(self, x):
        d = {
            -1  : "d",
            -2  : "c",
            -3  : "m",
            -6  : "μ",
            -9  : "n",
            -12 : "p",
            -15 : "f",
            -18 : "a",
            -21 : "z",
            -24 : "y",
            1  : "da",
            2  : "h",
            3  : "k",
            6  : "M",
            9  : "G",
            12 : "T",
            15 : "P",
            18 : "E",
            21 : "Z",
            24 : "Y",
        }
        return d[x]

si = _si()

def SI(x, eng=False):
    '''
    - Call with a single character string that is an SI prefix and
      you'll have the corresponding power of 10 returned.  An
      unrecognized SI string results in an exception.
 
    - Call with a number (integer or float) and a tuple (x, t, p) will
      be returned where x is the original number, t is the number's
      significand (a number in the interval [1, 10), and p is the
      appropriate SI prefix.  If x is not within a factor of 1000 of
      the largest or smallest SI prefix, then None is returned for t
      and p.  The exception is when x is 0, in which case (x, 0, "")
      will be returned.  If x is in (1/1000, 1000), then (x, x, "") is
      returned if eng is True.
 
    If eng is True, then the prefixes d, c, da, and h are not allowed.
    '''
    if isinstance(x, str):
        if not x:
            raise ValueError("x cannot be the empty string")
        if len(x) > 2 :
            raise ValueError("x must be string of length 1 or 2")
        if x in SI_p2n:
            if eng and x in ("d", "c", "da", "h"):
                msg = "Prefixes that aren't a power of 3 not allowed"
                raise ValueError(msg)
            return 10**SI_p2n[x]
        else:
            raise ValueError("'%s' is not a recognized SI prefix" % x)
    elif isinstance(x, (int, long, float)):
        val, sgn = abs(x), (-1 if x < 0 else 1)
        if not val:
            return (x, 0, "")
        exponent = log10(x)
    else:
        raise ValueError("x must be string, float, or integer")

if __name__ == "__main__":
    names = {
        -24 : "yocto",
        -21 : "zepto",
        -18 : "atto",
        -15 : "femto",
        -12 : "pico",
        -9 : "nano",
        -6 : "micro",
        -3 : "milli",
        -2 : "centi",
        -1 : "deci",
        1 : "deca",
        2 : "hecto",
        3 : "kilo",
        6 : "mega",
        9 : "giga",
        12 : "tera",
        15 : "peta",
        18 : "exa",
        21 : "zetta",
        24 : "yotta",
    }
    print("Symbol   Exponent    Prefix")
    print("------   --------    ------")
    for num in (-24, -21, -18, -15, -12, -9, -6, -3, -2, -1, 1, 2, 3, 6, 9,
                12, 15, 18, 21, 24):
        if num:
            sym = si(num)
            name = names[num]
            print("  %2s      %4d       %s" % (sym, num, name))
