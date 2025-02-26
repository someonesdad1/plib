"""
Elementary number theory and combinatorics functions

References
  ASPN Recipes, mathematics.py
"""

if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    # ∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    # ∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    # ∞license∞#
    # ∞what∞#
    # <math> Elementary number theory and combinatorics functions
    # ∞what∞#
    # ∞test∞# run #∞test∞#
    pass
if 1:  # Global variables
    ii = isinstance


def gcd(a, b):
    "Greatest common divisor of a and b using Euclid's algorithm"
    if not (ii(a, int) and ii(b, int)):
        raise TypeError("a and b must be integers")
    if not a and not b:
        raise ValueError("a and b cannot both be zero")
    a, b = abs(a), abs(b)
    if not a:
        return b
    if not b:
        return a
    while b:
        a, b = b, a % b
    return a


def gcd_seq(seq):
    "Greatest common divisor of a sequence of numbers"
    if not seq:
        return None
    r = seq[0]
    for i in range(1, len(seq)):
        r = gcd(r, seq[i])
        if r <= 1:
            break
    return r


def lcm(a, b):
    "Least common multiple of a and b"
    if not a or not b:
        return 0
    return a * b / gcd(a, b)


def lcm_seq(seq):
    "Least common multiple of numbers in seq"
    if not seq:
        return 0
    r = seq[0]
    for i in range(1, len(seq)):
        r = lcm(r, seq[i])
        if r <= 1:
            break
    return r


def factorial(n):
    "Returns the factorial of n: n! = n*(n-1)*(n-2)*...*2*1"
    if not ii(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be >= 0")
    p = 1
    for i in range(2, n + 1):
        p *= i
    return p
    """Another possible implementation:
    from functools import reduce
    reduce(lambda x, y: x*y, range(1, n))
    """


def rising_factorial(x, n):
    """Returns value of x (x + 1) (x + 2) ... (x+n-1)."""
    if n < 1 or not ii(n, int):
        raise ValueError("n must be an integer >= 1")
    p = x
    for i in range(1, n):
        p *= x + i
    return p


def falling_factorial(x, n):
    """Returns value of x (x-1) (x-2) ... (x - n + 1)."""
    if n < 1 or not ii(n, int):
        raise ValueError("n must be an integer >= 1")
    p = x
    for i in range(1, n):
        p *= x - i
    return p


def Comb(n, r):
    """Returns the number of combinations of n things taken r at a
    time.  Note recurrence relation
        Comb(r, r) = Comb(n-1, r) + Comb(n-1, r-1)
    """
    if not ii(n, int):
        raise TypeError("n must be an integer")
    if not ii(r, int):
        raise TypeError("r must be an integer")
    if r < 0 or n < 1 or r > n:
        raise ValueError("n and r must be greater than zero and r <= n")
    if not r or r == n:
        return 1
    x, i = n, n - 1
    for d in range(2, r + 1):
        x = x * i // d
        i -= 1
    return x


def Perm(n, r):
    """Returns the number of permutations of n things take n r at a
    time.  Note recurrence relation
        Perm(n, r) = Perm(n, r - 1) * (n - r + 1)
    """
    if r < 1 or n < 1 or r > n:
        raise ValueError("n and r must be greater than zero and r <= n")
    x = 1
    for i in range(n - r + 1, n + 1):
        x *= i
    return x


def int_partitions(n, k=1):
    """Returns the number of integer partitions that are >= k.

    Ramanujan's formula for upper bound for number of partitions of k:
        int(exp(pi*sqrt(2*n/3))/(4*n*sqrt(3)))
    """
    total = 1
    n -= k
    while n >= k:
        total += int_partitions(n, k)
        n, k = n - 1, k + 1
    return total


def ackermann(m, n):
    """Returns the ackermann function using recursion. (m, n are
    non-negative)."""
    if not ii(m, int):
        raise ValueError("m must be an integer >= 0")
    if not ii(n, int) or n < 0:
        raise ValueError("n must be an integer >= 0")
    if not m and n >= 0:
        return n + 1
    if not n and m >= 1:
        return ackermann(m - 1, 1)
    return ackermann(m - 1, ackermann(m, n - 1))


def bell(n):
    """Returns the nth Bell number."""
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if n < 2:
        return 1
    sum = 0
    for k in range(1, n + 1):
        sum = sum + Comb(n - 1, k - 1) * bell(k - 1)
    return sum


def catalan(n):
    """Returns the nth Catalan number."""
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if n <= 1:
        return 1
    elif n == 2:
        return 2
    return (2 * n) * (2 * n - 1) * catalan(n - 1) // ((n + 1) * n)


def fibonacci(n):
    """Returns the nth Fibonacci number."""
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if not n:
        return 0
    elif n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)


