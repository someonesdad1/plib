'''
Debug printing messages

    Dbg:  utility debugging messages
    Bug:  bug reminder; only prints once per location

    from dbg import Dbg, Bug
    Dbg.on = True               # Turn debug printing on
    Dbg.stream = sys.stderr     # stdout is default
    Dbg("This is a debugging message")  # Same syntax as print()
        -> '[file.py:123]:DBG This is a debugging message'
    Bug("Remember this bug")    # Always printed; same syntax as print()
        -> '[file.py:123]:BUG Remember this bug'

    The t instance is a trm.TrmDP() instance which provides color printing to the
    terminal; the functions should still work if 'import trm' fails for some reason.
    Here's how to output a message in a yellow color:

        Dbg(f"{t.yel}This message is in color")

    The DBG and file/line number portion won't be colorized.

    Use case:  for developing code, you can sprinkle Dbg() calls throughout your code
    and leave them in place.  There's not much overhead, as if Dbg.on is False, the code
    quickly exits.  At some point in your code's execution where a problem is occuring,
    set Dbg.on to True and you'll start seeing the debug messages, letting you see how
    the state of things changes over time.  If you redirect to a file, the colorizing
    escape sequences won't be emitted; if you want them to be there, set t.always to
    True.

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
    def Dbg(*p, **kw):
        '''Simple debugging command with the same syntax as print
        Attributes:
            .on     Set to True to see the messages
        '''
        if not hasattr(Dbg, "on"):
            Dbg.on = False
        if not Dbg.on:
            return
        frame = inspect.stack()[1]
        fi = os.path.basename(frame.filename)
        ln = frame.lineno
        print(f"DBG [{fi}:{ln}]: ", end="")
        print(*p, **kw)
    def Bug(*p, **kw):
        '''Print a bug you want to remember
        Only list it once for each call at a specific file and line number so you're not
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
    # Dbg demo
    Dbg("You shouldn't see this message")
    Dbg.on = True
    Dbg("You should see this message")
    for i in range(10):
        Bug("You should see this Bug message, but only once")
    
