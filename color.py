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
            
            - ∞∞1 
                - Remove eval()/exec() stuff.  Trm.load() loads color names from a file,
                  but I don't like that it has to exec() the incoming string.  It would
                  be better if no eval() or exec() calls were made in this module.
                - .on and .off must work absolutely and reliably.  See _palette_proto.py
                  for a way of changing Trm to a dict instance to do this.
                    - .on can have three states:
                        - None means to use stdout.isatty()
                        - False means always off so all t.x attributes are ""
                        - True means always on so all t.x attributes are proper escape
                          codes
            - ∞∞2 
                - Move RegexpDecorate to dpstr.py
            - ∞∞3 
                - When printing a Trm instance that uses t.str(), output the string
                  using Columnize to the current screen width, as this is more
                  attractive.
            
            - RegexpDecorate.register() needs to change to an argument list of (r,
              match_style, nomatch_style) where the latter two elements are escape codes
              used to define how things should be printed.  The use case is pfind.py
              where I want to see directories printed in red with the sky color for the
              match; plain files are printed with the default text style but matches
              with sky.  Thus, the default for nomatch_style should be None, meaning the
              default text style.
            - TRM attributes should be "" if .on is False
                - This needs __getattr__ and __setattr__
                - Could change to methods:  on(), off(), none().
            - TestInvariants() is made to pass, but I'd like to see the conversion work
              exactly.  It could be a problem with decimal roundoff in the colorsys
              module.
                
            - More color names could be handy
                - White
                    - pearl snow ivory cream egg cotton chiffon salt linen bone frost
                      rice vanilla cloud casper moon ghost milk blizzard polar crystal
                - Black
                    - ebony crow ink raven onyx soot coal obsidian
                - Gray
                    - graphite iron pewter cloud silver smoke slate ash dove fog flint
                      charcoal lead coin fossil lava rhino granite shark platinum
                - Purple
                    - mauve violet lavender plum lilac grape iris orchid thistle prune
                      indigo pansy fuchsia eggplant
                - Blue
                    - ice baby robin egg blueberry navy slate sky navy indigo cobalt
                      teal ocean azure lapis spruce denim sapphire arctic aqua steel
                      royal
                - Green
                    - juniper sage lime fern emerald pear moss shamrock pine mint
                      seaweed pickle pistachio basil tea army kelly jungle apple laurel
                      beryl tea moss sage spring copper mint army pea turtle lime leaf
                      kiwi jade teal kelly aqua grass frog emerald shamrock kermit
                      verdigris foilage glade willow mantis broccoli turf
                - Yellow
                    - canary gold flax butter lemon mustard corn banana dijon honey
                      blonde peach daffodil maize citrus topaz ochre custard tangerine
                      melon straw saffron khaki papaya sand pee sun mustard
                - Orange
                    - cider rust ginger tiger fire bronze apricot carrot amber yam mango
                      papaya sunset coral paprika nectarine squash salmon caramel umber
                - Red
                    - cherry rose jam merlot garnet ruby scarlet wine brick blood berry
                      candy lipstick chili barn fuchsia punch rouge tomato flame cerise
                      sunset pink pig barbie inferno claret
                - Tan
                    - beige oat fawn sand sepia latte oyster desert caramel latte beach
                      almond toffee vanilla butter wheat maple nutmeg
                - Brown
                    - coffee mocha peanut wood pecan walnut caramel syrup umber tawny
                      penny cedar cognac sienna
                
        oo>
    '''
    if 1:   # Standard imports
        import colorsys
        from decimal import Decimal
        from fractions import Fraction
        import math
        import os
        import re
        import sys
        from io import StringIO
        from pathlib import Path as P
        from collections.abc import Iterable
        from collections import deque
        from string import hexdigits
    if 1:   # Custom imports
        from columnize import Columnize
        from wsl import wsl
        from wrap import dedent
        import dpseq
        import get
        from dpprint import PP
        import termtables as tt
        pp = PP()
        try:
            from f import flt
        except ImportError:
            flt = float
        # NOTE:  can't use debug.py because of circular import
        try:
            import mpmath
            have_mpmath = True
        except ImportError:
            have_mpmath = False
    if 1:   # Global variables
        class G:
            pass
        g = G()  # Container for global variables
        ii = isinstance
        __all__ = "Color Trm TRM t ColorName CN RegexpDecorate".split()
if 1:   # Classes
    class Color:
        "Storage of the three numbers used to define a color"
        bits_per_color = 8
        def __init__(self, *p, **kw):
            "Initialize the Color object"
            # ∞∞1 Need detailed docstring on Color constructor syntax (for pydoc use)
            # Check for proper keyword arguments
            allowed = set("bpc hsv hls sunlight gamma".split())
            actual = set(kw.keys())
            if not (actual <= allowed):
                bad = actual - allowed
                s = ", ".join(bad)
                msg = f"Bad keyword(s):  {s}"
                raise ValueError(msg)
            # Set attributes
            self._bpc = kw.get("bpc", Color.bits_per_color)
            self._rgb = None
            self._sort = "rgb"
            if len(p) == 3:
                if 0:
                    # Check type
                    t1 = type(p[0])
                    if type(p[1]) is t1 or type(p[2]) is t1:
                        msg = f"'{p}' components are not all the same type"
                        raise TypeError(msg)
                if all(ii(i, int) for i in p):  # 3 integers
                    rgb = tuple(i & self.n for i in p)
                else:  # Convert to floats
                    try:
                        dec = tuple(float(i) for i in p)
                    except Exception:
                        msg = f"'{p}' couldn't be converted to floats"
                        raise TypeError(msg)
                    if not all(0 <= i <= 1 for i in dec):  # Need normalization
                        mag = sum(i*i for i in dec) ** (1/2)
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
            "Check invariants"
            assert ii(self._bpc, int) and self._bpc > 0
            assert len(self._rgb) == 3
            assert (0 <= i < self.N and ii(i, int) for i in self._rgb)
            assert self._sort in ("rgb", "hsv", "hls")
        def string(self, X):
            "Return 3-tuple int rgb value from a string"
            assert ii(X, str)
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
                # It names an elementary color.  Use the module's default CN
                # instance to decode this.
                try:
                    rgb = CN[x].irgb
                except Exception:
                    raise ValueError(f"'{x}' isn't recognized as a color name")
            assert all(0 <= i <= N and ii(i, int) for i in rgb)
            return rgb
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
            # per color values and compare equally to hier bpc colors.
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
                "Round and limit x to [0, self.n]"
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
                "Return int value of decimal values in 3-tuple of floats"
                assert all(ii(i, float) for i in three_tuple)
                return tuple(int(round(i*self.n, 1)) for i in three_tuple)
            def int_to_dec(self, three_tuple):
                "Return float value of 3-tuple of integers"
                assert all(ii(i, int) for i in three_tuple)
                return tuple(i/(self.N - 1) for i in three_tuple)
            def digits(self):
                '''Return number of digits for to use for decimal rounding,
                typically for printing to the screen.  Choose enough digits
                to hold all the color values.
                '''
                # self.N + 1 is the number of distinct color components.
                n = math.ceil(math.log10(self.N + 1))
                return max(1, n)
        if 1:  # Settable properties
            @property
            def sort(self):
                "Return sorting order string"
                return self._sort
            @sort.setter
            def sort(self, value):
                'Set sorting method:  "rgb", "hsv", or "hsl"'
                if value not in "rgb hsv hsl".split():
                    raise ValueError("value must be 'rgb', 'hsv', or 'hsl'")
                self._sort = value
        if 1:  # Read-only properties
            @property
            def sr(self):
                "Return short string form for RGB"
                a, b, c = self._rgb
                o = 0x100
                return f"R{chr(o + a)}{chr(o + b)}{chr(o + c)}"
            @property
            def sh(self):
                "Return short string form for HSV"
                a, b, c = self.ihsv
                o = 0x100
                return f"H{chr(o + a)}{chr(o + b)}{chr(o + c)}"
            @property
            def sl(self):
                "Return short string form for HLS"
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
                "How many bytes needed to express a color in hex"
                return math.ceil(self._bpc/8) + 1
            #
            @property
            def irgb(self):
                "Get rgb as a 3-tuple of integers on [0, 2**self.N - 1]"
                return self._rgb
            @property
            def drgb(self):
                "Get rgb as a 3-tuple of floats on [0, 1]"
                return tuple(i/(self.N - 1) for i in self._rgb)
            @property
            def xrgb(self):
                "Get rgb as a hex string of the form #000000"
                return "#" + Color.int_to_hex(self._rgb)
            #
            @property
            def ihsv(self):
                "Get hsv as a 3-tuple of integers on [0, 2**self.N - 1]"
                dec = colorsys.rgb_to_hsv(*self.drgb)
                hsv = tuple(int(round(i*(self.N - 1), 1)) for i in dec)
                return hsv
            @property
            def dhsv(self):
                "Get hsv as a 3-tuple of floats on [0, 1]"
                return colorsys.rgb_to_hsv(*self.drgb)
            @property
            def xhsv(self):     # @ffffff
                "Get hsv as a hex string of the form @000000"
                return "@" + Color.int_to_hex(self.ihsv)
            #
            @property
            def ihls(self):
                "Get hls as a 3-tuple of integers on [0, 2**self.N - 1]"
                dec = self.drgb
                hlsdec = colorsys.rgb_to_hls(*dec)
                hls = tuple(int(round(i*(self.N - 1), 1)) for i in hlsdec)
                return hls
            @property
            def dhls(self):
                "Get hls as a 3-tuple of floats on [0, 1]"
                return colorsys.rgb_to_hls(*self.drgb)
            @property
            def xhls(self):     # $ffffff
                "Get hls as a hex string of the form $000000"
                return "$" + Color.int_to_hex(self.ihls)
        if 1:  # Class methods
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
                    return d/3 ** (1/2)
            @classmethod
            def downshift(cls, c1, c2):
                "Return two Color instances with the same bpc (bits per color)"
                if not ii(c1, Color) or not ii(c2, Color):
                    raise TypeError("c1 and c2 need to be Color instances")
                bpc = min(c1.bpc, c2.bpc)
                return (c1.change_bpc(bpc), c2.change_bpc(bpc))
            @classmethod
            def int_to_hex(cls, s, bytes_per_color=1):
                "Convert 3-tuple of integers to hex string"
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
                t = "".join(x)
                assert (len(t) % 6) == 0
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
                if not ii(value, str) and ii(value, Iterable):
                    return tuple(round(float(i), n) for i in value)
                else:
                    if not ii(value, float):
                        raise TypeError("value must be a float or numerical sequence")
                    return round(value, n)
            @classmethod
            def Dot(cls, a, b):
                "Dot product of two sequences"
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
                    return 12.92*x if x <= 0.0031308 else 1.055*x ** (1/2.4) - 0.055
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
                    else:  # Use the predicate
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
            self._on = True  # If True, escape codes are generated
            # ColorNames dictionary (defaults to module's global variable CN)
            self.cn = CN
            self._bits = bits  # Bits per color
            if self._bits is None:
                self._bits = Trm.terminal_bits
            if self._bits != 24:
                raise ValueError("4 and 8 bit terminals not supported yet")
            self._fg = None  # Default foreground color
            self._bg = None  # Default background color
            self.reset()
            self._check()
        if 1:  # Utility methods
            def _check(self):
                "Validate the initial attributes"
                assert ii(self._bits, int) and self._bits in (4, 8, 24)
                assert ii(self._fg, Color)
                assert ii(self._bg, Color)
                assert ii(self.cn, ColorName)
            def _ta(self):
                "Return attributes mapping"
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
                "Return a set of user-defined attribute names"
                ignore = set(
                    '''_bits cn on _fg fg _bg bg _ta _always always _user _check
                    _get_code load n out print reset GetColorNames terminal_bits
                    default_color'''.split()
                )
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
                        if "bound" in s or "True_on" in s:
                            continue
                        out.append(s)
                classname = str(self.__class__)
                loc = classname.find(".")
                classname = classname[loc + 1:]
                if classname.endswith("'>"):
                    classname = classname[:-2]
                return classname + "(" + " ".join(out) + ")"
            def _get_code(self, color, bg=False):
                "For Color instance color, return escape code"
                if color is not None:
                    assert ii(color, Color)
                else:
                    return ""
                assert ii(bg, bool)
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
                    "Convert color string"
                    if s == "None":
                        return None
                    else:
                        try:
                            n = int(s)
                            return n
                        except Exception:
                            return s
                lines = get.GetNumberedLines(file)
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
                        attrs = " ".join(attrs)
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
                "Sets the instance to a default state"
                # Delete all user-set attributes
                for i in self._user():
                    try:
                        delattr(self, i)
                    except AttributeError as e:
                        if 0:  # Use to flag programming problems
                            print(e)
                            breakpoint()
                        else:
                            pass  # Ignore the problem
                # Reset to default colors
                self._fg, self._bg = Trm.default_color
                # Turn on output unless not to terminal
                self._on = False
                so = sys.stdout
                if (hasattr(so, "isatty") and so.isatty()) or self.always:
                    self._on = True
        if 1:  # Core methods
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
                        if "@" in fg or "#" in fg or "$" in fg:  # It's a composite
                            new = self.cn.split(fg)
                        fg = self.cn[fg] if new is None else new
                if bg and ii(bg, str):
                    if bg[0] in "@#$":
                        bg = Color(bg)
                    else:
                        new = None
                        if "@" in bg or "#" in bg or "$" in bg:  # It's a composite
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
                assert fg is None or ii(fg, Color)
                assert bg is None or ii(bg, Color)
                container.append(self._get_code(fg))
                container.append(self._get_code(bg, bg=True))
                return "".join(container)
            def print(self, *p, **kw):
                '''Print arguments with newline, reverting to normal color
                after finishing.
                '''
                self.out(*p, **kw)
                print(**kw)
            def out(self, *p, **kw):
                "Same as print() but no newline"
                k = kw.copy()
                if "end" not in k:
                    k["end"] = ""
                print(*p, **k)
                print(self.n, **k)
            def list(self, msg=None, ignore_std=True):
                'Print defined color attributes to stdout'
                std = set('''
                    blk blu brn cyn den grn gry lav lil lip lwn mag n  olv orn pnk pur red
                    roy sea sky trq vio wht yel'''.split())
                # Get the other standard names from colornames0
                with open("colornames0") as fp:
                    lines = fp.read().split("\n")
                    fp.close()
                while lines:
                    line = lines.pop(0).strip()
                    if not line:
                        continue
                    if line.strip()[0] == "#":
                        continue
                    s = line.split(":")[0].replace("'", "")
                    std.add(s)
                o = []
                for i in sorted(dir(self)):
                    s = eval(f"self.{i}")
                    try:
                        if s.startswith("\x1b["):
                            if ignore_std and i in std:
                                continue
                            o.append(f"{s}t.{i}{t.n}")
                    except Exception:
                        pass
                if o:
                    if msg is not None:
                        if msg.strip():
                            print(msg)
                    else:
                        if ignore_std:
                            print("class Trm color attributes ignoring standard ones:")
                        else:
                            print("class Trm color attributes:")
                    for i in Columnize(o, indent="  ", sep=" "*4):
                        print(i)
        if 1:  # Writable properties
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
        if 1:  # Read-only properties
            @property
            def n(self):
                "Return escape code for normal (default) screen"
                if not self._on:
                    return ""
                s = []
                s.append(self._get_code(self._fg, bg=False))
                s.append(self._get_code(self._bg, bg=True))
                s.append("\x1b[0m")  # Normal text attribute
                return "".join(s)
            @property
            def fg(self):
                "Returns default foreground color"
                if not self._on:
                    return ""
                return self._fg
            @property
            def bg(self):
                "Returns default background color"
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
        sep = ":"  # Separator string:  name<sep>Color_instance
        allow_exec = True  # Allow exec() of expressions
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
            return "\n".join(out)
        def load(self, file: str, clear=False):
            '''Extend ourselves by loading colors from file.  Set clear to True
            to first empty the dictionary.
            '''
            if clear:
                self.clear()
            vars = {}
            with open(file) as fd:
                contents = fd.read()
            for line in contents.split("\n"):
                line = line.strip()
                if not line or line[0] == "#":
                    continue
                if ColorName.sep in line:
                    a, b = line.split(ColorName.sep)
                    name = eval(a)
                    if self._normalize:
                        print("color.py exception reading colornames0:  normalization not implemented yet")
                        raise Exception("Normalization not implemented yet ∞∞2")
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
                        print(f"color.py exception reading colornames0:  illegal line:\n'{line}'")
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
if 1:   # Global variables
    # Define default ColorName instance
    CN = ColorName()
    if wsl:
        CN.load("/plib/colornames0")
    else:
        CN.load("d:/cygwin64/plib/colornames0")
    # Define default Trm instance
    TRM = Trm()
    t = TRM  # I use 't' so much it should be defined
    TRM.cn = CN
if 1:  # Add standard names based on resistor color code as t's attributes
    '''Add a number of attributes to the t instance giving the regular and light colors in the
    color table using my standard names.
    '''
    clrs = '''blk brn red orn yel grn blu vio gry wht cyn mag
              pnk lip lav lil pur roy den sky trq sea lwn olv'''.split()
    for clr in clrs:
        for i in ("", "l", "d", "b"):
            exec(f"t.{clr}{i} = t('{clr}{i}')")
    if 0:
        # Test that we got desire colors
        t.print(f"{t.mag}mag")
        t.print(f"{t.magl}magl")
        t.print(f"{t.magd}magd")
        t.print(f"{t.magb}magb")
if 1:   # RegexpDecorate class
    class RegexpDecorate:
        '''Decorate regular expression matches with color
        
        The styles attribute is a dictionary that contains the styles to apply for each regexp's match
        (key is the compiled regexp).  The style is a tuple of 1 to 3 values:  fg color, bg color, and
        text attributes.  None means to use the default.
        
        Example use:  highlight lines to stdout that contain '[Mm]adison'
        
            rd = RegexpDecorate()
            r = re.compile(r"[Mm]adison")
            fg = t.yell
            bg = t.n
            # Note fg and bg must be escape sequences
            rd.register(r, fg, bg)    # Print matches in light yellow on black
            for line in open(file).readlines():
                rd(line)    # Lines with matches are printed to stdout
                
            Can also be done with
                rd(open(file))
                
        Suppose you have python files in a directory "mydir" and you're interested in knowing how many
        lines contain the string "MySymbol".  This can be done with
        
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
        def register(self, r, match_style, nomatch_style=None):
            '''Register a regular expression and its styles
            
            Arguments:
                - match_style:  escape code to print before a match
                - nomatch_style:  escape code to print before a nonmatching string.  If it is None,
                  then t.n is used as the return-to-standard escape code.
                  
            You can generate these escape codes with a TRM instance.
            
            If your escape code for match_style includes an attribute, you'll want to include
            the 'no' attribute for normal text in your nomatch_style.  Otherwise, the remaining text
            will continue to be printed in the match_style's attribute.  The easiest way to do this is
            to not set nomatch_style.
            '''
            assert ii(r, re.Pattern)
            if nomatch_style is None:
                nomatch_style = t.n
            self._styles[r] = (match_style, nomatch_style)
        def unregister(self, r):
            "Remove regexp r from our styles dict"
            if r in self._styles:
                del self._styles[r]
        def __str__(self):
            return f"RegexpDecorate(<styles={len(self._styles)}>)"
        def __repr__(self):
            return str(self)
        def decorate(self, line):
            '''Apply the registered regular expressions to the string line and return the string,
            decorated if there was a match.
            '''
            assert ii(line, str)
            out = StringIO()
            self(line, file=out)
            return out.getvalue()
        def __call__(self, line, file=sys.stdout, insert_nl=False):
            '''Print the decorated line to a stream.  Check line for a match to one of the
            registered regexps and if there's a match, print the decorated line to the indicated
            stream.  Returns True if there was a match, False otherwise.
            
            Arguments:
                - line:  String to search
                - file:  Stream to send the decorated line
                - insert_nl:  If True, print a newline if line doesn't end with a newline.
                
            '''
            assert ii(line, str)
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
                print(f"{t.n}", end="")  # Default text style
                if not line and not has_nl and insert_nl:
                    print(file=file)
            return True
