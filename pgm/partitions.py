'''
Generate partitions of the integer n

    Performance:  on my 10-year-old computer under python 3.11.5 under WSL, it takes 19 s to
    calculate 'p partitions.py 70 &>/dev/null'.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2014 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Generate partitions of the integer n
        #∞what∞#
        #∞test∞# #∞test∞#
        pass
    if 1:   # Imports
        import getopt
        import sys
        from math import pi, exp, sqrt
        from collections import OrderedDict, defaultdict
    if 1:   # Custom imports
        from wrap import dedent
        from f import flt
        from columnize import Columnize
if 1:   # Utility
    def Error(*msg, status=1):
        print(*msg, file=sys.stderr)
        exit(status)
    def Usage(status=1):
        print(dedent(f'''
        Usage:  {sys.argv[0]} n [k]
          Generate the partitions of integer n.  If k is present, then the integers returned are <= k.
          The partitions of an integer n are the sets of integers <= n that sum to n.  Example:
          the partitions of 3 are 3, 2 1, 1 1 1.  In abbreviated form, this is 3, 2 1, 1³.
 
          The number of partitions grows rapidly with n.  Ramanujan's upper bound is 
          exp(pi*sqrt(2*n/3))/(4*n*sqrt(3)).  For n = 20, this is 692; for n = 200, it's 4✕10¹²,
          for n = 1000 it's 2✕10³¹.
        Options:
            -a      Output in abbreviated form
            -c      Columnize the abbreviated form (implies -a)
            -u      Estimate number of partitions of n (Ramanujan's upper bound)
        '''))
        exit(status)
    def ParseCommandLine(d):
        d["-a"] = False     # Output in abbreviated form
        d["-c"] = False     # Columnize the abbreviated form
        d["-u"] = False     # Upper bound estimate
        if len(sys.argv) < 2:
            Usage()
        try:
            opts, args = getopt.getopt(sys.argv[1:], "acu") 
        except getopt.GetoptError as e:
            print(str(e))
            exit(1)
        for o, a in opts:
            if o[1] in list("acu"):
                d[o] = not d[o]
        if d["-c"]:
            d["-a"] = True
        return args
if 1:  # Core functionality
    def partitions(n, k=None):
        '''Generator for partitions of the integer n.  For each iteration, a list of integers that sum
        to n is returned.  If k is an integer > 0, then the returned lists are limited to integers <=
        k.  If k is None, then the lists may contain integers up to n.
        '''
        for d in partitions_cs(n, k):
            # d will be an OrderedDict of integer keys with their repetition count as values.  Convert
            # this to a tuple of integers.
            result = []
            for i in d:
                result += [i]*d[i]
            assert sum(result) == n
            yield result
    def partitions_cs(n, k=None):
        '''This is Chris Smith's modification of Tim Peters' fast algorithm based on a dictionary.  If
        k is defined, then the partitions returned are limited to integers of value k or less; if k is
        None, then integers up to n are returned.
     
        See http://code.activestate.com/recipes/218332 for the discussion & algorithms.
        ----------------------------------------------------------------------------------------------
    
        Generate all partitions of integer n (>= 0) using integers no greater than k (default, None,
        allows the partition to contain n).
     
        Each partition is represented as a multiset, i.e. a dictionary mapping an integer to the number
        of copies of that integer in the partition.  For example, the partitions of 4 are {4: 1}, {3:
        1, 1: 1}, {2: 2}, {2: 1, 1: 2}, and {1: 4} corresponding to [4], [1, 3], [2, 2], [1, 1, 2] and
        [1, 1, 1, 1], respectively.  In general, sum(k*v for k, v in a_partition.iteritems()) == n, and
        len(a_partition) is never larger than about sqrt(2*n).
     
        Note that the _same_ dictionary object is returned each time.  This is for speed:  generating
        each partition goes quickly, taking constant time independent of n. If you want to build a list
        of returned values then use .copy() to get copies of the returned values:
     
        >>> p_all = []
        >>> for p in partitions(6, 2):
        ...    p_all.append(p.copy())
        ...
        >>> print(p_all)
        [{2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]
     
        Modified from Tim Peter's posting to accommodate a k value: http://code.activestate.com/recipes/218332/
        '''
        if n < 0:
            raise ValueError("n must be >= 0")
        if k is not None and k < 1:
            raise ValueError("k must be > 0")
        if n == 0:
            yield {}
            return
        if k is None or k > n:
            k = n
        q, r = divmod(n, k)
        ms = OrderedDict(((k, q),))
        keys = [k]
        if r:
            ms[r] = 1
            keys.append(r)
        yield ms
        while keys != [1]:
            # Reuse any 1's.
            if keys[-1] == 1:
                del keys[-1]
                reuse = ms.pop(1)
            else:
                reuse = 0
            # Let i be the smallest key larger than 1.  Reuse one instance of i.
            i = keys[-1]
            newcount = ms[i] = ms[i] - 1
            reuse += i
            if newcount == 0:
                del keys[-1], ms[i]
            # Break the remainder into pieces of size i - 1.
            i -= 1
            q, r = divmod(reuse, i)
            ms[i] = q
            keys.append(i)
            if r:
                ms[r] = 1
                keys.append(r)
            yield ms
    def RamanujaUpperBound(n):
        "Ramanujan's upper bound https://code.activestate.com/recipes/218332/#c2"
        return int(exp(pi*sqrt(2*n/3))/(4*n*sqrt(3)))
    def GetShortForm(lst):
        '''lst is a list of the integers making the partition.  Return the short string form.
        Example:  [5, 1, 1, 1, 1, 1] is a partition of 10; the returned string will be
        "5 1⁵".
        '''
        ss = dict(zip("0123456789", "⁰¹²³⁴⁵⁶⁷⁸⁹"))
        o = defaultdict(int)    # Count the integers in lst
        for i in lst:
            o[i] += 1
        q = []
        for i in reversed(sorted(o)):
            s = str(i)
            if o[i] > 1:
                for j in str(o[i]):
                    s += ss[j]
            q.append(s)
        return ' '.join(q)

if __name__ == "__main__":
    d = {}      # Options dictionary
    args = ParseCommandLine(d)
    try:
        n = int(args[0])
        k = None
        if n <= 0:
            raise Exception()
    except Exception:
        Error(f"{args[0]!r} is not an integer > 0")
    N = RamanujaUpperBound(n)
    ub = flt(N)
    ub.N = 1
    ub.u = True
    s = ""
    if n > 50:
        s = f"({ub.sci})"
    rub = f"Ramanujan's upper bound for number of partitions of {n} = {N} {s}"
    if d["-u"]:
        print(rub)
        exit(0)
    if len(args) == 2:
        try:
            k = int(args[1])
            if not (1 <= k <= n):
                raise Exception()
        except Exception:
            Error(f"{args[1]!r} is not an integer between 1 and {n}")
    if d["-c"]:
        count, o = 0, []
        for i in partitions(n, k):
            o.append(GetShortForm(i))
            count += 1
        for i in Columnize(o, sep=" | "):
            print(i)
        print(rub)
        print(f"Actual count = {count}")
    else:
        count = 0
        for i in partitions(n, k):
            if d["-a"]:
                print(GetShortForm(i))
            else:
                print(' '.join([str(j) for j in i]))
            count += 1
        print(rub)
        print(f"Actual count = {count}")
