'''
xx This functionality should be moved to fmt.py

xx A number like 3.14e-34 needs to be changed to a power of 10

----------------------------------------------------------------------
Module to format numbers using Unicode characters to make them easier
to read.
'''
#∞test∞# ignore #∞test∞#

from decimal import Decimal
from fpformat import FPFormat
from fractions import Fraction
from math import pi
from sig import sig
from string import ascii_letters
from uncertainties import ufloat
from roundoff import RoundOff

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

# Dictionary to translate exponents to Unicode characters
tt = {
    "0" : "⁰",
    "1" : "¹",
    "2" : "²",
    "3" : "³",
    "4" : "⁴",
    "5" : "⁵",
    "6" : "⁶",
    "7" : "⁷",
    "8" : "⁸",
    "9" : "⁹",
    "+" : "",
    "-" : "⁻",
    " " : "·",
    "^" : "",
}

def FormatUnits(unit, solidus=False):
    '''unit is a string of the form e.g. 'm2 s-2'.  The returned string
    will be of the form m²·s⁻².  This is a pure text translation; no
    syntax checking is done except to see that the first character is an
    ASCII letter.
 
    If solidus is True, then the negative exponent terms are collected
    and put after a single solidus in the returned string.  Thus, 'm2
    s-2 K-1' will be returned as m²/s²·K.  There will be only one
    solidus ('/') character and all the terms to the right of it will be
    interpreted as being in the denominator.  This is not valid SI
    syntax, but it's easier to read than a long string with negative
    exponents.  
 
    Note:  This function will do no arithmetic with the unit exponents.
    Thus, if you pass in a string like unit = "m2 m-2", you'll get the 
    result "m²·m⁻²" or "m²/m²".
    '''
    unit, out, neg = unit.replace("·", " ").strip(), [], "⁻"
    if not unit:
        return unit
    for u in unit.split():
        o = []
        for i, item in enumerate(u):
            # First character must be an ASCII letter
            if i == 0 and item not in ascii_letters:
                raise ValueError(f"'{item}' doesn't begin with an ASCII letter")
            if item in tt:
                o.append(tt[item])
            else:
                o.append(item)
        out.append(''.join(o))
    if solidus and neg in ''.join(out):
        numer, denom = [], []
        for i in out:
            if neg in i:
                if i[-2:] == "⁻¹" and i.count("¹") == 1:
                    i = i[:-2]
                else:
                    i = i.replace(neg, "")
                denom.append(i)
            else:
                numer.append(i)
        if not numer:
            numer = ["1"]
        return ''.join(['·'.join(numer), "/", '·'.join(denom)])
    else:
        return '·'.join(out)

def FormatNumber(num, units=None, digits=None, sci=False, eng=False, 
                 engsi=False, exact=False, length=None, improper=False,
                 position="<", solidus=False):
    '''Return a string form for the number num.  The type of num can be
    a float, integer, fraction, Decimal, or ufloat.
 
    units must be a string of unit characters followed by a positive or
    negative integer.  Example:  'm s-2' stands for meters per second
    squared.  The units must be separated by space characters or '·'
    characters (U+00b7).  The circumflex can be used for exponentiation
    if desired (it is ignored), e.g. 'm s^-2'.
 
    digits is the number of significant figures to format the number to
    (this is ignored for ufloats).  If set to None, it will default to
    3.
 
    sci if True means use scientific notation.
 
    eng if True means use engineering notation.
 
    engsi if True means use engineering notation and return an SI prefix
    after the formatted string with one space before the prefix.  You
    would usually use this only with a single unit string because it
    will bond tightly to the first unit designator and in a string with
    multiple units, this probably isn't what you meant.  Thus, if you
    use this, I suggest you not include a units keyword and add the unit
    string yourself after getting back the formatted number.
 
    exact indicates that the number is exact, so formatting with sig()
    or the FPFormat() instance won't be used.  The RoundOff function
    will be used to ensure it's string form as a float doesn't have
    nuisance digits.
 
    length is the returned length of the string.  An exception will be
    raised if the formatted string can't fit into the given length.
 
    improper if True means to format Fractions as improper fractions.
    If False, they will be formatted as mixed fractions.
 
    position is only used if length is not None.  > means to left
    justify, ^ means to center, and < means to right justify.
 
    solidus is a Boolean passed to FormatUnits.
    '''
    def F(s):
        '''Return string s formatted per position if length is given;
        otherwise just return s.
        '''
        if length:
            if len(s) > length:
                m = f"Formatted string '{s}' is longer than given length {length}"
                raise ValueError(m)
            return f"{s:{position}{length}s}"
        else:
            return s
    dig = 3 if digits is None else digits
    fp, ff = FormatNumber.fp, FormatFloat
    fp.digits(dig)
    un = (" " + FormatUnits(units, solidus=solidus)) if units else ""
    if isinstance(num, (float, Decimal)):
        if exact:
            return F(ff(str(RoundOff(num))) + un)
        elif sci:
            return F(ff(fp.sci(num)) + un)
        elif eng:
            return F(ff(fp.eng(num)) + un)
        elif engsi:
            return F(ff(fp.engsi(num)) + un)
        else:
            return (F(ff(sig(num, digits)) + un if digits
                    else ff(sig(num)) + un))
    elif isinstance(num, Fraction):
        return F(FormatFraction(num, improper=improper) + un)
    elif type(num) == type(ufloat(1, 0)):
        return F(ff(sig(num)) + un)
    else:
        return F(str(num) + un)
FormatNumber.fp = FPFormat()

def FormatFloat(num, length=None):
    '''num will be a string of the form 6.6(3)e-27 or without the
    uncertainty.  Translate it to the more conventional form of
    6.6(3)×10⁻²⁷.  length is the desired length of the string; None
    means don't return a fixed length.
    '''
    if "e" not in num.lower():
        return num + (" "*(length - len(num))) if length else num
    m, e = num.lower().split("e")
    e = str(int(e))     # Removes the 0 from e.g. -05
    x = [m, "×", "10"]
    for char in e:
        x.append(tt.get(char, char))
    t = ''.join(x)
    return t + (" "*(length - len(t))) if length else t

def FormatFraction(f, improper=False, length=None):
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
    for i in str(rem):
        s += FormatFraction.super[int(i)]
    s += "/"
    for i in str(d):
        s += FormatFraction.sub[int(i)]
    return s + (" "*(length - len(s))) if length else s
FormatFraction.super = "⁰¹²³⁴⁵⁶⁷⁸⁹"
FormatFraction.sub = "₀₁₂₃₄₅₆₇₈₉"
