'''
Functions for dealing with sequences.
'''
if 1:   # Header
    if 1:   # Standard includes
        import operator
    if 1:   # Custom includes
        from lwtest import Assert
    if 1:   # Global variables
        pass
if 1:   # Core functionality
    def GetClosest(x, seq, is_sorted=False, key=None, distance=operator.sub):
        '''Return the value in sequence seq that is closest to x.

        is_sorted
            If is_sorted is False, a sorted copy of the sequence is made and bisect.bisect_left is
            used to find the relevant insertion point.  If is_sorted is False, you must provide a
            key for the sorted() built-in if the elements don't have a relevant '<' operator.  If
            is_sorted is True, the original sequence is used.

            You can also set is_sorted to None, meaning do not use a sort sequence and the bisect
            module.  Instead, a sequence is constructed of the absolute value of the distance
            between x and each element of seq.  The index of the smallest value of this sequence
            is found and is used to return that particular sequence of seq.

        distance
            This is a binary function that returns the distance between x and a sequence element.
            This distance must be an integer or a floating point number.  This function is only
            used if is_sorted is set to None.


        '''
        if not seq:
            raise ValueError("Sequence seq cannot be empty")
        if is_sorted is None:
            # Get list of differences from x
            o = [abs(distance(i, x)) for i in seq]
            minimum = min(o)                # Minimum difference
            index = seq.index(minimum)      # Get index of minimum
            return seq[index]               # This is the closest value
        else:
            lseq = seq if is_sorted else sorted(seq, key=key)
            if x <= lseq[0]:
                return lseq[0]
            elif x >= lseq[-1]:
                return lseq[-1]
            else:
                # Use binary search
                l = bisect.bisect_left(lseq, x)
                r = bisect.bisect_right(lseq, x)
                if l == r:
                    return lseq[l]
                else:
                    diff_low, diff_high = abs(x - lseq[l]), abs(x - lseq[r])
                    return lseq[l] if diff_low <= diff_high else lseq[r]


if __name__ == "__main__":  
    def Test_GetClosest():
        seq = (0, 11, 28, 31, 40)
        if 1:   # Test with is_sorted == None
        Assert(GetClosest(-1e99, seq) == 0)
        Assert(GetClosest(-1, seq) == 0)
        Assert(GetClosest(0, seq) == 0)

    Test_GetClosest()
