# Copyright (C) 2014, 2019 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

from collections import deque
from multiprocessing import Lock as MLock
from threading import Lock as TLock

class StackLock(object):
    def __init__(self):
        self.mlock = MLock()
        self.tlock = TLock()
        self.state = "not locked"
    def acquire(self):
        self.mlock.acquire()
        self.tlock.acquire()
        self.state = "locked"
    def release(self):
        self.mlock.release()
        self.tlock.release()
        self.state = "not locked"

class Stack(deque):
    '''Stack implements a stack with the methods
        push
        pop
        clear
        copy (won't work on versions less than python 3.5)
        rotate
    If you pop() an empty stack, you'll get an IndexError.
 
    A Stack object is thread-safe and process-safe.  It should work on
    python 2.7 or 3.
    '''
    def __init__(self, iterable=None, maxlen=None, homogeneous=None):
        '''See deque's documentation for the first two keywords.  If
        homogeneous is not None, then all objects pushed on the stack
        must be the same type as the homogeneous object.
        '''
        self._lock = StackLock()
        self.NI = NotImplementedError("Operation not allowed for Stack")
        self._type = None if homogeneous is None else type(homogeneous)
        if iterable is None:
            super(Stack, self).__init__([], maxlen=maxlen)
        else:
            super(Stack, self).__init__(iterable, maxlen=maxlen)
    def _str(self):
        self._lock.acquire()
        s = [str(list(self))]
        if self.maxlen is not None:
            s.append("maxlen={}".format(self.maxlen))
        if self._type is not None:
            s.append("homogeneous={}".format(self._type))
        self._lock.release()
        return "Stack({})".format(', '.join(s))
    def __repr__(self):
        return self._str()
    def __str__(self):
        return self._str()
    def clear(self): 
        self._lock.acquire()
        super(Stack, self).clear()
        self._lock.release()
    def copy(self): 
        self._lock.acquire()
        s = super(Stack, self).copy()
        self._lock.release()
        return s
    def pop(self): 
        self._lock.acquire()
        t = super(Stack, self).popleft()
        self._lock.release()
        return t
    def push(self, x): 
        self._lock.acquire()
        if self._type is not None:
            if type(x) != self._type:
                msg = "'{}' is an incorrect type.\n".format(x)
                msg += "  It must be of type {}.".format(self._type)
                self._lock.release()
                raise TypeError(msg)
        super(Stack, self).appendleft(x)
        self._lock.release()
    def rotate(self, n=1): 
        self._lock.acquire()
        super(Stack, self).rotate(n)
        self._lock.release()
    @property
    def homogeneous(self):
        '''Returns the type of a homogeneous stack or None if not
        homogeneous.
        '''
        return self._type
    ## Disable unused deque methods
    def append(self, x):                        raise self.NI
    def appendleft(self, x):                    raise self.NI
    def count(self, x):                         raise self.NI
    def extend(self, iterable):                 raise self.NI
    def extendleft(self, iterable):             raise self.NI
    def index(self, x, start=None, stop=None):  raise self.NI
    def insert(self, i, x):                     raise self.NI
    def popleft(self):                          raise self.NI
    def remove(self, x):                        raise self.NI
    def reverse(self, x):                       raise self.NI
