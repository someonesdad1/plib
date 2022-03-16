'''
 
TODO
 
    - Definition of a color
        - Store internally as bytestring of length 3.
        - RGB or HSV
            - 3 numbers (r, g, b), normalized to (r/x, g/x, b/x) where x is
              max(r, g, b).  Then converted to bytes form.
        - #xxyyzz string:  standard RGB hex form used on web
        - ##xxyyzz string:  HSV hex form

    - Wanted
        - RGB to HSV
        - HSV to RGB
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
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Color conversion utilities
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Standard imports
    import colorsys
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from clr import Clr
    if len(sys.argv) > 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()
if 1:   # Classes
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
        def __eq__(self, x):
            if ii(x, Color):
                return self._rgb == x._rgb
            raise TypeError("x is not a Color instance")
        def __str__(self):
            r, g, b = [i for i in self._rgb]
            return f"Color(({r}, {g}, {b}))"
        def __repr__(self):
            return str(self)
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
    exit(run(globals(), halt=True)[0])
