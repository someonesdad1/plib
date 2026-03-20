'''
Vision
    - One file for color stuff:  color.py (besides data/colornames.py)
    - Color
        - Constructor works flawlessly
        - Look at getting rid of cruft:  this is primarily a class to hold a color and
          allow conversion to other coordinates
    - Trm & ColorName are obsoleted
    - New Trm is a dict where .on and .always work correctly
        - No instance is created by default; the t instance has created a large
          number of circular reference problems
        - Should Trm be in this file or trm.py?
    - Move RegexpDecorate to dpstr.py
    - Move colorcoord.py stuff to this file and have thorough docs & selftests
'''
'''
---------------------------------------------------------------------------
Functions to convert between ANSI 8-bit color numbers and 24-bit RGB values:
    RGBtoANSI8bit(r, g, b)
    Translate8bit(n)
    
Classes to help with color use in terminals
    - class Color
        - Immutable class to store the three numbers used to define a color
    - class Trm
        - Outputs ANSI escape sequences to allow color use in a terminal
    - class ColorName
        - Maps string names to a Color object
        
    - Typical usage
    
        from color import Color, t
        print(f"{t('redl')}Error:  you need to fix this{t.n}")
        print(f"{t('lblu', 'wht'} This is blue text in a white background")
        
        # The default color names are based on the resistor color code names.  Prefix with 'l' for
        # the lighter colors, 'd' for darker, and 'b' for light pastel background colors.  Run the
        # color.py file as a script to see these color names and how they render on your screen.
        
        # The Trm instance t can be called with a foreground and background color (either a name or
        # Color instance) and an optional attribute (e.g., for italics).  The t.n value means to
        # return to the default color.  You can store escape sequences as attributes:
        
            t.err = t("redl")
            print(f"{t.err}Error:  you need to fix this{t.n}")
            
        # You can use t.out and t.print to avoid having to reset to the default color.  t.out is
        # the same as t.print but without the newline.
        
    - This file includes some deprecated functionality to support an older python module I used for
      a couple of decades.  Over time, I expect to remove the dependencies on this stuff and it
      will eventually be removed with no warning (i.e., don't use these older features).  To
      disable the legacy code support, define the 'klr' environment variable to be empty (evaluate
      False as a boolean).
      
    - class Color
        - This immutable class is used to store the three integers that define a color.  You can
          set the number of bits to use to store these integers using the class variable
          Color.bits_per_color, which defaults to 8.
        - The Color constructor has a number of ways to instantiate a color:
            - One argument
                - A short string name for a color (these are actually handled by the global
                  ColorNum instance CN).
                - Hex strings
                    - '@abcdef' means an HSV hex string
                    - '#abcdef' means an RGB hex string
                    - '$abcdef' means an HLS hex string
                - Another Color instance:  a copy is made
                - A decimal number on [0, 1] defining a gray with white being 1.
            - Three arguments
                - Color(1, 2, 3)
                - Color(0.1, 0.2, 0.3)
                - Can use boolean keywords "hsv" or "hls" to not use the default rgb space.
        - Helpful functionality
            - Construct(x)
                - This class method returns a Color instance if the string argument x contains a
                  recognizable color initializer (hex string or 3-sequence of numbers).  If x was a
                  multiline string with one or more valid color initializers, a deque of (a, c)
                  objects is returned with a the line's string and c the Color instance.  This is
                  handy for e.g.  colorizing a set of lines in a file of color specifiers such as
                  an X11 rgb.txt file.
        - Distance between two colors
            - RGB, HSV, HLS known to be nonlinear with respect to perception
            - https://www.compuphase.com/cmetric.htm gives a practical formula he says is close to
              L*u*v* space with modified lightness curve (it's a weighted Euclidean distance in RGB
              space).   Let two colors be specified by (R1, G1, B1) and (R2, G2, B2) where each
              component is an int on [0, 255].  Then
                - r = (R1 + R2)/2
                - dX = X1 - X2
                - d**2 = (2 + r/256)*dR**2 + 4*dG**2 + (2 + (255 - r)/256)*dB**2
            - ColorDistance() is a simple Euclidean distance in RGB space using an integer square root.
            
    References
        - http://color.lukas-stratmann.com/  Nice web pages to help visualize a few color
          coordinate systems.
          
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Classes to help with color use in terminals oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2022 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ color oo>
        <oo test ∞ --test oo>
        <oo todo ∞ 
            
        oo>
    '''
    if 1:   # Standard imports
        import collections 
        import contextlib
        import colorsys
        import decimal
        import fractions
        import io 
        import math
        import os
        import pathlib 
        import pprint
        import re
        import string
        import sys
        import threading
    if 1:   # Custom imports
        import asciify
        import columnize
        import dpcolornames
        import dpmath
        import dpseq
        import dptypes
        import f
        import get
        import dputil
        import wrap
        if 0:
            # This doesn't import debug.py, which will have a circular import because
            # dpdb.py imports color.py.
            import debugg
            debugg.SetDebugger()
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    if 1:   # Symbols from imports
        Decimal = decimal.Decimal
        Fraction = fractions.Fraction
        StringIO = io.StringIO
        P = pathlib.Path
        Iterable = collections.abc.Iterable
        deque = collections.deque
        hexdigits = string.hexdigits
        #
        flt = f.flt
        Stack = dptypes.Stack
        pp = pprint.pprint
    if 1:   # Global variables
        g = dptypes.Constant()
        g.trm_new = 0
        __all__ = "Color RGBtoANSI8bit Translate8bit ColorDistance ToIntRGB".split()
