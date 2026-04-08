'''
Contains various routines related to prime numbers and factoring.
'''
if 1:  # Header
    if 1:  # Standard imports
        import collections
        import getopt
        import itertools
        import math
        import operator
        import subprocess
        import sys
        from functools import reduce
    if 1:  # Custom imports
        from columnize import Columnize
        from wrap import dedent
        import dparith
        import trm
    if 1:  # Global variables
        t = trm.TrmDP()
        t.prime = t.redl
        t.number = t.skyl
        nl = "\n"
        d = {"-c": False}
if 1:   # Core functionality
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
            opts, args = getopt.getopt(sys.argv[1:], "bCcdhpu", "test")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("bCcdpu"):
                d[o] = not d[o]
            elif o in ("-h", "--help"):
                Usage(status=0)
            elif o == "--test":     # Run selftests
                exit(run(globals(), halt=True)[0])
        if not d["-c"]:
            t.prime = t.number = ""
            t.on = False
        return args
if __name__ == "__main__": 
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
        L = dparith.PrimeList(m, n)
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
            s = dparith.FormatFactors(i) if d["-u"] else dparith.FormatFactors(i, plain=True)
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
