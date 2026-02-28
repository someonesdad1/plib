'''

dptypes is a module that contains various types:
    - SlushDict:  a hashable dictionary (use with care)
    - Bidict:  a dictionary that's an invertible function

'''
if 1:   # Header
    if 0:   # Standard imports
        pass
    if 0:   # Custom imports
        pass
if 1:   # class SlushDict:  a dictionary that is hashable (use with care)
    class FrozenError(Exception):
        pass
    class SlushDict(dict):
        '''Dictionary that is frozen after the constructor call.  You can unfreeze it by
        using a context manager idiom.
            di = SlushDict({"one": 1})
            di["one"] --> returns 1
            di["one"] = 4   --> raises a FrozenError exception
        Change with a context manager:
            with di:
                di["one"] = 4   # This change works
        The concept of a frozen dictionary has been added to the plans for python 3.15.
        Until then, use this class with care, knowing about the problems of storing hashable
        items in the data structure.  For a slightly more bullet-resistance implementation,
        you can wrap a dict in a types.MappingProxyType.
        '''
        def __init__(self, *p, **kw):
            '''Initialize with the standard dictionary initializers.  After this method
            returns, the instance can't be modified unless the context manager is used.
            '''
            self._frozen = False    # If True, instance can't be modified
            super().__init__(*p, **kw)
            self._frozen = True
        def __setitem__(self, name, value):     # Set self[name]
            'Set self[key] to value if self._frozen is False'
            if self._frozen:
                raise FrozenError("Instance is frozen")
            super().__setitem__(name, value)
        def __setattr__(self, name, value):     # Set an attribute
            if name == "_frozen":
                super().__setattr__("_frozen", bool(value))
            else:
                raise AttributeError(f"'SlushDict' has no attribute {name!r}")
        def __getattribute__(self, name):   
            if name in self:
                return self.__getitem__(name)
            elif name == "_frozen":
                return super().__getattribute__(name)
            else:
                funcs = set("clear pop popitem setdefault update".split())
                if name in funcs and self._frozen:
                    raise FrozenError("Instance is frozen")
                return super().__getattribute__(name)
        def __enter__(self):    # Context manager entry
            self._frozen = False
            return self
        def __exit__(self, exc_type, exc_val, exc_tb):  # Context manager exit
            self._frozen = True
            if exc_type is None or exc_type is TypeError:
                return True     # Ignore this exception
            else:
                return False    # Don't ignore this exception
        def __delitem__(self, name):
            'Needed for "del self[x]"'
            if self._frozen:
                raise FrozenError("Instance is frozen")
            super().__delitem__(name)
        def __hash__(self):
            '''Normally, a dict can't be hashed, but the SlushDict can by virtue of this
            method.  The returned value is the hash of the tuple of keys.  The use case is
            that this allows the SlushDict to be considered immutable, so it can be included
            in e.g. a set.  You as the programmer using this data type will know that the
            concept of immutability here entirely depends on how the structure is used.  If 
            you use values that are mutable, the structure will inherently be mutable
            because some code or thread may be able to change it at some time.  So, use this
            pseudo-immutability with care.
            '''
            return hash(tuple(self.keys()))
        if 0:
            def pop(self, name, default=None):
                if self._frozen:
                    raise FrozenError("Instance is frozen")
                super().pop(name, default=default)
            def popitem(self):
                if self._frozen:
                    raise FrozenError("Instance is frozen")
                super().popitem()
            def setdefault(self, name, default=None):
                if self._frozen:
                    raise FrozenError("Instance is frozen")
                super().setdefault(name)
            def update(self, *p, **kw):
                if self._frozen:
                    raise FrozenError("Instance is frozen")
                super().update(*p, **kw)
