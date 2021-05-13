'''
Functions to calculate Stirling numbers.
    Stirling1(n, k):  Stirling numbers of the first kind.
    Stirling2(n, k):  Stirling numbers of the second kind.

References:
    http://mathworld.wolfram.com/StirlingNumberoftheFirstKind.html
    http://mathworld.wolfram.com/StirlingNumberoftheSecondKind.html
'''

# Copyright (C) 2014 Don Peterson
# Contact:  gmail.com@someonesdad1

#
# Licensed under the Open Software License version 3.0.
# See http://opensource.org/licenses/OSL-3.0.
#

__all__ = ["Stirling1", "Stirling2"]

def s(n, k):
    '''Returns the Stirling number of the first kind.
 
    The recurrence relation is s(n+1, k) = s(n, k-1) - n*s(n, k) for k
    running from 1 to n.  This is a recursive calculation, although
    the intermediate results are cached to reduce subsequent
    computation time.
    '''
    if not isinstance(n, int) or n < 0 or not isinstance(k, int) or k < 0:
        raise ValueError("n and k must be integers >= 0")
    if n == k:
        return 1
    elif n == 0 and k == 0:
        return 1
    elif k == 0 and n >= 1:
        return 0
    elif k > n:
        return 0
    return s(n - 1, k - 1) - (n - 1)*s(n - 1, k)

def S(n, k):
    '''Returns the Stirling number of the second kind.
 
    The recurrence relation is S(n, k) = S(n - 1, k - 1) + k*S(n - 1, k).
    The Stirling number of the second kind is the number of ways of
    partitioning a set of n objects into k-sized subsets.
    '''
    if not isinstance(n, int) or n < 0 or not isinstance(k, int) or k < 0:
        raise ValueError("n and k must be integers >= 0")
    if k <= 1 or k == n:
        return 1
    elif k > n or n <= 0:
        return 0
    return S(n - 1, k - 1) + k * S(n - 1, k)

class Memoize:
    '''Class to cache return values for a function.
    '''
    def __init__(self, func):
        self.cache = {}
        self.func = func
    def __call__(self, *params):
        try:
            return self.cache[params]
        except KeyError:
            result = self.func(*params)
            self.cache[params] = result
            return result

Stirling1 = Memoize(s)
Stirling2 = Memoize(S)
