'''
Functions for dealing with sequences.

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Functions for dealing with sequences oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2024 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ 

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
                    - This allows e.g. two columns a = [1, 2, 3] and b = [4, 5, 6] to be
                      combined using a + b to result in the matrix [a.t, b.t].
                - row() and col() methods to get stated rows and columns
                - Holds arbitrary objects, so numpy isn't a good choice
                - Aim at composition and decomposition, not numerical computation
                - Constructor
                    - Sequence:  produces row vector by default; use column kw for
                      column vector
                    - Sequence with matrix size tuple:  produces matrix
                    - Nested sequence:  produces 2D matrix

        oo>
    '''
    if 1:  # Standard imports
        from fractions import Fraction
        import bisect
        import operator
    if 1:  # Custom imports
        from f import flt
        from lwtest import Assert, raises
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
if 1:  # Core functionality
    def iDistribute(n, a, b):
        '''Generator to return an integer sequence [a, ..., b] with n elements equally distributed
        between a and b.  Raises ValueError if no solution is possible.  Example:
            a, b = 1, 6
            for n in range(2, 8):
                s = list(iDistribute(n, a, b))
                print(f"iDistribute({n}, {a}, {b}) = {s}")
        produces
            iDistribute(2, 1, 6) = [1, 6]
            iDistribute(3, 1, 6) = [1, 4, 6]
            iDistribute(4, 1, 6) = [1, 3, 4, 6]
            iDistribute(5, 1, 6) = [1, 2, 4, 5, 6]
            iDistribute(6, 1, 6) = [1, 2, 3, 4, 5, 6]
        with a ValueError exception on the n == 7 term.  For the case n == 4, note how the adjective
        "equally" needs to be interpreted "symmetrically" and for the case n == 5, even that's not
        true.
        
        If you need a sequence of n floating point values, see util.fDistribute().
        '''
        if not (isinstance(a, int) and isinstance(b, int) and isinstance(n, int)):
            raise TypeError("Arguments must be integers")
        if a >= b:
            raise ValueError("Must have a < b")
        if n < 2:
            raise ValueError("n must be >= 2")
        if n == 2:
            yield a
            yield b
            return
        dx = Fraction(b - a, n - 1)
        if dx < 1:
            raise ValueError("No solution")
        for i in range(n):
            yield int(round(a + i * dx, 0))
    def fDistribute(n, a=0, b=1, impl=float):
        '''Generator to return n impl instances on [a, b] inclusive. A common use case is an
        interpolation parameter on [0, 1].  This is for floating point numbers.  Examples:
            fd = fDistribute
            fd(3) --> [0.0, 0.5, 1.0]
            fd(3, 1, 2) --> [1.0, 1.5, 2.0]
            fd(4, 1, 2, Fraction) --> [Fraction(1, 1), Fraction(4, 3), Fraction(5, 3), Fraction(2, 1)]
            
        You can use other impl types like decimal.Decimal.  Other types that define impl()/impl() to
        return an impl-type floating point number will also work (e.g., mpmath's mpf type).
        
        If you need a sequence of evenly-distributed integers, see util.iDistribute().
        '''
        # Check arguments
        msg = "n must be an integer > 1"
        if not isinstance(n, int):
            raise TypeError(msg)
        if n < 2:
            raise ValueError(msg)
        if not isinstance(a, (int, impl)) or not isinstance(b, (int, impl)):
            raise TypeError("a and b must be either an integer or impl")
        if not (a < b):
            raise ValueError("Must have a < b")
        x0 = impl(a)
        dx = impl(b) - x0
        for i in range(n):
            x = x0 + (impl(i) / impl(n - 1)) * dx
            # Check invariants
            assert a <= x <= b
            assert isinstance(x, impl)
            # Return value
            yield x
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
            minimum = min(o)  # Minimum difference
            # Get o's index of the minimum
            index = o.index(minimum)
            # Check for the special case where the question is unresolvable, as all of these
            # differences are the same number.  Example:  seq = (0, 1, 2, 3) and x = 1e99.  As
            # all of the numbers in seq subtracted from 1e99 give the same value, the problem
            # is not solvable with floating point arithmetic.  Thus, any entry from the array can
            # be returned.
            if len(set(o)) == 1:  # Problem can't be resolved
                if unresolved is not None and isinstance(unresolved, int):
                    index = unresolved
                    try:
                        seq[index]
                    except Exception:
                        raise ValueError("'resolved' is not an index for seq")
                else:
                    raise ValueError("Closest item is unresolvable")
            # Return the closest value
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
                L = Rightmost_le(sseq, x)  # L is sseq element, not index
                r = Leftmost_ge(sseq, x)  # r is sseq element, not index
                if L == r:
                    return L
                else:
                    diff_low, diff_high = abs(x - L), abs(x - r)
                    return L if diff_low <= diff_high else r