def lucas(n):
    """Returns the nth lucas number.
    Recursive version:
        return lucas(n - 1) + lucas(n - 2)
    """
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if not n:
        return 2
    elif n == 1:
        return 1
    elif n == 2:
        return 3
    else:
        return lucas(n - 1) + lucas(n - 2)


def stirling1(n, k):
    """Returns the Stirling number of the first kind."""
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if k < 0 or not ii(k, int):
        raise ValueError("k must be an integer >= 0")
    if not n and not k:
        return 1
    if (not k and n >= 1) or k > n:
        return 0
    return stirling1(n - 1, k - 1) - (n - 1) * stirling1(n - 1, k)


def stirling2(n, k):
    """Returns the Stirling number of the second kind."""
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if k < 0 or not ii(k, int):
        raise ValueError("k must be an integer >= 0")
    if k <= 1 or k == n:
        return 1
    if k > n or n <= 0:
        return 0
    return stirling2(n - 1, k - 1) + k * stirling2(n - 1, k)


def NumberOfDerangements(n):
    """Returns the number of derangements using the formula:
        d(n) = n*d(n - 1) + (-1)**n
    A derangement is a permutation where each element is not in its natural place, or p[i] != i.
    """
    if not n:
        return 1
    elif n == 1:
        return 0
    d, dn = -1, 0
    for i in range(2, n + 1):
        dnm1 = dn
        d = -d
        dn = i * dnm1 + d
    return dn


