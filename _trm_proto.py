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

class Trm(dict):
    '''This is a dictionary used to output escape codes to a terminal for colorizing the
    output.  It is initialized by passing in a dictionary of string names whose values
    encode a color, ultimately resulting in a color.Color instance.

    '''
    def __init__(self, names_dict):
        'Attributes with underscores are not meant to be accessed by the user'
        self._stack = Stack()   # Saves previous states of self
        self.on = True          # Output escape codes if True
        self.always = False     # If True, output escape codes even if stdout out isn't a terminal
        self._newstyles = None  # Used for context manager behavior
        super().__init__(names_dict)
        self.resolve()
    def resolve(self):
        '''Change all dict values into escape codes.  This is done by translating all
        the values received to a Color instance, then calling self._get_code().
        '''
        if 0:   # Old code before Color() updated
            for i in self:
                u = self[i]
                print(f"{i} = {u!r}")
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
                self[i] = self._get_code(c)
                #print(f"  {i} gave {self[i]}this color{t.n}")
        else:
            for i in self:
                u = self[i]
                try:
                    c = Color(u)
                except Exception:
                    print(f"{i} = {u!r} (type {type(u)})")
            exit()
    def __call__(self, *args, **kw):
        '''Initialize a terminal color by specifying the color in args.  The allowed
        forms are:

            - color.Color instance
            - string
                - Recognized name in color.Color
            - tuple of 3 integers
            - integer
            - float

        '''
    def __setitem__(self, name, value):
        if name in self:
            super().__setitem__(name, value)
        elif name == "on":
            self.on = value
        elif name == "always":
            self.always = value
        elif name == "_newstyles":
            self._newstyles = value
        elif name == "_stack":
            self._stack = value
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
    if 1:   # Existing TRM stuff
        def _get_code(self, color, bg=False):
            'For Color instance color, return escape code'
            if color is not None:
                if not isinstance(color, Color):    
                    raise TypeError("color must be a color.Color instance")
            bg = bool(bg)
            #if self._bits == 4:
            #    raise Exception("Not implemented")
            #elif self._bits == 8:
            #    raise Exception("Not implemented")
            #elif self._bits == 24:
            # We'll assume 24 bit color
            if 1:
                n = 48 if bg else 38
                if color.bpc > 8:
                    color = color.change_bpc(8)
                r, g, b = color.irgb
                return f"\x1b[{n};2;{r};{g};{b}m"
            #else:
            #    raise RuntimeError("self._bits bad")

if 1:
    # ∞∞1 These are a good set of test cases for the Color() constructor
    styles = {  # xstylesx
        # Build in names
        "a": "orn",         # Built-in name
        "b1": Color("#ff8700"),   # 24-bit hex string
        "b2": Color("$ff8700"),   # 24-bit hex string
        "b3": Color("@ff8700"),   # 24-bit hex string
        "c": 208,           # 8-bit #208
        "d": 0xd0,          # 8-bit #208
        "e": 0o320,         # 8-bit #208
        "f": 0b11010000,    # 8-bit #208
        "g": "#ff8700",     # 8-bit #208
        "h": "255 135 0",   # 8-bit #208
        "i": 0.5,           # float, middle gray
        "j": "555",         # Yellow-green, most visible to eye
        "k": (0.1,0.2,0.3), # 3-tuple of floats (Color() accepts this)
        "l": "0.1 0.2 0.3", # 3-tuple of floats (Color() accepts this)
        "l": "0.1,0.2,0.3", # 3-tuple of floats (Color() accepts this)
    }
    u = Trm(styles) 
    # Only one set of outputs here prove that the .on attribute works
    for v in (True, False):
        print(".on is True" if v else ".on is False (no colorizing)")
        u.on = v
        for i in u:
            t.print(f"{u[i]}{i} is this color")
    exit()

if __name__ == "__main__":  
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
        print("The following AttributeError shows the red key 'r' is gone")
        u.r
    Demo()
