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
        ##∞copyright∞# Copyright (C) 2024 Don Peterson #∞copyright∞#
        ##∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        ##∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        ##∞license∞#
        ##∞what∞#
        # Functions for dealing with sequences
        ##∞what∞#
        ##∞test∞# run #∞test∞#
        pass
    if 1:  # Standard imports
        from collections import Counter
        from fractions import Fraction
        import bisect
        import operator
    if 1:  # Custom imports
        from f import flt
        from lwtest import Assert, raises
        from color import t
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        class G:
            pass
        g = G()
        g.dbg = False
        ii = isinstance
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
if 1:  # Core functionality
    def find_le(x, seq):
        "Find rightmost value less than or equal to x; seq must be sorted"
        # From bisect module documentation
        i = bisect.bisect_right(seq, x)
        if i:
            return seq[i - 1]
        raise ValueError
    def find_ge(x, seq):
        "Find leftmost item greater than or equal to x; seq must be sorted"
        # From bisect module documentation
        i = bisect.bisect_left(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError
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
        if not (ii(a, int) and ii(b, int) and ii(n, int)):
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
        if not ii(n, int):
            raise TypeError(msg)
        if n < 2:
            raise ValueError(msg)
        if not ii(a, (int, impl)) or not ii(b, (int, impl)):
            raise TypeError("a and b must be either an integer or impl")
        if not (a < b):
            raise ValueError("Must have a < b")
        x0 = impl(a)
        dx = impl(b) - x0
        for i in range(n):
            x = x0 + (impl(i) / impl(n - 1)) * dx
            # Check invariants
            assert a <= x <= b
            assert ii(x, impl)
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
                L = find_le(x, sseq)  # L is sseq element, not index
                r = find_ge(x, sseq)  # r is sseq element, not index
                if L == r:
                    return L
                else:
                    diff_low, diff_high = abs(x - L), abs(x - r)
                    return L if diff_low <= diff_high else r
    def GetDupNodup(seq, type_important=False):
        '''Return (nodup, dup) where nodup is a list of the items in seq that are not
        duplicates and dup is a list of the items that are duplicates.  The order of
        the items in dup and nodup are the same as they were in seq.  The algorithm
        maintains the invariant len(nodup) + len(dup) == len(seq).
        
        If type_important is True, then the items must be equal AND have the same type
        to be considered a duplicate.  Example:  in python, 1 == 1.0, but type(1) is not
        the same as type(1.0).  There may be times when you'd want to consider the
        integer 1 not being equal to the floating point 1.0, which is why this keyword
        argument is present.
        
        Examples:
            GetDupNodup([1, 2, 3, 1, 2, 4]) --> [1, 2, 3, 4], [1, 2]
            GetDupNodup([1, 2, 3]) --> [1, 2, 3], []
            GetDupNodup([]) --> [], []
            GetDupNodup([1, 1, 1.0, 1.0], type_important=True) --> [1, 1.0], [1, 1.0]
            GetDupNodup([1, 1, 1.0, 1.0])                      --> [1], [1, 1.0, 1.0]
        
        This is an O(n²) algorithm because it does not rely on the elements being hashable.  
        Note it also keeps the order of the items found in the original sequence.
        This algorithm works well on small sequences (say, hundreds to thousands of
        items), but is not recommended for larger sequences because it will be slow.
        On my computer that was new in 2015 and was fairly inexpensive using python
        3.11.5, a list of n integers with an extra 1 at the end was timed with
        timeit.timeit() and the results were:
         
            log(n) = 3:  0.0141 s
            log(n) = 4:  1.42 s
            log(n) = 5:  148 s
        going up by a factor of 10² each time -- as expected.
        '''
        '''
        There are some processing nuances to this algorithm.  Let's use the above
        example of [1, 2, 3, 1, 2, 4].  The answer given above is [1, 2, 3, 4] is nodup
        and [1, 2] is dup.
        
        One way of writing this algorithm would be the following code that might be
        written by a beginning programmer (I'll ignore the type constraint):
        
            seq = [1, 2, 3, 1, 2, 4]
            n = len(seq)
            rev = False
            if rev:
                seq = list(reversed(seq))
            dup, nodup = [], []
            for i in range(n):
                item = seq[i]
                remainder = seq[i+1:]
                found = False
                for j in range(len(remainder)):
                    otheritem = remainder[j]
                    if otheritem == item:
                        found = True
                        break
                if found:
                    dup.append(item)
                else:
                    nodup.append(item)
            print("seq   =", seq)
            if rev:
                print("dup   =", list(reversed(dup)))
                print("nodup =", list(reversed(nodup)))
            else:
                print("dup   =", dup)
                print("nodup =", nodup)
        
        If you run this code, you'll get 
            seq   = [1, 2, 3, 1, 2, 4]
            dup   = [1, 2]
            nodup = [3, 1, 2, 4]
        Note the nodup list is not what was promised above.  If you follow the
        algorithm, you'll see that the first item processed is seq[0], a 1, and 
        the first step looks for 1 in the remaining sequence [2, 3, 1, 2, 4] and finds
        it at index 2.  Thus, found is True and seq[0] is added to dup.  But this is the
        "wrong" 1 to add, because now it means the 1 at index 3 will be the 1 that is in
        the nondup list.  So the order of processing is important.
        
        You might think that you could reverse the list and you'd get the correct
        answer.  Try it by setting rev to True; you'll get 
        
            seq   = [4, 2, 1, 3, 2, 1]
            dup   = [1, 2]
            nodup = [1, 2, 3, 4]
        
        This is the output we wanted, but the list(reversed()) call duplicates the input
        list seq, using more memory.  Since this algorithm should only be used on
        smaller arrays anyway, this probably isn't too bad of a penalty.  However, if
        you were writing this in C, you'd likely be using pointer arithmetic so you
        could operate on the original array without having to make a copy.  
        
        We can utilize python's ability to use negative indexes into arrays to
        facilitate our processing the list in the "backwards" order without reversing
        it.  Here's the sequence with the relevant index values
        
             0  1  2  3  4  5       Positive indexes
            [4, 2, 1, 3, 2, 1]
            -6 -5 -4 -3 -2 -1       Negative indexes
        
        You can get the positive indexes with range(n).  The negative indexes can be
        gotten with reversed(range(-n, 0)) where n is the length of the sequence.  For
        our seq, n is 6 and list(reversed(range(-n, 0))) is [-1, -2, -3, -4, -5, -6].
        Thus, we'll start with -1, get the remainder of the array from -2 to -6 and
        search it for duplicates.  The only twist is that we have to reverse the indexes
        because the -6 index element is more left array element than the -2 index.
        
        Let's try this approach:
        
            seq = [1, 2, 3, 1, 2, 4]
            n = len(seq)
            dup, nodup = [], []
            for i in reversed(range(-n, 0)):
                item = seq[i]
                remainder = seq[-n:i]
                found = False
                for j in range(len(remainder)):
                    otheritem = remainder[j]
                    if otheritem == item:
                        found = True
                        break
                if found:
                    dup.append(item)
                else:
                    nodup.append(item)
            print("seq   =", seq)
            print("dup   =", list(reversed(dup)))
            print("nodup =", list(reversed(nodup)))
        
        We get
        
            seq   = [1, 2, 3, 1, 2, 4]
            dup   = [1, 2]
            nodup = [1, 2, 3, 4]
        
        which is what we wanted.
        
        I started with the above code and experimented and added test cases until I had
        the following:
        
            def f(seq, type_important=False):
                n = len(seq)
                dup, nodup = [], []
                for i in reversed(range(-n, 0)):
                    item, remainder, found = seq[i], seq[-n:i], False
                    for j in range(len(remainder)):
                        otheritem = remainder[j]
                        if ((type_important and type(otheritem) is type(item) and otheritem == item)
                                    or 
                                (otheritem == item)):
                            found = True
                            break
                    dup.append(item) if found else nodup.append(item)
                if len(dup) != len(nodup) and len(dup) + len(nodup) != n:
                    raise RuntimeError("Bug in this function")
                print("seq   =", seq)
                print("dup   =", list(reversed(dup)))
                print("nodup =", list(reversed(nodup)))
        
            s = [
                [],
                [None],
                [None, None],
                [1],
                [1, 1],
                [1, 1.0],
                [1, 2, 3, 1, 2, 4],
                [1, 2, 3],
                "Hello",
                b"Hello",
                [1, 1, 1.0, 1.0],
            ]
            for i in s:
                f(i)
                print()
            print("With type_important=True")
            f(s[-1], type_important=1)
        
        This is in fact the finished code and I used the test cases in s for testing the
        function too.
        
        This is one of those algorithms that has a few subtle nuances, but you can do
        nearly everything you need to for development by using a small example test case
        like [1, 2, 3, 1, 2, 4] and working out the pointer arithmetic.
        '''
        n, dup, nodup = len(seq), [], []
        if not n:
            return nodup, dup
        for i in reversed(range(-n, 0)):
            item, remainder, found = seq[i], seq[-n:i], False
            for j in range(len(remainder)):
                otheritem = remainder[j]
                if ((type_important and type(otheritem) is type(item) and otheritem == item)
                            or 
                        (otheritem == item)):
                    found = True
                    break
            dup.append(item) if found else nodup.append(item)
        if len(dup) != len(nodup) and len(dup) + len(nodup) != n:
            raise RuntimeError("Bug in this function")
        return (list(reversed(nodup)), list(reversed(dup)))
    def GetDuplicates(seq):
        '''Return a list of the items in the sequence seq that are duplicates.  
        
        Examples:  
            GetDuplicates([1, 2, 3, 1, 2, 4]) --> [1, 2]
            GetDuplicates([1, 2, 3]) --> []
            GetDuplicates([]) --> []
            GetDuplicates([1, 1, 1, 1.0, 1.0, 1.0]) --> [1]
            
        Caution:  be aware of the behavior of the last example, caused because in python
        hash(1) == hash(1.0).  For some problems, you may not want to consider the
        integer 1 and the floating point number 1.0 the same thing.  To handle this
        issue, you can use the nonhashable keyword; see below.
        
        If you only want to know if seq has duplicates, the simplest way is to see if
        'len(seq) == len(set(seq))' is True, but this requires the elements of seq to be
        hashable.  Common nonhashable things are mutable things like lists,
        dictionaries, sets, deques, etc.  The reason for them being nonhashable is that
        they could change their contents during the program's lifetime, meaning the
        elements' hash values will change.
        
        The first algorithm in this function is O(n) where n is the size of the
        sequence.  It only works if all the elements in seq are hashable.  It uses
        collections.Counter, which uses a dictionary to count the objects.
        
        If seq contains nonhashable elements, the first algorithm will fail and the 
        second algorithm is used, which is O(n²).  This is because it is essentially
        
            duplicates = []
            for i, item in enumerate(seq):
                for item1 in seq[i:]:
                    if item == item1 and item not in duplicates:
                        duplicates.append(item)
        
        https://stackoverflow.com/questions/9835762/how-do-i-find-the-duplicates-in-a\
        -list-and-create-another-list-with-them, posted by georg gives more concise
        but equivalent list comprehensions:
        
            no_duplicates = [x for i, x in enumerate(seq) if x not in seq[:i]]
            duplicates =    [x for i, x in enumerate(seq) if x     in seq[:i]]
        
        Here's an illustration.  Suppose seq = [0, 1, 2, 3, 4, 1].  The first step
        gets seq[0] = 0 and asks if seq[0] is in the remaining [1, 2, 3, 4, 1].  No.
        The next step gets seq[1] = 1 and asks if seq[1] is in the remaining
        [2, 3, 4, 1].  Yes, so it's put into the duplicates list.  And so on.
        '''
        # First algorithm:  will fail if seq contains a non-hashable element like a
        # list, dict, or set.
        try:
            counts = Counter(seq)
            duplicates = [item for item, count in counts.items() if count > 1]
            return duplicates
        except TypeError:
            # This probably occurred because an element of seq wasn't hashable, a
            # requirement of Counter, which is a dict subclass
            pass
        # Second algorithm
        duplicates = []
        for i in range(1, len(seq)):
            if seq[i - 1] in seq[i:]:
                duplicates.append(seq[i - 1])
        return duplicates

if __name__ == "__main__":
    from functools import partial
    from lwtest import run, assert_equal, Assert
    GetColors()
    g.dbg = False  # Turn g.dbg on to see debug printing
    def Test_find():
        # Test find_le and find_ge; though these came from the python manpage on the
        # bisect module, they need to be proved working.
        N = 10
        seq = list(range(N))
        for i in range(N):
            n = find_le(i, seq)
            Assert(n == i)
            n = find_ge(i, seq)
            Assert(n == i)
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
    def Test_GetDuplicates():
        if 1:   # Basic testing
            class G:
                def __init__(self, x):
                    self.x = x
                def __str__(self):
                    return f"<{self.x}>"
                def __repr__(self):
                    return str(self)
            a, b, c = G(1), G(5), [1, 3]
            seq1 = ("8", 3, 4, 3, a, b, a,    "8") # Hashable
            seq2 = ("8", 3, 4, 3, a, b, a, c, "8") # Not hashable
            expected = ["8", 3, a]
            # Use the Counter implementation
            duplicates = GetDuplicates(seq1)
            Assert(duplicates == expected)
            # Use the slower second implementation
            duplicates = GetDuplicates(seq2)
            Assert(duplicates == expected)
        if 1:   # Test with large sequences
            # Lotsa numbers with one duplicate at end
            n, dup = 10**6, 1.0
            seq = [float(i) for i in range(n)] + [dup]
            duplicates = GetDuplicates(seq)
            Assert(duplicates == [dup])
            # Use second algorithm (much slower)
            n = 10**4
            seq = [float(i) for i in range(n)] + [dup, [0, 1]]
            duplicates = GetDuplicates(seq)
            Assert(duplicates == [dup])
    def Test_GetDupNodup():
        testcases = (
            # Function input, expected return value
            ([], ([], [])),
            ([None], ([None], [])),
            ([None, None], ([None], [None])),
            ([1], ([1], [])),
            ([1, 1], ([1], [1])),
            ([1, 1.0], ([1],[1.0])),
            ([1, 2, 3, 1, 2, 4], ([1, 2, 3, 4], [1, 2])),
            ([1, 2, 3], ([1, 2, 3], [])),
            ("Hello", (['H', 'e', 'l', 'o'], ['l'])),
            (b"Hello", ([72, 101, 108, 111], [108])),
            ([1, 1, 1.0, 1.0], ([1], [1, 1.0, 1.0])),
        )
        f = GetDupNodup
        for seq, expected in testcases:
            result = f(seq)
            Assert(result == expected)
            #t.print(f"{t.yel}{seq}    {t.purl}{result}")
        # With type_important
        result = f(testcases[-1][0], type_important=1)
        Assert(result == ([1], [1, 1.0, 1.0]))
        #print(f(testcases[-1][0], type_important=1))
    exit(run(globals(), halt=True)[0])
