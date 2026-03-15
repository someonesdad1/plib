
'''
Various arithmetic things
    
    Stirling1       Stirling numbers of the first kind
    Stirling2       Stirling numbers of the second kind
    FactorGenerator Returns the prime factors an integer n
    PrimeList       Returns a list of the primes that are between n and m inclusively
    PrimeNumberSieve    Infinite generator that returns primes
    IsPrime         Return True if n is prime
    Factor          Return a dictionary of the factors of n
    FactorList      Return a sorted list of the prime factors of n
    FormatFactors   Returns a string of the prime factors of n
    AllFactors      Return a list of the prime and composite factors of n
    Primes          Returns a list of primes < n
    RemoveCommonFactors  Return a tuple of the input integers with common factors removed

'''
if 1:  # Header
    if 1:  # Standard imports
        import collections
        import functools
        import itertools
        import math
        import operator
        import subprocess
        import sys
    if 1:  # Custom imports
        import multiset
        
        import dptypes
        import trm
        _have_bitarray = False
        try:
            # The bitarray module is used for fast bitfield manipulations.  If you get
            # version 3.7 or later, it also includes a bitarray.util.gen_primes() method
            # that is a fast sieve for primes.  bitarray is fast because it's in compiled
            # C code.  https://github.com/ilanschnell/bitarray
            import bitarray.util
            _have_bitarray = True
        except ImportError:
            pass
    if 1:  # Import symbols
        pass
    if 1:  # Global variables
        g = dptypes.Constant()
        t = trm.Trm()
