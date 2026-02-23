'''

t = Trm()

ToDo
    - https://runebook.dev/en/docs/python/library/collections/collections.UserDict
      explains why collections.UserDict might be a better choice:  dict.update() might
      ignore your __setitem__.  This means if I stick with Trm(dict), then every dict
      method I use has to be defined in the class to ensure it works.  Unfortunately,
      python's documentation doesn't discuss this.
    - Start writing selftests
    - Get .always working
    - t(x) returns the escape code for x
    - Working
        - .on works
        - Init with a variety of color specifications

Vision
    - Change Trm to a dict, letting it be a tool to convert names to escape sequences to
      get color output in a terminal.  Let t = Trm()
        - t.n is the same as t["n"]
        - Core attributes that are not color name to escape codes
            - t.on      Boolean to decide whether t[x] provides escape code or ""
            - t.always  If true, output even if stdout.isatty() is False
        - ppush() and ppop() methods for new dict names
        - Supports context manager pattern for temporarily changing styles

    - Initialization:  
        - See xstylesx for some tests cases below
            - All of these should be handled by the Color() constructor
        - The dict is initialized with f"t.{name}" = X where X is
            - "xxx"   Most typical, a short name
            - Color(...)
            - "#aabbcc"
            - "60 60 60" or (60,60,60)
            - 0xff or "0xff"    8-bit integer
            - 3.473     float, uses math.modf(x)[0] --> [0, 1] for a gray
            - "555 nm"  Wavelength between 400 and 700 nm
        - After these strings are set, the resolve() method is called to turn all the
          values into escape strings

    - class Trm(dict):  let t be an instance
        - Generates terminal escape codes
        - t.sky = t["sky"] and this returns the escape code
        - Defining colors 
            - t.sky = Color(...)            # Uses Color instance
            - t.sky = "#aabbcc"             # Uses Color(arg)
            - t.sky = "60 60 60"            # String form of Tuple of integers
            - t.sky = (60,60,60)            # Tuple of integers
            - t.sky = x:int                 # 8-bit color abs(int(x)) mod 256
            - t.sky = "0xff"                # Converted to int to get 8-bit color
            - t.sky = x:float               # math.modf(x)[0] --> [0, 1] for a gray
        - Uses external class to do the 4, 8, or 24 bit color conversions?  Or, use
          multiple inheritance to use a ColorBit class that is initialized with 4, 8, or
          24 bits
        - t.on = bool turns the output of escape codes on and off
        - t.always = bool If True, outputs even if stdout doesn't appear to be a
          terminal (sys.stdout.isatty() == False)
'''
if 1:   # Standard imports
    import collections
    import decimal
    import fractions
    import math
    import sys
    Decimal = decimal.Decimal
    Fraction = fractions.Fraction
if 1:   # Custom imports
    import color
    import dpcolornames
    import dpmath
    import dpprint
    import stack
    import wl2rgb
    Color = color.Color
    t = color.t
    Stack = stack.Stack
    PP = dpprint.PP
    pp = PP()   # Get pprint with current screen width
if 1:
    import debug
    debug.SetDebugger()

