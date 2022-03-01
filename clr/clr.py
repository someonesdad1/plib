'''
 
TODO
    - Features needing implementation
        - Demo:  print all colors
        - Demo:  print a demo page showing numerous mintty features
        - Demo:  changing 'themes'
        - Support 4, 8, and 24 bit environments
            - Look at 'set|grep TERM' to choose setup
                - TERM=xterm
                - TERM_PROGRAM=mintty
                - TERM_PROGRAM_VERSION=3.5.2
            - xterms are typically 8-bit color
            - 4-bit (old DOS type)
            - less manpage references
              https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_parameters and
              https://docs.microsoft.com/en-us/windows/console/char-info-str
                - Note less doesn't handle 24-bit sequences
        - Finish instructions on how to set it up for a user's terminal
 
This module is an aid for color printing in a terminal.  
    Design goals
        - Colors are defined by strings such as "red" and "#abcdef"
        - Terse syntax so things fit into f-strings
            - Short names for most-used colors
        - Simple for common use cases
        - Easy to add new colors
        - Support the terminals I use: mintty, Mac, xterm
        - Support the styles use case
        - Allow color decoration of regular expression matches
        - Class derivation should allow support of 4, 8, and 24 bit color
          terminals
        - On/off control for when output stream isn't a terminal
            - Can also be controlled by an environment variable
        - Convenience functions
            - Print a string in a color, no newline, then return to the
              default color
            - Print a string in a color, with newline, then return to the
              default color
            - Use print()'s semantics
        - Support idea of themes for a particular look
 
    Overview
 
        This module produces ANSI escape code strings to produce colors in
        output to terminals.  If you're unfamiliar with such things, see
        https://en.wikipedia.org/wiki/ANSI_escape_code.
 
        The primary component is the Clr object.  The basic colors use 3-letter
        abbreviations: blk for black, blu for blue, grn for green, cyn for
        cyan, mag for magenta, yel for yellow, and wht for wht.  An 'l' is
        prepended to the name to get the bright form of that color.
 
        The basic use case of the module is
 
            c = Clr()                   # Get an instance of the Clr class
            # Error messages are bright white text on a red background
            err = c("lwht", "red")
            print(f"'{err}xyzzy{c.n}' is an unsupported keyword")
 
        You'll see the word xyzzy in bright white text on a red background on
        your terminal.  The c.n attribute of the Clr instance is an escape code
        to return to the normal terminal color.
 
        Instead of using variables like 'err' above, you can add instance
        attributes to the c instance
 
            c.err = c("red")
 
        All the functionality is in the Clr.__call__ method, which returns
        either an ANSI escape sequence or the empty string:
 
            def __call__(self, fg, bg=None, attr=None):
 
        fg and bg are strings denoting the foreground and background colors.
        attr is an enum describing the text attributes you wish.  The TA class
        defines these attributes.  For example, setting attr to TA.italic
        causes the text to be italic.
 
        Other tidbits:
            - c.on(False) causes all subsequent function calls and attributes
              to return emtpy strings.  The use case for this is when the
              output is not going to a terminal (e.g., sys.stdout.isatty() is
              False).  Use c.on(True) to turn things on when desired.
            - c.out and c.print are convenience functions to provide colorized
              strings and revert to the normal color after they finish.  They
              both support print() semantics.
            - c.reset() removes all Clr instance attributes except for n.  This
              lets you e.g. define a new set of styles as instance attributes.
 
    Instructions to use this module
 
        - Set it up for your terminal
        - Set the Clr.n instance attribute to your normal color choices
 
        I have used this module with 1) mintty running under cygwin on a
        Windows 10 box and 2) on a Mac using Apple's terminal program.  This
        module will determine these two environments by using the TERM and
        TERM_PROGRAM environment variables.  If you're using different
        terminals, you'll have to modify the code to support your terminal.
 
Other stuff
    Regexp for ANSI escape sequences:
        https://stackoverflow.com/questions/41708623/regular-expression-for-
            separating-ansi-escape-characters-from-text#41709303
        split_ANSI_escape_sequences = re.compile(r"""
            (?P<col>(\x1b     # literal ESC
            \[       # literal [
            [;\d]*   # zero or more digits or semicolons
            [A-Za-z] # a letter
            )*)
            (?P<name>.*)
            """, re.VERBOSE).match
        def split_ANSI(s):
            return split_ANSI_escape_sequences(s).groupdict()
    Other python terminal coloring libraries
        - Colorama (PyPI)
            - import colorama
            - from colorama import Fore
            - print(Fore.RED + 'This text is red in color')
        - termcolor (PyPI)
            - from termcolor import colored
            - text = colored('Hello, World!', 'red', attrs=['reverse', 'blink'])
            - print(text)
        - colored (PyPI) https://pypi.org/project/colored/
            - Attributes:  bold, dim, underlined, blink, reverse, hidden
            - Colors:  256, with typical X-windows names
            - Understandable syntax:
                - print(fore.LIGHT_BLUE + back.RED + style.BOLD + "Hello World")
            - Composition method:
                - color = bg("indian_red_1a") + fg("white")
                - reset = attr("reset")
                - print(color + "Hello" + reset)
                - bg and fg are probably just dictionary lookups
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
    # Provides the Clr object for ANSI escape sequences to get colored text in
    # terminal applications.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    import os
    import pathlib
    import sys
    from enum import Enum, auto
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
if 1:   # Names of colors
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
    class CN:
        '''Encapsulate color names.  The default set is the following set of
        color names, functional on most terminals:
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
        def fg(self, s):
            'Return the ANSI escape sequence for a foreground color'
            if s is None or not s:
                return ""
            self._check(s)
            return "\033[38;2;{};{};{}m".format(*self.d[s])
        def bg(self, s):
            'Return the ANSI escape sequence for a foreground color'
            if s is None or not s:
                return ""
            self._check(s)
            return "\033[48;2;{};{};{}m".format(*self.d[s])
