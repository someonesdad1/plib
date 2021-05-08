'''
A dictionary that is an invertible function
'''

# Copyright (C) 2009, 2011, 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

class bidict(dict):
    '''A bidict is a dictionary that is an invertible function (a
    discrete bijective function).
 
    Typical use:
        >>> b = bidict()
        >>> b[1] = 2
        >>> b[2] = 3
        >>> print(b[2]) # Normal dictionary access
        3
        >>> print(b(2)) # Consider values as keys ("go in other direction")
        1
 
    Use b.invert() to get a new bidict object where the inverse mapping
    is the "forward" mapping.
    '''
    def __init__(self, *p, **kw):
        # Implementation:  keep the inverse mapping in self._inv.
        self.super = super(bidict, self)
        self.super.__init__(*p, **kw)
        self._inv = {}
        self._frozen = kw.get("frozen", False)
        # Construct the inverse mapping
        for key in self:
            value = self[key]
            try:
                if value in self._inv:
                    raise ValueError("'%s' is a duplicate value" % value)
            except TypeError as e:
                # Probably a mutable object
                raise TypeError("Can't put '%s' into a bidict" % value)
            self._inv[value] = key
    def __setitem__(self, key, value):
        self._check()
        if value in self._inv:
            raise ValueError("'%s' is duplicate value" % value)
        self.super.__setitem__(key, value)
        self._inv[value] = key
    def __delitem__(self, key):
        self._check()
        value = self[key]
        self.super.__delitem__(key)
        del self._inv[value]
    def __call__(self, value):
        'Return the key that corresponds to value.'
        return self._inv[value]
    def _check(self):
        if self._frozen:
            raise ValueError("bidict is frozen")
    def clear(self):
        self._check()
        self.super.clear()
        self._inv.clear()
    def invert(self):
        '''Return a new bidict object that has the dictionaries
        reversed.
        '''
        b = bidict(self._inv)
        b._inv = dict(self)
        return b
    def pop(self, key, default=None):
        self._check()
        if key in self:
            value = self.super.pop(key)
            del self._inv[value]
            return value
        if default is None:
            raise KeyError("No entry for key '%s'" % key)
        else:
            return default
    def popitem(self):
        self._check()
        key, value = self.super.popitem()
        del self._inv[value]
        return key, value
    def copy(self):
        b = bidict()
        b.super.update(self.super.copy())
        b._inv = self._inv.copy()
        return b
    def setdefault(self, key, default=None):
        self._check()
        if key not in self:
            self[key] = default
        return self[key]
    def update(self, *p, **kw):
        self._check()
        if p:
            if len(p) != 1:
                raise ValueError("Only one parameter allowed")
            if kw:
                msg = "Keyword parameters not allowed with a parameter"
                raise ValueError(msg)
            items = p[0].items() if isinstance(p[0], dict) else p[0]
        elif kw:
            items = kw.items()
        else:
            raise ValueError("Need a parameter or keyword arguments")
        for key, value in items:
            if value in self:
                raise ValueError("'%s' is a duplicate value" % value)
            self[key] = value
            self._inv[value] = key
    def __str__(self):
        return ''.join(("bidict", self.super.__str__()))
    def _set_frozen(self, frozen):
        self._frozen = bool(frozen)
    def _get_frozen(self, frozen):
        return self._frozen
    frozen = property(_get_frozen, _set_frozen)

# Convenience instance that maps month names to number and vice versa
months = bidict(zip("jan feb mar apr may jun jul aug sep oct nov dec".split(),
                    range(1, 13)))
