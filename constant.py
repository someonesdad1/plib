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

            - ∞∞1 The strict attribute should see if the added constant is hashable, as
              this should catch the needed problematic things (e.g., a deque isn't in
              the list of items that should be checked)

        oo>
    '''
    if 1:  # Standard imports
        import sys
    if 1:  # Custom imports
        pass
if 1:   # Classes
    class _Const:
        '''Class to define constants
        Usage:
            import constant
            constant.speed = 47.1
        Trying to change C.speed later will result in an exception.  It's
        best to bind immutable objects to the const name; if you e.g. bind a
        list, it will continue to be bound, but someone/something can change
        the list later.
        
        From page 193 of "Python Cookbook" (by Alex Martelli).
        
        The instance uses the 'strict' property to raise an exception when
        you bind something that appears to be mutable if strict is True.
        Set constant.strict to False to disable raising this exception.
        '''
        def __init__(self):
            self.strict = True
        def __setattr__(self, name, value):
            if name in self.__dict__ and name != "strict":
                raise ValueError(f"Can't change the constant '{name}'")
            if name not in self.__dict__ and name == "strict":
                self.__dict__["strict"] = bool(value)
                return
            if self.strict and isinstance(value, (dict, list, set)):
                raise TypeError("value is a mutable object")
            self.__dict__[name] = value
        def __delattr__(self, name):
            if name in self.__dict__:
                raise ValueError(f"Can't delete the constant '{name}'")
            raise ValueError(f"No constant named '{name}'")
    sys.modules[__name__] = _Const()

if __name__ == "__main__":
    from lwtest import run, raises, Assert
    def Init():
        sys.modules[__name__] = _Const()
        return sys.modules[__name__]
    def Test_can_change_strict_property():
        c = Init()
        Assert(c.strict)
        c.strict = False
        Assert(not c.strict)
    def Test_is_constant():
        c = Init()
        c.pi = 3.14
        for i in (False, True):
            c.strict = i
            with raises(ValueError):
                c.pi = 3.14
    def Test_not_strict():
        "Can set items to mutable objects without an exception"
        c, T = Init(), ([], {}, set())
        for i in T:
            with raises(TypeError):
                c.x = i
        c = Init()
        c.strict = False
        c.x = [1]
        c.y = {1: 1}
        c.z = set([1])
        # Note we can change contents
        c.x[0] = 2
        c.y[1] = 2
        c.z.add(3)
        # Can't change what's already set
        with raises(ValueError):
            c.x = [3]
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
