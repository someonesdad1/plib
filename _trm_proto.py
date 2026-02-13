'''

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
        - Trm is also a context manager to support the following behavior
        - self.stack is a deque of dictionaries that are saved when t.ppush() is called.
            - This lets you use the two patterns
                - Pattern 1:  Using ppush() and ppop()

                    mycolors # dict of keys = strings, value = Color instances or name
                            #strings that Color knows how to evaluate
                    t.ppush(mycolors)
                        # This makes the t instance push a dict of all its values onto the
                        # internal stack, then it updates itself with t.update(mycolors)
                    Do your tasks with the new colors
                    t.ppop()    # Restores the old color set

                - Pattern 2:  context manager

                    mycolors # dict of keys = strings, value = Color instances or name
                            #strings that Color knows how to evaluate
                    with t.uses(mycolors):
                        Do your tasks with the new colors

                    # In the context scope, all the colors in mycolors are usable.
                    # After the context manager scope exits, the old color set is being
                    # used again
                    
                - The context manager pattern is clean and understandable and it would
                  be my preferred method.  However, there are use cases where multiple
                  sets of color styles would be needed in sequential execution and the
                  stack pattern supports this.
                - Another way of supporting these patterns would be to have a
                  t.style(newstyle) method that lets you choose a new style.  You could 
                  use t.update(t.get(newstyle)) to merge the two styles, with the second
                  (newstyle) overwriting any existing keys.  This would be gotten by 
                  an attribute t.styles that's a dict storing the different styles.
        - I worry about multiple threads or processes using the same instance.  This
          would work OK if the instance was considered read-only.  The simplest pattern
          to support this is to have a Lock instance that gets used by any method that
          modifies the instance's data.  One approach is

            @contextmanager
            def locked(lock):
                lock.acquire()
                try:
                    yield
                finally:
                    lock.release()

            with locked(myLock):
                # Code here executes with myLock held.  The lock is
                # guaranteed to be released when the block is left (even
                # if via return or by an uncaught exception).

            - Question:  will a separate process block on a lock from threading?
              Probably, but it needs to be checked.
                    
The Trm class 

This is a class Trm that is a context manager that lets you do things like

    with Trm(names_dict) as p:
        print(f"{p.g}This is green, {p.y}yellow is to the end")

The pattern is that names_dict contains colorizing style names that translate from the
style name to the escape code.

Further, it internally contains a stack object to allow the methods 

    Trm.ppush(names_dict) 

        A copy of the current self dict is pushed onto the stack, then
        self.update(names_dict) is called so that the new names are added to the Trm
        instance or old ones updated.  If you don't want any of the old names in the
        Trm instance, call Trm.clear() just before calling palette_push().

    Trm.ppop()
        
        Makes a copy of the current dict and returns it to the caller.  The Trm
        instance's values are restored with the dict on the top of the stack.

    names_dict = Trm.palette_pop()

ppush() takes a dictionary of name to escape sequences (anything that's acceptable for
the Trm constructor) 
'''
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
        for i in self:
            u = self[i].strip()
            print(i, repr(u))
            if isinstance(u, str):
                if u[0] in "#$@":   # Hex format 
                    c = Color(u)
                elif u.endswith("nm"):  # Is a wavelength
                    wl_nm = float(u[:-2])
                    c = wl2rgb.wl2rgb(wl_nm)
                else:   # Float or integer
                    try:
                        x = abs(float(u))
                        fp, ip = math.modf(x)
                        c = Color(fp)
                    except Exception:
                        pass
                    i = dpmath.Int(u)
                    if not (0 <= i < 256):
                        raise ValueError("An integer i = {i} for a color must be on [0, 255]")
                    c = color.Translate8bit(j)
            elif isinstance(u, int):
                # It's an 8-bit color
                if not (0 <= u < 256):
                    raise ValueError("An integer i = {u} for a color must be on [0, 255]")
                c = color.Translate8bit(u)
            self[i] = self._get_code(c)
            print(f"{i} gave {self[i]}this color{t.n}")

    #yy
    def __setattr__(self, name, value):
        return dict.__setattr__(self, name, value)
    def __getattribute__(self, name):
        '''This allows you to access a dictionary key using the syntax self.key
        instead of self[key].  This is a useful shorthand for the Trm instance.
        It also lets us get to our other attributes that are not in the dict without
        infinite recursion.
        '''
        if name in self:
            return self[name]
        else:
            return dict.__getattribute__(self, name)
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
            if not self.on or color is None:
                return ""
            if not self.always and not sys.stdout.isatty():
                return ""
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
    styles = {
        "a": "orn",
        "b": Color("#ff8700"),   # 8-bit #208
        "c": 208,           # 8-bit #208
        "d": 0xd0,          # 8-bit #208
        "e": 0o320,         # 8-bit #208
        "f": 0b11010000,    # 8-bit #208
        "g": "#ff8700",     # 8-bit #208
        "h": "255 135 0",   # 8-bit #208
        "i": 0.5,           # float, middle gray
        "j": "555 nm",      # Yellow-green, most visible to eye
    }
    u = Trm(styles) 
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
