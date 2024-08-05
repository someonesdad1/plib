'''

ToDo
    - Add smatrix class
        - Simple matrices from sequences:  for manipulation only
        - Uses flat sequences with a size or a nested sequence
        - Primarily to get transpose, as this is an often-needed use case
            - Let m be a matrix, m.t is transpose
            - for i in m.t.rows:
                - Then i is a row vector you can do something with
            - But then 
                - for i in m.cols: 
                    - do something with column
                - is exactly what's desired
                - m.cols returns an iterator
        - Rows and columns are lists with an extra attribute
            - This allows e.g. two columns a = [1, 2, 3] and b = [4, 5, 6] to be combined using 
              a + b to result in the matrix [a.t, b.t].
        - row() and col() methods to get stated rows and columns
        - Holds arbitrary objects, so numpy isn't a good choice
        - Aim at composition and decomposition, not numerical computation
        - Constructor
            - Sequence:  produces row vector by default; use column kw for column vector
            - Sequence with matrix size tuple:  produces matrix
            - Nested sequence:  produces 2D matrix

Functions for dealing with sequences.
'''
if 1:  # Header
    if 1:  # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Functions for dealing with sequences
        #∞what∞#
        #∞test∞# run #∞test∞#
        pass
    if 1:   # Standard imports
        import bisect
        import operator
    if 1:   # Custom imports
        from f import flt
        from lwtest import Assert, raises
        from wrap import dedent
        if 0:
            import debug
            debug.SetDebugger()
    if 1:   # Global variables
        class G:
            pass
        g = G()
        g.dbg = True
        ii = isinstance
if 1:   # Utility
    def GetColors():
        t.err = t("redl")
        t.dbg = t("lill") if g.dbg else ""
        t.N = t.n if g.dbg else ""
    def GetScreen():
        'Return (LINES, COLUMNS)'
        return (
            int(os.environ.get("LINES", "50")),
            int(os.environ.get("COLUMNS", "80")) - 1
        )
    def Dbg(*p, **kw):
        if g.dbg:
            print(f"{t.dbg}", end="")
            print(*p, **kw)
            print(f"{t.N}", end="")
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
            # Get list of differences from x.  Note this can be slow for big sequences because it
            # creates another list.
            Dbg(f"GetClosest(seq = {seq})")
            o = [abs(distance(i, x)) for i in seq]
            if g.dbg:
                Dbg(f"  List of differences from x = {x}\n    {t('denl')}[", end="")
                out = []
                for i in o:
                    out.append(f"{i}")
                Dbg(f"{t('denl')}{', '.join(out)}", end="")
                Dbg(f"{t('denl')}]")
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
            if g.dbg:
                Dbg(f"{t('ornl')}  Answer = {seq[index]}")
            return seq[index]
        else:
            # Use binary search on a sorted array
            sseq = seq if is_sorted else sorted(seq, key=key)
            if x <= sseq[0]:
                return sseq[0]
            elif x >= sseq[-1]:
                return sseq[-1]
            else:
                # Use binary search
                l = find_le(x, sseq)    # l is sseq element, not index
                r = find_ge(x, sseq)    # r is sseq element, not index
                if l == r:
                    return l
                else:
                    diff_low, diff_high = abs(x - l), abs(x - r)
                    return l if diff_low <= diff_high else r

if __name__ == "__main__":  
    from functools import partial
    from color import t
    g.dbg = True
    GetColors()
    g.dbg = False   # Turn g.dbg on to see debug printing
    def Test_GetClosest():
        low, high = -3, 6
        seq = (4, low, high, 1)     # Unsorted sequence
        sseq = (low, 1, 4, high)    # Sorted sequence
        if 1:   
            # Test for each type of is_sorted.  This makes sure they each get the same results,
            # except when the unresolved keyword is different.
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
        if 1:   
            # Test with objects that are more complicated than numbers.  Here, the objects are 2D
            # Cartesian points with the Euclidean distance as the metric.
            class Pt:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
                def __eq__(self, other):
                    return self.x == other.x and self.y == other.y
                def __str__(self):
                    return f"Pt({self.x}, {self.y})"
                def __repr__(self):
                    return str(self)
                def dist(self, other):
                    x = (self.x - other.x)**2
                    y = (self.y - other.y)**2
                    return flt((x + y)**0.5)
            seq = (Pt(0, 0), Pt(-3, 6), Pt(4, 8), Pt(2, 0))
            f = partial(GetClosest, is_sorted=None)
            metric = lambda a, b: a.dist(b)
            Assert(f(Pt(0.1, 0.1), seq, distance=metric) == Pt(0, 0))
            Assert(f(Pt(-0.1, -0.1), seq, distance=metric) == Pt(0, 0))
            Assert(f(Pt(-100, 0.1), seq, distance=metric) == Pt(-3, 6))
            Assert(f(Pt(0, 1000), seq, distance=metric) == Pt(4, 8))
            Assert(f(Pt(1, 0), seq, distance=metric) == Pt(0, 0))
            Assert(f(Pt(1.0001, 0), seq, distance=metric) == Pt(2, 0))

    Test_GetClosest()
