"""
Prints out facts about integers
"""

if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        # ∞copyright∞# Copyright (C) 2010 Don Peterson #∞copyright∞#
        # ∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        # ∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        # ∞license∞#
        # ∞what∞#
        # Prints out facts about integers
        # ∞what∞#
        # ∞test∞# #∞test∞#
        pass
    if 1:  # Standard imports
        from functools import reduce
        import functools
        import getopt
        import itertools
        import math
        import operator
        import os
        import random
        import string
        import sys
    if 1:  # Custom imports
        from wrap import dedent
        from color import TRM as t
        import primes
    if 1:  # Global variables

        class g:
            pass

        g.max_num_to_use = 100  # For sum of squares and cubes
        # The following variable holds a list of primes
        g.primes = None
        # The following variable determines how large of a number we can factor;
        # this number will be the square of the largest prime less than max_prime.
        g.max_prime = int(1e6)
if 1:  # Utility

    def GetColors():
        # Colors for printing
        if d["-c"]:
            g.w = g.n = g.pr = g.fa = g.f = g.lg = g.b = g.r = ""
        else:
            g.w = t("whtl")  # General label
            g.n = t("yell")  # Number
            g.pr = t("lip")  # Is a prime
            g.fa = t("grnl")  # Factors
            g.f = t("magl")  # Factorization
            g.lg = t("royl")  # Logarithms
            g.b = t("trq")  # Bases
            g.r = t("pnk")  # Roots

    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)

    def Usage(status):
        print(
            dedent(f"""
        Usage:  {sys.argv[0]} [options] num1 [num2 ...]
          Prints out information on the integers num1, num2, ...
        Options
            -a n    Print the data out for the numbers 2 to n.  The other numbers
                    on the command line are ignored.
            -c      Use colors
            -f      Print out the all factors line if number is not prime
            -o      Print the sum of squares and cubes on one line.
            -P      Print out only primes with -a option
            -p      Print out only non-primes with -a option
            -o      Print the sum of squares and cubes on one line.
            -s n    Calculates sums of squares and cubes that are equal to the
                    number.  n is the maximum number to use.  The computation time
                    can be long if n is significantly above 100.
            -t      Include triple sums in sums of squares and cubes.
        """)
        )
        exit(status)

    def ParseCommandLine():
        d["-a"] = None  # All numbers from 2 to n
        d["-c"] = False  # Use color
        d["-f"] = False  # Only show all factors line
        d["-o"] = False  # Sum of squares & cubes on one line
        d["-P"] = False  # Only print out primes with -a
        d["-p"] = False  # Only print out non-primes with -a
        d["-s"] = None  # Calculate sums of squares and cubes
        d["-t"] = False  # Include triple sums
        if len(sys.argv) < 2:
            Usage(1)
        try:
            optlist, args = getopt.getopt(sys.argv[1:], "a:cfoPps:t")
        except getopt.GetoptError as str:
            msg, option = str
            print(msg)
            sys.exit(1)
        for o, a in optlist:
            if o[1] in "cfoPpt":
                d[o] = not d[o]
            elif o == "-a":
                try:
                    d[o] = int(a)
                    if d[o] < 2:
                        raise ValueError
                except ValueError:
                    Error(f"-a argument must be integer > 1")
            elif o == "-s":
                try:
                    d[o] = int(a)
                    if d[o] < 2:
                        raise ValueError
                except ValueError:
                    Error(f"-a argument must be integer > 1")
        if not args and d["-a"] is None:
            Usage()
        if d["-P"] and d["-p"]:
            Error("Can only use one of -p and -P")
        GetColors()
        return args