if __name__ == "__main__":
    import math
    from itertools import combinations, permutations
    import sys
    from partitions import partitions_cs
    from stirling import Stirling1, Stirling2
    from lwtest import run, assert_equal, raises, Assert
    from pdb import set_trace as xx

    def Test_gcd():
        assert_equal(gcd(0, 1), 1)
        assert_equal(gcd(1, 0), 1)
        assert_equal(gcd(1, 1), 1)
        #
        assert_equal(gcd(0, -1), 1)
        assert_equal(gcd(-1, 0), 1)
        assert_equal(gcd(-1, -1), 1)
        #
        assert_equal(gcd(10, 12), 2)
        assert_equal(gcd(-10, -12), 2)
        #
        raises(ValueError, gcd, 0, 0)
        raises(TypeError, gcd, 1.0, 0)
        raises(TypeError, gcd, 0, 1.0)
        raises(TypeError, gcd, 1.0, 1.0)
        # gcd_seq
        assert_equal(gcd_seq(None), None)
        assert_equal(gcd_seq(0), None)
        assert_equal(gcd_seq(range(1, 10)), 1)
        assert_equal(gcd_seq([12, 18, 24]), 6)

    def Test_lcm():
        assert_equal(lcm(0, 0), 0)
        assert_equal(lcm(1, 0), 0)
        assert_equal(lcm(0, 1), 0)
        #
        assert_equal(lcm(2, 2), 2)
        assert_equal(lcm(2, 4), 4)
        assert_equal(lcm(2, 3), 6)
        #
        assert_equal(lcm(7, 8), 56)
        assert_equal(lcm(-7, 8), -56)
        assert_equal(lcm(7, -8), -56)
        assert_equal(lcm(-7, -8), 56)
        # lcm_seq
        assert_equal(lcm_seq([-7, -8]), 56)

    def Test_factorial():
        raises(ValueError, factorial, -1)
        for i in range(20):
            assert_equal(factorial(i), math.factorial(i))
        # rising_factorial
        raises(ValueError, rising_factorial, 0, 0)
        raises(ValueError, rising_factorial, 0, 0.0)
        assert_equal(rising_factorial(2, 1), 2)
        assert_equal(rising_factorial(2, 2), 6)
        assert_equal(rising_factorial(2, 3), 24)
        x = 9.5
        assert_equal(rising_factorial(x, 3), x * (x + 1) * (x + 2))
        # falling_factorial
        raises(ValueError, falling_factorial, 0, 0)
        raises(ValueError, falling_factorial, 0, 0.0)
        assert_equal(falling_factorial(2, 1), 2)
        assert_equal(falling_factorial(2, 2), 2)
        assert_equal(falling_factorial(2, 3), 0)
        assert_equal(falling_factorial(2, 4), 0)
        x = 10.5
        assert_equal(falling_factorial(x, 3), x * (x - 1) * (x - 2))

    def Test_Comb():
        raises(ValueError, Comb, 0, 0)
        raises(ValueError, Comb, 0, 1)
        raises(ValueError, Comb, 1, 2)
        for n in range(2, 10):
            for r in range(2, n):
                assert_equal(Comb(n, r), len(list(combinations(range(n), r))))

    def Test_Perm():
        raises(ValueError, Perm, 0, 0)
        raises(ValueError, Perm, 0, 1)
        raises(ValueError, Perm, 1, 2)
        for n in range(2, 10):
            for r in range(2, n):
                assert_equal(Perm(n, r), len(list(permutations(range(n), r))))

    def Test_int_partitions():
        a, b = int_partitions, partitions_cs
        for n in range(2, 10):
            assert_equal(a(n, 1), len(list(b(n, None))))

    def Test_ackermann():
        """See definition at
        https://en.wikipedia.org/wiki/Ackermann_function.
        """
        raises(ValueError, ackermann, 0.0, 0)
        raises(ValueError, ackermann, 0, 0.0)
        raises(ValueError, ackermann, -1, 0)
        raises(ValueError, ackermann, 0, -1)
        for n in range(5):
            assert_equal(ackermann(0, n), n + 1)
            assert_equal(ackermann(1, n), n + 2)
            assert_equal(ackermann(2, n), 2 * n + 3)
            assert_equal(ackermann(3, n), 2 ** (n + 3) - 3)

    def Test_univariate():
        data = (
            (
                (
                    1,
                    1,
                    2,
                    5,
                    15,
                    52,
                    203,
                    877,
                    4140,
                    21147,
                    115975,
                    678570,
                    4213597,
                    27644437,
                ),
                bell,
            ),
            ((1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786, 208012), catalan),
            ((0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144), fibonacci),
            (
                (
                    2,
                    1,
                    3,
                    4,
                    7,
                    11,
                    18,
                    29,
                    47,
                    76,
                    123,
                    199,
                    322,
                    521,
                    843,
                    1364,
                    2207,
                ),
                lucas,
            ),
            (
                (
                    1,
                    0,
                    1,
                    2,
                    9,
                    44,
                    265,
                    1854,
                    14833,
                    133496,
                    1334961,
                    14684570,
                    176214841,
                    2290792932,
                ),
                NumberOfDerangements,
            ),
        )
        for answers, func in data:
            for n in range(len(answers)):
                assert_equal(func(n), answers[n])

    def Test_stirling():
        for f1, f2 in ((stirling1, Stirling1), (stirling2, Stirling2)):
            for n in range(10):
                for k in range(n):
                    assert_equal(f1(n, k), f2(n, k))

    exit(run(globals())[0])
