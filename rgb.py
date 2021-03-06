'''

    - Overall color strategy
        - clr.py is modern tool to use for all color work in a terminal
        - Move all stuff to clr.py so it's in one place with its self tests
        - Color object provides
            - Storage for a 24-bit color (memory efficient)
            - Conversion amongst different color representations
            - Can be initialized mutable for "tuning" by attributes, but
              then can be frozen to be immutable.  If mutable, the __hash__
              method raises an exception.
                - Once converted to immutable, it can't be changed back to
                  mutable
            - Metric attributes to determine closeness in a color space
                - Makes it easy to choose the sorting key for sorting the
                  colors in some way.
                - Even easier:  these attributes would be
                  mutually-exclusive booleans.  They would control how
                  __lt__ responds.
                - This might require a Color object container to avoid e.g.
                  having to set a class variable.  ColorDict might be nice,
                  as the keys could be color names.
        - Clr object provides 
            - ANSI escape codes for terminal output
            - Color styles as attributes
            - Name to Color conversions
                - Internal dict, so lookups are fast
                - Use standard method of reducing name for lookup (e.g.,
                  lower case, no spaces or punctuation)
                - Allow multiple dicts from UTF-8 text files
                    - '#' character indicates a comment
                    - Blank lines ignored
                    - First non-comment line contains a single character
                      defining the separation character
                    - All other lines are 'name_string sep_char
                      Color_constructor_argument
                        
TODO
 
    - Remove rgb.Color 
    - Rename ColorNum to Color
    - Color:  fundamental type to represent a 24-bit color
        - Make constructor take as wide a variety of forms as possible
            - Class method Construct() returns a Color instance if the 
              argument was recognized or returns None.  This allows for 
              fast processing of lines from text files.  See rgb/cdec.py
              for the needed regexps.
            - Color(*p)
            - Sequence of 3 numbers or bytes
                - If byte in [0, 255], use directly
                - If floats on [0, 1] convert to bytes by 
                  int(round(255*x, Color.n))
                - Otherwise convert to Decimals
                    - If on [0, 1], use as floats
                    - Otherwise normalize by dividing by largest number
                - Convert to 3 bytes for internal storage
            - Three numbers or bytes
                - Same as previous
            - Single float, fraction, or Decimal on [0, 1]:  a gray with
              black being 0 and white being 1
            - Wavelength in nm
            - 3 byte string
            - Strings:  @#$xxyyzz hex form
            - 7 characters when ''.join()'d, make a 7 byte string as
              previous
            - Another Color instance
            - kw parameters
                - rgb: bool, hsv: bool, hls: bool
                    - These three override the hex string char @#$
            - Internal representation is length 3 bytes string for RGB
              components
        - Attributes (D = floats on [0, 1], I = ints in [0, 255])
            - rgb, hsv, hls return (D, D, D)
            - RGB, HSV, HLS return (I, I, I)
            - xrgb, xhsv, xhls return hex strings
            - wl returns a wavelength in nm
            - Mutable?
                - This could be handy for adjusting colors, but if it's
                  done, then the instance is mutable and can't be a
                  dictionary key
                - Can this mutability be controlled by constructor?  Would
                  be a nice way, as if the item is made mutable, the
                  __hash__ function wouldn't work.
                - Or could be mutable attribute that could only be set to
                  False after making it true in constructor.  This would be
                  a nice feature, as __hash__ would cause an exception
                  until mutable was set to False -- and it could never be
                  set back to True.
        - Add Color.n, which contains the number of decimal digits to
            round the floats to.  Note this determines the sensitivity of
            color equality.
        - Move Color to clr.py, so all color stuff is in one file except
          for color names.
    - Clr
        - Add .on attribute.  If True, escape codes are emitted from
          __call__ and defined attributes.  Otherwise, empty strings are
          returned.  This is really a needed feature.
        - Keep because the Clr.__call__ method is convenient
        - Consider putting Color inside clr.py
        - Name to color mapping should be done by Clr
            - Add method to load data from file
                - String name, separation character, repr() of bytestring
            all arguments must be either string names or Color instances.
            Actually, if a string is used, an internal dictionary is used
            to translate it to a Color instance.
            - Clr should have a method to initialize the name to Color
                dictionary mapping.
            - The default should be something sensible.  xkcd's could
                be good, but it's 949 colors.  I like the naming scheme.
                See if it could be whittled down to a set about half the
                size.
    - Constructor
        - ColorNum(*p)
        - I should be able to use these equivalently:
            - ColorNum(b"\x01\x02\x03")
            - ColorNum([b"\x01", b"\x02", b"\x03"])
            - ColorNum("@010203")   # Not same, but gives the idea
            - ColorNum("#010203")
            - ColorNum("$010203")   # Not same, but gives the idea
            - ColorNum([1, 2, 3])
            - ColorNum((1, 2, 3))
            - ColorNum(1, 2, 3)
            - ColorNum([1., 2., 3.])
            - ColorNum((1., 2., 3.))
            - ColorNum(1., 2., 3.)
        - String
            - #xxyyzz string:  RGB hex
            - @xxyyzz string:  HSV hex
            - $xxyyzz string:  HLS hex
        - 3-tuple of floats, Decimals, or fractions
            - Used as-is if all three are on [0, 1]
            - Normalized by vector length other wise
        - 3-tuple of integers
            - Used as-is if all three are on [0, 255]
            - Normalized by vector length other wise
            

    - Wanted
        - Use colorsys functions
        - Allow decimal-tuple constructor
        - Color names
            - Name to RGB, HSV
            - RGB to nearest name(s)
        - RGB to wavelength, wavelength to RGB
        - Blackbody 
            - Color in RGB to a given T[/K]
            - T[/K] to RGB
 
    - Notation
        - x[//s] means x is a number with units string s.  The '//' means
          'divide by s to get a dimensionless number'.  For a unit like 
          'kJ/(kg*K)' which adheres to e.g. python's arithmetical
          precedence, I'll write 'kJ//kg*K' with the implicit assumption
          that there's only a numerator and one denominator.  This is of
          course incorrect syntax unless it's defined.  I used the double
          solidus to be a clue to this notation.
 
    - The color stuff I did in 2014 is in /pylib/pgm/colors
        - Look at the web_data directory.  It could be convenient to
          coalesce all the data into a single text file, maybe rgbdata.py,
          that maps color names to both RGB and HSV strings.  It would
          allow for multiple values for names.
 
    - References
        - [ford] http://poynton.ca/PDFs/coloureq.pdf "Colour Space Conversions" by
          A. Ford and A. Roberts, 11 Aug 1998.
        - [bruton] http://www.midnightkite.com/color.html
 
Color utilities
 
    This library uses the Color class to contain the RGB and HSV
    information on a color.  Internally, the color information is stored as
    two 3-byte values, one for the RGB form and one for the HSV form.  For
    the utility functions, the arguments are typically 3-tuples of floats
    on [0, 1].
 
''' 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #???copyright???# Copyright (C) 2022 Don Peterson #???copyright???#
    #???contact???# gmail.com@someonesdad1 #???contact???#
    #???license???#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #???license???#
    #???what???#
    # Color conversion utilities
    #???what???#
    #???test???# ignore #???test???#
    pass