if 1:  # Core functionality
    def IsPositiveInteger(n, msg):
        if not isinstance(n, int) or n < 1:
            raise ValueError(msg)
    def FactorGenerator(n, big=True):
        '''A generator that returns the prime factors an integer n.  If big is True,
        then the routine uses /usr/bin/factor to allow factoring much bigger numbers
        than a sieve can handle.  However, using /usr/bin/factor forks a process and 
        it will be slow if you want to factor a bunch of numbers; in the latter case,
        set big to False.
        '''
        IsPositiveInteger(n, "n must be an integer > 0")
        if not big:
            # Get a list of possible factors that are primes less than n.  Then reverse
            # the list and test each factor to see if it divides n.
            for i in reversed(Primes(n)):
                while n > 1 and n % i == 0:
                    yield i  # i is a factor of n
                    n //= i
                if n == 1:
                    break
        else:
            # Use /usr/bin/factor to do the work
            cmd = ["/usr/bin/factor", str(n)]
            r = subprocess.run(cmd, capture_output=True)
            if r.returncode:
                raise ValueError(f"{n!r} couldn't be factored (returned {r.returncode})")
            s = r.stdout.decode().split()
            s.pop(0)    # Get rid of the first term with ':'
            if len(s) == 1:
                return None # Integer is prime
            else:
                for i in s:
                    yield int(i)
    def PrimeList(m, n):
        'Return a list of the primes that are between n and m inclusively'
        IsPositiveInteger(n, "n must be an integer > 0")
        IsPositiveInteger(m, "m must be an integer > 0")
        n, m = (m, m) if m > n else (n, m)
        return [i for i in Primes(n + 1) if m <= i <= n]
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
                D[q*q] = q
                if n and q > n:
                    break
                yield q
            else:
                x = p + q
                while x in D or not (x & 1):
                    x += p
                D[x] = p
    def IsPrime(n, fast=False):
        '''Return True if n is prime; False otherwise.  If fast is True, then a sieve is
        used instead of /usr/bin/factor.
        '''
        IsPositiveInteger(n, "n must be an integer > 0")
        return False if Factor(n, big=not fast) else True
    def Factor(n, check=False, big=True, return_tuple=False):
        '''Return a dictionary of the factors of n; the values are the power of each
        factor.  If a number is prime, an empty dictionary is returned.  If check is
        True, the calculated factors are multiplied together to verify that the original
        number is gotten.  big is passed to FactorGenerator to use /usr/bin/factor.
        If return_tuple is True, return a tuple of the factors.
        '''
        IsPositiveInteger(n, "n must be an integer > 0")
        if n < 4:
            return {}
        factors, d = list(FactorGenerator(n, big=big)), collections.defaultdict(int)
        if return_tuple:
            return tuple(factors)
        if check and factors and functools.reduce(operator.mul, factors) != n:
            raise RuntimeError(f"Bug in Factor for n = {n}")
        if factors == [n]:
            return dict(d)  # n is prime
        for i in factors:  # Populate d with factors
            d[i] += 1
        return dict(d)
    def FactorList(n, check=False, incl_if_prime=False, big=True):
        '''Return a sorted list of the prime factors of n.  The list will be empty if n
        is prime.  If check is True, the calculated factors are multiplied together to
        verify that the original number is gotten.  big is passed to FactorGenerator to
        use /usr/bin/factor.
        
        If incl_if_prime is True and n is prime, then n will be returned.  This handles
        the case when you're looking for the common factors of a set of integers and you
        need the factor even if it's prime.  Example:  get the common factors of (2, 6,
        8).  FactorList(2) returns an empty list, but in this case you'd want it to
        return 2, so you'd use FactorList(2, incl_if_prime=True).
        '''
        IsPositiveInteger(n, "n must be an integer > 0")
        prime_factors = sorted(list(FactorGenerator(n, big=big)))
        if check and prime_factors and functools.reduce(operator.mul, prime_factors) != n:
            raise RuntimeError(f"Bug in FactorList for n = {n}")
        if not prime_factors and incl_if_prime:
            return [n]
        return prime_factors
    def FormatFactors(n, plain=False, factor_dict=None):
        '''Returns a string of the prime factors of n.  The form is e.g.  '168:
        2³·3·7'.  If n is prime, just the number is returned with no colon
        character.  If factor_dict is given, use it instead of calculating d
        again.  If plain is True, then return '168: 2^3 3 7'.  ANSI colors are
        used unless output is not to a terminal.
        '''
        e = dict(zip(list("0123456789"), list("⁰¹²³⁴⁵⁶⁷⁸⁹"), strict=True))
        def E(exp):
            "Return integer exp as string of exponent characters"
            return "".join([e[i] for i in str(exp)])
        IsPositiveInteger(n, "n must be an integer > 0")
        if factor_dict is not None:
            D = factor_dict
        else:
            D = Factor(n)
        t.prime = t.red
        t.composite = t.skyl
        t.factors = t.pnkl
        if not D:
            return f"{t.prime}{n}{t.n}" 
        keys = sorted(list(D.keys()))
        N, s = f"{t.composite}{n}{t.n}: ", []
        for key in keys:
            if D[key] > 1:
                if plain:
                    s.append(f"{t.factors}{key}^{D[key]}")
                else:
                    s.append(f"{t.factors}{key}{E(D[key])}")
            else:
                s.append(f"{t.factors}{key}")
        char = " " if plain else "·"
        return N + char.join(s)
    def AllFactors(n, big=True, split=False):
        '''Return a list of the prime and composite factors of n if split is False.  If
        split is True, return (A, B) where A is a list of the prime factors of n and B
        is a list of all the composite factors of n.  Both lists will be empty if n is
        prime.
        '''
        IsPositiveInteger(n, "n must be an integer > 0")
        assert n > 1
        prime_factors = list(FactorGenerator(n, big=big))
        composite_factors = set()
        for num_factors in range(2, len(prime_factors)):
            for comb in itertools.combinations(prime_factors, num_factors):
                composite_factors.add(functools.reduce(operator.mul, comb))
        composite = list(sorted(list(composite_factors)))
        if split:
            return (prime_factors, composite)
        else:
            return list(sorted(set(prime_factors + composite)))
    def Primes(n):
        'Returns a list of primes < n'
        # Install bitarray version 3.7 or later for faster performance
        IsPositiveInteger(n, "n must be an integer > 0")
        if _have_bitarray:
            if 0:   # Use sieve of Eratosthenes if don't have bitarray 3.7
                a = bitarray.util.ones(n)     # bitarray of all ones
                a[:2] = False   # Zero and one are not prime
                for i in range(2, math.isqrt(n) + 1):
                    if a[i]:    # i is prime, so all multiples are not
                        a[i*i::i] = False
                return [i for i in range(2, n) if a[i]]
            else:
                # Need to be >= version 3.7 of bitarray to have bitarray.util.gen_primes().
                # This is efficient because the work is done in compiled C code.  Call
                # it once and cache in Primes.primes.
                if not hasattr(Primes, "bitarray") or Primes.n < n:
                    # Construct a list of primes < n
                    if n > int(1e9):
                        msg = "Warning:  possible long delay in primes.Primes()"
                        t.print(f"{t.ornl}{msg}", file=sys.stderr)
                    # Get a bitarray of the odd primes
                    Primes.n = n
                    ba = bitarray.util.gen_primes(n + 1, odd=True)
                    Primes.primes = [2] + [2*i + 1 for i in range(n) if ba[i]]
                    del ba
                return [i for i in Primes.primes if i < n]
        else:
            # From https://stackoverflow.com/questions/2068372/ ...
            #      fastest-way-to-list-all-primes-below-n/33356284#33356284
            # Downloaded 20 Nov 2023
            zero = bytearray([False])
            size = n//3 + (n % 6 == 2)
            sieve = bytearray([True])*size
            sieve[0] = False
            for i in range(int(n**0.5)//3 + 1):
                if sieve[i]:
                    k = 3*i + 1 | 1
                    start = (k*k + 4*k - 2*k*(i & 1))//3
                    sieve[(k*k)//3::2*k] = zero*((size - (k*k)//3 - 1)//(2*k) + 1)
                    sieve[start::2*k] = zero*((size - start - 1)//(2*k) + 1)
            ans = [2, 3]
            poss = itertools.chain.from_iterable(
                itertools.zip_longest(*[range(i, n, 6) for i in (1, 5)]))
            ans.extend(itertools.compress(poss, sieve))
            return ans
    def RemoveCommonFactors(*integers):
        '''Return a tuple of the input integers with common factors removed.
        This implementation requires the multiset on PyPi:  'pip install multiset'.
        Examples:
            RemoveCommonFactors(*(1, 2, 4, 8)) returns (1, 2, 4, 8).
            RemoveCommonFactors(*(2, 6, 8, 2)) returns (1, 3, 4, 1).
            RemoveCommonFactors(*(300, 400)) returns (3, 4).
            RemoveCommonFactors(*(6, 8, 10)) returns (3, 4, 5).
        '''
        # Special cases
        if not integers or len(integers) == 1:
            return integers
        # Check parameters
        for i in integers:
            if not isinstance(i, int):
                raise TypeError(f"{i!r} is not an integer")
            if i < 1:
                raise ValueError(f"{i!r} is < 1")
        # Get the common set of factors
        common_factors = multiset.Multiset(FactorList(integers[0], incl_if_prime=True))
        for i in integers[1:]:
            common_factors &= multiset.Multiset(FactorList(i, incl_if_prime=True))
        # Remove these common factors
        results = list(integers)
        if common_factors:
            # Note when you iterate over a multiset, you'll get all the factors
            for factor in common_factors:
                results = [i//factor for i in results]
        return tuple(results)
if 1:   # Stirling numbers
    def Stirling1(n, k):
        '''Returns the Stirling number of the first kind.
        The recurrence relation is s(n+1, k) = s(n, k-1) - n*s(n, k) for k
        running from 1 to n.
        '''
        # Can be decorated with debug.Memoized to cache calls if used a lot
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
        return Stirling1(n - 1, k - 1) - (n - 1)*Stirling1(n - 1, k)
    def Stirling2(n, k):
        '''Returns the Stirling number of the second kind.
        The recurrence relation is S(n, k) = S(n - 1, k - 1) + k*S(n - 1, k).  The
        Stirling number of the second kind is the number of ways of partitioning a set
        of n objects into k-sized subsets.
        '''
        # Can be decorated with debug.Memoized to cache calls if used a lot
        if not isinstance(n, int) or n < 0 or not isinstance(k, int) or k < 0:
            raise ValueError("n and k must be integers >= 0")
        if k <= 1 or k == n:
            return 1
        elif k > n or n <= 0:
            return 0
        return Stirling2(n - 1, k - 1) + k*Stirling2(n - 1, k)

if __name__ == "__main__":
    # If run as a script, list primes and factors.

    from lwtest import Assert, raises, run
    def Test_Primes():
        s = "2 3 5 7 11 13 17 19 23 29 31 37 41 43 47 53 59 61 67 71 73 79 83 89 97"
        primes = [int(i) for i in s.split()]
        max = 100
        # Check that Primes() constructs an identical list to primes
        our_primes = Primes(max)
        Assert(primes == our_primes)
        # Check that our generator matches those in the above list
        n = 0
        for prime in PrimeNumberSieve(max):
            Assert(IsPrime(prime))
            Assert(prime == primes[n])
            n += 1
    def Test_FactorGenerator():
        for i in (2, 3, 5, 11, 13, 17, 19):
            Assert(list(FactorGenerator(i)) == [])
        #Assert(list(FactorGenerator(20)) == [5, 2, 2])
        Assert(list(FactorGenerator(20)) == [2, 2, 5])
    def Test_PrimeList():
        #Assert(list(PrimeList(10, 20)) == [11, 13, 17, 19])
        Assert(list(PrimeList(10, 20)) == [11, 13, 17, 19])
    def Test_PrimeNumberSieve():
        Assert(list(PrimeNumberSieve(10)) == [2, 3, 5, 7])
    def Test_IsPrime():
        Assert(IsPrime(11))
        Assert(not IsPrime(10))
    def Test_Factor():
        for i in (1, 2, 3):
            d = Factor(i)
            Assert(not d)
        d = Factor(40)
        Assert(d[2] == 3)
        Assert(d[5] == 1)
        Assert(len(d) == 2)
        # Test Factor() over a reasonable number range
        if 0:
            for i in range(2, 10000):
                Factor(i, check=True)
    def Test_FactorList():
        for i in (1, 2, 3):
            d = FactorList(i)
            Assert(not d)
        d = FactorList(2, incl_if_prime=True)
        Assert(d == [2])
        d = FactorList(4)
        Assert(d == [2, 2])
    def Test_FormatFactors():
        on = t.on
        t.on = False    # Turn off escape codes
        s = FormatFactors(168)
        expected = '168: 2³·3·7'
        Assert(s == expected)
        s = FormatFactors(168, plain=True)
        expected = '168: 2^3 3 7'
        Assert(s == expected)
        s = FormatFactors(13)
        expected = '13'
        Assert(s == expected)
        t.on = on
    def Test_AllFactors():
        s = AllFactors(2)
        Assert(s == [])
        s = AllFactors(120)
        Assert(s == [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60])
        # Test with split
        s = AllFactors(100, split=True)
        Assert(s == ([2, 2, 5, 5], [4, 10, 20, 25, 50]))
    def Test_RemoveCommonFactors():
        raises(ValueError, RemoveCommonFactors, *(0, 1))   # Has 0 element
        for s in (tuple(), (1,), (2,), (4,), (1, 2, 3)):
            r = RemoveCommonFactors(*s)
            Assert(r == s)
        #
        k = (1, 1, 1)
        for i in range(2, 20):
            s = [2*i*j for j in k]
            r = RemoveCommonFactors(*s)
            #print(s, r)
            Assert(r == k)
        #
        s = (2, 4, 12, 8, 4, 2)
        r = RemoveCommonFactors(*s)
        Assert(r == (1, 2, 6, 4, 2, 1))
    def Test_Stirling1():
        '''Numbers from https://oeis.org/A008275 (See the triangle down
        next to EXAMPLE).
        '''
        n = 1
        expected = (0, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 2
        expected = (0, -1, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 3
        expected = (0, 2, -3, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 4
        expected = (0, -6, 11, -6, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 5
        expected = (0, 24, -50, 35, -10, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 6
        expected = (0, -120, 274, -225, 85, -15, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 7
        expected = (0, 720, -1764, 1624, -735, 175, -21, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
        n = 8
        expected = (0, -5040, 13068, -13132, 6769, -1960, 322, -28, 1)
        for k in range(1, n):
            Assert(Stirling1(n, k) == expected[k])
    def Test_Stirling2():
        '''Numbers from https://oeis.org/A008277 (See the triangle down
        next to EXAMPLE).
        '''
        n = 1
        expected = (0, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 2
        expected = (0, 1, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 3
        expected = (0, 1, 3, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 4
        expected = (0, 1, 7, 6, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 5
        expected = (0, 1, 15, 25, 10, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 6
        expected = (0, 1, 31, 90, 65, 15, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 7
        expected = (0, 1, 63, 301, 350, 140, 21, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
        n = 8
        expected = (0, 1, 127, 966, 1701, 1050, 266, 28, 1)
        for k in range(1, n):
            Assert(Stirling2(n, k) == expected[k])
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])

def GetGist():
    g = {}
    g["gist"] = "Various arithmetical things (prime numbers, etc.)"
    g["copy"] = "Copyright © 2011 Don Peterson"
    g["lic"] = "MIT License (see /plib/_lic.mit)"
    g["test"] = "run"
    g["cat"] = "math"
    g["todo"] = '''

    '''
    return g
