'''
Prints out combinations & permutations of command line arguments.
'''
 
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Prints comb/perm of command line arguments
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Standard imports
    import getopt
    from pathlib import Path as P
    import math
    import sys
    from itertools import combinations, permutations
    from pdb import set_trace as xx
if 1:   # Custom imports
    from columnize import Columnize
    from wrap import wrap, dedent
    from color import t
    from f import flt
    try:
        import mpmath
        from mpmath.libmp import to_str
        have_mpmath = True
    except ImportError:
        have_mpmath = False
    if 0:
        import debug
        debug.SetDebugger()
if 1:   # Global variables
    ii = isinstance
if 1:   # Utility
    def Manpage():
        print(dedent(f'''
        Print the permutations of the letters 'rgb'
            python perm.py rgb
            prints
                rgb rbg grb gbr brg bgr
                6 permutations
        Print the permutations of the letters 'rgbhsv' taken 3 at a time
            python perm.py -k 3 rgbhsv
            prints
                rgb rbv rsh grh ...
                rgh rhg rsv grs ...
                ...
                120 permutations
        Print the combinations of the letters 'rgbhsv' taken 3 at a time
            python comb.py -k 3 rgbhsv
            prints
                rgb rgs rgv rbh rbs ...
                rgh
                20 combinations
        '''))
        exit(0)
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        which = "combinations" if comb else "permutations"
        formula = "C(n, k)" if comb else "P(n, k)"
        k = None if comb else "n"
        print(dedent(f'''
        Usage:  {sys.argv[0]} [options] A [B...]
          Prints out {which} of command line arguments.  A is a string and if the only argument,
          then its letters are used as the elements.  Otherwise the set of n arguments (A, B, ...)
          is used.  If the number of the results is larger than 10!, the calculation time is long,
          so just the numbers will be printed unless -f is used.
        Notation
          n = number of letters in A or number of arguments if > 1
          k = items to take for each subset'''))
        if comb:
            print(dedent(f'''
            C(n, k) = combinations of n objects taken k at a time
                    = n!/((n - k)!*k!)''', n=10))
        else:
            print(dedent(f'''
            P(n, k) = all permutations of the size k subsets taken from
                      all the n elements
                    = n!/(n - k)!
            P(n)    = P(n, n) = n!''', n=10))
        print(dedent(f'''
        Options (default in square brackets):
          -c      Don't print in columns
          -f      Print output even if number of items is large (over 10!)
          -h      Print some examples
          -k k    Number of objects in {formula} [{k}]
          -q      Quote the output strings
          -s x    Separator string for grouped items [""]
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-c"] = True      # Print in columns
        d["-f"] = False     # Force output for large numbers
        d["-k"] = None      # Choose number
        d["-q"] = False     # Quote output strings
        d["-s"] = ""        # Separator string
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "cfhk:qs:", "help")
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        global n, k
        n = len(args[0]) if len(args) == 1 else len(args)
        for o, a in opts:
            if o[1] in list("cfq"):
                d[o] = not d[o]
            elif o == "-k":
                d[o] = k = int(a)
                if k < 1 or k > n:
                    Error(f"k must be between 1 and {n}")
            elif o == "-s":
                d[o] = a
            elif o in ("-h", "--help"):
                Manpage()
        return args
if 1:   # Core functionality
    def Work(func, name, objects):
        k, count = d["-k"], 0
        if k is None and func == combinations:
            Error(f"Must use -k option with {name}")
        out = []
        for i in func(objects, k):
            t = d["-s"].join(i)
            if d["-q"]:
                t = f"'{t}'"
            out.append(t)
            count += 1
        if d["-c"]:
            for i in Columnize(out):
                print(i)
        else:
            for i in out:
                print(i)
        print(f"{count} {name}")
    def Factorial(n):
        '''Compute the factorial for n, which can be an integer or float.  If mpmath is available, 
        n can be as large as 1e308 and a result can be returned.  
 
        If mpmath is not available, then
        math.factorial is used and n can be 1558 or less.  However, to convert math.factorial(n) to
        a float, n must be 170 or less to be able to fit into a float.
 
        For math.factorial, the largest argument n allowed is 9_223_372_036_854_775_807 or 9e19.
        Even at a rate of 1e9 numbers per sec calculation rate, this would take over 316 years to
        complete, so it's not a feasible calculation.
        '''
        if have_mpmath:
            try:
                return mpmath.factorial(n)  # Returns mpmath.mpf
            except Exception:
                return mpmath.fac(n)        # Returns mpmath.mpf and uses Stirling's approximation
        else:
            return math.factorial(int(n))
    def GetHowManyObjects(objects, k):
        '''Calculate the number of combinations or permutations of the sequence objects taken k at
        a time.  This will return an integer, float, or mpmath.mpf.
        '''
        n = len(objects)
        if have_mpmath:
            f, F = mpmath.factorial, mpmath.fac
            try:
                if k is None:
                    p = f(n)
                else:
                    p = f(n)/f(n - k)
            except Exception:
                if k is None:
                    p = F(n)
                else:
                    p = F(n)/F(n - k)
            p = p/f(k) if comb else p
            assert ii(p, mpmath.mpf)
        else:
            if n > 9223372036854775807:
                raise ValueError("Number of objects must be no more than 9223372036854775807")
            try:
                if k is None:
                    p = math.factorial(n)
                else:
                    p = math.factorial(n)//math.factorial(n - k)
            except Exception:
                print("{n} objects is too many to compute factorial")
                exit(1)
            p = p//f(k) if comb else p
            assert ii(p, int)
        return p
    def Magnitude(n):
        assert(ii(n, int) and n > 0)
        s = str(n)
        m, e = s[0], len(s)
        e = len(s)
        return f"{m}e{e}"

if 0:
    comb = False
    n = 100000
    print(GetHowManyObjects([1]*n, n//2))
    exit()

if __name__ == "__main__":
    # Options dictionary
    d = {"name": P(sys.argv[0]).name.replace(".py", "")}
    comb = True if d["name"] == "comb" else False
    n, k = None, None   # These will be gotten in ParseCommandLine
    args = ParseCommandLine(d)
    too_many = math.factorial(10)
    objects = list(args[0]) if len(args) == 1 else args
    N = GetHowManyObjects(objects, k)
    large = True if N >= too_many else False
    if d["-f"]:
        large = False   # Ignore the size
    if large:
        if ii(N, int):
            e = Magnitude(N)
        elif ii(N, (float, flt)):
            e = flt(N).sci
        elif have_mpmath and ii(N, mpmath.mpf):
            e = to_str(N._mpf_, 3, min_fixed=2, max_fixed=1, show_zero_exponent=True)
    l = f"Answer too large (limit is {Magnitude(too_many)}):  "
    # This script handles both combinations and permutations
    if d["name"] == "perm":
        if large:
            print(f"{l}number of permutations = {e}")
        else:
            Work(permutations, "permutations", objects)
    else:
        if large:
            print(f"{l}number of combinations = {e}")
        else:
            Work(combinations, "combinations", objects)