if 1:  # Core functionality

    def Search(n, k):
        N = g.max_num_to_use

        def Find(n, power):
            m = power
            for i in range(1, N + 1):
                for j in range(i, N + 1):
                    if i**m + j**m == n:
                        print("  %d^%d + %d^%d\n" % (i, m, j, m))
                    if j**m - i**m == n:
                        print("  %d^%d - %d^%d\n" % (j, m, i, m))

        print(str(n) + "\n")
        for i in range(2, k + 1):
            Find(n, i)

    def GetPrimeFactors(n):
        """Get the prime factors of n.  The items returned are:
            - A boolean; if True, the number was factorable (it will be false
              if n is too large to factor).
            - A boolean; if True, the number is prime.
            - A string representing the prime factorization.
            - A list of the actual factors (will be empty if n is prime).
        Note:  we use int around elements from the prime array because it's
        possible that they're numpy integers and we want python integers.
        """
        num, msg, factorable, is_prime = (
            n,
            f"  {g.w}Prime factorization:{t.n}",
            True,
            False,
        )
        if primes.IsPrime(n):
            return True, True, f"  {g.pr}Is a prime number{t.n}", []
        factor_dict = primes.Factor(n)
        factors = []
        for factor in factor_dict:
            factors += [factor] * factor_dict[factor]
        s = primes.FormatFactors(n, factor_dict=factor_dict).split(":")[1]
        s = " * ".join(s.split())
        msg += f" {g.f}" + s + f"{t.n}"
        return (factorable, is_prime, msg, factors)

    def AllFactors(n, factors):
        """Construct a string representing all the factors of n, given the
        prime factors of n in the list factors.
        """
        assert len(factors) > 1
        all_factors = set([])
        for factor in factors:
            all_factors.add(factor)
        for num_factors in range(2, len(factors)):
            for comb in itertools.combinations(factors, num_factors):
                all_factors.add(reduce(operator.mul, comb))
        numbers = list(all_factors)
        numbers.sort()
        msg = "  All factors [%d]:  " % len(all_factors) + str(numbers).replace(
            "[", ""
        ).replace("]", "")
        m = " ".join(str(i) for i in numbers)
        msg = f"  {g.w}All Factors [{len(all_factors)}]:  {g.fa}{m}{t.n}"
        return msg

    def Factors(n):
        "Print out all factors of n"
        factorable, is_prime, msg, factors = GetPrimeFactors(n)
        print(msg)
        if factorable and not is_prime:
            # Make a list of all nonprime factors
            if 1 or d["-f"]:
                print(AllFactors(n, factors))
            else:
                print(str(AllFactors(n, factors)).replace("L", ""))

    def Logarithms(n):
        l, ln, l2 = math.log10(n), math.log(n), math.log(n) / math.log(2)
        print(
            f"  {g.lg}Logarithms:  log = %.10f, ln = %.10f, log2 = %.10f{t.n}"
            % (l, ln, l2)
        )

    def DecimalToBase(num, base):
        """Convert a decimal integer num to a string in base base.  Tested with
        random integers from 10 to 10,000 digits in bases 2 to 36 inclusive.
        """
        if not 2 <= base <= 36:
            raise ValueError("Base must be between 2 and 36.")
        if num == 0:
            return "0"
        s, sign, n = "0123456789abcdefghijklmnopqrstuvwxyz", "", abs(num)
        if num < 0:
            sign, num = "-", abs(num)
        d, in_base = dict(zip(range(len(s)), list(s))), ""
        while num:
            num, rem = divmod(num, base)
            in_base = d[rem] + in_base
        # Check our conversion with python's built-in conversion.  Comment this
        # line out for slightly better performance.
        assert int(in_base, base) == n
        return sign + in_base

    def Bases(n):
        bases = (2, 3, 8, 12, 16, 36)
        print(f"  {g.b}Bases:  ", end="")
        for base in bases:
            base_str = DecimalToBase(n, base)
            assert int(base_str, base) == n
            print("%d:%s " % (base, base_str), end="")
        print(f"{t.n}")

    def Search(n, max_number_to_use=100):
        N = g.max_num_to_use

        def Find(n, power):
            m = power
            for i in range(1, N + 1):
                for j in range(i, N + 1):
                    if i**m + j**m == n:
                        print("  %d^%d + %d^%d\n" % (i, m, j, m))
                    if j**m - i**m == n:
                        print("  %d^%d - %d^%d\n" % (j, m, i, m))

        print(str(n) + "\n")
        for i in range(2, k + 1):
            Find(n, i)

    def Sums(n):
        """Print out any sums of squares or sum of cubes (up to three terms) or
        difference of squares or cubes that compose n.
        """
        N, s = d["-s"], []  # N is the max number to use
        if d["-o"]:
            a, b = "", ""
        else:
            a, b = "    ", "\n"
        if n > 3 * N**3:
            return
        for i in range(1, N + 1):
            for j in range(i, N + 1):
                if i * i + j * j == n:
                    s.append("%s%d^2 + %d^2%s" % (a, i, j, b))
                if j * j - i * i == n:
                    s.append("%s%d^2 - %d^2%s" % (a, j, i, b))
                if i * i * i + j * j * j == n:
                    s.append("%s%d^3 + %d^3%s" % (a, i, j, b))
                if j * j * j - i * i * i == n:
                    s.append("%s%d^3 - %d^3%s" % (a, j, i, b))
                if d["-t"]:  # Triple sums
                    for k in range(i, N + 1):
                        if i * i + j * j + k * k == n:
                            s.append("%s%d^2 + %d^2 + %d^2%s" % (a, i, j, k, b))
                        if i * i * i + j * j * j + k * k * k == n:
                            s.append("%s%d^3 + %d^3 + %d^3%s" % (a, i, j, k, b))
        if s:
            msg = "  Sum of squares/cubes (terms < %d): " % N
            if d["-o"]:
                print(msg, ", ".join(s))
            else:
                print(msg)
                print("".join(s).rstrip())

    def Roots(n):
        print(f"  {g.r}Roots:  ", end="")
        for i in range(2, 10):
            print("%d:%.3f " % (i, math.pow(n, 1 / i)), end="")
        print(f"{t.n}")

    def Factorial(n):
        """When n > 50, we'll print a floating point approximation."""
        print("  Factorial:  ", end="")
        if n > 170:
            # We need to print the logarithm of the factorial because the
            # factorial is too large for a float.  We use the formula for ln n!
            # from http://en.wikipedia.org/wiki/Stirling%27s_approximation
            f = n * math.log(n) - n + math.log(2 * math.pi * n) / 2
            f += 1 / (12 * n) - 1 / (360 * n**3) + 1 / (1260 * n**5) - 1 / (1680 * n**7)
            # Convert to base 10 log
            f /= math.log(10)
            print("log = ", f, "(too large for floating point)")
        else:
            f = math.factorial(n)
            if n > 50:
                # Only show floating point form and log
                print(str(float(f)), " log = ", math.log10(float(f)))
            else:
                print(f, " log = ", math.log10(float(f)))

    def CheckNumber(number):
        try:
            n = int(number)
            if n < 2:
                print("Numbers must be positive integers > 2", file=sys.stderr)
                exit(1)
            else:
                return n
        except ValueError:
            print(f"'{number}' isn't an integer", file=sys.stderr)
            return None

    def PrintProperties(n):
        print(f"{g.n}{n}{t.n}")
        Bases(n)
        Logarithms(n)
        Factors(n)
        Roots(n)
        Factorial(n)
        if d["-s"]:
            Sums(n)


if __name__ == "__main__":
    d = {}  # Dictionary for command line options
    numbers = ParseCommandLine()
    g.primes = primes.Primes(g.max_prime)
    if d["-a"] is not None:
        for n in range(2, d["-a"] + 1):
            is_prime = primes.IsPrime(n)
            if d["-p"]:
                # Print if non-prime
                if not is_prime:
                    PrintProperties(n)
            elif d["-P"]:
                # Print if prime
                if is_prime:
                    PrintProperties(n)
            elif d["-f"]:
                if not primes.IsPrime(n):
                    s = " ".join(str(i) for i in primes.AllFactors(n))
                    print(f"{n}: {s}")
            else:
                PrintProperties(n)
    elif d["-f"]:
        for number in numbers:
            n = CheckNumber(number)
            if n is None:
                continue
            s = " ".join(str(i) for i in primes.AllFactors(n))
            print(f"{n}: {s}")
    else:
        for number in numbers:
            n = CheckNumber(number)
            if not n:
                continue
            PrintProperties(n)
