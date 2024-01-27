''' 
- Bugs
    - RegexpDecorate.register() needs to change to an argument list of 
      (r, match_style, nomatch_style) where the latter two elements are
      escape codes used to define how things should be printed.  The use
      case is pfind.py where I want to see directories printed in red with
      the sky color for the match; plain files are printed with the default
      text style but matches with sky.  Thus, the default for nomatch_style
      should be None, meaning the default text style.
    - TRM attributes should be "" if .on is False
        - This needs __getattr__ and __setattr__
        - .on can have three states
            - None means to use stdout.isatty()
            - False means always off so all t.x attributes are ""
            - True means always on so all t.x attributes are proper escape
              codes
        - Could change to methods:  on(), off(), none().
    - TestInvariants() is made to pass, but I'd like to see the conversion
      work exactly.  It could be a problem with decimal roundoff in the
      colorsys module.

Classes to help with color use in terminals
    - class Color
        - Immutable class to store the three numbers used to define a color
    - class Trm
        - Outputs ANSI escape sequences to allow color use in a terminal
    - class ColorName
        - Maps string names to a Color object

    - Typical usage

        from color import Color, Trm

        t = Trm()
        print(f"{t('redl')}Error:  you need to fix this{t.n}")
        print(f"{t('lblu', 'wht'} This is blue text in a white background")

        # The default color names are based on the resistor color code
        # names.  Prefix with 'l' for the lighter colors, 'd' for darker,
        # and 'b' for light pastel background colors.  Run the color.py
        # file as a script to see these color names and how they render on
        # your screen.

        # The Trm instance can be called with a foreground and background
        # color (either a name or Color instance) and an optional attribute
        # (e.g., for italics).  The t.n value means to return to the
        # default color.  You can store escape sequences as attributes:

        t.err = t("redl")
        print(f"{t.err}Error:  you need to fix this{t.n}")

        # You can use t.out and t.print to avoid having to reset to the
        # default color.  t.out is the same as t.print but without the
        # newline.
 
    - This file includes some deprecated functionality to support an older
      python module I used for a couple of decades.  Over time, I expect to
      remove the dependencies on this stuff and it will eventually be
      removed with no warning (i.e., don't use these older features).  To
      disable the legacy code support, define the 'klr' environment
      variable to be empty (evaluate False as a boolean).
 
    - class Color
        - This immutable class is used to store the three integers that
          define a color.  You can set the number of bits to use to store
          these integers using the class variable Color.bits_per_color,
          which defaults to 8.
        - The Color constructor has a number of ways to instantiate a
          color:
            - One argument
                - A short string name for a color (these are actually
                  handled by the global ColorNum instance CN).
                - Hex strings
                    - '@abcdef' means an HSV hex string
                    - '#abcdef' means an RGB hex string
                    - '$abcdef' means an HLS hex string
                - Another Color instance:  a copy is made
                - A decimal number on [0, 1] defining a gray with white
                  being 1.
            - Three arguments 
                - Color(1, 2, 3)
                - Color(0.1, 0.2, 0.3)
                - Can use boolean keywords "hsv" or "hls" to not use the
                  default rgb space.
        - Helpful functionality
            - Construct(x)
                - This class method returns a Color instance if the string
                  argument x contains a recognizable color initializer (hex
                  string or 3-sequence of numbers).  If x was a multiline
                  string with one or more valid color initializers, a deque
                  of (a, c) objects is returned with a the line's string
                  and c the Color instance.  This is handy for e.g.
                  colorizing a set of lines in a file of color specifiers
                  such as an X11 rgb.txt file.
        - Distance between two colors
            - RGB, HSV, HLS known to be nonlinear wrt perception
            - https://www.compuphase.com/cmetric.htm gives a practical
              formula he says is close to L*u*v* space with modified
              lightness curve (it's a weighted Euclidean distance in RGB
              space).   Let two colors be specified by (R1, G1, B1) and
              (R2, G2, B2) where each component is an int on [0, 255].
              Then
                - r = (R1 + R2)/2
                - dX = X1 - X2
                - d**2 = (2 + r/256)*dR**2 + 4*dG**2 + (2 + (255 -
                  r)/256)*dB**2 
 
    References
        - http://color.lukas-stratmann.com/  Nice web pages to help
          visualize a few color coordinate systems.
 
''' 
if 1:   # Header
    # Copyright, license
    if 1:
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # The Color class is used to hold the definition of a color.
        #∞what∞#
        #∞test∞# --test #∞test∞#
        pass
    # Standard imports
    if 1:
        import colorsys
        from decimal import Decimal
        from fractions import Fraction
        import math
        import os
        import re
        import sys
        from pathlib import Path as P
        from collections.abc import Iterable
        from collections import deque
        from string import hexdigits
    # Custom imports
    if 1:
        from wsl import wsl
        from wrap import wrap, dedent
        # Don't use flt for now until import dependencies fixed
        #from f import flt
        flt = float
        # NOTE:  can't use debug.py because of circular import
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    # Global variables
    if 1:
        ii = isinstance
        # This is commented out until I get rid of the legacy klr stuff
        #__all__ = "Color Trm TRM t ColorName CN RegexpDecorate".split()
