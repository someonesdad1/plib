"""
Functions to calculate Stirling numbers.
    Stirling1(n, k):  Stirling numbers of the first kind.
    Stirling2(n, k):  Stirling numbers of the second kind.

References:
    http://mathworld.wolfram.com/StirlingNumberoftheFirstKind.html
    http://mathworld.wolfram.com/StirlingNumberoftheSecondKind.html
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # <math> Calculates Stirling numbers of the first and second kinds.
    # ∞what∞#
    # ∞test∞# run #∞test∞#
    pass
if 1:  # Global variables
    __all__ = ["Stirling1", "Stirling2"]


def s(n, k):
    """Returns the Stirling number of the first kind.

    The recurrence relation is s(n+1, k) = s(n, k-1) - n*s(n, k) for k
    running from 1 to n.  This is a recursive calculation, although
    the intermediate results are cached to reduce subsequent
    computation time.
    """
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
    return s(n - 1, k - 1) - (n - 1) * s(n - 1, k)


def S(n, k):
    """Returns the Stirling number of the second kind.

    The recurrence relation is S(n, k) = S(n - 1, k - 1) + k*S(n - 1, k).
    The Stirling number of the second kind is the number of ways of
    partitioning a set of n objects into k-sized subsets.
    """
    if not isinstance(n, int) or n < 0 or not isinstance(k, int) or k < 0:
        raise ValueError("n and k must be integers >= 0")
    if k <= 1 or k == n:
        return 1
    elif k > n or n <= 0:
        return 0
    return S(n - 1, k - 1) + k * S(n - 1, k)


class Memoize:
    """Class to cache return values for a function."""

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

if __name__ == "__main__":
    from lwtest import run, raises, assert_equal, Assert

    def Test_first_kind():
        """Numbers from https://oeis.org/A008275 (See the triangle down
        next to EXAMPLE).
        """
        n = 1
        expected = (0, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 2
        expected = (0, -1, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 3
        expected = (0, 2, -3, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 4
        expected = (0, -6, 11, -6, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 5
        expected = (0, 24, -50, 35, -10, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 6
        expected = (0, -120, 274, -225, 85, -15, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 7
        expected = (0, 720, -1764, 1624, -735, 175, -21, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])
        n = 8
        expected = (0, -5040, 13068, -13132, 6769, -1960, 322, -28, 1)
        for k in range(1, n):
            Assert(s(n, k) == expected[k])

    def Test_second_kind():
        """Numbers from https://oeis.org/A008277 (See the triangle down
        next to EXAMPLE).
        """
        n = 1
        expected = (0, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 2
        expected = (0, 1, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 3
        expected = (0, 1, 3, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 4
        expected = (0, 1, 7, 6, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 5
        expected = (0, 1, 15, 25, 10, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 6
        expected = (0, 1, 31, 90, 65, 15, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 7
        expected = (0, 1, 63, 301, 350, 140, 21, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])
        n = 8
        expected = (0, 1, 127, 966, 1701, 1050, 266, 28, 1)
        for k in range(1, n):
            Assert(S(n, k) == expected[k])

    exit(run(globals(), halt=1)[0])
