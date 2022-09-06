'''
Contains various routines related to prime numbers and factors.
 
If you run this file as a script, it will print out prime numbers and
factors.
 
Note:  there is a limit to the largest prime you can factor, as you'll
get a memory error.  It is on the order of 1e9, at least on my machine.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # 
    #∞what∞#
    #∞test∞# --test #∞test∞#
    pass
if 1:   # Standard imports
    import collections
    import itertools
    import math
    import operator
    import pathlib
    import sys
    from functools import reduce
    from pdb import set_trace as xx
if 1:   # Custom imports
    from wrap import dedent
    from color import TRM as t
if 1:   # Global variables
    P = pathlib.Path
    ii = isinstance
    t.p = t("redl")
    t.N = t("grnl")
    nl = "\n"
    __all__ = '''AllFactors Factor FactorList FormatFactors IsPrime
                 PrimeList PrimeNumberSieve Primes factor_gen
              '''.split()
    d = {"-c": False}
def IsPositiveInteger(n, msg):
    if n < 1 or not ii(n, int):
        raise ValueError(msg)
def Primes(n, show=False):
    '''Returns a list of primes < n.  From
    http://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n-in-python/3035188#3035188
    The pure python method used here is named rwh_primes1.  If show is
    True, print out the sieve's contents for each iteration.
    '''
    # Times on 2.5 GHz Intel quad core:
    #     log10(n)       s        num primes
    #        6           0.4      78498
    #        7           1.0      664579
    #        8           8.3      5761455
    #        9    memory error
    IsPositiveInteger(n, "n must be an integer > 0")
    def Show(count, sieve):
        if show:
            # Make a string of 0's and 1's
            s = str([0 + i for i in sieve])
            if not count:
                # Print a ruler
                print(" " * 4, ("    .    |") * (len(sieve) // 10))
            print(
                "%3d " % count,
                s[1:-1]
                .replace(",", "")
                .replace(" ", "")
                .replace("0", " ")
                .replace("1", "x"),
            )
    sieve = [True] * (n // 2)  # Boolean array representing odd numbers
    if show:
        Show(0, sieve)
    # Iterate from 3 to sqrt(n), odd numbers only
    for i in range(3, int(n**0.5) + 1, 2):
        # If this element's value is true, then set each multiple of i to
        # false by using the proper stride.  This is very fast because it
        # will all be done in C code.  The RHS is the tricky part -- it's
        # the remaining number of items in the Boolean array.
        if sieve[i // 2]:
            sieve[i*i//2::i] = [False] * ((n - i*i - 1)//(2*i) + 1)
            if show:
                Show(i, sieve)
    return [2] + [2 * i + 1 for i in range(1, n // 2) if sieve[i]]
def factor_gen(N):
    '''This is a generator that factors an integer N.  We get a list of
    possible factors that are primes less than N.  Then we reverse the
    list and test each factor to see if it divides N.
 
    Example:  for N = 84, returns [7, 3, 2, 2].
    '''
    IsPositiveInteger(N, "N must be an integer > 0")
    n = N
    for i in reversed(Primes(n)):
        while n > 1 and n % i == 0:
            yield i  # i is a factor of n
            n //= i
        if n == 1:
            break
def PrimeList(m, n):
    '''Return a list of the primes that are between n and m inclusively.'''
    IsPositiveInteger(n, "n must be an integer > 0")
    IsPositiveInteger(m, "m must be an integer > 0")
    if m > n:
        m, n = n, m
    p = Primes(n + 1)
    # Find the last prime that is < m.  Put the lowest primes at the
    # end so we can efficiently use pop().
    p.reverse()
    while p and p[-1] < m:
        p.pop()
    p.reverse()
    return p
def PrimeNumberSieve(n=0):
    '''Provides an infinite generator that generates primes.  From
    http://code.activestate.com/recipes/577318-infinite-list-of-primes-yay/?in=lang-pythonhttp://code.activestate.com/recipes/577318-infinite-list-of-primes-yay/?in=lang-python
    If n is nonzero, the generator is terminated when it reaches n.
    '''
    if n:
        IsPositiveInteger(n, "n must be an integer > 0")
    D = {}
    yield 2
    for q in itertools.islice(itertools.count(3), 0, None, 2):
        p = D.pop(q, None)
        if p is None:
            D[q * q] = q
            if n and q > n:
                break
            yield q
        else:
            x = p + q
            while x in D or not (x & 1):
                x += p
            D[x] = p
def IsPrime(n):
    '''Return True if n is prime; False otherwise.'''
    IsPositiveInteger(n, "n must be an integer > 0")
    return False if Factor(n) else True
def Factor(n, check=False):
    '''Return a dictionary of the factors of n; the values are the power of
    each factor.  If a number is prime, an empty dictionary is returned.
    If check is True, the calculated factors are multiplied together
    to verify that the original number is gotten.
    '''
    IsPositiveInteger(n, "n must be an integer > 0")
    if n < 4:
        return {}
    factors, d = list(factor_gen(n)), collections.defaultdict(int)
    if check and factors and reduce(operator.mul, factors) != n:
        raise RuntimeError("Bug in Factor for n = %d" % n)
    if factors == [n]:
        return dict(d)  # n is prime
    for i in factors:  # Populate d with factors
        d[i] += 1
    return dict(d)
def FactorList(n, check=False):
    '''Return a sorted list of the prime factors of n.  The list will be
    empty if n is prime.  If check is True, the calculated factors are
    multiplied together to verify that the original number is gotten.
    '''
    IsPositiveInteger(n, "n must be an integer > 0")
    factors = sorted(list(factor_gen(n)))
    if check and factors and reduce(operator.mul, factors) != n:
        raise RuntimeError("Bug in FactorList for n = %d" % n)
    return factors
def FormatFactors(n, plain=False, factor_dict=None):
    '''Returns a string of the prime factors of n.  The form is e.g.  '168:
    2³·3·7'.  If n is prime, just the number is returned with no colon
    character.  If factor_dict is given, use it instead of calculating d
    again.  If plain is True, then return '168: 2^3 3 7'.  ANSI colors are
    used unless output is not to a terminal.
    '''
    e = dict(zip(list("0123456789"), list("⁰¹²³⁴⁵⁶⁷⁸⁹")))
    def E(exp): 
        'Return integer exp as string of exponent characters'
        return ''.join([e[i] for i in str(exp)])

    IsPositiveInteger(n, "n must be an integer > 0")
    if factor_dict is not None:
        D = factor_dict
    else:
        D = Factor(n)
    if not D:
        return f"{t.p}{n}{t.n}" if d["-c"] else f"{n}"
    keys = sorted(list(D.keys()))
    N, s = f"{t.N}{n}{t.n}: ", []
    for key in keys:
        if D[key] > 1:
            if plain:
                #s.append("%d^%d" % (key, D[key]))
                s.append(f"{key}^{D[key]}")
            else:
                s.append(f"{key}{E(D[key])}")
        else:
            s.append("%d" % key)
    char = " " if plain else "·"
    return N + char.join(s)
def AllFactors(n):
    '''Return a sorted tuple of all the integer factors of n; n must
    be greater than 1.
    '''
    IsPositiveInteger(n, "n must be an integer > 0")
    assert n > 1
    factors = list(factor_gen(n))
    all_factors = set(factors)
    for num_factors in range(2, len(factors)):
        for comb in itertools.combinations(factors, num_factors):
            all_factors.add(reduce(operator.mul, comb))
    numbers = list(all_factors)
    numbers.sort()
    return tuple(numbers)
if __name__ == "__main__":
    # If run as a script, list primes and factors.
    from lwtest import Assert, run
    import getopt
    def Test():
        # The following list came from
        # https://primes.utm.edu/lists/small/1000.txt, downloaded on 9 Mar
        # 2022.
        primes = [int(i) for i in '''
            2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89
            97 101 103 107 109 113 127 131 137 139 149 151 157 163 167 173 179
            181 191 193 197 199 211 223 227 229 233 239 241 251 257 263 269 271
            277 281 283 293 307 311 313 317 331 337 347 349 353 359 367 373 379
            383 389 397 401 409 419 421 431 433 439 443 449 457 461 463 467 479
            487 491 499 503 509 521 523 541 547 557 563 569 571 577 587 593 599
            601 607 613 617 619 631 641 643 647 653 659 661 673 677 683 691 701
            709 719 727 733 739 743 751 757 761 769 773 787 797 809 811 821 823
            827 829 839 853 857 859 863 877 881 883 887 907 911 919 929 937 941
            947 953 967 971 977 983 991 997 1009 1013 1019 1021 1031 1033 1039
            1049 1051 1061 1063 1069 1087 1091 1093 1097 1103 1109 1117 1123
            1129 1151 1153 1163 1171 1181 1187 1193 1201 1213 1217 1223 1229
            1231 1237 1249 1259 1277 1279 1283 1289 1291 1297 1301 1303 1307
            1319 1321 1327 1361 1367 1373 1381 1399 1409 1423 1427 1429 1433
            1439 1447 1451 1453 1459 1471 1481 1483 1487 1489 1493 1499 1511
            1523 1531 1543 1549 1553 1559 1567 1571 1579 1583 1597 1601 1607
            1609 1613 1619 1621 1627 1637 1657 1663 1667 1669 1693 1697 1699
            1709 1721 1723 1733 1741 1747 1753 1759 1777 1783 1787 1789 1801
            1811 1823 1831 1847 1861 1867 1871 1873 1877 1879 1889 1901 1907
            1913 1931 1933 1949 1951 1973 1979 1987 1993 1997 1999 2003 2011
            2017 2027 2029 2039 2053 2063 2069 2081 2083 2087 2089 2099 2111
            2113 2129 2131 2137 2141 2143 2153 2161 2179 2203 2207 2213 2221
            2237 2239 2243 2251 2267 2269 2273 2281 2287 2293 2297 2309 2311
            2333 2339 2341 2347 2351 2357 2371 2377 2381 2383 2389 2393 2399
            2411 2417 2423 2437 2441 2447 2459 2467 2473 2477 2503 2521 2531
            2539 2543 2549 2551 2557 2579 2591 2593 2609 2617 2621 2633 2647
            2657 2659 2663 2671 2677 2683 2687 2689 2693 2699 2707 2711 2713
            2719 2729 2731 2741 2749 2753 2767 2777 2789 2791 2797 2801 2803
            2819 2833 2837 2843 2851 2857 2861 2879 2887 2897 2903 2909 2917
            2927 2939 2953 2957 2963 2969 2971 2999 3001 3011 3019 3023 3037
            3041 3049 3061 3067 3079 3083 3089 3109 3119 3121 3137 3163 3167
            3169 3181 3187 3191 3203 3209 3217 3221 3229 3251 3253 3257 3259
            3271 3299 3301 3307 3313 3319 3323 3329 3331 3343 3347 3359 3361
            3371 3373 3389 3391 3407 3413 3433 3449 3457 3461 3463 3467 3469
            3491 3499 3511 3517 3527 3529 3533 3539 3541 3547 3557 3559 3571
            3581 3583 3593 3607 3613 3617 3623 3631 3637 3643 3659 3671 3673
            3677 3691 3697 3701 3709 3719 3727 3733 3739 3761 3767 3769 3779
            3793 3797 3803 3821 3823 3833 3847 3851 3853 3863 3877 3881 3889
            3907 3911 3917 3919 3923 3929 3931 3943 3947 3967 3989 4001 4003
            4007 4013 4019 4021 4027 4049 4051 4057 4073 4079 4091 4093 4099
            4111 4127 4129 4133 4139 4153 4157 4159 4177 4201 4211 4217 4219
            4229 4231 4241 4243 4253 4259 4261 4271 4273 4283 4289 4297 4327
            4337 4339 4349 4357 4363 4373 4391 4397 4409 4421 4423 4441 4447
            4451 4457 4463 4481 4483 4493 4507 4513 4517 4519 4523 4547 4549
            4561 4567 4583 4591 4597 4603 4621 4637 4639 4643 4649 4651 4657
            4663 4673 4679 4691 4703 4721 4723 4729 4733 4751 4759 4783 4787
            4789 4793 4799 4801 4813 4817 4831 4861 4871 4877 4889 4903 4909
            4919 4931 4933 4937 4943 4951 4957 4967 4969 4973 4987 4993 4999
            5003 5009 5011 5021 5023 5039 5051 5059 5077 5081 5087 5099 5101
            5107 5113 5119 5147 5153 5167 5171 5179 5189 5197 5209 5227 5231
            5233 5237 5261 5273 5279 5281 5297 5303 5309 5323 5333 5347 5351
            5381 5387 5393 5399 5407 5413 5417 5419 5431 5437 5441 5443 5449
            5471 5477 5479 5483 5501 5503 5507 5519 5521 5527 5531 5557 5563
            5569 5573 5581 5591 5623 5639 5641 5647 5651 5653 5657 5659 5669
            5683 5689 5693 5701 5711 5717 5737 5741 5743 5749 5779 5783 5791
            5801 5807 5813 5821 5827 5839 5843 5849 5851 5857 5861 5867 5869
            5879 5881 5897 5903 5923 5927 5939 5953 5981 5987 6007 6011 6029
            6037 6043 6047 6053 6067 6073 6079 6089 6091 6101 6113 6121 6131
            6133 6143 6151 6163 6173 6197 6199 6203 6211 6217 6221 6229 6247
            6257 6263 6269 6271 6277 6287 6299 6301 6311 6317 6323 6329 6337
            6343 6353 6359 6361 6367 6373 6379 6389 6397 6421 6427 6449 6451
            6469 6473 6481 6491 6521 6529 6547 6551 6553 6563 6569 6571 6577
            6581 6599 6607 6619 6637 6653 6659 6661 6673 6679 6689 6691 6701
            6703 6709 6719 6733 6737 6761 6763 6779 6781 6791 6793 6803 6823
            6827 6829 6833 6841 6857 6863 6869 6871 6883 6899 6907 6911 6917
            6947 6949 6959 6961 6967 6971 6977 6983 6991 6997 7001 7013 7019
            7027 7039 7043 7057 7069 7079 7103 7109 7121 7127 7129 7151 7159
            7177 7187 7193 7207 7211 7213 7219 7229 7237 7243 7247 7253 7283
            7297 7307 7309 7321 7331 7333 7349 7351 7369 7393 7411 7417 7433
            7451 7457 7459 7477 7481 7487 7489 7499 7507 7517 7523 7529 7537
            7541 7547 7549 7559 7561 7573 7577 7583 7589 7591 7603 7607 7621
            7639 7643 7649 7669 7673 7681 7687 7691 7699 7703 7717 7723 7727
            7741 7753 7757 7759 7789 7793 7817 7823 7829 7841 7853 7867 7873
            7877 7879 7883 7901 7907 7919'''.split()]
        if 1:
            # Check that Primes() constructs an identical list to primes
            max_prime = 7920
            our_primes = Primes(max_prime)
            Assert(primes == our_primes)
            # Check that our generator matches those in the above list
            n = 0
            for prime in PrimeNumberSieve(max_prime):
                Assert(IsPrime(prime))
                Assert(prime == primes[n])
                n += 1
            # Test Factor() over a reasonable number range
            for i in range(2, 10000):
                Factor(i, check=True)
    if 1:   # Utility
        def Error(*msg, status=1):
            print(*msg, file=sys.stderr)
            exit(status)
        def Usage():
            name = sys.argv[0]
            print(dedent(rf'''
            Usage:  {name} n [m]
              Prints primes and factors for numbers <= n or between n and m.  Each
              number is printed on a separate line with its factors; if it is prime,
              no factors and no ":" character are printed.
            Options
              -C        Compact form (output is on one line)
              -c        Do not print in color
              --test    Run self-tests
              -p        Only show the primes
              -u        Use plain ASCII printout
            Examples
              - Show the factors of 64:
                  {name} 64 64
              - Show all primes less than 1000:
                  {name} 1000 | grep -v ":"
              - Show all numbers less than 100000 that have 911 as a factor:
                  {name} 100000 | grep "\<911\>"
            '''))
            exit(1)
        def ParseCommandLine(d):
            d["-C"] = False     # Compact
            d["-c"] = True      # Use color
            d["-d"] = False     # Debug sent to stderr
            d["-p"] = False     # Only show primes
            d["-u"] = True      # Use Unicode exponents
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "Ccdhpu", "test")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("Ccdpu"):
                    d[o] = not d[o]
                elif o in ("-h", "--help"):
                    Usage(status=0)
                elif o == "--test":
                    exit(run(globals(), halt=True)[0])
            if not d["-c"]:
                t.p = t.n = t.N = ""
            return args
    if 1:
        d = {}      # Options dictionary
        args = ParseCommandLine(d)
        if len(args) == 1:
            m, n = 2, int(args[0])
        else:
            m, n = [int(i) for i in args]
        if m < 1 or n < 1:
            raise ValueError("n and m must be integers greater than 0")
        t = "" if d["-p"] else ","
        end = f"{t} " if d["-C"] else "\n"
        for i in range(m, n + 1):
            if i == n:
                end = ""
            s = FormatFactors(i) if d["-u"] else FormatFactors(i, plain=True)
            if d["-p"]:     # Primes only
                if ":" in s:
                    continue
            print(s, end=end)
        if not d["-p"]:
            print()
