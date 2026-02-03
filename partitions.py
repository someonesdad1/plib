'''
Generate partitions of the integer n.
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Generate partitions of the integer n oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2014 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ math oo>
        <oo test ∞ notest oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        import sys
        from collections import OrderedDict
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Core functionality
    def partitions(n, k=None):
        '''Generator for partitions of the integer n.  For each iteration, a
        tuple of integers that sum to n is returned.  If k is an integer > 0,
        then the returned tuples are limited to integers <= k.  If k is None,
        then the tuples may contain integers up to n.
        '''
        # Timing:  on my quad Intel machine bought Feb 2011, a partition of 40
        # takes about 1.5 s ('partitions 40 >nul').  Roughly about 20% of this
        # is due to the following loop and the rest is due to Peters'
        # algorithm.  A C algorithm written by Glenn Rhoads can find partitions
        # to n = 55 in the same time.
        for d in partitions_cs(n, k):
            # d will be an OrderedDict of integer keys with their
            # repetition count as values.  Convert this to a tuple of
            # integers.
            result = []
            for i in d:
                result += [i] * d[i]
            result = tuple(result)
            assert sum(result) == n
            yield result
    def partitions_cs(n, k=None):
        '''This is Chris Smith's modification of Tim Peters' fast
        algorithm based on a dictionary.  If k is defined, then the
        partitions returned are limited to integers of value k or less; if
        k is None, then integers up to n are returned.
        
        See http://code.activestate.com/recipes/218332 for the discussion
        & algorithms.
        
        -----------------------------------------------------------------
        Generate all partitions of integer n (>= 0) using integers no
        greater than k (default, None, allows the partition to contain n).
        
        Each partition is represented as a multiset, i.e. a dictionary
        mapping an integer to the number of copies of that integer in the
        partition.  For example, the partitions of 4 are {4: 1}, {3: 1, 1:
        1}, {2: 2}, {2: 1, 1: 2}, and {1: 4} corresponding to [4], [1, 3],
        [2, 2], [1, 1, 2] and [1, 1, 1, 1], respectively.  In general,
        sum(k * v for k, v in a_partition.iteritems()) == n, and
        len(a_partition) is never larger than about sqrt(2*n).
        
        Note that the _same_ dictionary object is returned each time.
        This is for speed:  generating each partition goes quickly, taking
        constant time independent of n. If you want to build a list of
        returned values then use .copy() to get copies of the returned
        values:
        
        >>> p_all = []
        >>> for p in partitions(6, 2):
        ...         p_all.append(p.copy())
        ...
        >>> print(p_all)
        [{2: 3}, {1: 2, 2: 2}, {1: 4, 2: 1}, {1: 6}]
        
        Reference
        ---------
        Modified from Tim Peter's posting to accommodate a k value:
        http://code.activestate.com/recipes/218332/
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
            # Break the remainder into pieces of size i-1.
            i -= 1
            q, r = divmod(reuse, i)
            ms[i] = q
            keys.append(i)
            if r:
                ms[r] = 1
                keys.append(r)
            yield ms

if __name__ == "__main__":
    from wrap import dedent
    k = None
    try:
        n = int(sys.argv[1])
    except IndexError:
        print(dedent(f'''
            Usage:  {sys.argv[0]} n [k]
                Generates the partitions of integer n.  If k is present, then the
                integers returned are <= k.  Each line output has its integers sum
                to n.
        '''))
        exit(1)
    try:
        k = int(sys.argv[2])
    except IndexError:
        pass
    if k is not None and k < 1:
        print("k must be > 0")
        exit(1)
    for i in partitions(n, k):
        print(" ".join([str(j) for j in i]))