if 1:   # Standard imports
    import colorsys
    from decimal import Decimal
    from fractions import Fraction
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    raise Exception("This file shouldn't be used")
    from clr import Clr
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()
if 1:   # Classes
    class ColorNum:
        '''Store the three numbers used to define a color; they are stored
        in canonical form of as a 3-tuple of RGB floats on [0, 1].
        Use attributes to get other forms:  HLS (hue, lightness, saturation)
        and HSV (hue, saturation, value).
        '''
        n = 3   # Number of decimal digits to round floats to
        def __init__(self, x):
            '''Initialize in various ways:
                ColorNum(x)                 x is ColorNum instance
                ColorNum(b"\x01\x02\x03")   3-byte string
                ColorNum("#abcdef")         RGB string
                ColorNum("@abcdef")         HSV string
                ColorNum("$abcdef")         HLS string
                ColorNum((0.1, 0.2, 0.3))   Tuple of floats
                ColorNum((1, 2, 3))         Tuple of integers
                ColorNum((100, 200, 3020))  Tuple of arbitrary integers
            Can be initialized with any iterable of three or more numbers;
            they will be normalized to lie on [0, 1] by dividing by the
            maximum of the three values.
            '''
            e = ValueError(f"'{x}' is of improper form for class ColorNum")
            if ii(x, ColorNum):
                self._rgb = x._rgb
            elif ii(x, bytes):
                if len(x) != 3:
                    raise e
                self._rgb = tuple([i/255 for i in x])
            elif ii(x, str):
                if len(x) != 7 or x[0] not in "@#$":
                    raise e
                # clamp to [0, 1]
                f = lambda x:  max(0, min(int(x, 16), 255))/255
                # Put into canonical float form
                try:
                    s = f(x[1:3]), f(x[3:5]), f(x[5:7])
                    if x[0] == "@":         # It's HSV
                        self._rgb = colorsys.hsv_to_rgb(*s)
                    elif x[0] == "#":       # It's RGB
                        self._rgb = s
                    elif x[0] == "$":       # It's HLS
                        self._rgb = colorsys.hls_to_rgb(*s)
                except Exception:
                    raise e
            else:
                # It must be an iterable of at least three numbers
                try:
                    y = iter(x)
                    s = next(y), next(y), next(y)
                except Exception:
                    raise e
                # They must be the same type
                t = [type(i) for i in s]
                if not all([type(i) == type(s[0]) for i in s]):
                    msg = "The components of x are not the same type"
                    raise TypeError(msg)
                # Convert them to Decimals
                was_int = False
                if ii(s[0], str):
                    u = [Decimal(i) for i in s]
                elif ii(s[0], int):
                    was_int = True
                    u = [Decimal(i) for i in s]
                elif ii(s[0], float):
                    u = [Decimal(str(i)) for i in s]
                elif ii(s[0], Fraction):
                    u = [Decimal(i.numerator)/Decimal(i.denominator) for i in s]
                elif ii(s[0], Decimal):
                    u = s
                else:
                    msg = "x is a sequence of the improper type"
                    raise TypeError(msg)
                # Take absolute values
                u = [abs(i) for i in u]
                # Normalize if needed
                if not all([0 <= i <= 1 for i in u]):
                    if was_int and all([0 <= i <= 255 for i in u]):
                        u = [i/255 for i in u]
                    else:
                        # Divide by the maximum value
                        m = max(u)
                        u = [i/m for i in u]
                assert(all([0 <= i <= 1 for i in u]))
                # Convert the numbers to floats to four places
                self._rgb = tuple([round(float(i), ColorNum.n) for i in u])
                self.sort = "hls"
        def __str__(self):
            'Show components as decimal fractions'
            r, g, b = self._rgb
            n = ColorNum.n
            return f"ColorNum({r:{2+n}.{n}f}, {g:{2+n}.{n}f}, {b:{2+n}.{n}f})"
        def __repr__(self):
            'Show components as integers on [0, 255]'
            r, g, b = self.RGB
            return f"ColorNum({r!r:3d}, {g!r:3d}, {b!r:3d})"
        def __eq__(self, other):
            'Equal if components match to 6 decimal places'
            if not ii(other, ColorNum):
                raise TypeError("'other' must be a ColorNum instance")
            n = ColorNum.n
            me  = [round(i, n) for i in self._rgb]
            you = [round(i, n) for i in other._rgb]
            return bool(me == you)
        def __lt__(self, other):
            'Compare self and other for sorting'
            if self.sort == "hls":
                return self.hsv < other.hsv
            elif self.sort == "rgb":
                return self.rgb < other.rgb
            elif self.sort == "hsv":
                return self.hls < other.hls
            elif self.sort == "wl":
                raise Exception("Not implemented yet")
                # Need to decide on algorithm
            else:
                raise ValueError("self.sort not one of 'hls rgb hsv wl'")
        def __hash__(self):
            return id(self)
        def interpolate(self, other, t, typ="rgb"):
            '''Interpolate between two colors:  self and other.  t is a
            parameter on [0, 1].  If t is 0, you'll get back self and if t
            is 1, you'll get back other.  If t is intermediate, you'll get
            a color "between" the two.  typ can be "rgb", "hsv", or "hls"
            and controls the numbers intepolated between.
            '''
            # Here's the algorithm for each component.  The starting point
            # is (x0, y0) and the ending point is (x1, y1).  We have x0 = 0
            # and x1 = 1.  The slope of the line is
            #     m = (y1 - y0)/(x1 - x0) = y1 - y0
            # Given the parameter t on [0, 1], the interpolated value along
            # the line is
            #     y = y0 + m*t
            # Example:  y0 = 1, y1 = 0, t = 0.5.  m = 0 - 1 = -1.  Thus, the
            # interpolated value is y = 1 + (-1)*0.5 = 0.5.
            if not ii(other, ColorNum):
                raise TypeError("other must be a ColorNum instance")
            if not (0 <= t <= 1):
                raise ValueError("t must be a float on [0, 1]")
            if typ not in ("rgb", "hsv", "hls"):
                raise ValueError("typ must be 'rgb', 'hsv', or 'hls'")
            # Get color space coordinates
            if typ == "rgb":
                a = self._rgb
                b = other._rgb
            elif typ == "hsv":
                a = self.hsv
                b = other.hsv
            else:
                a = self.hls
                b = other.hls
            # Interpolate in this space from a's to b's
            m = [j - i for i, j in zip(a, b)]   # Slopes
            new = [i + slope*t for i, slope in zip(a, m)]
            # They should all be on [0, 1]
            ok = all([0 <= i <= 1 for i in new])
            assert(all([0 <= i <= 1 for i in new]))
            # Convert to rgb space
            if typ == "hsv":
                new = colorsys.hsv_to_rgb(*new)
            elif typ == "hls":
                new = colorsys.hls_to_rgb(*new)
            return ColorNum(new)
        @property
        def HLS(self):  
            'Get hls in integer form'
            return tuple([int(round(i*255, 1)) for i in self.hls])
        @property
        def hls(self):
            'Get hls in float form'
            s = tuple(colorsys.rgb_to_hls(*self._rgb))
            return tuple([round(i, ColorNum.n) for i in s])
        @property
        def hlshex(self):
            'Get hls in hex string form'
            return "${0:02x}{1:02x}{2:02x}".format(*self.HLS)
        @property
        def HSV(self):
            'Get hsv in integer form'
            return tuple([int(round(i*255, 1)) for i in self.hsv])
        @property
        def hsv(self):  
            'Get hsv in float form'
            s = tuple(colorsys.rgb_to_hsv(*self._rgb))
            return tuple([round(i, ColorNum.n) for i in s])
        @property
        def hsvhex(self):
            'Get hsv in hex string form'
            return "@{0:02x}{1:02x}{2:02x}".format(*self.HSV)
        @property
        def RGB(self):
            'Get rgb in integer form'
            # The rounding step is important, as you'll see things like 79
            # get converted to 78.9990 and taking the int() will be off by
            # one unit.
            return tuple([int(round(i*255, 1)) for i in self._rgb])
        @property
        def rgb(self):
            'Get rgb in float form'
            return tuple(self._rgb)
        @property
        def rgbhex(self):
            'Get rgb in hex string form'
            return "#{0:02x}{1:02x}{2:02x}".format(*self.RGB)
    class Color:
        '''Container for a triple of RGB numbers representing a color.
        Equivalent constructor calls are:
            Color([3, 4, 5])
            Color((3, 4, 5))
            Color(x) where x is an iterator that returns 3 numbers
            Color("#030405")
            Color(b"\x03\x04\x05")
            Color((3/255, 4/255, 5/255))
            Color((0.011765, 0.015686, 0.019608))
 
        Warning:  str(Color((1, 0, 0))) is 'Color((1, 0, 0))' and
        str(Color((1.0, 0, 0))) is 'Color((255, 0, 0))'.  The number type
        of the first component is important.
 
        Internally, the color is stored as six bytes, three for the RGB
        representation and three for the HSV representation.
  
        The r, g, b attributes return integer values in [0, 255] for red,
        green, or blue.  The h, s, v attributes return integer values in
        [0, 255] for hue, saturation, and value.
        '''
        def __init__(self, x):
            e = ValueError(f"'{x}' is an incorrect color initializer")
            if ii(x, str):  # It's a string of the #xxyyzz form
                if len(x) != 7 or x[0] != "#":
                    raise e
                try:
                    r = int(x[1:3], 16)
                    g = int(x[3:5], 16)
                    b = int(x[5:7], 16)
                except Exception:
                    raise e
            else:
                # Assume it's an iterable of three numbers
                try:
                    y = iter(x)
                    a = next(y)
                    b = next(y)
                    c = next(y)
                    r, g, b = Color.Convert(a, b, c)
                except Exception:
                    raise e
            self._rgb = bytes((r, g, b))
        @classmethod
        def Convert(Color, x1, x2, x3):
            '''Convert to 3-tuple with each component on [0, 255] and of
            integer type.  x1, x2, x3 must be objects that can be
            converted to integers or floats.
            '''
            e = Exception()
            if ii(x1, int):     # Must be integers in [0, 255]
                try:
                    a = [int(i) for i in (x1, x2, x3)]
                    if not all([i >= 0 for i in a]):
                        raise e
                    if not all([i <= 255 for i in a]):
                        raise e
                    return tuple(a)
                except Exception:
                    pass
            elif ii(x1, float):   # Floats in [0, 1]
                try:
                    a = [float(i) for i in (x1, x2, x3)]
                    # Check numbers are on [0, 1]
                    if not all([i >= 0 for i in a]):
                        raise e
                    if not all([i <= 1 for i in a]):
                        raise e
                    a = [min(int(i*256), 255) for i in a]
                    return tuple(a)
                except Exception:
                    pass
            # See if we can convert to floats
            e = ValueError("Each argument must convert to a float >= 0")
            try:
                a = [float(i) for i in (x1, x2, x3)]
                mn, mx = min(a), max(a)
                if mn < 0:      # All must be >= 0
                    raise e
                if not mx:
                    return (0, 0, 0)
                # Scale to [0, 1]
                a = [i/mx for i in a]
                # Convert to integers on [0, 255]
                a = [int(i*255) for i in a]
                # Check
                if not all([i >= 0 for i in a]):
                    raise e
                if not all([i <= 255 for i in a]):
                    raise e
                return tuple(a)
            except Exception:
                raise e
        def __lt__(self, x):
            if not ii(x, Color):
                raise TypeError("x must be a Color instance")
            return self.rgb < x.rgb
        def __eq__(self, x):
            if ii(x, Color):
                return self._rgb == x._rgb
            raise TypeError("x is not a Color instance")
        def __str__(self):
            r, g, b = [i for i in self._rgb]
            return f"Color(({r:3d}, {g:3d}, {b:3d}))"
        def __repr__(self):
            return str(self)
        def __int__(self):
            'Returns an integer that uniquely maps to the RGB values'
            r, g, b = self.rgb
            return (r << 16) | (g << 8) | b
        def __hash__(self):
            return hash(self._rgb)
        def __float__(self):
            'Returns a float that uniquely maps to the HSV values'
            h, s, v = self.hsv
            return float((h << 16) | (s << 8) | v)
        @property
        def hsvhex(self):
            'Capital letters for HSV'
            s = self.hsv
            return f"{s[0]:02X}{s[1]:02X}{s[2]:02X}"
        @property
        def hex(self):
            'Lower case letters for HSV'
            s = self._rgb
            return f"{s[0]:02x}{s[1]:02x}{s[2]:02x}"
        @property
        def rgb(self):
            'Returns (red, green, blue) values on [0, 255]'
            s = self._rgb
            return (s[0], s[1], s[2])
        @property
        def hsv(self):
            'Returns (hue, saturation, value) values on [0, 255]'
            rgb = [i/255 for i in self.rgb]
            hsv = colorsys.rgb_to_hsv(*rgb)
            s = [int(i*255) for i in hsv]
            return tuple(s)