class Color:
    '''Storage of the three numbers used to define a color.  
        
        Constructor forms are (note that the absolute values of the components are
        used):
    
        Color(inst)     Makes a copy of another Color instance
        Color(seq)
                        seq is a sequence of 3 numbers or strings
        Color(int)
            0-255       8-bit ANSI color number
            > 255       Light wavelength in nm (black if not on [380, 780])
        Color(float)
            0-1         Grayscale, 0 == black, 1 == white
            > 1         Light wavelength in nm (black if not on [380, 780])
        Color(str)
            "\x1b..."   ANSI escape sequence
            "#abcdef"   RGB hex form
            "$abcdef"   HLS hex form
            "@abcdef"   HSV hex form
            "x x x"     Three space-separated numbers
            "x,x,x"     Three comma-separated numbers
            name        Look up an existing color name (normalized)
        Color(int, int, int)
            Values must be on [0, 255] and are interpreted as 24-bit RGB unless the
            keywords hsv or hls are True.
        Color(float, float, float)
            A 3-vector normalized to be a unit vector, then converted to integers to
            call Color(int, int, int).
        
        Where a floating point type is used for a number, the number can also be a
        Decimal, Fraction, or mpmath.mpf type.
        
        Color names are normalized with Color.NormalizeColorName(), which returns
        snake-case lowercase ASCII letter names.  The allowed names used are in
        /plib/data/dpcolornames.py.
    '''
    bits_per_color = 8
    def __init__(self, *p, **kw):
        'Initialize the Color object'
        if 1:
            if 1:   # Check for proper keyword arguments
                allowed = set("bpc hsv hls".split())
                actual = set(kw.keys())
                if not (actual <= allowed):
                    bad = actual - allowed
                    s = ", ".join(bad)
                    msg = f"Bad keyword(s):  {s}"
                    raise ValueError(msg)
            if 1:   # Set attributes
                self._bpc = kw.get("bpc", Color.bits_per_color)
                self._rgb = None    # RGB integer components
                self._sort = "rgb"  # Sorting order (must be rgb, hsv, or hls)
            if 1:   # Process the arguments:  get (u, v, w), which covers all constructor use cases
                # If p is a single argument, v and w will be None.  Otherwise, we should
                # have the tuple (u, v, w) as the supplied arguments.
                try:
                    u = p[0]
                except Exception:
                    raise ValueError("color.Color() constructor needs at least one argument")
                try:
                    v, w = p[1], p[2]
                except Exception:
                    v, w = None, None
                if (v and u is None) or (v and u and len(p) > 3):
                    raise ValueError("color.Color() constructor needs either 1 or 3 arguments")
                # u could be a tuple or list of numbers
                if isinstance(u, (tuple, list)):
                    if len(u) != 3:
                        raise ValueError("color.Color() constructor must be sequence of 3 items")
                    u, v, w = u
        # Core constructor code
        if (u is not None) and (v is not None) and (w is not None):     # p is a sequence of 3 items
            # Possibilities ('hsv' and 'hls' keywords meaningful):
            #   1.  3 integers
            #   2.  3 floats
            r = (u, v, w)
            if all(isinstance(i, int) for i in r):  # Case 1:  3 integers
                rgb = tuple(abs(i) & self.n for i in r)
            else:  # Convert to floats
                try:
                    dec = tuple(abs(float(i)) for i in r)   # Case 2:  3 floats
                except Exception:
                    msg = f"'{r}' couldn't be converted to floats"
                    raise TypeError(msg)
                else:
                    if not all(0 <= i <= 1 for i in dec):
                        # Normalize to a unit 3-vector
                        magnitude = sum(i*i for i in dec)**(1/2)
                        dec = tuple(i/magnitude for i in dec)
                # Convert to 3-tuple of integers
                rgb = tuple(int(round(i*self.n, 1)) for i in dec)
            self._rgb = rgb
            # Handle 'hsv' and 'hls' keywords
            if kw.get("hsv", False):
                dec = colorsys.hsv_to_rgb(*self.drgb)
                self._rgb = tuple(int(round(i*self.n)) for i in dec)
            elif kw.get("hls", False):
                dec = colorsys.hls_to_rgb(*self.drgb)
                self._rgb = tuple(int(round(i*self.n)) for i in dec)
        elif (u is not None) and (v is None) and (w is None):           # p is one object
            # Possibilities:
            #   1.  Color instance
            #   2.  int
            #   3.  float
            #   4.  object --> int
            #   5.  object --> float
            #   6.  str
            #       ANSI escape sequence
            #       Hex string for color
            #           '#123456', '$123456', '@123456'
            #       Color name
            #           'red'
            #       3-tuple of integers
            #           '12 34 56' or '12,34,56' or '12;34;56'
            #       3-tuple of floats
            #           '1.2 3.4 5.6' or '1.2,3.4,5.6' or '1.2;3.4;5.6'
            #       int
            #           '12'
            #       float
            #           '1.2'
            if isinstance(u, Color):    # Case 1
                self._bpc = u._bpc
                self._rgb = u._rgb
                self._sort = u._sort
            elif isinstance(u, int):    # Case 2
                u = abs(u)
                if 0 <= u <= 255:   # 8-bit ANSI color
                    c = Translate8bit(u)
                else:               # Wavelength of light in nm
                    c = Color.wl2rgb(u, bpc=self._bpc)
                self._rgb = c.irgb
            elif (isinstance(u, (float, Decimal, Fraction))
                    or (have_mpmath and isinstance(u, mpmath.mpf))
            ):  # Case 3
                u = abs(u)
                if 0 <= u <= 1:
                    # Interpret as a gray
                    self._rgb = tuple(int(round(float(i)*self.n, 1)) for i in (u, u, u))
                else:
                    # Interpret as a light wavelength in nm
                    c = Color.wl2rgb(u, bpc=self._bpc)
                    self._rgb = c.irgb
            elif isinstance(u, str):    # Case 6
                u = u.strip()
                if not u:
                    raise ValueError("Argument can't be only whitespace")
                if u[0] == "\x1b":
                    self._rgb = self.escape(u)
                else:
                    try:
                        self._rgb = self.string(u)      # Hex string or color name
                    except ValueError:
                        # Only other choice is it's a string that can be interpreted as
                        # an integer or float or three integers or floats
                        e = ValueError(f"{u!r} can't be interpreted as a Color initializer")
                        if " " in u or "," in u or ";" in u:
                            a = u.replace(",", " ").replace(";", " ")
                            try:
                                seq = [dpmath.Int(i) for i in a.split()]    # 3-tuple of int
                                self._rgb = Color(*seq).irgb
                            except Exception:
                                try:
                                    seq = [float(i) for i in a.split()]     # 3-tuple of float
                                    self._rgb = Color(*seq).irgb
                                except Exception:
                                    raise e
                        else:
                            try:
                                v = dpmath.Int(u)               # Case 4
                                self._rgb = Color(v).irgb
                            except Exception:
                                try:
                                    v = float(u)                # Case 5
                                    self._rgb = Color(v).irgb
                                except Exception:
                                    raise e
            else:
                s = f"{u!r} Bug in color.Color():  unhandled case"
                raise Exception(s)
        else:
            from pdb import set_trace as yy; yy() 
            raise Exception("Bug in color.Color():  should be impossible to reach this point")
        self._check()
    def _check(self):
        'Check invariants'
        assert isinstance(self._bpc, int) and self._bpc > 0
        assert len(self._rgb) == 3
        assert (0 <= i < self.N and isinstance(i, int) for i in self._rgb)
        assert self._sort in ("rgb", "hsv", "hls")
    def string(self, X):
        'Return 3-tuple int rgb value from a string'
        assert isinstance(X, str)
        if not X:
            raise ValueError("Can't initialize with an empty string")
        x, N = X.lower(), self.N - 1
        first_char, s = x[0], x[1:]
        if first_char in "@#$":
            # It must be a hex string form.  '@' means HSV,
            # '#' means RGB, '$' means HLS.
            n, rem = divmod(len(s), 6)
            if not s or rem:
                raise ValueError("Hex string length must be a multiple of 6 characters")
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
            # It names a color
            msg = f"{x!r} isn't recognized as a color name"
            if 0:   # Old method
                try:
                    rgb = CN[x].irgb
                except Exception:
                    raise ValueError(msg)
            else:
                name = Color.NormalizeColorName(x)
                if name in dpcolornames.colornames:
                    # This gets the color with the lowest number key, as this is the
                    # order I want things searched for (most colors will be in 0 or
                    # 1, my color names; 2 is the X11 names, and the remaining ones
                    # are various name sets downloaded from the web).
                    found = sorted(dpcolornames.colornames[name], key=lambda x: x.key)[0]
                    # found is a ColorName instance, a namedtuple
                    c = Color(found.hex)   # .hex attribute is a hex string 
                    rgb = c.irgb
                else:
                    raise ValueError(msg)
        assert all(0 <= i <= N and isinstance(i, int) for i in rgb)
        return rgb
    def escape(self, X):
        '''Return 3-tuple int rgb value from an ANSI escape code.
        
        To be technically correct, this should handle double escape codes like 
        '\x1b[38:5:⟨n⟩m\x1b[48:5:⟨n⟩m', which specifies both a foreground and
        background color.   However, for the first implementation, I'm going to
        keep it simple, as the only "user" is the new Trm object and the vast
        majority of the time it will be single escape sequences.
        
        Examples of typical values for X:
            \x1b[38;5;⟨n⟩m  8-bit foreground color n
            \x1b[48;5;⟨n⟩m  8-bit background color n
            \x1b[38;2;⟨r⟩;⟨g⟩;⟨b⟩m 24-bit foreground color
            \x1b[48;2;⟨r⟩;⟨g⟩;⟨b⟩m 24-bit background color
        '''
        assert X and isinstance(X, str) and X[0] == "\x1b"
        n = X.count("\x1b")
        if not n:
            raise ValueError("X = {X!r} doesn't have an escape character")
        elif n != 1:
            raise ValueError("Only one escape character allowed in string")
        x = X.replace("\x1b[", "")
        f = x.split(";")
        if len(f) == 3:
            assert f[0] in "38 48".split()
            assert f[1] == "5"
            n = int(f[2].replace("m", ""))
            return Translate8bit(n)
        elif len(f) == 5:
            assert f[0] in "38 48".split()
            assert f[1] == "2"
            r, g = [int(i) for i in (f[2], f[3])]
            b = int(f[4].replace("m", ""))
            return (r, g, b)
        else:
            raise ValueError(f"{X!r} is an unrecognized escape code")
    def __str__(self):
        u = "⁰¹²³⁴⁵⁶⁷⁸⁹"
        b = "".join(u[int(i)] for i in str(self._bpc))
        n, w = self._rgb, len(str(self.n))
        return f"C{b}({n[0]:{w}d}, {n[1]:{w}d}, {n[2]:{w}d})"
    def __repr__(self):
        n, w = self._rgb, len(str(self.n))
        return f"Color({n[0]:{w}d}, {n[1]:{w}d}, {n[2]:{w}d}, bpc={self._bpc})"
    def _str(self, dec=True):
        "Return string representations"
        name, n = type(self).__name__, self.digits()
        if dec:
            r, g, b = self.rgb
            return f"{name}({r:{2 + n}.{n}f}, {g:{2 + n}.{n}f}, {b:{2 + n}.{n}f})"
        else:
            s = self.fmt_int(*self._rgb)
            return f"{name}({s})"
    def __eq__(self, other):
        "Two instances are equal if their RGB components are equal"
        # This embraces a subtle but crucial point in defining the
        # fractions used for comparisons (the Fraction objects are used in
        # the change_bpc method):  the denominator is 2**self._bpc.
        # This lets color integers be "downshifted" (scaled) to lower bits
        # per color values and compare equally to higher bpc colors.
        bpc = min(self.bpc, other.bpc)
        me, you = self.irgb, other.irgb
        if bpc != self.bpc:
            me = self.change_bpc(bpc).irgb
        if bpc != other.bpc:
            you = other.change_bpc(bpc).irgb
        return me == you
    def __lt__(self, other):
        "Compare self and other for e.g. sorting"
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
        if not isinstance(bpc, int) and bpc < 1:
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
            "Round and limit x to [0, self.n]"
            y = int(round(x, 1))
            return min(self.n, max(0, y))
        allowed = "rgbhsvHLS"
        if set:
            if not isinstance(p, int):
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
            h, l, s = self.ihls     # noqa
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
        if not isinstance(bpc, int) or bpc < 1:
            raise TypeError("bpc must be an integer")
        if bpc < 1:
            raise ValueError("bpc must be > 0")
        N = 2**bpc - 1  # Integers for new color are on [0, N]
        newrgb = tuple(int(round(i*N, 1)) for i in self.rgb)
        return Color(*newrgb)
    def interpolate(self, other, t, space="rgb"):
        '''Interpolate between two colors:  self and other.  t is a parameter on
        [0, 1].  If t is 0, you'll get back self and if t is 1, you'll get back
        other.  If t is intermediate, you'll get a color "between" the two.  space
        can be "rgb", "hsv", or "hls" and picks the coordinates used to interpolate.
        '''
        '''
        The algorithm is linear interpolation in 2D Cartesian coordinates (x, y) for
        each color component.  Let the starting point be P = (x0, y0) and the ending
        point be Q = (x1, y1).  Further, let x0 = 0 and x1 = 1.
        
        The slope of the line connecting P and Q is
            m = (y1 - y0)/(x1 - x0) = y1 - y0
        
        Given the parameter t on [0, 1], the interpolated value along the line
        between P and Q is R = (t, y0 + m*t).  For t = 0, you get R == P and for
        t = 1 you get R == Q.
        '''
        if not isinstance(other, Color):
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
        m = [j - i for i, j in zip(P, Q)]  # 3-vector of slopes
        R = [i + slope*t for i, slope in zip(P, m)]
        # Convert the coordinates of R back to rgb space
        if space == "hsv":
            R = colorsys.hsv_to_rgb(*R)
        elif space == "hls":
            R = colorsys.hls_to_rgb(*R)
        rgb = self.dec_to_int(R)
        return Color(*rgb, bpc=me.bpc)
    if 1:  # Utility
        def fmt_int(self, a, b, c):
            '''Format with uniform spacing for integers.  Example: self.fmt_int(1,
            23, 214) will return '  1,  23, 21'.  This is handy for making lists of
            color numbers because the spacing makes them easier to read in a text
            file.
            '''
            if not all(isinstance(i, int) for i in (a, b, c)):
                raise TypeError("Arguments must be integers")
            w = len(str(self.N))
            return f"{a:{w}d}, {b:{w}d}, {c:{w}d}"
        def dec_to_int(self, three_tuple):
            'Return int value of decimal values in 3-tuple of floats'
            assert all(isinstance(i, float) for i in three_tuple)
            return tuple(int(round(i*self.n, 1)) for i in three_tuple)
        def int_to_dec(self, three_tuple):
            'Return float value of 3-tuple of integers'
            assert all(isinstance(i, int) for i in three_tuple)
            return tuple(i/(self.N - 1) for i in three_tuple)
        def digits(self):
            '''Return number of digits for to use for decimal rounding, typically
            for printing to the screen.  Choose enough digits to hold all the color
            values.
            '''
            # self.N + 1 is the number of distinct color components.
            n = math.ceil(math.log10(self.N + 1))
            return max(1, n)
    if 1:  # Settable properties
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
    if 1:  # Read-only properties
        @property
        def N(self):    # 2**bits_per_color
            'Number of colors we represent == 2**bits_per_color'
            return 2**self._bpc
        @property       # 2**bits_per_color - 1
        def n(self):
            'self.N - 1'
            return self.N - 1
        @property       # Bits per color
        def bpc(self):
            'Bits per color'
            return self._bpc
        @property
        def hex_bytes_per_color(self):  # How many bytes needed to express a color in hex
            'How many bytes needed to express a color in hex'
            return math.ceil(self._bpc/8) + 1
        #
        @property
        def irgb(self):     # 3-tuple of integers on [0, 2**self.N - 1]
            'Get rgb as a 3-tuple of integers on [0, 2**self.N - 1]'
            return self._rgb
        @property
        def drgb(self):     # 3-tuple of floats on [0, 1]
            'Get rgb as a 3-tuple of floats on [0, 1]'
            return tuple(i/(self.N - 1) for i in self._rgb)
        @property
        def xrgb(self):     # #000000
            'Get rgb as a hex string of the form #000000'
            return "#" + Color.int_to_hex(self._rgb)
        #
        @property
        def ihsv(self):     # hsv as a 3-tuple of integers on [0, 2**self.N - 1]
            'Get hsv as a 3-tuple of integers on [0, 2**self.N - 1]'
            dec = colorsys.rgb_to_hsv(*self.drgb)
            hsv = tuple(int(round(i*(self.N - 1), 1)) for i in dec)
            return hsv
        @property
        def dhsv(self):     # hsv as a 3-tuple of floats on [0, 1]
            'Get hsv as a 3-tuple of floats on [0, 1]'
            return colorsys.rgb_to_hsv(*self.drgb)
        @property
        def xhsv(self):     # @ffffff
            "Get hsv as a hex string of the form @000000"
            return "@" + Color.int_to_hex(self.ihsv)
        #
        @property
        def ihls(self):     # hls as a 3-tuple of integers on [0, 2**self.N - 1]
            'Get hls as a 3-tuple of integers on [0, 2**self.N - 1]'
            dec = self.drgb
            hlsdec = colorsys.rgb_to_hls(*dec)
            hls = tuple(int(round(i*(self.N - 1), 1)) for i in hlsdec)
            return hls
        @property
        def dhls(self):     # hls as a 3-tuple of floats on [0, 1]
            'Get hls as a 3-tuple of floats on [0, 1]'
            return colorsys.rgb_to_hls(*self.drgb)
        @property
        def xhls(self):     # $ffffff
            'Get hls as a hex string of the form $000000'
            return "$" + Color.int_to_hex(self.ihls)
    if 1:  # Class methods
        @classmethod
        def dist(cls, c1, c2, space="rgb", taxicab=False):
            '''Calculate a distance between two color instances.  They are both
            converted into Color objects with the same bpc and the Euclidean
            distance between the components is calculated.  The number returned is a
            float on [0, 1].
            
            Euclidean distances in these color spaces are known to be nonlinear with
            respect to human perception, but they are easy to calculate.
            
            space can be "rgb", "hsv", or "hls".
            
            If taxicab is True, then use the "taxicab" distance, which is how you'd
            e.g. calculate a walking distance in a city where you can only walk on
            the sidewalks (i.e., it's the sum of the absolute value of the
            coordinates' differences).
            
            Example:  The Euclidean distance between (Color(0, 0, 0) and Color(a, a,
            a) where a = 2**bpc - 1 will be sqrt(3).  Thus, the Euclidean distance
            is divided by sqrt(3) to get a float on [0, 1].  For taxicab distance,
            the distance is normalized to [0, 1] by dividing by 3.
            '''
            if not isinstance(c1, Color) or not isinstance(c2, Color):
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
                return d/3 ** (1/2)
        @classmethod
        def downshift(cls, c1, c2):
            "Return two Color instances with the same bpc (bits per color)"
            if not isinstance(c1, Color) or not isinstance(c2, Color):
                raise TypeError("c1 and c2 need to be Color instances")
            bpc = min(c1.bpc, c2.bpc)
            return (c1.change_bpc(bpc), c2.change_bpc(bpc))
        @classmethod
        def int_to_hex(cls, threetuple, bytes_per_color=1):
            "Convert 3-tuple of integers to hex string"
            e = TypeError(f"'{threetuple}' argument must be a 3-sequence of  integers")
            if not all(isinstance(i, int) for i in threetuple) or len(threetuple) != 3:
                raise e
            w = 2*bytes_per_color
            x = [f"{i:0{w}x}" for i in threetuple]
            ml = max(len(i) for i in x)
            if ml % 2:
                ml += 1
            for i, value in enumerate(x):
                while len(value) < ml:
                    value = "0" + value
                x[i] = value
            t = "".join(x)
            assert (len(t) % 6) == 0
            return t
        @classmethod
        def hex_to_int(cls, s):
            '''s must be a multiple of six hex digits; return a tuple of the
            three integers it represents.
            '''
            if not isinstance(s, str):
                raise TypeError(f"'{s}' argument must be a string")
            div, rem = divmod(len(s), 6)
            if rem:
                raise ValueError("Length of s must be a multiple of six")
            if not div:
                raise ValueError("Must have at least 6 hex characters")
            hd = set(hexdigits)
            if not all(i in hd for i in s):
                raise ValueError(f"String '{s}' contains non-hex characters")
            n = 2*div  # Number of hex digits per color
            rgb = (
                s[0*div:0*div + n],
                s[2*div:2*div + n],
                s[4*div:4*div + n],
            )
            try:
                rgb = tuple(int(i, 16) for i in rgb)
            except Exception:
                raise ValueError(f"'{s}' is not a valid hex string")
            return rgb
        @classmethod
        def round(cls, value, digits):
            "Round value to number of digits (value can be float or sequence)"
            n = digits
            if not isinstance(value, str) and isinstance(value, Iterable):
                return tuple(round(float(i), n) for i in value)
            else:
                if not isinstance(value, float):
                    raise TypeError("value must be a float or numerical sequence")
                return round(value, n)
        @classmethod
        def Dot(cls, a, b):
            "Dot product of two sequences"
            assert len(a) == len(b)
            return sum(i*j for i, j in zip(a, b))
        @classmethod
        def XYZ_to_sRGB(cls, XYZ):
            '''CIE XYZ to sRGB (XYZ is a 3-sequence of positive numbers)
            sRGB will be 3-sequence of floats on [0, 1]
            https://en.wikipedia.org/wiki/SRGB#From_CIE_XYZ_to_sRGB
            '''
            if isinstance(XYZ, str) or len(XYZ) != 3:
                raise TypeError(f"'{XYZ}' must be a sequence of 3 numbers")
            if not all(i >= 0 for i in XYZ):
                raise TypeError(f"'{XYZ}' must be numbers >= 0")
            def GammaCompressed(x):
                return 12.92*x if x <= 0.0031308 else 1.055*x ** (1/2.4) - 0.055
            r1 = (+3.2406, -1.5372, -0.4986)
            r2 = (-0.9689, +1.8758, +0.0415)
            r3 = (+0.0557, -0.2040, +1.0570)
            rgb = Color.Dot(r1, XYZ), Color.Dot(r2, XYZ), Color.Dot(r3, XYZ)
            def clip(x):
                return min(1.0, max(x, 0.0))
            return tuple(clip(GammaCompressed(i)) for i in rgb)
        @classmethod
        def wl2rgb(cls, nm, sunlight=False, gamma=0.0, bpc=None):
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
            if not isinstance(nm, (int, float, flt, Decimal, Fraction)):
                if have_mpmath and not isinstance(nm, mpmath.mpf):
                    raise TypeError("nm must be an int or float")
            # Convert it to a float
            nm = float(nm)
            if bpc is None:
                bpc = Color.bits_per_color
            if not isinstance(bpc, int):
                raise TypeError("bpc must be an int")
            if not isinstance(gamma, (int, float, flt)):
                raise TypeError("gamma must be an int or float")
            if gamma < 0:
                raise ValueError("gamma must be >= 0")
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
                    # DP I made it '<= 700' so wavelength range is on [400, 700]
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
                # From D. Bruton's FORTRAN code (algorithm apparently due to Earl F.
                # Glynn).
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
                i, u, v = 1.0, 0.3, 0.7
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
            assert all([0 <= i <= 1 for i in rgb])
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
            if isinstance(seq, str) or not isinstance(seq, Iterable):
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
                else:  # Use the predicate
                    c = get(item)
                if not isinstance(c, Color):
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
        @classmethod
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
                "Return tuple of regexps to use to recognize color identifiers"
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
                "Turn a matched string into a Color instance"
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
        @classmethod
        def NormalizeColorName(cls, name):
            '''Return a normalized color name from the string name.
            Example:  "dark red", "Dark Red", "DarkRed", "Dark_red" as arguments will all
            return "dark_red".
            
            Algorithm:
                - Convert to ASCII-only form
                - " " inserted before each capital letter
                - " " substituted for each "_"
                - Split on whitespace
                - Convert each token to lowercase
                - Reassemble with "_"
            '''
            if not isinstance(name, str):
                raise TypeError("name must be a str instance")
            name = name.strip()
            if not name:
                raise ValueError("A name cannot be only whitespace or empty")
            # Make sure we have only printable ASCII characters
            name = asciify.Asciify(name)
            printable = set(string.printable)
            mychars = set(name)
            capitals = set(string.ascii_uppercase)
            if not (mychars <= printable):
                not_allowed = mychars - printable
                raise ValueError(f"{str(not_allowed)!r} are characters not allowed in names")
            # Process the characters
            new = []
            dq = collections.deque(name)
            while dq:
                char = dq.popleft()
                if char in capitals or char == "_":
                    new.append(" ")
                new.append(char)
            newstr = ''.join(new).replace("_", " ")
            new = '_'.join(i.lower() for i in newstr.split())
            return new