if 1:   # class Bidict:  A dictionary that is an invertible function
    class Bidict(dict):
        '''A dictionary that is an invertible function
            Keys and values must be unique in "both directions".  Call the instance
            as if it were a function to go in the reverse direction.

            Example:
            
            Here's how to initialize from a dict:
                categories = Bidict()
                categories.update(
                    {
                        'all':      0,
                        'gas':      1,
                        'liquid':   2,
                        'metal':    3,
                        'mineral':  4,
                        'misc':     5,
                        'plastic':  6,
                        'wood':     7,
                    }
                )
                
            Then
                categories["metal"] returns 3
                categories(3) returns "metal"
                
            Use categories.invert() to get a new Bidict object where the inverse
            mapping is the "forward" mapping.
        '''
        def __init__(self, *p, **kw):
            # Implementation:  keep the inverse mapping in self._inv.
            self.super = super(Bidict, self)
            self.super.__init__(*p, **kw)
            self._inv = {}
            self._frozen = kw.get("frozen", False)
            # Construct the inverse mapping
            for key in self:
                value = self[key]
                try:
                    if value in self._inv:
                        raise ValueError("'%s' is a duplicate value" % value)
                except TypeError:
                    # Probably a mutable object
                    raise TypeError("Can't put '%s' into a Bidict" % value)
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
            "Return the key that corresponds to value."
            return self._inv[value]
        def _check(self):
            if self._frozen:
                raise ValueError("Bidict is frozen")
        def clear(self):
            self._check()
            self.super.clear()
            self._inv.clear()
        def invert(self):
            '''Return a new Bidict object that has the dictionaries
            reversed.
            '''
            b = Bidict(self._inv)
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
            b = Bidict()
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
            return "".join(("Bidict", self.super.__str__()))
        def _set_frozen(self, frozen):
            self._frozen = bool(frozen)
        def _get_frozen(self, frozen):
            return self._frozen
        frozen = property(_get_frozen, _set_frozen)