if 1:   # Class definitions
    class TA(Enum):
        'Text attributes'
        normal          = auto()
        bold            = auto()
        italic          = auto()
        underline       = auto()
        doubleunderline = auto()
        overline        = auto()
        blink           = auto()
        rapidblink      = auto()
        reverse         = auto()
        strikeout       = auto()
        dim             = auto()
        hide            = auto()
        subscript       = auto()
        superscript     = auto()
        # Short aliases
        no  = auto()    # normal
        bo  = auto()    # bold
        it  = auto()    # italic
        ul  = auto()    # underline
        dul = auto()    # doubleunderline
        ol  = auto()    # overline
        bl  = auto()    # blink
        rb  = auto()    # rapidblink
        rev = auto()    # reverse
        so  = auto()    # strikeout
        di  = auto()    # dim
        hi  = auto()    # hide
        sub = auto()    # subscript
        sup = auto()    # superscript
    class AD:
        'Attribute decoding'
        def __init__(self):
            self.ta = {  # Translate text attribute to escape code's parameter
                TA.normal          : 0,
                TA.bold            : 1,
                TA.dim             : 2,
                TA.italic          : 3,
                TA.underline       : 4,
                TA.blink           : 5,
                TA.rapidblink      : 6,
                TA.reverse         : 7,
                TA.hide            : 8,
                TA.strikeout       : 9,
                TA.doubleunderline : 21,
                TA.overline        : 53,
                TA.superscript     : 73,
                TA.subscript       : 74,
            }
            # Short aliases
            self.ta[TA.no]  = self.ta[TA.normal]
            self.ta[TA.bo]  = self.ta[TA.bold]
            self.ta[TA.di]  = self.ta[TA.dim]
            self.ta[TA.it]  = self.ta[TA.italic]
            self.ta[TA.ul]  = self.ta[TA.underline]
            self.ta[TA.bl]  = self.ta[TA.blink]
            self.ta[TA.rb]  = self.ta[TA.rapidblink]
            self.ta[TA.rev] = self.ta[TA.reverse]
            self.ta[TA.hi]  = self.ta[TA.hide]
            self.ta[TA.so]  = self.ta[TA.strikeout]
            self.ta[TA.dul] = self.ta[TA.doubleunderline]
            self.ta[TA.ol]  = self.ta[TA.overline]
            self.ta[TA.sup] = self.ta[TA.superscript]
            self.ta[TA.sub] = self.ta[TA.subscript]
    class Clr:
        '''For typical use, instantiate by c = Clr().  Store "styles" by using
        the Clr instance's attributes:
            c.err = c("red")      # Error messages are red
        Use the styles in f-strings:
            print(f"{c.err}Error:  symbol doesn't exist{c.n}")
        where c.n is the escape code for the standard terminal text.  The
        previous can be a little more terse with the equivalent:
            c.print(f"{c.err}Error:  symbol doesn't exist")
        To remove all your "style" definitions, use c.reset().  To see the
        styles you've defined, use print(c).
        '''
        def __init__(self, override=False):
            '''If override is True, always emit escape codes.  The normal
            behavior is not to emit escape codes if stdout is not a terminal.
            '''
            self._override = override
            self.reset()
        def _user(self):
            'Return a set of user-defined attribute names'
            ignore = set("n reset on out print _override _user _cn _st".split())
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
        def __call__(self, fg, bg=None, attr=None):
            '''Return the indicated color style escape code string.  attr must
            be an enum of type TA.
            '''
            assert(ii(fg, str))
            assert(ii(fg, str) or bg is None)
            assert(attr is None or ii(attr, TA))
            a = ""
            if attr is not None:
                if attr not in self._st:
                    msg = f"'{attr}' is not a valid attribute"
                    raise ValueError(msg)
                a = f"\033[{self._st[attr]}m"
            f = self._cn.fg(fg)
            b = self._cn.bg(bg)
            return a + f + b
        # ----------------------------------------------------------------------
        # User interface
        def reset(self):
            'Sets the instance to a default state'
            # Delete all user-set attributes
            for i in self._user():
                delattr(self, i)
            # Define the basic attributes
            self._cn = CN(full=True)    # Get color info for color names
            # Reset to default color
            self.n = self._cn.n
            # dict to translate TA enums to escape code numbers
            self._st = AD().ta 
            # Turn on output unless not to terminal
            self.on = True
            if not sys.stdout.isatty() and not self._override:
                self.on = False
        def out(self, *p, **kw):
            '''Print arguments with no newline, then revert to normal
            color.
            '''
            k = kw.copy()
            if "end" not in k:
                k["end"] = ""
            print(*p, **k)
            print(self.n, **k)
        def print(self, *p, **kw):
            '''Print arguments with newline, reverting to normal color
            after finishing.
            '''
            self.out(*p, **kw)
            print()
 
