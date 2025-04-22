'''
Thread-safe and process-safe stack
'''
if 1:  # Header
    # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    ##∞copyright∞# Copyright (C) 2014, 2019 Don Peterson #∞copyright∞#
    ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    ##∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    ##∞license∞#
    ##∞what∞#
    # Thread-safe and process-safe stack
    ##∞what∞#
    ##∞test∞# run #∞test∞#
    # Standard imports
    from collections import deque
    from multiprocessing import Lock as MultiprocessingLock
    from threading import Lock as ThreadingLock
    # Global variables
    ii = isinstance
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
    
    These methods are essentially already implemented by the deque object, so little new
    code was required.  You might think that a list would be as good of a base object,
    but implementing the rotate method probably wouldn't be as efficient as a deque.
    
    If you pop() an empty stack, you'll get an IndexError.
    
    A Stack object is thread-safe and process-safe.
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
            super(Stack, self).__init__([], maxlen=maxlen)
        else:
            super(Stack, self).__init__(iterable, maxlen=maxlen)
    def _str(self):
        with self._lock:
            s = [str(list(self))]
            if self.maxlen is not None:
                s.append("maxlen={}".format(self.maxlen))
            if self._type is not None:
                s.append("homogeneous={}".format(self._type))
        return "Stack({})".format(", ".join(s))
    def __repr__(self):
        return self._str()
    def __str__(self):
        return self._str()
    def clear(self):
        with self._lock:
            super(Stack, self).clear()
    def copy(self):
        with self._lock:
            s = super(Stack, self).copy()
        return s
    def pop(self):
        with self._lock:
            t = super(Stack, self).pop()
        return t
    def push(self, x):
        with self._lock:
            if self._type is not None:
                if type(x) != self._type:
                    msg = "'{}' is an incorrect type.\n".format(x)
                    msg += "  It must be of type {}.".format(self._type)
                    raise TypeError(msg)
            super(Stack, self).append(x)
    def rotate(self, n=1):
        with self._lock:
            super(Stack, self).rotate(n)
    @property
    def homogeneous(self):
        '''Returns the type of a homogeneous stack or None if not
        homogeneous.
        '''
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
    import sys
    from lwtest import run, raises, Assert
    n = 5
    def init():
        "Make a stack with n integers"
        st = Stack()
        for i in range(n):
            st.push(i)
        return st
    def TestLen():
        st = init()
        Assert(len(st) == n)
    def TestPop():
        st = init()
        R = list(st)
        for i in reversed(R):
            Assert(st.pop() == i)
        # Make sure empty stack raises exception when popped
        Assert(len(st) == 0)
        Assert(not st)
        with raises(IndexError):
            st.pop()
    def TestPush():
        st = Stack()
        r = list(range(n))
        for i in r:
            st.push(i)
        Assert(list(st) == r)
        for i in reversed(r):
            Assert(st.pop() == i)
        Assert(len(st) == 0)
        Assert(not st)
    def TestCopy():
        'The copy() method appeared in python 3.5'
        v = sys.version_info
        if v[0] < 3 or (v[0] == 3 and v[1] < 5):
            return
        st = init()
        s = st.copy()
        Assert(st == s)
        Assert(id(st) != id(s))
    def TestBool():
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
    def TestClear():
        st = init()
        Assert(len(st) == n)
        st.clear()
        Assert(len(st) == 0)
    def TestHomogeneity():
        st = Stack(["a", "b"], homogeneous=str)
        Assert(st.homogeneous and st.homogeneous == str)
        raises(TypeError, st.push, 1)
        st.push("b")
        st = init()     # Stack of integers; non-homogeneous
        st.push("a")    # Allowed
    def TestMaxlen():
        st = Stack([1, 2], maxlen=2)
        st.push(3)
        Assert(list(st) == [2, 3])
        Assert(st.maxlen == 2)
    exit(run(globals())[0])
