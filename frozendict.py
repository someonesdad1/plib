'''
Class to make frozen dictionaries
    This code is derived from the routine by Oren Tirosh dated 16 May
    2005 at
    http://code.activestate.com/recipes/414283-frozen-dictionaries/.
    On 10 Jun 2021 the above link states that this code is licensed
    under the Python Software Foundation License.
    
    I downloaded this code on Fri 25 Jul 2014 04:53:59 PM and made the
    following modifications

        * Included the modification by Ero Carrera (in the above web
          page's comments) to get it to work with mutable contents.
        * Added some unit tests.
        * Changed the _blocked_attribute method to let things work with
          unittest.assertRaises.
        * Checked that a frozendict can be made from a defaultdict or
          OrderedDict.
        * The copy.copy() method in Carrera's code isn't necessary, as
          it's a shallow copy which can be done by dict.copy().
        * Unit tests are in /pylib/test/frozendict_test.py.  On 10 Jun
          2021 I moved the unit test code into this file.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Python Software License.
    #   See https://docs.python.org/3/license.html
    #∞license∞#
    #∞what∞#
    # <programming> Class to make frozen dictionaries
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
class frozendict(dict):
    def __init__(self, *args, **kw):
        pass
    def __new__(cls, *args, **kw):
        new = dict.__new__(cls)
        # It was pointed out that the original algorithm doesn't work
        # when one of the dictionary's elements is mutable.  Here's a
        # modification to change things to immutable objects.
        newargs = []
        for arg in args:
            if isinstance(arg, dict):
                arg = arg.copy()
                # Iterate over each element and change them to
                # immutable objects
                for key, value in arg.items():
                    if isinstance(value, dict):
                        arg[key] = frozendict(value)
                    elif isinstance(value, list):
                        new_values = list()
                        for element in value:
                            if isinstance(element, dict):
                                new_values.append(frozendict(element))
                            else:
                                new_values.append(element)
                        arg[key] = tuple(new_values)
                newargs.append(arg)
            else:
                newargs.append(arg)
        dict.__init__(new, *newargs, **kw)
        return new
    def __hash__(self):
        try:
            return self._cached_hash
        except AttributeError:
            items = self.items()
            # Soren Lovborg commented that a faster O(n) routine would
            # be the following:
            self._cached_hash = hash(frozenset(self.items()))
            return self._cached_hash
    def __repr__(self):
        return "frozendict(%s)" % dict.__repr__(self)
    def __str__(self):
        keys = str(self.keys()).replace("[", "").replace("]", "")
        return "frozendict(keys = %s)" % keys
    def _blocked_guts(self):
        raise AttributeError("A frozendict cannot be modified")
    def _blocked_attribute(self, *p, **kw):
        self._blocked_guts()
    __delitem__ = __setitem__ = clear = _blocked_attribute
    pop = popitem = setdefault = update = _blocked_attribute
if __name__ == "__main__": 
    if 1:   # Imports
        from collections import defaultdict, OrderedDict
    if 1:   # Custom imports
        from lwtest import run, assert_equal, raises, Assert
    if 1:   # Global variables
        mydict = {"a" : [1, 2], "b" : {1:2, 2:[3, 4]}}
        d = frozendict(mydict)
        hashvalue = hash(d)
    def Test_Hashable():
        # Check that a dict with two mutable objects can still be used
        # to construct a frozendict.
        mydict = {"a" : [1, 2], "b" : {1:2, 2:[3, 4]}}
        d = frozendict(mydict)
        assert(d == d)
        assert(d["a"] == (1, 2))
        assert(d["b"] == {1:2, 2:(3, 4)})
        assert(hash(d) == hashvalue)
    def Test_CannotBeModified():
        d = frozendict({})
        try:
            d[1] = 1
            raise SyntaxError("Modification was allowed")
        except AttributeError:
            pass
        raises(AttributeError, d.__setitem__, 1, 1)
    def Test_BlockedMethods():
        d = frozendict({1:1})
        raises(AttributeError, d.__delitem__, 1)
        raises(AttributeError, d.clear)
        raises(AttributeError, d.pop)
        raises(AttributeError, d.popitem)
        raises(AttributeError, d.setdefault, 1, 1)
        raises(AttributeError, d.update, {})
    def Test_WithDefaultDict():
        dd = defaultdict(int)
        dd[1] += 1
        dd[2] += 1
        d = frozendict(dd)
        assert(d[1] == 1)
        assert(d[2] == 1)
    def Test_WithOrderedDict():
        dd = OrderedDict()
        dd[1] = 1
        dd[2] = 1
        d = frozendict(dd)
        assert(d[1] == 1)
        assert(d[2] == 1)
    exit(run(globals(), regexp=r"Test_", halt=1)[0])
