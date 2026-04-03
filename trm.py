r'''
    
Trm class for color output in terminals
    
Trm is a specialized dictionary with elements that are turned into strings that are ANSI
escape sequences.  It facilitates getting colorized output in python scripts run in a
terminal.  Here's an example of printing an error message in red:
    
    u = Trm()       # Creates an empty Trm instance
    u.red = "red"   # Defines a dict entry u["red"]
    u.print(f"{u.red}Error message")
    
This produces the string "Error message" on the screen in the red color.  My terminal's
background color is black, so this is quite visible compared to the normal white
foreground text.
    
The 'u.red = "red"' line is syntactic sugar for making a dict element behave the same
way as a class attribute.  This works if the string variable xx is such that
xx.isidentifier() is True, meaning it's a valid python identifier.  The reason for it is
that it makes the use in f-strings a little less cluttered.  The u.print line could also
be written u.print(f"{u['red']}Error message"), which is legal python syntax but a
little harder to read and mentally parse quickly.
    
We could have defined the red color with an integer index
    
    u[0] = "red" 
    
and used u.print(f"{u[0]}Error message").
    
If you do the above in the python REPL, you'll find that the "Error message" string is
printed in red, but then so are all the following lines you type.  This is because the
ANSI escape code is '\x1b[38;2;254;0;0m', which is the string value of u.red (this
assumes your terminal is using 24-bit colors).  After printing, we need to have the
foreground color set back to the default color.  On my terminal, that color is "wht",
short for "white".  The Trm class has a special name for this foreground color, which is
"n", short for the normal color.  Thus, define u.n as
    
    u.n = "wht"
    
If you execute u.print(f"{u.red}Error message") again, the REPL's '>>>' prompt will be
white.  This works because Trm.print() is an instance method that sends the u.n escape
code to the output stream at the end of printing if the Trm dict contains the "n" key.
    
A common use case of this Trm object is to define a set of colors you want to use for a
script at script initialization.  Occasionally, perhaps in a function, you'd like to use
a slightly different set of colors, but you don't want to mess up the script's global
color definitions.  The Trm is a context manager that makes it easy to handle this case:
define the new colors you want to use in a dictionary (or another Trm instance).
Suppose for the above red error message example, we instead wanted to use an orange
error message.  The pattern to use in the function is 
    
    new_colors = {"red": "orn"}
    with u.uses(new_colors) as v:
        v.print(f"{v.red}Error message")
        
and the global u Trm instance reverts to its original state as the context manager block
exits.
    
If you want to customize the Trm class for your own use:
    - Choose names of colors you'd like to use from data/dpcolornames.py.  If you like,
      you can edit data/dp_make_colornames.py to produce the set of color names you'd
      like to use.
    - Set the class variable Trm.std to the set of color names you'd like to use.
    - Set the class variable Trm.normal to the normal foreground color, background
      color, and style that is normal for your terminal.
    - You may want to edit the Trm constructor (__init__()) to behave as you wish.  As
      written, the 'default' keyword of the constructor can let you choose some different
      sets of color names at initialization.
    
The color.Color constructor takes a number of different specifications for color and 
Color.adjust() lets you fiddle with getting a color.

'''
if 1:   # Header
    if 1:   # Standard imports
        import collections
        import contextlib
        import decimal
        import fractions
        import math
        import pdb
        import pprint
        import sys
        import types
        import typing as ty
    if 1:   # Custom imports
        import color
        import columnize
        import dpcolornames
        import dpmath
        import dptypes
        pp = pprint.pprint
        if 0:
            import debug
            debug.SetDebugger()
        if ty.TYPE_CHECKING:
            import color  # Only seen by Mypy, ignored at runtime
    if 1:   # Core file gist information
        __gist__      = "Trm class for color output in terminals"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __category__  = "util"
        __todo__      = ''' 

            - ∞∞2 Need a test to prove that default behavior is colorizing in a script
              to stdout, but when stdout isn't a TTY, then there are no escape codes
              emitted

        '''
    if 1:   # Global variables
        yy = pdb.set_trace
