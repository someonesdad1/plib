import math
from itertools import combinations, permutations
import sys
from partitions import partitions_cs
from stirling import Stirling1, Stirling2
from combinatorial import gcd, gcd_seq, lcm, lcm_seq, factorial
from combinatorial import rising_factorial, falling_factorial, Comb, Perm
from combinatorial import int_partitions, ackermann, bell, catalan, fibonacci
from combinatorial import lucas, stirling1, stirling2, NumberOfDerangements
from lwtest import run, assert_equal, raises

from pdb import set_trace as xx
if 0:
    import debug
    debug.SetDebugger()

def Test_gcd():
    assert_equal(gcd(0, 0), 0)
    assert_equal(gcd(0, 1), 1)
    assert_equal(gcd(1, 0), 1)
    assert_equal(gcd(1, 1), 1)
    #
    assert_equal(gcd(0, 0), 0)
    assert_equal(gcd(0, -1), 1)
    assert_equal(gcd(-1, 0), 1)
    assert_equal(gcd(-1, -1), 1)
    #
    assert_equal(gcd(10, 12), 2)
    assert_equal(gcd(-10, -12), 2)
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
    assert_equal(rising_factorial(x, 3), x*(x + 1)*(x + 2))
    # falling_factorial
    raises(ValueError, falling_factorial, 0, 0)
    raises(ValueError, falling_factorial, 0, 0.0)
    assert_equal(falling_factorial(2, 1), 2)
    assert_equal(falling_factorial(2, 2), 2)
    assert_equal(falling_factorial(2, 3), 0)
    assert_equal(falling_factorial(2, 4), 0)
    x = 10.5
    assert_equal(falling_factorial(x, 3), x*(x - 1)*(x - 2))
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
    '''See definition at
    https://en.wikipedia.org/wiki/Ackermann_function.
    '''
    raises(ValueError, ackermann, 0.0, 0)
    raises(ValueError, ackermann, 0, 0.0)
    raises(ValueError, ackermann, -1, 0)
    raises(ValueError, ackermann, 0, -1)
    for n in range(5):
        assert_equal(ackermann(0, n), n + 1)
        assert_equal(ackermann(1, n), n + 2)
        assert_equal(ackermann(2, n), 2*n + 3)
        assert_equal(ackermann(3, n), 2**(n + 3) - 3)
def Test_univariate():
    data = (
        ((1, 1, 2, 5, 15, 52, 203, 877, 4140, 21147, 115975, 678570,
            4213597, 27644437), bell),
        ((1, 1, 2, 5, 14, 42, 132, 429, 1430, 4862, 16796, 58786,
        208012), catalan),
        ((0, 1, 1, 2, 3, 5, 8, 13, 21, 34, 55, 89, 144), fibonacci),
        ((2, 1, 3, 4, 7, 11, 18, 29, 47, 76, 123, 199, 322, 521,
            843, 1364, 2207), lucas),
        ((1, 0, 1, 2, 9, 44, 265, 1854, 14833, 133496, 1334961,
        14684570, 176214841, 2290792932), NumberOfDerangements),
    )
    for answers, func in data:
        for n in range(len(answers)):
            assert_equal(func(n), answers[n])
def Test_stirling():
    for f1, f2 in ((stirling1, Stirling1), (stirling2, Stirling2)):
        for n in range(10):
            for k in range(n):
                assert_equal(f1(n, k), f2(n, k))

if __name__ == "__main__":
    exit(run(globals())[0])