class Trm(dict):
    '''Dictionary used to output escape codes to a terminal.

    '''
    def __init__(self, names_dict):
        '''Call with a dictionary relating a name string to something that will be
        recognized by the color.Color constructor.
        '''
        # Attributes with underscores are not meant to be accessed by the user
        self._stack = Stack()   # Saves previous states of self
        self.on = True          # Output escape codes if True
        self.always = False     # If True, output escape codes even if stdout out isn't a terminal
        self._newstyles = None  # Used for context manager behavior
        # Convert the items in names_dict to escape codes and add them to our mapping
        for i in names_dict:
            self[i] = names_dict[i]
    def _get_escape_code(self, color, bg=False):
        'Return escape code for the Color instance color'
        # Assumes 24-bit color
        if color is None or (isinstance(color, str) and color == ""):
            return ""
        assert isinstance(color, Color)
        n = 48 if bg else 38
        if color.bpc < 8:
            raise ValueError(f"{__file__}:Trm:_get_escape_code:  must have 8 bits per color")
        elif color.bpc > 8:
            color = color.change_bpc(8)
        r, g, b = color.irgb
        return f"\x1b[{n};2;{r};{g};{b}m"
    def __call__(self, fg=None, bg=None, attr=None):
        '''Return the indicated color style escape code string.  
        fg and bg can be
            - Color instance
            - Color name that can be found in data/dpcolornames.py
        attr is a string
            - Separate multiple attributs by spaces
            - Typical:  'no' for normal, 'bo' for bold, 'it' for italic, etc.
        '''
        ok = (str, Color)
        msg = "{} must be None, a string, or a Color instance"
        if fg is not None and not isinstance(fg, ok):
            s = msg.format("fg") + f":\n    It's {fg!r}" 
            raise ValueError(s)
        if bg is not None and not isinstance(bg, ok):
            s = msg.format("bg") + f":\n    It's {bg!r}" 
            raise ValueError(s)
        if attr is not None and not isinstance(attr, str):
            s = f"attr must be a string:\n    It's {attr!r}" 
            raise ValueError(s)
        if not self.on or all(i is None for i in (fg, bg, attr)):
            return ""
        '''
        Primer on ANSI escape sequences
        https://en.wikipedia.org/wiki/ANSI_escape_code#SGR_(Select_Graphic_Rendition)_parameters
        gives information on attributes and the section below that discusses colors.
    
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
        # Convert to a Color instance
        if fg and isinstance(fg, ok):
            fg = Color(fg)
        if bg and isinstance(bg, ok):
            bg = Color(bg)
        # Construct the needed escape codes
        out = []
        out.append(self._get_escape_code(fg))
        out.append(self._get_escape_code(bg, bg=True))
        if attr is not None:    # Get attribute codes
            # See the table at
            # https://en.wikipedia.org/wiki/ANSI_escape_code#Select_Graphic_Rendition_parameters
            k1 = '''normal bold dim italic underline blink rapidblink reverse hide
                    strikeout doubleunderline overline superscript subscript'''.split()
            k2 = "no bo di it ul bl rb rv hi so du ol sp sb".split()
            v = (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 21, 53, 73, 74)
            assert len(k1) == len(k2) == len(v)
            di = dict(zip(k1, v))
            di.update(dict(zip(k2, v)))
            for a in attr.split():
                if a not in di:
                    raise ValueError(f"{a!r} is not a valid attribute")
                out.append(f"\x1b[{am[a]}m")
        return ''.join(out)
    def __setitem__(self, name, value):
        if name == "on":
            self.on = value
        elif name == "always":
            self.always = value
        elif name == "_newstyles":  # Used for context manager behavior
            self._newstyles = value
        elif name == "_stack":
            self._stack = value
        else:
            # value can be a single argument or a sequence of 1 to 3 arguments.  They 
            # will be used with the __call__ method
            if isinstance(value, (tuple, list)):
                if len(value) in (1, 2, 3):
                    escape_code = self(*value)
                else:
                    raise ValueError("value sequence must have 1 to 3 components")
            else:
                escape_code = self(value)
            assert isinstance(escape_code, str) and escape_code[0] == "\x1b"
            super().__setitem__(name, escape_code)
    def __getitem__(self, name):
        'This is used to get self[name]'
        # If self.on isn't True, always return an empty string
        if not self.on:
            return ""
        # If self.always is False and stdout isn't a tty, return ""
        if not self.always and not sys.stdout.isatty():
            return ""
        # Otherwise, return the escape sequence
        return super().__getitem__(name)
    def __getattribute__(self, name):
        '''This allows you to access a dictionary key using the syntax self.key
        instead of self[key].  This is a useful shorthand for the Trm instance.
        It also lets us get to our other attributes that are not in the dict without
        infinite recursion.
        '''
        if name in self:
            return super().__getitem__(name)
        else:
            return super().__getattribute__(name)
    def ppush(self, styles_dict):
        '''The styles dict must be a dict instance.  Update our values with
        styles_dict's values after saving a copy of ourself on the stack.
        '''
        if not isinstance(styles_dict, dict):
            raise TypeError("styles_dict must be a dict instance")
        self._stack.push(self.copy())
        self.update(styles_dict)
    def ppop(self):
        '''Get a copy of ourself, then clear ourself and set our state to that of the
        top of the stack; return our self-copy.
        '''
        cp = self.copy()
        self.clear()
        old = self._stack.pop()
        self.update(old)
        return cp
    if 1:   # Context manager
        def uses(self, styles_dict):
            'Used to utilize a new set of styles in a context manager block'
            self._newstyles = styles_dict
            return self
        def __enter__(self):
            assert self._newstyles is not None
            self.ppush(self._newstyles)
            self._newstyles = None
            return self     # Gives caller access to new instance state
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.ppop()
            if exc_type is None or exc_type is TypeError:
                return True     # Ignore this exception
            else:
                return False    # Don't ignore this exception

if __name__ == "__main__":  
    from lwtest import run, Assert, raises
    def Demo():
        from color import t
        styles = {"y": t.yell, "g": t.grnl, "n": t.n}
        u = Trm(styles) 
        print("The following demonstrates normal dictionary access to colors:")
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        newstyles = {"r": t.red, "g": t.blul, "y": t.cynl}
        with u.uses(newstyles) as p:
            print("Now we're inside the context manager and the colors will change.")
            print("Green will become blue and yellow will be cyan:")
            print(f"  This is {p.g}green, {p.y}yellow is to the end{p.n}")
            print("This demonstrates changing the 'styles' with a new dict.")
            print("The following shows the new color in the context:")
            print(f"  The new color is {p.r}red{p.n}")
            print("Inside the context manager:")
            pp(u)
            if 0:
                raise ValueError("Raised inside context manager")
            else:
                raise TypeError("Raised inside context manager")
        print("\nOutside the context manager:")
        pp(u)
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        with raises(AttributeError):
            u.r
    def Test_Init():
        styles = {
            "a": "orn",
            "b1": Color("#ff8700"),
            "b2": Color("$00a0a0"),
            "b3": Color("@00a0a0"),
            "c": Color(208),           
            "d": Color(0xd0),          
            "e": Color(0o320),         
            "f": Color(0b11010000),
            "g": Color("#ff8700"),
            "h": Color("255 135 0"),
            "i": Color(0.5),
            "j": Color("555"),
            "k": Color((0.5,0.7,0.9)),
            "l": Color("0.5 0.7 0.9"),
            "m": Color("0.5,0.7,0.9"),
        }
        # Verify that all values are escape codes
        u = Trm(styles)
        for i in u:
            value = u[i]
            Assert(isinstance(value, str))
            Assert(len(value) > 0)
            Assert(value[0] == "\x1b")

    if len(sys.argv) > 1:
        Demo()
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
