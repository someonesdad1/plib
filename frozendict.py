'''
Class to make frozen dictionaries.

This code is derived from the routine by Oren Tirosh dated 16 May 2005
at http://code.activestate.com/recipes/414283-frozen-dictionaries/.
There was no license given, so I'm assuming it's OK to make a modified
copy.

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
    * Unit tests are in /pylib/test/frozendict_test.py.
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

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
