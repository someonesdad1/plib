'''
TODO
    Change the functions to a class, which allows the state to be saved
    with the function.  This makes them thread safe if a lock is used
    for each instance.

    ------------------------------------------------------------

    These functions generate combinations and permutations in lexical
    order.

    WARNING:  These functions are not reentrant!

    If you must use these functions with multiple threads, you'll have
    to develop thread-safe storage for the global variables.  One way to
    do this would be to change the function signatures so that you pass
    in a list of the globals needed.

    The python algorithms here were implemented to return one
    combination or permutation with each call to a function.  These are
    intended to be used with schemes to exhaustively search all
    combinations or permutations of some problem without having to
    generate a large list or file of the combinatorial data.

    Note 20 Sep 2010:  The routines in this module are obsoleted by the
    combinations() and permutations() methods of the itertools module.
    Also note the URLs given below do not work anymore; I had last
    accessed them when solving the "Einstein" fish puzzle in February of
    2002.

    A quick comparison of comb(100, 4) with GetCombination() versus
    itertools.combinations() shows itertools is about 23 times faster.
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2005 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <math> Generate combinations and permutations in lexical order.
    # Derived from C code by Glenn Rhoads.  Note they are not
    # thread-safe.
    #∞what∞#
    #∞test∞# #∞test∞#
    pass
if 1:   # Imports
    import sys
if 1:   # Global variables
    # The following global variables are used to save the state within the
    # routines so that they can be called once for each combination or
    # permutation.
    #
    # Globals for the combination routine
    c_jx = 0
    c_array = []
    c_0_based = 0
    # Globals for the permutation routine
    p_ix = 0
    p_jx = 0
    p_array = []
    p_0_based = 0
def GetCombination(n, k, init=0, zero_based=0):
    '''Each call will return a tuple of the next combination of n items
    taken k at a time.  The procedure for use is:
 
        1.  Call with init == 1.  This will return a list of the integers
            from 1 to k in their initial order.
        2.  Subsequent calls with init == 0 will return a list of k integers
            that is next in the sequence of k combinations of n items.
        3.  All the combinations have been returned when the function
            returns None.
 
    If you wish the returned tuple of numbers to be zero based (which is
    handy for selecting items from python sequences), set zero_based to
    1 on the initialization call.
 
    This routine is adapted from a C routine given at
    http://remus.rutgers.edu/~rhoads/Code/lex_comb.c, which is a C
    implementation by Glenn C. Rhoads of an algorithm from "Combinatorial
    Algorithms" by Reingold, Nievergelt, Deo.
    '''
    assert(n > 0 and k > 0 and n >= k)
    global c_jx, c_array, c_0_based
    if init:
        c_array = list(range(k+1))
        c_jx = 1
        c_0_based = zero_based
        if zero_based:
            c_0_based = 1
            return tuple(map(lambda x: x-1, c_array[1:]))
        else:
            return tuple(c_array[1:])
    if c_jx:
        c_jx = k
        while c_array[c_jx] == n - k + c_jx:
            c_jx = c_jx - 1
        if c_jx == 0:
            return None
        c_array[c_jx] = c_array[c_jx] + 1
        for ix in range(c_jx+1, k+1):
            c_array[ix] = c_array[ix-1] + 1
        if c_0_based:
            return tuple(map(lambda x: x-1, c_array[1:]))
        else:
            return tuple(c_array[1:])
    else:
        return None
def PrintArray(array, stream, num_places):
    if num_places == 0:
        fmt = "%d "
    else:
        fmt = "%%%dd " % num_places
    for num in array:
        stream.write(fmt % num)
    stream.write("\n")
def GetPermutation(n, init=0, zero_based=0):
    '''Each call will return a tuple of the next permutation of n items
    The procedure for use is:
 
        1.  Call with init == 1.  This will return a tuple of the integers
            from 1 to k in their initial order.
        2.  Subsequent calls with init == 0 will return a tuple of k integers
            that is next in the sequence of permutations of n items.
        3.  All the permutations have been returned when the function
            returns None.
 
    If you wish the returned tuple of numbers to be zero based (which is
    handy for selecting items from python sequences), set zero_based to
    1 on the initialization call.
 
    This routine is adapted from a C routine given at
    http://remus.rutgers.edu/~rhoads/Code/perm_lex.c:
 
        /* generating permutations lexicographic order */
        /* Algorithm due to Dijkstra.
        C Implementation by Glenn C. Rhoads */
 
        #include <stdio.h>
        #include <stdlib.h>
 
        int main(void)
        {
            int i, j, r, s, temp, n;
            int *pi;
 
            printf("Enter n: ");
            scanf("%d", &n);
 
            pi = malloc((n+1) * sizeof(int));
 
            for (i=0; i <= n; i++)
                pi[i] = i;
 
            i = 1;
 
            while (i)
            {
                for (i=1; i <= n; i++)
                    printf(" %2d", pi[i]);
                printf("\n");
 
                i = n-1;
                while (pi[i] > pi[i+1])
                    i--;
 
                j = n;
                while (pi[i] > pi[j])
                    j--;
 
                temp  = pi[i];
                pi[i] = pi[j];
                pi[j] = temp;
 
                r = n;
                s = i+1;
                while (r > s)
                {
                    temp = pi[r];
                    pi[r] = pi[s];
                    pi[s] = temp;
                    r--; s++;
                }
            }
        }
    '''
    assert(n > 0)
    global p_ix, p_jx, p_array, p_0_based
    if init:
        p_array = list(range(n+1))
        p_ix = 1
        if zero_based:
            p_0_based = 1
            return tuple(map(lambda x: x-1, p_array[1:]))
        else:
            return tuple(p_array[1:])
    if p_ix:
        p_ix = n - 1
        while p_array[p_ix] > p_array[p_ix+1]:
            p_ix = p_ix - 1
        p_jx = n
        while p_array[p_ix] > p_array[p_jx]:
            p_jx = p_jx - 1
        temp = p_array[p_ix]
        p_array[p_ix] = p_array[p_jx]
        p_array[p_jx] = temp
        r = n
        s = p_ix + 1
        while r > s:
            temp = p_array[r]
            p_array[r] = p_array[s]
            p_array[s] = temp
            r = r - 1
            s = s + 1
        if p_array[1] != 0:
            if p_0_based:
                return tuple(map(lambda x: x-1, p_array[1:]))
            else:
                return tuple(p_array[1:])
        else:
            return None
    else:
        return None
def P(n, stream=sys.stdout, num_places=3):
    '''Print all n permutations to a stream.  n is the number of objects
    to permute, stream is the stream to print the permutations to, and
    num_places is the width of the integer field.
 
    Example:  P(3) prints:
        1   2   3
        1   3   2
        2   1   3
        2   3   1
        3   1   2
        3   2   1
    whereas P(3, sys.stdout, 1) prints
        1 2 3
        1 3 2
        2 1 3
        2 3 1
        3 1 2
        3 2 1
    '''
    PrintArray(GetPermutation(n, 1), stream, num_places)
    array = GetPermutation(n, 0)
    while array:
        PrintArray(array, stream, num_places)
        array = GetPermutation(n, 0)
def C(n, k, stream=sys.stdout, num_places=3):
    '''Print all (n, k) combinations to a stream.  n is the number of the
    items to choose from, k is the number of items in the combination,
    stream is where the combinations get printed, and num_places is the
    width of the integer field.
 
    Examples:  C(5, 2) prints
        1   2
        1   3
        1   4
        1   5
        2   3
        2   4
        2   5
        3   4
        3   5
        4   5
    C(5, 2, sys.stdout, 1) prints
        1 2
        1 3
        1 4
        1 5
        2 3
        2 4
        2 5
        3 4
        3 5
        4 5
    '''
    PrintArray(GetCombination(n, k, 1), stream, num_places)
    array = GetCombination(n, k, 0)
    while array:
        PrintArray(array, stream, num_places)
        array = GetCombination(n, k, 0)
def permute(s):
    '''Return all possible permutations of sequence s.  Adapted from the
    mathutil.py file in the utilities from
    http://linux.softpedia.com/progDownload/pyutil-Download-44044.html.
    This code was put under the GPL by the author and is Copyright (c)
    2005-2009 by Zooko Wilcox-O'Hearn.
 
    Note that for lists of size 10 or above you'll probably find the
    execution time to be excessive; it would be better to use the
    generator-based solution given below.  However, this is a nice
    use of recursion and yields an easy-to-understand method, although
    the permutations aren't in lexicographic order as Rhoads' routines
    are.
    '''
    if len(s) == 1:
        return [s]
    res = []
    for i in range(len(s)):
        s2 = list(s[:])
        x = s2.pop(i)
        for s3 in permute(s2):
            s3.append(x)
            res.append(s3)
    return res
def permute_g(s, use_generator=True):
    '''Generator form of permute() above.  Example of use:
    for i in permute_g(range(3)):
        print i
    produces:
        [2, 1, 0]
        [1, 2, 0]
        [2, 0, 1]
        [0, 2, 1]
        [1, 0, 2]
        [0, 1, 2]
    '''
    if len(s) == 1:
        yield [s[0]]
    res = []
    for i in range(len(s)):
        s2 = list(s[:])
        x = s2.pop(i)
        for s3 in permute(s2):
            s3.append(x)
            yield s3
