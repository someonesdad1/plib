'''

Vision
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
                    
The Palette class 

This is a class Palette that is a context manager that lets you do things like

    with Palette(names_dict) as p:
        print(f"{p.g}This is green, {p.y}yellow is to the end")

The pattern is that names_dict contains colorizing style names that translate from the
style name to the escape code.

Further, it internally contains a stack object to allow the methods 

    Palette.ppush(names_dict) 

        A copy of the current self dict is pushed onto the stack, then
        self.update(names_dict) is called so that the new names are added to the Palette
        instance or old ones updated.  If you don't want any of the old names in the
        Palette instance, call Palette.clear() just before calling palette_push().

    Palette.ppop()
        
        Makes a copy of the current dict and returns it.  The Palette instance's values
        are restored with the dict on the top of the stack.

    names_dict = Palette.palette_pop()

spush() takes a dictionary of name to escape sequences (anything that's acceptable for
the Palette constructor) 
'''
from stack import Stack

class Palette(dict):
    def __init__(self, names_dict):
        self.stack = Stack()
        super().__init__(names_dict)
    def __getattribute__(self, name):
        return self[name]
    def __enter__(self):
        # Returning self lets the code inside the calling manager have access to this
        # instance's attributes and methods
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is None or exc_type is TypeError:
            return True     # Ignore this exception
        else:
            return False    # Don't ignore this exception

if __name__ == "__main__":  
    from color import t
    styles = {"y": t.yell, "g": t.grnl, "n": t.n}
    # Demonstrate this works
    with Palette(styles) as p:
        print("The following demonstrates normal dictionary access to colors:")
        print(f"  This is {p['g']}green, {p['y']}yellow is to the end{p['n']}")
        print("The following demonstrates attribute access to colors:")
        print(f"  This is {p.g}green, {p.y}yellow is to the end{p.n}")
        if 0:
            raise ValueError("Raised inside context manager")
        else:
            raise TypeError("Raised inside context manager")
    print("Outside the context manager")