class Trm(collections.UserDict[str, str]):
    '''Dictionary used to output escape codes to a terminal.
    
        u = Trm()   # Initialized with my default set of colors
        u.list()    # Print the defined color names to stdout
        print(u)    # See the overall state
    
        Define new colors:
            u[0] = "Pine glade"         # Name will be normalized to "pine_glade"
                # Uses data/dpcolornames.py to look up normalized color names
            # Use white foreground on blue background and bold underlined
            u.debug = u("wht", "blu", "bo ul")
            u.it = u(attr="it")         # Normal color but italics
            Defining new attributes like this converts them to Color instances, then
            converts them to ANSI escape code strings.  Thus, this is a specialized
            dictionary that holds escape sequence strings.
        Access color names in two ways:
            u["red"]                    # Dictionary style
            u.red                       # Attribute style (name must be valid python symbol)
        Print to the terminal in color:
            print(f"Here's a message {u.red}partly in red.")
            --> Problem:  terminal output remains in color red, so next output is in the same
            color.  Use the Trm.print() method instead (same syntax as print):
            u.print(f"Here's a message {u.red}partly in red.")  # Back to default colors at end
    
        Changing color styles: There are a few ways to use different sets of colors
        without losing your old ones:
            
        - Push and pop:  an internal stack maintains the Trm instance's dictionary state
          (i.e., the key:value pairs).  Call u.ppush() and the stack holds the existing
          state.  Change the Trm instance as needed; when finished, call u.ppop() to get
          back to the old state.
    
        - Context manager (internally, this uses the stack like the previous example,
          but this is syntactically "cleaner"):  
    
            di = {"red": color.Color("blu")}
            with u.uses(di) as p:
                p.print("{p.red}This is red")
            u.print("{u.red}No, this is red")
            
        - Make a copy:  v = Trm(u) is a deep copy of u.  Toss it out when you're finished.
    
        Attributes
            - You can store attributes in the dictionary instance, but they must start
              with "_" so that they do not get modified.  All other attributes you set
              are converted to a color.Color instance, then changed to an escape code.
    
        u.on and u.always
            - At anytime, set u.on to False and all escape codes "disappear", as all
              dictionary access through keys returns an empty string.
            - If u.always is False, then all escape codes "disappear" if you print to
              e.g. a file (technically, if sys.stdout.isatty() is False).  If you want
              the output to contain the escape codes even if e.g. redirecting to a file,
              set u.always to True.
    
        References:
        - Normal, bold, italic, underlined, subscript, superscript, etc.:
            https://en.wikipedia.org/wiki/ANSI_escape_code#Select_Graphic_Rendition_parameters
        - 8-bit color
            https://en.wikipedia.org/wiki/ANSI_escape_code#8-bit
        - 24-bit color
            https://en.wikipedia.org/wiki/ANSI_escape_code#24-bit
    '''
    def __init__(self, initial_data: ty.Optional[ty.Dict[str, str]] = None) -> None:
        '''Calling with None creates an empty container.  Otherwise, you can initialize
        with a regular dict that maps names to desired color names.
        
        Since this is a UserDict, metadata are separated from the dictionary's payload:
            - Attributes in self.__dict__:  knobs and dials
            - Data:  stored in self.data, the native python dict this class is wrapping
        '''
        # Initialize the skeleton (but DON'T pass data yet)
        super().__init__(dict())
        if 1:   # Set up our core attributes
            self._stack: list[dict[str, str]] = []  # Saves previous states of self
            self._on = True                         # Output escape codes if True
            self._always = False                    # If True, output escape codes even if stdout isn't a tty
           #self._isatty = sys.stdout.isatty()      # False in a pipe
            self._newstyles: dict[str, str] = {}    # Used for context manager behavior
        # Process initial_data, a dictionary
        if initial_data is not None:
            for key in initial_data:
                # Note this form is required to ensure __setattr__ is called
                self[key] = initial_data[key]
    def _esc(self,      # Return escape code for the color.Color instance clr
             clr: "color.Color|None" = None,
             bg: bool=False
            ) -> str:
        '''Return escape code for the color.Color instance clr
        If bg is True, this means it's a background color rather than a foreground
        color, resulting in a different escape code.
        '''
        if clr is None:
            return ""
        elif not isinstance(clr, color.Color):
            raise TypeError("color must be a color.Color instance")
        if clr.bpc < 8:  # Assumes 24-bit color
            raise ValueError(f"Must have 8 bits per color")
        elif clr.bpc > 8:
            clr = clr.change_bpc(8)
        r, g, b = clr.irgb
        return f"\x1b[{48 if bg else 38};2;{r};{g};{b}m"
    def __call__(self,  # Return escape code string for (fg, bg, attr)
                 fg: "color.Color | str | int | None" = None,
                 bg: "color.Color | str | int | None" = None,
                 attr: str | None = None
                ) -> str:
        '''Return the indicated color style escape code string
        fg and bg can be
            - color.Color instance
            - Color name that can be found in data/dpcolornames.py
            - Other argument that color.Color constructor accepts
        attr is a string
            - Separate multiple attributs by spaces
            - Typical:  'no' for normal, 'bo' for bold, 'it' for italic, etc.
        '''
        ok = (str, color.Color, int, float, decimal.Decimal, fractions.Fraction)
        msg = "{} must be None, a string, or a color.Color instance"
        if fg is None and bg is None and attr is None:
            raise ValueError("At least one of fg, bg, or attr must be not None")
        if fg is not None and not isinstance(fg, ok):
            s = msg.format("fg") + f":\n    It's {fg!r}" 
            raise ValueError(s)
        if bg is not None and not isinstance(bg, ok):
            s = msg.format("bg") + f":\n    It's {bg!r}" 
            raise ValueError(s)
        if attr is not None and not isinstance(attr, str):
            s = f"attr must be a string:\n    It's {attr!r}" 
            raise ValueError(s)
        if not self._on or all(i is None for i in (fg, bg, attr)):
            return ""
        # Convert to a Color instance
        if fg is not None and isinstance(fg, ok):
            fg = color.Color(fg)
        if bg is not None and isinstance(bg, ok):
            bg = color.Color(bg)
        # Construct the needed escape codes
        out = []
        out.append(self._esc(fg))
        out.append(self._esc(bg, bg=True))
        if attr is not None and attr:    # Get attribute codes
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
    def __setitem__(self, name: str, value: ty.Any) -> None:     # Set self[key]
        'Set self[key] to value and convert it to an escape sequence'
        # value can be a single argument or a sequence of 1 to 3 arguments.  They 
        # will be used with the __call__ method
        if isinstance(value, (tuple, list)):
            if len(value) in (1, 2, 3):
                escape_code = self(*value)
            else:
                raise ValueError("value sequence must have 1 to 3 components")
        else:
            if isinstance(value, str):
                if not value:               # Empty string
                    escape_code = value
                elif value[0] == "\x1b":    # It's already an escape code
                    escape_code = value
                else:
                    escape_code = self(value)
            else:
                escape_code = self(value)
        # Note escape code is allowed to be an empty string
        assert isinstance(escape_code, str)
        self.data[name] = escape_code
    def __getitem__(self, key: str) -> str:             # All attribute access
        '''This is the "gatekeeper", as all attribute and data access goes through this
        function, unlike the builtin dict.
        '''
        # Internal logic uses the private variables for speed/clarity
        #if not self._on or (not self._isatty and not self._always):
        if not self._on or (not sys.stdout.isatty() and not self._always):
            return ""
        # Return the escape code or empty string if missing
        return self.data.get(key, "")
    def __setattr__(self, name: str, value: ty.Any) -> None:     # Set an attribute
        '''This function gives us complete control over metadata versus data.  In this
        implementation, the metadata variables are named by 'allowed' below, so these
        are our attributes and go to the superclass.  Everything else is assumed to be a
        user-defined dict key, i.e., a color definition.
        '''
        if 0:
            print(f"Trm.__setattr__: name = {name!r}, value = {value!r}", file=sys.stderr)
        # 1. Check if the class (or any parent) has a PROPERTY named 'name'
        # We look at the class (type(self)), not the instance.
        prop = getattr(type(self), name, None)
        if isinstance(prop, property) and prop.fset:
            # This EXPLICITLY triggers the @on.setter
            prop.fset(self, value)
            return
        allowed = {"data", "_stack", "_on", "_always", "_newstyles"}
        if name in allowed:     # self.data and private underscore variables
            super().__setattr__(name, value)
        else:
            self[name] = value  # Color definition -> escape code string
    def __getattr__(self, name: str) -> str:
        '''This allows 't.red' instead of t["red"]'''
        if name in self.__dict__:
            if 0:
                print(f"__getattr__:  {name} = {super().__getattribute__(name)!r}", file=sys.stderr)
            return super().__getattribute__(name)   # type: ignore
        if not self._on or (not sys.stdout.isatty() and not self._always):
            if 0:
                print(f"__getattr__:  {name}, output off, return empty string", file=sys.stderr)
            return ""
        if 0:
            print(f"__getattr__:  {name}, normal color lookup = {self.data[name]!r}", file=sys.stderr)
        return self.data[name]   # It's a color lookup
    def __enter__(self) -> "Trm":                    # Context manager entry
        assert self._newstyles is not None
        self.ppush(self._newstyles)
        self._newstyles = {}
        return self     # Gives caller access to new instance state
    def __exit__(self,          # Context manager exit
                 exc_type: ty.Type[BaseException] | None,
                 exc_val: BaseException | None,
                 exc_tb: types.TracebackType | None
                ):
        self.ppop()
        # Return False so we don't suppress exceptions (let caller handle their own crashes)
        return False
    def __str__(self) -> str:
        n = len(self)
        on = int(self._on)
        alw = int(self._always)
        ns = len(self._stack)
        new = 0 if self._newstyles is None else len(self._newstyles)
        s = "s" if n > 1 else ""
        return f"Trm({n} style{s}, on={on}, always={alw}, stack={ns}, newstyles={new})"
    def update(self, *p: ty.Any, **kw: ty.Any) -> None:     # Update ourselves with another dict, etc.
        '''Update ourselves with another dict, an iterable of pairs, or keywords.
        '''
        # Iterate with a for loop to make sure __setattr__ is called
        if len(p) == 1 and hasattr(p[0], "keys"):   # It's a dict
            for key in p[0]:
                self[key] = p[0][key]
        elif p:
            for key, value in p:                    # (key, value) pairs
                self[key] = value
        for key in kw:                              # Keyword dict
            self[key] = kw[key]
    def copy(self) -> "Trm":
        'Create a clone including dictionary data and slot states'
        cp = Trm()
        cp.on = self._on
        cp.always = self._always
        cp._stack = self._stack.copy()
        cp._newstyles = self._newstyles.copy() if self._newstyles is not None else None
        cp.update(self)
        return cp
    def ppush(self,                         # Push our state on stack; update with styles_dict
              styles_dict: ty.Optional[ty.Dict[str, ty.Any]] = None
             ) -> None:
        '''Push our dict state onto the stack and update with styles_dict
        
        Note the stack doesn't hold the state of the attributes.  The styles dict
        must be a dict instance or None.  Update our values with styles_dict's values
        after saving a copy of our values on the stack.
        '''
        if not styles_dict:
            self._stack.append(dict(self.items()))
            return
        elif not isinstance(styles_dict, dict):
            raise TypeError("styles_dict must be a dict instance")
        self._stack.append(dict(self.items()))
        self.update(styles_dict)
    def ppop(self) -> dict[str, str]:       # Pop previous state; return last-used state
        '''Get a copy X of ourself, then clear ourself and set our state to that of the
        top of the stack.  Return the state copy X.
        '''
        if self._stack:     # Make sure stack isn't empty
            self.clear()
            previous = self._stack.pop()
            self.update(previous)
        return X
    def list(self, sort=False, horiz=False, columns=0):     # Print columnized list of defined colors
        'Print defined color attributes to stdout in their colors'
        o = []
        if sort:
            for i in sorted(self):
                if i in Trm.attr:   # Don't print the text attributes
                    continue
                o.append(f"{self[i]}{i}{self.n}")
        else:
            for i in self:
                if i in Trm.attr:   # Don't print the text attributes
                    continue
                o.append(f"{self[i]}{i}{self.n}")
        for i in columnize.Columnize(o, sep=" "*4, horiz=horiz, columns=columns):
            print(i)
    def print(self, *p: ty.Any, **kw: ty.Any) -> None:      # Convenience print with .n at end
        'Print arguments with newline, reverting to normal color after finishing'
        self.out(*p, **kw)
        print(**kw)
    def out(self, *p: ty.Any, **kw: ty.Any) -> None:    # Same as print() but no newline; end with .n
        'Same as print() but no newline'
        k = kw.copy()
        if "end" not in k:
            k["end"] = ""
        print(*p, **k)
        if self.on:     # Don't send self["n"] unless our state is on
            revert = self.get("n", "")
            print(revert, **k)
    def uses(self, styles_dict: dict[str, str]) -> "Trm":  # Utilize styles in context manager block
        'Used to utilize a new set of styles in a context manager block'
        self._newstyles = styles_dict
        return self
    def __dir__(self) -> ty.List[str]:
        'Show standard attributes + all the color keys in the dict'
        # Mike pointed out this will be appreciated by autocompleters
        return list(super().__dir__()) + list(self.data.keys())
    if 1:   # Properties
        @property
        def on(self) -> bool:
            return self._on
        @on.setter
        def on(self, value: bool):
            self._on = bool(value)
        @property
        def always(self) -> bool:
            return self._always
        @always.setter
        def always(self, value: bool):
            self._always = bool(value)
