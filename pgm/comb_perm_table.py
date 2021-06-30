'''
Generate a table of the number of combinations and permutations sorted
by the resulting number.  This lets you look up an integer and see if
it's equal to (or close to) a permutation or combination.

Note that the output integer is limited to numbers less than 28
factorial.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # Number of combinations and permutations table
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import mpmath as mp
    from math import factorial as fac
    from collections import defaultdict
    from pdb import set_trace as xx 
if 1:   # Custom imports
    from wrap import dedent
    from color import C as c
if 1:   # Global variables
    C = c.lyel
    P = c.lred
    N = c.norm
if __name__ == "__main__": 
    limit = fac(28)
    max_number = 100
    d = defaultdict(list)
    perm = lambda x: int(mp.fac(x))
    comb = lambda n, m:  int(mp.fac(n)/(mp.fac(n - m)*mp.fac(m)))
    for n in range(max_number + 1):
        d[perm(n)].append(f"{P}[{n}]{N}")
        for m in range(1, n//2):
            d[comb(n, m)].append(f"{C}({n}, {m}){N}")
    print(f"Number of combinations {C}(n, m){N} and permutations {P}[n]{N}")
    for key in sorted(d):
        if key and key <= limit:
            print(f"{key:,d}  {key:.0e}  ", end="")
            for i in d[key]:
                print(i, end=" ")
            print()