if __name__ == "__main__":  
    import sys
    import lwtest
    run = lwtest.run
    Assert = lwtest.Assert
    raises = lwtest.raises
    def Demo():
        breakpoint() # ∞∞
    if 1:   # SlushDict tests
        def Test_SlushDict():
            k, v, v1, v2 = "three", 0, 42, 83189
            def Init():
                return SlushDict({k: v})
            if 1:   # Demonstrate core behavior
                # Test the three methods of constructing a dict
                d = SlushDict({k: v})       # Create from an existing dict
                Assert(d[k] == v and d == Init())
                tuples = ((k, v), )
                d = SlushDict(tuples)       # Create from tuples
                Assert(d[k] == v and d == Init())
                d = SlushDict(three=v)      # Create from keywords
                Assert(d[k] == v and d == Init())
            if 1:   # Show normal dict changing methods don't work
                d = Init()
                with raises(FrozenError):
                    d[k] = 42
                with raises(FrozenError):
                    del d[k]
                with raises(FrozenError):
                    d.clear()
                with raises(FrozenError):
                    d.pop(k)
                with raises(FrozenError):
                    d.popitem()
                with raises(FrozenError):
                    d.setdefault(k, 88)
                with raises(FrozenError):
                    d.update({k: 42})
            if 1:   # But you can change the dict in a context manager
                # Normal assignment
                d = Init()
                with d:
                    d[k] = 42
                Assert(d[k] == 42)
                # Delete an item
                d = Init()
                with d:
                    del d[k]
                Assert(not d)
                # Clear the dict
                d = Init()
                with d:
                    d.clear()
                Assert(not d)
                # Pop the item keyed by k
                d = Init()
                with d:
                    d.pop(k)
                Assert(not d)
                # popitem
                d = Init()
                with d:
                    d.popitem()
                Assert(not d)
                # setdefault
                k1 = "four"
                d = Init()
                with d:
                    d.setdefault(k1)
                Assert(d[k1] is None)
                d = Init()
                v1 = 83189
                with d:
                    d.setdefault(k1, v1)
                Assert(d[k1] is v1)
                # update
                d = Init()
                with d:
                    d.update({k1: v1})
                Assert(d[k] == v)
                Assert(d[k1] == v1)
            if 1:   # Show you can get a hash
                d = Init()
                hash(d)     # No exception
                set(d)      # No exception
    if 1:   # Bidict tests
        def Bidict_init():
            keys, values = ["jan", "feb"], [1, 2]
            d = dict(zip(keys, values))
            bd = Bidict(d)
            BidictCheck(bd, keys, values)
            return keys, values, bd
        def BidictCheck(bd, keys, values):
            assert isinstance(bd, Bidict)
            for i in bd:
                assert i in keys
            for i in bd.values():
                assert i in values
            assert set(bd.keys()) == set(bd._inv.values())
            assert set(bd.values()) == set(bd._inv.keys())
        def Test_Bidict_Lookup():
            keys, values, bd = Bidict_init()
            assert bd["jan"] == 1
            assert bd(1) == "jan"
        def Test_Bidict_KeysAndValues():
            keys, values, bd = Bidict_init()
            assert set(values) == set(bd.values())
            assert set(keys) == set(bd.keys())
        def Test_Bidict_AddDeleteNewValue():
            keys, values, bd = Bidict_init()
            bd["mar"] = 3
            keys.append("mar")
            values.append(3)
            BidictCheck(bd, keys, values)
            # Show we can delete it
            del bd["mar"]
            del keys[-1]
            del values[-1]
            BidictCheck(bd, keys, values)
        def Test_Bidict_SwapDictionaries():
            keys, values, bd = Bidict_init()
            rev_bd = bd.invert()
            BidictCheck(rev_bd, values, keys)
        def Test_Bidict_Methods():
            keys, values, bd = Bidict_init()
            assert set(bd.items()) == set(zip(keys, values))
            assert "jan" in bd
            assert bd.get("xyz", 88) == 88
            assert bd.get("jan", None) == 1
            b2 = bd.copy()
            assert bd == b2  # Can be tested for equality
            b2.clear()
            assert not len(b2)
            b2 = bd.copy()
            assert b2.setdefault("jun", 89) == 89
            assert b2.setdefault("jun") == 89
            # assert(set(bd.iterkeys()) == set(bd.keys()))
            # assert(set(bd.itervalues()) == set(bd.values()))
            value = b2.pop("jun")
            assert value == 89
            # Get exception on empty pops
            raises(KeyError, b2.pop, "xyz")
            raises(KeyError, b2.pop, "jun")
            # Show default value for pop works
            value = b2.pop("jun", 91)
            assert value == 91
            key, value = b2.popitem()
            assert len(b2) == 1
            # Get ValueError exception for a duplicate value
            raises(ValueError, bd.__setitem__, "xyz", 2)
            # Get key error for accessing nonexistent key
            raises(KeyError, b2.__getitem__, "xyz")
            # Get key error for accessing nonexistent value
            raises(KeyError, b2, 1000)
        def Test_Bidict_CannotUseMutableObject():
            keys, values, bd = Bidict_init()
            d = dict([("jan", [1])])
            raises(TypeError, Bidict, d)
            # OK to use a tuple
            d = dict([("jan", (1,))])
            Bidict(d)
        def Test_Bidict_Update():
            keys, values, bd = Bidict_init()
            # Update with dict
            d = {"new": 24}
            bd.update(d)
            assert bd["new"] == 24
            assert bd(24) == "new"
            # Update with key/value pair iterable
            keys, values, bd = Bidict_init()
            d = [("new", 24)]
            bd.update(d)
            assert bd["new"] == 24
            assert bd(24) == "new"
            # Update with keywords
            keys, values, bd = Bidict_init()
            bd.update(new=24)
            assert bd["new"] == 24
            assert bd(24) == "new"
            # TypeError if update with mutable
            keys, values, bd = Bidict_init()
            d = {"new": [1, 2]}
            raises(TypeError, bd.update, d)
        def Test_Bidict_Frozen():
            keys, values, bd = Bidict_init()
            bd.frozen = True
            with raises(ValueError):
                del bd["jan"]
    if len(sys.argv) > 1:
        Demo()
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

def GetGist():
    g = {}
    g["gist"] = "Various useful types"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "programming"
    g["todo"] = ''' '''
    return g