if 1:   # Core functionality
    def Visible(wavelength):
        '''Convert a wavelength in nm into a Color instance.  Adapted
        from FORTRAN code by [bruton].
        '''
        if wavelength >= 380 and wavelength <= 440:
            x = (float(-(wavelength - 440)/(440 - 380)), 0.0, 1.0)
        elif wavelength >= 440 and wavelength <= 490:
            x = (0.0, float((wavelength - 440)/(490 - 440)), 1.0)
        elif wavelength >= 490 and wavelength <= 510:
            x = (0.0, 1.0, float(-(wavelength - 510)/(510 - 490)))
        elif wavelength >= 510 and wavelength <= 580:
            x = (float((wavelength - 510)/(580 - 510)), 1.0, 0.0)
        elif wavelength >= 580 and wavelength <= 645:
            x = (1.0, -float((wavelength - 645)/(645 - 580)), 0.0)
        elif wavelength >= 645 and wavelength <= 780:
            x = (1.0, 0.0, 0.0)
        else:
            raise ValueError("wavelength must be in [380, 780] nm")
        return Color(x)
    def IsNormalized(a, b, c):
        'Raise a ValueError exception unless each number is a float on [0, 1]'
        if not all(0 <= i <= 1 and ii(i, float) for i in (a, b, c)):
            raise ValueError("Elements in tuple must be floats on [0, 1]")

