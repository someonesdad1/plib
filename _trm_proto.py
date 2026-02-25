'''

ToDo
    - Add update() and only take dicts
    - Trm(di):  if di is a Trm instance, make an identical (deep) copy of it

'''
if 1:   # Header
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
        import columnize
        import dpcolornames
        import dpmath
        import dpprint
        import stack
        import wl2rgb
        Color = color.Color
        Columnize = columnize.Columnize
        Stack = stack.Stack
        PP = dpprint.PP
        pp = PP()   # Get pprint with current screen width
    if 0:
        import debug
        debug.SetDebugger()

class Trm(dict):
    '''Dictionary used to output escape codes to a terminal.

        u = Trm(default=True)   # Initialized with my default set of colors
        u.list()                # Print the defined color names to stdout

        Define new colors:
            u[0] = "Pine glade"         # Name will be normalized to "pine_glade"
            # Use white foreground on blue background and bold underlined
            u.debug = u("wht", "blu", "bo ul")
            u.ul = u(attr="it")         # Normal color but italics
            Defining new attributes like this converts them to Color instances, then
            converts them to ANSI escape code strings.
        Access color names in two ways:
            u["red"]                    # Dictionary style
            u.red                       # Attribute style (name must be valid python symbol)
        Print to the terminal in color:
            print(f"Here's a message {u.red}partly in red.")
            --> Problem:  terminal output remains in color red, so next output is in the same
            color.  Here's a fix:
            u.print(f"Here's a message {u.red}partly in red.")  # Back to default colors at end

        Changing color styles: There are a few different ways to use different sets of
        colors without losing your old ones:
            
        - Push and pop:  an internal stack maintains the Trm instance's dictionary state
          (i.e., the key:value pairs).  Call u.ppush() and the stack holds the existing
          state.  Change the Trm instance as needed; when finished, call u.ppop() to get
          back to the old state.

        - Context manager (internally, it uses the stack like the previous example):  

            di = {"red": Color("blu")}
            with u.uses(di) as p:
                p.print("{p.red}This is red")
            u.print("{u.red}No, this is red")
            
        - Make a copy:  v = Trm(u) is a deep copy of u.  Toss it out when you're finished.

        References:
        - Normal, bold, italic, underlined, subscript, superscript, etc.:
            https://en.wikipedia.org/wiki/ANSI_escape_code#Select_Graphic_Rendition_parameters
        - 8-bit color
            https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
        - 24-bit color
            https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    '''
    # Standard color names to use by default
    std = set('''red ord orn yon yel ygr lwn grn sea trq cyn sky den roy blu vio lav
                 mag pnk lip blk brn gry wht lil pur olv'''.replace("\n", "").split())
    # Normal terminal text foreground and background colors and attribute(s)
    normal = ("wht", "blk", "normal")
    def __init__(self, *p, **kw):
        '''Initialize with the standard dictionary initializers.  The key can be any
        hashable type and the value should be anything accepted by the color.Color
        constructor.

        'default' is the only keyword not related to dictionary initialization.  If
        present, it should be an integer of 0, 1, 2, which are used to identify the 
        colors of Trm.std that are included in the Trm instance:
            0 = the colors in Trm.std
            1 = 0 plus the "l" additions
            2 = 1 plus the 1, 2, and 3 additions
        Note default is ignored unless di is None.  Colors in di that match those in the
        default names will overwrite the defaults.
        '''
        # Attributes with underscores are not meant to be accessed by the user
        self._stack = Stack()   # Saves previous states of self
        self.on = True          # Output escape codes if True
        self.always = False     # If True, output escape codes even if stdout out isn't a terminal
        self._newstyles = None  # Used for context manager behavior

        # Process p
        if len(p) == 1 and hasattr(p[0], "keys"):
            di = p[0]
            # It's a dictionary
            if isinstance(di, Trm):
                # It's a Trm instance, so make a deep copy
                self._stack = di._stack
                self.on = di.on
                self.always = di.always
                self._newstyles = di._newstyles
            for key in di:
                self[key] = di[key]
        elif p:
            for key, value in p:
                self[key] = value
        # Process kw
        default = None
        for key in kw:
            if key == "default":
                default = kw[key]
            else:
                self[key] = kw[key]
        if default is not None:  # Get the default colors
            if not isinstance(default, int):
                raise TypeError("default keyword must be an integer")
            if default not in (0, 1, 2):
                raise ValueError("default keyword must be 0, 1, or 2")
            for i in Trm.std:
                if default > 0:
                    self[i + "l"] = Color(i + "l")
                self[i] = Color(i)
                if default > 1:
                    for j in ("1", "2", "3"):
                        self[i + j] = Color(i + j)
            # Add n attribute to return to default color
            self["n"] = self(*Trm.normal)
    def _esc(self, color=None, bg=False):
        'Return escape code for the Color instance color'
        if color is None:
            return ""
        if not isinstance(color, Color):
            raise TypeError("color must be a color.Color instance")
        if color.bpc < 8:  # Assumes 24-bit color
            raise ValueError(f"Must have 8 bits per color")
        elif color.bpc > 8:
            color = color.change_bpc(8)
        r, g, b = color.irgb
        return f"\x1b[{48 if bg else 38};2;{r};{g};{b}m"
    def __call__(self, fg=None, bg=None, attr=None):
        '''Return the indicated color style escape code string.  
        fg and bg can be
            - Color instance
            - Color name that can be found in data/dpcolornames.py
        attr is a string
            - Separate multiple attributs by spaces
            - Typical:  'no' for normal, 'bo' for bold, 'it' for italic, etc.
        '''
        ok = (str, Color, int, float, Decimal, Fraction)
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
        out.append(self._esc(fg))
        out.append(self._esc(bg, bg=True))
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
    def __setitem__(self, name, value):     # Set self[key]
        'Set self[key] to value and convert it to an escape sequence'
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
    def __setattr__(self, name, value):     # Set an attribute
        '''This is used to make sure the on, always, and any attributes that start with
        '_' get set correctly.  It also adds syntactic sugar to the class by letting you
        set and access dictionary keys by using them like attributes, as long as they
        are strings that have isidentifier() True.
        '''
        if name in set("on always".split()):
            super().__setattr__(name, bool(value))
        elif name.startswith("_"):
            super().__setattr__(name, value)
        else:
            self[name] = value
    def __getitem__(self, name):        # Get self[name]
        'This is used to get self[name]'
        # If self.on isn't True, always return an empty string
        if not self.on:
            return ""
        # If self.always is False and stdout isn't a tty, return ""
        if not self.always and not sys.stdout.isatty():
            return ""
        # Otherwise, return the escape sequence
        return super().__getitem__(name)
    def __getattribute__(self, name):   # Get instance's attributes and dict's keys
        '''This allows you to access a dictionary key using the syntax self.key instead
        of self[key] (key.isidentifier() must be True).  It also lets us get to our
        other attributes that are not in the dict without the infinite recursion
        problem.
        '''
        return self.__getitem__(name) if name in self else super().__getattribute__(name)
    def __enter__(self):    # Context manager entry
        assert self._newstyles is not None
        self.ppush(self._newstyles)
        self._newstyles = None
        return self     # Gives caller access to new instance state
    def __exit__(self, exc_type, exc_val, exc_tb):  # Context manager exit
        self.ppop()
        if exc_type is None or exc_type is TypeError:
            return True     # Ignore this exception
        else:
            return False    # Don't ignore this exception
    def update(self, *p, **kw):
        '''Update ourselves with another dictionary, an iterable of pairs, or keywords.
        Note this method will result in __setitem__ being called, which ensures
        translation to an escape code.
        '''
        if len(p) == 1 and hasattr(p[0], "keys"):
            for key in p[0]:
                self[key] = p[0][key]
        elif p:
            for key, value in p:
                self[key] = value
        for key in kw:
            self[key] = kw[key]
    def ppush(self, styles_dict=None):
        '''The styles dict must be a dict instance or None.  Update our values with
        styles_dict's values after saving a copy of ourself on the stack.
        '''
        if styles_dict is not None and not isinstance(styles_dict, dict):
            raise TypeError("styles_dict must be a dict instance")
        self._stack.push(self.copy())
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
    def list(self, msg=None, ignore_std=True, sort=False):
        'Print defined color attributes to stdout'
        o = []
        if sort:
            for i in sorted(self):
                o.append(f"{self[i]}{i}{self.n}")
        else:
            for i in self:
                o.append(f"{self[i]}{i}{self.n}")
        for i in Columnize(o, sep=" "*4):
            print(i)
    def print(self, *p, **kw):
        'Print arguments with newline, reverting to normal color after finishing'
        self.out(*p, **kw)
        print(**kw)
    def out(self, *p, **kw):
        'Same as print() but no newline'
        k = kw.copy()
        if "end" not in k:
            k["end"] = ""
        print(*p, **k)
        print(self.n, **k) if "n" in self else print("", **k)
    def uses(self, styles_dict):
        'Used to utilize a new set of styles in a context manager block'
        self._newstyles = styles_dict
        return self