class Color:
    'Storage of the three numbers used to define a color'
    bits_per_color = 8
    def __init__(self, *p, **kw):
        'Initialize the Color object'
        # Check for proper keyword arguments
        allowed = set("bpc hsv hls sunlight gamma".split())
        actual = set(kw.keys())
        if not (actual <= allowed):
            bad = actual - allowed
            s = ', '.join(bad)
            msg = f"Bad keyword(s):  {s}"
            raise ValueError(msg)
        # Set attributes
        self._bpc = kw.get("bpc", Color.bits_per_color)
        self._rgb = None
        self._sort = "rgb"
        if len(p) == 3:
            # Check type
            t1 = type(p[0])
            if type(p[1]) != t1 or type(p[2]) != t1:
                msg = f"'{p}' components are not all the same type"
                raise TypeError(msg)
            if all(ii(i, int) for i in p):  # 3 integers
                rgb = tuple(i & self.n for i in p)
            else:   # Convert to floats
                try:
                    dec = tuple(float(i) for i in p)
                except Exception:
                    msg = f"'{p}' couldn't be converted to floats"
                    raise TypeError(msg)
                if not all(0 <= i <= 1 for i in dec):   # Need normalization
                    mag = sum(i*i for i in dec)**(1/2)
                    dec = tuple(i/mag for i in dec)
                rgb = tuple(int(round(i*self.n, 1)) for i in dec)
            self._rgb = rgb
            # Handle 'hsv' and 'hls' keywords
            if kw.get("hsv", False):
                dec = colorsys.hsv_to_rgb(*self.drgb)
                self._rgb = tuple(int(round(i*self.n)) for i in dec)
            elif kw.get("hls", False):
                dec = colorsys.hls_to_rgb(*self.drgb)
                self._rgb = tuple(int(round(i*self.n)) for i in dec)
        elif len(p) == 1:
            x = p[0]
            if ii(x, Color):
                # Copy the state
                self._bpc = x._bpc
                self._rgb = x._rgb
                self._sort = x._sort
            elif ii(x, (int, float)):
                if 0 <= x <= 1:
                    # Interpret as a gray
                    self._rgb = tuple(int(round(i*self.n, 1)) for i in (x, x, x))
                else:
                    # Interpret as a light wavelength in nm
                    sunlight = kw.get("sunlight", True)
                    gamma = kw.get("gamma", 0.0)
                    c = Color.wl2rgb(x, sunlight=sunlight, gamma=gamma, bpc=self._bpc)
                    self._rgb = c.irgb
            else:
                # Hex string or short color name
                self._rgb = self.string(x)
        self._check()
    def _check(self):
        'Check invariants'
        assert(ii(self._bpc, int) and self._bpc > 0)
        assert(len(self._rgb) == 3)
        assert(0 <= i < self.N and ii(i, int) for i in self._rgb)
        assert(self._sort in ("rgb", "hsv", "hls"))
    def string(self, X):
        'Return 3-tuple int rgb value from a string'
        assert(ii(X, str))
        if not X:
            raise ValueError("Can't initialize with an empty string")
        x, N = X.lower(), self.N - 1
        first_char, s = x[0], x[1:]
        if first_char in "@#$":
            # It must be a hex string form.  '@' means HSV,
            # '#' means RGB, '$' means HLS.
            n, rem = divmod(len(s), 6)
            if not s or rem:
                raise ValueError(f"Hex string length must be a multiple of 6 characters")
            n *= 2
            t = s[0:n], s[n:2*n], s[2*n:3*n]
            rgb = tuple(int(i, 16) & N for i in t)
            dec = tuple(i/N for i in rgb)
            if first_char == "@":
                rgbdec = colorsys.hsv_to_rgb(*dec)
            elif first_char == "#":
                rgbdec = dec
            elif first_char == "$":
                rgbdec = colorsys.hls_to_rgb(*dec)
            else:
                raise ValueError(f"'{first_char}' is an illegal first character")
            rgb = tuple(int(round(i*N, 1)) for i in rgbdec)
        else:
            # It names an elementary color.  Use the module's default CN
            # instance to decode this.
            try:
                rgb = CN[x].irgb
            except Exception:
                raise ValueError(f"'{x}' isn't recognized as a color name")
        assert(all(0 <= i <= N and ii(i, int) for i in rgb))
        return rgb
    def __str__(self):
        u = "⁰¹²³⁴⁵⁶⁷⁸⁹"
        b = ''.join(u[int(i)] for i in str(self._bpc))
        n, w = self._rgb, len(str(self.n))
        return f"C{b}({n[0]:{w}d}, {n[1]:{w}d}, {n[2]:{w}d})"
    def __repr__(self):
        n, w = self._rgb, len(str(self.n))
        return f"Color({n[0]:{w}d}, {n[1]:{w}d}, {n[2]:{w}d}, bpc={self._bpc})"
    def _str(self, dec=True):
        'Return string representations'
        name, n = type(self).__name__, self.digits()
        if dec:
            r, g, b = self.rgb
            return f"{name}({r:{2+n}.{n}f}, {g:{2+n}.{n}f}, {b:{2+n}.{n}f})"
        else:
            s = self.fmt_int(*self._rgb)
            return f"{name}({s})"
    def __eq__(self, other):
        'Two instances are equal if their RGB components are equal'
        # This embraces a subtle but crucial point in defining the
        # fractions used for comparisons (the Fraction objects are used in
        # the change_bpc method):  the denominator is 2**self._bpc.
        # This lets color integers be "downshifted" (scaled) to lower bits
        # per color values and compare equally to hier bpc colors.  
        bpc = min(self.bpc, other.bpc)
        me, you = self.irgb, other.irgb
        if bpc != self.bpc:
            me = self.change_bpc(bpc).irgb
        if bpc != other.bpc:
            you = other.change_bpc(bpc).irgb
        return me == you
    def __lt__(self, other):
        'Compare self and other for e.g. sorting'
        if self.sort == "hls":
            return self.ihls < other.ihls
        elif self.sort == "rgb":
            return self.irgb < other.irgb
        elif self.sort == "hsv":
            return self.ihsv < other.ihsv
        elif self.sort == "wl":
            # Wavelength sorting might be handy, but I first need to
            # develop suitable inverses for the two approximation
            # functions I have.
            raise Exception("Not implemented yet")
        else:
            raise ValueError("self.sort not one of 'hls rgb hsv wl'")
    def __hash__(self):
        '''The hash includes the RGB components along with the number
        of bits per color.  This ensures that two colors initialized with 
        Color(1, 2, 3) are different if they have different bits per color.
        '''
        return hash((self._rgb, self._bpc))
    def change_bpc(self, bpc):
        '''Return a new instance with this instance's color that has the
        indicated bpc (bits per color).
        '''
        if not ii(bpc, int) and bpc < 1:
            raise TypeError("bpc must be an int")
        if bpc < 1:
            raise ValueError("bpc must be > 0")
        # Method:  convert RGB components to Fraction objects with our
        # current bpc value.  Convert these components to the new bpc value
        # using Fraction.limit_denominator.
        frgb, n = [Fraction(i, self.N) for i in self._rgb], 2**bpc
        for i, x in enumerate(frgb):
            x.limit_denominator(n)
            if x == 1:
                # Need to adjust the 1's because we want integers on 
                # [0, 2**bpc)
                x = Fraction(x.numerator - 1, x.denominator)
            frgb[i] = x
        rgb = [int(n*i) for i in frgb]
        return Color(*rgb, bpc=bpc)
    def adjust(self, p, comp=None, set=False):
        '''Allows adjusting a color and returns a new Color instance.  comp
        must be a letter in "rgbhsvHLS".  Note "saturation" s and S are
        different numbers in HSV and HLS spaces.
 
        p is a number.  If set is False, the new value will be old*(1 + p/100).
        The new number will be clamped to the range of the Color instance.
 
        If set is True, then p is converted to an integer and that
        component's value is set.
        '''
        def Clamp(x):
            'Round and limit x to [0, self.n]'
            y = int(round(x, 1))
            return min(self.n, max(0, y))
        allowed = "rgbhsvHLS"
        if set:
            if not ii(p, int):
                raise TypeError("p must be an integer if set is True")
            x = Clamp(p)
        else:
            try:
                x = 1 + float(p)/100
            except Exception:
                raise TypeError("p must be convertible to a float")
        if comp is None or comp not in allowed:
            raise ValueError(f"comp must be letter in '{allowed}'")
        # Get components to modify
        if comp in "rgb":
            r, g, b = self._rgb
            if comp == "r":
                r = x if set else Clamp(r*x)
            elif comp == "g":
                g = x if set else Clamp(g*x)
            else:
                b = x if set else Clamp(b*x)
            rgb = (r, g, b)
        elif comp in "hsv":
            h, s, v = self.ihsv
            if comp == "h":
                h = x if set else Clamp(h*x)
            elif comp == "g":
                s = x if set else Clamp(s*x)
            else:
                v = x if set else Clamp(v*x)
            rgb = Color(h, s, v, hsv=True)._rgb
        elif comp in "HLS":
            h, l, s = self.ihls
            if comp == "h":
                h = x if set else Clamp(h*x)
            elif comp == "l":
                L = x if set else Clamp(l*x)
            else:
                s = x if set else Clamp(s*x)
            rgb = Color(h, L, s, hls=True)._rgb
        # Make a copy of our instance
        c = Color(self)
        c._rgb = rgb
        return c
    def convert(self, bpc):
        '''Convert this color into an 'equivalent' Color object with a
        different number of bits per color bpc.  This is done by converting
        the RGB values to decimal, then converting the decimals back to 
        [0, 2**bpc - 1].
        '''
        if not ii(bpc, int) or bpc < 1:
            raise TypeError("bpc must be an integer")
        if bpc < 1:
            raise ValueError("bpc must be > 0")
        N = 2**bpc - 1  # Integers for new color are on [0, N]
        newrgb = tuple(int(round(i*N, 1)) for i in self.rgb)
        return Color(*newrgb)
    def interpolate(self, other, t, space="rgb"):
        '''Interpolate between two colors:  self and other.  t is a
        parameter on [0, 1].  If t is 0, you'll get back self and if t
        is 1, you'll get back other.  If t is intermediate, you'll get
        a color "between" the two.  space can be "rgb", "hsv", or "hls"
        and picks the coordinates used to interpolate.
        '''
        '''
        The algorithm is linear interpolation in 2D Cartesian
        coordinates (x, y) for each color component.  Let the starting
        point be P = (x0, y0) and the ending point be Q = (x1, y1).
        Further, let x0 = 0 and x1 = 1.
 
        The slope of the line connecting P and Q is 
            m = (y1 - y0)/(x1 - x0) = y1 - y0
 
        Given the parameter t on [0, 1], the interpolated value along
        the line between P and Q is R = (t, y0 + m*t).  For t = 0, you
        get R == P and for t = 1 you get R == Q.
        '''
        if not ii(other, Color):
            raise TypeError("other must be a Color instance")
        if not (0 <= t <= 1):
            raise ValueError("t must be on [0, 1]")
        if space not in ("rgb", "hsv", "hls"):
            raise ValueError("space must be 'rgb', 'hsv', or 'hls'")
        # Use Color instances that have the same number of bits per color.
        me, you = Color.downshift(self, other)
        # Get color space coordinates in decimal.  The vectors P and Q will be
        # 3-vectors and have components on [0, 1].
        if space == "rgb":
            P, Q = me.drgb, you.drgb
        elif space == "hsv":
            P, Q = me.dhsv, you.dhsv
        else:
            P, Q = me.dhls, you.dhls
        # Interpolate in this space from P to Q.  Set R as the intermediate
        # 3-vector between P and Q.
        m = [j - i for i, j in zip(P, Q)]   # 3-vector of slopes
        R = [i + slope*t for i, slope in zip(P, m)]
        # Convert the coordinates of R back to rgb space
        if space == "hsv":
            R = colorsys.hsv_to_rgb(*R)
        elif space == "hls":
            R = colorsys.hls_to_rgb(*R)
        rgb = self.dec_to_int(R)
        return Color(*rgb, bpc=me.bpc)
    if 1:   # Utility
        def fmt_int(self, a, b, c):
            '''Format with uniform spacing for integers.  Example:
            self.fmt_int(1, 23, 214) will return '  1,  23, 21'.  This is
            handy for making lists of color numbers because the spacing
            makes them easier to read in a text file.
            '''
            if not all(ii(i, int) for i in (a, b, c)):
                raise TypeError("Arguments must be integers")
            w = len(str(self.N))
            return f"{a:{w}d}, {b:{w}d}, {c:{w}d}"
        def dec_to_int(self, three_tuple):
            'Return int value of decimal values in 3-tuple of floats'
            assert(all(ii(i, float) for i in three_tuple))
            return tuple(int(round(i*self.n, 1)) for i in three_tuple)
        def int_to_dec(self, three_tuple):
            'Return float value of 3-tuple of integers'
            assert(all(ii(i, int) for i in three_tuple))
            return tuple(i/(self.N - 1) for i in three_tuple)
        def digits(self):
            '''Return number of digits for to use for decimal rounding,
            typically for printing to the screen.  Choose enough digits 
            to hold all the color values.
            '''
            # self.N + 1 is the number of distinct color components.
            n = math.ceil(math.log10(self.N + 1))
            return max(1, n)
    if 1:   # Settable properties
        @property
        def sort(self):
            'Return sorting order string'
            return self._sort
        @sort.setter
        def sort(self, value):
            'Set sorting method:  "rgb", "hsv", or "hsl"'
            if value not in "rgb hsv hsl".split():
                raise ValueError("value must be 'rgb', 'hsv', or 'hsl'")
            self._sort = value
    if 1:   # Read-only properties
        @property
        def sr(self):
            'Return short string form for RGB'
            a, b, c = self._rgb
            o = 0x100
            return f"R{chr(o + a)}{chr(o + b)}{chr(o + c)}"
        @property
        def sh(self):
            'Return short string form for HSV'
            a, b, c = self.ihsv
            o = 0x100
            return f"H{chr(o + a)}{chr(o + b)}{chr(o + c)}"
        @property
        def sl(self):
            'Return short string form for HLS'
            a, b, c = self.ihls
            o = 0x100
            return f"L{chr(o + a)}{chr(o + b)}{chr(o + c)}"
        @property
        def N(self):
            return 2**self._bpc
        @property
        def n(self):
            return self.N - 1
        @property
        def bpc(self):
            return self._bpc
        @property
        def hex_bytes_per_color(self):
            'How many bytes needed to express a color in hex'
            return math.ceil(self._bpc/8) + 1
        #
        @property
        def irgb(self):
            'Get rgb as a 3-tuple of integers on [0, 2**self.N - 1]'
            return self._rgb
        @property
        def drgb(self):
            'Get rgb as a 3-tuple of floats on [0, 1]'
            return tuple(i/(self.N - 1) for i in self._rgb)
        @property
        def xrgb(self):
            'Get rgb as a hex string of the form #000000'
            return "#" + Color.int_to_hex(self._rgb)
        #
        @property
        def ihsv(self):
            'Get hsv as a 3-tuple of integers on [0, 2**self.N - 1]'
            dec = colorsys.rgb_to_hsv(*self.drgb)
            hsv = tuple(int(round(i*(self.N - 1), 1)) for i in dec)
            return hsv
        @property
        def dhsv(self):
            'Get hsv as a 3-tuple of floats on [0, 1]'
            return colorsys.rgb_to_hsv(*self.drgb)
        @property
        def xhsv(self):
            'Get hsv as a hex string of the form @000000'
            return "@" + Color.int_to_hex(self.ihsv)
        #
        @property
        def ihls(self):
            'Get hls as a 3-tuple of integers on [0, 2**self.N - 1]'
            dec = self.drgb
            hlsdec = colorsys.rgb_to_hls(*dec)
            hls = tuple(int(round(i*(self.N - 1), 1)) for i in hlsdec)
            return hls
        @property
        def dhls(self):
            'Get hls as a 3-tuple of floats on [0, 1]'
            return colorsys.rgb_to_hls(*self.drgb)
        @property
        def xhls(self):
            'Get hls as a hex string of the form $000000'
            return "$" + Color.int_to_hex(self.ihls)
    if 1:   # Class methods
        @classmethod
        def dist(cls, c1, c2, space="rgb", taxicab=False):
            '''Calculate a distance between two color instances.  They are
            both converted into Color objects with the same bpc and the
            Euclidean distance between the components is calculated.  The
            number returned is a float on [0, 1].
 
            Euclidean distances in these color spaces are known to be
            nonlinear with respect to human perception, but they are easy
            to calculate.
 
            space can be "rgb", "hsv", or "hls".
 
            If taxicab is True, then use the "taxicab" distance, which is how
            you'd e.g. calculate a walking distance in a city where you can
            only walk on the sidewalks (i.e., it's the sum of the absolute
            value of the coordinates' differences).
 
            Example:  The Euclidean distance between (Color(0, 0, 0) and
            Color(a, a, a) where a = 2**bpc - 1 will be sqrt(3).
            Thus, the Euclidean distance is divided by
            sqrt(3) to get a float on [0, 1].  For taxicab distance, the
            distance is normalized to [0, 1] by dividing by 3.
            '''
            if not ii(c1, Color) or not ii(c2, Color):
                raise TypeError("c1 and c2 must be Color instances")
            # Convert to same bpc
            me, him = Color.downshift(c1, c2)
            # Get decimal components
            if space == "rgb":
                me, him = me.drgb, him.drgb
            elif space == "hsv":
                me, him = me.dhsv, him.dhsv
            elif space == "hls":
                me, him = me.dhls, him.dhls
            if taxicab:
                d = sum(abs(i - j) for i, j in zip(me, him))
                return d/3
            else:
                d = sum((i - j)**2 for i, j in zip(me, him))**(1/2)
                return d/3**(1/2)
        @classmethod
        def downshift(cls, c1, c2):
            'Return two Color instances with the same bpc'
            if not ii(c1, Color) or not ii(c2, Color):
                raise TypeError("c1 and c2 need to be Color instances")
            bpc = min(c1.bpc, c2.bpc)
            return (c1.change_bpc(bpc), c2.change_bpc(bpc))
        @classmethod
        def int_to_hex(cls, s, bytes_per_color=1):
            'Convert 3-tuple of integers to hex string'
            e = TypeError(f"'{s}' argument must be a 3-sequence of  integers")
            if not all(ii(i, int) for i in s) or len(s) != 3:
                raise e
            w = 2*bytes_per_color
            x = [f"{i:0{w}x}" for i in s]
            ml = max(len(i) for i in x)
            if ml % 2:
                ml += 1
            for i, value in enumerate(x):
                while len(value) < ml:
                    value = "0" + value
                x[i] = value
            t = ''.join(x)
            assert((len(t) % 6) == 0)
            return t
        @classmethod
        def hex_to_int(cls, s):
            '''s must be a multiple of six hex digits; return a tuple of the
            three integers it represents.
            '''
            if not ii(s, str):
                raise TypeError(f"'{s}' argument must be a string")
            div, rem = divmod(len(s), 6)
            if rem:
                raise ValueError("Length of s must be a multiple of six")
            if not div:
                raise ValueError("Must have at least 6 hex characters")
            hd = set(hexdigits)
            if not all(i in hd for i in s):
                raise ValueError(f"String '{s}' contains non-hex characters")
            n = 2*div   # Number of hex digits per color
            rgb = s[0*div:0*div + n], s[2*div:2*div + n], s[4*div:4*div + n]
            try:
                rgb = tuple(int(i, 16) for i in rgb)
            except Exception:
                raise ValueError(f"'{s}' is not a valid hex string")
            return rgb
        @classmethod
        def round(cls, value, digits):
            'Round value to number of digits (value can be float or sequence)'
            n = digits
            if not ii(value, str) and ii(value, Iterable):
                return tuple(round(float(i), n) for i in value)
            else:
                if not ii(value, float):
                    raise TypeError("value must be a float or numerical sequence")
                return round(value, n)
        @classmethod
        def Dot(cls, a, b):
            'Dot product of two sequences'
            Assert(len(a) == len(b))
            return sum(i*j for i, j in zip(a, b))
        @classmethod
        def XYZ_to_sRGB(cls, XYZ):
            '''CIE XYZ to sRGB (XYZ is a 3-sequence of positive numbers)
            sRGB will be 3-sequence of floats on [0, 1]
            https://en.wikipedia.org/wiki/SRGB#From_CIE_XYZ_to_sRGB
            '''
            if ii(XYZ, str) or len(XYZ) != 3:
                raise TypeError(f"'{XYZ}' must be a sequence of 3 numbers")
            if not all(i >= 0 for i in XYZ):
                raise TypeError(f"'{XYZ}' must be numbers >= 0")
            def GammaCompressed(x):
                return 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
            r1 = (+3.2406, -1.5372, -0.4986)
            r2 = (-0.9689, +1.8758, +0.0415)
            r3 = (+0.0557, -0.2040, +1.0570)
            rgb = Color.Dot(r1, XYZ), Color.Dot(r2, XYZ), Color.Dot(r3, XYZ)
            def clip(x):
                return min(1.0, max(x, 0.0))
            return tuple(clip(GammaCompressed(i)) for i in rgb)
        @classmethod
        def wl2rgb(cls, nm, sunlight=True, gamma=0.0, bpc=None):
            '''Convert nm (light wavelength in nm) into an rgb decimal
            3-tuple using an approximation.  The color black is returned
            for wavelengths out of the visible spectrum.  nm must be
            greater than zero.  Keywords:
 
            sunlight    If True, the colors returned are from an approximation
                        constructed from the sun's spectrum.  If False, a
                        "wider" approximation is made, but it is less physical
                        in the sense that it has colors that don't appear in
                        e.g. white light from the sun.
 
            gamma       If nonzero, perform a gamma correction on components 
                        (raise them to the gamma power).  Be careful with
                        gamma, as it can change the color.
 
            bpc         Bits per color.  Uses Color.bits_per_color if None.
            '''
            # Check parameters
            if not isinstance(nm, (int, float, flt)):
                raise TypeError("nm must be an int or float")
            if bpc is None:
                bpc = Color.bits_per_color
            if not isinstance(bpc, int):
                raise TypeError("bpc must be an int")
            if nm <= 0:
                raise ValueError("nm must be > 0")
            if not isinstance(gamma, (int, float, flt)):
                raise TypeError("gamma must be an int or float")
            if gamma < 0:
                raise ValueError(f"gamma must be >= 0")
            if sunlight:
                # From user Spektre's post last edited 5 Nov 2016 at
                # https://stackoverflow.com/questions/3407942/rgb-values-of-visible-spectrum/22681410#22681410
                # Edited by DP to return RGB = (3, 0, 3) for 400 nm
                if not (400 <= nm <= 700):
                    a = 0.0
                    return Color(a, a, a)
                r = g = b = 0.0
                # Red component
                if nm >= 400 and nm < 410:
                    t = (nm - 400)/(410 - 400)
                    r = 0.33*t - 0.2*t*t
                elif nm >= 410 and nm < 475: 
                    t = (nm - 410)/(475 - 410)
                    r = 0.14 - 0.13*t*t
                elif nm >= 545 and nm < 595: 
                    t = (nm - 545)/(595 - 545)
                    r = 1.98*t - t*t
                elif nm >= 595 and nm < 650:
                    t = (nm - 595)/(650 - 595)
                    r = 0.98 + 0.06*t - 0.4*t*t
                elif nm >= 650 and nm <= 700:
                    # DP I made it '<= 700' so wavelength range is on
                    # [400, 700].
                    t = (nm - 650)/(700 - 650)
                    r = 0.65 - 0.84*t + 0.2*t*t
                # Green component
                if nm >= 415 and nm < 475: 
                    t = (nm - 415)/(475 - 415)
                    g = 0.8*t*t
                elif nm >= 475 and nm < 590: 
                    t = (nm - 475)/(590 - 475)
                    g = 0.8 + 0.76*t - 0.8*t*t
                elif nm >= 585 and nm < 639: 
                    t = (nm - 585)/(639 - 585)
                    g = 0.84 - 0.84*t       
                # Blue component
                if nm >= 400 and nm < 475: 
                    t = (nm - 400)/(475 - 400)
                    b = 2.2*t - 1.5*t*t
                elif nm >= 475 and nm < 560: 
                    t = (nm - 475)/(560 - 475)
                    b = 0.7 - t + 0.3*t*t
                # DP correction for 400 nm:  401 nm gives (7, 0, 7) for RGB
                # [(215, 3, 255) for HLS], so I made 400 nm give (2, 0, 1)
                # [(233, 1, 255) in HLS].
                if nm == 400:
                    r, g, b = 2/255, 0, 1/255
                rgb = tuple([float(i) for i in (r, g, b)])
            else:
                # From # http://www.physics.sfasu.edu/astro/color/spectra.html (defunct).
                # Also see http://www.midnightkite.com/color.html.
                # From D. Bruton's FORTRAN code.
                if not (380 <= nm <= 780):
                    a = 0.0 
                    return Color(a, a, a)
                if 380 <= nm <= 440:
                    a = (440 - nm)/(440 - 380), 0, 1
                elif 440 <= nm <= 490:
                    a = 0, (nm - 440)/(490 - 440), 1
                elif 490 <= nm <= 510:
                    a = 0, 1, (510 - nm)/(510 - 490)
                elif 510 <= nm <= 580:
                    a = (nm - 510)/(580 - 510), 1, 0
                elif 580 <= nm <= 645:
                    a = 1, (645 - nm)/(645 - 580), 0
                elif 645 <= nm <= 780:
                    a = 1, 0, 0
                # Intensity i falls off near vision limits
                i, u, v = 1, 0.3, 0.7
                if nm > 700:
                    i = u + v*(780 - nm)/(780 - 700)
                elif nm < 420:
                    i = u + v*(nm - 380)/(420 - 380)
                # Scale the components by i
                rgb = [float(i*j) for j in a]
            # If gamma is not zero, perform a gamma transformation
            if gamma:
                rgb = [i**gamma for i in rgb]
            # Make sure the numbers are on [0, 1]
            assert(all([0 <= i <= 1 for i in rgb]))
            return Color(*rgb, bpc=bpc)
        @classmethod
        def Sort(cls, seq, keys="hL", get=None):
            '''Return a sorted copy of the sequence of Color instances.
            The keys parameter determines how to sort:  each element is a
            letter:  rgbhsvHLS that is used in the rgb, hls, and hsv attributes.
            Unfortunately, the 's' is hls and hsv mean different things.
            Here, 's' means the s in 'hls' and 'S' means the s in 'hsv'.
            Though they are described by the same term "saturation", the two
            functions return different values for s in python's colorsys module
            for the same RGB value.
 
            If get is not None, it's a predicate that is used to get the
            Color instance from the sequence seq.
            '''
            # The algorithm is to decorate an auxiliary sequence with the
            # indicated attribute values, sort it, and return it after
            # stripping off the decorations.
            if ii(seq, str) or not ii(seq, Iterable):
                raise TypeError("seq is not a suitable sequence")
            if not keys:
                raise ValueError("keys cannot be empty")
            S = set("rgbhsvHLS")
            for key in keys:
                if key not in S:
                    raise TypeError(f"keys '{keys}' contains an illegal letter")
            aux = []
            # Decorate the auxiliary copy of seq with the attribute numbers
            for item in seq:
                # Get the Color instance from the sequence
                if get is None:
                    c = item
                else:   # Use the predicate
                    c = get(item)
                if not ii(c, Color):
                    raise TypeError(f"'{c}' is not a Color instance")
                itemkey = []
                for key in keys:
                    # Get the integer form of the key
                    if key == "r":
                        k = c.irgb[0]
                    elif key == "g":
                        k = c.irgb[1]
                    elif key == "b":
                        k = c.irgb[2]
                    elif key == "h" or key == "H":
                        k = c.ihls[0]
                    elif key == "L":
                        k = c.ihls[1]
                    elif key == "S":
                        k = c.ihls[2]
                    elif key == "s":
                        k = c.ihsv[1]
                    elif key == "v":
                        k = c.ihsv[2]
                    itemkey.append(k) 
                decorated = tuple(itemkey), item
                aux.append(decorated)
            # Now we can use a default sort on aux
            aux = sorted(aux, key=lambda x: x[0])
            # Strip decorations
            return tuple(i[1] for i in aux)
        classmethod
        def Construct(cls, s):
            '''Uses regular expressions to recognize color initializers in a
            string s.  Returns a Color instance or None.  If s is a multiline
            string, a deque of (line, Color_instance) tuples is returned.
            Trailing whitespace of the line is stripped.
             
            Forms recognized:
                '@000000' or '#000000' or '$000000' 
                '1, 2, 3'
                '1 2 3'
                '1.0, 2.0, 3.0'
                '1.0 2.0 3.0'
 
            An example use case is the /plib/pgm/cdec.py script, which is
            used to print out the lines of a file containing a color
            specification in that color.
            '''
            def GetColorRegexps():
                'Return tuple of regexps to use to recognize color identifiers'
                R = re.compile
                # Recognize an integer or float
                s = r'''
                        (                               # Group
                            # First is for numbers like .234
                            [+-]?                       # Optional sign
                            \.\d+
                            ([eE][+-]?\d+)?             # Optional exponent
                        |                             # or
                            # This is for integers or 2.3 or 2.3e4
                            [+-]?                       # Optional sign
                            \d+\.?\d*                   # Number:  2.345
                            ([eE][+-]?\d+)?             # Optional exponent
                        )                               # End group
                '''
                flags = re.I | re.X
                regexps = (
                    # [@#$]XXYYZZ form
                    ("hex", R(r"([@#$][0-9a-f]{6})", flags)),
                    # Three integers or floats separated by commas
                    ("fcomma", R(rf"({s},\s*{s},\s*{s})", flags)),
                    # Three integers or floats separated by whitespace
                    ("fspace", R(rf"({s}\s+{s}\s+{s})", flags)),
                )
                return regexps
            def Decode(match, name):
                'Turn a matched string into a Color instance'
                if name == "hex":
                    return Color(match)
                elif name == "fcomma":
                    if "." in match or "e" in match:
                        rgb = [float(i) for i in match.split(",")]
                    else:
                        rgb = [int(i) for i in match.split(",")]
                    return Color(*rgb)
                elif name == "fspace":
                    if "." in match or "e" in match:
                        rgb = [float(i) for i in match.split()]
                    else:
                        rgb = [int(i) for i in match.split(",")]
                    return Color(*rgb)
            regexps = GetColorRegexps()
            def Find(line):
                for name, r in regexps:
                    mo = r.search(line)
                    if mo:
                        # Got a match
                        color = mo.groups()[0]
                        return Decode(color, name)
                return None
            if "\n" in s:
                # It's a multiline string
                keep = deque()
                for line in s.split("\n"):
                    line = line.rstrip()
                    if not line:
                        continue
                    color = Find(line)
                    if color:
                        keep.append((line, color))
                return keep if keep else None
            else:
                return Find(s)

