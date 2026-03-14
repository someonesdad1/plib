'''
    
dptypes is a module that contains utility types:
    - Bidict:  a dictionary that's an invertible function
    - CommandDecode:  Decode user command strings
    - Constant:  Define runtime constants
    - SlushDict:  a hashable dictionary (use with care)
    
'''
if 1:   # Header
    if 1:   # Standard imports
        import collections
        import multiprocessing
        import re
        import threading
    if 1:   # Custom imports
        pass
    if 1:   # Import symbols
        defaultdict = collections.defaultdict
        deque = collections.deque
        MultiprocessingLock = multiprocessing.Lock
        ThreadingLock = threading.Lock
    if 1:   # Global variables
        pass
if 1:   # class Bidict:  A dictionary that is an invertible function
    class Bidict(dict):
        '''A dictionary that is an invertible function (a bijection).
            Keys and values must be unique in "both directions".  Call the instance
            as if it were a function to go in the reverse direction.
                Example:
                    dict = {"solid": 0, "liquid": 1, "gas": 2}
                    categories = Bidict(dict)
                Then
                    categories["liquid"] returns 1
                    categories(1) returns "liquid"
            Use categories.invert() to get a new Bidict object where the inverse
            mapping is the "forward" mapping.
        '''
        def __init__(self, *p, **kw):
            # Implementation:  keep the inverse mapping in self._inv.
            self.super = super()
            self.super.__init__(*p, **kw)
            self._inv = {}
            self._frozen = kw.get("frozen", False)
            # Construct the inverse mapping
            for key in self:
                value = self[key]
                try:
                    if value in self._inv:
                        raise ValueError(f"{value!r} is a duplicate value")
                except TypeError as e:
                    # Probably a mutable object
                    raise TypeError(f"Can't put {value!r} into a Bidict") from e
                self._inv[value] = key
        def __setitem__(self, key, value):
            self._check()
            if value in self._inv:
                raise ValueError(f"{value!r} is duplicate value")
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
                raise KeyError(f"No entry for key {key!r}")
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
                    raise ValueError(f"{value!r} is a duplicate value")
                self[key] = value
                self._inv[value] = key
        def __str__(self):
            return "".join(("Bidict", self.super.__str__()))
        def _set_frozen(self, frozen):
            self._frozen = bool(frozen)
        def _get_frozen(self, frozen):
            return self._frozen
        frozen = property(_get_frozen, _set_frozen)
if 1:   # class CommandDecode:  Decode user command strings
    class CommandDecode:
        '''Decode user command strings, even if they are incomplete.
        Instantiate the class with a sequence of command strings.  Then call the object
        with a command candidate; the returned list will have either 0, 1, or multiple
        commands that matched.
        '''
        def __init__(self, commands, ignore_case=False):
            '''commands is a sequence that contains a unique set of strings.
            If you set ignore_case to True, then the commands will all be
            converted to lower case; if this lower-case set doesn't contain
            the same number of elements as commands, then you'll get a
            ValueError.
            '''
            self.ignore_case = ignore_case
            # See if we can convert commands to a set
            try:
                c = set(commands)
                if len(c) != len(commands):
                    raise ValueError("commands container has replicates")
            except TypeError as e:
                raise ValueError("commands must be a sequence of strings") from e
            if not c:
                raise ValueError("commands must contain at least one command")
            if ignore_case:
                self.commands = set([i.lower() for i in c])
                if len(self.commands) != len(commands):
                    msg = "Some commands are not unique after conversion to lower case"
                    raise ValueError(msg)
            else:
                self.commands = c
            self.commands.discard("")   # Get rid of empty string
            # Build index dictionary; each key is the first letter of the
            # command and each element is a list of commands that have that
            # first letter.
            self.index = defaultdict(list)
            for cmd in self.commands:
                first_char = cmd[0]
                self.index[first_char].append(cmd)
            self.first_char_list = self.index.keys()
        def __str__(self):
            s = " ".join(sorted(self.commands))
            return f"CommandDecode({s}, ignore_case={self.ignore_case})"
        def __call__(self, user_string):
            '''Remove any leading and trailing whitespace in user_string and return a
            list of the commands it matches, starting at the beginning of the string.
            '''
            if not isinstance(user_string, str):
                raise ValueError("Input must be a string")
            s = user_string.strip()
            if not s:
                return []   # No matches
            if self.ignore_case:
                s = s.lower()
            if s in self.commands:  # It's in the set, so can be the only match
                return [user_string]
            first_char = s[0]
            if first_char not in self.first_char_list:
                return []
            # Get a list of the possible matches
            possible_commands = self.index[first_char]
            if self.ignore_case:
                regexp = re.compile("^" + s, re.I)
            else:
                regexp = re.compile("^" + s)
            matches = []
            for cmd in possible_commands:
                if regexp.match(cmd):
                    matches.append(cmd)
            # Return the list of matches (length 0, 1, or more than 1)
            if len(matches) == 0:
                return []
            if len(matches) == 1:
                return [matches[0]]
            return matches
