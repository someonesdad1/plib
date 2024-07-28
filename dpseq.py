'''
Functions for dealing with sequences.
'''
if 1:   # Header
    if 1:   # Standard includes
        import bisect
        import operator
    if 1:   # Custom includes
        from lwtest import Assert, raises
        if 1:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        pass
if 1:   # Core functionality
    def find_le(x, seq):
        'Find rightmost value less than or equal to x'
        # From bisect module documentation
        i = bisect.bisect_right(seq, x)
        if i:
            return seq[i-1]
        raise ValueError
    def find_ge(x, seq):
        'Find leftmost item greater than or equal to x'
        # From bisect module documentation
        i = bisect.bisect_left(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError
    def GetClosest(x, seq, is_sorted=False, key=None, distance=operator.sub, unresolved=0):
        '''Return the value in sequence seq that is closest to x.
 
        The intended common use case is where x is a number and seq is a sequence of numbers, but
        the pattern should apply to any objects that can be ordered with "<" or have the notion of
        distance between x and any of seq's elements.
 
        For best efficiency, have seq be in sorted order or allow it to be sorted, as this uses
        the bisect module to find the relevant item in O(log(n)).  Otherwise, the algorithm is
        O(n).
 
        is_sorted
            If is_sorted is False, a sorted copy of the sequence is made and bisect.bisect_left is
            used to find the relevant insertion point.  If is_sorted is False, you must provide a
            key for the sorted() built-in if the elements don't have a relevant '<' operator.  If
            is_sorted is True, the original sequence is used as is.
 
            You can also set is_sorted to None, meaning do not use bisection.  Instead, a sequence
            is constructed of the absolute value of the distance between x and each element of
            seq.  The index of the smallest value of this sequence is found and is used to return
            the corresponding element of seq.
 
        distance
            This is a binary function that returns the distance between x and a sequence element.
            This distance must be an integer or a floating point number.  This function is only
            used if is_sorted is set to None.
 
        unresolved
            An example like seq = (0, 1, 2, 3) and x = 1e99 will return the list o with all
            elements the same number, so the problem is unresolved.  If unresolved is set to an
            integer, then that array index of seq is returned in this case.  Otherwise, a
            ValueError exception is raised.

        Example:  let seq = (5, -8, 10, 1).  Then
            GetClosest(-1e99, seq) = -8
            GetClosest(-9, seq) = -8
            GetClosest(-7, seq) = -8
            GetClosest(0, seq) = 1
            GetClosest(-7, seq) = 5
            GetClosest(1e99, seq) = 10
        '''
        if not seq:
            raise ValueError("Sequence seq cannot be empty")
        if is_sorted is None:
            # Get list of differences from x
            o = [abs(distance(i, x)) for i in seq]
            minimum = min(o)                # Minimum difference
            # Get o's index of the minimum
            index = o.index(minimum)
            # Check for the special case where the question is unresolvable, as all of these
            # differences are the same number.  Example:  seq = (0, 1, 2, 3) and x = 1e99.  As
            # all of the numbers in seq subtracted from 1e99 give the same value, the problem
            # is not solvable with floating point arithmetic.  Thus, any entry from the array can
            # be returned.
            if len(set(o)) == 1:    # Problem can't be resolved
                if unresolved is not None and isinstance(unresolved, int):
                    index = unresolved
                    try:
                        seq[index]
                    except Exception:
                        raise ValueError(f"'resolved' is not an index for seq")
                else:
                    raise ValueError("Closest item is unresolvable")
            # Return the closest value
            return seq[index]
        else:
            lseq = seq if is_sorted else sorted(seq, key=key)
            # lseq is now the sorted sequence seq
            if x <= lseq[0]:
                return lseq[0]
            elif x >= lseq[-1]:
                return lseq[-1]
            else:
                # Use binary search
                l = find_le(x, lseq)    # l is lseq element, not index
                r = find_ge(x, lseq)    # r is lseq element, not index
                if l == r:
                    return l
                else:
                    diff_low, diff_high = abs(x - l), abs(x - r)
                    return l if diff_low <= diff_high else r

if __name__ == "__main__":  
    from functools import partial
    def Test_GetClosest():
        low, high = -3, 6
        seq = (4, low, high, 1)     # Unsorted sequence
        sseq = (low, 1, 4, high)    # Sorted sequence
        if 1:   # Test for each type of is_sorted
            for k in (None, False, True):
                f = partial(GetClosest, is_sorted=k)
                seq = sseq if k else seq
                if k is None:
                    raises(ValueError, f, -1e99, seq, unresolved=None)
                    raises(ValueError, f, 1e99, seq, unresolved=None)
                    Assert(f(-1e99, seq) == seq[0])
                    Assert(f(1e99, seq) == seq[0])
                else:
                    Assert(f(-1e99, seq) == low)
                    Assert(f(1e99, seq) == high)
                Assert(f(-40, seq) == low)
                Assert(f(-4, seq) == low)
                # Note x can be a float also
                Assert(f(-4., seq) == low)
                Assert(f(-3, seq) == low)
                Assert(f(-2, seq) == low)
                Assert(f(-1, seq) == low)
                Assert(f(0, seq) == 1)
                Assert(f(1, seq) == 1)
                Assert(f(2, seq) == 1)
                Assert(f(3, seq) == 4)
                Assert(f(4, seq) == 4)
                Assert(f(5, seq) == 4)
                Assert(f(6, seq) == high)
                Assert(f(7, seq) == high)
                Assert(f(20, seq) == high)
                Assert(f(100, seq) == high)

        exit()#xx

        seq = (0, 11, 28, 31, 40)
        if 1:   # Test with is_sorted == None
            f = partial(GetClosest, is_sorted=None)
            raises(ValueError, f, -1e99, seq)
            raises(ValueError, f, 1e99, seq)
            Assert(f(-1, seq) == 0)
            Assert(f(0, seq) == 0)

    Test_GetClosest()
