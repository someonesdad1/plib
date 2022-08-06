'''
Format floating point numbers in a variety of ways
    Run this file as a script for help info.  Note:  this is obsolete
    code that was developed using python 2, but it will run under python
    3.  I recommend use of the fmt.py module for python 3 stuff.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2008, 2012 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Obsolete formatter for floating point numbers.  Use
    # fmt.py as a replacement.
    #∞what∞#
    #∞test∞# ["test/fpformat_test.py"] #∞test∞#
    pass
if 1:   # Imports
    import sys
    from os import name as platform
if 1:   # Global variables
    # These variables can be used to control the characters that appear in
    # output.
    decimal_point = "."
    exponent_character = "e"
    imaginary_unit = "i"
class FPFormat:
    '''Formats a floating point number in a variety of ways:
    Fixed           Fixed number of digits after the decimal point (may
                    spill over to scientific notation at a platform-
                    dependent value).
    Significant     Fixed number of significant digits; switches to
                    scientific at user-specified values.
    Scientific      Scientific with a specified number of significant
                    digits.
    Engineering     Engineering with a specified number of significant
                    digits.
    EngineeringSI   Engineering with an SI suffix if appropriate.
 
    Setting the number of digits controls the number of digits after
    the decimal point for Fixed mode and the number of significant
    digits for the other modes.
 
    Use fp.trailing_decimal_point(False) to turn off trailing decimal
    point.  It is on by default to show that a number is floating point.
 
    You can set as many significant digits as you want; your python
    implementation may or may not choke on your chosen value.  On my
    platform, I was able to get fixed outputs such as
        314159265358979330000000000000000000000000000000000000000
    and
        0.0000000000000000000000000000000000000000000000000000000314
    The actual number of significant figures in a python float is
    typically the size of your platform's C double, so if you specify
    more significant figures than that, the resulting excess number of
    digits will almost certainly be wrong unless you use extended-precision
    libraries like python's decimal class or mpmath.
 
    You can fine-tune the scientific and engineering display's exponents by
    the attributes
        expdigits     Number of digits in exponent
        expsign       If true, always display sign
    If the value of expdigits is too small for the given number, the minimum
    number needed will be used.
    '''
    def __init__(self, num_digits=3):
        self.num_digits = 0
        self.digits_min = 0
        self.digits(num_digits)
        self.expdigits = 2    # Number of digits in exponent
        self.expsign = True   # Always display the exponent's sign
        self.low = 1e-4  # Below this, use scientific for sig
        self.high = 1e6   # Above this, use scientific for sig
        self.suffixes = {

            -8: "y", -7: "z", -6: "a", -5: "f", -4: "p", -3: "n", -2:
            "\u03bc", -1: "m", 0: "", 1: "k", 2: "M", 3: "G", 4: "T",
            5: "P", 6: "E", 7: "Z", 8: "Y"}  # SI suffixes (key is exponent/3)

        self.trailing_dp = True
        self.dp_width = 10      # Width of output string
        self.dp_position = 4    # Position of dp from left
    def trailing_decimal_point(self, trail=True):
        'Set whether a trailing decimal point is displayed'
        self.trailing_dp = True if trail else False
    def digits(self, num_digits):
        'Set the number of significant digits'
        if num_digits < self.digits_min:
            raise ValueError("must be >= %d" % self.digits_min)
        self.num_digits = num_digits
    def fix(self, number):
        f = "%%.%df" % self.num_digits
        f1 = "%%+.%df" % self.num_digits
        # Note:  we have to use 'j' here because that's what python's
        # representation uses.
        if "j" in str(number):
            if number.real == 0:
                return (f % number.imag) % imaginary_unit
            elif number.imag == 0:
                return f % number.real
            else:
                return (f % number.real) + (f1 % number.imag) + imaginary_unit
        else:
            return f % number
    def sci(self, number):
        if "j" in str(number):
            if number.real == 0:
                return self._sci(number.imag) + imaginary_unit
            elif number.imag == 0:
                return self._sci(number.real)
            else:
                im_sign = "+" if number.imag > 0 else ""
                return (self._sci(number.real) + im_sign +
                        self._sci(number.imag) + imaginary_unit)
        else:
            return self._sci(number)
    def _sci(self, number):
        "Scientific format for a floating point number"
        f = "%%.%de" % max(self.num_digits - 1, 0)
        s = f % number
        significand, exponent = s.split("e")
        significand = significand.replace(".", decimal_point)
        # Adjust the exponent
        exponent_sign = exponent[0]
        if not self.expsign and exponent_sign == "+":
            exponent_sign = ""
        # Get exponent with required leading zeros
        e = ("%%0%dd" % max(0, self.expdigits)) % abs(int(exponent))
        return ''.join((significand, exponent_character, exponent_sign, e))
    def eng(self, number):
        if "j" in str(number):
            if number.real == 0:
                return self._eng(number.imag) + imaginary_unit
            elif number.imag == 0:
                return self._eng(number.real)
            else:
                im_sign = "+" if number.imag > 0 else ""
                return (self._eng(number.real) + im_sign +
                        self._eng(number.imag) + imaginary_unit)
        else:
            return self._eng(number)
    def engsic(self, number):
        return self.engsi(number, cuddle=True)
    def engsi(self, number, cuddle=False):
        '''Same as eng(), but decorate with SI suffix.
        Will throw exception for a complex number.  If cuddle is true,
        do not put a space between the number and the SI suffix.
        '''
        if "j" in str(number):
            raise TypeError("Complex numbers not supported")
        s = self.eng(number)
        pos = s.find(exponent_character)
        try:
            exponent = int(s[pos + 1:])//3
        except ValueError:
            # Can't format it (e.g., it's like '-1.#IND'
            return s
        except OverflowError:
            return str(number)
        if exponent in self.suffixes:
            if cuddle:
                return s[:pos] + self.suffixes[exponent]
            else:
                return s[:pos] + " " + self.suffixes[exponent]
        return s
    def sig(self, number):
        if number and (abs(number) < self.low or abs(number) > self.high):
            return self.sci(number)
        if "j" in str(number):
            if number.real == 0:
                return self._sig(number.imag) + imaginary_unit
            elif number.imag == 0:
                return self._sig(number.real)
            else:
                re = self.sig(number.real)
                im = self.sig(number.imag)
                im_sign = "+" if number.imag > 0 else ""
                return re + im_sign + im + imaginary_unit
        else:
            return self._sig(number)
    def _sig(self, number):
        "Handle the real number case"
        sign = "-" if number < 0 else ""
        if str(number) == "1.0":
            # This handles case where number is around 1 - 1e-16, which
            # is 1 for all intents and purposes, but will of course
            # test less than 1, causing the value to be sent back 10
            # times too small.
            number = 1
        n = max(self.num_digits - 1, 0)
        s = ("%%.%de" % n) % abs(number)
        fld = s.split("e")
        significand, exponent = fld[0], int(fld[1])
        significand_rounded = float(significand)
        # Remove decimal point from significand string
        significand = significand.replace(".", "")
        if significand_rounded*10.**exponent < 1:
            num_zeros_needed = abs(exponent) - 1
            while num_zeros_needed > 0:
                significand = "0" + significand
                num_zeros_needed -= 1
            significand = "0" + decimal_point + significand
        else:
            if len(significand) > exponent + 1:
                # Need to position decimal point in significand
                e = exponent + 1
                significand = significand[:e] + decimal_point + significand[e:]
            else:
                # Need to add zeros
                num_zeros_needed = exponent - n
                while num_zeros_needed > 0:
                    significand += "0"
                    num_zeros_needed -= 1
                if self.num_digits:
                    if self.trailing_dp:
                        significand += decimal_point
        return sign + significand
    def _eng(self, number):
        "Engineering format for a floating point number"
        efmt = "%%0%dd" % max(0, self.expdigits)
        n = max(self.num_digits - 1, 0)
        significand, exponent = self.sci(number).split(exponent_character)
        significand_rounded = abs(float(significand))
        if self.expsign:
            esign = "-" if int(exponent) < 0 else "+"
        else:
            esign = "-" if int(exponent) < 0 else ""
        exponent = int(exponent)
        if significand[0] == "-":
            significand = significand[1:]
        significand = significand.replace(decimal_point, "")
        if significand_rounded*10.**exponent < 1:
            num_3, remainder = divmod(abs(exponent) - 1, 3)
            # Note abs is used because sign is added below; if number is
            # negative, efmt doesn't work correctly.
            e = efmt % abs(-3*(num_3 + 1))
            dp = 3 - remainder  # Decimal point position
            while len(significand) < dp:
                significand += "0"
            if self.num_digits == 0:
                m = significand
            else:
                if len(significand) == dp:
                    if self.trailing_dp:
                        m = significand + decimal_point
                    else:
                        m = significand
                else:
                    m = significand[:dp] + decimal_point + significand[dp:]
        else:
            num_3, remainder = divmod(exponent, 3)
            e = efmt % (3*num_3)
            while len(significand) < remainder+1:
                significand += "0"
            if self.num_digits == 0:
                m = significand
            else:
                # Insert decimal point
                if len(significand) == remainder + 1:
                    if self.trailing_dp:
                        m = significand + decimal_point
                    else:
                        m = significand
                else:
                    m = (significand[:remainder+1] + decimal_point + 
                         significand[remainder+1:])
        if number < 0:
            m = "-" + m
        return ''.join((m, exponent_character, esign, e))
    def dp(self, num, width=None, dpoint=None):
        '''Fit the string into a stated width with the decimal point at the
        0-based position starting from the left.  width overrides the
        self.dp_width setting; dpoint overrides the self.dp_position
        setting.  Note the number significant figures in the result may be
        reduced to get it to fit into the given space.
 
        The intent is to let you have a field of known width where the
        decimal points line up -- this is useful when displaying
        information that varies over a few orders of magnitude.  The
        routine will display "-.-" for numbers outside the displayable
        range.
 
        Algorithm:
 
            0 1 2 3 4 5 6 7 8 9
           +-------------------+
           | | | | | |.| | | | |
           +-------------------+
                      ^
                      |
                      dp
           |<----------------->| = w
 
        String index of decimal point = dp
        Width of whole string = w
        Number of spots to left of decimal place  = dp
        Number of spots to right of decimal place = r = w - dp - 1
 
        Allowed forms:
            1.  sig with a decimal point
            2.  sig with no decimal point
        Scientific format isn't allowed, so if the number can't fit
        in the given space, "-.-" is displayed.
 
        Numbers displayable are:
            if x < 1:
                abs(x) > 10**r
            else:
                x < 10**dp - 10**(-r)
                and
                x > -(10**(dp - 1) - 10**(-r)
        '''
        bad = "-.-"
        if "j" in str(num):
            raise TypeError("Complex numbers not supported")
        w = self.dp_width if width is None else width
        dp = self.dp_position if dpoint is None else dpoint
        r, displayable = w - dp - 1, True
        def Get(num, digits):
            '''Set the indicated number of digits and get the sig() string.
            '''
            old_digits = self.num_digits
            self.num_digits = digits
            s = self.sig(num)
            self.num_digits = old_digits
            return s
        # Determine if number is displayable
        q = 10**(-r)
        if num < 1:
            if abs(num) < q:
                displayable = False
        else:
            if not (-(10**(dp - 1) - q) <= num <= (10**dp - q)):
                displayable = False
        if not displayable:
            s = " "*(dp - 1) + bad + " "*(r - 1)
            if len(s) <= w:
                return s
            raise ValueError("width of %d too small" % w)
        # Number is displayable, so find a number of digits that allow
        # self.sig() to be displayed in the given space.
        for digits in range(self.num_digits, 0, -1):
            s = Get(num, digits)
            loc = s.find(decimal_point)
            if loc == -1:
                raise ValueError("Number doesn't contain decimal point")
            while loc < dp:
                s = " " + s
                loc = s.find(decimal_point)
            right = len(s) - loc - 1
            while right < r:
                s += " "
                right = len(s) - loc - 1
            if exponent_character in s:
                raise ValueError("Number %s requires sci()" % num)
            if len(s) == w:
                # We've found the proper expression, so just return it
                return s
        # Not displayable
        s = " "*(dp - 1) + bad + " "*(r - 1)
        if len(s) <= w:
            return s
        raise ValueError("width of %d too small" % w)
if __name__ == "__main__":
    from wrap import dedent
    print(dedent(f'''
    How to use fpformat:
      Create an object:      fp = fpformat.FPFormat(num_digits=3)
      Set number of digits:  fp.digits(num_digits)
      Get formatted string:  sig(x), fix(x), sci(x), eng(x), engsi(x), engsic(x)
      The fp.dp() method is used to get strings of fixed width where the
          decimal points line up.
      Use fp.trailing_decimal_point(False) to turn off trailing decimal point.
        It is on by default to show that a number is floating point.
      Set the attributes
          low, high       Determine when sci format is output for sig()
          expdigits       Number of digits in exponent
          expsign         If true, display exponent's sign
        for fine control over the scientific display.
     
    Set the following global variables to control some of the output
    characteristics:             Default
                                 -------
        decimal_point               {decimal_point}
        exponent_character          {exponent_character}
        imaginary_unit              {imaginary_unit}
    '''))
    f, L, indent = FPFormat(4), 10, " "*5
    f.low, f.high = 10**(-L), 10**L
    w, dp = 15, 8
    x, places = 1.23456*10**(-dp), w - dp - 1
    print(dedent(f'''
    Demonstration of dp() method for decimal point alignment.  Note
    it can reduce the number of significant figures printed.  The form of
    the function is fpformat.dp(x, width=w, dpoint=dp) where here
    w = {w} and dp = {dp}.  The total width is 15 spaces and the decimal
    point is at position dp, which is numbered from zero from the left.
    This leaves room for {w} - {dp} - 1 = {places} decimal places.
    '''))
    print(indent + " ", end="")
    for i in range(w):
        print(str(i)[-1], end="")
    print()
    while x < 1e9:
        try:
            s = f.dp(x, width=w, dpoint=dp)
            print(indent, end="")
            print("|" + s + "| number = ", end="")
            print(f.sci(x), end="")
            print()
        except ValueError as e:
            print(str(e))
        x *= 10