class Trm:
    '''This class is used to generate terminal escape codes
        Ref:  https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
        For typical use, instantiate with t = Trm().  Store "styles" by
        using the Trm instance's attributes:
 
            t.err = t("red")      # Error messages are red
 
        Use the styles in f-strings:
 
            print(f"{t.err}Error:  symbol doesn't exist{t.n}")
 
        t.err and t.n are strings containing the ANSI escape codes
        (t.n is the escape code for the standard terminal text).  The
        previous can be a little more terse with the equivalent:
 
            t.print(f"{t.err}Error:  symbol doesn't exist")
 
        t.print() and t.out() output their strings then output the
        escape code to return to the normal style.  To remove all your
        "style" definitions, use t.reset().  To see the styles you've
        defined, use print(t).
 
        Read/write properties
            always      (bool) Set to True if you want the object to
                        generate escape codes, even if stdout isn't a
                        terminal. 
            cn          ColorNames instance used to translate string names
                        to Color instances.
            on          (bool) If True, then escape codes are generated.
 
        For first time use, define the terminal_bits class variable for
        your terminal and monitor.  Most modern terminals are 24 bits.
        You'll also want to define Trm.default_color as a tuple of two
        Color instances for your default foreground and background colors.
 
        A common use case in an application is a command line option is
        used to enable or disable colorizing.  Suppose this option is
        encoded in the Boolean variable use_colorizing.  I recommend the
        following pattern near the beginning of your program (t is the Trm
        instance):
 
            def SetColors(t):
                t.on = use_colorizing
                t.a = t("red")
                t.b = t("brn")
                t.c = t("grn")
 
        This ensures that the t instance's attributes will either have the
        correct escape code strings or be empty strings if colorizing
        wasn't wanted.
    '''
    terminal_bits = 24
    default_color = (Color(192, 192, 192), Color(0, 0, 0))
    def __init__(self, bits=None):
        '''Initialize the Trm instance
        bits
            Can override the default value of Trm.terminal_bits.  This
            setting determines the type of ANSI escape codes that are
            emitted.  Must be 4, 8, or 24.
 
            Note:  4 and 8 bit not currently supported.
        '''
        # If True, generate escape codes even if stdout isn't a terminal
        self._always = False
        self._on = True         # If True, escape codes are generated
        # ColorNames dictionary (defaults to module's global variable CN)
        self.cn = CN
        self._bits = bits       # Bits per color
        if self._bits is None:
            self._bits = Trm.terminal_bits
        if self._bits != 24:
            raise ValueError("4 and 8 bit terminals not supported yet")
        self._fg = None     # Default foreground color
        self._bg = None     # Default background color
        self.reset()
        self._check()
    if 1:   # Utility methods
        def _check(self):
            'Validate the initial attributes'
            assert(ii(self._bits, int) and self._bits in (4, 8, 24))
            assert(ii(self._fg, Color))
            assert(ii(self._bg, Color))
            assert(ii(self.cn, ColorName))
        def _ta(self):
            'Return attributes mapping'
            s = '''normal-no:0 bold-bo:1 dim-di:2 italic-it:3
            underline-ul:4 blink-bl:5 rapidblink-rb:6 reverse-rv:7
            hide-hi:8 strikeout-so:9 doubleunderline-du:21 overline-ol:53
            superscript-sp:73 subscript-sb:74'''
            ta = {}
            for i in s.split():
                name, num = i.split(":")
                short, long = name.split("-")
                num = int(num)
                ta[short] = num
                ta[long] = num
            return ta
        def _user(self):
            'Return a set of user-defined attribute names'
            ignore = set('''_bits cn on _fg fg _bg bg _ta _always always _user _check
                _get_code load n out print reset GetColorNames terminal_bits
                default_color'''.split())
            attributes = []
            for i in dir(self):
                if i.startswith("__") or i in ignore:
                    continue
                attributes.append(i)
            return set(attributes)
        def __str__(self):
            '''Returns a string that can be printed to stdout to show all the
            currently-defined styles.
            '''
            show = []
            for style in sorted(self._user()):
                s = getattr(self, style)
                if s:
                    show.append(style)
            out = []
            if show:
                for i in show:
                    s = f"{getattr(self, i)}{i}{self.n}"
                    out.append(s)
            classname = str(self.__class__)
            loc = classname.find(".")
            classname = classname[loc + 1:]
            if classname.endswith("'>"):
                classname = classname[:-2]
            return classname + "(" + ' '.join(out) + ")"
        def _get_code(self, color, bg=False):
            'For Color instance color, return escape code'
            if color is not None:
                assert(ii(color, Color))
            else:
                return ""
            assert(ii(bg, bool))
            if self._bits == 4:
                raise Exception("Not implemented")
            elif self._bits == 8:
                raise Exception("Not implemented")
            elif self._bits == 24:
                n = 48 if bg else 38
                if color.bpc > 8:
                    color = color.change_bpc(8)
                r, g, b = color.irgb
                code = f"\x1b[{n};2;{r};{g};{b}m"
            else:
                raise RuntimeError("self._bits bad")
            return code
        def load(self, file, reset=False, show=False):
            '''Read style definitions from a file (filename string, stream,
            or string of characters).  Each line is either a comment
            (leading '#') or must contain the following fields separated by
            whitespace:
                style_name fg_color_name bg_color_name [attr1 [attr2 ...]]
            where fg_color_name and bg_color_name are either color name
            strings or None.  These strings can also be suitable integer
            strings (e.g., '21') and will be converted to integers.  attr1,
            etc. are attribute strings that are in the dictionary ta.
     
            If show is True, print this object to stdout after loading is
            finished.
            '''
            def Convert(s):
                'Convert color string'
                if s == "None":
                    return None
                else:
                    try:
                        n = int(s)
                        return n
                    except Exception:
                        return s
            lines = GetNumberedLines(file)
            # Remove blank lines
            lines = [i for i in lines if i[1]]
            # Remove leading spaces
            lines = [(i, j.strip()) for i, j in lines]
            # Remove comments
            lines = [(i, j) for i, j in lines if j[0] != "#"]
            if reset:
                self.reset()
            # Parse the remainder
            for n, line in lines:
                f = line.split()
                if len(f) < 3:
                    msg = f"Line {n}:  not enough fields:\n  '{line}"
                    raise ValueError(msg)
                name = f.pop(0)
                s = f.pop(0)
                fg = Convert(s)
                s = f.pop(0)
                bg = Convert(s)
                attrs = f if f else None
                if attrs:
                    attrs = ' '.join(attrs)
                s = f"self.{name} = self(fg={fg!r}, bg={bg!r}, attr={attrs!r})"
                exec(s)
            if show:
                t = "string"
                try:
                    f = P(file)
                    if f.exists():
                        t = f"file '{file}'"
                except Exception:
                    if hasattr(file, "read"):
                        t = "stream"
                print(f"Trm.load() from {t}: ", self)
        def reset(self):
            'Sets the instance to a default state'
            # Delete all user-set attributes
            for i in self._user():
                try:
                    delattr(self, i)
                except AttributeError as e:
                    if 0:       # Use to flag programming problems
                        print(e)
                        breakpoint()
                    else:
                        pass    # Ignore the problem
            # Reset to default colors
            self._fg, self._bg = Trm.default_color
            # Turn on output unless not to terminal
            self._on = False
            so = sys.stdout
            if (hasattr(so, "isatty") and so.isatty()) or self.always:
                self._on = True
    if 1:   # Core methods
        def __call__(self, fg=None, bg=None, attr=None):
            '''Return the indicated color style escape code string.  fg and
            bg must be Color instances.  They may also be strings if a
            ColorNames dictionary has been loaded with GetColorNamesDict().
            Hex strings beginning with "@" (hsv), "#" (rgb), or "$" (hls)
            are also allowed.
     
            attr    String of attributes (separate multiple attributes by
                    spaces).
            fg      Foreground Color instance or string
            bg      Background Color instance or string
            '''
            msg = "{} must be None, a string, or a Color instance"
            if fg is not None and not ii(fg, (Color, str)):
                raise ValueError(msg.format("fg"))
            if bg is not None and not ii(bg, (Color, str)):
                raise ValueError(msg.format("bg"))
            if attr is not None and not ii(attr, str):
                raise ValueError("attr must be None or a string")
            if not self._on:
                return ""
            '''
            Primer on ANSI escape sequences
            https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
            gives information on attributes and the section below that
            discusses colors.
     
            4-bit color
                ESC[<f>;<b>m    f is foreground, b is background
                f   g                               Short name
                30  40  Black                       blk
                31  41  Red                         red
                32  42  Green                       grn
                33  43  Yellow                      yel
                34  44  Blue                        blu
                35  45  Magenta                     mag
                36  46  Cyan                        cyn
                37  47  White                       wht
                90 100  Bright black (gray)         blkl
                91 101  Bright red                  redl
                92 102  Bright green                grnl
                93 103  Bright yellow               yell
                94 104  Bright blue                 blul
                95 105  Bright magenta              magl
                96 106  Bright cyan                 cynl
                97 107  Bright white                whtl
            8-bit color
                ESC[38;5;<n>m      Foreground color
                ESC[48;5;<n>m      Background color
                0-7    :  Standard colors
                8-15   :  High intensity colors
                16-231 :  6x6x6 cube:  16 + 36*r + 6*g + b (0 <= r, b, g <= 5)
                232-255:  Grayscale from black to white in 24 steps
            24-bit color
                ESC[38;2;<r>;<g>;<b>m      RGB foreground color
                ESC[48;2;<r>;<g>;<b>m      RGB background color
            '''
            # If they are strings, they are either a name or a hex string.
            if fg and ii(fg, str):
                if fg[0] in "@#$":
                    fg = Color(fg)
                else:
                    new = None
                    if "@" in fg or "#" in fg or "$" in fg:     # It's a composite
                        new = self.cn.split(fg)
                    fg = self.cn[fg] if new is None else new
            if bg and ii(bg, str):
                if bg[0] in "@#$":
                    bg = Color(bg)
                else:
                    new = None
                    if "@" in bg or "#" in bg or "$" in bg:     # It's a composite
                        new = self.cn.split(bg)
                    bg = self.cn[bg] if new is None else new
            # Put the escape codes for fg, bg, and attributes in the
            # container
            container = []
            # Get attr codes
            if attr is not None:
                ta = self._ta()
                attrs = attr.split()
                while attrs:
                    a = attrs.pop(0)
                    if a not in ta:
                        msg = f"'{a}' is not a valid attribute"
                        raise ValueError(msg)
                    container.append(f"\x1b[{ta[a]}m")
            # Get other codes
            assert(fg is None or ii(fg, Color))
            assert(bg is None or ii(bg, Color))
            container.append(self._get_code(fg))
            container.append(self._get_code(bg, bg=True))
            return ''.join(container)
        def print(self, *p, **kw):
            '''Print arguments with newline, reverting to normal color
            after finishing.
            '''
            self.out(*p, **kw)
            print(**kw)
        def out(self, *p, **kw):
            'Same as print() but no newline'
            k = kw.copy()
            if "end" not in k:
                k["end"] = ""
            print(*p, **k)
            print(self.n, **k)
    if 1:   # Writable properties
        @property
        def on(self):
            return self._on
        @on.setter
        def on(self, value):
            self._on = bool(value)
        @property
        def always(self):
            return self._always
        @always.setter
        def always(self, value):
            self._always = bool(value)
            self._on = True
    if 1:   # Read-only properties
        @property
        def n(self):
            'Return escape code for normal (default) screen'
            if not self._on:
                return ""
            s = []
            s.append(self._get_code(self._fg, bg=False))
            s.append(self._get_code(self._bg, bg=True))
            s.append("\x1b[0m")     # Normal text attribute
            return ''.join(s)
        @property
        def fg(self):
            'Returns default foreground color'
            if not self._on:
                return ""
            return self._fg
        @property
        def bg(self):
            'Returns default background color'
            if not self._on:
                return ""
            return self._bg