if 1:  # Translate between ANSI 8-bit and 24-bit colors
    def RGBtoANSI8bit(r, g, b):
        '''This function takes an RGB integer tuple and returns an integer on [0, 255]
        representing the closest ANSI 8-bit color.  This function is adapted from the
        file https://github.com/tmux/tmux/blob/master/colour.c.
        '''
        # Original tmux authors' copyright and license text:
        #
        #   Copyright (c) 2008 Nicholas Marriott <nicholas.marriott@gmail.com>
        #   Copyright (c) 2016 Avi Halachmi <avihpit@yahoo.com>.
        #
        #   Permission to use, copy, modify, and distribute this software for any purpose with or
        #   without fee is hereby granted, provided that the above copyright notice and this permission
        #   notice appear in all copies.
        #
        #   THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES WITH REGARD TO
        #   THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS. IN NO EVENT
        #   SHALL THE AUTHOR BE LIABLE FOR ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR
        #   ANY DAMAGES WHATSOEVER RESULTING FROM LOSS OF MIND, USE, DATA OR PROFITS, WHETHER IN AN
        #   ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF OR IN CONNECTION
        #   WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.
        def color_dist_sq(R, G, B, r, g, b):
            return (R - r)*(R - r) + (G - g)*(G - g) + (B - b)*(B - b)
        def color_to_6cube(v):
            assert isinstance(v, int)
            x = 0 if v < 48 else 1 if v < 114 else (v - 35) // 40
            assert 0 <= x < 256
            return x
        def ir(x):
            return int(round(x, 0))
        q2c = (0x00, 0x5F, 0x87, 0xAF, 0xD7, 0xFF)
        # Map RGB to 6x6x6 cube
        qr = color_to_6cube(r)
        qg = color_to_6cube(g)
        qb = color_to_6cube(b)
        cr = q2c[qr]
        cg = q2c[qg]
        cb = q2c[qb]
        # If we hit the color exactly, return early
        if cr == r and cg == g and cb == b:
            x = 16 + 36*qr + 6*qg + qb
            assert 0 <= x < 256
            return x
        # Work out the closest grey (average of RGB)
        grey_avg = ir((r + g + b)/3)
        grey_idx = 23 if grey_avg > 238 else (grey_avg - 3) // 10
        grey = 8 + 10*grey_idx
        # Is grey or 6x6x6 color
        d = color_dist_sq(cr, cg, cb, r, g, b)
        if color_dist_sq(grey, grey, grey, r, g, b) < d:
            idx = 232 + grey_idx
        else:
            idx = 16 + 36*qr + 6*qg + qb
        assert 0 <= idx < 256
        return idx
    def Translate8bit(n):
        '''Translate n, an 8-bit color number to a Color instance.  These should agree
        with common xterm values except that in 1 to 6 and 8 the 0x80 term was changed
        to 0x87 so that RGBtoANSI8bit() and Translate8bit() are inverses.
        
        Other lists:
            MIT license:
                https://github.com/sindresorhus/xterm-colors
            No license given:
                https://gist.github.com/2868981 
                Perl script that prints the xterm colors to the screen
                    http://web.archive.org/web/20130125000058/http://www.frexx.de/xterm-256-notes/
        
        I got these data from https://gist.github.com/jasonm23/2868981, downloaded 12
        Feb 2026 01:34:58 pm Thu.  In 2024 originally used the data from J. Jacek at
        https://www.ditig.com/publications/256-colors-cheat-sheet, but in Feb 2026 I
        changed my python modules to the MIT license, which is not compatible with the
        license (CC BY-NC-SA 4.0) that Jacek used, which is a copyleft license.  
        
        These data are used to translate an 8-bit number to an RGB color and this
        translation is taken from what's done with an ANSI Xterm.
        
        In the following table, I've made two substitutions so that RGBtoANSI8bit() and
        Translate8bit() are inverses:
                    Normal      Changed to
            YY      0xc0        0xbc
            ZZ      0x80        0x87
        These changes help the Test8bitConversions() test to pass.
         
        Note there is no standard to translate from an 8-bit color number to an RGB
        color.  The table in the section
        https://en.wikipedia.org/wiki/ANSI_escape_code#3-bit_and_4-bit shows the 
        different choices that have been made in various terminals.
        '''
        data = '''
            0 #000000
            1 #ZZ0000
            2 #00ZZ00
            3 #ZZZZ00
            4 #0000ZZ
            5 #ZZ00ZZ
            6 #00ZZZZ
            7 #YYYYYY
            8 #ZZZZZZ
            9 #ff0000
            10 #00ff00
            11 #ffff00
            12 #0000ff
            13 #ff00ff
            14 #00ffff
            15 #ffffff
            16 #000000
            17 #00005f
            18 #000087
            19 #0000af
            20 #0000d7
            21 #0000ff
            22 #005f00
            23 #005f5f
            24 #005f87
            25 #005faf
            26 #005fd7
            27 #005fff
            28 #008700
            29 #00875f
            30 #008787
            31 #0087af
            32 #0087d7
            33 #0087ff
            34 #00af00
            35 #00af5f
            36 #00af87
            37 #00afaf
            38 #00afd7
            39 #00afff
            40 #00d700
            41 #00d75f
            42 #00d787
            43 #00d7af
            44 #00d7d7
            45 #00d7ff
            46 #00ff00
            47 #00ff5f
            48 #00ff87
            49 #00ffaf
            50 #00ffd7
            51 #00ffff
            52 #5f0000
            53 #5f005f
            54 #5f0087
            55 #5f00af
            56 #5f00d7
            57 #5f00ff
            58 #5f5f00
            59 #5f5f5f
            60 #5f5f87
            61 #5f5faf
            62 #5f5fd7
            63 #5f5fff
            64 #5f8700
            65 #5f875f
            66 #5f8787
            67 #5f87af
            68 #5f87d7
            69 #5f87ff
            70 #5faf00
            71 #5faf5f
            72 #5faf87
            73 #5fafaf
            74 #5fafd7
            75 #5fafff
            76 #5fd700
            77 #5fd75f
            78 #5fd787
            79 #5fd7af
            80 #5fd7d7
            81 #5fd7ff
            82 #5fff00
            83 #5fff5f
            84 #5fff87
            85 #5fffaf
            86 #5fffd7
            87 #5fffff
            88 #870000
            89 #87005f
            90 #870087
            91 #8700af
            92 #8700d7
            93 #8700ff
            94 #875f00
            95 #875f5f
            96 #875f87
            97 #875faf
            98 #875fd7
            99 #875fff
            100 #878700
            101 #87875f
            102 #878787
            103 #8787af
            104 #8787d7
            105 #8787ff
            106 #87af00
            107 #87af5f
            108 #87af87
            109 #87afaf
            110 #87afd7
            111 #87afff
            112 #87d700
            113 #87d75f
            114 #87d787
            115 #87d7af
            116 #87d7d7
            117 #87d7ff
            118 #87ff00
            119 #87ff5f
            120 #87ff87
            121 #87ffaf
            122 #87ffd7
            123 #87ffff
            124 #af0000
            125 #af005f
            126 #af0087
            127 #af00af
            128 #af00d7
            129 #af00ff
            130 #af5f00
            131 #af5f5f
            132 #af5f87
            133 #af5faf
            134 #af5fd7
            135 #af5fff
            136 #af8700
            137 #af875f
            138 #af8787
            139 #af87af
            140 #af87d7
            141 #af87ff
            142 #afaf00
            143 #afaf5f
            144 #afaf87
            145 #afafaf
            146 #afafd7
            147 #afafff
            148 #afd700
            149 #afd75f
            150 #afd787
            151 #afd7af
            152 #afd7d7
            153 #afd7ff
            154 #afff00
            155 #afff5f
            156 #afff87
            157 #afffaf
            158 #afffd7
            159 #afffff
            160 #d70000
            161 #d7005f
            162 #d70087
            163 #d700af
            164 #d700d7
            165 #d700ff
            166 #d75f00
            167 #d75f5f
            168 #d75f87
            169 #d75faf
            170 #d75fd7
            171 #d75fff
            172 #d78700
            173 #d7875f
            174 #d78787
            175 #d787af
            176 #d787d7
            177 #d787ff
            178 #d7af00
            179 #d7af5f
            180 #d7af87
            181 #d7afaf
            182 #d7afd7
            183 #d7afff
            184 #d7d700
            185 #d7d75f
            186 #d7d787
            187 #d7d7af
            188 #d7d7d7
            189 #d7d7ff
            190 #d7ff00
            191 #d7ff5f
            192 #d7ff87
            193 #d7ffaf
            194 #d7ffd7
            195 #d7ffff
            196 #ff0000
            197 #ff005f
            198 #ff0087
            199 #ff00af
            200 #ff00d7
            201 #ff00ff
            202 #ff5f00
            203 #ff5f5f
            204 #ff5f87
            205 #ff5faf
            206 #ff5fd7
            207 #ff5fff
            208 #ff8700
            209 #ff875f
            210 #ff8787
            211 #ff87af
            212 #ff87d7
            213 #ff87ff
            214 #ffaf00
            215 #ffaf5f
            216 #ffaf87
            217 #ffafaf
            218 #ffafd7
            219 #ffafff
            220 #ffd700
            221 #ffd75f
            222 #ffd787
            223 #ffd7af
            224 #ffd7d7
            225 #ffd7ff
            226 #ffff00
            227 #ffff5f
            228 #ffff87
            229 #ffffaf
            230 #ffffd7
            231 #ffffff
            232 #080808
            233 #121212
            234 #1c1c1c
            235 #262626
            236 #303030
            237 #3a3a3a
            238 #444444
            239 #4e4e4e
            240 #585858
            241 #626262
            242 #6c6c6c
            243 #767676
            244 #808080
            245 #8a8a8a
            246 #949494
            247 #9e9e9e
            248 #a8a8a8
            249 #b2b2b2
            250 #bcbcbc
            251 #c6c6c6
            252 #d0d0d0
            253 #dadada
            254 #e4e4e4
            255 #eeeeee
        '''.strip()
        if 1:   # Perform the substitution
            data = data.replace("ZZ", "87").replace("YY", "bc").strip()
        if not hasattr(Translate8bit, "colormap"):
            # Convert the table into a dictionary that maps an integer from 0
            # to 255 to a Color instance; cache it in Translate8bit.colormap.
            di = {}
            for i, line in enumerate(data.split("\n")):
                line = line.strip()
                if not line or line.startswith("#"):
                    continue
                f = line.split()
                assert len(f) == 2, f"[{i + 1}]:  {line!r} doesn't have 2 fields"
                key, value = int(f[0]), f[1]
                value = Color(value)
                #print(f"{f[0]:3s} {f[1]}") # Uncomment to print
                di[key] = value
            Translate8bit.colormap = di
        return Translate8bit.colormap[n]