if __name__ == "__main__":
    from lwtest import run, raises, Assert, assert_equal
    from collections import deque
    def TestConvert():
        # Test with integers
        x = Color.Convert(0, 0, 0)
        Assert(ii(x, tuple) and x == (0, 0, 0))
        for a in (0, 1, 2, 254, 255):
            x = Color.Convert(a, 0, 0)
            Assert(ii(x, tuple) and x == (a, 0, 0))
            x = Color.Convert(0, a, 0)
            Assert(ii(x, tuple) and x == (0, a, 0))
            x = Color.Convert(0, 0, a)
            Assert(ii(x, tuple) and x == (0, 0, a))
        x = Color.Convert(256, 0, 0)
        Assert(x == (255, 0, 0))
        x = Color.Convert(2000, 2000, 0)
        Assert(x == (255, 255, 0))
        x = Color.Convert(2000, 2000, 2000)
        Assert(x == (255, 255, 255))
        raises(ValueError, Color.Convert, -1, 0, 0)
        raises(ValueError, Color.Convert, 0, -1, 0)
        raises(ValueError, Color.Convert, 0, 0, -1)
        # Test with floats
        for a in (0.0, 1.0, 2.0, 254.0, 255.0):
            b = int(a)
            x = Color.Convert(b, 0, 0)
            Assert(ii(x, tuple) and x == (b, 0, 0))
            x = Color.Convert(0, b, 0)
            Assert(ii(x, tuple) and x == (0, b, 0))
            x = Color.Convert(0, 0, b)
            Assert(ii(x, tuple) and x == (0, 0, b))
        x = Color.Convert(256, 0, 0)
        Assert(x == (255.0, 0, 0))
        x = Color.Convert(2000.0, 2000.0, 0)
        Assert(x == (255, 255, 0))
        x = Color.Convert(2000, 2000.0, 2000.0)
        Assert(x == (255, 255, 255))
        raises(ValueError, Color.Convert, -1, 0, 0)
        raises(ValueError, Color.Convert, 0, -1, 0)
        raises(ValueError, Color.Convert, 0, 0, -1)
    def TestColorConstructor():
        ref = Color((3, 4, 5))
        for i in [
            [3, 4, 5], 
            (3, 4, 5), 
            b"\x03\x04\x05",
            "#030405",
            (3/255, 4/255, 5/255),
            (0.011765, 0.015686, 0.019608),
            deque((3, 4, 5))
        ]:
            Assert(Color(i) == ref)
        raises(ValueError, Color, (-1, 0, 0))
        raises(ValueError, Color, (0, -1, 0))
        raises(ValueError, Color, (0, 0, -1))
        raises(ValueError, Color, "#0g0000")
        raises(ValueError, Color, "#000g00")
        raises(ValueError, Color, "#00000g")
    def TestColorNumConstructor():
        D, F = Decimal, Fraction
        for x in (0, 1, "0.5"):
            std = ColorNum((x, x, x))
            if x == 1:
                a = ColorNum((0.9999999, 1.0000001, 1.0))   # Check rounding
                assert_equal(a == std, True)
            if x == "0.5":
                d, f = D(x), F(1, 2)
            elif x == 0:
                d, f = D(x), F(0, 1)
            else:
                d, f = D(x), F(x, x)
            b = ColorNum((d, d, d))
            c = ColorNum((f, f, f))
            i = ColorNum((x, x, x))
            t = x if ii(x, str) else str(x)
            s = ColorNum((t, t, t))
            for j in (b, c, i, s):
                if j != std: xx() #xx
                assert_equal(j == std, True)
        # Check bytes
        x = 1.0
        std = ColorNum((x, x, x))
        a = ColorNum(b"\xff\xff\xff")
        assert_equal(a == std, True)
        # Check normalization
        x = 7.348
        s = ColorNum((x, x, x))
        std = ColorNum((1, 1, 1))
        assert_equal(s == std, True)
        a, b, c = 4.377, -89.009, 12.2
        s = ColorNum((a, b, c))
        m = max(a, b, c)
        t = ColorNum((a/m, b/m, c/m))
        assert_equal(s == t, True)
        # Bad forms
        raises(TypeError, ColorNum, ["4", 4, 4])
        raises(TypeError, ColorNum, [D("4"), 4, 4])
        raises(TypeError, ColorNum, [4.0, 4, 4])
        raises(TypeError, ColorNum, [F(4, 1), 4, 4])
        raises(ValueError, ColorNum, "#0000000")
        raises(ValueError, ColorNum, "#00000g")
        raises(ValueError, ColorNum, "@00000g")
        raises(ValueError, ColorNum, "$00000g")
        raises(ValueError, ColorNum, b"xxxx")
    def TestColorNumInterpolate():
        a = ColorNum((0, 0, 0))
        b = ColorNum((1, 1, 1))
        new = a.interpolate(b, 1/2, typ="rgb")
        assert_equal(new, ColorNum((1/2, 1/2, 1/2)))
        new = a.interpolate(b, 1/2, typ="hsv")
        assert_equal(new, ColorNum((1/2, 1/2, 1/2)))
        new = a.interpolate(b, 1/2, typ="hls")
        assert_equal(new, ColorNum((1/2, 1/2, 1/2)))
        from frange import frange
        for i in frange("0", "1", "0.1"):
            pass
    def TestColorNumProperties():
        x = ColorNum((1, 1, 1))
        # Canonical floating point form
        assert_equal(x.rgb, (1.0, 1.0, 1.0))
        assert_equal(x.hls, (0.0, 1.0, 0.0))
        assert_equal(x.hsv, (0.0, 0.0, 1.0))
        # Integer form
        assert_equal(x.RGB, (255, 255, 255))
        assert_equal(x.HLS, (  0, 255,   0))
        assert_equal(x.HSV, (  0,   0, 255))
        # String form
        assert_equal(x.rgbhex, "#ffffff")
        assert_equal(x.hlshex, "$00ff00")
        assert_equal(x.hsvhex, "@0000ff")

    exit(run(globals(), halt=True)[0])