if 1:  # Translate between ANSI 8-bit colors (256 of them) and 24-bit RGB colors
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
            assert ii(v, int)
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
        if ii(rgb1, Color):
            seq1 = rgb1.irgb
        else:
            assert ii(rgb1, (list, tuple)) and len(rgb1) == 3
            assert all(ii(i, int) for i in rgb1)
            seq1 = rgb1
        if ii(rgb2, Color):
            seq2 = rgb2.irgb
        else:
            assert ii(rgb2, (list, tuple)) and len(rgb2) == 3
            assert all(ii(i, int) for i in rgb2)
            seq2 = rgb2
        d = [(i - j)**2 for i, j in zip(seq1, seq2)]
        return math.isqrt(sum(d))
    def ToIntRGB(rgb):
        'Convert 3-tuple of floats on [0, 1] to [0, 255]'
        return tuple(dpseq.Clamp((int(i*256) for i in rgb), low=0, high=255, typ=int))

if __name__ == "__main__":
    import getopt
    from lwtest import run, raises, Assert
    from collections import deque
    from columnize import Columnize
    from wrap import dedent
    from dpprint import PP
    pp = PP()  # Screen width aware form of pprint.pprint
    from wsl import wsl  # wsl is True when running under WSL Linux
    import wl2rgb
    def GetScreen():
        "Return (LINES, COLUMNS)"
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1,
        )
    def GetColors():
        t.dbg = t("cyn") if g.dbg else ""
        t.N = t.n if g.dbg else ""
        t.err = t("redl")
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="", file=Dbg.file)
            k = kw.copy()
            k["file"] = Dbg.file
            print(*p, **k)
            print(f"{t.N}", end="", file=Dbg.file)
    Dbg.file = sys.stderr  # Debug printing to stderr by default
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
    def Test8bitConversions():
        for i in range(256):
            rgb1 = Translate8bit(i)
            n = RGBtoANSI8bit(*rgb1.irgb)
            rgb2 = Translate8bit(n)
            dist = ColorDistance(rgb1, rgb2)
            Assert(not dist)
    def TestTrm():
        # Not exhaustive, but will test some features.  Tested only
        # under mintty 3.5.2.
        t = Trm()
        t.m = t(Color(239, 132, 239), attr="rv")  # Orchid for test case headings
        def TestLoad():
            "Test Trm.load() from file, stream and string"
            t.print(f"{t.m}Test of Trm.load()")
            s = "/tmp/tmp.clr.py"
            f = P(s)
            open(P(s), "w").write("err redl None\n")
            x = Trm()
            x.load(f, show=True)  # File
            x.load(open(f), show=True)  # Stream
            s = "err redl None"
            x.load(s, show=True)  # String
            f.unlink()
        def TestRegexpDecorate():
            x = Trm()
            x.of = x(Color("blk"), Color("grnl"))
            x.man = x(Color("yell"), attr="rv rb")
            x.so = x(Color("redl"), Color("blul"))
            x.Is = x(None, None, attr="ul ol")
            t.print(
                dedent(f'''
                {t.m}Test of regular expression decoration{t.n}
                    'of' should be {x.of}of{x.n}{t.n}.
                    'man' should be {x.man}man{x.n}{t.n}.
                    'so' should be {x.so}so{x.n}{t.n}.
                    'is' should be lined as {x.Is}is{x.n}{t.n}.
            ''')
            )
            s = dedent('''
                However little known the feelings or views of such
                a man may be on his first entering a neighbourhood,
                this truth is so well fixed in the minds of the
                surrounding families, that he is considered the rightful
                property of some one or other of their daughters.\n
            ''')
            r = [
                (re.compile(r"of"), x.of),
                (re.compile(r"man"), x.man),
                (re.compile(r"so"), x.so),
                (re.compile(r"is"), x.Is),
            ]
            s  # Quiet linter
            r  # Quiet linter
            #PrintMatches(s, r)
        # TestLoad()             # Themes not working yet
        # TestRegexpDecorate()   # Not working yet
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
                c   # Quiet linter
                #c = Color(i, bpc=10)
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
        def Test_dist():
            n = 8
            m = 2**n - 1
            c1 = Color(0, 0, 0, bpc=n)
            c2 = Color(m, m, m, bpc=n)
            #x = Color.dist(c1, c2)
            Assert(Color.dist(c1, c2) == 1)
            Assert(Color.dist(c1, c2, taxicab=True) == 1)
        def TestEquality():
            Reset()
            if 1:  # Integers in constructor
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
            if 1:  # Floats in constructor
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
                return (sum((i - j) ** 2 for i, j in zip(x, y))/3) ** (1/2)
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
            if 1:  # Sorting
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
                Assert(seq1[0] == ("alice", a))
                Assert(seq1[1] == ("bob", b))
            if 1:  # Test the < operator
                a = Color("#000000")
                b = Color("#010000")
                Assert(a < b)
                Assert(not (b < a))
                Assert(not (a < a))
                Assert(not (b < b))
        def TestClassMethods():
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
                    Assert(f(arg) == expected)
                    got = g(expected, bytes_per_color)
                    Assert(got == arg)
                raises(TypeError, f, 0)
                raises(ValueError, f, "12345")
                raises(ValueError, f, "1234567890")
                raises(ValueError, f, "00000g")
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
                    Assert(f(pi, digits) == expected)
                # Test sequence
                seq = [pi, pi, pi]
                seq1 = f(seq, digits)
                a = round(pi, digits)
                Assert(seq1 == (a, a, a))
            if 1:  # Dot
                f = Color.Dot
                a, b = (1, 2, 3), (3, 2, 1)
                Assert(f(a, b) == 10)
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
                Assert(got == expected)
            if 1:  # wl2rgb
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
                #x = f(589, sunlight=F)
                Assert(f(589, sunlight=F) == Color(255, 219, 0, bpc=8))
                Assert(f(high, sunlight=F) == Color(0, 0, 0))
        def TestProperties():
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
            if 1:  # Color instance:  make a copy
                c = Color(0.1, 0.2, 0.3)
                c1 = Color(c)
                Assert(c.drgb == c1.drgb)
            if 1:  # Hex strings
                for i in "@#$":
                    c = Color(f"{i}000000")
                    Assert(c.irgb == (0, 0, 0))
                c = Color("#010203")
                Assert(c.irgb == (1, 2, 3))
                # Note the HSV and HLS transformations can lose a little
                # information because of conversion between ints and floats.
                c = Color("@010203")
                Assert(c.ihsv == (0, 0, 3))
                c = Color("@808080")
                Assert(c.ihsv == (128, 129, 128))
                Assert(c.ihls == (128, 95, 86))
                c = Color("$010203")
                Assert(c.ihls == (0, 2, 0))
            if 1:  # Single number:  wavelength in nm or gray
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
                    (1.0, 1.0),
                ):
                    c = Color(a, a, a)
                    rgb = tuple(round(i, 3) for i in c.drgb)
                    Assert(rgb == (b, b, b))
        def Test3ArgsColorConstructor():
            Reset()
            if 1:  # Integer arguments
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
                    Assert(got == expected)
            if 1:  # Normalization of floats
                a = 1.0001
                t = (a, a, a)
                c = Color(*t)
                mag = sum(i*i for i in t) ** (1/2)
                dec = tuple(i/mag for i in t)
                rgb = c.dec_to_int(dec)
                Assert(c.irgb == rgb)
                a = (0.99999, 1.00001, 1.0)
                c = Color(*a)
                mag = sum(i*i for i in t) ** (1/2)
                dec = tuple(i/mag for i in t)
                rgb = c.dec_to_int(dec)
                Assert(c.irgb == rgb)
            if 1:  # Fraction arguments
                for n, d, e in ((0, 1, 0.0), (1, 2, 0.498), (2, 3, 0.667), (1, 1, 1.0)):
                    a = Fraction(n, d)
                    c = Color(a, a, a)
                    got = tuple(round(i, 3) for i in c.drgb)
                    expected = (e, e, e)
                    Assert(got == expected)
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
                    Assert(got == expected)
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
                        Assert(got == expected)
        def TestConstructorKeywords():
            #kw = {"bpc": 8, "hsv": 0, "hls": 0, "sunlight": 0, "gamma": 0}
            #c = Color(0, 0, 0, **kw)
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
                    # print(f"Failed for {i}:  {c} {c1} dist={dist}")
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
    if 1:  # Example stuff
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
            c = Trm(bits=24)
            c.hdr = c(attr="ul")
            def Header():
                c.print(
                    dedent(f'''
                {c.hdr}Demonstration of some color.py features{c.n}
 
                ''')
                )
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
                x.print(dedent('''
 
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
                c.print(
                    dedent(f'''
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
                ''')
                )
            def TextEditing():
                cl = Color("grnl")
                n, a, d = c.n, c(cl), c(None, None, attr="so")
                c.print(
                    dedent(f'''
 
                    {c.hdr}Text editing{c.n}
                    Using a green color for added text and strikethrough for deleted text, you can
                    show how some text has been edited:
            
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                ''')
                )
                cl = Color("redl")
                d = c(cl, attr="so")
                c.print(
                    dedent(f'''
 
                    The strikethrough text can be hard to see.  A quick change adds a red color:
 
                        This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
                ''')
                )
                print()
            Header()
            # Theme()
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
                # Print the RGB codes for the first two colors
                k, kl, kd, kb = cn[i], cn[i + "l"], cn[i + "d"], cn[i + "b"]
                print(f"{c(k)}{k.xrgb}{c.n} {c(kl)}{kl.xrgb}{c.n}", end=" ")
                print(f"{c(kd)}{kd.xrgb}{c.n} {c(kb)}{kb.xrgb}{c.n}", end="")
                print()
            print(dedent(f'''
 
                Examples:               #ffffff = RGB, $ffffff = HLS, @ffffff = HSV
                    t(Color(0.35)) gives a {t(Color(0.35))}gray like this{t.n}
                    t('ornl') gives an {t("ornl")}orange like this{t.n}
                    t('ornl', 'royd') gives an {t("ornl", "royd")}orange on a royd background{t.n}
                    t('blk', 'yel', attr="rb") gives a {t("blk", "yel", attr="rb")}rapid blink{t.n}
                    Blinking doesn't work in WSL
            ''')
            )
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
        
        If you need a sequence of n floating point values, see util.fDistribute().
        '''
        if not (ii(a, int) and ii(b, int) and ii(n, int)):
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
            Assert(ii(c, Color))
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
        if 1:   # Make a dict of the names vs. colors
            lines = get.GetLines("/plib/colornames0", nonl=1, script=1, strip=1, ignore_empty=1)
            di = {}
            for line in sorted(lines):
                line = line.strip()
                name, clr = [i.strip() for i in line.split(":")]
                c = eval(clr)
                di[name.replace("'", "")] = c
        w = 2   # Spaces between columns
        i, f, block = " "*w, lambda x: " "*x, "█"*6
        hdr = f"Name{f(8)}RGB{f(10)}XRGB{f(5)}XHSV{f(5)}XHLS{f(5)}8-BIT{f(3)}Name "
        t.hdr = t("whtl", "royd", "")
        t.print(f"{t.hdr}{hdr}")
        for name, c in di.items():
            s = str(c).replace("C⁸", "")
            n = RGBtoANSI8bit(*c.irgb)
            c8 = Translate8bit(n)
            t.print(f"{t(c)}{name:4s}{i}"
                    f"{s}{i}"
                    f"{c.xrgb}{i}"
                    f"{c.xhsv}{i}"
                    f"{c.xhls}{i}"
                    f"{t(c8)}"
                    f"{n:3d}{block}{t(c)}{block}")
        t.print(f"{t.hdr}{hdr}")
        if extra != "ll":
            print(dedent('''
            The solid blocks at the end of each line help you see the difference in color
            between the 8-bit and 24-bit representations.  There are only 256 of the 8-bit
            colors and the mapping isn't perfect.  Use 'll' to include a sample of text that
            compares these colors.'''))
            return
        # Print columnized text to show how text looks different; the use of solid
        # color blocks is a bit "strong" for how I use text in a terminal.
        t.print(f"\n{t(attr='ul')}Samples of text in the 24-bit and 8-bit color pairs:")
        o = []
        for name, c in di.items():
            n = RGBtoANSI8bit(*c.irgb)
            c8 = Translate8bit(n)
            s = f"{t(c)}{name:4s} sample {t(c8)}sample{t.n}"
            o.append(s)
        for i in Columnize(o):
            print(i)
        print("\nTo my eye, these 8-bit translations work OK except for:")
        print("  brnd dend lavd lipd pnkb pnkd royd sead")
    def ShowHTMLColors(by_hue=False):
        data = dedent('''
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
                c = t(Color(spec))
                o.append(f"{c}{item}{t.n}")
        for i in Columnize(o, esc=True):
            print(i)
    def PrintRGB(orig, x, rgb):
        "Show the color in various forms"
        q = "({:3d}, {:3d}, {:3d})"
        def dec(c):
            "c is a Color instance; return decimal string form"
            Assert(ii(c, Color))
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
        Assert(len(rgb) == 3)
        Assert(all([ii(i, int) for i in rgb]))
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
        out = []
        for i in range(256):
            ci = Translate8bit(i)  # Get Color instance
            t.c = t(ci)
            out.append(f"{t.c}{i:3d}{t.n}")
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
        for i in Columnize(out, horiz=True, width=width):
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
            o = Columnize(out, indent=" "*2, horiz=True)
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
        for i in Columnize(o1):
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
        for i in Columnize(o1):
            print(i)
        print("Note that saturation plays a large part in how the color appears")
    def GetNames():
        '''Return a dict of my short color names sorted by name.  An example entry is 
            'sky': Color('$90c3ff', bpc=8).
        '''
        lines, di = get.GetLines("/plib/colornames0", nonl=True, script=True), {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            name, clr = line.split(":")
            di[eval(name)] = eval(clr)
        return di
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
                exit(run(globals(), halt=True)[0])
        if not args:
            return ["s"]
        return args
    def Usage(status=1):
        print(dedent(f'''
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
    d = {}  # Options dictionary
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
