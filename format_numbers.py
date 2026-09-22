'''
∞∞2 This functionality should be moved to fmt.py
∞∞2 A number like 3.14e-34 needs to be changed to a power of 10
----------------------------------------------------------------------
Module to format numbers using Unicode characters to make them easier
to read.
'''
if 1:   # Header
    _pgminfo = '''
        <oo gist ∞ Format numbers using Unicode characters oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2022 Don Peterson oo>
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
        from decimal import Decimal
        from fractions import Fraction
        from string import ascii_letters
    if 1:   # Custom imports
        from fpformat import FPFormat
        from sig import sig
        from uncertainties.core import Variable
        from roundoff import RoundOff
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        # Dictionary to translate exponents to Unicode characters
        tt = {
            "0": "⁰",
            "1": "¹",
            "2": "²",
            "3": "³",
            "4": "⁴",
            "5": "⁵",
            "6": "⁶",
            "7": "⁷",
            "8": "⁸",
            "9": "⁹",
            "+": "",
            "-": "⁻",
            " ": "·",
            "^": "",
        }
if 1:   # Core functionality
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
            out.append("".join(o))
        if solidus and neg in "".join(out):
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
            return "".join(["·".join(numer), "/", "·".join(denom)])
        else:
            return "·".join(out)
    def FormatNumber(num, units=None, digits=None, sci=False, eng=False, engsi=False,
        exact=False, length=None, improper=False, position="<", solidus=False,):
        '''Return a string form for the number num.  The type of num can be a float,
        integer, fraction, Decimal, or ufloat.
        
        units must be a string of unit characters followed by a positive or negative
        integer.  Example:  'm s-2' stands for meters per second squared.  The units
        must be separated by space characters or '·' characters (U+00b7).  The
        circumflex can be used for exponentiation if desired (it is ignored), e.g. 'm
        s^-2'.
        
        digits is the number of significant figures to format the number to (this is
        ignored for ufloats).  If set to None, it will default to 3.
        
        sci if True means use scientific notation.
        
        eng if True means use engineering notation.
        
        engsi if True means use engineering notation and return an SI prefix after the
        formatted string with one space before the prefix.  You would usually use this
        only with a single unit string because it will bond tightly to the first unit
        designator and in a string with multiple units, this probably isn't what you
        meant.  Thus, if you use this, I suggest you not include a units keyword and add
        the unit string yourself after getting back the formatted number.  exact
        indicates that the number is exact, so formatting with sig() or the FPFormat()
        instance won't be used.  The RoundOff function will be used to ensure it's
        string form as a float doesn't have nuisance digits.
        
        length is the returned length of the string.  An exception will be raised if the
        formatted string can't fit into the given length.
        
        improper if True means to format Fractions as improper fractions.  If False,
        they will be formatted as mixed fractions.
        
        position is only used if length is not None.  > means to left justify, ^ means
        to center, and < means to right justify.
        
        solidus is a Boolean passed to FormatUnits.
        '''
        if not hasattr(FormatNumber, "fp"):
            FormatNumber.fp = FPFormat()
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
                return F(ff(sig(num, digits)) + un if digits else ff(sig(num)) + un)
        elif isinstance(num, Fraction):
            return F(FormatFraction(num, improper=improper) + un)
        elif isinstance(num, Variable):
            # Old method:  comparing types, but pycodestyle complains
            # elif type(num) == type(ufloat(1, 0)):
            return F(ff(sig(num)) + un)
        else:
            return F(str(num) + un)
    def FormatFloat(num, length=None):
        '''num will be a string of the form 6.6(3)e-27 or without the
        uncertainty.  Translate it to the more conventional form of
        6.6(3)×10⁻²⁷.  length is the desired length of the string; None
        means don't return a fixed length.
        '''
        if "e" not in num.lower():
            return num + (" " * (length - len(num))) if length else num
        m, e = num.lower().split("e")
        e = str(int(e))  # Removes the 0 from e.g. -05
        x = [m, "×", "10"]
        for char in e:
            x.append(tt.get(char, char))
        t = "".join(x)
        return t + (" " * (length - len(t))) if length else t
    def FormatFraction(f, improper=False, length=None):
        '''Return the string form of a fraction using Unicode subscript and
        superscript characters.  If improper is True, return an improper
        fraction.
        '''
        if not hasattr(FormatFraction, "fp"):
            FormatFraction.super = "⁰¹²³⁴⁵⁶⁷⁸⁹"
            FormatFraction.sub = "₀₁₂₃₄₅₆₇₈₉"
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
        return s + (" " * (length - len(s))) if length else s

if __name__ == "__main__":  
    if 1:   # Standard imports
        from math import pi
    if 1:   # Custom imports
        from lwtest import raises, run
        from uncertainties import ufloat
    def TestUnitFormatting():
        # Basics
        s = "m"
        assert FormatUnits(s, solidus=True) == "m"
        assert FormatUnits(s, solidus=False) == "m"
        s = "m2"
        assert FormatUnits(s, solidus=True) == "m²"
        assert FormatUnits(s, solidus=False) == "m²"
        s = "m-1"
        assert FormatUnits(s, solidus=True) == "1/m"
        assert FormatUnits(s, solidus=False) == "m⁻¹"
        s = "m-2"
        assert FormatUnits(s, solidus=True) == "1/m²"
        assert FormatUnits(s, solidus=False) == "m⁻²"
        # Lots of digits
        s = "m22222"
        assert FormatUnits(s, solidus=True) == "m²²²²²"
        assert FormatUnits(s, solidus=False) == "m²²²²²"
        s = "m-22222"
        assert FormatUnits(s, solidus=True) == "1/m²²²²²"
        assert FormatUnits(s, solidus=False) == "m⁻²²²²²"
        # + and -
        s = "m s⁻¹"
        assert FormatUnits(s, solidus=True) == "m/s"
        assert FormatUnits(s, solidus=False) == "m·s⁻¹"
        s = "m s⁻²"
        assert FormatUnits(s, solidus=True) == "m/s²"
        assert FormatUnits(s, solidus=False) == "m·s⁻²"
        # All digits handled
        s = "m1234567890"
        assert FormatUnits(s, solidus=True) == "m¹²³⁴⁵⁶⁷⁸⁹⁰"
        assert FormatUnits(s, solidus=False) == "m¹²³⁴⁵⁶⁷⁸⁹⁰"
        s = "m-1234567890"
        assert FormatUnits(s, solidus=True) == "1/m¹²³⁴⁵⁶⁷⁸⁹⁰"
        assert FormatUnits(s, solidus=False) == "m⁻¹²³⁴⁵⁶⁷⁸⁹⁰"
        # + ignored
        s = "m+2"
        assert FormatUnits(s, solidus=True) == "m²"
        assert FormatUnits(s, solidus=False) == "m²"
        s = "m+2 m-2"
        assert FormatUnits(s, solidus=True) == "m²/m²"
        assert FormatUnits(s, solidus=False) == "m²·m⁻²"
        # Just a digit
        s = "2"
        raises(ValueError, FormatUnits, s)
    def TestFormatFraction():
        # Regular fraction
        f = Fraction(2, 3)
        s = FormatNumber(f, units="m s-1", solidus=True)
        assert s == "²/₃ m/s"
        s = FormatNumber(f, units="m s-1", solidus=False)
        assert s == "²/₃ m·s⁻¹"
        # Mixed/improper fraction
        f = Fraction(3, 2)
        s = FormatNumber(f, units="m s-1", solidus=True, improper=False)
        assert s == "1¹/₂ m/s"
        s = FormatNumber(f, units="m s-1", solidus=True, improper=True)
        assert s == "³/₂ m/s"
        # Fixed length
        f = Fraction(2, 3)
        s = FormatNumber(f, solidus=True, length=7, position="<")
        assert s == "²/₃    "
        s = FormatNumber(f, solidus=True, length=7, position="^")
        assert s == "  ²/₃  "
        s = FormatNumber(f, solidus=True, length=7, position=">")
        assert s == "    ²/₃"
        raises(ValueError, FormatNumber, f, solidus=True, length=2, position=">")
    def TestFormatNumber():
        x = pi
        s = FormatNumber(x, units="m s-1")
        assert s == "3.14 m·s⁻¹"
        s = FormatNumber(x, units="m s-1", digits=8)
        assert s == "3.1415927 m·s⁻¹"
        x = pi * 1e-34
        s = FormatNumber(x, units="m s-1")
        assert s == "3.14×10⁻³⁴ m·s⁻¹"
        # Ufloat
        x = ufloat(pi * 1e8, 0.0123e8)
        s = FormatNumber(x, units="m s-1")
        assert s == "3.14(1)×10⁸ m·s⁻¹"
        # Decimal
        x = Decimal("3.14159e8")
        s = FormatNumber(x, units="m s-1")
        assert s == "3.14×10⁸ m·s⁻¹"
        s = FormatNumber(x, units="m s-1", digits=6)
        assert s == "3.14159×10⁸ m·s⁻¹"
        # Integer
        x = 314159
        s = FormatNumber(x, units="m s-1")
        assert s == "314159 m·s⁻¹"
        # String
        x = "314159"
        s = FormatNumber(x, units="m s-1")
        assert s == "314159 m·s⁻¹"
    exit(run(globals())[0])
