if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Class to define constants in your scripts oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2026 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞

            - ∞∞1 
                - Add change() method, which lets you change a value and ignores the
                  setting of strict.  Raise an exception if the attribute doesn't exist.
                - Deleting an attribute should work if strict is False
                - Could raise AttributeError on trying to change an attribute
                - It could be handy to keep track of the file:line where the constant's
                  value was set, as if multiple modules use this module, there could be
                  conflicts or you'd want to see where the thing was first set.  This
                  might be enabled by setting the _Const.debug class variable to True.
                  When there's an exception, then the file:line information is included
                  in the exception so you see it on the traceback.

        oo>
    '''
    if 1:  # Standard imports
        import sys
        import threading
    if 1:  # Custom imports
        pass
if 1:   # Classes
    class _Const:
        '''Class to define constants
        Usage:
            import constant
            constant.speed = 47.1
        
        Trying to change C.speed later will result in an exception.  It's best to bind
        immutable objects to the constant name; if you e.g. bind a list, it will
        continue to be bound, but someone/something can change the list later.
        
        From page 193 of "Python Cookbook", the entry was by Alex Martelli.
        
        The instance uses the 'strict' property to raise an exception when you bind
        something that appears to be mutable if strict is True.  Set constant.strict to
        False to disable raising this exception.
        
        This class is a context manager and uses threading.Lock to protect access to its
        attributes during a with statement block.  This context manager is provide to
        let you do things like
        
            with constant as x:
                x.speed = 27
        
        Thus, inside the context manager the strict attribute is set to False, letting
        you change any of the constants.  This is a better paradigm than making the user
        remember to set strict to False, change the variable, then set strict to True
        again.
        '''
        def __init__(self):
            self.lock = None
            self.strict = True
            self.last_strict = self.strict  # Used for context management
        def __setattr__(self, name, value):
            if name == "lock":
                # This gives us the chance to create the lock
                self.__dict__["lock"] = threading.Lock()
                return
            self.lock.acquire()
            if name == "strict" or name == "last_strict":
                self.__dict__[name] = bool(value)
            else:
                if name in self.__dict__:
                    if self.strict:
                        self.lock.release()
                        raise ValueError(f"Can't change the constant '{name}'")
                    else:
                        self.__dict__[name] = value
                else:
                    if "strict" in self.__dict__ and self.strict:
                        try:
                            hash(value)
                        except TypeError:   # Was a mutable object
                            self.lock.release()
                            raise
                    self.__dict__[name] = value
            if "lock" in self.__dict__:
                self.lock.release()
        def __delattr__(self, name):
            if name in self.__dict__:
                raise ValueError(f"Can't delete the constant '{name}'")
            raise ValueError(f"No constant named '{name}'")
        def __enter__(self):
            self.lock.acquire()
            self.last_strict = self.strict
        def __exit__(self, exc_type, exc_val, exc_tb):
            self.strict = self.last_strict
            self.lock.release()
            # Return True if you want the with statement to suppress the exception and
            # continue execution.  Otherwise, the exception will continue propagating.
            # Here, any exceptions are passed on because this context manager's jobs are
            # to 1) make sure strict is set to what it was before the call and 2) to
            # acquire and release the lock appropriately.
            return True if exc_type is None else False
        def change(self, name, value):
            '''This method allows you to change the value of an attribute called name
            regardless of the value of strict.  The use case for this is that I feel
            this is a better way of doing it than setting strict to False, doing your
            work, then forgetting to set strict back to True.

            '''
            self.lock.acquire()
            self.lock.release()

    # The following allows you to add any instance as a module in the global namespace.
    # Here, __name__ is the name of this module, less the '.py'.
    sys.modules[__name__] = _Const()

if __name__ == "__main__":
    from lwtest import run, raises, Assert
    def Init():
        sys.modules[__name__] = _Const()
        return sys.modules[__name__]
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
        except ValueError:
            pass
        Assert(c.pi == a)
    def Test_not_strict():
        "Can set items to mutable objects without an exception"
        # Hashable objects cause a TypeError
        c = Init()

        # Why is there a problem with dict?
        #  - Lock acquired OK
        for i in ([], {}, set()):
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
        # Can't change if strict is True
        c.strict = True
        with raises(ValueError) as x:
            c.x = [6]
        # But can change the elements of the list.  If you really do need the constant
        # behavior, set the list to a tuple before setting strict back to True.
        c.x.append(4)
        Assert(c.x == [3, 4])
        # Can't set the c.x list to a tuple with strict True?
        with raises(ValueError) as x:
            c.x = tuple(c.x)
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