if __name__ == "__main__":  
    from lwtest import run, Assert, raises
    import io
    import contextlib
    def Demo():
        print("Here's the color names in the default instance:")
        u = Trm(default=True)
        u.list()
        print()
        #
        styles = {"y": "yel", "g": "grn", "n": "wht"}
        newstyles = {"r": "red", "g": "blu", "y": "cyn"}
        u.print(f"{u(attr='ul')}u is a Trm instance (defined without the default colors):")
        u = Trm(styles, default=False) 
        pp(u)
        print("The following demonstrates normal dictionary access to colors:")
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        print("The following will demonstrate the context manager behavior of u:")
        print(f"{'-'*80}")
        with u.uses(newstyles) as p:
            print("  Now we're inside the context manager and the colors will change.")
            print("  Green will become blue and yellow will be cyan:")
            print(f"    This is {p.g}green, {p.y}yellow is to the end{p.n}")
            print("  This demonstrates changing the 'styles' with a new dict.")
            print("  The following shows the new color in the context:")
            print(f"    The new color is {p.r}red{p.n}")
            print("  Inside the context manager, contents of u:")
            pp(u)
            if 0:
                raise ValueError("Raised inside context manager")
            else:
                raise TypeError("Raised inside context manager")
        print(f"{'-'*80}")
        print("Outside the context manager (note 'r' key is gone):")
        pp(u)
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        # This proves the r attribute is no longer present
        with raises(AttributeError):
            u.r
        # Use u.update() to make permanent changes
        print("\nThe Trm instance u was updated with the new styles dict using update():")
        u.update(newstyles)
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        pp(u)
    def Test_Trm_Init():
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
            8: Color((0, 0, 0)),
            9: Color("0 0 0"),
            10: Color("0, 0, 0"),
            11: Color(0.0),
            12: Color((0.0, 0.0, 0.0)),
            13: Color("0.0 0.0 0.0"),
            14: Color("0.0,0.0,0.0"),
            15: Color("555"),
            16: Color(555),
            17: Color(555.0),
        }
        # Verify that all values are escape codes and that all are the same as blk
        # except for #15, which is a yellow-green
        u = Trm(styles)
        blk = "\x1b[38;2;0;0;0m"
        yg = "\x1b[38;2;90;240;6m"
        for i in u:
            value = u[i]
            Assert(isinstance(value, str) and len(value) > 0)
            Assert(value[0] == "\x1b")
            Assert(value == yg if i >= 15 else blk)
    def Test_Trm_Stack():
        'Show we can push and pop a new state'
        # Demonstrate we can initialize an empty dictionary
        u = Trm()
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
    def Test_Trm_Default():
        'Show that the default Trm instance has some of the basic names'
        u = Trm(default=0)
        items = "red ord orn yon yel ygr lwn grn sea trq cyn".split()
        items += "sky den roy blu vio lav mag pnk lip blk ".split()
        items += "brn gry wht lil pur olv".split()
        for i in items:
            Assert(i in u)
    def Test_Trm_Call():
        '''Test the __call__ method to show that it's capable of reproducing the
        behavior of the old implementation, particularly changing the background color
        and attributes.
        '''
        u = Trm(default=0)
        u.c = u("whtl", "blu", attr="ul")
        Assert(u.c == '\x1b[38;2;255;255;255m\x1b[48;2;0;0;254m\x1b[4m')
        Assert(u.n == '\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m')
    def Test_Trm_ContextManager():
        u = Trm()
        u[0] = "red"
        red = '\x1b[38;2;254;0;0m'
        Assert(u[0] == red)
        di = {0: Color("blu")}
        blu = '\x1b[38;2;0;0;254m'
        with u.uses(di) as p:
            Assert(u[0] == blu)
        Assert(u[0] == red)
    def Test_Trm_Attributes():
        'Verify that on and always work, along with attributes'
        if 1:   # Attribute behavior:  Color --> escape code
            u = Trm()
            # Normal dictionary setting works 
            u["red"] = u("red")
            Assert(u["red"] == '\x1b[38;2;254;0;0m')
            # red also acts as if it was an attribute
            Assert(u.red == '\x1b[38;2;254;0;0m')
            del u["red"]
            Assert("red" not in u)
            with raises(AttributeError):
                u.red   # Now it's not an attribute anymore
            # Set it as an attribute
            u.red = u("red")
            Assert(u.red == '\x1b[38;2;254;0;0m')
            Assert(u["red"] == '\x1b[38;2;254;0;0m')
            del u["red"]
            Assert("red" not in u)
        if 1:   # Attributes that start wit underscores
            a = 42
            with raises(AttributeError):
                u._x
            u._x = a
            Assert(u._x == a)
            del u._x
            with raises(AttributeError):
                u._x
        if 1:   # Show that on toggles escape code output on and off
            esc, nl = '\x1b[38;2;254;0;0m', "\n"
            u = Trm()
            u.red = u("red")
            u.on = True
            Assert(u.red == esc)
            u.on = False
            Assert(u.red == "")
            u.on = True
            Assert(u.red == esc)
        if 1:   # Show that always == on gets output even if stdout isn't a tty
            esc, nl = '\x1b[38;2;254;0;0m', "\n"
            u = Trm()
            u.red = u("red")
            u.always = False
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                print(u.red)
            s = f.getvalue()
            Assert(s == nl)
            u.always = True
            f = io.StringIO()
            with contextlib.redirect_stdout(f):
                print(u.red)
            s = f.getvalue()
            Assert(s == esc + nl)
    def Test_Trm_Update():
        'Verify the update method works with the three types of input'
        result = {'red': '\x1b[38;2;254;0;0m'}
        # Method 1:  a dict
        di = {"red": "red"}
        u = Trm(di)     # Check constructor works with a dict too
        Assert(u == result)
        u = Trm()
        u.update(di)
        Assert(u == result)
        # Method 2:  an iterable (won't work with constructor)
        a = ["red", "red"]
        u = Trm(a)     # Check constructor works with a sequence
        Assert(u == result)
        u = Trm()
        u.update(a)
        Assert(u == result)
        # Method 3:  keyword arguments (won't work with constructor)
        kw = {"red": "red"}
        u = Trm(**kw)     # Check constructor works with a keyword dict
        Assert(u == result)
        u = Trm()
        u.update(kw)
        Assert(u == result)

    if 0:
        u = Trm()
        for i in (0, 1, 2):
            print(i)
            u = Trm(default=i)
            u.list()
        exit()
    if 0 or len(sys.argv) > 1:
        Demo()
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