class ColorName(dict):
    '''This class is a dictionary initialized with a file name.  This must be
        a text file that has lines with the following forms:
            
            # A comment
            "<key_string>" : <color identifier>
    
        You can use any string for <key_string> as long as it doesn't contain the
        '==' string.  It must be surrounded by single or double quote
        characters.
    
        A color identifier is a Color constructor call, such as
    
            Color(255, 0, 0)        # Can have a comment
            Color(0.1, 0.2, 0.3, hsv=True)
            Color(0.1)
            Color("@010203")
            Color("#010203")
            Color("$010203")
    
        The key strings are normalized to the form of all lower case letters
        and uses underscores separate words.  This is done by changing
        underscores to space characters and inserting a space character before
        every capital 7-bit ASCII letter; then the resulting string is split on
        whitespace into its word components.  You are free to use any Unicode
        characters in the string except ':'.  If you wish to use a different
        separator string, change the class Variable ColorName.sep.
    
        Thus, the following strings are equivalent:
            
                "light green"
                "light     green"
                "Light green"
                "Light Green"
                "LightGreen"
                "light Green"
                "light_Green"
                etc.
    
        and normalize to "light_green".
    
        Note that "lightgreen" is a distinct name not equal to any in the
        previous list.
    
        You can also call the load() method at anytime to load a new file.
 
        load() uses exec() for assignment statments (statements that contain
        '=') unless ColorName.allow_exec is set to False.  Use False if you
        haven't vetted the file for possible malicious code.  An advantage of
        setting it to True is that you can define variables to use in the color
        definitions.
 
        An advantage of this file format is the cdec.py script can be used to
        show you the color definitions in the file.
    '''
    sep = ":"           # Separator string:  name<sep>Color_instance
    allow_exec = True   # Allow exec() of expressions
    def __new__(cls):
        instance = super().__new__(cls)
        instance._normalize = False
        return instance
    def __str__(self):
        "Show the dict's contents in color"
        k, out, blk = Trm(), [], Color("blk")
        w = max(len(i) for i in self)
        for name in self:
            c = self[name]
            out.append(f"{name:{w}s}: {k(c)}{c!s}{k.n}  {k(blk, c)}background{k.n}")
        return '\n'.join(out)
    def load(self, file: str, clear=False):
        '''Extend ourselves by loading colors from file.  Set clear to True
        to first empty the dictionary.
        '''
        if clear:
            self.clear()
        vars = {}
        for line in open(file).read().split("\n"):
            line = line.strip()
            if not line or line[0] == "#":
                continue
            if ColorName.sep in line:
                a, b = line.split(ColorName.sep)
                name = eval(a)
                if self._normalize:
                    raise Exception("Normalization not implemented yet")
                c = eval(b, None, locals())
                try:
                    self[name] = c
                except Exception as e:
                    print(e)
                    breakpoint()
            else:
                if "=" in line and ColorName.allow_exec:
                    exec(line)
                else:
                    raise ValueError(f"Illegal line:\n'{line}'")
    def split(self, name):
        '''A name string can be made up of multiple names separated by one
        of the characters '@', '#', or '$'.  The resultant color is
        computed by taking each pair of names and interpolating halfway
        between them.  Each component must be a valid color name.  @ means
        to interpolate in HSV space, @ in RGB, and $ in HLS.
 
        Returns a Color instance or None if it can't be calculated.
        '''
        if not ("@" in name or "#" in name or "$" in name):
            return None
        sep = "@" if "@" in name else "#" if "#" in name else "$"
        space = "hsv" if sep == "@" else "rgb" if sep == "#" else "hls"
        names = deque(name.split(sep))
        old = self[names.popleft()]
        while names:
            new = self[names.popleft()]
            old = old.interpolate(new, 0.5, space=space)
        return old

# Define default ColorName instance
CN = ColorName()
if wsl:
    CN.load("/plib/colornames0")
else:
    CN.load("d:/cygwin64/plib/colornames0")

# Define default Trm instance
TRM = Trm()
t = TRM     # I use 't' so much it should be defined
TRM.cn = CN

class RegexpDecorate:
    '''Decorate regular expression matches with color.
        The styles attribute is a dictionary that contains the styles to
        apply for each regexp's match (key is the compiled regexp).  The
        style is a tuple of 1 to 3 values:  fg color, bg color, and text
        attributes.  None means to use the default.
    
        Example use:
    
            rd = RegexpDecorate()
            r = re.compile(r"[Mm]adison")
            fg = t("yell")
            bg = t.n
            # Note fg and bg must be escape sequences
            rd.register(r, fg, bg)    # Print matches in light yellow on black
            for line in open(file).readlines():
                rd(line)    # Lines with matches are printed to stdout
    
        The previous can also be done with
            rd(open(file))
    
        multiline = """
            Here's a multiline string that
            might contain madison or Madison.
        """
        rd(multiline)
    
        Suppose the string pnp contains the text of "Pride and Prejudice".  You
        could print out all the lines with the string "Elizabeth" or "Lizzy"
        with
            rd = RegexpDecorate()
            r = re.compile(r"Elizabeth|Lizzy", re.I)
            rd.register(r, t(Color("yell")), t.n)
            rd(pnp)
    
        Suppose you have python files in a directory "mydir" and you're
        interested in knowing how many lines contain the string "MySymbol".
        This can be done with
            rd = RegexpDecorate()
            r = re.compile(r"MySymbol")
            files = pathlib.Path("mydir").glob("*.py")
            rd.register(r, t(Color("yell")), t.n)
            rd(*files)
    
        A command line tool like grep is capable of more precise searching
        including file names and line numbers.
    '''
    def __init__(self):
        self._styles = {}
    def register(self, r, match_style, nomatch_style=""):
        '''Register a regexp and its styles.  
            match_style is the escape code to print before a match and
            nomatch_style is the escape code to print before a nonmatching
            string.  You can generate these escape codes with a TRM
            instance.
        '''
        assert(ii(r, re.Pattern))
        self._styles[r] = (match_style, nomatch_style)
    def unregister(self, r):
        'Remove regexp r from our styles dict'
        if r in self._styles:
            del self._styles[r]
    def __str__(self):
        return f"RegexpDecorate(<styles={len(self._styles)}>)"
    def __repr__(self):
        return str(self)
    def __call__(self, line, file=sys.stdout, insert_nl=False):
        '''Print the decorated line to the stream.
            Check line for a match to one of the registered regexps and if
            there's a match, print the decorated line to the indicated
            stream.  Returns True if there was a match, False otherwise.
 
            If insert_nl is True, print a newline if line doesn't end with
            a newline.
 
            Note:  if your escape code for match_style includes an
            attribute, you'll want to include
            the 'no' attribute for normal text in your nomatch_style.
            Otherwise, the remaining text will continue to be printed in
            the match_style's attribute.
        '''
        assert(ii(line, str))
        if not line:
            return
        has_nl = line.endswith("\n")
        had_match = False
        match_style, nomatch_style = "", t.n
        while line:
            # Find regexp match closest to beginning of line
            shortest = []
            for r in self._styles:
                mo = r.search(line)
                if mo:
                    shortest.append((mo.start(), mo, r))
                    had_match = True
            if not shortest:
                # No more matches
                if line and had_match:
                    if not has_nl and insert_nl:
                        print(f"{line}{nomatch_style}", file=file)
                    else:
                        print(f"{line}{nomatch_style}", end="", file=file)
                elif line:
                    # Print rest of line
                    if not has_nl and insert_nl:
                        print(f"{nomatch_style}{line}{t.n}", file=file)
                    else:
                        print(f"{nomatch_style}{line}{t.n}", end="", file=file)
                return had_match
            # Sort shortest to find the first match
            location, mo, r = sorted(shortest, key=lambda x: x[0])[0]
            match_style, nomatch_style = self._styles[r]
            # Print non-matching start stuff in nomatch_style
            print(f"{nomatch_style}{line[:location]}", end="", file=file)
            # Print the match in match_style, then the escape code to
            # switch back to the default print style (t.n).
            match = line[mo.start():mo.end()]
            print(f"{match_style}{match}{nomatch_style}", file=file, end="")
            # Trim the line and search again
            line = line[mo.end():]
        if had_match:
            print(f"{t.n}", end="")     # Default text style
            if not line and not has_nl and insert_nl:
                print(file=file)
        return True

# Legacy color.py support:  define the environment variable 'klr' to be a
# nonempty string to enable this section (this is done by
# default).  Legacy code should then work.  You can then work on porting
# the old code to the new color.py functionality and quickly test that it
# no longer needs the legacy code by setting klr="".
klr = bool(os.environ.get("klr", "on"))
if klr:   # Legacy code support
    '''This is intended to support the old color.py file and the
    approximately 80 files that used it under /plib.  The intent is to
    allow each of the dependent files to have 'kolor' renamed to 'color'
    and have things continue to work with no other work.  Then each of
    these legacy dependent files can be edited when appropriate to work
    with the new interfaces.
    '''
    if 1:   # Utility
        def _is_iterable(x):
            '''Return True if x is an iterable that isn't a string.
            '''
            return ii(x, Iterable) and not ii(x, str)
        def _DecodeColor(*c):
            '''Return a 1-byte integer that represents the foreground and
            background color.  c can be
                * An integer
                * Two integers
                * A sequence of two integers
            '''
            if len(c) == 1:
                # It can either be a number or a tuple of two integers
                if _is_iterable(c[0]):
                    if len(c[0]) != 2:
                        raise ValueError("Must be a sequence of two integers")
                    color = ((c[0][1] << 4) | c[0][0]) & 0xff
                else:
                    if not ii(c[0], int):
                        raise ValueError("Argument must be an integer")
                    color = c[0] & 0xff
            elif len(c) == 2:
                color = ((c[1] << 4) | c[0]) & 0xff
            else:
                raise ValueError("Argument must be one or two integers")
            return color
        def _GetNibbles(c):
            assert 0 <= c < 256
            return (0x0f & c, (0xf0 & c) >> 4)
    class Colors(int):
        '''Used to identify colors; shift left by 4 bits to get a
        background color.  The main reason to use a class allows the
        __call__ method to be added, which returns the escape code.
        This is a convenience for use in f-strings; for example
            print(f"{yellow()}Hello {norm()}there")
        will print 'Hello' in yellow and 'there' in the normal color.
        '''
        _DecodeColor = None
        _GetNibbles = None
        _cfg = None
        _cbg = None
        def __new__(cls, value):
            return super(Colors, cls).__new__(cls, int(value))
        def __call__(self, arg=None):
            '''Return the ASCII escape code for the color.  If arg is
            not none, return the escape code for the background color.
            '''
            val = self << 4 if arg else self
            one_byte_color = Colors._DecodeColor(val)
            cfg, cbg = Colors._GetNibbles(one_byte_color)
            f, b = Colors._cfg[cfg], Colors._cbg[cbg]
            s = "\x1b[%s;%s" % (f, b)
            return s
    # Legacy foreground colors; shift left by 4 bits to get a background color.
    (
        black, blue, green, cyan, red, magenta, brown, white,
        gray, lblue, lgreen, lcyan, lred, lmagenta, yellow, lwhite
    ) = [Colors(i) for i in range(16)]
    # Set the default_colors global variable to be the defaults for your system
    default_colors = (white, black)
    # Dictionary to translate between color numbers/names and escape sequence
    _cfg = {
        black: "0;30",
        blue: "0;34",
        green: "0;32",
        cyan: "0;36",
        red: "0;31",
        magenta: "0;35",
        brown: "0;33",
        white: "0;37",
        gray: "1;30",
        # Note legacy names
        lblue: "1;34",
        lgreen: "1;32",
        lcyan: "1;36",
        lred: "1;31",
        lmagenta: "1;35",
        yellow: "1;33",
        lwhite: "1;37",
    }
    _cbg = {
        black: "40m",
        blue: "44m",
        green: "42m",
        cyan: "46m",
        red: "41m",
        magenta: "45m",
        brown: "43m",
        white: "47m",
        gray: "40m",
        # Note legacy names
        lblue: "44m",
        lgreen: "42m",
        lcyan: "46m",
        lred: "41m",
        lmagenta: "45m",
        yellow: "43m",
        lwhite: "47m",
    }
    def normal(*p, **kw):
        '''If the argument is None, set the foreground and background
        colors to their default values.  Otherwise, use the argument to
        set the default colors.
    
        If keyword 's' is True, return a string instead of printing.
        '''
        ret_string = kw.setdefault("s", False)
        global default_colors
        if p:
            one_byte_color = _DecodeColor(*p)
            default_colors = _GetNibbles(one_byte_color)
        else:
            if ret_string:
                return fg(default_colors, **kw)
            else:
                fg(default_colors, **kw)
    def fg(*p, **kw):
        '''Set the color.  p can be an integer or a tuple of two
        integers.  If it is an integer that is greater than 15, then it
        also contains the background color encoded in the high nibble.
        fgcolor can be a sequence of two integers of length two also.
    
        The keyword 'style' can be:
            normal
            italic
            underline
            blink
            reverse
    
        If the keyword 's' is True, return a string containing the escape
        codes rather than printing it.  Note this won't work if _win is True.
        '''
        style = kw.setdefault("style", None)
        ret_string = kw.setdefault("s", False)
        one_byte_color = _DecodeColor(*p)
        # Use ANSI escape sequences
        cfg, cbg = _GetNibbles(one_byte_color)
        f, b = _cfg[cfg], _cbg[cbg]
        s = "\x1b[%s;%s" % (f, b)
        if style is not None:
            if ret_string:
                st = SetStyle(style, **kw)
                return s + st
            else:
                SetStyle(style)
                return ""
        else:
            if ret_string:
                return s
            print(s, end="")
            return ""
    class C:
        '''This is a convenience instance that holds the escape strings for
        the colors.  The color names are abbreviated with three letters
        commonly seen in resistor color codes.  Preface with 'l' to get the
        brighter color.
        '''
        blk = fg(black, s=1)
        blu = fg(blue, s=1)
        grn = fg(green, s=1)
        cyn = fg(cyan, s=1)
        red = fg(red, s=1)
        mag = fg(magenta, s=1)
        yel = fg(brown, s=1)
        wht = fg(white, s=1)
        gry = fg(gray, s=1)
        # Note these are legacy color support, so the bright names begin
        # with 'l', not end with 'l'.
        lblu = fg(lblue, s=1)
        lgrn = fg(lgreen, s=1)
        lcyn = fg(lcyan, s=1)
        lred = fg(lred, s=1)
        lmag = fg(lmagenta, s=1)
        lyel = fg(yellow, s=1)
        lwht = fg(lwhite, s=1)
        norm = normal(s=1)

