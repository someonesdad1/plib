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
    def __init__(self, di=None, default=True):
        '''Call with a dictionary di relating a name string to something that will be
        recognized by the color.Color constructor.  If default is True, then initialize
        with the colors with key == 0 in data/dpcolornames.py.  Colors in di that match
        those in the default names will overwrite the defaults.
        '''
        # Attributes with underscores are not meant to be accessed by the user
        self._stack = Stack()   # Saves previous states of self
        self.on = True          # Output escape codes if True
        self.always = False     # If True, output escape codes even if stdout out isn't a terminal
        self._newstyles = None  # Used for context manager behavior
        # Get the defaults
        if default:
            items = "red ord orn yon yel ygr lwn grn sea trq cyn".split()
            items += "sky den roy blu vio lav mag pnk lip blk ".split()
            items += "brn gry wht lil pur olv".split()
            for i in items:
                self[i] = Color(i)
        # Convert the items in names_dict to escape codes and add them to our mapping
        if di is not None:
            if not isinstance(di, dict):
                raise TypeError("di must be a dict")
            for i in di:
                self[i] = di[i]
        if default:
            # Add n attribute to return to default color
            self["n"] = self("wht", "blk", "no")
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
                out.append(f"\x1b[{di[a]}m")
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
                if isinstance(value, str) and value[0] == "\x1b":
                    # It's already an escape code
                    escape_code = value
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
    def ppush(self, styles_dict=None):
        '''The styles dict must be a dict instance or None.  Update our values with
        styles_dict's values after saving a copy of ourself on the stack.
        '''
        if styles_dict is not None and not isinstance(styles_dict, dict):
            raise TypeError("styles_dict must be a dict instance")
        self._stack.push(self.copy())
        # Note:  the dict.__update__ method won't work properly here; we use a loop
        # which causes __setitem__ to be used.
        if styles_dict is not None:
            for i in styles_dict:
                self[i] = styles_dict[i]
    def ppop(self):
        '''Get a copy of ourself, then clear ourself and set our state to that of the
        top of the stack; return the copy of our old self.
        '''
        old_self = self.copy()
        self.clear()
        previous = self._stack.pop()
        self.update(previous)
        return old_self
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
        '''Show the common initializers for a Color instance work and are returned with
        the proper escape codes.
        '''
        styles = {
            0: "blk",
            1: Color("#000000"),
            2: Color("$000000"),
            3: Color("@000000"),
            4: Color(0),           
            5: Color(0x0),          
            6: Color(0o0),         
            7: Color(0b0),
            8: Color("0 0 0"),
            9: Color("0,0,0"),
            10: Color(0.0),
            11: Color((0.0,0.0,0.0)),
            12: Color("0.0 0.0 0.0"),
            13: Color("0.0,0.0,0.0"),
            14: Color("555"),
            15: Color(555),
            16: Color(555.0),
        }
        # Verify that all values are escape codes and that all are the same as blk
        # except for #14, which is a yellow-green
        u = Trm(styles, default=False)
        blk = "\x1b[38;2;0;0;0m"
        yg = "\x1b[38;2;90;240;6m"
        for i in u:
            value = u[i]
            Assert(isinstance(value, str) and len(value) > 0)
            Assert(value[0] == "\x1b")
            Assert(value == yg if i > 13 else blk)
    def Test_Stack():
        'Show we can push and pop a new state'
        # Demonstrate we can initialize an empty dictionary
        u = Trm(default=False)
        Assert(not len(u))
        # Add two new colors
        u[0] = "red"
        u[1] = "grn"
        red = '\x1b[38;2;254;0;0m'
        grn = '\x1b[38;2;0;254;0m'
        Assert(u[0] == red)
        Assert(u[1] == grn)
        orig = u.copy()
        # Push the old state and add a new color
        u.ppush()
        Assert(u == orig)
        blu = '\x1b[38;2;0;0;254m'
        u[2] = "blu"
        Assert(u[2] == blu)
        # Push again
        u.ppush()
        u.clear()
        Assert(not u)
        # Pop and show we've got blu again
        u.ppop()
        Assert(u[2] == blu)
        # Pop and show we're back to orig
        u.ppop()
        Assert(u == orig)
        with raises(KeyError):
            u[2]    # This shows u[2] no longer exists
        # Show we can push with a styles dict.  An important feature is that the
        # updating process with this styles dict must call the necessary methods to turn
        # the new elements into ones with resolved escape codes.
        di = {2: "blu"}
        u.ppush(di)
        Assert(u[2] == blu)
    def Test_Default():
        'Show that the default Trm instance has some of the basic names'
        u = Trm()
        items = "red ord orn yon yel ygr lwn grn sea trq cyn".split()
        items += "sky den roy blu vio lav mag pnk lip blk ".split()
        items += "brn gry wht lil pur olv".split()
        for i in items:
            Assert(i in u)
    def Test_Call():
        '''Test the __call__ method to show that it's capable of reproducing the
        behavior of the old implementation, particularly changing the background color
        and attributes.
        '''
        u = Trm()
        u.c = u("whtl", "blu", attr="ul")
        Assert(u.c == '\x1b[38;2;255;255;255m\x1b[48;2;0;0;254m\x1b[4m')
        Assert(u.n == '\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m')

    if len(sys.argv) > 1:
        Demo()
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
