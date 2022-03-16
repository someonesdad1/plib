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
        - x[/s] means x is a number with units string s.  The '/' means
          'divide by s to get a dimensionless number'.  For a unit like 
          'kJ/(kg*K)' which adheres to e.g. python's arithmetical
          precedence, I'll write 'kJ//kg*K' with the implicit assumption
          that there's only a numerator and one denominator.  This is of
          course incorrect syntax unless it's defined.  I used the double
          solidus to be a clue to this notation.
        - Hex notation:  #xxyyzz for RGB, ##xxyyzz for HSV
        - Shorter but probably adequate
            - Float:  0.xxyyzz using decimal digits
            - Integer:  xxyyzz using decimal digits
        - Single number
            - Integer:  24-bit
            - Float:  0.xxxyyyzzz

    - All the color stuff I did in 2014 is in /pylib/pgm/colors
        - Look at the web_data directory.  It could be convenient to
          coalesce all the data into a single text file, maybe rgbdata.py,
          that maps color names to both RGB and HSV strings.  It would
          allow for multiple values for names.

    - Is 3seq of integers or floats best?  On reflection, integers are
      probably best because of speed and 24-bit color is better than almost
      anything we can do.

    - References
        - http://www.poynton.com/PDFs/coloureq.pdf
        - http://www.midnightkite.com/color.html

Color utilities

    In this library, colors are represented as 3-tuples of floating point
    numbers, each on the closed interval of [0, 1].  These are either RGB
    tuples (red-green-blue) or HSV tuples (hue-saturation-value).  They can
    also be tuples of integers; if they are, the integers must be on [0,
    255].

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
    import getopt
    import os
    import pathlib
    import sys
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import wrap, dedent
    from f import flt
    from clr import Clr
    if 1:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    c = Clr()
if 1:   # Classes
    class Color:
        def __init__(self, x):
            if ii(x, str):  # It's a string of the #xxyyzz form
                e = ValueError(f"'{x}' is an incorrect color string")
                if len(x) != 7:
                    raise e
                if x[0] != "#":
                    raise e
                try:
                    r = int(x[1:3], 16)
                    g = int(x[3:5], 16)
                    b = int(x[5:7], 16)
                except Exception:
                    raise e
            elif ii(x, (list, tuple)):  # Sequence
                e = ValueError(f"'{x}' is an incorrect color sequence")
                try:
                    r, g, b = x[0], x[1], x[2]
                    # They must be numbers
                    r, g, b = [float(i) for i in (r, g, b)]
                    m = max(r, g, b)
                    # Scale to [0, 1]
                    r, g, b = [i/m for i in (r, g, b)]
                    # Convert to integers on [0, 255]
                    r, g, b = [int(i*255) for i in (r, g, b)]
                    # Check
                    if not all([i >= 0 for i in (r, g, b)]):
                        raise Exception()
                    if not all([i <= 255 for i in (r, g, b)]):
                        raise Exception()
                except Exception:
                    raise e
        @classmethod
        def Normalize(Color, x1, x2, x3):
            '''Convert to 3-tuple with each component on [0, 255] and of
            integer value.  x1, x2, x3 must be objects that can be
            converted to integers or floats.
            '''
            # See if we can convert to integers on [0, 255]
            try:
                a = [int(i) for i in (x1, x2, x3)]
                # Check numbers are on [0, 255]
                if not all([i >= 0 for i in a]):
                    raise Exception()
                if not all([i <= 255 for i in a]):
                    raise Exception()
                return tuple(a)
            except Exception:
                pass
            # See if we can convert to floats
            e = ValueError("Each argument must convert to a float >= 0")
            try:
                a = [float(i) for i in (x1, x2, x3)]
                mi, mx = min(a), max(a)
                if mi < 0:
                    raise Exception()
                if mx:
                    # Scale to [0, 1]
                    a = [i/mx for i in a]
                    # Convert to integers on [0, 255]
                    a = [int(i*255) for i in a]
                    # Check
                    if not all([i >= 0 for i in a]):
                        raise Exception()
                    if not all([i <= 255 for i in a]):
                        raise Exception()
                    return tuple(a)
                else:
                    return (0, 0, 0)
            except Exception:
                raise e

if 1:   # Core functionality
    def hsv2rgb(h, s, v):
        '''Convert an HSV tuple to RGB.
        '''
        from math import floor
        if H < 0 or H > 1:
            raise Exception("Hue must be between 0 and 1")
        if S < 0 or S > 1:
            raise Exception("Saturation must be between 0 and 1")
        if V < 0 or V > 1:
            raise Exception("Value must be between 0 and 1")
        Hex = H*6.  # Algorithm wants H in degrees, then divides by 60
        primary_color = floor(Hex)
        secondary_color = Hex - primary_color
        a = (1-S)*V
        b = (1-(S*secondary_color))*V
        c = (1-(S*(1-secondary_color)))*V
        if primary_color == 0 or primary_color == 6:
            self.r, self.g, self.b = (V, c, a)
        elif primary_color == 1:
            self.r, self.g, self.b = (b, V, a)
        elif primary_color == 2:
            self.r, self.g, self.b = (a, V, c)
        elif primary_color == 3:
            self.r, self.g, self.b = (a, b, V)
        elif primary_color == 4:
            self.r, self.g, self.b = (c, a, V)
        elif primary_color == 5:
            self.r, self.g, self.b = (V, a, b)
        else:
            raise Exception("Internal error:  unexpected value of primary_color")
        self.color = (self.r, self.g, self.b)

if __name__ == "__main__":
    from lwtest import run, raises, Assert, assert_equal
    def TestNormalize():
        x = Color.Normalize(0, 0, 0)
        Assert(ii(x, tuple) and x == (0, 0, 0))
        for a in (0, 1, 2, 254, 255):
            x = Color.Normalize(a, 0, 0)
            Assert(ii(x, tuple) and x == (a, 0, 0))
            x = Color.Normalize(0, a, 0)
            Assert(ii(x, tuple) and x == (0, a, 0))
            x = Color.Normalize(0, 0, a)
            Assert(ii(x, tuple) and x == (0, 0, a))
        x = Color.Normalize(256, 0, 0)
        Assert(x == (255, 0, 0))
        x = Color.Normalize(2000, 2000, 0)
        Assert(x == (255, 255, 0))
        x = Color.Normalize(2000, 2000, 2000)
        Assert(x == (255, 255, 255))
        raises(ValueError, Color.Normalize, -1, 0, 0)
    exit(run(globals(), halt=True)[0])
