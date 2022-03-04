'''
This python module produces ANSI escape code strings to produce colors in
output to terminals (see https://en.wikipedia.org/wiki/ANSI_escape_code).
 
The primary component is the Clr object.  The basic colors use 3-letter
abbreviations: blk for black, blu for blue, grn for green, cyn for cyan,
mag for magenta, yel for yellow, and wht for wht.  An 'l' is prepended to
the name to get the bright form of that color.  These support the
traditional 4-bit terminal, which is the form I use the most for day-to-day
work (even though the terminal I use supports 24-bit color).
 
Here's basic usage:
 
    c = Clr()                   # Get an instance of the Clr class
    # We want red error messages
    err = c("red")
    print(f"{err}'xyzzy' is an unsupported keyword{c.n}")
 
The c.n attribute of the Clr instance is an escape code to return to the
normal terminal color.  c.print() and c.out() are convenience functions
that automatically emit the escape code in c.n.
 
Instead of using regular variables like 'err' above, you can add instance
attributes to the c instance
 
    c.err = c("red")
 
This is handy, as print(c) will show the Clr instance with the names of
its style attributes in their chosen form.
 
I call these attributes styles, as a common pattern in my scripts is to
define a number of these styles, then use them where needed in f-strings.
The Clr.load() method can be used to read in a number of these styles from
a file.
 
The functionality is in the Clr.__call__ method, which returns either an
ANSI escape sequence (or an empty string if output isn't to a terminal):
 
    def __call__(self, fg, bg=None, attr=None):
 
fg and bg are strings denoting the foreground and background colors
(integers for 8-bit terminals).  attr is a string describing the text
attributes you wish.  Example:  "it bl" gives italics (it) and blinking
text (bl).
 
TO USE THIS MODULE
    - Edit GetTerm() to set things up for your terminal
    - Set the Clr.n instance attribute to your normal color choices
    - Modify the CN4, CN8, CN24 class definitions of colors to your tastes
 
Run the module as a script to see example output.  Note that you'll not be
able to see all the 24-bit color choices, but use the argument of 'all' to
see typical XWindows' color names printed in their colors.
 
The functions PrintMatch() and PrintMatches() can decorate regular
expression matches in strings, helping you develop expressions faster.
 
My design goals for this module were:
    - Colors are defined by strings or integers
    - Terse syntax so things fit into f-strings
        - Short names for most-used colors
    - Easy to add/change colors
    - Support the terminals I use: mintty, Mac, xterm
    - Support the "styles" pattern
    - Allow color decoration of regular expression matches
    - Run as a script to see colors' names and effects
 
Other python libraries for color output you might want to look at are at
PyPI:  Colorama, termcolor, colored.
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
    # <programming> Provides the Clr object for ANSI escape sequences to
    # get colored text in terminals.  Replaces /plib/color.py.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import re
    import sys
    from enum import Enum, auto
    from functools import partial
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from get import GetNumberedLines
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # CN color classes
    if 1:   # 4-bit colors
        class CN4:
            '''Encapsulate 4-bit color names.  The default set is the following
            set of color names, functional on most terminals:
                blk,  blu,  grn,  cyn,  red,  mag,  yel,  wht
                lblk, lblu, lgrn, lcyn, lred, lmag, lyel, lwht
            '''
            def __init__(self, full=False):
                'full is ignored'
                self.dfg = {   # Foreground colors
                    "blk" : "0;30",
                    "blu" : "0;34",
                    "grn" : "0;32",
                    "cyn" : "0;36",
                    "red" : "0;31",
                    "mag" : "0;35",
                    "yel" : "0;33",
                    "wht" : "0;37",
                    "lblk": "1;30",
                    "lblu": "1;34",
                    "lgrn": "1;32",
                    "lcyn": "1;36",
                    "lred": "1;31",
                    "lmag": "1;35",
                    "lyel": "1;33",
                    "lwht": "1;37",
                }
                self.dbg = {   # Background colors
                    "blk" : "40",
                    "blu" : "44",
                    "grn" : "42",
                    "cyn" : "46",
                    "red" : "41",
                    "mag" : "45",
                    "yel" : "43",
                    "wht" : "47",
                    "lblk": "40",
                    "lblu": "44",
                    "lgrn": "42",
                    "lcyn": "46",
                    "lred": "41",
                    "lmag": "45",
                    "lyel": "43",
                    "lwht": "47",
                }
                self._default()
            def _default(self):
                'Set self.n to the default color'
                a = "\033[0m"   # Normal text attribute
                b = f"\033[{self.dfg['wht']};{self.dbg['blk']}m"
                self.n = a + b
            def _check(self, name):
                msg = f"'{name}' is an unrecognized color"
                if name not in self.dfg:
                    raise ValueError(msg)
            def fg(self, s):
                'Return the ANSI escape sequence for a foreground color'
                if s is None or not s:
                    return ""
                self._check(s)
                return f"\033[{self.dfg[s]}m"
            def bg(self, s):
                'Return the ANSI escape sequence for a background color'
                if s is None or not s:
                    return ""
                self._check(s)
                return f"\033[{self.dbg[s]}m"
    if 1:   # 8-bit colors
        class CN8:
            '''Encapsulate 8-bit color names.  The default set is the following
            set of color names, functional on most terminals:
                blk,  blu,  grn,  cyn,  red,  mag,  yel,  wht
                lblk, lblu, lgrn, lcyn, lred, lmag, lyel, lwht
            '''
            def __init__(self, full=False):
                'full is ignored'
                self._default()
            def _default(self):
                'Set self.n to the default color'
                a = "\033[0m"   # Normal text attribute
                self.n = a + self.fg(7) + self.bg(0)
            def fg(self, n=-1):
                '''Return the ANSI escape sequence for a foreground color.  If n is
                outside the range [0, 255], return the empty string.
                '''
                if n is None or not (0 <= n <= 255):
                    return ""
                return f"\033[38;5;{n}m"
            def bg(self, n=-1):
                '''Return the ANSI escape sequence for a background color.  If n is
                outside the range [0, 255], return the empty string.
                '''
                if n is None or not (0 <= n <= 255):
                    return ""
                return f"\033[48;5;{n}m"
    if 1:   # 24-bit colors
        xw = {  # Typical XWindows color names
            "aliceblue": (239, 247, 255),
            "antiquewhite": (249, 234, 214),
            "aquamarine": (51, 191, 193),
            "aquamarine1": (127, 255, 211),
            "aquamarine2": (117, 237, 198),
            "aquamarine3": (102, 204, 170),
            "aquamarine4": (68, 140, 114),
            "azure": (239, 255, 255),
            "azure1": (239, 255, 255),
            "azure2": (224, 237, 237),
            "azure3": (193, 204, 204),
            "azure4": (130, 140, 140),
            "beige": (244, 244, 219),
            "bisque": (255, 226, 196),
            "bisque1": (255, 226, 196),
            "bisque2": (237, 214, 183),
            "bisque3": (204, 183, 158),
            "bisque4": (140, 124, 107),
            "black": (0, 0, 0),
            "blanchedalmond": (255, 234, 204),
            "blue": (0, 0, 255),
            "blue1": (0, 0, 255),
            "blue2": (0, 0, 237),
            "blue3": (0, 0, 204),
            "blue4": (0, 0, 140),
            "blueviolet": (137, 43, 226),
            "brown": (165, 40, 40),
            "brown1": (255, 63, 63),
            "brown2": (237, 58, 58),
            "brown3": (204, 51, 51),
            "brown4": (140, 35, 35),
            "burlywood": (221, 183, 135),
            "burlywood1": (255, 211, 155),
            "burlywood2": (237, 196, 145),
            "burlywood3": (204, 170, 124),
            "burlywood4": (140, 114, 84),
            "cadetblue": (94, 145, 158),
            "chartreuse": (127, 255, 0),
            "chartreuse1": (127, 255, 0),
            "chartreuse2": (117, 237, 0),
            "chartreuse3": (102, 204, 0),
            "chartreuse4": (68, 140, 0),
            "chocolate": (209, 104, 30),
            "chocolate1": (255, 127, 35),
            "chocolate2": (237, 117, 33),
            "chocolate3": (204, 102, 28),
            "chocolate4": (140, 68, 17),
            "coral": (255, 114, 86),
            "coral1": (255, 114, 86),
            "coral2": (237, 107, 79),
            "coral3": (204, 91, 68),
            "coral4": (140, 61, 45),
            "cornflowerblue": (33, 33, 153),
            "cornsilk": (255, 247, 219),
            "cornsilk1": (255, 247, 219),
            "cornsilk2": (237, 232, 204),
            "cornsilk3": (204, 198, 175),
            "cornsilk4": (140, 135, 119),
            "cyan": (0, 255, 255),
            "cyan1": (0, 255, 255),
            "cyan2": (0, 237, 237),
            "cyan3": (0, 204, 204),
            "cyan4": (0, 140, 140),
            "darkgoldenrod": (183, 135, 10),
            "darkgreen": (0, 86, 45),
            "darkkhaki": (188, 183, 107),
            "darkolivegreen": (84, 86, 45),
            "darkorange": (255, 140, 0),
            "darkorchid": (140, 33, 140),
            "darksalmon": (232, 150, 122),
            "darkseagreen": (142, 188, 142),
            "darkslateblue": (56, 73, 102),
            "darkslategray": (45, 79, 79),
            "darkslategrey": (45, 79, 79),
            "darkturquoise": (0, 165, 165),
            "darkviolet": (147, 0, 211),
            "deeppink": (255, 20, 147),
            "deepskyblue": (0, 191, 255),
            "dimgray": (84, 84, 84),
            "dimgrey": (84, 84, 84),
            "dodgerblue": (30, 142, 255),
            "firebrick": (142, 35, 35),
            "firebrick1": (255, 48, 48),
            "firebrick2": (237, 43, 43),
            "firebrick3": (204, 38, 38),
            "firebrick4": (140, 25, 25),
            "floralwhite": (255, 249, 239),
            "forestgreen": (79, 158, 104),
            "gainsboro": (219, 219, 219),
            "ghostwhite": (247, 247, 255),
            "gold": (216, 170, 0),
            "gold1": (255, 214, 0),
            "gold2": (237, 201, 0),
            "gold3": (204, 173, 0),
            "gold4": (140, 117, 0),
            "goldenrod": (239, 221, 132),
            "goldenrod1": (255, 193, 38),
            "goldenrod2": (237, 181, 33),
            "goldenrod3": (204, 155, 28),
            "goldenrod4": (140, 104, 20),
            "green": (0, 255, 0),
            "green1": (0, 255, 0),
            "green2": (0, 237, 0),
            "green3": (0, 204, 0),
            "green4": (0, 140, 0),
            "greenyellow": (173, 255, 45),
            "honeydew": (239, 255, 239),
            "honeydew1": (239, 255, 239),
            "honeydew2": (224, 237, 224),
            "honeydew3": (193, 204, 193),
            "honeydew4": (130, 140, 130),
            "hotpink": (255, 104, 181),
            "indianred": (107, 56, 56),
            "ivory": (255, 255, 239),
            "ivory1": (255, 255, 239),
            "ivory2": (237, 237, 224),
            "ivory3": (204, 204, 193),
            "ivory4": (140, 140, 130),
            "khaki": (178, 178, 124),
            "khaki1": (255, 244, 142),
            "khaki2": (237, 229, 132),
            "khaki3": (204, 198, 114),
            "khaki4": (140, 135, 79),
            "lavender": (229, 229, 249),
            "lavenderblush": (255, 239, 244),
            "lawngreen": (124, 252, 0),
            "lemonchiffon": (255, 249, 204),
            "lightblue": (175, 226, 255),
            "lightcoral": (239, 127, 127),
            "lightcyan": (224, 255, 255),
            "lightgoldenrod": (237, 221, 130),
            "lightgoldenrodyellow": (249, 249, 209),
            "lightgray": (168, 168, 168),
            "lightgrey": (168, 168, 168),
            "lightpink": (255, 181, 193),
            "lightsalmon": (255, 160, 122),
            "lightseagreen": (33, 178, 170),
            "lightskyblue": (135, 206, 249),
            "lightslateblue": (132, 112, 255),
            "lightslategray": (119, 135, 153),
            "lightslategrey": (119, 135, 153),
            "lightsteelblue": (124, 153, 211),
            "lightyellow": (255, 255, 224),
            "limegreen": (0, 175, 20),
            "linen": (249, 239, 229),
            "magenta": (255, 0, 255),
            "magenta1": (255, 0, 255),
            "magenta2": (237, 0, 237),
            "magenta3": (204, 0, 204),
            "magenta4": (140, 0, 140),
            "maroon": (142, 0, 81),
            "maroon1": (255, 51, 178),
            "maroon2": (237, 48, 165),
            "maroon3": (204, 40, 142),
            "maroon4": (140, 28, 96),
            "mediumaquamarine": (0, 147, 142),
            "mediumblue": (51, 51, 204),
            "mediumforestgreen": (51, 130, 73),
            "mediumgoldenrod": (209, 193, 102),
            "mediumorchid": (188, 81, 188),
            "mediumpurple": (147, 112, 219),
            "mediumseagreen": (51, 119, 102),
            "mediumslateblue": (107, 107, 140),
            "mediumspringgreen": (35, 142, 35),
            "mediumturquoise": (0, 209, 209),
            "mediumvioletred": (214, 33, 119),
            "midnightblue": (45, 45, 99),
            "mintcream": (244, 255, 249),
            "mintty": (191, 191, 191),
            "mistyrose": (255, 226, 224),
            "moccasin": (255, 226, 181),
            "navajowhite": (255, 221, 173),
            "navy": (35, 35, 117),
            "navyblue": (35, 35, 117),
            "oldlace": (252, 244, 229),
            "olivedrab": (107, 142, 35),
            "orange": (255, 135, 0),
            "orange1": (255, 165, 0),
            "orange2": (237, 153, 0),
            "orange3": (204, 132, 0),
            "orange4": (140, 89, 0),
            "orangered": (255, 68, 0),
            "orchid": (239, 132, 239),
            "orchid1": (255, 130, 249),
            "orchid2": (237, 122, 232),
            "orchid3": (204, 104, 201),
            "orchid4": (140, 71, 137),
            "palegoldenrod": (237, 232, 170),
            "palegreen": (114, 221, 119),
            "paleturquoise": (175, 237, 237),
            "palevioletred": (219, 112, 147),
            "papayawhip": (255, 239, 214),
            "peachpuff": (255, 216, 186),
            "peru": (204, 132, 63),
            "pink": (255, 181, 196),
            "pink1": (255, 181, 196),
            "pink2": (237, 168, 183),
            "pink3": (204, 145, 158),
            "pink4": (140, 99, 107),
            "plum": (196, 71, 155),
            "plum1": (255, 186, 255),
            "plum2": (237, 173, 237),
            "plum3": (204, 150, 204),
            "plum4": (140, 102, 140),
            "powderblue": (175, 224, 229),
            "purple": (160, 33, 239),
            "purple1": (155, 48, 255),
            "purple2": (145, 43, 237),
            "purple3": (124, 38, 204),
            "purple4": (84, 25, 140),
            # Note 'red' is commented out, as it's the bright red that
            # I use the name 'lred' for.
            #"red": (255, 0, 0),
            "red1": (255, 0, 0),
            "red2": (237, 0, 0),
            "red3": (204, 0, 0),
            "red4": (140, 0, 0),
            "rosybrown": (188, 142, 142),
            "royalblue": (63, 104, 224),
            "saddlebrown": (140, 68, 17),
            "salmon": (232, 150, 122),
            "salmon1": (255, 140, 104),
            "salmon2": (237, 130, 96),
            "salmon3": (204, 112, 84),
            "salmon4": (140, 76, 56),
            "sandybrown": (244, 163, 96),
            "seagreen": (81, 147, 132),
            "seashell": (255, 244, 237),
            "seashell1": (255, 244, 237),
            "seashell2": (237, 229, 221),
            "seashell3": (204, 196, 191),
            "seashell4": (140, 135, 130),
            "sienna": (150, 81, 45),
            "sienna1": (255, 130, 71),
            "sienna2": (237, 119, 66),
            "sienna3": (204, 104, 56),
            "sienna4": (140, 71, 38),
            "skyblue": (114, 158, 255),
            "slateblue": (124, 135, 170),
            "slategray": (112, 127, 142),
            "slategrey": (112, 127, 142),
            "snow": (255, 249, 249),
            "snow1": (255, 249, 249),
            "snow2": (237, 232, 232),
            "snow3": (204, 201, 201),
            "snow4": (140, 137, 137),
            "springgreen": (63, 170, 63),
            "steelblue": (84, 112, 170),
            "tan": (221, 183, 135),
            "tan1": (255, 165, 79),
            "tan2": (237, 153, 73),
            "tan3": (204, 132, 63),
            "tan4": (140, 89, 43),
            "thistle": (216, 191, 216),
            "thistle1": (255, 224, 255),
            "thistle2": (237, 209, 237),
            "thistle3": (204, 181, 204),
            "thistle4": (140, 122, 140),
            "tomato": (255, 99, 71),
            "tomato1": (255, 99, 71),
            "tomato2": (237, 91, 66),
            "tomato3": (204, 79, 56),
            "tomato4": (140, 53, 38),
            "transparent": (0, 0, 0),
            "turquoise": (25, 204, 221),
            "turquoise1": (0, 244, 255),
            "turquoise2": (0, 229, 237),
            "turquoise3": (0, 196, 204),
            "turquoise4": (0, 135, 140),
            "violet": (155, 61, 206),
            "violetred": (242, 61, 150),
            "wheat": (244, 221, 178),
            "wheat1": (255, 232, 186),
            "wheat2": (237, 216, 173),
            "wheat3": (204, 186, 150),
            "wheat4": (140, 124, 102),
            "white": (255, 255, 255),
            "whitesmoke": (244, 244, 244),
            "yellow": (255, 255, 0),
            "yellow1": (255, 255, 0),
            "yellow2": (237, 237, 0),
            "yellow3": (204, 204, 0),
            "yellow4": (140, 140, 0),
            "yellowgreen": (51, 216, 56),
        }
        class CN24:
            '''Encapsulate 24-bit color names.  The default set is the following
            set of color names, functional on most terminals:
                blk,  blu,  grn,  cyn,  red,  mag,  yel,  wht
                lblk, lblu, lgrn, lcyn, lred, lmag, lyel, lwht
            '''
            def __init__(self, full=False):
                a, b = 255, 255//2
                self.d = {
                    "blk": (0, 0, 0),
                    # Bright colors
                    "lblk": (b//2, b//2, b//2),     # A dark gray
                    "lblu": (0, 0, a),
                    "lgrn": (0, a, 0),
                    "lcyn": (0, a, a),
                    "lmag": (a, 0, a),
                    "lred": (a, 0, 0),
                    "lyel": (a, a, 0),
                    "lwht": (a, a, a),
                    # Normal dim colors
                    "blu": (0, 0, b),
                    "cyn": (0, b, b),
                    "grn": (0, b, 0),
                    "mag": (b, 0, b),
                    "red": (b, 0, 0),
                    "yel": (b, b, 0),
                    "wht": (b, b, b),
                    # Special to match my mintty terminal's normal color
                    "mintty": (191, 191, 191),
                }
                if full:
                    self.d.update(xw)   # Use XWindows RGB color names
                self._default()
            def _default(self):
                'Set self.n to the default color'
                a = "\033[0m"   # Normal text attribute
                self.n = a + self.fg("mintty") + self.bg("blk")
            def _check(self, name):
                msg = f"'{name}' is an unrecognized color"
                if name not in self.d:
                    raise ValueError(msg)
            def _parse_color(self, name):
                "Handle the '#xxxxxx' form"
                e = ValueError(f"'{name}' is not a proper color string")
                def f(x):
                    a = int("0x" + x, 16)
                    if not 0 <= a <= 255:
                        raise e
                    return a
                if not ii(name, str) or len(name) != 7:
                    raise e
                try:
                    r, g, b = f(name[1:3]), f(name[3:5]), f(name[5:])
                    return (r, g, b)
                except Exception:
                    raise e
            def fg(self, s):
                'Return the ANSI escape sequence for a foreground color'
                if s is None or not s:
                    return ""
                if s.startswith("#"):
                    rgb = self._parse_color(s)
                else:
                    self._check(s)
                    rgb = self.d[s]
                return "\033[38;2;{};{};{}m".format(*rgb)
            def bg(self, s):
                'Return the ANSI escape sequence for a background color'
                if s is None or not s:
                    return ""
                if s.startswith("#"):
                    rgb = self._parse_color(s)
                else:
                    self._check(s)
                    rgb = self.d[s]
                return "\033[48;2;{};{};{}m".format(*rgb)
if 1:   # Utility
    def GetTerm(choice=None):
        'Modify this code to handle your terminal'
        term = os.environ.get("TERM", "")
        termpgm = os.environ.get("TERM_PROGRAM", "")
        #pgmver = os.environ.get("TERM_PROGRAM_VERSION", "")
        #
        if not choice:
            if term == "xterm" and termpgm == "mintty":
                return "24-bit"
            elif term == "xterm-256color" and termpgm == "Apple-Terminal":
                return "8-bit"
            else:
                return "4-bit"
        else:
            if choice not in "4-bit 8-bit 24-bit".split():
                raise ValueError("choice must be 4bit, 8bit, or 24bit")
            return choice
if 1:   # Text attributes
    # This dictionary is used to translate text attribute strings to the
    # escape code's number.  See the table at
    # https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
    ta = {  # Translate text attribute to escape code's parameter
        "normal"          : 0,
        "no"              : 0,
        "bold"            : 1,
        "bo"              : 1,
        "dim"             : 2,
        "di"              : 2,
        "italic"          : 3,
        "it"              : 3,
        "underline"       : 4,
        "ul"              : 4,
        "blink"           : 5,
        "bl"              : 5,
        "rapidblink"      : 6,
        "rb"              : 6,
        "reverse"         : 7,
        "rv"              : 7,
        "hide"            : 8,
        "hi"              : 8,
        "strikeout"       : 9,
        "so"              : 9,
        "doubleunderline" : 21,
        "du"              : 21,
        "overline"        : 53,
        "ol"              : 53,
        "superscript"     : 73,
        "sp"              : 73,
        "subscript"       : 74,
        "sb"              : 74,
    }
if 1:   # Classes
    class Clr:
        '''For typical use, instantiate with c = Clr().  Store "styles" by using
        the Clr instance's attributes:
            c.err = c("red")      # Error messages are red
        Use the styles in f-strings:
            print(f"{c.err}Error:  symbol doesn't exist{c.n}")
        c.err and c.n are strings containing the ANSI  escape codes (c.n is the
        escape code for the standard terminal text).  The previous can be a
        little more terse with the equivalent:
            c.print(f"{c.err}Error:  symbol doesn't exist")
        c.print() and c.out() output their strings then output the escape
        code to return to the normal style.  To remove all your "style"
        definitions, use c.reset().  To see the styles you've defined, use
        print(c).
        '''
        def __init__(self, bits=None, override=False):
            '''If override is True, always emit escape codes.  The normal
            behavior is not to emit escape codes unless stdout is a terminal.
            bits must be None, 4, 8, or 24.  If None, the model is chosen
            from the TERM and TERM_PROGRAM environment variables.
            '''
            self._override = bool(override)
            # Find the terminal type
            if bits is None:
                terminal = GetTerm(choice=choice)
                if terminal == "4-bit":
                    self._bits = 4
                elif terminal == "8-bit":
                    self._bits = 8
                else:
                    self._bits = 24
            else:
                self._bits = bits
            self.reset()
        def _user(self):
            'Return a set of user-defined attribute names'
            ignore = set('''_bits _cn _on _override _parse_color _user load n
                out print reset'''.split())
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
        def __call__(self, fg=None, bg=None, attr=None):
            '''Return the indicated color style escape code string.  attr
            is a string of attributes (separate multiple attributes by
            spaces).  fg and bg are strings like "red" or "#abcdef" for
            24-bit terminals, numbers on [0, 255] for 8-bit terminals, and
            short color names like "blk", "red", etc. for 4-bit terminals.
            '''
            if TERM == "8-bit":
                assert(fg is None or ii(fg, int))
                assert(bg is None or ii(bg, int) or bg is None)
            else:
                assert(fg is None or ii(fg, str))
                assert(bg is None or ii(bg, str))
            assert(attr is None or ii(attr, str))
            a = ""
            container = []
            if attr is not None:
                attrs = attr.split()
                while attrs:
                    a = attrs.pop(0)
                    if a not in ta:
                        msg = f"'{a}' is not a valid attribute"
                        raise ValueError(msg)
                    container.append(f"\033[{ta[a]}m")
            f = "" if fg is None else self._cn.fg(fg)
            b = "" if bg is None else self._cn.bg(bg)
            return f + b + ''.join(container)
        # ----------------------------------------------------------------------
        # User interface
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
                print(f"Clr.load() from {t}: ", self)
        def reset(self):
            'Sets the instance to a default state'
            # Delete all user-set attributes
            for i in self._user():
                delattr(self, i)
            # Define the basic attributes
            #
            # Get color info for color names
            if self._bits == 4:
                self._cn = CN4(full=True)
            elif self._bits == 8:
                self._cn = CN8(full=True)
            elif self._bits == 24:
                self._cn = CN24(full=True)
            else:
                raise Exception(f"'{self._bits}' is an illegal number of bits")
            # Reset to default color
            self.n = self._cn.n
            # Turn on output unless not to terminal
            self._on = True
            if not sys.stdout.isatty() and not self._override:
                self._on = False
        def print(self, *p, **kw):
            '''Print arguments with newline, reverting to normal color
            after finishing.
            '''
            self.out(*p, **kw)
            print()
        def out(self, *p, **kw):
            'Same as print() but no newline'
            k = kw.copy()
            if "end" not in k:
                k["end"] = ""
            print(*p, **k)
            print(self.n, **k)
if 1:   # Choose color name class for your terminal
    # Set choice to force the class to use
    choice = None
    if 0:
        choice = "4-bit" if 0 else "8-bit" if 0 else "24-bit"
    TERM = GetTerm(choice=choice)
    if TERM == "4-bit":
        CN = CN4
    elif TERM == "8-bit":
        CN = CN8
    else:
        CN = CN24
if 1:   # Printing regular expression matches
    def PrintMatch(text, regexp, style=None, file=sys.stdout, clr=Clr()):
        '''Decorate regexp matches in the string text with the indicated
        style (defaults to reversed if None) and print to the indicated
        stream.  If you wish to override the default style used when style
        is None, set PrintMatch.c to the desired escape sequence.  To see
        matched whitespace characters more easily, you may want to use 
        'reverse' as a style attribute.
        '''
        c = clr
        if isinstance(regexp, str):     # Convert it to a regexp
            # Need to escape magic characters
            magic = set("*+^$.?{}[]|()")
            t, q = deque(regexp), deque()
            while t:
                u = t.popleft()
                q.append("\\" + u if u in magic else u)
            r = re.compile(''.join(q)) 
        else:
            r = regexp
        mo = r.search(text)
        if style is None:
            if hasattr(PrintMatch, "style"):
                style = PrintMatch.style
            else:
                style = c(attr="reverse")
        if not mo:
            # No match, so just print text
            print(text, file=file)
            return
        text = mo.string
        P = partial(print, end="", file=file)
        while text:
            # Print non-matching starting portion.  Assumes the current
            # style is the default.
            s = text[:mo.start()]
            print(s, end="", file=file)
            # Print the match in the indicated style
            s = text[mo.start():mo.end()]
            c.out(f"{style}{s}", file=file)
            # Use the remaining substring
            text = text[mo.end():]
            mo = r.search(text)
            if not mo:
                print(text)
                return
    def PrintMatches(text, regexps, file=sys.stdout, clr=Clr()):
        '''Given a string text, search for regular expression matches
        given in the sequence of regexps, which contain pairs of regular
        expressions and Style objects, then print the text to stdout with
        the indicated styles.
        '''
        def out(s):
            print(s, end="")
        def GetShortestMatch(text):
            '''Return (start, end, style) of the earliest match or (None, None,
            None) if there were no matches.
            '''
            matches = []
            for r, style in regexps:
                mo = r.search(text)
                if mo:
                    matches.append([mo.start(), mo.end(), style])
            return sorted(matches)[0] if matches else (None, None, None)
        c = clr
        while text:
            start, end, style = GetShortestMatch(text)
            if start is None:
                # No matches, so print remainder
                c.out(text, file=file)
                return
            # Print non-matching start text
            c.out(f"{c.n}{text[:start]}", file=file)
            # Print match in chosen style
            c.out(f"{style}{text[start:end]}")    
            text = text[end:]       # Use the remaining substring
            if not text:
                print(file=file)    # Print a newline

if __name__ == "__main__":
    # Demonstrate module's output
    c = Clr(override=True)
    c.hdr = c("orchid", attr="rv")
    width = int(os.environ["COLUMNS"])
    def TestCases():
        # Not exhaustive, but will test some key features.  Tested only
        # under mintty 3.5.2.
        c.m = c("violetred")    # Test case headings
        def TestLoad():
            'Test Clr.load() from file, stream and string'
            c.print(f"{c.m}Test of Clr.load()")
            s = "/tmp/tmp.clr.py"
            f = P(s)
            open(P(s), "w").write("err lred None\n")
            x = Clr(override=True)
            x.load(f, show=True)            # File
            x.load(open(f), show=True)      # Stream
            s = "err lred None"
            x.load(s, show=True)            # String
            f.unlink()
        def TestRegexpDecorate():
            x = Clr()
            x.of = x("blk", "lgrn")
            x.man = x("lyel", attr="rv rb")
            x.so = x("lred", "lblu")
            x.Is = x(None, None, attr="ul ol")
            c.print(dedent(f'''
                {c.m}Test of regular expression decoration
                    'of' should be {x.of}of{x.n}{c.m}.
                    'man' should be {x.man}man{x.n}{c.m}.
                    'so' should be {x.so}so{x.n}{c.m}.
                    'is' should be lined as {x.Is}is{x.n}{c.m}.
            '''))
            t = dedent('''
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
            PrintMatches(t, r)
        TestLoad()
        TestRegexpDecorate()
    def ColorTable():
        def H(bright=False):
            c.out(f"{'':{w}s} ")
            for i in T:
                if bright:
                    c.out(f"{c('lwht')}{'l' + i:{w}s}{c.n} ")
                else:
                    c.out(f"{c('wht')}{i:{w}s}{c.n} ")
            print()
        def Tbl(msg, fg=False, bg=False, last=True):
            print(f"{c('lyel')}{msg:^{W}s}{c.n}")
            H("l" if bg else "")
            for i in T:
                if fg:
                    i = "l" + i 
                    c.out(f"{c('lwht')}{i:{w}s}{c.n} ")
                else:
                    c.out(f"{c('wht')}{i:{w}s}{c.n} ")
                for j in T:
                    j = "l" + j if bg else j
                    c.out(f"{c(i, j)}{t}{c.n} ")
                print()
            if last:
                print()
        T = "blk  blu grn  cyn  red  mag  yel  wht".split()
        w, t = 4, "text"
        W = 44
        print(f"{TERM} terminal")
        if TERM == "24-bit":
            Tbl("Dim text, dim background", False, False)
            Tbl("Bright text, dim background", True, False)
            Tbl("Dim text, bright background", False, True)
            Tbl("Bright text, bright background", True, True, last=False)
            c.out(c.n)
        elif TERM == "4-bit":
            Tbl("Dim text", False, False)
            Tbl("Bright text", True, False, last=False)
        elif TERM == "8-bit":
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
        - theme example with Clr.load()
        - regexp matches
        - Unicode in sub/superscripts (e.g., Hz**(1/2)
        '''
        def Header():
            c.print(dedent(f'''
            {c.hdr}Demonstration of some clr.py features{c.n}
 
            '''))
        def Theme():
            x = Clr()
            s = "This {ul}truth{n} is well-{em}fixed{n} in our minds."
            x.print(dedent(f'''
                {c.hdr}Themes{x.n}
                This example shows how standardizing some style names can be used to change
                "themes" with the Clr.load() method.  We'll use the style names 'em' and
                'ul'. The sentence is "{s}"
                The older string interpolation method of str.format() is used so that the
                single instance of the string can be used (normally, I like to use f-strings
                because of the brevity).
 
                The first "theme" will use underlining for the ul style and 'lyel' text for
                the em style:
            '''))
            # Load the first theme
            theme1 = dedent('''
                ul None None ul
                em lyel None
            ''')
            x.load(theme1)
            d = {"ul": x.ul, "em": x.em, "n": x.n}
            x.print("\n    First  style: ", s.format(**d))
            # Load the second theme
            x.print(dedent(f'''
 
                The second "theme" will use reversed 'lyel' text for the ul style and 
                italics for the em style:
            '''))
            theme2 = dedent('''
                ul lyel None rv
                em None None it
            ''')
            x.load(theme2)
            d = {"ul": x.ul, "em": x.em, "n": x.n}
            x.print("\n    Second style: ", s.format(**d))
        def Exponents():
            n = c.n
            e = c("lyel")
            u = c("lyel", attr="sp")
            b = c("lyel", attr="sb")
            c.print(dedent(f'''
 
                {c.hdr}Exponents{c.n}
                The mintty terminal can display exponents and subscripts, even using Unicode
                characters.
 
                    SI units: kg/(m·s²)
                        With built-in Unicode:      {e}ξ{b}λ{n}{e} = 3 kg·m⁻¹·s⁻²{c.n}
                        With superscripts:          {e}ξ{b}λ{n}{e} = 3 kg·m{u}-1{c.n}{e}·s{u}-2{c.n}
                        (Unicode looks better, but Unicode doesn't support 'obvious' exponent
                        characters.  Here's an example with mintty:
                                                    {e}ξ{b}λ{n}{e} = 3 kg·m{u}θ{c.n}{e}·s{u}μ²{c.n}
            '''))
        def TextEditing():
            n, a, d = c.n, c("lgrn"), c(None, None, attr="so")
            c.print(dedent(f'''
 
                {c.hdr}Text editing{c.n}
                Using a green color for added text and strikethrough for deleted text, you can
                show how some text has been edited:
        
                    This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
            '''))
            d = c("lred", attr="so")
            c.print(dedent(f'''
 
                The strikethrough text can be hard to see.  A quick change adds a red color:
 
                    This {a}new{n} {d}old{n} text was {a}added{n} {d}deleted{n}.
            '''))
        Header()
        Theme()
        Exponents()
        TextEditing()
    def Attributes():
        def f(a):
            return c("wht", attr=a)
        print(dedent(f'''
        Text attributes ('hide' is to the right of 'dim')
          {f("no")}normal      no{c.n}       {f("bo")}bold        bo{c.n}
          {f("it")}italic      it{c.n}       {f("ul")}underline   ul{c.n}
          {f("bl")}blink       bl{c.n}       {f("rb")}rapidblink  rb{c.n}
          {f("rv")}reverse     rv{c.n}       {f("so")}strikeout     so{c.n}
          {f("di")}dim         di{c.n}       {f("hi")}hide         hi{c.n}
          sub{f("sb")}script   {c.n}sb       super{f("sp")}script  {c.n}sp
        '''.rstrip()))
    def Help():
        if TERM != "24-bit":
            return
        print(dedent(f'''
 
            Include one or more arguments to see other tables/demos:
                all         All colors
                attr        Attributes
                test        Run some self-tests
                ex          Examples
        '''))
    def ShowAllColors():
        for name in c._cn.d:
            escseq = c(name)
            c.out(f"{escseq}{name} ")
        print()
    args = sys.argv[1:]
    if args and TERM == "24-bit":
        if "attr" in args:
            Attributes()
        if "all" in args:
            ShowAllColors()
        if "test" in args:
            TestCases()
        if "ex" in args:
            Examples()
    else:
        ColorTable()
        Help()
# vim: tw=75