if 1:   # class Constant:  Define runtime constants
    class Constant:
        '''Class to define constants: 
        
            import dptypes
            C = dptypes.Constant()
            C.speed = 47.1
        
        Trying to change C.speed later to a new value will result in an exception.  When
        needed, you can change the value using
        
            with C:
                C.speed = 42
        
        or 
            C.strict = False
            C.speed = 42
            C.strict = True
        
        I recommend the context manager pattern, as it's too easy to set C.strict to
        False, then forget to change it back to True later in your code.

        While the name is Constant, I use this class instance as a holder for global
        variables in my modules and scripts.  I used to use the simple pattern

            class G:
                pass
            g = G()

        where g's attributes held the global variables.  This worked well, but the real
        pattern is that much or most of the time you set these global variables once,
        then don't plan on changing them again.  But later when maintaining a big file,
        you might forget this agreement about constancy.  This Constant pattern then
        lets the (desired constancy) be found by an exception, as you need to make the
        change using the context manager.

        To keep with the name Constant, you'll want to bind immutable (hashable) objects
        to the constant name.  If you e.g. bind a list or dict, it will continue to be
        bound, but someone/something can change the list/dict later, so it's not really
        a constant.
        
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
if 1:   # class Stack
    class StackLock:
        "This is a context manager for the needed locks"
        def __init__(self):
            self.mlock = MultiprocessingLock()
            self.tlock = ThreadingLock()
            self.state = "not locked"
        def __enter__(self):
            self.mlock.acquire()
            self.tlock.acquire()
            self.state = "locked"
            return None
        def __exit__(self, exception, exception_value, traceback):
            self.mlock.release()
            self.tlock.release()
            self.state = "not locked"
            # Returning None means any exception is passed on to the following
            # code
            return None
    class Stack(deque):
        '''Stack implements a stack with the methods
            push
            pop
            clear
            copy
            rotate
        
        These methods are essentially already implemented by the deque object, so little
        new code was required.  You might think that a list would be as good of a base
        object, but implementing the rotate method probably wouldn't be as efficient as
        a deque.
        
        If you pop() an empty stack, you'll get an IndexError.
        
        A Stack object is thread-safe and process-safe because a StackLock instance is
        used before every operation.
        '''
        def __init__(self, iterable=None, maxlen=None, homogeneous=None):
            '''See deque's documentation for the first two keywords.  If homogeneous is not
            None, then all objects pushed on the stack must be the same type as the
            homogeneous object.
            '''
            self._lock = StackLock()
            self.NI = NotImplementedError("Operation not allowed for Stack")
            self._type = homogeneous
            if iterable is None:
                super().__init__([], maxlen=maxlen)
            else:
                super().__init__(iterable, maxlen=maxlen)
        def _str(self):
            with self._lock:
                s = [str(list(self))]
                if self.maxlen is not None:
                    s.append(f"maxlen={self.maxlen}")
                if self._type is not None:
                    s.append(f"homogeneous={self._type}")
            return "Stack({})".format(", ".join(s))
        def __repr__(self):
            with self._lock:
                return self._str()
        def __str__(self):
            with self._lock:
                return self._str()
        def clear(self):
            with self._lock:
                super().clear()
        def copy(self):
            with self._lock:
                s = super().copy()
            return s
        def pop(self):
            with self._lock:
                t = super().pop()
            return t
        def push(self, x):
            with self._lock:
                if self._type is not None:
                    if type(x) is not self._type:
                        msg = f"'{x}' is an incorrect type.\n"
                        msg += f"  It must be of type {self._type}."
                        raise TypeError(msg)
                super().append(x)
        def rotate(self, n=1):
            with self._lock:
                super().rotate(n)
        @property
        def homogeneous(self):
            'Returns the type of a homogeneous stack or None if not homogeneous'
            with self._lock:
                return self._type
        # Disable unused deque methods
        def append(self, x):
            raise self.NI
        def appendleft(self, x):
            raise self.NI
        def count(self, x):
            raise self.NI
        def extend(self, iterable):
            raise self.NI
        def extendleft(self, iterable):
            raise self.NI
        def index(self, x, start=None, stop=None):
            raise self.NI
        def insert(self, i, x):
            raise self.NI
        def popleft(self):
            raise self.NI
        def remove(self, x):
            raise self.NI
        def reverse(self, x):
            raise self.NI

if __name__ == "__main__":  
    import collections
    import sys

    import lwtest
    deque = collections.deque
    run = lwtest.run
    Assert = lwtest.Assert
    raises = lwtest.raises
    if 1:   # Demo code
        def Demo_CommandDecode():
            # Demonstrate the class; use some typical UNIX program names.
            cmds, d = ('''
                ar awk banner basename bc cal cat cc chmod cksum clear cmp
                compress cp cpio crypt ctags cut date dc dd df diff dirname du
                echo ed egrep env ex expand expr false fgrep file find fmt
                fold getopt grep gzip head id join kill ksh ln logname ls m4
                mailx make man mkdir more mt mv nl nm od paste patch perl pg
                pr printf ps pwd rev rm rmdir rsh sed sh sleep sort spell
                split strings strip stty sum sync tail tar tee test touch tr
                true tsort tty uname uncompress unexpand uniq uudecode
                uuencode vi wc which who xargs zcat
            ''', [])
            for i in cmds.replace("\n", "").split():
                d.append((i, ""))
            c, prompt = CommandDecode(dict(d), ignore_case=True), "> "
            print("Enter some UNIX commands, 'q' to quit, '.' to list all:")
            while True:
                cmd = input(prompt)
                if cmd == "q":
                    break
                elif cmd == ".":
                    for i in list(c.commands):
                        print(i, end=" ")
                    print()
                else:
                    x = c(cmd)
                    if not x:
                        print(f"{cmd!r} unrecognized")
                    elif len(x) == 1:
                        print(f"{cmd!r} was an exact match to {x[0]!r}")
                    else:
                        x.sort()
                        print(f"{cmd!r} is ambiguous:  {x!r}")
        def Demo_Bidict():
            pass
            # ∞∞1 Needs to be written
        def Demo_SlushDict():
            pass
            # ∞∞1 Needs to be written
    if 1:   # SlushDict tests
        def Test_SlushDict():
            k, v, v1 = "three", 0, 42
            def Slushdict_Init():
                return SlushDict({k: v})
            if 1:   # Demonstrate core behavior
                # Test the three methods of constructing a dict
                d = SlushDict({k: v})       # Create from an existing dict
                Assert(d[k] == v and d == Slushdict_Init())
                tuples = ((k, v), )
                d = SlushDict(tuples)       # Create from tuples
                Assert(d[k] == v and d == Slushdict_Init())
                d = SlushDict(three=v)      # Create from keywords
                Assert(d[k] == v and d == Slushdict_Init())
            if 1:   # Show normal dict changing methods don't work
                d = Slushdict_Init()
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
                d = Slushdict_Init()
                with d:
                    d[k] = 42
                Assert(d[k] == 42)
                # Delete an item
                d = Slushdict_Init()
                with d:
                    del d[k]
                Assert(not d)
                # Clear the dict
                d = Slushdict_Init()
                with d:
                    d.clear()
                Assert(not d)
                # Pop the item keyed by k
                d = Slushdict_Init()
                with d:
                    d.pop(k)
                Assert(not d)
                # popitem
                d = Slushdict_Init()
                with d:
                    d.popitem()
                Assert(not d)
                # setdefault
                k1 = "four"
                d = Slushdict_Init()
                with d:
                    d.setdefault(k1)
                Assert(d[k1] is None)
                d = Slushdict_Init()
                v1 = 83189
                with d:
                    d.setdefault(k1, v1)
                Assert(d[k1] is v1)
                # update
                d = Slushdict_Init()
                with d:
                    d.update({k1: v1})
                Assert(d[k] == v)
                Assert(d[k1] == v1)
            if 1:   # Show you can get a hash
                d = Slushdict_Init()
                hash(d)     # No exception
                set(d)      # No exception
    if 1:   # Bidict tests
        def Bidict_init():
            keys, values = ["jan", "feb"], [1, 2]
            d = dict(zip(keys, values, strict=True))
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
            assert set(bd.items()) == set(zip(keys, values, strict=True))
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
    if 1:   # CommandDecode tests
        def Test_CommandDecode_Exceptions():
            commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
            # Case-insensitive instantiation results in an exception ('Aaa' and
            # 'aaa' collide).
            raises(ValueError, CommandDecode, commands, ignore_case=True)
            # commands not a dict/set
            raises(ValueError, CommandDecode, 4)
            # Empty dict/set
            raises(ValueError, CommandDecode, {})
            raises(ValueError, CommandDecode, set())
            # Cannot contain empty string
            raises(ValueError, CommandDecode, set("",))
            # Call's argument must be a string
            cmd = CommandDecode(commands)
            raises(ValueError, cmd, 4)
            # Can't make empty call
            raises(TypeError, cmd)
        def Test_CommandDecode():
            commands = set(("a", "Aaa", "Aab", "aaa", "aab"))
            cmd = CommandDecode(commands, ignore_case=False)
            assert set(cmd("a")) == set(["a"])
            assert set(cmd("ax")) == set([])
            assert set(cmd("aa")) == set(["aaa", "aab"])
            assert set(cmd("Aa")) == set(["Aaa", "Aab"])
            assert set(cmd("Aab")) == set(["Aab"])
            # Case insensitive
            commands = set(("A", "AAA", "AAB"))
            cmd = CommandDecode(commands, ignore_case=True)
            assert set(cmd("a")) == set(["a"])
            assert set(cmd("ax")) == set([])
            assert set(cmd("AX")) == set([])
            assert set(cmd("aa")) == set(["aaa", "aab"])
            assert set(cmd("Aa")) == set(["aaa", "aab"])
            assert set(cmd("Aab")) == set(["Aab"])
    if 1:   # Constant tests
        def Constant_Init():
            return Constant()
        def Test_Constant_can_change_strict_property():
            c = Constant_Init()
            # Default value of strict is True
            Assert(c.strict)
            c.strict = False
            Assert(not c.strict)
        def Test_Constant_is_constant():
            c = Constant_Init()
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
        def Test_Constant_not_strict():
            'Can set items to mutable objects without an exception'
            # Nonhashable objects cause a TypeError
            c = Constant_Init()
            for i in ([], {}, set(), deque([])):
                with raises(TypeError):
                    c.x = i
            # If strict is False, then OK to store hashable items
            c = Constant_Init()
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
        def Test_Constant_Delete():
            c = Constant_Init()
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
        def Test_Constant_ContextManager():
            c = Constant_Init()
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
    if 1:   # Stack tests
        stack_n = 5
        def Stack_init():
            "Make a stack with n integers"
            st = Stack()
            for i in range(stack_n):
                st.push(i)
            return st
        def Test_Stack_Len():
            st = Stack_init()
            Assert(len(st) == stack_n)
        def Test_Stack_Pop():
            st = Stack_init()
            R = list(st)
            for i in reversed(R):
                Assert(st.pop() == i)
            # Make sure empty stack raises exception when popped
            Assert(len(st) == 0)
            Assert(not st)
            with raises(IndexError):
                st.pop()
        def Test_Stack_Push():
            st = Stack()
            r = list(range(stack_n))
            for i in r:
                st.push(i)
            Assert(list(st) == r)
            for i in reversed(r):
                Assert(st.pop() == i)
            Assert(len(st) == 0)
            Assert(not st)
        def Test_Stack_Copy():
            'The copy() method appeared in python 3.5'
            v = sys.version_info
            if v[0] < 3 or (v[0] == 3 and v[1] < 5):
                return
            st = Stack_init()
            s = st.copy()
            Assert(st == s)
            Assert(id(st) != id(s))
        def Test_Stack_Bool():
            'Verify a stack s with one or more elements returns True from bool(s)'
            st = Stack()
            Assert(not bool(st))
            st.push(8)
            Assert(bool(st))
            st.push(9)
            Assert(bool(st))
            st.pop()
            Assert(bool(st))
            st.pop()
            Assert(not bool(st))
            st.push(9)
            st.clear()
            Assert(not bool(st))
        def Test_Stack_Clear():
            st = Stack_init()
            Assert(len(st) == stack_n)
            st.clear()
            Assert(len(st) == 0)
        def Test_Stack_Homogeneity():
            st = Stack(["a", "b"], homogeneous=str)
            Assert(st.homogeneous is str)
            raises(TypeError, st.push, 1)
            st.push("b")
            st = Stack_init()     # Stack of integers; non-homogeneous
            st.push("a")    # Allowed
        def Test_Stack_Maxlen():
            st = Stack([1, 2], maxlen=2)
            st.push(3)
            Assert(list(st) == [2, 3])
            Assert(st.maxlen == 2)
        def Test_Stack_BadOps():
            st = Stack([1, 2], maxlen=2)
            with raises(NotImplementedError):
                st.append(1)
                st.append_left(1)
                st.count(1)
                st.extend(1)
                st.extendleft(1)
                st.index(1)
                st.insert(1)
                st.popleft(1)
                st.remove(1)
                st.reverse(1)
    if len(sys.argv) > 1:
        exit(run(globals(), regexp=r"^Demo_", quiet=1, halt=1, verbose=0)[0])
    else:
        exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])


def GetGist():
    g = {}
    g["gist"] = "Various types for programming tasks"
    g["copy"] = "Copyright © 2026 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "programming"
    g["todo"] = '''

    - IntFixed:  immutable fixed-size (number of bits) integers.  Use bitarray module's
      frozenbitarray for the implementation.  It would be handy if class IntFixed(int,
      bitarray) could be used.  Or, IntFixed(int) and the instance._i attribute is a 
      suitable frozenbitarray for the class.

    '''
    return g