if 1:   # Searching sorted sequences from bisect module
        # bisect_left(seq, x) partitions seq into two halves so that 
        #   all values < x on the left side
        #   all values >= x on the right side
        # bisect_right(seq, x) partitions seq into two halves so that 
        #   all values <= x on the left side
        #   all values > x on the right side
    def Leftmost_eq(seq, x):
        'Return index of the leftmost value == x'
        # index(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i != len(seq) and seq[i] == x:
            return i
        raise ValueError(f"No leftmost value == {x}")
    def Leftmost_gt(seq, x):
        'Return index of leftmost value > x'
        # find_gt(a, x) in bisect module document
        i = bisect.bisect_right(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError(f"No leftmost value > {x}")
    def Leftmost_ge(seq, x):
        'Return index of leftmost item >= x'
        # find_ge(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError(f"No leftmost value >= {x}")
    #
    def Rightmost_eq(seq, x):
        'Return index of the rightmost value == x'
        try:
            n = Rightmost_le(seq, x)
            if seq[n] == x:
                return n
            elif n < len(seq) - 1:
                return n + 1
            else:
                raise ValueError
        except ValueError:
            raise ValueError(f"No rightmost value == {x}")
    def Rightmost_lt(seq, x):
        'Return index of rightmost value < x'
        # find_lt(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i:
            return seq[i-1]
        raise ValueError(f"No rightmost value < {x}")
    def Rightmost_le(seq, x):
        'Return index of rightmost value <= x'
        # find_le(a, x) in bisect module document
        i = bisect.bisect_right(seq, x)
        if i:
            return seq[i-1]
        raise ValueError(f"No rightmost value <= {x}")
if 1:   # Get or transform numbers from a sequence
    def GetNum(seq, typ=int):
        '''Return a list of numbers found in sequence seq.  The intent is that all the
        elements of seq that can be converted to a number of type typ will be returned
        in the list.  Examples:
            seq = ("1", "2.", 3., "four")
            GetNum(seq) --> [1, 3]
            GetNum(seq, typ=float) --> [1.0, 2.0, 3.0]
            GetNum(seq, typ=Decimal) --> [Decimal(1), Decimal(2), Decimal(3)]
        '''
        def Num(x):
            try:
                return typ(x)
            except Exception:
                return None
        return [i for i in map(Num, seq) if i is not None]
    def Clamp(seq, low=0, high=1, typ=None):
        '''Generator to return elements of a sequence "clamped" to an interval.  The
        type of the returned value is typ if not None; otherwise, it's the same type as
        the element processed.

        Example:  list(Clamp((-0.02, 0.4, 1.6), low=0, high=1.5, typ=float)) returns
            [0.0, 0.4, 1.5].
        '''
        for x in seq:
            T = type(x) if typ is None else typ
            if x < low:
                yield T(low)
            elif x > high:
                yield T(high)
            else:
                yield T(x)
            
if 1:   # Finding duplicates in sequences
    if 0:   # Notes
        '''
        An obvious approach to this problem is to use the facilities of lists:
        
            def FindDuplicates(seq):
                seqcopy = list(seq)
                nodup, dup = [], []
                    item = seqcopy.pop()
                    dup.append(item) if item in seqcopy else nodup.append(item)
                return (nodup, dup)
        
        It's simple, understandable, and obviously correct.  Unfortunately it's O(n²)
        because looking at each element in the list with pop() is O(n) and the 'item in
        seqcopy' is an implicit for loop.
        
        A fix for this is to copy the sequence into a set, which has no duplicates.  Then
        we'd use
        
            def FindDuplicates(seq):
                seen = set(seq)  # Contains items in seq that are not duplicates
                n, nodup, dup = len(seqcopy), [], []
                for i in range(n):
                    item = seq[i]
                    dup.append(item) if item in seen else nodup.append(item)
                return (nodup, dup)
        
        which is also simple, understandable, obviously correct, and O(n).  An extra
        cost is more memory for the set.  Unfortunately, it fails with an exception if
        seq contains a nonhashable element.  Nonhashable things are mutable items that
        can change over time, such as lists, sets, and dictionaries.
        
        The function DupNodup below fixes this hashability problem by using a helper class
        Hashable that makes every object hashable.  The helper class uses __slots__ to
        minimize memory use.
        
            def FindDuplicates(seq):
                n, dup, nodup, seen = len(seq), [], [], set()
                for i in range(n):
                    item = seq[i]
                    sitem = Hashable(seq[i])
                    dup.append(item) if sitem in seen else nodup.append(item)
                    seen.add(sitem)
                return (nodup, dup)
        
        It's understandable, correct, and O(n) because seeing if something is in a set
        and adding an item to a set are both O(1).  The extra cost is the memory of the
        two copies of the original sequence: dup/nodup and the set.
        '''
    class Hashable:
        '''Encapsulate an object and make it hashable by defining a __hash__ method.  It
        is your responsibility to ensure that the items being stored don't change while
        being processed or you'll get incorrect results.
        '''
        __slots__ = ("object", "typ")
        def __init__(self, object, typ=False):
            '''If typ in the constructor is True, then the objects must also have the
            same type to be considered equal.
            '''
            self.object = object
            self.typ = bool(typ)
        def __hash__(self):
            # In CPython, the hash of repr(self.object) seems to work to differentiate
            # e.g. the hash of 1 and the hash of 1.0 when stored in a Hashable instance.
            # If this doesn't work (e.g. in some other python instantiation), then the
            # DupNodup() algorithm won't work correctly.
            if self.typ:
                return hash(repr(self.object))
            try:
                return hash(self.object)
            except TypeError:
                return hash(repr(self.object))
        def __eq__(self, other):
            eqval = (self.object == other.object)
            if self.typ:
                return (eqval and (type(self) is type(other)))
            return eqval
    def Nodup(seq, type_important=False):
        '''seq is a sequence; returns nodup where nodup is a list of the elements in seq
        that are not duplicates.  See DupNodup() for details.
        '''
        return DupNodup(seq, type_important=type_important)[1]
    def NodupHashable(seq):
        '''seq is a sequence; returns nodup where nodup is a list of the elements in seq
        that are not duplicates.  See DupNodupHashable() for details.
        '''
        return DupNodupHashable(seq)[1]
    def Dup(seq, type_important=False):
        '''seq is a sequence; returns dup where dup is a list of the elements in seq
        that are duplicates.  See DupNodup() for details.
        '''
        return DupNodup(seq, type_important=type_important)[0]
    def DupHashable(seq):
        '''seq is a sequence; returns dup where dup is a list of the elements in seq
        that are duplicates.  See DupNodupHashable() for details.
        '''
        return DupNodupHashable(seq)[0]
    def DupNodup(seq, type_important=False):
        '''seq is a sequence; returns (dup, nodup) where dup and nodup are lists.  nodup
        has the elements in seq that are not duplicates.  dup contains the elements that
        are duplicates of earlier elements in the list.  Both dup and nodup maintain the
        order of the elements in the original sequence.

        This function will work on arbitrary sequences.  If you know the sequence only
        contains hashable objects, use DupNodupHashable().

        If type_important is True, then itemA and itemB are defined to be duplicates iff
        both 'itemA == itemB' and 'type(itemA) is type(itemB)' expressions are True.
        This is useful in situations where e.g. you don't want the integer 1 and the
        floating point 1.0 values to be considered equal (in python, '1 == 1.0' is
        True).
        
        Examples:
            DupNodup([1, 2, 3, 1, 4, 1.0]) returns 
                nodup = [1, 2, 3, 4]
                dup   = [1, 1.0]
            because 1 == 1.0, so the second 1 and the 1.0 in seq are considered
            duplicates.

            DupNodup([1, 2, 3, 1, 4, 1.0], type_important=True) returns 
                nodup = [1, 2, 3, 4, 1.0]
                dup   = [1]
            because type_important=True means two items aren't duplicates unless they
            are equal and have the same type.
        
        Warnings
            - The algorithm in this function uses a set of the elements in seq to
              identify duplicate items.  To ensure this works with unhashable objects,
              the objects are encapsulated in the Hashable class.  For DupNodup() to
              work correctly, the contents of all the items in seq cannot change while
              DupNodup() is processing; otherwise, you'll get incorrect results.  This
              is important in programs with multiple threads, so you'd probably want to
              use a lock just before calling this function.
            - Each element of seq is accessed in a loop.  If seq is a type like a large
              deque, you may want to convert it to a list for better performance
              (accessing the middle of a deque is O(n), not like O(1) for a list).
        
        The algorithm effectively creates two copies of the list seq (one copy in dup
        and nodup and one copy in the set seen).  The extra memory of these auxiliary
        structures allows this to be an O(n) algorithm.
        '''
        n, dup, nodup, seen = len(seq), [], [], set()
        for i in range(n):
            item, sitem = seq[i], Hashable(seq[i], typ=type_important)
            dup.append(item) if sitem in seen else nodup.append(item)
            seen.add(sitem)
        return (dup, nodup)
    def DupNodupHashable(seq):
        '''seq is a sequence; returns (dup, nodup) where dup and nodup are lists.  nodup
        has the elements in seq that are not duplicates.  dup contains the elements that
        are duplicates of earlier elements in the list.  Both dup and nodup maintain the
        order of the elements in the original sequence.  You'll get a TypeError
        exception if seq contains an unhashable object.
        '''
        n, dup, nodup, seen = len(seq), [], [], set()
        for i in range(n):
            dup.append(seq[i]) if seq[i] in seen else nodup.append(seq[i])
            seen.add(seq[i])
        return (dup, nodup)

if __name__ == "__main__":
    import f
    import timeit
    from functools import partial
    from collections import deque
    from lwtest import run, assert_equal, raises, Assert
    from color import t
    from decimal import Decimal as D
    t.dbg = False
    if 1:  # Utility
        def GetColors():
            t.err = t("redl")
            t.dbg = t("lill") if g.dbg else ""
            t.N = t.n if g.dbg else ""
        def Dbg(*p, **kw):
            if g.dbg:
                print(f"{t.dbg}", end="")
                print(*p, **kw)
                print(f"{t.N}", end="")
        g.dbg = False  # Turn g.dbg on to see debug printing
        def MeasureTiming():
            x = f.flt(0)
            x.N = 2     # Show only two figures
            global seq, b
            print("DupNodup")
            for b, seq in ((True, "Type not important"), (False, "Type important")):
                print(f"  {seq}")
                for i in (3, 4, 5, 6):
                    seq = list(range(10**i)) + [0.0]  # seq has one duplicate
                    tm = timeit.timeit('DupNodup(seq, type_important=b)', globals=globals(), number=1)
                    print(f"    1e{i}:  {flt(tm).engsi}s")
            print("DupNodupSlow")
            for b, seq in ((True, "Type not important"), (False, "Type important")):
                print(f"  {seq}")
                for i in (2, 3, 4):
                    seq = list(range(10**i)) + [0.0]  # seq has one duplicate
                    tm = timeit.timeit('DupNodupSlow(seq, type_important=b)', globals=globals(), number=1)
                    print(f"    1e{i}:  {flt(tm).engsi}s")
    if 1:  # Testing functions
        def Test_SearchingSortedSequences():
            seq = [0, 1, 2, 3, 4, 5]
            n = len(seq)
            for i in range(n):
                if 1:   # Rightmost
                    Assert(Rightmost_le(seq, i) == i)
                    Assert(Rightmost_eq(seq, i) == i)
                    if i:
                        Assert(Rightmost_lt(seq, i) == i - 1)
                if 1:   # Leftmost
                    Assert(Leftmost_ge(seq, i) == i)
                    Assert(Leftmost_eq(seq, i) == i)
                    if i < n - 1:
                        Assert(Leftmost_gt(seq, i) == i + 1)
            n = 10
            raises(ValueError, Leftmost_eq, seq, n)
            raises(ValueError, Leftmost_gt, seq, n)
            raises(ValueError, Leftmost_ge, seq, n)
            raises(ValueError, Rightmost_eq, seq, n)
            raises(ValueError, Rightmost_eq, seq, -n)
            raises(ValueError, Rightmost_lt, seq, -n)
            raises(ValueError, Rightmost_le, seq, -n)
        def Test_iDistribute():
            def Dist(seq):
                "Return distances between numbers in seq"
                out = []
                for i in range(1, len(seq)):
                    out.append(abs(seq[i] - seq[i - 1]))
                return out
            a, b = 0, 255
            if 1:
                for n in range(2, 256):
                    s = iDistribute(n, a, b)
                    if s is None:
                        print(f"n = {n} no solution")
                        continue
                    d = list(set(Dist(list(s))))
                    if len(d) > 1 and n > 2:
                        assert_equal(len(d), 2)
                        assert_equal(abs(d[0] - d[1]), 1)
            for n in range(257, 265):
                raises(ValueError, list, iDistribute(n, a, b))
        def Test_GetClosest():
            low, high = -3, 6
            seq = (4, low, high, 1)  # Unsorted sequence
            sseq = (low, 1, 4, high)  # Sorted sequence
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
                    Assert(f(-4.0, seq) == low)
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
                        x = (self.x - other.x) ** 2
                        y = (self.y - other.y) ** 2
                        return flt((x + y) ** 0.5)
                seq = (Pt(0, 0), Pt(-3, 6), Pt(4, 8), Pt(2, 0))
                f = partial(GetClosest, is_sorted=None)
                def metric(a, b): return a.dist(b)
                Assert(f(Pt(0.1, 0.1), seq, distance=metric) == Pt(0, 0))
                Assert(f(Pt(-0.1, -0.1), seq, distance=metric) == Pt(0, 0))
                Assert(f(Pt(-100, 0.1), seq, distance=metric) == Pt(-3, 6))
                Assert(f(Pt(0, 1000), seq, distance=metric) == Pt(4, 8))
                Assert(f(Pt(1, 0), seq, distance=metric) == Pt(0, 0))
                Assert(f(Pt(1.0001, 0), seq, distance=metric) == Pt(2, 0))
        def Test_GetDupNodup():
            testcases = (
                # (function input, 
                #       expected (nodup, dup))
                ([], 
                    ([], [])),
                ([None], 
                    ([], [None])),
                ([None, None], 
                    ([None], [None])),
                ([1], 
                    ([], [1])),
                ([1, 1], 
                    ([1], [1])),
                ([1, 1.0], 
                    ([1.0],[1])),
                ([1, 2, 3, 1, 2, 4], 
                    ([1, 2], [1, 2, 3, 4])),
                ([1, 2, 3], 
                    ([], [1, 2, 3])),
                ("Hello", 
                    (['l'], ['H', 'e', 'l', 'o'])),
                (b"Hello", 
                    ([108], [72, 101, 108, 111])),
                ([1, 1, 1.0, 1.0], 
                    ([1, 1.0, 1.0], [1])),
            )
            for seq, expected in testcases:
                for typ in (list, tuple, deque):
                    result = DupNodup(typ(seq))
                    Assert(result == expected)
                    result = DupNodupHashable(typ(seq))
                    Assert(result == expected)
            # Testing with type_important
            seq = [1, 1, 1.0, 1.0]
            result = DupNodup(seq, type_important=False)
            Assert(result == ([1, 1.0, 1.0], [1]))
            result = DupNodup(seq, type_important=True)
            Assert(result == ([1, 1.0], [1, 1.0]))
        def Test_GetNum():
            Assert(GetNum([]) == [])
            Assert(GetNum(tuple()) == [])
            s = ["1", "2.", 3, 4., "five"]
            Assert(GetNum(s) == [1, 3, 4])
            Assert(GetNum(s, typ=float) == [1.0, 2.0, 3.0, 4.0])
            Assert(GetNum(s, typ=flt) == [1.0, 2.0, 3.0, 4.0])
            Assert(GetNum(s, typ=D) == [D(1), D(2), D(3), D(4)])
            Assert(GetNum(["1.0093753795"], typ=flt) == [1.0093753795])
        def Test_Clamp():
            rgb = (0.03, 1.223, 0.855)
            RGB = tuple(Clamp(rgb))     # Default behavior
            Assert(RGB == (0.03, 1.0, 0.855))
            # Typical use case:  scaling (r, g, b) when elements on [0, 1] to int on [0, 255]
            RGB = tuple(Clamp((int(i*256) for i in rgb), low=0, high=255, typ=int))
            Assert(RGB == (7, 255, 218))
            RGB = tuple(Clamp((int(i*256) for i in rgb), low=0, high=255, typ=D))
            Assert(RGB == (D(7), D(255), D(218)))

    GetColors()
    exit(run(globals(), halt=True)[0])