if 1:  # Utility functions
    def ColorDistance(rgb1, rgb2):
        '''Return an integer representing the Cartesian distance between two colors in RGB space.
        The arguments can be Color instances or 3-sequences of integers.  The returned value is an
        integer gotten with the math module's isqrt function.  The returned integer will
        be on [0, 441], as math.floor(math.sqrt(3*255²)) is 441.
        '''
        if isinstance(rgb1, Color):
            seq1 = rgb1.irgb
        else:
            assert isinstance(rgb1, (list, tuple)) and len(rgb1) == 3
            assert all(isinstance(i, int) for i in rgb1)
            seq1 = rgb1
        if isinstance(rgb2, Color):
            seq2 = rgb2.irgb
        else:
            assert isinstance(rgb2, (list, tuple)) and len(rgb2) == 3
            assert all(isinstance(i, int) for i in rgb2)
            seq2 = rgb2
        d = [(i - j)**2 for i, j in zip(seq1, seq2)]
        return math.isqrt(sum(d))
    def ToIntRGB(rgb):
        'Convert 3-tuple of floats on [0, 1] to [0, 255]'
        return tuple(dpseq.Clamp((int(i*256) for i in rgb), low=0, high=255, typ=int))

if __name__ == "__main__":
    if 1:   # Standard imports
        import collections
        import getopt
        import io
    if 1:   # Custom imports
        import columnize
        import lwtest as lw
        import trm
        import wrap
        import termtables as tt
    if 1:   # Symbols from imports
        u = trm.Trm()
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (int(os.environ.get("LINES", "50")),
                int(os.environ.get("COLUMNS", "80")) - 1)
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=sys.stderr)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=sys.stderr)
    def GetShortNames(all=False):
        '''Return a tuple of the short names.  If all is True, then
        also append the letters d, l, and b to get all of the basic
        colors.
        '''
        if 0:   # This is for older short names
            R = '''blk brn red orn yel grn blu vio gry wht cyn mag
                    pnk lip lav lil pur roy den sky trq sea lwn olv'''.split()
            if all:
                others = []
                others.extend(i + "d" for i in R)
                others.extend(i + "l" for i in R)
                others.extend(i + "b" for i in R)
                R.extend(others)
            return tuple(R)
        else:
            # Get the short names from dpcolornames module's dictionary
            di = dpcolornames.colornames
            names = []
            for i in di:
                for j in di[i]:
                    if j.key == 0:
                        names.append(j.name)
            return tuple(names)
    def Reset():
        Color.bits_per_color = 8
    def Test_8bitConversions():
        for i in range(256):
            rgb1 = Translate8bit(i)
            n = RGBtoANSI8bit(*rgb1.irgb)
            rgb2 = Translate8bit(n)
            dist = ColorDistance(rgb1, rgb2)
            lw.Assert(not dist)
    def Test_Color_adjust():
        Reset()
        c = Color(0, 100, 0)
        # Adjust green up and down by 10%
        c1 = c.adjust(10, comp="g", set=False)
        lw.Assert(c1.irgb == (0, 110, 0))
        c1 = c.adjust(-10, comp="g", set=False)
        lw.Assert(c1.irgb == (0, 90, 0))
        # Set green to 0
        c1 = c.adjust(0, comp="g", set=True)
        lw.Assert(c1.irgb == (0, 0, 0))
    def Test_Color_short_color_names():
        # This just sees that the names are recognized.
        R = GetShortNames(all=True)
        for i in R:
            c = Color(i, bpc=8)
            c   # Quiet linter
            #c = Color(i, bpc=10)
    def Test_Color_change_bpc():
        Reset()
        a = (15, 3, 7)
        c = Color(*a, bpc=4)
        d = c.change_bpc(8)
        lw.Assert(d == Color(240, 48, 112, bpc=8))
        e = c.change_bpc(4)
        lw.Assert(e == c)
        f = c.change_bpc(34)
        lw.Assert(f == Color(16106127360, 3221225472, 7516192768, bpc=34))
        g = f.change_bpc(4)
        lw.Assert(g == c)
    def Test_ColorAttributes():
        Reset()
        a = (3, 34, 18)
        c = Color(*a)
        n = c.N - 1
        lw.Assert(c.irgb == c._rgb)
        dec = tuple(i/n for i in c._rgb)
        lw.Assert(c.drgb == dec)
        lw.Assert(c.xrgb == "#032212")
        #
        lw.Assert(c.ihsv == (105, 232, 34))
        e = Color(*c.ihsv, hsv=True)
        lw.Assert(e == c)  # Shows c.ihsv converts back to original color
        dec = (0.41397849462365593, 0.9117647058823529, 0.13333333333333333)
        lw.Assert(c.dhsv == dec)
        lw.Assert(c.xhsv == "@69e822")
        # Can add attributes (no __slots__)
        c.a = 4
        lw.Assert(c.a == 4)
    def Test_Color_downshift():
        n = 7
        c1 = Color(1, 2, 3, bpc=13)
        c2 = Color(88, 233, 73, bpc=n)
        n1, n2 = Color.downshift(c1, c2)
        lw.Assert(n1.bpc == n and n2.bpc == n)
    def Test_Color_dist():
        n = 8
        m = 2**n - 1
        c1 = Color(0, 0, 0, bpc=n)
        c2 = Color(m, m, m, bpc=n)
        #x = Color.dist(c1, c2)
        lw.Assert(Color.dist(c1, c2) == 1)
        lw.Assert(Color.dist(c1, c2, taxicab=True) == 1)
    def Test_ColorEquality():
        Reset()
        if 1:  # Integers in constructor
            a, b, c = (36, 40, 99)
            c1 = Color(a, b, c)
            e, f, g = c1.irgb
            c2 = Color(a, b, c)
            c3 = Color(a + 1, b, c)
            lw.Assert(c1 == c2)
            lw.Assert(hash(c1) == hash(c2))
            lw.Assert(c1 != c3)
            # Show equality only depends on the stored integers
            c3._rgb = (a, b, c)
            lw.Assert(c1 == c3)
            lw.Assert(hash(c1) == hash(c3))
        if 1:  # Floats in constructor
            c1 = Color(e, f, g)
            c2 = Color(e, f, g)
            lw.Assert(c1 == c2)
        if 1:
            # Colors with different bpcs can be equal
            c1 = Color(15, 0, 0, bpc=4)
            c2 = Color(255, 0, 0, bpc=8)
            lw.Assert(c1 == c2)
    def Test_ColorInterpolate():
        Reset()
        c1 = Color(210, 105, 30)  # chocolate
        c2 = Color(205, 41, 144)  # maroon3
        got = c1.interpolate(c2, 0.65)
        expected = Color(206, 63, 104)
        lw.Assert(got == expected)
    def Test_ColorConstruct():
        Reset()
        def f(x):
            return tuple(round(i, 3) for i in x)
        # No color specifier gets None
        s = "kldjfkdj"
        c = Color.Construct(s)
        lw.Assert(c is None)
        # Separated by commas or spaces
        expected = Color(25, 51, 76)
        for s in (".1, .2, .3", ".1 .2 .3"):
            c = Color.Construct(s)
            lw.Assert(c == expected)
        # Multiline
        t = "This is a line"
        s = f'''
            {t} (.1, .2, .3)
            {t} (.2, .4, .7)
        '''
        a = Color.Construct(s)
        lw.Assert(isinstance(a, collections.deque))
        name, c = a.popleft()
        lw.Assert(t in name)
        lw.Assert(c == expected)
        name, c = a.popleft()
        lw.Assert(t in name)
        lw.Assert(f(c.drgb) == (0.200, 0.400, 0.698))
    def Test_ColorDistance():
        Reset()
        a = 12, 6, 247
        b = 101, 171, 124
        c1 = Color(*a)
        c2 = Color(*b)
        def f(x, y):
            return (sum((i - j) ** 2 for i, j in zip(x, y))/3) ** (1/2)
        # rgb
        d1 = f(c1.drgb, c2.drgb)
        d2 = Color.dist(c1, c2, space="rgb")
        lw.Assert(d1 == d2)
        # hsv
        d1 = f(c1.dhsv, c2.dhsv)
        d2 = Color.dist(c1, c2, space="hsv")
        lw.Assert(d1 == d2)
        # hls
        d1 = f(c1.dhls, c2.dhls)
        d2 = Color.dist(c1, c2, space="hls")
        lw.Assert(d1 == d2)
        # Distance from self is always zero
        for i in "rgb hsv hls".split():
            lw.Assert(Color.dist(c1, c1, space=i) == 0)
            lw.Assert(Color.dist(c2, c2, space=i) == 0)
    def Test_ColorSort():
        Reset()
        if 1:  # Sorting
            a = Color(12, 6, 247)
            b = Color(168, 255, 4)
            c = Color(252, 252, 129)
            seq = (a, b, c)
            # Sort on r; sequence should be unchanged
            seq1 = Color.Sort(seq, keys="r")
            lw.Assert(seq == seq1)
            # Sort on g
            seq1 = Color.Sort(seq, keys="g")
            lw.Assert(seq1 == (a, c, b))
            # Sort on b
            seq1 = Color.Sort(seq, keys="b")
            lw.Assert(seq1 == (b, c, a))
            # Sort on L
            seq1 = Color.Sort(seq, keys="L")
            lw.Assert(seq == seq1)
            # Sort on h
            seq1 = Color.Sort(seq, keys="h")
            lw.Assert(seq1 == (c, b, a))
            # Sort on s
            seq1 = Color.Sort(seq, keys="s")
            lw.Assert(seq1 == (c, a, b))
            # Sort on S
            seq1 = Color.Sort(seq, keys="S")
            lw.Assert(seq1 == (a, c, b))
        if 1:  # Test with predicate
            a = Color(12, 6, 247)
            b = Color(168, 255, 4)
            seq = (
                ("bob", b),
                ("alice", a),
            )
            def f(x):
                return x[1]
            seq1 = Color.Sort(seq, keys="r", get=f)
            lw.Assert(seq1[0] == ("alice", a))
            lw.Assert(seq1[1] == ("bob", b))
        if 1:  # Test the < operator
            a = Color("#000000")
            b = Color("#010000")
            lw.Assert(a < b)
            lw.Assert(not (b < a))
            lw.Assert(not (a < a))
            lw.Assert(not (b < b))
    def Test_ColorClassMethods():
        if 1:  # convert_hex
            f = Color.hex_to_int
            g = Color.int_to_hex
            for arg, expected in (
                ("000000", (0, 0, 0)),
                ("010203", (1, 2, 3)),
                ("fefefe", (0xFE, 0xFE, 0xFE)),
                ("ffffff", (0xFF, 0xFF, 0xFF)),
                ("000000000000", (0, 0, 0)),
                ("000100020003", (1, 2, 3)),
                ("00ff00ff00ff", (0xFF, 0xFF, 0xFF)),
                ("ffffffffffff", (0xFFFF, 0xFFFF, 0xFFFF)),
            ):
                bytes_per_color = len(arg) // 6
                lw.Assert(f(arg) == expected)
                got = g(expected, bytes_per_color)
                lw.Assert(got == arg)
            lw.raises(TypeError, f, 0)
            lw.raises(ValueError, f, "12345")
            lw.raises(ValueError, f, "1234567890")
            lw.raises(ValueError, f, "00000g")
        if 1:  # round
            f = Color.round
            pi = math.pi
            for arg, digits, expected in (
                (pi, 1, round(pi, 1)),
                (pi, 2, round(pi, 2)),
                (pi, 3, round(pi, 3)),
                (pi, 4, round(pi, 4)),
                (pi, 5, round(pi, 5)),
            ):
                lw.Assert(f(pi, digits) == expected)
            # Test sequence
            seq = [pi, pi, pi]
            seq1 = f(seq, digits)
            a = round(pi, digits)
            lw.Assert(seq1 == (a, a, a))
        if 1:  # Dot
            f = Color.Dot
            a, b = (1, 2, 3), (3, 2, 1)
            lw.Assert(f(a, b) == 10)
        if 1:  # XYZ_to_sRGB
            def GammaCompressed(x):
                return (
                    12.92*x if x <= 0.0031308 else 1.055*x ** (1/2.4) - 0.055
                )
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
            lw.Assert(got == expected)
        if 1:  # wl2rgb
            f = Color.wl2rgb
            T, F = True, False
            lw.raises(TypeError, f, "a")
            lw.raises(TypeError, f, 1, gamma="")
            lw.raises(ValueError, f, 1, gamma=-1)
            # Using the spectrum of sunlight
            lw.Assert(f(1.1, sunlight=T) == Color(0, 0, 0))
            lw.Assert(f(399, sunlight=T) == Color(0, 0, 0))
            # About the sodium D line
            lw.Assert(f(589, sunlight=T) == Color(246, 195, 0, bpc=8))
            lw.Assert(f(701, sunlight=T) == Color(0, 0, 0))
            # Bruton's approximation
            low, high = 379, 781
            lw.Assert(f(1.1, sunlight=F) == Color(0, 0, 0))
            lw.Assert(f(low, sunlight=F) == Color(0, 0, 0))
            # About the sodium D line
            #x = f(589, sunlight=F)
            lw.Assert(f(589, sunlight=F) == Color(255, 219, 0, bpc=8))
            lw.Assert(f(high, sunlight=F) == Color(0, 0, 0))
    def Test_ColorProperties():
        # Integer conversions should remain exact.  Check by testing some
        # samples.
        Reset()
        for bpc in (8, 10):
            Color.bits_per_color = bpc
            n = 2**bpc - 1
            R = range(0, n, n // 10)
            for i in R:
                for j in R:
                    for k in R:
                        a = (i, j, k)
                        c = Color(*a)
                        lw.Assert(c.irgb == a)
        Reset()
        # Properties return 3-tuples
        c = Color(1, 2, 3)
        lw.Assert(isinstance(c.irgb, tuple) and len(c.irgb) == 3)
        lw.Assert(isinstance(c.drgb, tuple) and len(c.drgb) == 3)
        lw.Assert(isinstance(c.ihsv, tuple) and len(c.irgb) == 3)
        lw.Assert(isinstance(c.dhsv, tuple) and len(c.drgb) == 3)
        lw.Assert(isinstance(c.ihls, tuple) and len(c.ihls) == 3)
        lw.Assert(isinstance(c.dhls, tuple) and len(c.dhls) == 3)
        # Hex string properties return proper hex forms
        s, n = c.xrgb, 7
        lw.Assert(isinstance(s, str) and len(s) == n and s[0] == "#")
        s = c.xhsv
        lw.Assert(isinstance(s, str) and len(s) == n and s[0] == "@")
        s = c.xhls
        lw.Assert(isinstance(s, str) and len(s) == n and s[0] == "$")
    def Test_Color_Constructor_1Arg():
        Reset()
        if 1:  # Color instance:  make a copy
            c = Color(0.1, 0.2, 0.3)
            c1 = Color(c)
            lw.Assert(c.drgb == c1.drgb)
        if 1:  # Name
            c = Color("Red")
            lw.Assert(c.irgb == (254, 0, 0))
        if 1:  # Hex strings
            for i in "@#$":
                c = Color(f"{i}000000")
                lw.Assert(c.irgb == (0, 0, 0))
            c = Color("#010203")
            lw.Assert(c.irgb == (1, 2, 3))
            # Note the HSV and HLS transformations can lose a little
            # information because of conversion between ints and floats.
            c = Color("@010203")
            lw.Assert(c.ihsv == (0, 0, 3))
            c = Color("@808080")
            lw.Assert(c.ihsv == (128, 129, 128))
            lw.Assert(c.ihls == (128, 95, 86))
            c = Color("$010203")
            lw.Assert(c.ihls == (0, 2, 0))
        if 1:  # Single number:  wavelength in nm or gray or 8-bit number
            # Wavelengths
            expected = (1.0, 0.859, 0.0)
            for i in (589, 589.0, Decimal(589), Fraction(589, 1)):
                c = Color(i)  # About sodium yellow-orange
                rgb = tuple(round(i, 3) for i in c.drgb)
                lw.Assert(rgb == expected)
                if have_mpmath:
                    c = Color(mpmath.mpf(float(i)))
                    rgb = tuple(round(i, 3) for i in c.drgb)
                    lw.Assert(rgb == expected)
            black = (0.0, 0.0, 0.0)
            for i in (0, -300, -300.0, 300, 300.0, 800, 800.0):
                c = Color(i, hsv=True)  # hsv keyword ignored for 1 argument
                lw.Assert(c.irgb == black)
                c = Color(i, hls=True)  # hls keyword ignored for 1 argument
                lw.Assert(c.irgb == black)
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
                (1.0, 1.0),
            ):
                c = Color(a, a, a)
                rgb = tuple(round(i, 3) for i in c.drgb)
                lw.Assert(rgb == (b, b, b))
            # Integers on [0, 255]:  ANSI 8-bit colors
            c = Color(200)
            lw.Assert(c.irgb == (255, 0, 215)) # It's a medium magenta
    def Test_Color_Constructor_3Args():
        Reset()
        if 1:  # Integer arguments
            for a in (0, 1, 2, 254, 255, 256):
                b = (a, a, a)
                c = Color(*b)
                expected = tuple(i & c.n for i in b)
                lw.Assert(c.irgb == expected)
            # Works for 10-bit arguments
            Color.bits_per_color = 10
            a = 1023
            b = (a, a, a)
            c = Color(*b)
            lw.Assert(c.irgb == b)
            Reset()
        if 1:  # Float arguments
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
                lw.Assert(got == expected)
        if 1:  # Normalization of floats
            a = 1.0001
            t = (a, a, a)
            c = Color(*t)
            mag = sum(i*i for i in t) ** (1/2)
            dec = tuple(i/mag for i in t)
            rgb = c.dec_to_int(dec)
            lw.Assert(c.irgb == rgb)
            #
            a = (0.99999, 1.00001, 1.0)
            c = Color(*a)
            mag = sum(i*i for i in t) ** (1/2)
            dec = tuple(i/mag for i in t)
            rgb = c.dec_to_int(dec)
            lw.Assert(c.irgb == rgb)
            #
            # Normalization with one very large component effectively gives a
            # monochromatic color
            c = Color(1e9, 1, 1)
            lw.Assert(c == Color(255, 0, 0))
        if 1:  # Fraction arguments
            for n, d, e in ((0, 1, 0.0), (1, 2, 0.498), (2, 3, 0.667), (1, 1, 1.0)):
                a = Fraction(n, d)
                c = Color(a, a, a)
                got = tuple(round(i, 3) for i in c.drgb)
                expected = (e, e, e)
                lw.Assert(got == expected)
        if 1:  # Decimal arguments
            for x, e in (
                ("0", 0.0),
                ("0.5", 0.498),
                ("0.666667", 0.667),
                ("1.0", 1.0),
            ):
                a = Decimal(x)
                c = Color(a, a, a)
                got = tuple(round(i, 3) for i in c.drgb)
                expected = (e, e, e)
                lw.Assert(got == expected)
        if 1:  # mpmath.mpf arguments
            if have_mpmath:
                for x, e in (
                    ("0", 0.0),
                    ("0.5", 0.498),
                    ("0.666667", 0.667),
                    ("1.0", 1.0),
                ):
                    a = mpmath.mpf(x)
                    c = Color(a, a, a)
                    got = tuple(round(i, 3) for i in c.drgb)
                    expected = (e, e, e)
                    lw.Assert(got == expected)
    def Test_ColorConstructorKeywords():
        Reset()
        # Test keyword arguments
        c = Color(16, 16, 16, hsv=True)
        lw.Assert(c == Color(16, 15, 15))
        c = Color(16, 16, 16, hls=True)
        lw.Assert(c == Color(17, 16, 15))
        # sunlight and gamma used to be OK, but I removed them Feb 2026
        for kw in "sunlight gamma aaa bbb".split():
            mykw = {kw: 0}
            lw.raises(ValueError, Color, 0, 0, 0, **mykw)
    def Test_Color_int_to_hex():
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
            lw.Assert(y == d)
    def Test_ColorHash():
        a, bpc = (18, 3333, 3578457), 28
        c = Color(*a, bpc=bpc)
        got = hash(c)
        expected = hash((a, bpc))
        lw.Assert(got == expected)
    def Test_ColorInvariants():
        '''Make sure things like
            c = Color('mag')
            c1 = Color(c.xhls)
            assert(c == c1)
        are true.
        '''
        distances = []
        for i in GetShortNames(all=True):
            c = Color(i)
            c1 = Color(c.xhls)
            if c != c1:
                dist = flt(Color.dist(c, c1))
                distances.append(dist)
                lw.Assert(dist < 0.014)
                # print(f"Failed for {i}:  {c} {c1} dist={dist}")
        if 0 and distances:
            # Note max possible distance value is 1.  Max is 0.0136 for
            # vio.  So, it's either ignore any dist < 0.014 or see if the
            # calculations with Fractions produces better conversions.
            print(f"Max dist = {max(distances)}")
            print("Tests failed")
            exit(1)
    if 1:  # Example stuff
        def ShowAttributes():
            c = trm.Trm()
            def f(a):
                return c(attr=a)
            c.it = c(attr="it")
            c.rv = c(attr="rv")
            c.di = c(attr="di")
            c.ul = c(attr="ul")
            c.so = c(attr="so")
            c.hi = c(attr="hi")
            if 0:
                print(wrap.dedent(f'''
                Text attributes (e.g., t('ornl', attr="ul"))
                    ('hide' is to the right of 'dim')
                    {f("no")}normal      no{c.n}       {f("bo")}bold        bo{c.n}
                    {f("it")}italic      it{c.n}       {f("ul")}underline   ul{c.n}
                    {f("bl")}blink       bl{c.n}       {f("rb")}rapidblink  rb{c.n}
                    {f("rv")}reverse     rv{c.n}       {f("so")}strikeout   so{c.n}
                    {f("di")}dim         di{c.n}       {f("hi")}hide         hi{c.n}
                    sub{f("sb")}script   {c.n}sb       super{f("sp")}script {c.n}sp
                '''.rstrip()))
            else:
                n = c.n
                print(f"Text attributes:  no it bl rv di bo ul rb so hi sb sp")
                print(f"  In WSL:  {c.it}it{n} {c.rv}rv{n} {c.di}di{n} {c.ul}ul{n} ", end="")
                print(f"{c.so}so{n} \"{c.hi}hi{n}\"(hi, but it's hidden)")
        def ColorTable(bits):
            c = trm.Trm()
            width = int(os.environ["COLUMNS"])
            width + 1   # Dummy to quiet linter
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
            try:
                term = os.environ["TERM_PROGRAM"]
            except KeyError:
                term = os.environ["TERM"]
            if bits == 24:
                print(f"Running on '{term}' terminal")
                Tbl("Dim text, dim background", False, False)
                Tbl("Bright text, dim background", True, False)
                Tbl("Dim text, bright background", False, True)
                Tbl("Bright text, bright background", True, True, last=False)
                c.out(c.n)
            elif bits == 4:
                print(f"Running on '{term}' terminal")
                Tbl("Dim text", False, False)
                Tbl("Bright text", True, False, last=False)
            elif bits == 8:
                Print256Colors()
        def Examples():
            # These work under mintty (https://mintty.github.io/)
            '''
            - theme example with Trm.load()
            - regexp matches
            - Unicode in sub/superscripts (e.g., Hz**(1/2)
            '''
            c = trm.Trm()
            c.hdr = c(attr="ul")
            def Header():
                c.print(wrap.dedent(f'''
                {c.hdr}Demonstration of some color.py features{c.n}
                '''))
            def Theme():
                # ∞∞2 This needs to be redone
                x = trm.Trm()
                s = "This {ul}truth{n} is well-{em}fixed{n} in our minds."
                x.print(wrap.dedent(f'''
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
                theme1 = wrap.dedent('''
                    ul None None ul
                    em yell None
                ''')
                x.load(theme1)
                d = {"ul": x.ul, "em": x.em, "n": x.n}
                x.print("\n    First  style: ", s.format(**d))
                # Load the second theme
                x.print(wrap.dedent('''
 
                    The second "theme" will use reversed 'yell' text for the ul style and
                    italics for the em style:
                '''))
                theme2 = wrap.dedent('''
                    ul yell None rv
                    em None None it
                ''')
                x.load(theme2)
                d = {"ul": x.ul, "em": x.em, "n": x.n}
                x.print("\n    Second style: ", s.format(**d))
            def Exponents():
                c = trm.Trm()
                n = c.n
                cl = "yel"
                e = c(cl)
                u = c(cl, attr="sp")
                b = c(cl, attr="sb")
                c.print(wrap.dedent(f'''
                    {c.yel}Exponents{c.n}
                    The terminal can display exponents and subscripts, even using Unicode
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
                c = trm.Trm()
                cl = "grn"
                n, a, d = c.n, c(cl), c(None, None, attr="so")
                c.print(wrap.dedent(f'''
                    {c.yel}Text editing{c.n}
                    Using a green color for added text and strikethrough for deleted text, you can
                    show how some text has been edited:
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                '''))
                d = c("red", attr="so")
                c.print(wrap.dedent(f'''
                    The strikethrough text can be hard to see.  A quick change adds a red color:
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                '''))
                print()
            Header()
            #Theme()
            Exponents()
            TextEditing()
        def ShortNames():
            if 1:   # New stuff
                # My default names
                u = trm.Trm()
                u.ul = u(attr="ul")
                u.print(f"{u.ul}Default color names from trm.Trm():")
                u.list(horiz=True, columns=10)
                # Color by wavelength
                o = []
                for wl in range(400, 701, 10):
                    o.append(f"{u(wl)}{wl}{u.n}")
                u.print(f"{u.ul}Color by wavelength in nm:")
                for i in columnize.Columnize(o, columns=16, horiz=True, sep=" "*2):
                    print(i)
            else:   # Old stuff when Trm was in color.py
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
                c = trm.Trm()
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
                    # Print the RGB codes for the first two colors
                    k, kl, kd, kb = cn[i], cn[i + "l"], cn[i + "d"], cn[i + "b"]
                    print(f"{c(k)}{k.xrgb}{c.n} {c(kl)}{kl.xrgb}{c.n}", end=" ")
                    print(f"{c(kd)}{kd.xrgb}{c.n} {c(kb)}{kb.xrgb}{c.n}", end="")
                    print()
                print(wrap.dedent(f'''
    
                    Examples:               #ffffff = RGB, $ffffff = HLS, @ffffff = HSV
                        t(Color(0.35)) gives a {t(Color(0.35))}gray like this{t.n}
                        t('ornl') gives an {t("ornl")}orange like this{t.n}
                        t('ornl', 'royd') gives an {t("ornl", "royd")}orange on a royd background{t.n}
                        t('blk', 'yel', attr="rb") gives a {t("blk", "yel", attr="rb")}rapid blink{t.n}
                        Blinking doesn't work in WSL
                '''))
    def Int(s):
        "Convert s to an integer; 0x33 and 0o33 forms allowed"
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
            4.  An 8-bit integer on [0, 255]
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
        n = None
        try:
            n = Int(x)
        except Exception:
            pass
        # Set the variable rgb to a tuple of three base 10 integers
        if n:  # It's an 8-bit color number
            if 0 <= n <= 255:
                rgb = Translate8bit(n)
            else:
                Error("An 8-bit number must be between 0 and 255 inclusive")
            t.print(f"8-bit color name '{n}'    {t(rgb)}Represents this color")
            ShowRepresentations(rgb)
            return
        elif len(x) in (3, 4):  # Short name form
            try:
                c = CN[x]
                rgb = c.irgb
            except Exception:
                Error(f"'{x}' not recognized as a color name")
            t.print(f"Color name '{x}'    {t(c)}Represents this color")
            ShowRepresentations(c)
            return
        elif x[0] in "@#$":  # Hex form
            c = Color(x)
            rgb = c.irgb
        else:  # Three numbers
            # Must be 3 RGB numbers separated by white space (either
            # integers or floats)
            if "." in x or "e" in x:  # Three floats
                rgb = [Int(255*float(i)) for i in x.split()]
            else:  # Three integers
                rgb = [Int(i) for i in x.split()]
        if len(rgb) != 3:
            Error(f"'{x!s}' doesn't represent three numbers")
        PrintRGB(s, x, rgb)
    def iDistribute(n, a, b):
        '''Generator to return an integer sequence [a, ..., b] with n elements equally distributed
        between a and b.  Raises ValueError if no solution is possible.  Example:
            a, b = 1, 6
            for n in range(2, 8):
                s = list(iDistribute(n, a, b))
                print(f"iDistribute({n}, {a}, {b}) = {s}")
        produces
            iDistribute(2, 1, 6) = [1, 6]
            iDistribute(3, 1, 6) = [1, 4, 6]
            iDistribute(4, 1, 6) = [1, 3, 4, 6]
            iDistribute(5, 1, 6) = [1, 2, 4, 5, 6]
            iDistribute(6, 1, 6) = [1, 2, 3, 4, 5, 6]
        with a ValueError exception on the n == 7 term.  For the case n == 4, note how the adjective
        "equally" needs to be interpreted "symmetrically" and for the case n == 5, even that's not
        true.
        
        If you need a sequence of n floating point values, see dputil.fDistribute().
        '''
        if not (isinstance(a, int) and isinstance(b, int) and isinstance(n, int)):
            raise TypeError("Arguments must be integers")
        if a >= b:
            raise ValueError("Must have a < b")
        if n < 2:
            raise ValueError("n must be >= 2")
        if n == 2:
            yield a
            yield b
            return
        dx = Fraction(b - a, n - 1)
        if dx < 1:
            raise ValueError("No solution")
        for i in range(n):
            yield int(round(a + i*dx, 0))
    def ShowRepresentations(c):
        "Show the Color instance c in various representations"
        q = "({:3d}, {:3d}, {:3d})"
        def dec(c):
            "c is a Color instance; return decimal string form"
            lw.Assert(isinstance(c, Color))
            t = tuple(f"{i:5.3f}" for i in c.drgb)
            return f"({', '.join(t)})"
        def P(x, name):
            "x is an integer tuple and name is RGB, HSV, or HLS"
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
        # Show some variations of this color in different lightness and saturation to
        # help with color selection.  Use the #ffffff form for the color specifier.
        # There currently are only 4 lines printed, so another 10 or 20 would be fine.
        # Column width is typically 88 and 8 chars are needed per spec, so 8 columns
        # would be fine.  Thus, choose 8 lightness and saturation values.
        H, S, V = c.ihsv
        r = (32, 64, 96, 128, 160, 192, 224, 255)
        Q = ' '.join(str(i) for i in r)
        R = ' '.join(f"{i:02X}" for i in r)
        print(f"  Same hue 0x{H:02X}:  value across, saturation down")
        print(f"  Numbers are {Q} ({R})")
        data = []
        for s in r:
            row = []
            for v in r:
                u = f"@{H:02x}{s:02x}{v:02x} "
                x = Color.Construct(Color, u)
                row.append(f"{t(x)}{u}{t.n}")
            data.append(row)
        tt.print(data, style=" "*15)
    def ShowShortNames(extra):
        u = trm.Trm()
        # Make a dict of the names vs. colors
        di = {}
        for i in trm.Trm.std:
            for j in ("l", "", "1", "2", "3"):
                di[i + j] = Color(i + j)
        w = 2   # Spaces between columns
        i, f, block = " "*w, lambda x: " "*x, "█"*6
        hdr = f"Name{f(8)}RGB{f(10)}XRGB{f(5)}XHSV{f(5)}XHLS{f(3)}8-BIT{f(3)}        "
        u.hdr = u("whtl", "royd", "")
        u.print(f"{u.hdr}{hdr}")
        for name, c in di.items():
            s = str(c).replace("C⁸", "")
            n = RGBtoANSI8bit(*c.irgb)
            c8 = Translate8bit(n)
            u.print(f"{u(c.xrgb)}{name:4s}{i}"
                    f"{s}{i}"
                    f"{c.xrgb}{i}"
                    f"{c.xhsv}{i}"
                    f"{c.xhls}{i}"
                    f"{u(c8.xrgb)}"
                    f"{n:3d} {block}{u(c.xrgb)}{block}")
        u.print(f"{u.hdr}{hdr}")
        if extra != "ll":
            print(wrap.dedent('''
            The solid blocks at the end of each line help you see the difference in color
            between the 8-bit and 24-bit representations.  There are only 256 of the 8-bit
            colors and the mapping isn't perfect.  Use 'll' to include a sample of text that
            compares these colors.'''))
            return
        # Print columnized text to show how text looks different; the use of solid
        # color blocks is a bit "strong" for how I use text in a terminal.
        u.print(f"\n{u(attr='ul')}Samples of text in the 24-bit and 8-bit color pairs:")
        o = []
        for name, c in di.items():
            n = RGBtoANSI8bit(*c.irgb)
            c8 = Translate8bit(n)
            s = f"{u(c.xrgb)}{name:4s} sample {u(c8.xrgb)}sample{u.n}"
            o.append(s)
        for i in columnize.Columnize(o):
            print(i)
        print("\nTo my eye, these 8-bit translations work OK except for:")
        print("  brnd dend lavd lipd pnkb pnkd royd sead")
    def ShowHTMLColors(by_hue=False):
        data = wrap.dedent('''
            AliceBlue #F0F8FF
            AntiqueWhite #FAEBD7
            Aqua #00FFFF
            Aquamarine #7FFFD4
            Azure #F0FFFF
            Beige #F5F5DC
            Bisque #FFE4C4
            Black #000000
            BlanchedAlmond #FFEBCD
            Blue #0000FF
            BlueViolet #8A2BE2
            Brown #A52A2A
            BurlyWood #DEB887
            CadetBlue #5F9EA0
            Chartreuse #7FFF00
            Chocolate #D2691E
            Coral #FF7F50
            CornflowerBlue #6495ED
            Cornsilk #FFF8DC
            Crimson #DC143C
            Cyan #00FFFF
            DarkBlue #00008B
            DarkCyan #008B8B
            DarkGoldenRod #B8860B
            DarkGray #A9A9A9
            DarkGrey #A9A9A9
            DarkGreen #006400
            DarkKhaki #BDB76B
            DarkMagenta #8B008B
            DarkOliveGreen #556B2F
            DarkOrange #FF8C00
            DarkOrchid #9932CC
            DarkRed #8B0000
            DarkSalmon #E9967A
            DarkSeaGreen #8FBC8F
            DarkSlateBlue #483D8B
            DarkSlateGray #2F4F4F
            DarkSlateGrey #2F4F4F
            DarkTurquoise #00CED1
            DarkViolet #9400D3
            DeepPink #FF1493
            DeepSkyBlue #00BFFF
            DimGray #696969
            DimGrey #696969
            DodgerBlue #1E90FF
            FireBrick #B22222
            FloralWhite #FFFAF0
            ForestGreen #228B22
            Fuchsia #FF00FF
            Gainsboro #DCDCDC
            GhostWhite #F8F8FF
            Gold #FFD700
            GoldenRod #DAA520
            Gray #808080
            Grey #808080
            Green #008000
            GreenYellow #ADFF2F
            HoneyDew #F0FFF0
            HotPink #FF69B4
            IndianRed #CD5C5C
            Indigo #4B0082
            Ivory #FFFFF0
            Khaki #F0E68C
            Lavender #E6E6FA
            LavenderBlush #FFF0F5
            LawnGreen #7CFC00
            LemonChiffon #FFFACD
            LightBlue #ADD8E6
            LightCoral #F08080
            LightCyan #E0FFFF
            LightGoldenRodYellow #FAFAD2
            LightGray #D3D3D3
            LightGrey #D3D3D3
            LightGreen #90EE90
            LightPink #FFB6C1
            LightSalmon #FFA07A
            LightSeaGreen #20B2AA
            LightSkyBlue #87CEFA
            LightSlateGray #778899
            LightSlateGrey #778899
            LightSteelBlue #B0C4DE
            LightYellow #FFFFE0
            Lime #00FF00
            LimeGreen #32CD32
            Linen #FAF0E6
            Magenta #FF00FF
            Maroon #800000
            MediumAquaMarine #66CDAA
            MediumBlue #0000CD
            MediumOrchid #BA55D3
            MediumPurple #9370DB
            MediumSeaGreen #3CB371
            MediumSlateBlue #7B68EE
            MediumSpringGreen #00FA9A
            MediumTurquoise #48D1CC
            MediumVioletRed #C71585
            MidnightBlue #191970
            MintCream #F5FFFA
            MistyRose #FFE4E1
            Moccasin #FFE4B5
            NavajoWhite #FFDEAD
            Navy #000080
            OldLace #FDF5E6
            Olive #808000
            OliveDrab #6B8E23
            Orange #FFA500
            OrangeRed #FF4500
            Orchid #DA70D6
            PaleGoldenRod #EEE8AA
            PaleGreen #98FB98
            PaleTurquoise #AFEEEE
            PaleVioletRed #DB7093
            PapayaWhip #FFEFD5
            PeachPuff #FFDAB9
            Peru #CD853F
            Pink #FFC0CB
            Plum #DDA0DD
            PowderBlue #B0E0E6
            Purple #800080
            RebeccaPurple #663399
            Red #FF0000
            RosyBrown #BC8F8F
            RoyalBlue #4169E1
            SaddleBrown #8B4513
            Salmon #FA8072
            SandyBrown #F4A460
            SeaGreen #2E8B57
            SeaShell #FFF5EE
            Sienna #A0522D
            Silver #C0C0C0
            SkyBlue #87CEEB
            SlateBlue #6A5ACD
            SlateGray #708090
            SlateGrey #708090
            Snow #FFFAFA
            SpringGreen #00FF7F
            SteelBlue #4682B4
            Tan #D2B48C
            Teal #008080
            Thistle #D8BFD8
            Tomato #FF6347
            Turquoise #40E0D0
            Violet #EE82EE
            Wheat #F5DEB3
            White #FFFFFF
            WhiteSmoke #F5F5F5
            Yellow #FFFF00
            YellowGreen #9ACD32
        ''')
        o = []
        if by_hue:
            for item in data.split("\n"):
                name, spec = item.split()
                c = Color(spec)
                o.append((c, item))
            # Sort by hue
            p = Color.Sort(o, get=lambda x: x[0])
            o = []
            for c, item in p:
                o.append(f"{t(c)}{item}{t.n}")
        else:
            for item in data.split("\n"):
                name, spec = item.split()
                c = u(Color(spec))
                o.append(f"{c}{item}{t.n}")
        for i in columnize.Columnize(o, esc=True):
            print(i)
    def PrintRGB(orig, x, rgb):
        "Show the color in various forms"
        q = "({:3d}, {:3d}, {:3d})"
        def dec(c):
            "c is a Color instance; return decimal string form"
            lw.Assert(isinstance(c, Color))
            t = tuple(f"{i:5.3f}" for i in c.drgb)
            return f"({', '.join(t)})"
        def P(x, name):
            "x is an integer tuple and name is RGB, HSV, or HLS"
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
        lw.Assert(len(rgb) == 3)
        lw.Assert(all([isinstance(i, int) for i in rgb]))
        c = Color(*rgb)
        t.print(f"Input string = '{orig}' = {t(c)}{x.strip()}")
        P(c.irgb, "RGB")
        P(c.ihsv, "HSV")
        P(c.ihls, "HLS")
    def Print256Colors():
        '''This prints the color numbers for 8-bit colors.  A quirk is that
        a newline is printed after the first 16 numbers.  This allows you
        to resize the terminal window to show the next row of 16-51; when
        you do this, the numbers are arranged as they are in the bitmap
        ~/.0rc/256colors.png.
        '''
        u = trm.Trm()
        out = []
        for i in range(256):
            u.c = u(Color(i).xrgb)
            out.append(f"{u.c}{i:3d}{u.n}")
        term = os.environ.get("TERM", "unknown")
        print(f"Table of 8-bit colors (on {term!r} terminal)")
        width = int(os.environ["COLUMNS"]) - 1
        # Print the first 16 colors
        indent = " "*2
        n = 16
        print(f"{indent}", end="")
        for i in out[:n]:
            print(f"{i} ", end="")
        print()
        del out[:n]
        for i in columnize.Columnize(out, horiz=True, width=width):
            print(f"{indent}{i}")
        print(
            "\nNote:  change terminal width to show numbers 16-51 in the second row and"
        )
        print("the table will coincide with the bitmap ~/.0rc/256colors.png.")
    def Wavelengths():
        '''Print a table of colors with their RGB specs as a function of approximate wavelength in
        nm.  Following this, print the color.py standard names with their approximate wavelengths.
        '''
        # Wavelength in nm to color specifier
        gamma = 0.8
        step_nm = 10
        print(f"{t.whtl}Wavelength in steps of {step_nm} nm to RGB colors")
        t.print("         rgb        hsv        hsl")
        out, out_long, count, i = [], [], 0, " "*4
        # Table for some named colors that are close to a wavelength
        c = {
            380: ("magl", ""),
            400: ("purl", " 406"),
            420: ("lill", " 422"),
            440: ("blu", ""),
            450: ("roy", ", royl 449"),
            460: ("denl", " 458"),
            470: ("sky", " 467"),
            490: ("cynl", ""),
            500: ("trql", " 498"),
            510: ("grnl", ""),
            540: ("lwn", " 537"),
            550: ("olvl", " 555"),
            580: ("yell", ""),
            620: ("brnl", " 618"),
            630: ("ornl", " 628"),
            640: ("redl", ", lip, lipl, pnk, pnkl 645"),
        }
        for nm in range(380, 781, step_nm):
            colornum = wl2rgb.wl2rgb(nm, gamma=gamma)
            s = colornum.xrgb
            out.append(f"{t(s)}{nm}{t.n}")
            if nm in c:
                a, b = c[nm]
                out_long.append(
                    f"{t(s)}{nm}{i}{s}{i}{colornum.xhsv}{i}{colornum.xhls}"
                    f" {t(a)}{a}{b}{t.n}"
                )
            else:
                out_long.append(
                    f"{t(s)}{nm}{i}{s}{i}{colornum.xhsv}{i}{colornum.xhls}{t.n}"
                )
            count += 1
        if 0:  # Columnize the short form
            o = columnize.Columnize(out, indent=" "*2, horiz=True)
            for line in o:
                print(line)
        else:  # Print table data
            for i in out_long:
                print(i)
        print(f"{count} wavelengths printed")
        # Color names to approximate wavelength
        print()
        o = []
        for name in colordict:
            c = colordict[name]
            wavelength_nm = wl2rgb.rgb2wl(c)
            o.append((name, wavelength_nm))
        # Print table by sorted names
        t.hdr = t("whtl", attr="ul")
        print(
            f"{t.hdr}color.py names with their approximate "
            f"wavelength in nm, sorted by name{t.n}"
        )
        o1 = []
        for i in sorted(o):
            o1.append(f"{t(i[0])}{i[0]:4s} {i[1]:3d}{t.n}    ")
        for i in columnize.Columnize(o1):
            print(i)
        # Print table sorted by wavelength
        print()
        print(
            f"{t.hdr}color.py names with their approximate "
            f"wavelength in nm, sorted by wavelength{t.n}"
        )
        o1 = []
        for i in sorted(o, key=lambda x: x[1]):
            o1.append(f"{t(i[0])}{i[1]:3d} {i[0]:4s}{t.n}    ")
        for i in columnize.Columnize(o1):
            print(i)
        print("Note that saturation plays a large part in how the color appears")
    def GetNames():
        '''Return a dict of my short color names sorted by name.  An example entry is 
            'sky': Color('$90c3ff', bpc=8).
        '''
        if 0:   # Old method with /plib/colornames0
            lines, di = get.GetLines("/plib/colornames0", nonl=True, script=True), {}
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                name, clr = line.split(":")
                di[eval(name)] = eval(clr)
            return di
        else:   # New method that uses the default colors in trm.Trm()
            t = trm.Trm()
            # The Trm class is a dict and its keys are the default color names I wish to
            # use.  The name pattern is that valid names are 3 or more letters.  Two
            # letter names are for attributes like "it" (italic).  The only one-letter
            # name is "n", which is the default terminal color.
            names = [i for i in t.keys() if len(i) >= 3]
            return {i: Color(i) for i in names}
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def ParseCommandLine(d):
        d["-t"] = False  # Run self-tests
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
                exit(lw.run(globals(), regexp="^Test_.*$", halt=True, verbose=0)[0])
        if not args:
            return ["s"]
        return args
    def Usage(status=1):
        print(wrap.dedent(f'''
        Usage:  {sys.argv[0]} [options] [cmd]
          cmd
           d    Show demo
           H    Show HTML colors sorted by hue
           h    Show HTML colors sorted by name
           l    List short names with various Color constructor arguments
           s    Show short names, attributes [default action for empty cmd]
           t4   Show 4-bit color table
           t8   Show 8-bit color table
           t24  Show 24-bit color table
           a    Attributes
           w    Show colors of light wavelengths (approximate)
         <num>  Convert color specifier on command line to various representations
                in RGB, HSV, and HLS.  Argument type examples:
                    'ornl',     '128 64 32',    '0x80 0o100 0b100000', '202'
                    '#804020',  '@0ebf80'       '$0e5099'
        Options
          -h      Print this help
          -t      Run self-tests
        '''))
        exit(status)
    d: dict[str, str|int] = {}  # Options dictionary
    cmds = ParseCommandLine(d)
    colordict = GetNames()
    if cmds[0] in colordict:
        # Interpret color strings on command line
        for i in cmds:
            InterpretColorSpecifier(i)
    else:
        first_char = cmds[0][0]
        if first_char == "d":    # Show examples
            Examples()
        elif first_char == "a":  # Show attributes
            ShowAttributes()
        elif first_char == "H":  # Show HTML colors by hue
            ShowHTMLColors(by_hue=True)
        elif first_char == "h":  # Show HTML colors
            ShowHTMLColors()
        elif first_char == "s":  # Default for no arguments
            ShortNames()
            print()
            ShowAttributes()
            print("\nUse d for examples, 't[4|8|24]' for color table, l for short name properties,")
            print("otherwise interpret the color specifier")
        elif first_char == "t":  # Show 4, 8, or 24 bit color table
            ColorTable(int(cmds[0][1:]))
        elif first_char == "l":  # Show #/@/$ and RGB numbers for short names
            ShowShortNames(cmds[0])
        elif first_char == "w":  # Show wavelengths and RGB color specifier
            Wavelengths()

def GetGist():
    gist = {}
    gist["gist"] = "Classes to help with color use in terminals"
    gist["copy"] = "Copyright © 2022 Don Peterson"
    gist["lic"] = "MIT License (see /plib/_lic.mit)"
    gist["test"] = "--test"
    gist["cat"] = "color"
    gist["todo"] = '''
    
    - ∞∞2 
        - Color.adjust could use some examples in the docstring, as I had forgotten
          about it and it's likely it's a tool I should use
            - Or add a demo function in the code that shows percentage adjustments,
              which is what I've been wanting to do.  It would be very nice if an 
              interactive function could be set up to use in the REPL that prompts you
              for an adjustment number and optional parameter and you'd see a set of 
              colors getting generated to the screen, letting you home into a desired
              color
        - Move RegexpDecorate to dpstr.py
    - RegexpDecorate.register() needs to change to an argument list of (r, match_style,
      nomatch_style) where the latter two elements are escape codes used to define how
      things should be printed.  The use case is pfind.py where I want to see
      directories printed in red with the sky color for the match; plain files are
      printed with the default text style but matches with sky.  Thus, the default for
      nomatch_style should be None, meaning the default text style.
    - TestInvariants() is made to pass, but I'd like to see the conversion work exactly.
      It could be a problem with decimal roundoff in the colorsys module.
        
    - More color names could be handy
        - White
            - pearl snow ivory cream egg cotton chiffon salt linen bone frost rice
              vanilla cloud casper moon ghost milk blizzard polar crystal
        - Black
            - ebony crow ink raven onyx soot coal obsidian
        - Gray
            - graphite iron pewter cloud silver smoke slate ash dove fog flint charcoal
              lead coin fossil lava rhino granite shark platinum
        - Purple
            - mauve violet lavender plum lilac grape iris orchid thistle prune indigo
              pansy fuchsia eggplant
        - Blue
            - ice baby robin egg blueberry navy slate sky navy indigo cobalt teal ocean
              azure lapis spruce denim sapphire arctic aqua steel royal
        - Green
            - juniper sage lime fern emerald pear moss shamrock pine mint seaweed pickle
              pistachio basil tea army kelly jungle apple laurel beryl tea moss sage
              spring copper mint army pea turtle lime leaf kiwi jade teal kelly aqua
              grass frog emerald shamrock kermit verdigris foilage glade willow mantis
              broccoli turf
        - Yellow
            - canary gold flax butter lemon mustard corn banana dijon honey blonde peach
              daffodil maize citrus topaz ochre custard tangerine melon straw saffron
              khaki papaya sand pee sun mustard
        - Orange
            - cider rust ginger tiger fire bronze apricot carrot amber yam mango papaya
              sunset coral paprika nectarine squash salmon caramel umber
        - Red
            - cherry rose jam merlot garnet ruby scarlet wine brick blood berry candy
              lipstick chili barn fuchsia punch rouge tomato flame cerise sunset pink
              pig barbie inferno claret
        - Tan
            - beige oat fawn sand sepia latte oyster desert caramel latte beach almond
              toffee vanilla butter wheat maple nutmeg
        - Brown
            - coffee mocha peanut wood pecan walnut caramel syrup umber tawny penny
              cedar cognac sienna
    
        Not in existing colornames:
            arctic    chili     ginger    nectarine robin
            baby      cider     glade     oat       salt
            barbie    coal      granite   obsidian  soot
            barn      coin      inferno   oyster    spring
            basil     cotton    ink       pansy     syrup
            beach     crow      jam       papaya    tawny
            beryl     daffodil  jungle    pecan     tiger
            blizzard  dijon     kelly     pee       turf
            blonde    dove      lapis     penny     turtle
            broccoli  egg       lead      pickle    willow
            candy     foilage   maple     pig       wood
            carrot    frog      moon      rice      yam
    '''
    return gist
