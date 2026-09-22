'''
Debug printing messages

    Dbg:  utility debugging messages (convenience instance of class Debug)
    Debug:  Debug message class
    Bug:  bug reminder; only prints once per location

    These message can be put into code (and left in if you wish).  When there's a
    problem, set Dbg.on to True and you'll see the Dbg messages after that point.  

    Here's how to use the methods:

        from dbg import Dbg, Bug
        Dbg.on = True               # Turn debug printing on
        Dbg.stream = sys.stderr     # stdout is default
        Dbg("This is a debugging message")  # Same syntax as print()
            -> 'DBG [file.py:123]: This is a debugging message'
        Bug("Remember this bug")    # Always printed; same syntax as print()
            -> 'BUG [file.py:123]: Remember this bug'

    Use case:  for developing code, you can sprinkle Dbg() calls throughout your code
    and leave them in place.  There's not much overhead, as if Dbg.on is False, the code
    quickly exits.  At some point in your code's execution where a problem is occuring,
    set Dbg.on to True and you'll start seeing the debug messages, letting you see how
    the state of things changes over time.

'''
if 1:  # Header
    if 1:  # Standard imports
        import inspect
        import os
        import sys
    if 1: # Custom imports
        try:
            import trm
            _have_trm = True
        except Exception:
            _have_trm = False
    if 1: # Global variables
        if _have_trm:
            # Print messages colorized
            t = trm.TrmDP()
        else:
            # Use a class to swallow colorizing commands
            class T:
                def __setattr__(self, value):
                    pass
                def __getattr__(self, name):
                    return ""
                def __call__(self, *args, **kw):
                    return ""
            t = T()
        __all__ = "Dbg Bug".split()
    if 1:   # File gist information
        __gist__      = "Debug printing"
        __copyright__ = "Copyright © 2026 Don Peterson"
        __license__   = "MIT License (see /plib/_lic.mit)"
        __test__      = "notest"
        __history__   = ''' '''
        __category__  = "utility"
        __todo__      = ''' '''
if 1:  # Core functionality
    class Debug:
        '''A debugging print class with a __call__ method with the same syntax as print()
        Usage:
            Dbg = Debug()
            Dbg.on = True
            ...
            Dbg("Here's a debugging message")
                -> Message printed to stdout with file:line_number
        '''
            
        def __init__(self, 
                     file: str = sys.stdout,    # Where output is sent
                     color: str = "",           # Color escape sequence for print color
                     header: str = "DBG",       # Leading string message
                     show_file: bool = False,   # Show file in message
                     show_linenum: bool = True, # Show line number in message
                     on: bool = False):         # If True, output sent to stream
            self.file = file
            self.color = color
            self.header = header
            self.show_file = show_file
            self.show_linenum = show_linenum
            self.on = on
        def __call__(self, *p, **kw):
            if not self.on:
                return
            # Get file & line number for calling point from stack
            frame = inspect.stack()[1]
            fi = os.path.basename(frame.filename)
            ln = frame.lineno
            # Construct debugging header string
            hdr = ""
            if self.color:
                hdr += f"{self.color}"
            if self.header:
                hdr += f"{self.header} "
            if self.show_file or self.show_linenum:
                f = fi if self.show_file else ""
                l = ln if self.show_linenum else ""
                c = ":" if f and l else ""
                hdr += f"[{f}{c}{l}]: "
            # Output the header string
            print(f"{hdr}", end="", file=self.file)
            # Print the user's information
            print(*p, **kw)
            if self.color:
                print(f"{t.n}", end="", file=self.file)

    # Convenience instance
    Dbg = Debug()

    def Bug(*p, **kw):
        '''Print a bug you want to remember
        Only print it once for each call at a specific file and line number so you're not
        inundated with messages.  Printed in a very visible color.
        '''
        if not hasattr(Bug, "buglist"):
            Bug.buglist = set()
        frame = inspect.stack()[1]
        fi = os.path.basename(frame.filename)
        ln = frame.lineno
        if (fi, ln) not in Bug.buglist:
            print(f"{t.ygr}BUG [{fi}:{ln}]: ", end="")
            t.print(*p, **kw)
            Bug.buglist.add((fi, ln))

if __name__ == "__main__":
    # Demo
    print("Normal message using print()")
    Dbg("You shouldn't see this message")
    Dbg.on = True
    Dbg("You should see this message")
    Dbg(f"{t.grn}Here's a debug message in color{t.n}")
    # Here's how to get a Dbg printer in a specific color of text
    db = Debug(color=t.skyl)
    db.on = True
    db("A different Debug instance in color")
    print("Another normal message using print()")
    for i in range(5):
        Bug("You should see this Bug message, but only once")
    
