'''
This module lets you define constants
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Module to define constants
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
if 1:   # Imports
    import sys
if 1:   # Custom imports
    from wrap import dedent
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
    from lwtest import run, raises, assert_equal, Assert
    from pdb import set_trace as xx 
    from pprint import pprint as pp
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
        'Can set items to mutable objects without an exception'
        c, T = Init(), ([], {}, set())
        for i in T:
            with raises(TypeError):
                c.x = i
        c = Init()
        c.strict = False 
        c.x = [1]
        c.y = {1:1}
        c.z = set([1])
        # Note we can change contents
        c.x[0] = 2
        c.y[1] = 2
        c.z.add(3)
        # Can't change what's already set
        with raises(ValueError):
            c.x = [3]
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
