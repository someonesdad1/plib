'''
Contains various routines related to prime numbers and factoring.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        ##∞copyright∞# Copyright (C) 2011 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        #
        ##∞what∞#
        ##∞test∞# --test #∞test∞#
        pass
    if 1:  # Standard imports
        import collections
        import itertools
        import math
        import operator
        import subprocess
        import sys
        from functools import reduce
    if 1:  # Custom imports
        have_bitarray = False
        try:
            # The bitarray module is used for fast bitfield manipulations.  If you get
            # version 3.7 or later, it also includes a bitarray.util.gen_primes() method
            # that is a fast sieve for primes.  bitarry is fast because it's in compiled
            # C code.  https://github.com/ilanschnell/bitarray
            from bitarray.util import ones, gen_primes
            have_bitarray = True
        except ImportError:
            pass
        from wrap import dedent
        from color import t
        from multiset import Multiset
    if 1:  # Global variables
        ii = isinstance
        t.prime = t.redl
        t.number = t.skyl
        nl = "\n"
        __all__ = '''AllFactors Factor FactorList FormatFactors IsPrime
                     PrimeList PrimeNumberSieve Primes FactorGenerator
                  '''.split()
        d = {"-c": False}
if 1:  # Core functionality
    def IsPositiveInteger(n, msg):
        if n < 1 or not ii(n, int):
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
        if check and factors and reduce(operator.mul, factors) != n:
            raise RuntimeError("Bug in Factor for n = %d" % n)
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
        factors = sorted(list(FactorGenerator(n, big=big)))
        if check and factors and reduce(operator.mul, factors) != n:
            raise RuntimeError("Bug in FactorList for n = %d" % n)
        if not factors and incl_if_prime:
            return [n]
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
            "Return integer exp as string of exponent characters"
            return "".join([e[i] for i in str(exp)])
        IsPositiveInteger(n, "n must be an integer > 0")
        if factor_dict is not None:
            D = factor_dict
        else:
            D = Factor(n)
        if not D:
            return f"{t.prime}{n}{t.n}" if d["-c"] else f"{n}"
        keys = sorted(list(D.keys()))
        N, s = f"{t.number}{n}{t.n}: ", []
        for key in keys:
            if D[key] > 1:
                if plain:
                    # s.append("%d^%d" % (key, D[key]))
                    s.append(f"{key}^{D[key]}")
                else:
                    s.append(f"{key}{E(D[key])}")
            else:
                s.append("%d" % key)
        char = " " if plain else "·"
        return N + char.join(s)
    def AllFactors(n, big=True):
        "Return a list of all factors of n if n is not prime"
        IsPositiveInteger(n, "n must be an integer > 0")
        assert n > 1
        factors = list(FactorGenerator(n, big=big))
        all_factors = set(factors)
        for num_factors in range(2, len(factors)):
            for comb in itertools.combinations(factors, num_factors):
                all_factors.add(reduce(operator.mul, comb))
        return list(sorted(list(all_factors)))
    def Primes(n):
        'Returns a list of primes < n'
        # Install bitarray version 3.7 or later for faster performance
        IsPositiveInteger(n, "n must be an integer > 0")
        if have_bitarray:
            if 0:   # Use sieve of Eratosthenes if don't have bitarray 3.7
                a = ones(n)     # bitarray of all ones
                a[:2] = False   # Zero and one are not prime
                for i in range(2, math.isqrt(n) + 1):
                    if a[i]:    # i is prime, so all multiples are not
                        a[i*i::i] = False
                return [i for i in range(2, n) if a[i]]
            else:
                # Need to be >= version 3.7 of bitarray to have bitarray.util.gen_primes().
                # This is efficient because the work is done in compiled C code.
                if not hasattr(Primes, "bitarray") or Primes.n < n:
                    # Construct a list of primes < n
                    if n > int(1e9):
                        msg = "Warning:  possible long delay in primes.Primes()"
                        t.print(f"{t.ornl}{msg}", file=sys.stderr)
                    # Get a bitarray of the odd primes
                    Primes.n = n
                    ba = gen_primes(n + 1, odd=True)
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
    def Reduce(*integers):
        '''Return a tuple of the input integers with common factors removed.
        This implementation requires the multiset on PyPi:  'pip install multiset'.
        Examples:
            Reduce(*(1, 2, 4, 8)) returns (1, 2, 4, 8).
            Reduce(*(2, 6, 8, 2)) returns (1, 3, 4, 1).
            Reduce(*(300, 400)) returns (3, 4).
            Reduce(*(6, 8, 10)) returns (3, 4, 5).
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
        common_factors = Multiset(FactorList(integers[0], incl_if_prime=True))
        for i in integers[1:]:
            common_factors &= Multiset(FactorList(i, incl_if_prime=True))
        # Remove these common factors
        results = list(integers)
        if common_factors:
            # Note when you iterate over a multiset, you'll get all the factors
            for factor in common_factors:
                results = [i//factor for i in results]
        return tuple(results)

if __name__ == "__main__":
    # If run as a script, list primes and factors.
    from lwtest import Assert, run, raises
    import getopt
    from columnize import Columnize
    if 1:   # Test routines
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
            s = FormatFactors(168)
            expected = '\x1b[38;2;175;223;255m168\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m: 2³·3·7'
            Assert(s == expected)
            s = FormatFactors(168, plain=True)
            expected = '\x1b[38;2;175;223;255m168\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m: 2^3 3 7'
            Assert(s == expected)
            s = FormatFactors(13)
            expected = '\x1b[38;2;255;1;1m13\x1b[38;2;192;192;192m\x1b[48;2;0;0;0m\x1b[0m'
            Assert(s == expected)
        def Test_AllFactors():
            s = AllFactors(2)
            Assert(s == [])
            s = AllFactors(120)
            Assert(s == [2, 3, 4, 5, 6, 8, 10, 12, 15, 20, 24, 30, 40, 60])
        def Test_Reduce():
            raises(ValueError, Reduce, *(0, 1))   # Has 0 element
            for s in (tuple(), (1,), (2,), (4,), (1, 2, 3)):
                r = Reduce(*s)
                Assert(r == s)
            #
            k = (1, 1, 1)
            for i in range(2, 20):
                s = [2*j for j in k]
                r = Reduce(*s)
                Assert(r == k)
            #
            s = (2, 4, 12, 8, 4, 2)
            r = Reduce(*s)
            Assert(r == (1, 2, 6, 4, 2, 1))
    if 1:  # Utility
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
              -b        Compact form (output is on one line)
              -C        Print in columns
              -c        Do not print in color
              -t        Run self-tests
              -p        Only show the primes
              -u        Use plain ASCII printout (i.e., no Unicode exponents)
            Examples
              - Show the factors of 64:
                  {name} 64 64
              - Show all primes less than 1000:
                  {name} 1000 | grep -v ":"
              - Show all numbers less than 100000 that have 911 as a factor:
                  {name} 100000 | grep "\<911\>"
            ''')
            )
            exit(1)
        def ParseCommandLine(d):
            d["-b"] = False     # Compact
            d["-C"] = False     # Print in columns
            d["-c"] = True      # Use color
            d["-d"] = False     # Debug sent to stderr
            d["-p"] = False     # Only show primes
            d["-u"] = True      # Use Unicode exponents
            if len(sys.argv) < 2:
                Usage()
            try:
                opts, args = getopt.getopt(sys.argv[1:], "bCcdhptu")
            except getopt.GetoptError as e:
                print(str(e))
                exit(1)
            for o, a in opts:
                if o[1] in list("bCcdpu"):
                    d[o] = not d[o]
                elif o in ("-h", "--help"):
                    Usage(status=0)
                elif o == "-t":     # Run selftests
                    exit(run(globals(), halt=True)[0])
            if not d["-c"]:
                t.prime = t.number = ""
                t.on = False
            return args
    if 1:
        d = {}  # Options dictionary
        args = ParseCommandLine(d)
        if len(args) == 1:
            m, n = 2, int(args[0])
        else:
            m, n = [int(i) for i in args]
        if m < 1 or n < 1:
            raise ValueError("n and m must be integers greater than 0")
        u = "" if d["-p"] else ","
        end = f"{u} " if d["-b"] else "\n"
        o = []
        if d["-p"]:
            # This is pretty speedy, as it gives the primes less than 1 billion in
            # 1.7 seconds.
            L = PrimeList(m, n)
            if d["-C"]:
                for i in Columnize(str(j) for j in L):
                    print(i)
            else:
                for i in L:
                    print(i)
        else:
            for i in range(m, n + 1):
                if i == n:
                    end = ""
                s = FormatFactors(i) if d["-u"] else FormatFactors(i, plain=True)
                if d["-p"]:  # Primes only
                    if ":" in s:
                        continue
                o.append(s)
                if not d["-C"]:
                    print(s, end=end)
            if d["-C"]:
                for i in Columnize(o):
                    print(i)
            elif d["-p"]:
                print()
