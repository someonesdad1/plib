'''
Elementary number theory and combinatorics functions.

References
  ASPN Recipes, mathematics.py
'''

import sys

nl = "\n"
ii = isinstance

def gcd(a, b):
    '''Greatest common divisor of a and b using Euclid's algorithm.
    '''
    a, b = abs(a), abs(b)
    if not a:
        return b
    if not b:
        return a
    while b:
        a, b = b, a % b
    return a

def gcd_seq(seq):
    '''Greatest common divisor of a sequence of numbers.
    '''
    if not seq:
        return None
    r = seq[0]
    for i in range(1, len(seq)):
        r = gcd(r, seq[i])
        if r <= 1:
            break
    return r

def lcm(a, b):
    '''Least common multiple of a and b.
    '''
    if not a or not b:
        return 0
    return a*b/gcd(a, b)

def lcm_seq(seq):
    '''Least common multiple of numbers in seq.
    '''
    if not seq:
        return 0
    r = seq[0]
    for i in range(1, len(seq)):
        r = lcm(r, seq[i])
        if r <= 1:
            break
    return r

def factorial(n):
    '''Returns the factorial of n.
        n! = n * (n-1) * (n-2) * ... * 2 * 1
    '''
    if not ii(n, int):
        raise TypeError("n must be an integer")
    if n < 0:
        raise ValueError("n must be >= 0")
    p = 1
    for i in range(2, n + 1):
        p *= i
    return p
    '''Another possible implementation:
    from functools import reduce
    reduce(lambda x, y: x*y, range(1, n))
    '''

def rising_factorial(x, n):
    '''Returns value of x (x + 1) (x + 2) ... (x+n-1).
    '''
    if n < 1 or not ii(n, int):
        raise ValueError("n must be an integer >= 1")
    p = x
    for i in range(1, n):
        p *= x + i
    return p

def falling_factorial(x, n):
    '''Returns value of x (x-1) (x-2) ... (x - n + 1).
    '''
    if n < 1 or not ii(n, int):
        raise ValueError("n must be an integer >= 1")
    p = x
    for i in range(1, n):
        p *= (x - i)
    return p

def Comb(n, r):
    '''Returns the number of combinations of n things taken r at a
    time.  Note recurrence relation
        Comb(r, r) = Comb(n-1, r) + Comb(n-1, r-1)
    '''
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
        x = x*i//d
        i -= 1
    return x

def Perm(n, r):
    '''Returns the number of permutations of n things take n r at a
    time.  Note recurrence relation
        Perm(n, r) = Perm(n, r - 1) * (n - r + 1)
    '''
    if r < 1 or n < 1 or r > n:
        raise ValueError("n and r must be greater than zero and r <= n")
    x = 1
    for i in range(n - r + 1, n + 1):
        x *= i
    return x

def int_partitions(n, k=1):
    '''Returns the number of integer partitions that are >= k.
 
    Ramanujan's formula for upper bound for number of partitions of k:
        int(exp(pi*sqrt(2*n/3))/(4*n*sqrt(3)))
    '''
    total = 1
    n -= k
    while n >= k:
        total += int_partitions(n, k)
        n, k = n - 1, k + 1
    return total

def ackermann(m, n):
    '''Returns the ackermann function using recursion. (m, n are
    non-negative).'''
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
    '''Returns the nth Bell number.
    '''
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if n < 2:
        return 1
    sum = 0
    for k in range(1, n + 1):
        sum = sum + Comb(n - 1, k - 1)*bell(k - 1)
    return sum

def catalan(n):
    '''Returns the nth Catalan number.
    '''
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if n <= 1:
        return 1
    elif n == 2:
        return 2
    return (2*n)*(2*n - 1)*catalan(n - 1)//((n + 1)*n)

def fibonacci(n):
    '''Returns the nth Fibonacci number.
    '''
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if not n:
        return 0
    elif n <= 2:
        return 1
    return fibonacci(n - 1) + fibonacci(n - 2)

def lucas(n):
    '''Returns the nth lucas number.
    Recursive version:
        return lucas(n - 1) + lucas(n - 2)
    '''
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
    '''Returns the Stirling number of the first kind.
    '''
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if k < 0 or not ii(k, int):
        raise ValueError("k must be an integer >= 0")
    if not n and not k:
        return 1
    if (not k and n >= 1) or k > n:
        return 0
    return stirling1(n - 1, k - 1) - (n - 1)*stirling1(n - 1, k)

def stirling2(n, k):
    '''Returns the Stirling number of the second kind.
    '''
    if n < 0 or not ii(n, int):
        raise ValueError("n must be an integer >= 0")
    if k < 0 or not ii(k, int):
        raise ValueError("k must be an integer >= 0")
    if k <= 1 or k == n:
        return 1
    if k > n or n <= 0:
        return 0
    return stirling2(n - 1, k - 1) + k*stirling2(n - 1, k)

def NumberOfDerangements(n):
    '''Returns the number of derangements using the formula:
        d(n) = n*d(n-1) + (-1)**n
    A derangement is a permutation where each element is not in its
    natural place, or p[i] != i.
    '''
    if not n:
        return 1
    elif n == 1:
        return 0
    d, dn = -1, 0
    for i in range(2, n + 1):
        dnm1 = dn
        d = -d
        dn = i*dnm1 + d
    return dn
