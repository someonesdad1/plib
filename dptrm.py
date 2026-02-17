'''

t = Trm()

ToDo
    - Core features
        - t.x is short for t["x"]; x has to be a valid python identifier
        - t.on (bool) used to turn escape code emission and and off
        - t.always (bool) causes output of escape codes to stdout even if it's not a tty
        - t(x) returns the escape code for a color specifier x (x accepted by Color
          constructor)
        - with t.users(styles_dict) is context manager
        - t.ppush() and t.ppop() methods save/restore state on a stack
            - Use stack.StackLock in Trm too?
        - bool(t) is True while you can ppop()
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
import sys
import wl2rgb
import color
import math
import dpmath
Color = color.Color
t = color.t
from stack import Stack
from dpprint import PP
pp = PP()   # Get pprint with current screen width
if len(sys.argv) > 1:
    import debug
    debug.SetDebugger()

class Trm(dict):
    '''Dictionary to hold color names for colorizing terminal output.
        Normal usage:
            # Create an initializer that the dict constructor will take:  
            mystyles = {"red": "#ff0000", "n": Color("#a0a0a0", 0)}
            t = Trm(mystyles)
            print("This is a plain message with no colorizing")
            print(f"{t.red}This is a message in red{t.n}")

        Temporary change of styles with context manager
            newstyles = {"red": "#0000ff"}  # Now red is actually blue
            with t.uses(newstyles) as p:
                print(f"{p.red}This is a message in blue{p.n}")
            with t.uses(newstyles):
                print(f"{t.red}This is a message in blue{t.n}")
            # Note both with statements give the same results
            # After context manager exits, revert to old definitions
            print(f"{t.red}This is a message in red{t.n}")

        Trm instance has a stack to let you save the current state, create a modified
        state, do arbitrary processing, then return to the previous state.  The context
        manager example above is just syntactic sugar for the following behavior:
            print("Showing use of stack feature")
            print(f"{t.red}This is a message in red{t.n}")
            t.ppush(newstyles)
            print("Just pushed a new dict with red changed to blue")
            print(f"{t.red}This is a message in blue{t.n}")
            print("Do other processing...")
            print("Calling t.ppop() restores the old state")
            print(f"{t.red}This is a message in red{t.n}")
    '''
    def __init__(self, names_dict):
        # Attributes with underscores are not meant to be accessed by the user
        self._stack = Stack()   # Saves previous states of self
        self.on = True          # Output escape codes if True
        self.always = False     # If True, output escape codes even if stdout out isn't a terminal
        self._newstyles = None  # Used for context manager behavior
        super().__init__(names_dict)
        self.esc()              # Change color content to escape codes
    def esc(self):
        '''Change all dict values into escape codes.  This is done by translating all
        the values received to a Color instance, then calling self._get_code().

        Eventually, color.Color() will handle everything, so this will be 
            for i in self:
                self[i] = self.get_escape_code(Color(i))

        Note:  this functionality will eventually be moved into dpcolor.py.  It will
        either be a method or class method of Color or be a separate function.
        '''
        for i in self:
            u = self[i]
            #print(f"{i} = {u!r}")
            if isinstance(u, str):
                if u[0] == "\x1b":      # Escape character; it's already resolved
                    continue
                u = u.strip()
                if u[0] in "#$@":       # Hex format 
                    c = Color(u)
                elif u.endswith("nm"):  # Is a wavelength
                    wl_nm = float(u[:-2])
                    c = wl2rgb.wl2rgb(wl_nm)
                elif " " in u or "," in u:  # Tuple of 3 integers
                    v = u.replace(",", " ")
                    f = v.split()
                    if len(f) != 3:
                        msg = f"{u!r} must be 3 integers separated by ' ' or ','"
                        raise ValueError(msg)
                    values = tuple(dpmath.Int(j) for j in f)
                    Color(*values)
                else:   # Float or integer
                    try:
                        x = abs(float(u))
                        fp, ip = math.modf(x)
                        c = Color(fp)
                    except Exception:
                        pass
                    n = None
                    try:
                        n = dpmath.Int(u)
                    except Exception:
                        pass
                    if n is None:
                        c = Color(u)    # Is it a string that Color() recognizes?
                    else:
                        if not (0 <= n < 256):
                            raise ValueError("An integer {n} for a color must be on [0, 255]")
                        c = color.Translate8bit(n)
            elif isinstance(u, int):
                # It's an 8-bit color
                if not (0 <= u < 256):
                    raise ValueError("An integer i = {u} for a color must be on [0, 255]")
                c = color.Translate8bit(u)
            elif isinstance(u, Color):
                c = u
            self[i] = self.get_escape_code(c)
            #print(f"  {i} gave {self[i]}this color{t.n}")
    def __call__(self, *args, **kw):
        '''Initialize a terminal color by specifying the color in args.
        This just calls Color(*args, **kw)
        '''
    def __setitem__(self, name, value):
        # Note this nicely separates the dict keys from the instance's attributes
        if name in self:
            super().__setitem__(name, value)
        elif name == "on":
            self.on = bool(value)
        elif name == "always":
            self.always = bool(value)
        elif name == "_newstyles":
            self._newstyles = value
        else:
            raise KeyError(f"{name!r} not in Trm instance")
    def __getitem__(self, name):
        'This is used to get self[name]'
        # If self.on isn't True, always return an empty string
        if not self.on:
            return ""
        # If self.always is False and stdout isn't a tty, return ""
        if not self.always and not sys.stdout.isatty():
            return ""
        # Otherwise, return self[name], which will be an escape sequence
        return super().__getitem__(name)
    def __getattribute__(self, name):
        '''This allows you to access a dictionary key using the syntax self.key instead
        of self[key].  This is a useful shorthand for the Trm instance, although it
        requires the key to be a string that's a valid python variable name.  It also
        lets us get to our other attributes that are not in the dict without infinite
        recursion.
        '''
        if super().__getattribute__("on"):
            return super().__getitem__(name) if name in self else super().__getattribute__(name)
        else:
            return ""
    def ppush(self, styles_dict):
        '''The styles dict must be a dict instance.  Update our values with
        styles_dict's values after saving a copy of ourself on the stack.
        '''
        if not isinstance(styles_dict, dict):
            raise TypeError("styles_dict must be a dict instance")
        self._stack.push(self.copy())
        self.update(styles_dict)
        self.esc()
    def ppop(self):
        '''Get a copy of ourself, then clear ourself and set our state to that of the
        top of the stack; return our self-copy.
        '''
        cp = self.copy()
        self.clear()
        self.update(self._stack.pop())
        return cp
    @property
    def stack_size(self):
        '''Return number of items on stack.  If this number is > 0, self.ppop won't
        result in an exception.
        '''
        return len(self._stack)
    if 1:   # Context manager
        def uses(self, styles_dict):
            'Used to utilize a new set of styles in a context manager block'
            if not isinstance(styles_dict, dict):
                raise TypeError("styles_dict must be a dict instance")
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
    if 1:   # Existing TRM stuff
        def get_escape_code(self, color, bg=False):
            'For Color instance color, return escape code'
            if not isinstance(color, Color):    
                raise TypeError("color must be a color.Color instance")
            bg = bool(bg)
            # We'll assume 24 bit color
            n = 48 if bg else 38
            if color.bpc > 8:
                color = color.change_bpc(8)
            r, g, b = color.irgb
            return f"\x1b[{n};2;{r};{g};{b}m"

if 0:
    # ∞∞1 These are a good set of test cases for the Color() constructor
    styles = {  # xstylesx
        # Build in names
        "a": "orn",         # Built-in name
        "b1": Color("#ff8700"),   # 24-bit hex string
        "b2": Color("$ff8700"),   # 24-bit hex string
        "b3": Color("@ff8700"),   # 24-bit hex string
        "c": 208,           # 8-bit int [0, 255]
        "d": 0xd0,          # 8-bit #208
        "e": 0o320,         # 8-bit #208
        "f": 0b11010000,    # 8-bit #208
        "g": "#ff8700",     # 8-bit #208
        "h": "255 135 0",   # 8-bit #208
      # These don't work in Color() yet
      # "i1": "0.5",        # float [0, 1] --> gray
      # "i2": 0.5,          # float [0, 1] --> gray
      # "j1": "555",        # >= 400 means a wavelength in nm
      # "j2": 555,          # >= 400 means a wavelength in nm
      # "j3": 555.0,        # >= 400 means a wavelength in nm
      # "k": (0.1,0.2,0.3), # 3-tuple of floats (Color() accepts this)
      # "l": "0.1 0.2 0.3", # 3-tuple of floats (Color() accepts this)
      # "l": "0.1,0.2,0.3", # 3-tuple of floats (Color() accepts this)
    }
    u = Trm(styles) 
    if 0:   # Only one set of outputs here prove that the .on attribute works
        for v in (True, False):
            print(".on is True (colorizing on)" if v else ".on is False (no colorizing)")
            u.on = v
            for i in u:
                t.print(f"  {u[i]}{i} is this color")
    if 1:   # Develop correct len() method
        print(f"len(u) = {len(u)}")
        for i in u:
            print(f"{i}: {u[i]!r}")
    exit()

if __name__ == "__main__":  
    from lwtest import run, raises, Assert
    from color import t
    def Demo2():
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
            #pp(u)
            if 0:
                raise ValueError("Raised inside context manager")
            else:
                raise TypeError("Raised inside context manager")
        print("\nOutside the context manager:")
        #pp(u)
        print(f"  This is {u['g']}green, {u['y']}yellow is to the end{u['n']}")
        print("The following AttributeError shows the red key 'r' is gone")
        u.r
    def Demo1():
        'Demo shown in the Trm docstring'
        # Create an initializer that the dict constructor will take:  
        mystyles = {"red": "#ff0000", "n": "#a0a0a0"}
        t = Trm(mystyles)
        print("This is a plain message with no colorizing")
        print(f"{t.red}This is a message in red{t.n}")
        if 1:   # Temporary change of styles with context manager
            newstyles = {"red": "#0000ff"}  # Now red is actually blue
            with t.uses(newstyles) as p:
                print("\n  In first context manager")
                print(f"  {p.red}This is a message in blue{p.n}")
            with t.uses(newstyles):
                print("\n  In second context manager")
                print(f"  {t.red}This is a message in blue{t.n}")
            print("\n  Note both statements gave the same result because in the context manager")
            print("  block, both t and p instances contain the same colors.")
        # After context manager exits, revert to old definitions
        print("\nOutside the context manager, t.red gives the red color again:")
        print(f"{t.red}This is a message in red{t.n}")
        exit()
    def Test_Trm():
        mystyles = {"red": Color(255, 0, 0), "n": "#a0a0a0"}
        T = Trm(mystyles)
        Assert(T.red == '\x1b[38;2;255;0;0m')
        Assert(T.n == '\x1b[38;2;160;160;160m')
        if 1:   # Verify stack works:  change red to blue
            newstyles = {"red": Color(0, 0, 255), "n": "#a0a0a0"}
            T.ppush(newstyles)
            Assert(T.red == '\x1b[38;2;0;0;255m')
            T.ppop()
            Assert(T.red == '\x1b[38;2;255;0;0m')
        if 1:   # Do same with context manager
            with T.uses(newstyles):
                Assert(T.red == '\x1b[38;2;0;0;255m')
            Assert(T.red == '\x1b[38;2;255;0;0m')
            with T.uses(newstyles) as p:
                Assert(p.red == '\x1b[38;2;0;0;255m')
            Assert(T.red == '\x1b[38;2;255;0;0m')
        if 1:   # Verify .on works
            Assert(T.red == '\x1b[38;2;255;0;0m')
            T.on = False
            Assert(T.red == '')
            T.on = True
            Assert(T.red == '\x1b[38;2;255;0;0m')
        if 1:   # Verify .always works
            raise Exception("Need .always functionality")

    if len(sys.argv) > 1:
        Demo1()
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