class TrmDP(Trm):
    '''Container of my personalized terminal colors.
    '''
    # Standard color names to use by default
    std = set('''red ord orn yon yel ygr lwn grn sea trq cyn sky den roy blu vio lav
                 mag pnk lip blk brn gry wht lil pur olv'''.replace("\n", "").split())
    # Normal terminal text foreground and background colors and attribute(s)
    normal = ("wht", "blk", "normal")
    # Text attributes
    attr = set("no it bl rv di bo ul rb so hi sb sp".split())
    def __init__(self, initial_data: ty.Optional[ty.Dict[str, str]] = None) -> None:
        super().__init__(initial_data)
        # Get my default colors
        for i in TrmDP.std:
            self[i] = color.Color(i)
            self[i + "l"] = color.Color(i + "l")
            for j in ("1", "2", "3"):
                self[i + j] = color.Color(i + j)
        # Add text attributes (just those that work in WSL)
        for i in TrmDP.attr:
            setattr(self, i, self(attr=i))
        # Add n attribute to return to default color
        self["n"] = self(*TrmDP.normal)

if 0 and __name__ == "__main__":  
    # ∞∞
    d = {0: color.Color(0)}
    u = Trm(d)
    print(u)
    exit()

if __name__ == "__main__":  
    from lwtest import run, Assert, raises
    import io
    import contextlib
    def TrmDemo():
        print("Here's the color names in the default instance:")
        u = Trm()
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
            1: color.Color("#000000"),
            2: color.Color("$000000"),
            3: color.Color("@000000"),
            4: color.Color(0),           
            5: color.Color(0x0),          
            6: color.Color(0o0),         
            7: color.Color(0b0),
            8: color.Color((0, 0, 0)),
            9: color.Color("0 0 0"),
            10: color.Color("0, 0, 0"),
            11: color.Color(0.0),
            12: color.Color((0.0, 0.0, 0.0)),
            13: color.Color("0.0 0.0 0.0"),
            14: color.Color("0.0,0.0,0.0"),
            15: color.Color("555"),
            16: color.Color(555),
            17: color.Color(555.0),
        }
        # Verify that all values are escape codes and that all are the same as blk
        # except for #15, which is a yellow-green
        u = Trm(styles)
        blk = "\x1b[38;2;0;0;0m"
        c555 = "\x1b[38;2;163;255;0m"
        for i in u:
            value = u[i]
            Assert(isinstance(value, str) and len(value) > 0)
            Assert(value[0] == "\x1b")
            Assert(value == c555 if i >= 15 else blk)
    def Test_Trm_Stack():
        'Show we can push and pop a new state'
        if 1:   # Demonstrate we can initialize an empty dictionary
            u = Trm()
            Assert(not len(u))
        if 1:   # Add two new colors
            u[0] = "red"
            u[1] = "grn"
            red = '\x1b[38;2;254;0;0m'
            grn = '\x1b[38;2;0;254;0m'
            Assert(u[0] == red)
            Assert(u[1] == grn)
            orig = u.copy()
        if 1:   # Push the old state and add a new color
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
            Assert(2 not in u)  # Shows u[2] no longer exists
        if 1:   # Show we can push with a styles dict.  An important feature is that the
                # updating process with this styles dict must call the necessary methods
                # to turn the new elements into ones with resolved escape codes.
            di = {2: "blu"}
            u.ppush(di)
            Assert(u[2] == blu)
    def Test_Trm_Default():
        'Show that the default Trm instance has some of the basic names'
        u = TrmDP()
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
        u = TrmDP()
        u.c = u("whtl", "blu", attr="ul")
        Assert(u.c == '\x1b[38;2;255;255;255m\x1b[48;2;0;0;254m\x1b[4m')
        Assert(u.n == '\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m')
    def Test_Trm_ContextManager():
        u = Trm()
        u[0] = "red"
        red = '\x1b[38;2;254;0;0m'
        Assert(u[0] == red)
        di = {0: color.Color("blu")}
        blu = '\x1b[38;2;0;0;254m'
        with u.uses(di) as p:
            Assert(u[0] == blu)
        Assert(u[0] == red)
    def Test_Trm_Attributes():
        'Verify that on and always work, along with attributes'
        if 1:   # Attribute behavior:  color.Color --> escape code
            u = Trm()
            # Normal dictionary setting works 
            u["red"] = u("red")
            Assert(u["red"] == '\x1b[38;2;254;0;0m')
            # red also acts as if it was an attribute
            Assert(u.red == '\x1b[38;2;254;0;0m')
            del u["red"]
            Assert("red" not in u)
            with raises(KeyError):
                u.red   # Now it's not an attribute anymore
            # Set it as an attribute
            u.red = u("red")
            Assert(u.red == '\x1b[38;2;254;0;0m')
            Assert(u["red"] == '\x1b[38;2;254;0;0m')
            del u["red"]
            Assert("red" not in u)
        if 1:   # Attributes that start with underscores
            with raises(KeyError):
                u._x
            u._x = 42
            Assert(u._x == '\x1b[38;2;0;215;135m') 
            del u["_x"]
            # Note:  del u._x immediately gives an AttributeError
            with raises(KeyError):
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
        if 1:   # Show that always == True gets output even if stdout isn't a tty
            esc, nl = '\x1b[38;2;254;0;0m', "\n"
            u = Trm()
            if 1:   # Set always to True
                u.red = u("red")
                u.always = True
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    print(u.red)
                s = f.getvalue()
                Assert(s == esc + nl)
            if 1:   # Set always to False
                u.always = False
                f = io.StringIO()
                with contextlib.redirect_stdout(f):
                    print(u.red)
                s = f.getvalue()
                Assert(s == nl)
    def Test_Trm_Update():
        'Verify the update method works with the three types of input'
        result = {'red': '\x1b[38;2;254;0;0m'}
        di = {"red": "red"}
        if 1:   # Method 1:  Can update with a dict
            u = Trm() 
            Assert(len(u) == 0)
            u.update(di)
            Assert(u == result)
        if 1:   # Method 2:  an iterable (won't work with constructor)
            a = ["red", "red"]
            u = Trm() 
            u.update(a)
            Assert(u == result)
        if 1:   # Method 3:  keyword arguments (won't work with constructor)
            kw = {"red": "red"}
            u = Trm() 
            u.update(kw)
            Assert(u == result)
    def Test_Trm_Big_Dict():
        '''Load one of all the colors in data/dpcolornames.py.  This is nearly 6000
        colors, but it only takes about 100 ms to load on my 10-year-old computer, so
        you can have access to a lot of colors if you want them.
        '''
        di = dpcolornames.colornames
        keys, values = [], []
        for key in di:
            keys.append(key)
            value = di[key][0]  # This is a namedtuple
            values.append(color.Color(value.hex))
        d = dict(zip(keys, values))
        u = Trm(d)
        #print(len(u))
    def Test_Trm_No_Output():
        'No escape codes emitted when self.on is False'
        u = TrmDP()
        if 1:   # self.on is False
            out = io.StringIO()
            u.on = False
            u.print(f"{u.orn}Hello", file=out)
            s = out.getvalue()
            Assert(s == "Hello\n")
        if 1:   # self.on is True
            out = io.StringIO()
            u.on = True
            u.print(f"{u.orn}Hello", file=out)
            s = out.getvalue()
            expected = '\x1b[38;2;254;120;0mHello\x1b[38;2;181;181;181m\x1b[48;2;0;0;0m\x1b[0m\n'
            Assert(s == expected)
    def Test_Trm_Basics():
        t = Trm()
        Assert(not len(t))
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