if 0:
    # Get attributes working
    c = Clr()
    c.err = c("lred")
    c.nor = c("lgrn")
    print(f"{c.err}c.err is set{c.n}")
    c.print(f"{c.nor}c.nor is set")
    print("User attr:", c._user())
    print(c)
    c.reset()
    print(c)
    exit()
if 0:
    # Print out examples of the base theme colors
    c = Clr()
    for i in '''blk  blu grn  cyn  red  mag  yel  wht
                lblk lblu lgrn lcyn lred lmag lyel lwht'''.split():
        print(f"{c('blk', i)}{i}{c.n}")
    c.out(f"{c.n}")
    exit()
if __name__ == "__main__":
    # Demonstrate module's output
    def ColorTable():
        c = Clr()
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
        Tbl("Dim text, dim background", False, False)
        Tbl("Bright text, dim background", True, False)
        Tbl("Dim text, bright background", False, True)
        Tbl("Bright text, bright background", True, True, last=False)
        c.out(c.n)
    def Attributes():
        def f(a):
            return c("mintty", attr=a)
        print(dedent(f'''
        Text attributes ('hide' is to the right of 'dim')
          {f(TA.no)}normal      no{c.n}       {f(TA.bo)}bold        bo{c.n}
          {f(TA.it)}italic      it{c.n}       {f(TA.ul)}underline   ul{c.n}
          {f(TA.bl)}blink       bl{c.n}       {f(TA.rb)}rapidblink  rb{c.n}
          {f(TA.rev)}reverse     rev{c.n}      {f(TA.so)}strikeout     so{c.n}
          {f(TA.dim)}dim         dim{c.n}     {f(TA.hi)}hide         hi{c.n}
          sub{f(TA.sub)}script   {c.n}sub     super{f(TA.sup)}script  {c.n}sup
        '''.rstrip()))
    def Help():
        print(dedent(f'''
 
            Include one or more arguments to see other tables:
                all         All colors
                attr        Attributes
        '''))
    def ShowAllColors():
        c = Clr()
        for name in c._cn.d:
            escseq = c(name)
            c.out(f"{escseq}{name} ")
        print()

    args = sys.argv[1:]
    if args:
        if "attr" in args:
            Attributes()
        if "all" in args:
            ShowAllColors()
    else:
        ColorTable()
        Help()
