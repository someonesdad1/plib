if 1:  # Header
    if 1:  # Standard imports
        import sys
        import threading
    if 1:  # Custom imports
        pass
if 1:   # Classes
    class Constant:
        '''Class to define constants: 
        
            import constant as C
            C.speed = 47.1
        
        Trying to change C.speed later to a new value will result in an exception.

        You can change the value later using

            with C:
                C.speed = 42
        
        or 
            C.strict = False
            C.speed = 42
            C.strict = True

        It's best to bind immutable (hashable) objects to the constant name.  If you
        e.g. bind a list or dict, it will continue to be bound, but someone/something
        can change the list/dict later, so it's not really a constant.

        Based on a nice idea by Alex Martelli on page 193 of the "Python Cookbook".
        '''
        def __init__(self):
            self.lock = None
            self.strict = True
            self.last_strict = self.strict  # Used for context management
        def __setattr__(self, name, value):
            if name == "lock":
                self.__dict__[name] = threading.Lock()
                return
            if not self.lock.locked():
                self.lock.acquire()
            if name == "strict" or name == "last_strict":
                self.__dict__[name] = bool(value)
            else:
                if name in self.__dict__:
                    if self.strict:
                        if self.lock.locked():
                            self.lock.release()
                        raise AttributeError(f"Can't change the constant '{name}'")
                    else:
                        self.__dict__[name] = value
                else:
                    if "strict" in self.__dict__ and self.strict:
                        try:
                            hash(value)
                        except TypeError:   # value is a mutable object
                            if self.lock.locked():
                                self.lock.release()
                            raise
                    # It's hashable or strict is False, so we can add it
                    self.__dict__[name] = value
            if "lock" in self.__dict__ and self.lock.locked():
                self.lock.release()
        def __delattr__(self, name):
            if name in self.__dict__:
                if self.strict:
                    raise AttributeError(f"Can't delete the constant '{name}'")
                else:
                    del self.__dict__[name]
                    return
            raise AttributeError(f"No constant named '{name}'")
        def __enter__(self):
            self.last_strict = self.strict
            self.strict = False     # The constant can now be changed
            if not self.lock.locked():
                self.lock.acquire()
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):
            if self.lock.locked():
                self.lock.release()
            self.strict = self.last_strict
            # Return True if you want the with statement to suppress the exception and
            # continue execution.  Otherwise, the exception will continue propagating.
            # Here, any exceptions are passed on because this context manager's jobs are
            # to 1) make sure strict is set to what it was before the call and 2) to
            # acquire and release the lock appropriately.
            return True if exc_type is None else False
    def MakeGlobal():
        '''If you call this function, an instance of Constant gets added to the global
        namespace and python code can access it with 'import constant'.  Personally, I
        don't think this is a good idea by default, so this function needs to be called
        to put it into the global namespace.
        '''
        # Here, __name__ is the name of this module, less the '.py'.
        sys.modules[__name__] = Constant()

if __name__ == "__main__":
    from lwtest import run, raises, Assert
    from collections import deque
    def Init():
        # Guarantee a "fresh" instance
        c = Constant()
        return c 
    def Test_can_change_strict_property():
        c = Init()
        # Default value of strict is True
        Assert(c.strict)
        c.strict = False
        Assert(not c.strict)
    def Test_is_constant():
        c = Init()
        c.pi = 3.14
        # OK to change if strict not True
        c.strict = False
        a = 4.14
        c.pi = a
        Assert(c.pi == a)
        # Not OK to change if strict is True
        c.strict = True
        try:
            c.pi = 3.14
            raise Exception("Shouldn't reach this point")
        except AttributeError:
            pass
        Assert(c.pi == a)
    def Test_not_strict():
        'Can set items to mutable objects without an exception'
        # Nonhashable objects cause a TypeError
        c = Init()
        for i in ([], {}, set(), deque([])):
            with raises(TypeError):
                c.x = i
        # If strict is False, then OK to store hashable items
        c = Init()
        c.strict = False
        c.x = [1]
        c.y = {1: 1}
        c.z = set([1])
        # Note we can change contents
        c.x[0] = 2
        c.y[1] = 2
        c.z.add(3)
        # Can change what's already set
        c.x = [3]
        if 1:   # Can't change if strict is True
            c.strict = True
            with raises(AttributeError):
                c.x = [6]
            # But can change the elements of the list.  If you really do need the constant
            # behavior, set the list to a tuple before setting strict back to True.
            c.x.append(4)
            Assert(c.x == [3, 4])
            # Can't set the c.x list to a tuple with strict True?
            with raises(AttributeError):
                c.x = tuple(c.x)
    def Test_Delete():
        c = Init()
        c.strict = True
        c.speed = 42
        c.velocity = 43
        try:
            del c.speed     # Doesn't work
            raise Exception("Shouldn't reach this point")
        except AttributeError:
            pass
        # Now try it with the context manager
        with c:
            del c.speed     # Works
        Assert(not hasattr(c, "speed"))
        # Delete velocity by setting strict to False
        c.strict = False
        del c.velocity
        Assert(not hasattr(c, "velocity"))
    def Test_ContextManager():
        c = Init()
        c.speed = 42
        c.strict = True
        # The speed attribute is read-only.  However, if we put it in a context manager
        # block, the values can be changed.
        with c as x:
            x.speed = 21
        # That showed that we could make the change and that the context manager returns
        # the _Const instance as x
        Assert(c.speed == 21)
        Assert(c.strict)    # The strict value was restored
    exit(run(globals(), regexp=r"Test_", halt=1)[0])

def GetGist():
    g = {}
    g["gist"] = "Class to define constants in your scripts"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "utility"
    g["todo"] = '''

        - ∞∞3 Keeping track of [file:line]
            - It could be handy to keep track of where the constant's value was set
                or changed
            - Use debug.fln() to get the string and store it in a dict indexed by
                the attribute name
            - Or make it a derived class with this feature
    
    '''
    return g