if 0:   # Prototyping area
    # Develop new escape-code styles for RegexpDecorate.register()
    s = "Hello world"
    r = re.compile("llo ")
    rd = RegexpDecorate()
    match_style = t("skyl")
    nomatch_style = t.n
    rd.register(r, match_style, nomatch_style)
    rd(s, insert_nl=True)
    exit()

if __name__ == "__main__":
    import getopt
    from lwtest import run, raises, Assert, assert_equal
    from collections import deque
    from columnize import Columnize
    def GetShortNames(all=False):
        '''Return a tuple of the short names.  If all is True, then
        also append the letters d, l, and b to get all of the basic
        colors.
        '''
        R = '''blk brn red orn yel grn blu vio gry wht cyn mag
                pnk lip lav lil pur roy den sky trq sea lwn olv'''.split()
        if all:
            others = []
            others.extend(i + "d" for i in R)
            others.extend(i + "l" for i in R)
            others.extend(i + "b" for i in R)
            R.extend(others)
        return tuple(R)
    def Reset():
        Color.bits_per_color = 8
    def TestTrm():
        # Not exhaustive, but will test some features.  Tested only
        # under mintty 3.5.2.
        t = Trm()
        t.m = t(Color(239, 132, 239), attr="rv")    # Orchid for test case headings
        def TestLoad():
            'Test Trm.load() from file, stream and string'
            t.print(f"{t.m}Test of Trm.load()")
            s = "/tmp/tmp.clr.py"
            f = P(s)
            open(P(s), "w").write("err redl None\n")
            x = Trm()
            x.load(f, show=True)            # File
            x.load(open(f), show=True)      # Stream
            s = "err redl None"
            x.load(s, show=True)            # String
            f.unlink()
        def TestRegexpDecorate():
            x = Trm()
            x.of = x(Color("blk"), Color("grnl"))
            x.man = x(Color("yell"), attr="rv rb")
            x.so = x(Color("redl"), Color("blul"))
            x.Is = x(None, None, attr="ul ol")
            t.print(dedent(f'''
                {t.m}Test of regular expression decoration{t.n}
                    'of' should be {x.of}of{x.n}{t.n}.
                    'man' should be {x.man}man{x.n}{t.n}.
                    'so' should be {x.so}so{x.n}{t.n}.
                    'is' should be lined as {x.Is}is{x.n}{t.n}.
            '''))
            s = dedent('''
                However little known the feelings or views of such
                a man may be on his first entering a neighbourhood,
                this truth is so well fixed in the minds of the 
                surrounding families, that he is considered the rightful
                property of some one or other of their daughters.\n
            ''')
            r = [(re.compile(r"of"), x.of),
                 (re.compile(r"man"), x.man),
                 (re.compile(r"so"), x.so),
                 (re.compile(r"is"), x.Is)]
            PrintMatches(s, r)
        #TestLoad()             # Themes not working yet
        #TestRegexpDecorate()   # Not working yet
    def TestColor():
        def Test_adjust():
            Reset()
            c = Color(0, 100, 0)
            # Adjust green up and down by 10%
            c1 = c.adjust(10, comp="g", set=False)
            Assert(c1.irgb == (0, 110, 0))
            c1 = c.adjust(-10, comp="g", set=False)
            Assert(c1.irgb == (0, 90, 0))
            # Set green to 0
            c1 = c.adjust(0, comp="g", set=True)
            Assert(c1.irgb == (0, 0, 0))
        def Test_short_color_names():
            # This just sees that the names are recognized.
            R = GetShortNames(all=True)
            for i in R:
                c = Color(i, bpc=8)
                c = Color(i, bpc=10)
        def Test_change_bpc():
            Reset()
            a = (15, 3, 7)
            c = Color(*a, bpc=4)
            d = c.change_bpc(8)
            Assert(d == Color(240, 48, 112, bpc=8))
            e = c.change_bpc(4)
            Assert(e == c)
            f = c.change_bpc(34)
            Assert(f == Color(16106127360, 3221225472, 7516192768, bpc=34))
            g = f.change_bpc(4)
            Assert(g == c)
        def TestAttributes():
            Reset()
            a = (3, 34, 18)
            c = Color(*a)
            n = c.N - 1
            Assert(c.irgb == c._rgb)
            dec = tuple(i/n for i in c._rgb)
            Assert(c.drgb == dec)
            Assert(c.xrgb == "#032212")
            #
            Assert(c.ihsv == (105, 232, 34))
            e = Color(*c.ihsv, hsv=True)
            Assert(e == c)  # Shows c.ihsv converts back to original color
            dec = (0.41397849462365593, 0.9117647058823529, 0.13333333333333333)
            Assert(c.dhsv == dec)
            Assert(c.xhsv == "@69e822")
            # Can add attributes (no __slots__)
            c.a = 4
            Assert(c.a == 4)
        def Test_downshift():
            n = 7
            c1 = Color(1, 2, 3, bpc=13)
            c2 = Color(88, 233, 73, bpc=n)
            n1, n2 = Color.downshift(c1, c2)
            Assert(n1.bpc == n and n2.bpc == n)
        #xx Need to test with space = "hsv", "hls"
        def Test_dist():
            n = 8
            m = 2**n - 1
            c1 = Color(0, 0, 0, bpc=n)
            c2 = Color(m, m, m, bpc=n)
            x = Color.dist(c1, c2)
            Assert(Color.dist(c1, c2) == 1)
            Assert(Color.dist(c1, c2, taxicab=True) == 1)
        def TestEquality():
            Reset()
            if 1:   # Integers in constructor
                a, b, c = (36, 40, 99)
                c1 = Color(a, b, c)
                e, f, g = c1.irgb
                c2 = Color(a, b, c)
                c3 = Color(a + 1, b, c)
                Assert(c1 == c2)
                Assert(hash(c1) == hash(c2))
                Assert(c1 != c3)
                # Show equality only depends on the stored integers
                c3._rgb = (a, b, c)
                Assert(c1 == c3)
                Assert(hash(c1) == hash(c3))
            if 1:   # Floats in constructor
                c1 = Color(e, f, g)
                c2 = Color(e, f, g)
                Assert(c1 == c2)
            if 1:
                # Colors with different bpcs can be equal
                c1 = Color(15, 0, 0, bpc=4)
                c2 = Color(255, 0, 0, bpc=8)
                Assert(c1 == c2)
        def TestInterpolate():
            Reset()
            c1 = Color(210, 105, 30)  # chocolate    
            c2 = Color(205, 41, 144)  # maroon3
            got = c1.interpolate(c2, 0.65)
            expected = Color(206, 63, 104)
            Assert(got == expected)
        def TestConstruct():
            Reset()
            def f(x):
                return tuple(round(i, 3) for i in x)
            # No color specifier gets None
            s = "kldjfkdj"
            c = Color.Construct(Color, s)
            Assert(c is None)
            # Separated by commas or spaces
            expected = Color(25, 51, 76)
            for s in (".1, .2, .3", ".1 .2 .3"):
                c = Color.Construct(Color, s)
                Assert(c == expected)
            # Multiline
            t = "This is a line"
            s = f'''
                {t} (.1, .2, .3)
                {t} (.2, .4, .7)
            '''
            a = Color.Construct(Color, s)
            Assert(ii(a, deque))
            name, c = a.popleft()
            Assert(t in name)
            Assert(c == expected)
            name, c = a.popleft()
            Assert(t in name)
            Assert(f(c.drgb) == (0.200, 0.400, 0.698))
        def TestDistance():
            Reset()
            a = 12, 6, 247
            b = 101, 171, 124
            c1 = Color(*a)
            c2 = Color(*b)
            def f(x, y):
                return (sum((i - j)**2 for i, j in zip(x, y))/3)**(1/2)
            # rgb
            d1 = f(c1.drgb, c2.drgb)
            d2 = Color.dist(c1, c2, space="rgb")
            Assert(d1 == d2)
            # hsv
            d1 = f(c1.dhsv, c2.dhsv)
            d2 = Color.dist(c1, c2, space="hsv")
            Assert(d1 == d2)
            # hls
            d1 = f(c1.dhls, c2.dhls)
            d2 = Color.dist(c1, c2, space="hls")
            Assert(d1 == d2)
            # Distance from self is always zero
            for i in "rgb hsv hls".split():
                Assert(Color.dist(c1, c1, space=i) == 0)
                Assert(Color.dist(c2, c2, space=i) == 0)
        def TestSort():
            Reset()
            if 1:   # Sorting
                a = Color(12, 6, 247)
                b = Color(168, 255, 4)
                c = Color(252, 252, 129)
                seq = (a, b, c)
                # Sort on r; sequence should be unchanged
                seq1 = Color.Sort(seq, keys="r")
                Assert(seq == seq1)
                # Sort on g
                seq1 = Color.Sort(seq, keys="g")
                Assert(seq1 == (a, c, b))
                # Sort on b
                seq1 = Color.Sort(seq, keys="b")
                Assert(seq1 == (b, c, a))
                # Sort on L
                seq1 = Color.Sort(seq, keys="L")
                Assert(seq == seq1)
                # Sort on h
                seq1 = Color.Sort(seq, keys="h")
                Assert(seq1 == (c, b, a))
                # Sort on s
                seq1 = Color.Sort(seq, keys="s")
                Assert(seq1 == (c, a, b))
                # Sort on S
                seq1 = Color.Sort(seq, keys="S")
                Assert(seq1 == (a, c, b))
            if 1:   # Test with predicate 
                a = Color(12, 6, 247)
                b = Color(168, 255, 4)
                seq = (
                    ("bob", b),
                    ("alice", a),
                )
                def f(x):
                    return x[1]
                seq1 = Color.Sort(seq, keys="r", get=f)
                Assert(seq1[0] == ("alice", a))
                Assert(seq1[1] == ("bob", b))
            if 1:   # Test the < operator
                a = Color("#000000")
                b = Color("#010000")
                Assert(a < b)
                Assert(not (b < a))
                Assert(not (a < a))
                Assert(not (b < b))
        def TestClassMethods():
            if 1:   # convert_hex
                f = Color.hex_to_int
                g = Color.int_to_hex
                for arg, expected in (
                        ("000000", (0, 0, 0)),
                        ("010203", (1, 2, 3)),
                        ("fefefe", (0xfe, 0xfe, 0xfe)),
                        ("ffffff", (0xff, 0xff, 0xff)),
                        ("000000000000", (0, 0, 0)),
                        ("000100020003", (1, 2, 3)),
                        ("00ff00ff00ff", (0xff, 0xff, 0xff)),
                        ("ffffffffffff", (0xffff, 0xffff, 0xffff)),
                        ):
                    bytes_per_color = len(arg)//6
                    Assert(f(arg) == expected)
                    got = g(expected, bytes_per_color)
                    Assert(got == arg)
                raises(TypeError, f, 0)
                raises(ValueError, f, "12345")
                raises(ValueError, f, "1234567890")
                raises(ValueError, f, "00000g")
            if 1:   # round
                f = Color.round
                pi = math.pi
                for arg, digits, expected in (
                        (pi, 1, round(pi, 1)),
                        (pi, 2, round(pi, 2)),
                        (pi, 3, round(pi, 3)),
                        (pi, 4, round(pi, 4)),
                        (pi, 5, round(pi, 5)),
                        ):
                    Assert(f(pi, digits) == expected)
                # Test sequence
                seq = [pi, pi, pi]
                seq1 = f(seq, digits)
                a = round(pi, digits)
                Assert(seq1 == (a, a, a))
            if 1:   # Dot
                f = Color.Dot
                a, b = (1, 2, 3), (3, 2, 1)
                Assert(f(a, b) == 10)
            if 1:   # XYZ_to_sRGB
                def GammaCompressed(x):
                    return 12.92*x if x <= 0.0031308 else 1.055*x**(1/2.4) - 0.055
                f = Color.XYZ_to_sRGB
                XYZ = (1, 1, 1)
                got = f(XYZ)
                r1 = sum((+3.2406, -1.5372, -0.4986))
                r2 = sum((-0.9689, +1.8758, +0.0415))
                r3 = sum((+0.0557, -0.2040, +1.0570))
                expected = (r1, r2, r3)
                def clip(x):
                    return min(1.0, max(x, 0.0))
                expected = tuple(clip(GammaCompressed(i)) for i in expected)
                Assert(got == expected)
            if 1:   # wl2rgb
                f = Color.wl2rgb
                T, F = True, False
                raises(TypeError, f, "a")
                raises(ValueError, f, 0)
                raises(TypeError, f, 1, gamma="")
                raises(ValueError, f, 1, gamma=-1)
                # Using the spectrum of sunlight
                Assert(f(1.1, sunlight=T) == Color(0, 0, 0))
                Assert(f(399, sunlight=T) == Color(0, 0, 0))
                # About the sodium D line
                Assert(f(589, sunlight=T) == Color(246, 195, 0, bpc=8))
                Assert(f(701, sunlight=T) == Color(0, 0, 0))
                # Bruton's approximation
                low, high = 379, 781
                Assert(f(1.1, sunlight=F) == Color(0, 0, 0))
                Assert(f(low, sunlight=F) == Color(0, 0, 0))
                # About the sodium D line
                x = f(589, sunlight=F)
                Assert(f(589, sunlight=F) == Color(255, 219, 0, bpc=8))
                Assert(f(high, sunlight=F) == Color(0, 0, 0))
        def TestProperties():
            # Integer conversions should remain exact.  Check by testing some
            # samples.
            Reset()
            for bpc in (8, 10):
                Color.bits_per_color = bpc
                n = 2**bpc - 1
                R = range(0, n, n//10)
                for i in R:
                    for j in R:
                        for k in R:
                            a = (i, j, k)
                            c = Color(*a)
                            Assert(c.irgb == a)
            Reset()
            # Properties return 3-tuples
            c = Color(1, 2, 3)
            Assert(ii(c.irgb, tuple) and len(c.irgb) == 3)
            Assert(ii(c.drgb, tuple) and len(c.drgb) == 3)
            Assert(ii(c.ihsv, tuple) and len(c.irgb) == 3)
            Assert(ii(c.dhsv, tuple) and len(c.drgb) == 3)
            Assert(ii(c.ihls, tuple) and len(c.ihls) == 3)
            Assert(ii(c.dhls, tuple) and len(c.dhls) == 3)
            # Hex string properties return proper hex forms
            s, n = c.xrgb, 7
            Assert(ii(s, str) and len(s) == n and s[0] == "#")
            s = c.xhsv
            Assert(ii(s, str) and len(s) == n and s[0] == "@")
            s = c.xhls
            Assert(ii(s, str) and len(s) == n and s[0] == "$")
        def Test1ArgColorConstructor():
            Reset()
            if 1:   # Color instance:  make a copy
                c = Color(0.1, 0.2, 0.3)
                c1 = Color(c)
                Assert(c.drgb == c1.drgb)
            if 1:   # Hex strings
                for i in "@#$":
                    c = Color(f"{i}000000")
                    Assert(c.irgb == (0, 0, 0))
                c = Color(f"#010203")
                Assert(c.irgb == (1, 2, 3))
                # Note the HSV and HLS transformations can lose a little
                # information because of conversion between ints and floats.
                c = Color(f"@010203")
                Assert(c.ihsv == (0, 0, 3))
                c = Color(f"@808080")
                Assert(c.ihsv == (128, 129, 128))
                Assert(c.ihls == (128, 95, 86))
                c = Color(f"$010203")
                Assert(c.ihls == (0, 2, 0))
            if 1:   # Single number:  wavelength in nm or gray
                # Wavelengths
                c = Color(589)  # About sodium yellow-orange
                rgb = tuple(round(i, 3) for i in c.drgb)
                Assert(rgb == (0.965, 0.765, 0.000))
                black = (0.0, 0.0, 0.0)
                c = Color(300)
                Assert(c.irgb == black)
                c = Color(800)
                Assert(c.irgb == black)
                # Grays
                for a, b in (
                        (0.0, 0.0),
                        (0.1, 0.098),
                        (0.2, 0.2),
                        (0.3, 0.298),
                        (0.4, 0.4),
                        (0.5, 0.498),
                        (0.6, 0.6),
                        (0.7, 0.698),
                        (0.8, 0.8),
                        (0.9, 0.898),
                        (1.0, 1.0)):
                    c = Color(a, a, a)
                    rgb = tuple(round(i, 3) for i in c.drgb)
                    Assert(rgb == (b, b, b))
        def Test3ArgsColorConstructor():
            Reset()
            if 1:   # Integer arguments
                for a in (0, 1, 2, 255, 256):
                    b = (a, a, a)
                    c = Color(*b)
                    expected = tuple(i & c.n for i in b)
                    Assert(c.irgb == expected)
                # Works for 10-bit arguments
                Color.bits_per_color = 10
                a = 1023
                b = (a, a, a)
                c = Color(*b)
                Assert(c.irgb == b)
                Reset()
            if 1:   # Float arguments
                for a, e in (
                        (0.0, 0.0), 
                        (0.0039, 0.0039),
                        (0.5, 0.498),
                        (0.9999, 1.0),
                        (1.0, 1.0),
                        ):
                    b = (a, a, a)
                    c = Color(*b)
                    got = tuple(round(i, 4) for i in c.drgb)
                    expected = (e, e, e)
                    Assert(got == expected)
            if 1:   # Normalization of floats
                a = 1.0001
                t = (a, a, a)
                c = Color(*t)
                mag = sum(i*i for i in t)**(1/2)
                dec = tuple(i/mag for i in t)
                rgb = c.dec_to_int(dec)
                Assert(c.irgb == rgb)
                a = (0.99999, 1.00001, 1.0)
                c = Color(*a)
                mag = sum(i*i for i in t)**(1/2)
                dec = tuple(i/mag for i in t)
                rgb = c.dec_to_int(dec)
                Assert(c.irgb == rgb)
            if 1:   # Fraction arguments
                for n, d, e in (
                        (0, 1, 0.0),
                        (1, 2, 0.498),
                        (2, 3, 0.667),
                        (1, 1, 1.0)
                        ):
                    a = Fraction(n, d)
                    c = Color(a, a, a)
                    got = tuple(round(i, 3) for i in c.drgb)
                    expected = (e, e, e)
                    Assert(got == expected)
            if 1:   # Decimal arguments
                for x, e in (
                        ("0", 0.0),
                        ("0.5", 0.498),
                        ("0.666667", 0.667),
                        ("1.0", 1.0)):
                    a = Decimal(x)
                    c = Color(a, a, a)
                    got = tuple(round(i, 3) for i in c.drgb)
                    expected = (e, e, e)
                    Assert(got == expected)
            if 1:   # mpmath.mpf arguments
                if have_mpmath:
                    for x, e in (
                            ("0", 0.0),
                            ("0.5", 0.498),
                            ("0.666667", 0.667),
                            ("1.0", 1.0)):
                        a = mpmath.mpf(x)
                        c = Color(a, a, a)
                        got = tuple(round(i, 3) for i in c.drgb)
                        expected = (e, e, e)
                        Assert(got == expected)
            if 1:   # Bad forms
                raises(TypeError, Color, "4", 4, 4)
                raises(TypeError, Color, Decimal("4"), 4, 4)
                raises(TypeError, Color, 4.0, 4, 4)
                raises(TypeError, Color, Fraction(4, 1), 4, 4)
        def TestConstructorKeywords():
            kw = {"bpc": 8, "hsv": 0, "hls": 0, "sunlight": 0, "gamma": 0}
            c = Color(0, 0, 0, **kw)
            bkw = {"aaa": 0, "bbb": 0}
            raises(ValueError, Color, 0, 0, 0, **bkw)
        def Test_int_to_hex():
            '''This checks that int_to_hex and hex_to_int are inverse for all
            numbers < 0x10000.
            '''
            n = 0x10000
            for i in range(n):
                a = max(i - 1, 0)
                b = i
                c = min(i, n)
                d = (a, b, c)
                x = Color.int_to_hex(d)
                y = Color.hex_to_int(x)
                Assert(y == d)
        def TestHash():
            a, bpc = (18, 3333, 3578457), 28
            c = Color(*a, bpc=bpc)
            got = hash(c)
            expected = hash((a, bpc))
            Assert(got == expected)
        def TestInvariants():
            '''Make sure things like
                c = Color('mag')
                c1 = Color(c.xhls)
                assert(c == c1)
            are true.
            '''
            from f import flt
            distances = [] 
            for i in GetShortNames(all=True):
                c = Color(i)
                c1 = Color(c.xhls)
                if c != c1:
                    dist = flt(Color.dist(c, c1))
                    distances.append(dist)
                    Assert(dist < 0.014)
                    #print(f"Failed for {i}:  {c} {c1} dist={dist}")
            if 0 and distances:
                # Note max possible distance value is 1.  Max is 0.0136 for
                # vio.  So, it's either ignore any dist < 0.014 or see if the
                # calculations with Fractions produces better conversions.
                print(f"Max dist = {max(distances)}")
                print("Tests failed")
                exit(1)
        if 1:
            Test_short_color_names()
            Test_change_bpc()
            TestAttributes()
            Test_downshift()
            Test_dist()
            TestEquality()
            TestInterpolate()
            TestConstruct()
            TestDistance()
            TestSort()
            TestClassMethods()
            TestProperties()
            Test1ArgColorConstructor()
            Test3ArgsColorConstructor()
            TestConstructorKeywords()
            Test_int_to_hex()
            TestHash()
            Test_adjust()
            TestInvariants()
    if 1:   # Example stuff
        def ShowAttributes():
            c = Trm()
            def f(a):
                return c(attr=a)
            print(dedent(f'''
            Text attributes (e.g., t('ornl', attr="ul"))
                ('hide' is to the right of 'dim')
                {f("no")}normal      no{c.n}       {f("bo")}bold        bo{c.n}
                {f("it")}italic      it{c.n}       {f("ul")}underline   ul{c.n}
                {f("bl")}blink       bl{c.n}       {f("rb")}rapidblink  rb{c.n}
                {f("rv")}reverse     rv{c.n}       {f("so")}strikeout   so{c.n}
                {f("di")}dim         di{c.n}       {f("hi")}hide         hi{c.n}
                sub{f("sb")}script   {c.n}sb       super{f("sp")}script {c.n}sp
            '''.rstrip()))
        def ColorTable(bits):
            c = Trm()
            width = int(os.environ["COLUMNS"])
            def H(bright=False):
                c.out(f"{'':{w}s} ")
                for i in T:
                    if bright:
                        c.out(f"{c('whtl')}{'l' + i:{w}s}{c.n} ")
                    else:
                        c.out(f"{c('wht')}{i:{w}s}{c.n} ")
                print()
            def Tbl(msg, fg=False, bg=False, last=True):
                print(f"{c('yell')}{msg:^{W}s}{c.n}")
                H("l" if bg else "")
                for i in T:
                    if fg:
                        i = i + "l"
                        c.out(f"{c('whtl')}{i:{w}s}{c.n} ")
                    else:
                        c.out(f"{c('wht')}{i:{w}s}{c.n} ")
                    for j in T:
                        j = j + "l" if bg else j
                        c.out(f"{c(i, j)}{t}{c.n} ")
                    print()
                if last:
                    print()
            T = "blk  blu grn  cyn  red  mag  yel  wht".split()
            w, t = 4, "text"
            W = 44
            term = os.environ["TERM_PROGRAM"]
            print(f"Running on a {term} terminal")
            if bits == 24:
                Tbl("Dim text, dim background", False, False)
                Tbl("Bright text, dim background", True, False)
                Tbl("Dim text, bright background", False, True)
                Tbl("Bright text, bright background", True, True, last=False)
                c.out(c.n)
            elif bits == 4:
                Tbl("Dim text", False, False)
                Tbl("Bright text", True, False, last=False)
            elif bits == 8:
                print("8 bit not working yet")
                if 0:
                    T = range(256)
                    N = width//4        # Items that can fit per line
                    use_white = set([int(i) for i in '''
                        0 4 8 16 17 18 19 20 21 52 53 54 55 56 57 88 89 90 91 92 93 94
                        95 96 97 98 99 232 233 234 235 236 237 238 239
                            '''.split()])
                    print("As foreground colors")
                    for i in T:
                        c.out(f"{c(i)}{i:^4d}")
                        if i and not ((i + 1) % N):
                            c.print()
                    c.print()
                    print("As background colors")
                    for i in T:
                        fg = 15 if i in use_white else 0
                        c.out(f"{c(fg, i)}{i:^4d}")
                        if i and not ((i + 1) % N):
                            c.print()
                    c.print()
        def Examples():
            # These work under mintty (https://mintty.github.io/)
            '''
            - theme example with Trm.load()
            - regexp matches
            - Unicode in sub/superscripts (e.g., Hz**(1/2)
            '''
            c = Trm(bits=24)
            c.hdr = c(attr="ul")
            def Header():
                c.print(dedent(f'''
                {c.hdr}Demonstration of some color.py features{c.n}
 
                '''))
            def Theme():
                x = Trm()
                s = "This {ul}truth{n} is well-{em}fixed{n} in our minds."
                x.print(dedent(f'''
                    {c.hdr}Themes{x.n}
                    This example shows how standardizing some style names can be used to change
                    "themes" with the Trm.load() method.  We'll use the style names 'em' and
                    'ul'. The sentence is "{s}"
                    The older string interpolation method of str.format() is used so that the
                    single instance of the string can be used (normally, I like to use f-strings
                    because of the brevity).
 
                    The first "theme" will use underlining for the ul style and 'yell' text for
                    the em style:
                '''))
                # Load the first theme
                theme1 = dedent('''
                    ul None None ul
                    em yell None
                ''')
                x.load(theme1)
                d = {"ul": x.ul, "em": x.em, "n": x.n}
                x.print("\n    First  style: ", s.format(**d))
                # Load the second theme
                x.print(dedent(f'''
 
                    The second "theme" will use reversed 'yell' text for the ul style and 
                    italics for the em style:
                '''))
                theme2 = dedent('''
                    ul yell None rv
                    em None None it
                ''')
                x.load(theme2)
                d = {"ul": x.ul, "em": x.em, "n": x.n}
                x.print("\n    Second style: ", s.format(**d))
            def Exponents():
                n = c.n
                cl = Color("yell")
                e = c(cl)
                u = c(cl, attr="sp")
                b = c(cl, attr="sb")
                c.print(dedent(f'''
                    {c.hdr}Exponents{c.n}
                    The mintty terminal can display exponents and subscripts, even using Unicode
                    characters.
 
                        SI units: kg/(m·s²)
                            With built-in Unicode:      {e}ξ{b}λ{n}{e} = 3 kg·m⁻¹·s⁻²{c.n}
                            With superscripts:          {e}ξ{b}λ{n}{e} = 3 kg·m{u}-1{c.n}{e}·s{u}-2{c.n}
                            (Unicode looks better, but Unicode doesn't support 'obvious'
                            exponent characters.  Here's an example with mintty (doesn't
                            work under Windows Terminal):
                                                        {e}ξ{b}λ{n}{e} = 3 kg·m{u}θ{c.n}{e}·s{u}μ²{c.n}
                '''))
            def TextEditing():
                cl = Color("grnl")
                n, a, d = c.n, c(cl), c(None, None, attr="so")
                c.print(dedent(f'''
 
                    {c.hdr}Text editing{c.n}
                    Using a green color for added text and strikethrough for deleted text, you can
                    show how some text has been edited:
            
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                '''))
                cl = Color("redl")
                d = c(cl, attr="so")
                c.print(dedent(f'''
 
                    The strikethrough text can be hard to see.  A quick change adds a red color:
 
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                '''))
                print()
            Header()
            #Theme()
            Exponents()
            TextEditing()
        def ShortNames():
            '''The default set of color names comes from the colorname0
            file.  The 12 basic names are the 10 resistor color code names
            of blk, brn, red, orn, yel, grn, blu, vio, gry, wht and the
            added colors cyn for cyan and mag for magenta.  Three suffixes
            give 12 more colors each:  'l' for 'light', 'd' for 'dark', and
            'b' for background.  An auxiliary 12 more colors are also
            defined.  Each of these colors is printed out with foreground
            and background text to show their effect.
            '''
            R = GetShortNames()
            c = Trm()
            # Make escape codes always be printed so that capturing to a
            # file lets you grab the escape codes easily.
            c.always = True
            w = 5
            cn = CN
            print("Grays:", end=" "*2)
            for i in range(1, 11):
                k = Color(i/10)
                s = str(i/10)
                print(f"{c(k)}{s:{w}s}{c.n}", end=" ")
            print()
            # Print out one color per line
            w, sp, a = 4, 2, "ul it"
            print(f"{' '*12}{c('whtl', attr=a)}Foregrounds{c.n}", end="")
            print(f"{' '*12}{c('whtl', attr=a)}Backgrounds{c.n}")
            for i in R:
                # Foregrounds
                print(f"{i:{w}s}", end=" "*3)
                print(f"{c(cn[i])}{i:{w}s}{c.n}", end=" "*sp)
                for j in "ldb":
                    k = i + j
                    print(f"{c(cn[k])}{k:{w}s}{c.n}", end=" "*sp)
                # Backgrounds
                print(f"{c('blk', cn[i])}{i:{w}s}{c.n}", end=" "*sp)
                for j in "ldb":
                    k = i + j
                    print(f"{c('blk', cn[k])}{k:{w}s}{c.n}", end=" "*sp)
                print()
            print(dedent(f'''
 
                Examples:
                    t(Color(0.35)) gives a {t(Color(0.35))}gray like this{t.n}
                    t('ornl') gives an {t('ornl')}orange like this{t.n}
                    t('ornl', 'royd') gives an {t('ornl', 'royd')}orange on a royd background{t.n}
                    t('blk', 'yel', attr="rb") gives a {t('blk', 'yel', attr="rb")}rapid blink{t.n}
                    Blinking doesn't work in WSL
            '''))
    def Int(s):
        'Convert s to an integer; 0x33 and 0o33 forms allowed'
        s = s.strip()
        if s.startswith("0x"):
            return int(s, 16)
        elif s.startswith("0o"):
            return int(s, 8)
        elif s.startswith("0b"):
            return int(s, 2)
        else:
            return int(s)
    def InterpretColorSpecifier(s):
        '''s will be a string of one of the following forms:
            1.  One of the short names such as 'ornl'
            2.  #XXXXXX, @XXXXXX, and $XXXXXX hex forms
            3.  "a b c" where the letters represent integers
        Instead of space characters, nearly any characters can be used as
        delimiters, as they are replaced by spaces.
        '''
        x = s.strip()
        if not x:
            return
        # Replace nearly all delimiters
        for i in "~!%^&*()_-+=|{}[}:;\"'<>,?/":
            x = x.replace(i, " ")
        while "  " in x:
            x = x.replace("  ", " ")
        # Set the variable rgb to a tuple of 3 base 10 integers
        if len(x) in (3, 4):
            # Short name form
            try:
                c = CN[x]
                rgb = c.irgb
            except Exception:
                Error(f"'{x}' not recognized as a color name")
            t.print(f"Color name '{x}'    {t(c)}Represents this color")
            ShowRepresentations(c)
            return
        elif x[0] in "@#$":
            c = Color(x)
            rgb = c.irgb
        else:
            # Must be 3 RGB numbers separated by white space (either
            # integers or floats)
            if "." in x or "e" in x:
                # Interpret as floats
                rgb = [Int(255*float(i)) for i in x.split()]
            else:
                # Interpret as ints
                rgb = [Int(i) for i in x.split()]
        if len(rgb) != 3:
            Error(f"'{x!s}' doesn't represent three numbers")
        PrintRGB(s, x, rgb)
    def ShowRepresentations(c):
        'Show the Color instance c in various representations'
        q = "({:3d}, {:3d}, {:3d})"
        def dec(c):
            'c is a Color instance; return decimal string form'
            Assert(ii(c, Color))
            s = c.drgb
            t = tuple(f"{i:5.3f}" for i in c.drgb)
            return f"({', '.join(t)})"
        def P(x, name):
            'x is an integer tuple and name is RGB, HSV, or HLS'
            if name == "RGB":
                s = q.format(*c.irgb)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xrgb!s}")
            elif name == "HSV":
                s = q.format(*c.ihsv)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xhsv!s}")
            elif name == "HLS":
                s = q.format(*c.ihls)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xhls!s}")
            else:
                Error(f"'{name}' is bad")
        P(c.irgb, "RGB")
        P(c.ihsv, "HSV")
        P(c.ihls, "HLS")
    def PrintRGB(orig, x, rgb):
        'Show the color in various forms'
        q = "({:3d}, {:3d}, {:3d})"
        def dec(c):
            'c is a Color instance; return decimal string form'
            Assert(ii(c, Color))
            s = c.drgb
            t = tuple(f"{i:5.3f}" for i in c.drgb)
            return f"({', '.join(t)})"
        def P(x, name):
            'x is an integer tuple and name is RGB, HSV, or HLS'
            if name == "RGB":
                s = q.format(*c.irgb)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xrgb!s}")
            elif name == "HSV":
                s = q.format(*c.ihsv)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xhsv!s}")
            elif name == "HLS":
                s = q.format(*c.ihls)
                print(f"  {name} = {s} = {dec(Color(*x))} = {c.xhls!s}")
            else:
                Error(f"'{name}' is bad")
        # Check that it's a 3-tuple of integers
        Assert(len(rgb) == 3)
        Assert(all([ii(i, int) for i in rgb]))
        c = Color(*rgb)
        t.print(f"Input string = '{orig}' = {t(c)}{x.strip()}")
        P(c.irgb, "RGB")
        P(c.ihsv, "HSV")
        P(c.ihls, "HLS")
    def Print256Colors():
        '''An 8-bit color xterm only uses 256 colors.
 
        https://www.ditig.com/publications/256-colors-cheat-sheet gave a
        table translating an 8-bit color code to #XXXXXX, RGB, and HSL
        representations.  This table is used to translate an 8-bit number
        to an RGB represenation (the table was screen-scraped and is
        tab-separated.  Downloaded Sat 27 Jan 2024 11:14:21 AM.
        '''
        data = '''
            Display	Xterm Number	Xterm Name	HEX	RGB	HSL
            0	Black (SYSTEM)	#000000	rgb(0,0,0)	hsl(0,0%,0%)
            1	Maroon (SYSTEM)	#800000	rgb(128,0,0)	hsl(0,100%,25%)
            2	Green (SYSTEM)	#008000	rgb(0,128,0)	hsl(120,100%,25%)
            3	Olive (SYSTEM)	#808000	rgb(128,128,0)	hsl(60,100%,25%)
            4	Navy (SYSTEM)	#000080	rgb(0,0,128)	hsl(240,100%,25%)
            5	Purple (SYSTEM)	#800080	rgb(128,0,128)	hsl(300,100%,25%)
            6	Teal (SYSTEM)	#008080	rgb(0,128,128)	hsl(180,100%,25%)
            7	Silver (SYSTEM)	#c0c0c0	rgb(192,192,192)	hsl(0,0%,75%)
            8	Grey (SYSTEM)	#808080	rgb(128,128,128)	hsl(0,0%,50%)
            9	Red (SYSTEM)	#ff0000	rgb(255,0,0)	hsl(0,100%,50%)
            10	Lime (SYSTEM)	#00ff00	rgb(0,255,0)	hsl(120,100%,50%)
            11	Yellow (SYSTEM)	#ffff00	rgb(255,255,0)	hsl(60,100%,50%)
            12	Blue (SYSTEM)	#0000ff	rgb(0,0,255)	hsl(240,100%,50%)
            13	Fuchsia (SYSTEM)	#ff00ff	rgb(255,0,255)	hsl(300,100%,50%)
            14	Aqua (SYSTEM)	#00ffff	rgb(0,255,255)	hsl(180,100%,50%)
            15	White (SYSTEM)	#ffffff	rgb(255,255,255)	hsl(0,0%,100%)
            16	Grey0	#000000	rgb(0,0,0)	hsl(0,0%,0%)
            17	NavyBlue	#00005f	rgb(0,0,95)	hsl(240,100%,18%)
            18	DarkBlue	#000087	rgb(0,0,135)	hsl(240,100%,26%)
            19	Blue3	#0000af	rgb(0,0,175)	hsl(240,100%,34%)
            20	Blue3	#0000d7	rgb(0,0,215)	hsl(240,100%,42%)
            21	Blue1	#0000ff	rgb(0,0,255)	hsl(240,100%,50%)
            22	DarkGreen	#005f00	rgb(0,95,0)	hsl(120,100%,18%)
            23	DeepSkyBlue4	#005f5f	rgb(0,95,95)	hsl(180,100%,18%)
            24	DeepSkyBlue4	#005f87	rgb(0,95,135)	hsl(97,100%,26%)
            25	DeepSkyBlue4	#005faf	rgb(0,95,175)	hsl(07,100%,34%)
            26	DodgerBlue3	#005fd7	rgb(0,95,215)	hsl(13,100%,42%)
            27	DodgerBlue2	#005fff	rgb(0,95,255)	hsl(17,100%,50%)
            28	Green4	#008700	rgb(0,135,0)	hsl(120,100%,26%)
            29	SpringGreen4	#00875f	rgb(0,135,95)	hsl(62,100%,26%)
            30	Turquoise4	#008787	rgb(0,135,135)	hsl(180,100%,26%)
            31	DeepSkyBlue3	#0087af	rgb(0,135,175)	hsl(93,100%,34%)
            32	DeepSkyBlue3	#0087d7	rgb(0,135,215)	hsl(02,100%,42%)
            33	DodgerBlue1	#0087ff	rgb(0,135,255)	hsl(08,100%,50%)
            34	Green3	#00af00	rgb(0,175,0)	hsl(120,100%,34%)
            35	SpringGreen3	#00af5f	rgb(0,175,95)	hsl(52,100%,34%)
            36	DarkCyan	#00af87	rgb(0,175,135)	hsl(66,100%,34%)
            37	LightSeaGreen	#00afaf	rgb(0,175,175)	hsl(180,100%,34%)
            38	DeepSkyBlue2	#00afd7	rgb(0,175,215)	hsl(91,100%,42%)
            39	DeepSkyBlue1	#00afff	rgb(0,175,255)	hsl(98,100%,50%)
            40	Green3	#00d700	rgb(0,215,0)	hsl(120,100%,42%)
            41	SpringGreen3	#00d75f	rgb(0,215,95)	hsl(46,100%,42%)
            42	SpringGreen2	#00d787	rgb(0,215,135)	hsl(57,100%,42%)
            43	Cyan3	#00d7af	rgb(0,215,175)	hsl(68,100%,42%)
            44	DarkTurquoise	#00d7d7	rgb(0,215,215)	hsl(180,100%,42%)
            45	Turquoise2	#00d7ff	rgb(0,215,255)	hsl(89,100%,50%)
            46	Green1	#00ff00	rgb(0,255,0)	hsl(120,100%,50%)
            47	SpringGreen2	#00ff5f	rgb(0,255,95)	hsl(42,100%,50%)
            48	SpringGreen1	#00ff87	rgb(0,255,135)	hsl(51,100%,50%)
            49	MediumSpringGreen	#00ffaf	rgb(0,255,175)	hsl(61,100%,50%)
            50	Cyan2	#00ffd7	rgb(0,255,215)	hsl(70,100%,50%)
            51	Cyan1	#00ffff	rgb(0,255,255)	hsl(180,100%,50%)
            52	DarkRed	#5f0000	rgb(95,0,0)	hsl(0,100%,18%)
            53	DeepPink4	#5f005f	rgb(95,0,95)	hsl(300,100%,18%)
            54	Purple4	#5f0087	rgb(95,0,135)	hsl(82,100%,26%)
            55	Purple4	#5f00af	rgb(95,0,175)	hsl(72,100%,34%)
            56	Purple3	#5f00d7	rgb(95,0,215)	hsl(66,100%,42%)
            57	BlueViolet	#5f00ff	rgb(95,0,255)	hsl(62,100%,50%)
            58	Orange4	#5f5f00	rgb(95,95,0)	hsl(60,100%,18%)
            59	Grey37	#5f5f5f	rgb(95,95,95)	hsl(0,0%,37%)
            60	MediumPurple4	#5f5f87	rgb(95,95,135)	hsl(240,17%,45%)
            61	SlateBlue3	#5f5faf	rgb(95,95,175)	hsl(240,33%,52%)
            62	SlateBlue3	#5f5fd7	rgb(95,95,215)	hsl(240,60%,60%)
            63	RoyalBlue1	#5f5fff	rgb(95,95,255)	hsl(240,100%,68%)
            64	Chartreuse4	#5f8700	rgb(95,135,0)	hsl(7,100%,26%)
            65	DarkSeaGreen4	#5f875f	rgb(95,135,95)	hsl(120,17%,45%)
            66	PaleTurquoise4	#5f8787	rgb(95,135,135)	hsl(180,17%,45%)
            67	SteelBlue	#5f87af	rgb(95,135,175)	hsl(210,33%,52%)
            68	SteelBlue3	#5f87d7	rgb(95,135,215)	hsl(220,60%,60%)
            69	CornflowerBlue	#5f87ff	rgb(95,135,255)	hsl(225,100%,68%)
            70	Chartreuse3	#5faf00	rgb(95,175,0)	hsl(7,100%,34%)
            71	DarkSeaGreen4	#5faf5f	rgb(95,175,95)	hsl(120,33%,52%)
            72	CadetBlue	#5faf87	rgb(95,175,135)	hsl(150,33%,52%)
            73	CadetBlue	#5fafaf	rgb(95,175,175)	hsl(180,33%,52%)
            74	SkyBlue3	#5fafd7	rgb(95,175,215)	hsl(200,60%,60%)
            75	SteelBlue1	#5fafff	rgb(95,175,255)	hsl(210,100%,68%)
            76	Chartreuse3	#5fd700	rgb(95,215,0)	hsl(3,100%,42%)
            77	PaleGreen3	#5fd75f	rgb(95,215,95)	hsl(120,60%,60%)
            78	SeaGreen3	#5fd787	rgb(95,215,135)	hsl(140,60%,60%)
            79	Aquamarine3	#5fd7af	rgb(95,215,175)	hsl(160,60%,60%)
            80	MediumTurquoise	#5fd7d7	rgb(95,215,215)	hsl(180,60%,60%)
            81	SteelBlue1	#5fd7ff	rgb(95,215,255)	hsl(195,100%,68%)
            82	Chartreuse2	#5fff00	rgb(95,255,0)	hsl(7,100%,50%)
            83	SeaGreen2	#5fff5f	rgb(95,255,95)	hsl(120,100%,68%)
            84	SeaGreen1	#5fff87	rgb(95,255,135)	hsl(135,100%,68%)
            85	SeaGreen1	#5fffaf	rgb(95,255,175)	hsl(150,100%,68%)
            86	Aquamarine1	#5fffd7	rgb(95,255,215)	hsl(165,100%,68%)
            87	DarkSlateGray2	#5fffff	rgb(95,255,255)	hsl(180,100%,68%)
            88	DarkRed	#870000	rgb(135,0,0)	hsl(0,100%,26%)
            89	DeepPink4	#87005f	rgb(135,0,95)	hsl(17,100%,26%)
            90	DarkMagenta	#870087	rgb(135,0,135)	hsl(300,100%,26%)
            91	DarkMagenta	#8700af	rgb(135,0,175)	hsl(86,100%,34%)
            92	DarkViolet	#8700d7	rgb(135,0,215)	hsl(77,100%,42%)
            93	Purple	#8700ff	rgb(135,0,255)	hsl(71,100%,50%)
            94	Orange4	#875f00	rgb(135,95,0)	hsl(2,100%,26%)
            95	LightPink4	#875f5f	rgb(135,95,95)	hsl(0,17%,45%)
            96	Plum4	#875f87	rgb(135,95,135)	hsl(300,17%,45%)
            97	MediumPurple3	#875faf	rgb(135,95,175)	hsl(270,33%,52%)
            98	MediumPurple3	#875fd7	rgb(135,95,215)	hsl(260,60%,60%)
            99	SlateBlue1	#875fff	rgb(135,95,255)	hsl(255,100%,68%)
            100	Yellow4	#878700	rgb(135,135,0)	hsl(60,100%,26%)
            101	Wheat4	#87875f	rgb(135,135,95)	hsl(60,17%,45%)
            102	Grey53	#878787	rgb(135,135,135)	hsl(0,0%,52%)
            103	LightSlateGrey	#8787af	rgb(135,135,175)	hsl(240,20%,60%)
            104	MediumPurple	#8787d7	rgb(135,135,215)	hsl(240,50%,68%)
            105	LightSlateBlue	#8787ff	rgb(135,135,255)	hsl(240,100%,76%)
            106	Yellow4	#87af00	rgb(135,175,0)	hsl(3,100%,34%)
            107	DarkOliveGreen3	#87af5f	rgb(135,175,95)	hsl(90,33%,52%)
            108	DarkSeaGreen	#87af87	rgb(135,175,135)	hsl(120,20%,60%)
            109	LightSkyBlue3	#87afaf	rgb(135,175,175)	hsl(180,20%,60%)
            110	LightSkyBlue3	#87afd7	rgb(135,175,215)	hsl(210,50%,68%)
            111	SkyBlue2	#87afff	rgb(135,175,255)	hsl(220,100%,76%)
            112	Chartreuse2	#87d700	rgb(135,215,0)	hsl(2,100%,42%)
            113	DarkOliveGreen3	#87d75f	rgb(135,215,95)	hsl(100,60%,60%)
            114	PaleGreen3	#87d787	rgb(135,215,135)	hsl(120,50%,68%)
            115	DarkSeaGreen3	#87d7af	rgb(135,215,175)	hsl(150,50%,68%)
            116	DarkSlateGray3	#87d7d7	rgb(135,215,215)	hsl(180,50%,68%)
            117	SkyBlue1	#87d7ff	rgb(135,215,255)	hsl(200,100%,76%)
            118	Chartreuse1	#87ff00	rgb(135,255,0)	hsl(8,100%,50%)
            119	LightGreen	#87ff5f	rgb(135,255,95)	hsl(105,100%,68%)
            120	LightGreen	#87ff87	rgb(135,255,135)	hsl(120,100%,76%)
            121	PaleGreen1	#87ffaf	rgb(135,255,175)	hsl(140,100%,76%)
            122	Aquamarine1	#87ffd7	rgb(135,255,215)	hsl(160,100%,76%)
            123	DarkSlateGray1	#87ffff	rgb(135,255,255)	hsl(180,100%,76%)
            124	Red3	#af0000	rgb(175,0,0)	hsl(0,100%,34%)
            125	DeepPink4	#af005f	rgb(175,0,95)	hsl(27,100%,34%)
            126	MediumVioletRed	#af0087	rgb(175,0,135)	hsl(13,100%,34%)
            127	Magenta3	#af00af	rgb(175,0,175)	hsl(300,100%,34%)
            128	DarkViolet	#af00d7	rgb(175,0,215)	hsl(88,100%,42%)
            129	Purple	#af00ff	rgb(175,0,255)	hsl(81,100%,50%)
            130	DarkOrange3	#af5f00	rgb(175,95,0)	hsl(2,100%,34%)
            131	IndianRed	#af5f5f	rgb(175,95,95)	hsl(0,33%,52%)
            132	HotPink3	#af5f87	rgb(175,95,135)	hsl(330,33%,52%)
            133	MediumOrchid3	#af5faf	rgb(175,95,175)	hsl(300,33%,52%)
            134	MediumOrchid	#af5fd7	rgb(175,95,215)	hsl(280,60%,60%)
            135	MediumPurple2	#af5fff	rgb(175,95,255)	hsl(270,100%,68%)
            136	DarkGoldenrod	#af8700	rgb(175,135,0)	hsl(6,100%,34%)
            137	LightSalmon3	#af875f	rgb(175,135,95)	hsl(30,33%,52%)
            138	RosyBrown	#af8787	rgb(175,135,135)	hsl(0,20%,60%)
            139	Grey63	#af87af	rgb(175,135,175)	hsl(300,20%,60%)
            140	MediumPurple2	#af87d7	rgb(175,135,215)	hsl(270,50%,68%)
            141	MediumPurple1	#af87ff	rgb(175,135,255)	hsl(260,100%,76%)
            142	Gold3	#afaf00	rgb(175,175,0)	hsl(60,100%,34%)
            143	DarkKhaki	#afaf5f	rgb(175,175,95)	hsl(60,33%,52%)
            144	NavajoWhite3	#afaf87	rgb(175,175,135)	hsl(60,20%,60%)
            145	Grey69	#afafaf	rgb(175,175,175)	hsl(0,0%,68%)
            146	LightSteelBlue3	#afafd7	rgb(175,175,215)	hsl(240,33%,76%)
            147	LightSteelBlue	#afafff	rgb(175,175,255)	hsl(240,100%,84%)
            148	Yellow3	#afd700	rgb(175,215,0)	hsl(1,100%,42%)
            149	DarkOliveGreen3	#afd75f	rgb(175,215,95)	hsl(80,60%,60%)
            150	DarkSeaGreen3	#afd787	rgb(175,215,135)	hsl(90,50%,68%)
            151	DarkSeaGreen2	#afd7af	rgb(175,215,175)	hsl(120,33%,76%)
            152	LightCyan3	#afd7d7	rgb(175,215,215)	hsl(180,33%,76%)
            153	LightSkyBlue1	#afd7ff	rgb(175,215,255)	hsl(210,100%,84%)
            154	GreenYellow	#afff00	rgb(175,255,0)	hsl(8,100%,50%)
            155	DarkOliveGreen2	#afff5f	rgb(175,255,95)	hsl(90,100%,68%)
            156	PaleGreen1	#afff87	rgb(175,255,135)	hsl(100,100%,76%)
            157	DarkSeaGreen2	#afffaf	rgb(175,255,175)	hsl(120,100%,84%)
            158	DarkSeaGreen1	#afffd7	rgb(175,255,215)	hsl(150,100%,84%)
            159	PaleTurquoise1	#afffff	rgb(175,255,255)	hsl(180,100%,84%)
            160	Red3	#d70000	rgb(215,0,0)	hsl(0,100%,42%)
            161	DeepPink3	#d7005f	rgb(215,0,95)	hsl(33,100%,42%)
            162	DeepPink3	#d70087	rgb(215,0,135)	hsl(22,100%,42%)
            163	Magenta3	#d700af	rgb(215,0,175)	hsl(11,100%,42%)
            164	Magenta3	#d700d7	rgb(215,0,215)	hsl(300,100%,42%)
            165	Magenta2	#d700ff	rgb(215,0,255)	hsl(90,100%,50%)
            166	DarkOrange3	#d75f00	rgb(215,95,0)	hsl(6,100%,42%)
            167	IndianRed	#d75f5f	rgb(215,95,95)	hsl(0,60%,60%)
            168	HotPink3	#d75f87	rgb(215,95,135)	hsl(340,60%,60%)
            169	HotPink2	#d75faf	rgb(215,95,175)	hsl(320,60%,60%)
            170	Orchid	#d75fd7	rgb(215,95,215)	hsl(300,60%,60%)
            171	MediumOrchid1	#d75fff	rgb(215,95,255)	hsl(285,100%,68%)
            172	Orange3	#d78700	rgb(215,135,0)	hsl(7,100%,42%)
            173	LightSalmon3	#d7875f	rgb(215,135,95)	hsl(20,60%,60%)
            174	LightPink3	#d78787	rgb(215,135,135)	hsl(0,50%,68%)
            175	Pink3	#d787af	rgb(215,135,175)	hsl(330,50%,68%)
            176	Plum3	#d787d7	rgb(215,135,215)	hsl(300,50%,68%)
            177	Violet	#d787ff	rgb(215,135,255)	hsl(280,100%,76%)
            178	Gold3	#d7af00	rgb(215,175,0)	hsl(8,100%,42%)
            179	LightGoldenrod3	#d7af5f	rgb(215,175,95)	hsl(40,60%,60%)
            180	Tan	#d7af87	rgb(215,175,135)	hsl(30,50%,68%)
            181	MistyRose3	#d7afaf	rgb(215,175,175)	hsl(0,33%,76%)
            182	Thistle3	#d7afd7	rgb(215,175,215)	hsl(300,33%,76%)
            183	Plum2	#d7afff	rgb(215,175,255)	hsl(270,100%,84%)
            184	Yellow3	#d7d700	rgb(215,215,0)	hsl(60,100%,42%)
            185	Khaki3	#d7d75f	rgb(215,215,95)	hsl(60,60%,60%)
            186	LightGoldenrod2	#d7d787	rgb(215,215,135)	hsl(60,50%,68%)
            187	LightYellow3	#d7d7af	rgb(215,215,175)	hsl(60,33%,76%)
            188	Grey84	#d7d7d7	rgb(215,215,215)	hsl(0,0%,84%)
            189	LightSteelBlue1	#d7d7ff	rgb(215,215,255)	hsl(240,100%,92%)
            190	Yellow2	#d7ff00	rgb(215,255,0)	hsl(9,100%,50%)
            191	DarkOliveGreen1	#d7ff5f	rgb(215,255,95)	hsl(75,100%,68%)
            192	DarkOliveGreen1	#d7ff87	rgb(215,255,135)	hsl(80,100%,76%)
            193	DarkSeaGreen1	#d7ffaf	rgb(215,255,175)	hsl(90,100%,84%)
            194	Honeydew2	#d7ffd7	rgb(215,255,215)	hsl(120,100%,92%)
            195	LightCyan1	#d7ffff	rgb(215,255,255)	hsl(180,100%,92%)
            196	Red1	#ff0000	rgb(255,0,0)	hsl(0,100%,50%)
            197	DeepPink2	#ff005f	rgb(255,0,95)	hsl(37,100%,50%)
            198	DeepPink1	#ff0087	rgb(255,0,135)	hsl(28,100%,50%)
            199	DeepPink1	#ff00af	rgb(255,0,175)	hsl(18,100%,50%)
            200	Magenta2	#ff00d7	rgb(255,0,215)	hsl(09,100%,50%)
            201	Magenta1	#ff00ff	rgb(255,0,255)	hsl(300,100%,50%)
            202	OrangeRed1	#ff5f00	rgb(255,95,0)	hsl(2,100%,50%)
            203	IndianRed1	#ff5f5f	rgb(255,95,95)	hsl(0,100%,68%)
            204	IndianRed1	#ff5f87	rgb(255,95,135)	hsl(345,100%,68%)
            205	HotPink	#ff5faf	rgb(255,95,175)	hsl(330,100%,68%)
            206	HotPink	#ff5fd7	rgb(255,95,215)	hsl(315,100%,68%)
            207	MediumOrchid1	#ff5fff	rgb(255,95,255)	hsl(300,100%,68%)
            208	DarkOrange	#ff8700	rgb(255,135,0)	hsl(1,100%,50%)
            209	Salmon1	#ff875f	rgb(255,135,95)	hsl(15,100%,68%)
            210	LightCoral	#ff8787	rgb(255,135,135)	hsl(0,100%,76%)
            211	PaleVioletRed1	#ff87af	rgb(255,135,175)	hsl(340,100%,76%)
            212	Orchid2	#ff87d7	rgb(255,135,215)	hsl(320,100%,76%)
            213	Orchid1	#ff87ff	rgb(255,135,255)	hsl(300,100%,76%)
            214	Orange1	#ffaf00	rgb(255,175,0)	hsl(1,100%,50%)
            215	SandyBrown	#ffaf5f	rgb(255,175,95)	hsl(30,100%,68%)
            216	LightSalmon1	#ffaf87	rgb(255,175,135)	hsl(20,100%,76%)
            217	LightPink1	#ffafaf	rgb(255,175,175)	hsl(0,100%,84%)
            218	Pink1	#ffafd7	rgb(255,175,215)	hsl(330,100%,84%)
            219	Plum1	#ffafff	rgb(255,175,255)	hsl(300,100%,84%)
            220	Gold1	#ffd700	rgb(255,215,0)	hsl(0,100%,50%)
            221	LightGoldenrod2	#ffd75f	rgb(255,215,95)	hsl(45,100%,68%)
            222	LightGoldenrod2	#ffd787	rgb(255,215,135)	hsl(40,100%,76%)
            223	NavajoWhite1	#ffd7af	rgb(255,215,175)	hsl(30,100%,84%)
            224	MistyRose1	#ffd7d7	rgb(255,215,215)	hsl(0,100%,92%)
            225	Thistle1	#ffd7ff	rgb(255,215,255)	hsl(300,100%,92%)
            226	Yellow1	#ffff00	rgb(255,255,0)	hsl(60,100%,50%)
            227	LightGoldenrod1	#ffff5f	rgb(255,255,95)	hsl(60,100%,68%)
            228	Khaki1	#ffff87	rgb(255,255,135)	hsl(60,100%,76%)
            229	Wheat1	#ffffaf	rgb(255,255,175)	hsl(60,100%,84%)
            230	Cornsilk1	#ffffd7	rgb(255,255,215)	hsl(60,100%,92%)
            231	Grey100	#ffffff	rgb(255,255,255)	hsl(0,0%,100%)
            232	Grey3	#080808	rgb(8,8,8)	hsl(0,0%,3%)
            233	Grey7	#121212	rgb(18,18,18)	hsl(0,0%,7%)
            234	Grey11	#1c1c1c	rgb(28,28,28)	hsl(0,0%,10%)
            235	Grey15	#262626	rgb(38,38,38)	hsl(0,0%,14%)
            236	Grey19	#303030	rgb(48,48,48)	hsl(0,0%,18%)
            237	Grey23	#3a3a3a	rgb(58,58,58)	hsl(0,0%,22%)
            238	Grey27	#444444	rgb(68,68,68)	hsl(0,0%,26%)
            239	Grey30	#4e4e4e	rgb(78,78,78)	hsl(0,0%,30%)
            240	Grey35	#585858	rgb(88,88,88)	hsl(0,0%,34%)
            241	Grey39	#626262	rgb(98,98,98)	hsl(0,0%,37%)
            242	Grey42	#6c6c6c	rgb(108,108,108)	hsl(0,0%,40%)
            243	Grey46	#767676	rgb(118,118,118)	hsl(0,0%,46%)
            244	Grey50	#808080	rgb(128,128,128)	hsl(0,0%,50%)
            245	Grey54	#8a8a8a	rgb(138,138,138)	hsl(0,0%,54%)
            246	Grey58	#949494	rgb(148,148,148)	hsl(0,0%,58%)
            247	Grey62	#9e9e9e	rgb(158,158,158)	hsl(0,0%,61%)
            248	Grey66	#a8a8a8	rgb(168,168,168)	hsl(0,0%,65%)
            249	Grey70	#b2b2b2	rgb(178,178,178)	hsl(0,0%,69%)
            250	Grey74	#bcbcbc	rgb(188,188,188)	hsl(0,0%,73%)
            251	Grey78	#c6c6c6	rgb(198,198,198)	hsl(0,0%,77%)
            252	Grey82	#d0d0d0	rgb(208,208,208)	hsl(0,0%,81%)
            253	Grey85	#dadada	rgb(218,218,218)	hsl(0,0%,85%)
            254	Grey89	#e4e4e4	rgb(228,228,228)	hsl(0,0%,89%)
            255	Grey93	#eeeeee	rgb(238,238,238)	hsl(0,0%,93%)
        '''[1:-1]
        out = []
        for i, line in enumerate(data.split("\n")):
            line = line.strip()
            if not line:
                continue
            f = line.split("\t")
            if len(f) != 5 and not i:
                continue    # Ignore the first line, as it has 6 fields
            assert len(f) == 5, f"[{i + 1}]:  {line!r} doesn't have 5 fields"
            num256 = int(f[0])
            rgb = f[3].replace("rgb", "")
            t.c = t(eval(f"Color{rgb}"))
            if 0:
                print(f"{num256}{t.c} {f[1]}")
            else:
                out.append(f"{t.c}{num256:3d}{t.n}")
        print("Table of 8-bit colors")
        width = int(os.environ["COLUMNS"]) - 1
        for i in Columnize(out, horiz=True, width=width):
            print(f"{' '*2}{i}")

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd]
          cmd
           s     Show short color names
           a     Attributes
          None   Convert color specifier on command line to various
                 representations in RGB, HSV, and HLS.  Argument can be
                 e.g. 'ornl', '128 64 32', '0x80 0o100 0b100000', '#804020',
                 '@0ebf80' '$0e5099' forms (',' and ';' removed).
           d     Demo
           t4    4 bit color table
           t8    8 bit color table
           t24   24 bit color table
        Options:
          -h      Print this help
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-t"] = False
        try:
            opts, args = getopt.getopt(sys.argv[1:], "ht", ["help", "test"])
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list(""):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o in ("-t", "--test"):
                exit(run(globals(), halt=True)[0])
        if not args:
            return ["s"]
        return args
    ###########################################################################
    # Do some tasks
    #   d       Show examples
    #   s       Show short names, attributes
    #   t       Show color table
    # Otherwise interpret the color string
    d = {}      # Options dictionary
    cmds = ParseCommandLine(d)


    first_char = cmds[0][0]
    if first_char == "d":
        Examples()
    elif first_char == "T":
        TestTrm()
        TestColor()
        print("Tests passed")
    elif first_char == "8":
        Print256Colors()
    elif first_char == "s":
        # Default for no arguments
        ShortNames()
        print()
        ShowAttributes()
        print("\nUse d for examples, t for color table, 8 for 8-bit color table;")
        print("otherwise interpret the color specifier")
    elif first_char == "t":
        ColorTable(int(cmds[0][1:]))
    else:
        for i in cmds:
            InterpretColorSpecifier(i)
