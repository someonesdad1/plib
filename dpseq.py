'''
Functions for sequences
    Batch           Generator to pick n items at a time from a sequence
    Clamp           Return elements clamped to an interval
    Dup             Return elements that are duplicates
    DupHashable     Return elements that are duplicates
    DupNodup        Return (dup, nodup)
    DupNodupHashable Return (dup, nodup)
    fDistribute     Return equally-distributed numbers
    Flatten         Flatten sequences to specified depth
    Flatten_generator Generator to return a flattened sequence
    frange          Floating point generator analog of range()
    GetClosest      Return value closest to x
    GetNum          Return a list of numbers in sequence
    GetSize         Recursively finds size of objects in bytes
    GroupByN        Return iterator giving groups of n items from sequence
    grouper         map/reduce for data analysis
    hyphen_range    
    iDistribute     Return equally-distributed integers
    ifrange         Simpler iterator implementation of frange
    IsHomogeneous   Return True if sequence is homogeneous
    IsIterable      Return True if argument is an iterable
    ItemCount       Return a sorted list of (item, count) in sequence
    Leftmost_eq     Return index of the leftmost value == x
    Leftmost_ge     Return index of the leftmost value >= x
    Leftmost_gt     Return index of the leftmost value > x
    lrange          Logarithmic analog to frange()
    Nodup           Return elements that are not duplicates
    NodupHashable   Return elements that are not duplicates
    Paste           Return a pasted sequence from a group of sequences
    PPSeq           Class to format sequences for pretty printing
    Ranges          Return numerical sequence of ranges from sequence of integers
    Rational        Fraction with proper fraction string representation
    Rightmost_eq    Return index of the rightmost value == x
    Rightmost_le    Return index of the rightmost value <= x
    Rightmost_lt    Return index of the rightmost value < x
    Sequence        Sequence of numbers based on start:end:increment spec
    transpose       Transpose of a nested two-dimensional sequence
    Unique          Generator returns unique elements in sequence of hashable items
    unrange         Turn seq of integers into a collection of ranges; return as a string
    unrange_real    Turn seq of numbers into a collection of ranges; return as a string
    VisualCount     Return a list of strings representing a histogram of the items in seq
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
        import bisect
        import collections
        import decimal
        import fractions
        import inspect
        import itertools
        import math
        import numbers
        import operator
        import os
        import typing as ty
    if 1:  # Custom imports
        import dptypes
        import f
        import wrap
        if 0:
            import debugg
            debugg.SetDebugger()
        try:
            import mpmath
            _have_mpmath = True
        except ImportError:
            _have_mpmath = False
    if 1:  # Global variables
        g = dptypes.Constant()
        g.dbg = False
    if 1:  # Types
        T = ty.TypeVar("T")     # A short type
        # A nested sequence for flatten()
        NestedSequence: ty.TypeAlias = T | ty.Sequence["NestedSequence[T]"]
        # A type for numbers (int, float, Decimal, ...)
        Tnum = ty.TypeVar("Tnum", int, float, ty.Any)
        # A type specifically for floating point numbers (float, Decimal, ...)
        T_Arith = ty.TypeVar("T_Arith", bound="SupportsFPArithmetic")
        @ty.runtime_checkable
        class SupportsFPArithmetic(ty.Protocol):
            '''An interface spec for types that support basic arithmetic
            and can be constructed from a numeric value.
            '''
            def __init__(self, value: ty.Any) -> None: ...
            def __add__(self: T_Arith, other: ty.Any) -> T_Arith: ...
            def __sub__(self: T_Arith, other: ty.Any) -> T_Arith: ...
            def __mul__(self: T_Arith, other: ty.Any) -> T_Arith: ...
            def __truediv__(self: T_Arith, other: ty.Any) -> T_Arith: ...
            def __lt__(self: T_Arith, other: ty.Any) -> bool: ...
            def __le__(self: T_Arith, other: ty.Any) -> bool: ...
        # We use the Protocol to constrain our TypeVar
        Tfp = ty.TypeVar("Tfp", bound=SupportsFPArithmetic)
        
        # A Protocol that defines "I can be compared and added".  This is intended to be
        # a type used by frange that allows the use of any suitable numerical type, such
        # as float, decimal.Decimal, fractions.Fraction, mpmath.mpf or other floating
        # point types that don't exist today.
        class SupportsRange(ty.Protocol):
            def __add__(self, other: ty.Any) -> "SupportsRange": ...
            def __lt__(self, other: ty.Any) -> bool: ...
            def __gt__(self, other: ty.Any) -> bool: ...
        # Tfrange is now "Universal" - any type that meets the Protocol above
        Tfrange = ty.TypeVar("Tfrange", bound=SupportsRange)
        # ∞∞1 Tfrange and Tfp are quite similar; can they be coalesced?

if 1:  # Distribute and GetClosest
    def iDistribute(n: int, a: int, b: int) -> ty.Iterable[int]:
        '''Generator to return an integer sequence [a, ..., b] with n elements
        
        The elements are "equally" distributed between a and b, but since we're dealing
        with integers, you'll have to be a little flexible about what "equally" means
        (see the example below).
        
        Algorithm
            The spacing between the returned integers dx is a Fraction.  The n numbers
            are generated as [f(a + 0*dx), f(a + 1*dx), ..., b] where f is a function
            that rounds to the nearest integer.
        
        Invariants
            This generator returns n values; the first value will always be a and the
            last value will always be b.  Proof:  dx = (b - a)/(n - 1); when i is 0,
            i*dx is 0, so a + i*dx is equal to a.  When i is n - 1 (last value from
            range(n)), then i*dx is (b - a), so a + (b - a) is equal to b.
        
        Arguments
            n: Number of items in returned sequence
            a: The starting value of the returned sequence
            b: The ending value of the returned sequence
        
        Returns
            An iterator yielding the sequence.
        
        Example
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
            with a ValueError exception on the n == 7 term.  For the case n == 4, note
            how the adjective "equally" needs to be interpreted "symmetrically" and for
            the case n == 5, even that's not true.
        '''
        if 1:   # Check parameters
            if not (
                    isinstance(a, int) 
                    and isinstance(b, int)
                    and isinstance(n, int)
                ):
                raise TypeError("Arguments must be integers")
            if a >= b:
                raise ValueError("Must have a < b")
            if n < 2:
                raise ValueError("n must be >= 2")
        if n == 2:
            yield a
            yield b
            return
        dx = fractions.Fraction(b - a, n - 1)
        if dx < 1:
            raise ValueError("No solution")
        for i in range(n):
            yield int(round(a + i*dx, 0))
    def fDistribute(
            n: int,
            a: ty.Any = 0.0,
            b: ty.Any = 1.0,
            fpimpl: type[Tfp] = float  # type: ignore # default 'float' matches the Protocol
            ) -> ty.Iterator[Tfp]:
        '''Generator to return n fpimpl instances on [a, b] inclusive
        
        A common use case is an interpolation parameter on [0, 1].  You can use other
        floating point implementation types like decimal.Decimal.  Other types that
        define fpimpl()/fpimpl() to return an fpimpl-type floating point number will
        also work (e.g., mpmath's mpf type).
        
        Algorithm
            The i-th element of the sequence is a + dx*i/divisor for i in range(n),
            divisor = n - 1, and dx = (b - a).  When i = 0, the output is a; when i = n
            - 1, the output is a + dx*(n - 1)/(n - 1) = a + (b - a) or b.
        
        Invariants
            The returned sequence generator will produce n terms.  The difference
            between any two adjacent elements of the sequence is 
        
            [a + dx*(i + 1)/divisor] - [a + (dx*i/divisor]
            = a - a  + dx/divisor*[(i + 1) - i] = dx/divisor
        
        Arguments
            n: Number of items in sequence (must be an integer > 1).
            a: The starting number of the sequence
            b: The ending number of the sequence
        
        Returns
            An iterator yielding instances of type 'fpimpl'.
        
        Numerical note
            Cumulative precision error is a property of the 'fpimpl' type.  If you are
            using near the full number of digits of the floating point instance, beware
            of numerical irregularities.
        
        Examples
            >>> import decimal
            >>> import fractions
            >>> list(fDistribute(3, 0, 1, float))
            [0.0, 0.5, 1.0]
            >>> list(fDistribute(3, 0, 1, decimal.Decimal))
            [Decimal('0'), Decimal('0.5'), Decimal('1')]
            >>> list(fDistribute(3, 0, 1, fractions.Fraction))
            [Fraction(0, 1), Fraction(1, 2), Fraction(1, 1)]
        '''
        if 1:   # Check arguments
            msg = "n must be an integer > 1"
            if not isinstance(n, int):
                raise TypeError(msg)
            if n < 2:
                raise ValueError(msg)
            if not isinstance(a, int | fpimpl) or not isinstance(b, int | fpimpl):
                raise TypeError("a and b must be either an integer or fpimpl")
            if not (fpimpl(a) < fpimpl(b)):
                raise ValueError("Must have a < b")
        # Tfp is a floating point type
        x0: Tfp = fpimpl(a)
        width: Tfp = fpimpl(b) - x0
        # Pre-calculate the denominator as a Tfp type to avoid 'float' drift
        denominator: Tfp = fpimpl(n - 1)
        for i in range(n):
            # All operations here involve Tfp types, so 'x' remains a Tfp
            x = x0 + (fpimpl(i)/denominator)*width
            yield x
    def GetClosest(x: ty.Any, 
                   seq: ty.Sequence[ty.Any],
                   is_sorted: bool | None =False,
                   key: ty.Any=None,
                   distance=operator.sub,
                   unresolved: int=0) -> ty.Any:
        '''Return the value in sequence seq that is closest to x
        
        Algorithm 
            Two different algorithms are used, depending on whether seq is in sorted
            order.  If seq is sorted, then binary search is used which is O(n*log(n)).
            If seq is not sorted and its elements don't have a relevant '<' operation
            defined, you'll want to provide a key function in the argument key for the
            sorted() builtin.
        
        Invariants
            The sequence seq is not modified.
        
        Arguments
            x           The number to find the closest value in seq
            seq         The sequence to search through
            is_sorted   True if seq is sorted, False if not, None if can't sort
            key         Key for sorted() builtin
            distance    Binary function for dist(x, seq element)
            unresolved  The element in seq to return when can't resolve
        
        Returns
            The value in seq that is closest to x.
        
        is_sorted is None
            In this case, you've indicated that the sequence can't be put into sorted
            order and the distance function is used to calculate the distance of each
            element in the sequence from x.  The index of the lowest distance is used to
            get the closest element in seq.  The following example shows that some
            problems are "unresolvable", meaning that any element in the sequence can be
            returned.
                >>> x = 1e99
                >>> seq = [3, 0, 2, 1]
                >>> [i - x for i in seq]
                [-1e+99, -1e+99, -1e+99, -1e+99]
            In such a case, the keyword 'unresolved' is used to pick the element of seq
            to return; otherwise a ValueError exception is raised.
        
        Cautions
            - If is_sorted is False and key is None, the sequence will be sorted with
              sorted(seq, key=None) and this may or may not work.  If seq is not e.g. a
              simple sequence of numbers, you'll want to supply a suitable key function.
            - If is_sorted is None or False, a second sequence is created to hold the
              distances and this can take extra time and memory.
        
        Example
            >>> seq = (5, -8, 10, 1)
            >>> GetClosest(-1e99, seq)
            -8
            >>> GetClosest(-9, seq)
            -8
            >>> GetClosest(-7, seq)
            -8
            >>> GetClosest(0, seq)
            1
            >>> GetClosest(7, seq)
            5
            >>> GetClosest(1e99, seq)
            10
        '''
        if not seq:
            raise ValueError("Sequence seq cannot be empty")
        if is_sorted is None:
            # is_sorted is None means the sequence can't be sorted for some reason.  In
            # this case, we use the distance binary function to find the closest element
            # to x.
            o = [abs(distance(i, x)) for i in seq] # Get list of differences from x
            minimum = min(o)  # Minimum difference
            index = o.index(minimum)
            if 1:   # Check for unresolved
                if len(set(o)) == 1 and len(seq) > 1:  # Problem can't be resolved
                    if unresolved is not None and isinstance(unresolved, int):
                        index = unresolved
                        try:
                            seq[index]
                        except IndexError as e:
                            raise ValueError("'resolved' is not an index for seq") from e
                    else:
                        raise ValueError("Closest item is unresolvable")
            # Return the closest value
            return seq[index]
        else:
            # Use binary search on a sorted array
            sortedseq = seq if is_sorted else sorted(seq, key=key)
            if x <= sortedseq[0]:
                return sortedseq[0]
            elif x >= sortedseq[-1]:
                return sortedseq[-1]
            else:
                # Use binary search
                left = Rightmost_le(sortedseq, x)   # left is sortedseq element, not index
                right = Leftmost_ge(sortedseq, x)   # right is sortedseq element, not index
                if left == right:
                    return left
                else:
                    diff_low, diff_high = abs(x - left), abs(x - right)
                    return left if diff_low <= diff_high else right
if 1:   # Searching sorted sequences from bisect module
    '''
    Binary search is a fundamental technique for searching sorted sequences.  Its
    fundamental approach is to divide the set of items being searched into two halves
    and ask "Is the desired item in the left half or the right half?".  If it's in
    either half, then the same division/question approach is used again, continuing
    until the answer is known.   The worst-case number of divisions is floor(N+1) where
    N = ln(n)/ln(2).  ln is the natural logarithm and n is the size of the sequence.
        
    bisect.bisect_left(seq, x) partitions seq into two halves so that 
        all values < x on the left side
        all values >= x on the right side
    bisect.bisect_right(seq, x) partitions seq into two halves so that 
        all values <= x on the left side
        all values > x on the right side
        
    This behavior can help you mentally check the following utility functions.
    '''
    def Leftmost_eq(seq: ty.Sequence[ty.Any], x: ty.Any) -> ty.Any:
        'Return index of the leftmost value == x'
        # index(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i != len(seq) and seq[i] == x:
            return i
        raise ValueError(f"No leftmost value == {x}")
    def Leftmost_gt(seq: ty.Sequence[ty.Any], x) -> ty.Any:
        'Return index of leftmost value > x'
        # find_gt(a, x) in bisect module document
        i = bisect.bisect_right(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError(f"No leftmost value > {x}")
    def Leftmost_ge(seq: ty.Sequence[ty.Any], x) -> ty.Any:
        'Return index of leftmost item >= x'
        # find_ge(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i != len(seq):
            return seq[i]
        raise ValueError(f"No leftmost value >= {x}")
    #
    def Rightmost_eq(seq: ty.Sequence[ty.Any], x) -> ty.Any:
        'Return index of the rightmost value == x'
        try:
            n = Rightmost_le(seq, x)
            if seq[n] == x:
                return n
            elif n < len(seq) - 1:
                return n + 1
            else:
                raise ValueError
        except ValueError as e:
            raise ValueError(f"No rightmost value == {x}") from e
    def Rightmost_lt(seq: ty.Sequence[ty.Any], x) -> ty.Any:
        'Return index of rightmost value < x'
        # find_lt(a, x) in bisect module document
        i = bisect.bisect_left(seq, x)
        if i:
            return seq[i-1]
        raise ValueError(f"No rightmost value < {x}")
    def Rightmost_le(seq: ty.Sequence[ty.Any], x) -> ty.Any:
        'Return index of rightmost value <= x'
        # find_le(a, x) in bisect module document
        i = bisect.bisect_right(seq, x)
        if i:
            return seq[i-1]
        raise ValueError(f"No rightmost value <= {x}")
if 1:   # Get or transform numbers from a sequence
    def GetNum(seq: ty.Sequence[ty.Any],
               typ: type[Tnum] = int  # type: ignore # float/int don't explicitly inherit
              ) -> ty.List[Tnum]:
        '''Return a list of numbers found in sequence seq
        
        The intent is that all the elements of seq that can be converted to a number of
        type typ will be returned in the list.  Examples:
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
    def Clamp(seq: ty.Sequence[ty.Any], low: Tnum=0, high: Tnum=1) -> ty.Any:
        '''Generator to return sequence's elements "clamped" to an interval
        
        The returned elements will be in the interval [low, high].  The type of the each
        returned value is the same type as the corresponding element processed.
        
        Invariants:
            The number of elements returned is equal to the number elements in seq.
        
        Arguments:
            seq     The input sequence (will not be changed)
            low     Low value of the allowed interval
            high    High value of the allowed interval
        
        Returns:
            An iterator yielding the numbers in seq; they are modified if necessary to
            lie within [low, high].
        
        Example:
            >>> list(Clamp((-0.02, 0.4, 1.6), low=0, high=1.5, typ=float))
            [0.0, 0.4, 1.5].
        '''
        for x in seq:
            typex = type(x)
            if x < low:
                yield typex(low)
            elif x > high:
                yield typex(high)
            else:
                yield typex(x)
if 1:   # Finding duplicates in sequences
    if 0:   # Notes
        '''
        The obvious approach to this duplicates problem is to use the facilities of
        lists:
        
            def FindDuplicates(seq):
                seqcopy = list(seq)
                nodup, dup = [], []
                    item = seqcopy.pop()
                    dup.append(item) if item in seqcopy else nodup.append(item)
                return (nodup, dup)
        
        It's simple, understandable, and obviously correct.  Unfortunately it's O(n²)
        because looking at each element in the list with pop() is O(n) and the 'item in
        seqcopy' is an implicit for loop.  It also creates extra lists, using up more
        memory.
        
        One fix for this is to copy the sequence into a set, which has no duplicates.  Then
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
        and adding an item to a set are both O(1).  The extra cost is the extra memory 
        for dup/nodup and the set.
        '''
    class Hashable:
        '''Encapsulate an object and make it hashable by defining a __hash__ method.  It
        is your responsibility to ensure that the items being stored don't change while
        being processed or you'll get incorrect results.
        '''
        __slots__ = ("object", "typ")
        def __init__(self, object: ty.Any, typ: bool=False) -> None:
            '''If typ in the constructor is True, then the objects must also have the
            same type to be considered equal.
            '''
            self.object = object
            self.typ = bool(typ)
        def __hash__(self) -> int:
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
        def __eq__(self, other: ty.Any) -> bool:
            eqval = bool(self.object == other.object)
            if self.typ:
                return bool(eqval and (type(self) is type(other)))
            return eqval
    def Nodup(seq: ty.Sequence[ty.Any], type_important: bool=False) -> list[ty.Any]:
        '''Returns a list of elements in seq that are not duplicates
        
        See DupNodup() for details.
        
        Example
            >>> list(fDistribute(3, 0, 1, float))
            [0.0, 0.5, 1.0]
        '''
        _, nodup = DupNodup(seq, type_important=type_important)
        return nodup
    def NodupHashable(seq: ty.Sequence[ty.Any]) -> list[ty.Any]:
        '''seq is a sequence; returns nodup where nodup is a list of the elements in seq
        that are not duplicates.  See DupNodupHashable() for details.
        '''
        _, nodup = DupNodupHashable(seq)
        return nodup
    def Dup(seq: ty.Sequence[ty.Any], type_important: bool=False) -> list[ty.Any]:
        '''seq is a sequence; returns dup where dup is a list of the elements in seq
        that are duplicates.  See DupNodup() for details.
        '''
        dup, _ = DupNodup(seq, type_important=type_important)
        return dup
    def DupHashable(seq: ty.Sequence[ty.Any]) -> list[ty.Any]:
        '''seq is a sequence; returns dup where dup is a list of the elements in seq
        that are duplicates.  See DupNodupHashable() for details.
        '''
        dup, _ = DupNodupHashable(seq)
        return dup
    def DupNodupHashable(seq: ty.Sequence[ty.Any]) -> tuple[list[ty.Any], list[ty.Any]]:
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
    def DupNodup(seq: ty.Sequence[ty.Any],
                 type_important: bool=False
                ) -> tuple[list[ty.Any], list[ty.Any]]:
        '''Returns [dup, nodup]:  the duplicates and non-duplicates in seq
        
        This function will work on arbitrary sequences.  If you know the sequence only
        contains hashable objects, use DupNodupHashable().
        
        Algorithm 
            The method "stores" each item from seq in a class Hashable that allows
            the item to be stored in a set.  This set is used to identify when a
            particular element has been seen before; the algorithm puts the element into
            dup if it has been seen before and into nodup if it hasn't been seen.
        
        Invariants
            len(dup) + len(nodup) == len(seq)
        
        Arguments
            seq     The sequence to process
            type_important
                If this variable is True, then itemA and itemB are defined to be
                duplicates iff both 'itemA == itemB' and 'type(itemA) is type(itemB)'
                expressions are True.  This is useful in situations where e.g. you don't
                want the integer 1 and the floating point 1.0 values to be considered
                equal (in python, '1 == 1.0' is True).
        
        Returns
            [dup, nodup] where both dup and nodup are lists.  
        
        Notes
            - The algorithm in this function uses a set of the elements in seq to
              identify duplicate items.  To ensure this works with unhashable objects,
              the objects are encapsulated in the Hashable class.  For DupNodup() to
              work correctly, the contents of all the items in seq cannot change while
              DupNodup() is processing; otherwise, you'll get incorrect results.
            - Each element of seq is accessed in a loop.  If seq is a type like a large
              deque, you may want to convert it to a list for better performance
              (accessing the middle of a deque is O(n), not like O(1) for a list).
        
        Example
            >>> DupNodup([1, 2, 3, 1, 4, 1.0])
            [[1, 1.0], [1, 2, 3, 4]]
            >>> DupNodup([1, 2, 3, 1, 4, 1.0], type_important=True)
            [[1], [1, 2, 3, 4, 1.0]]
        '''
        n:     int  = len(seq)
        dup:   list = []
        nodup: list = []
        seen:  set  = set()
        for i in range(n):
            item, sitem = seq[i], Hashable(seq[i], typ=type_important)
            dup.append(item) if sitem in seen else nodup.append(item)
            seen.add(sitem)
        assert len(dup) + len(nodup) == n
        return (dup, nodup)
if 1:   # frange, lrange, Sequence, irange, Rational
    '''
    Generators that are floating point analogs of range()
        frange(start, stop, step)
            Best to initialize with string representations of floating point numbers.  You
            can control the output type and the implementation type, allowing use with a
            variety of number types.  Example:
                for i in frange("0", "1", "0.1"):
                    sys.stdout.write(str(i) + " ")
            results in
                0.0 0.1 0.2 0.3 0.4 0.5 0.6 0.7 0.8 0.9
            If start contains a '/' character, impl and return_type
            parameters are set to dpseq.Rational (see below).
            
        ifrange(start, stop, step)
            Generator that works similarly to frange, but is a simpler implementation.  Must
            be used with 12 or less significant figures.  Requires dpmath.RoundOff; if not
            present, the module still works but this function won't be available.
            
        lrange(start_decade, stop_decade)
            Useful for producing sequences that can be used for log-log plotting.  Can also
            return numpy arrays.  Examples:
                for i in lrange(0, 2):
                    sys.stdout.write(str(i) + " ")
            results in
                1 2 3 4 5 6 7 8 9 10 20 30 40 50 60 70 80 90
            and
                for i in lrange(0, 3, mantissas=[1, 2, 5]):
                    sys.stdout.write(str(i) + " ")
            results in
                1 2 5 10 20 50 100 200 500
                
        Sequence(string)
            A convenience function Sequence(string) is supplied that will return a list from
            the specifications in the string.  Example:
                Sequence('1:1.5:0.1   5:1:-1  1/4:3/4:1/8')
            returns
                [1, 1.1, 1.2, 1.3, 1.4, 1.5,
                5, 4, 3, 2, 1,
                1/4, 3/8, 1/2, 5/8, 3/4]
    '''
    class Rational(fractions.Fraction):
        '''The Rational class is a fractions.Fraction object except that it has a
        conventional proper fraction string representation.
        '''
        def __str__(self) -> str:
            n, d = abs(self.numerator), abs(self.denominator)
            s = ["-"] if self.numerator*self.denominator < 0 else [""]
            if d == 1:
                s.append(str(n))
            else:
                ip, remainder = divmod(n, d)
                if ip:
                    s.extend([str(ip), "-"])
                s.extend([str(remainder), "/", str(d)])
            return "".join(s)
    # yy
    def frange(start: Tfrange|None, 
               stop: Tfrange|None = None, 
               step: Tfrange|None = None, 
               return_type: type[Tfrange] = float,      # type: ignore[assignment]
               impl: type[ty.Any] = decimal.Decimal,       # type: ignore[assignment]
               strict: bool=True,
               include_end: bool=False
               ) -> ty.Generator[Tfrange]:
        '''A floating point generator analog of range()
        
        Algorithm 
            Describe the algorithm
        
        Invariants
            Mention any specific mathematical invariants (e.g., returns n values).
        
        Arguments
            start, stop, step
                Can be python floats, integers, or strings representing floating point
                numbers (or any other object that impl can convert to an object that
                behaves with numerical semantics).
            return_type
                The returned numbers are converted to this type.
            impl
                The calculations to produce the desired numbers are done with this
                number implementation.  I recommend you use either decimal.Decimal 
                or mpmath.mpf, as these give you an arbitrary number of digits when
                needed.
            strict
                If False, try to convert an impl object to a string before converting it
                to a return_type number.  Setting strict to False may allow some number
                types to work with other number types; however, the burden is on the
                user to determine if frange still behaves as expected.
            include_end
                If True, then the step is added to the stop number.  This allows you to
                get e.g.  an inclusive list of integers.  However, for floating point
                values, you may get a number one step beyond the stopping point.
        
        Returns
            A sequence of numbers of type return_type.
        
        Notes
            - Python's Decimal class is used for the default implementation, but you can
              choose it to be e.g. floats if you wish (however, you'll then have the
              typical naive implementation seen all over the web).  Consult
              http://www.python.org/dev/peps/pep-0327/ and the decimal module's
              documentation to learn why a float implementation is naive.
            - To help ensure you get the output you want, use strings for start, stop
              and step.  This is the "proper" way to initialize Decimals with
              non-integer values.
                - For an example, compare the output of frange(9.6001, 9.601, 0.0001)
                  and frange("9.6001", "9.601", "0.0001").  Most users will probably
                  expect the output from the second form, which excludes the stop value
                  like range does.
        
        Example
            >>> list(frange(9.6001, 9.601, 0.0001))
            [9.6001, 9.6002, 9.6003, 9.6004, 9.6005, 9.6006, 9.6007, 9.6008, 9.6009]
            >>> list(frange("9.6001", "9.601", "0.0001"))
            [9.6001, 9.6002, 9.6003, 9.6004, 9.6005, 9.6006, 9.6007, 9.6008, 9.6009]

            Interestingly, this works the same way in python 3.11, but when originally
            tested, the first form using floats gave one more item in the sequence.
        '''

        '''
        
        
        Examples of use (also look at the unit tests):
            a = list(frange("0.125", "1", ".125"))
        results in a being
            [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
            
        Alternatively, you can use python fractions in frange because they have the
        proper numerical semantics.  A convenience class called Rational is provided in
        this module because it allows fractions to be printed in their customary proper
        form.
            R = Rational
            b = list(frange("1/8", "1", "1/8", impl=R, return_type=R))
        results in b being
            [1/8, 1/4, 3/8, 1/2, 5/8, 3/4, 7/8]
        and we also have a == b is True.
        
        The happy accident of a == b being True is only because these decimal fractions
        can be represented exactly in binary floating point.  This is not true in
        general:
            c = list(frange("0.1", "1", "0.1"))
            d = list(frange("1/10", "1", "1/10", impl=R, return_type=R))
        results in c == d being False.
        
        Print out c to see why c and d are not equal (this is practically the canonical
        example of the problems with binary floating point for us humans that love
        decimal arithmetic).
        
        A convenience is that if '/' is in the string for start, all the numbers are
        interpreted as Rational objects.
        '''
        def ceil(x):
            i = int(abs(x))
            if x > i:
                i += 1
            return (-1 if x < 0 else 1)*i
        if isinstance(start, str) and "/" in start:
            impl = return_type = Rational
        def init(x):
            if isinstance(x, f.flt):
                return impl(repr(float(x)))
            elif isinstance(x, float):
                return impl(repr(x))
            else:
                return impl(x)
        start = init(start)
        if stop is not None:
            stop = init(stop)
        else:
            start, stop = impl(0), start
        step = impl(1) if step is None else init(step)
        if include_end:
            stop += step
        if not step and start < stop:
            while True:
                try:
                    yield return_type(start)
                except TypeError:
                    if strict:
                        raise
                    yield return_type(str(start))
        else:
            for i in range(ceil((stop - start)/step)):    # noqa
                try:
                    yield return_type(start)
                except TypeError:
                    if strict:
                        raise
                    yield return_type(str(start))
                start += step
    def lrange(start_decade: int, end_decade: int, dx=1, x=1, 
               mantissas: list[float] | None=None) -> list[float]:
        '''Provides a logarithmic analog to the frange function.  Returns a list of
        values with logarithmic spacing.
        
        Example:  lrange(0, 2, mantissas=[1, 2, 5]) returns [1, 2, 5, 10, 20, 50].
        '''
        msg = "%s must be an integer"
        if not isinstance(start_decade, numbers.Integral):
            raise ValueError(msg % "start_decade")
        if not isinstance(end_decade, numbers.Integral):
            raise ValueError(msg % "end_decade")
        msg = "%s must lie in [1, 10)"
        if not (1 <= dx < 10):
            raise ValueError(msg % "dx")
        if not (1 <= x < 10):
            raise ValueError(msg % "x")
        if mantissas is None:
            mantissas = []
            while x < 10:
                mantissas.append(x)
                x += dx
        values = []
        for exp in range(start_decade, end_decade):
            values += [i*10**exp for i in mantissas]
        return values
    def Sequence(s: str):
        '''Return a sequence of numbers based on the specifications in the string s.
        Specifications are separated by whitespace characters and are of the forms
            a
            a:b
            a:b:c
        where a is the starting number and b is the ending number.  The increment is 1
        unless c is given.  Unlike python's range function, the endpoint is included in
        the sequence.
        
        Example:  Sequence('1:1.5:0.1   5:1:-1  1/4:3/4:1/8') returns
            [1, 1.1, 1.2, 1.3, 1.4, 1.5,
            5, 4, 3, 2, 1,
            1/4, 3/8, 1/2, 5/8, 3/4]
        '''
        out = []
        for spec in s.split(s): 
            spec = spec.strip()
            if not spec:
                continue
            c = "1"
            f = spec.split(":")
            if len(f) == 1:
                a = f[0]
                b = a
            elif len(f) == 2:
                a, b = f
            elif len(f) == 3:
                a, b, c = f
            else:
                msg = "'{}' is a bad sequence specification"
                raise ValueError(msg.format(spec))
            out += list(frange(a, b, c, include_end=True))
        def MakeIntIfPossible(x):
            i = int(x)
            if i == x:
                return i
            return x
        return [MakeIntIfPossible(i) for i in out]
    def ifrange(start: ty.Any, stop: ty.Any, step: ty.Any=1) -> ty.Any:
        '''Generator similar to frange but with a simpler implementation; note the end
        point is returned.  Use with any number type compatible with dpmath.RoundOff
        such as int, float, Fraction, Decimal, complex, mpmath.mpf, mpmath.mpc,
        uncertainties.UFloat.  You should rely on no more than 12 significant figures in
        the returned numbers.
        
        Examples:
            ifrange(1, 3) --> [1, 2, 3]
            ifrange(0, 1, 0.12) --> [0, 0.12, 0.24, 0.36, 0.48, 0.6, 0.72, 0.84, 0.96]
        '''
        import dpmath
        for i in itertools.count(start, step):
            x = dpmath.RoundOff(i)
            if x >= stop:
                return
            yield x
if 1:   # yy From util
    def flatten(seq: NestedSequence[T]) -> ty.Iterator[T]:
        '''Generator to flatten a nested sequence
        
        Algorithm 
            This elegant implementation was given to me by Google and Google's AI,
            Gemini.  Note particularly that it avoids the recursion trap that can happen
            with strings and bytes.
        
        Arguments
            seq     The nested sequence
        
        Returns
            An iterator yielding a flattened version of seq.
        
        Caution
            - Be aware of the behavior with strings and bytes.  Because it's a
              generator, you may not get what you expect.  See the second example below,
              where you might have expected to get the original string back, but instead
              you need list() to consume the generator; thus, use
              list(flatten("abc"))[0] to get the original string.

        Example
            >>> list(flatten((1, [2.5, 3.5], ["alpha", ["beta", "gamma"]], 42)))
            [1, 2.5, 3.5, 'alpha', 'beta', 'gamma', 42]
            >>> list(flatten("abc"))
            ['abc']
        '''
        if isinstance(seq, (str, bytes)):
            yield seq  # type: ignore
        elif isinstance(seq, ty.Iterable):
            for item in seq:
                yield from flatten(item)
        else:
            yield seq
    def Batch(iterable, size):
        '''Generator that gives you batches from an iterable in manageable sizes.  Slightly adapted
        from Raymond Hettinger's entry in the comments to
        http://code.activestate.com/recipes/303279-getting-items-in-batches/
        
        Example:
            for n in (3, 4, 5, 6):
                s = tuple(tuple(i) for i in Batch(range(n), 3))
                print(s)
        gives
            ((0, 1, 2),)
            ((0, 1, 2), (3,))
            ((0, 1, 2), (3, 4))
            ((0, 1, 2), (3, 4, 5))
            
        Another way of doing this is with slicing (but you'll need to have the whole iterable in memory
        to do this):
            def Pick(iterable, size):
                i = 0
                while True:
                    s = iterable[i:i + size]
                    if not s:
                        break
                    yield s
                    i += size
        '''
        def counter(x):
            counter.n += 1
            return counter.n//size
        counter.n = -1
        for _, g in itertools.groupby(iterable, counter):
            yield g
    def VisualCount(seq, n=None, char="*", width=None, indent=0):
        '''Return a list of strings representing a histogram of the items in the iterable seq.  If the
        values in the sequence can be sorted, the histogram will be shown by increasing item value;
        otherwise, the items will be shown sorted by frequency.
        
        n       Return the n largest items if n is not None.
        char    String to build the histogram element.
        width   Fit each element into this width.  If none, use the value of
                the COLUMNS environment variable or 79 if it isn't defined.
        indent  Indent each line by this amount.
        
        Note:  the width calculations are only correct if the length of the char string is 1.
        
        Example:
            seq = [1,1,1,1,1,8,8,8,9,9,9,9,9,9,9,9,9,9,9]
            for i in VisualCount(seq, width=40, indent=8):
                print(i)
            prints
                1 *************
                8 ********
                9 ******************************
        '''
        counts = ItemCount(seq, n=n)
        try:
            counts = sorted(counts)  # Sort by item values if possible
        except TypeError:
            pass
        max_obj_len = max([len(str(i[0])) for i in counts])
        max_count = max([i[1] for i in counts])
        if width is None:
            width = int(os.environ.get("COLUMNS", 80)) - 1
        max_hist_len = width - indent - 1 - max_obj_len
        assert max_hist_len > 0
        # Scale counts to fit on screen
        counts = [(i, int(j/max_count*max_hist_len)) for i, j in counts]
        # Construct the output list
        output = []
        for item, count in counts:
            s = "{}{:{}s} ".format(" "*indent, str(item), max_obj_len)
            output.append(s + char*count)
        return output
    def hyphen_range(s):
        '''Takes a set of range specifications of the form "a-b" and returns a list of
        integers between a and b inclusive.  The string s will be separated on whitespace
        after commas are replaced by spaces.
        
        See unrange() for doing the opposite thing.
        
        Examples:
            "" returns []
            "1" returns [1]
            "2 3 4" returns [2, 3, 4]
            "2-4" returns [2, 3, 4]
            "4 3 2" returns [4, 3, 2]
            "4-2" returns [4, 3, 2]
            "1--2" returns [1, 0, -1, -2]
            "-1--3" returns [-1, -2, -3]
            "-3--1" returns [-3, -2, -1]
            "1-3 5 10-8" returns [1, 2, 3, 5, 10, 9, 8]
        '''
        if not isinstance(s, str):
            raise TypeError("s must be a string")
        msg = f"{0!r} is of improper form"
        fields, o = s.replace(",", " ").split(), []
        for item in fields:
            # See if it's a single integer
            try:
                o.append(int(item))
                continue
            except Exception:
                pass
            if item.startswith("-"):
                n = item.count("-")
                # It must have at least 2 hyphens in it, otherwise it would have been caught
                # as an integer (unless e.g. it's a float or bad syntax)
                if n < 2 or n > 3:
                    raise ValueError(msg.format(item))
                f = item[1:].split("-", maxsplit=1)
                try:
                    num1 = int("-" + f[0])
                    num2 = int(f[1])
                    if num1 <= num2:
                        o.extend(list(range(num1, num2 + 1)))
                    else:
                        o.extend(list(range(num1, num2 - 1, -1)))
                except Exception as e1:
                    raise ValueError(msg.format(item)) from e1
            else:
                f = item.split("-", maxsplit=1)
                try:
                    num1, num2 = [int(i) for i in f]
                    if num1 <= num2:
                        o.extend(list(range(num1, num2 + 1)))    
                    else:
                        o.extend(list(range(num1, num2 - 1, -1)))
                except Exception as e:
                    raise ValueError(msg.format(item)) from e
        return o
    def unrange(seq, sort_first=False, sep="─"):   # Note ─ is required for e.g. -4 to -1
        '''Turn a sequence of integers seq into a collection of ranges and return as a string.  It
        provides a string summary of the ranges in the sequence.  See unrange_real() for sequences of
        real numbers.
        
        If sort_first is True, the sequence is sorted before processing.  The sep string is used to
        separate a number range.
        
        Examples: | represents the sep character
            seq = [1, 5, 6, 7, 3, 4, 8, 10, 11, 12]
            unrange(seq, sort_first=True)  outputs 1 3|8 10|12
            unrange(seq, sort_first=False) outputs 1 5|7 3|4 8 10|12
            seq = [-1, -5, -6, -7, -3, -4, -8, -10, -11, -12]
            unrange(seq, sort_first=True)  outputs -12|-10 -8|-3 -1
            unrange(seq, sort_first=False) outputs -1 -5 -6 -7 -3 -4 -8 -10 -11 -12
        '''
        if not seq:
            return ""
        dq = deque(sorted(seq)) if sort_first else deque(seq)
        in_sequence = False
        lastx = dq.popleft()
        out = [lastx]
        while dq:
            x = dq.popleft()
            if not isinstance(x, int):
                raise TypeError(f"{x!r} is not an integer")
            if not in_sequence and x == out[-1] + 1:
                in_sequence = True
            elif in_sequence:
                if x != lastx + 1:
                    in_sequence = False
                    out.extend([sep, lastx])
                    # Restart for the next range
                    out.append(x)
            else:
                out.append(x)
            lastx = x
        if in_sequence:
            out.extend([sep, lastx])
        s = " ".join([str(i) for i in out])
        u = s.replace(" " + sep + " ", sep)
        return u
    def unrange_real(seq, sort_first=False, sep="┅"):
        '''Turn a sequence of numbers seq into a collection of ranges and return as a string.  It
        provides a string summary of the ranges in the sequence.  See unrange() for sequences of
        integers.
        
        If sort_first is True, the sequence is sorted before processing.  The sep string is used to
        separate a number range.
        
        Note:  no knowledge about the sequence elements being real numbers is used; the only
        operation used is ordering by the >= operator.  Thus, any sequence of items that can be
        ordered by >= can be converted to a range.
        
        Examples:
            seq = [1.0, 2.2, 3.1, 2.7, 8.1]
            unrange_real(seq, sort_first=True)  outputs 1.0┅8.1
            unrange_real(seq, sort_first=False) outputs 1.0┅3.1 2.7┅8.1
        '''
        if not seq:
            return ""
        dq = deque(sorted(seq)) if sort_first else deque(seq)
        out, seq = [], []
        while dq:
            x = dq.popleft()
            seq = [x]
            while dq and dq[0] >= seq[-1]:
                seq.append(dq.popleft())
            s = f"{seq[0]}"
            if len(seq) > 1:
                s += f"{sep}{seq[-1]}"
            out.append(s)
            if not dq:
                break  # Finished
        return " ".join(out)
    def Unique(seq):
        '''Generator to return only the unique elements in sequence.  The order of the items in the
        sequence is maintained.
        '''
        found = set()
        for item in seq:
            if item in found:
                continue
            else:
                found.add(item)
                yield item
    def transpose(seq, typ=list, check=False):
        '''Return the transpose of a nested two-dimensional sequence, such as an n x m matrix.
        len(seq) is n and len(seq[i]) is m for i in range(0, n).
        
        typ:  The returned sequence will be of type typ, with each nested sequence also of type typ.
        
        check:  If check is True, then checks are made on seq to ensure it's of proper type.
            If checks are not satisfied, a ValueError exception is raised.  I recommend not
            using checking in production code because copies of seq are made, using up
            memory.
            
        Example:
            data = [[1, 2],
                    [3, 4],
                    [5, 6]]
            transpose(data) --> [[1, 3, 5],
                                [2, 4, 6]]
                            
        '''
        if check:
            # seq can't be a string, set, or dict
            if isinstance(seq, (str, dict, set)):
                raise TypeError("seq cannot be a string, set, or dictionary")
            # seq must be an iterable
            try:
                iter(seq)
            except TypeError as e:
                raise TypeError("seq is not an iterable") from e
            # seq must be an n x m nested sequence
            nrows = len(seq)  # Number of rows
            try:
                ncols = len(seq[0])  # Number of columns
            except Exception as e:
                if seq:  # Empty sequence ok
                    raise TypeError("seq[0] is not a sequence") from e
            # Look for extra dimensionality
            if seq:
                num_elements = nrows*ncols
                if len(Flatten(seq)) != num_elements:
                    raise TypeError(
                        "seq is not a proper 2D nested list representing a matrix"
                    )
            # Each sequence in seq must have the same length
            if seq and not all(len(i) == ncols for i in seq):
                raise TypeError(f"seq row lengths not all {ncols}")
        if not seq:
            return typ(seq)
        # There are two algorithms here:  one using map and the other using zip.  I prefer
        # using zip because the strict keyword gives us some automatic checking.  Using
        # timeit, measurements show that transposing a 20x10 matrix of floats takes 2.5 μs
        # for the zip implementation and 3.4 μs for the map implementation, so zip is the
        # default.
        if 1:
            seqT = typ(typ(j) for j in zip(*[typ(i) for i in seq], strict=True))
        else:
            seqT = typ(map(lambda *x: typ(x), *seq))
        if check:  # transpose(seqT) == seq
            orig = list(map(list, seq))
            tseq = transpose(seqT, typ=list)
            Assert(orig == tseq)
        return seqT
    def Ranges(seq, validate=False):
        '''seq is a sequence of integers.  This function will return the sequence as a
        list of either 2-tuples or single integers.  The 2-tuples represent the
        arguments to range() to reproduce the original sequence of integers.  If
        validate is True, the returned list will be validated by reproducing the
        original sequence.
        
        Examples
            [1, 2, 3, 5] --> [(1, 4), 5]
            [1, 3, 2, 5] --> [1, 3, 2, 5]
        
        The intended use case is a form of "compression" for long sequences and an index
        case is the set of Unicode codepoints, where I wanted to see how much shorter
        such a representation is than the set of integers.
        
        The algorithm is derived from 
        https://stackoverflow.com/questions/3429510/pythonic-way-to-convert-a-list-\
        of-integers-into-a-string-of-comma-separated-range/3430231#3430231
        and is the 7 Aug 2010 answer due to John La Rooy.  It's a neat solution and I 
        thank La Rooy and StackOverflow for posting the answer.
        
            Content of above link
            # Source - https://stackoverflow.com/a
            # Posted by John La Rooy, modified by community. See post 'Timeline' for change history
            # Retrieved 2026-01-18, License - CC BY-SA 2.5
        
            >>> from itertools import count, groupby
            >>> L=[1, 2, 3, 4, 6, 7, 8, 9, 12, 13, 19, 20, 22, 23, 40, 44]
            >>> G=(list(x) for _,x in groupby(L, lambda x,c=count(): next(c)-x))
            >>> print ",".join("-".join(map(str,(g[0],g[-1])[:len(g)])) for g in G)
            1-4,6-9,12-13,19-20,22-23,40,44
        
        Note 18 Jan 2026:  this function was broken when the selftests ran.  I attribute the
        cause to 'ruff check' telling me to get rid of the lambda function I had; so I
        defined the function f(x, c) instead and the linter was happy.  But things broke a
        week or so later when I ran the self tests.  Thus, I'll use the original code with
        the lambda in the generator.
        
        '''
        if validate:
            orig = list(seq)    # Copy of original sequence
        # Make sure all the elements of seq are integers
        if not all(isinstance(i, int) for i in seq):
            raise TypeError("Not all elements of seq are integers")
        # This is the same code used in the StackOverflow solution, substituting seq for L.
        # And things work again.
        G = [list(x) for _,x in itertools.groupby(seq, lambda x,c=itertools.count(): next(c)-x)]  # noqa
        # Convert into pairs of numbers for range()
        o = []
        for i in list(G):
            o.append((i[0], i[-1] + 1)) if len(i) > 1 else o.append(i[0])
        if validate:
            p = []
            for i in o:
                p.append(list(range(i[0], i[1]))) if isinstance(i, tuple) else p.append(i)
            if Flatten(p) != orig:
                raise ValueError("Validation failed")
        return o
    class PPSeq:
        '''Format sequences for pretty printing
        Floats must be in [0, 1].
        
        Example:
            p = PPSeq(bits_per_number=32)
            a = [.4, .12, .33, .16000]
            print(p(a))
        prints
            [0.4000000000, 0.1200000000, 0.3300000000, 0.1600000000]
        '''
        def __init__(self, bits_per_number=8):
            self._bpn = bits_per_number
        def __call__(self, seq, **kw):
            "Return a pretty string form of seq"
            # Get keyword arguments
            exp = kw.get("exp", False)  # Show bits exponent
            brackets = kw.get("brackets", True)  # Enclose in brackets
            comma = kw.get("comma", True)  # Separate with commas
            sep = kw.get("sep", " ")  # Element separation string
            # Get the container type and decorators
            if isinstance(seq, tuple):
                left, right = "(", ")"
            elif isinstance(seq, list):
                left, right = "[", "]"
            elif isinstance(seq, set):
                left, right = "{", "}"
            elif isinstance(seq, deque):
                left, right = "<", ">"
            elif isinstance(seq, bytes):
                left, right = "«", "»"
            else:
                raise TypeError("Unsupported container type")
            x = self.get_element(seq)
            # Must be an iterable
            if not IsIterable(seq):
                raise TypeError("seq isn't an iterable")
            # Must contain a supported type
            if not self.is_monotype(seq):
                raise TypeError("seq doesn't contain only one numerical type")
            # Get strings
            if isinstance(x, int):
                myseq = [self.format(i) for i in seq]
            else:
                myseq = [self.format(float(i)) for i in seq]
            s = "," if comma else ""
            s += sep
            t = s.join(myseq)
            if brackets:
                t = f"{left}{t}{right}"
                if exp:
                    u = "⁰¹²³⁴⁵⁶⁷⁸⁹"
                    t += "".join(u[int(i)] for i in str(self._bpn))
            return t
        def get_element(self, seq):
            if isinstance(seq, tuple):
                return seq[0]
            elif isinstance(seq, list):
                return seq[0]
            elif isinstance(seq, set):
                x = seq.pop()
                seq.add(x)
                return x
            elif isinstance(seq, deque):
                x = seq.pop()
                seq.append(x)
                return x
            elif isinstance(seq, bytes):
                return seq[0]
        def format(self, x):
            "Return the string form of number x (float or int)"
            if isinstance(x, int):
                w = len(str(2**self._bpn - 1))
                return f"{x:{w}d}"
            else:
                assert 0 <= x <= 1
                # Get the number of decimal places to display this float
                w = math.ceil(-math.log10(1/(2**self._bpn - 1)))
                return f"{x:{w + 2}.{w}f}"
        def is_monotype(self, seq):
            "Return True if seq contains only one supported type"
            x = self.get_element(seq)
            # Check the type of each element
            typ = type(x)
            if not all(type(i) is typ for i in seq):
                return False
            # Make sure they are of the allowed types
            if not isinstance(x, (int, float, decimal.Decimal, fractions.Fraction)):
                try:
                    float(x)
                except Exception:
                    return False
            return True
    def Paste(*seq, missing="", sep="\t"):
        '''Return a list whose elements are each corresponding element of the sequences in *seq,
        separated by the string sep.  If a sequence is too short, the missing string will be
        substituted.  All sequence elements will be converted to strings using str().
        
        Example:
            Paste([1, 2, "a"], ["3 4", 5], missing="X")
        will return
            ['1\t3 4', '2\t5', 'a\tX']
        '''
        result = list(itertools.zip_longest(*seq, fillvalue=missing))
        # Convert all elements to strings
        result = [str(j) for j in result]   # ∞∞1 Broken because of lint forced change
        return [sep.join(i) for i in result]
    def ItemCount(seq, n=None):
        '''Return a sorted list of (item, count) in the iterable seq, with the highest count first in
        the list.  If n is given, only return the largest n counts.  The items in seq must be
        hashable.
        
        Example:
        If a = (1, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
        returns [(5, 5), (1, 3), (4, 2), (2, 1), (3, 1)].
        
        If a = (1.0, 1, 1, 2, 3, 4, 4, 5, 5, 5, 5, 5), then ItemCount(a)
        returns [(5, 5), (1.0, 3), (4, 2), (2, 1), (3, 1)].
        
        Note that 1, 1.0, and Fraction(1, 1) hash to the same value; since a dictionary is used as the
        counting container, these are considered to be the same items.  Thus, you can get syntactically
        different results that are semantically the same.
        '''
        items = collections.defaultdict(int)
        for item in seq:
            items[item] += 1
        s = sorted(items.items(), key=operator.itemgetter(1), reverse=True)
        return s if n is None else s[:n]
    def IsIterable(x, ignore_strings=True):
        '''Return True if x is an iterable.  You can exclude strings from the things that can be
        iterated on if you wish.
        
        Note:  if you don't care whether x is a string or not, a simpler way
        is:
            try:
                iter(x)
                return True
            except TypeError:
                return False
        '''
        if ignore_strings and isinstance(x, str):
            return False
        return isinstance(x, collections.abc.Iterable)
    def IsHomogeneous(seq):
        "Return True if seq is homogeneous"
        if not seq:
            return True
        typ = type(seq[0])
        return all(type(i) is typ for i in seq)
    def grouper(data, mapper, reducer=None):
        '''Simple map/reduce for data analysis.
        
        Each data element is passed to a *mapper* function.  The mapper returns key/value pairs or None
        for data elements to be skipped.
        
        Returns a dict with the data grouped into lists.  If a *reducer* is specified, it aggregates
        each list.
        
        >>> def even_odd(elem):                     # sample mapper
        ...     if 10 <= elem <= 20:                # skip elems outside the range
        ...         key = elem % 2                  # group into evens and odds
        ...         return key, elem
        
        >>> grouper(range(30), even_odd)         # show group members
        {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}
        
        >>> grouper(range(30), even_odd, sum)    # sum each group
        {0: 90, 1: 75}
        
        Note:  from http://code.activestate.com/recipes/577676-dirt-simple-mapreduce/?in=lang-python I
        renamed the function to grouper.
        '''
        d = {}
        for elem in data:
            r = mapper(elem)
            if r is not None:
                key, value = r
                if key in d:
                    d[key].append(value)
                else:
                    d[key] = [value]
        if reducer is not None:
            for key, group in d.items():
                d[key] = reducer(group)
        return d
    def Flatten_generator(seq, ltypes=(list, tuple)):
        '''A generator that will return a flattened sequence from seq.  If an element in
        seq is of one of the types in ltypes, then it's considered to be a sequence;
        otherwise, it's a scalar element.  The method is a nice use of a deque from
        https://dev.to/miguendes/5-different-ways-to-flatten-a-list-of-lists-in-python-2cmn
        The algorithm is:
        
        - dq = deque()
        - Iterate through each element e of seq
        - If e is not one of ltypes
            - Append e to left of dq
        - else
            - dq.extendleft(reversed(e))
        - Note:  reversing is needed because of the way extendleft works:
            >>> dq = deque()
            >>> dq.extendleft([1, 2, 3])
            >>> dq
            deque([3, 2, 1]
        - Now iterate over the deque by popping the leftmost element e; if it's not an
        ltypes, yield it; otherwise extendleft(reversed(e)).
        '''
        dq = deque()
        for item in seq:
            if isinstance(item, ltypes):
                dq.extendleft(reversed(item))
            else:
                dq.appendleft(item)
            while dq:
                elem = dq.popleft()
                if isinstance(elem, ltypes):
                    dq.extendleft(reversed(elem))
                else:
                    yield elem
    def Flatten(L, max_depth=None, ltypes=(list, tuple)):
        '''Flatten every sequence in L whose type is contained in 'ltypes' to
        'max_depth' levels down the tree.  The sequence returned has the same type as
        the input sequence.  Written by Kevin L. Sitze on 2010-11-25.  From
        http://code.activestate.com/recipes/577470-fast-flatten-with-depth-control-and-oversight-over/?in=lang-python
        This code may be used pursuant to the MIT License.
        '''
        if max_depth is None:
            def make_flat(x):
                return True
        else:
            def make_flat(x):
                return max_depth > len(x)
        if callable(ltypes):
            is_sequence = ltypes
        else:
            def is_sequence(x):
                return isinstance(x, ltypes)
        r, s = [], []
        s.append((0, L))
        while s:
            i, L = s.pop()
            while i < len(L):
                while is_sequence(L[i]):
                    if not L[i]:
                        break
                    elif make_flat(s):
                        s.append((i + 1, L))
                        L = L[i]
                        i = 0
                    else:
                        r.append(L[i])
                        break
                else:
                    r.append(L[i])
                i += 1
        try:
            return type(L)(r)
        except TypeError:
            return r
    def GetSize(obj, seen=None):
        'Recursively finds size of objects in bytes'
        # Taken from https://github.com/bosswissam/pysize/blob/master/pysize.py
        size = sys.getsizeof(obj)
        if seen is None:
            seen = set()
        obj_id = id(obj)
        if obj_id in seen:
            return 0
        # Important mark as seen *before* entering recursion to gracefully handle
        # self-referential objects
        seen.add(obj_id)
        if hasattr(obj, '__dict__'):
            for cls in obj.__class__.__mro__:
                if '__dict__' in cls.__dict__:
                    d = cls.__dict__['__dict__']
                    if inspect.isgetsetdescriptor(d) or inspect.ismemberdescriptor(d):
                        size += GetSize(obj.__dict__, seen)
                    break
        if isinstance(obj, dict):
            size += sum(GetSize(v, seen) for v in obj.values())
            size += sum(GetSize(k, seen) for k in obj.keys())
        elif hasattr(obj, '__iter__') and not isinstance(obj, (str, bytes, bytearray)):
            try:
                size += sum(GetSize(i, seen) for i in obj)
            except TypeError as e:
                raise TypeError(f"nable to get size of {obj}") from e
        if hasattr(obj, '__slots__'): # can have __slots__ with __dict__
            size += sum(GetSize(getattr(obj, s), seen) for s in obj.__slots__ if hasattr(obj, s))
        return size
    def GroupByN(seq, n, fill=False):
        '''Return an iterator that gives groups of n items from the sequence.  If fill is True, return
        None for any missing items.  In other words, if fill is False, groups without the full number
        of elements are discarded.
        
        Example:
            print("fill = False:")
            for i in GroupByN(range(7), 3, fill=False):
                print("  ", i)
            print("fill = True:")
            for i in GroupByN(range(7), 3, fill=True):
                print("  ", i)
        prints
            fill = False:
            (0, 1, 2)
            (3, 4, 5)
            fill = True:
            (0, 1, 2)
            (3, 4, 5)
            (6, None, None)
        ∞∞2 See grouper() recipe in itertools docs
        '''
        # Inspired by http://code.activestate.com/recipes/303060-group-a-list-into-sequential-n-tuples
        if fill:
            return itertools.zip_longest(*([iter(seq)]*n), fillvalue=None)
        else:
            return zip(*([iter(seq)]*n))    # noqa

if __name__ == "__main__":
    if 1:  # Standard imports
        import collections
        import decimal
        import fractions
        import functools
        import sys
        import timeit
    if 1:  # Custom imports
        import lwtest
        import trm
        try:
            import mpmath
            _have_mpmath = True
        except ImportError:
            _have_mpmath = False
        try:
            import numpy
            _have_numpy = True
        except ImportError:
            _have_numpy = False
    if 1:  # Import symbols
        partial = functools.partial
        deque = collections.deque
        D = decimal.Decimal
        #
        t = trm.Trm()
        run = lwtest.run
        assert_equal = lwtest.assert_equal
        raises = lwtest.raises
        Assert = lwtest.Assert
    if 1:  # Global variables
        pass
    if 1:  # Utility
        def GetColors():
            t.err = t.red
            t.dbg = t.lil
        def Dbg(*p, **kw):
            if g.dbg:
                print(f"{t.dbg}", end="")
                print(*p, **kw)
                print(f"{t.n}", end="")
        def MeasureTiming():
            x = f.flt(0)
            x.N = 2     # Show only two figures
            global seq, b
            print("DupNodup")
            for a in ((True, "Type not important"), (False, "Type important")):
                b, seq = a
                print(f"  {seq}")
                for i in (3, 4, 5, 6):
                    seq = list(range(10**i)) + [0.0]  # seq has one duplicate
                    tm = timeit.timeit('DupNodup(seq, type_important=b)', globals=globals(), number=1)
                    print(f"    1e{i}:  {f.flt(tm).engsi}s")
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
                'Return distances between numbers in seq'
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
            if 1:   # Test corner cases
                # Arguments need to be integers
                with raises(TypeError):
                    list(iDistribute(1.0, 1, 2))
                with raises(TypeError):
                    list(iDistribute(1, 1.0, 2))
                with raises(TypeError):
                    list(iDistribute(1, 1, 2.0))
                # Must have a < b
                with raises(ValueError):
                    list(iDistribute(2, 2, 1))
                # n must be > 1
                with raises(ValueError):
                    list(iDistribute(1, 2, 1))
                # No solution
                with raises(ValueError):
                    list(iDistribute(5, 1, 1))
        def Test_fDistribute():
            a, b, n = 0, 1, 3
            expected = [0.0, 0.5, 1.0]
            for impl in (float, 
                         decimal.Decimal,
                         fractions.Fraction, 
                         mpmath.mpf if _have_mpmath else float
                        ):
                s = list(fDistribute(n, a, b, fpimpl=impl))
                Assert(s == expected)                           # Numerically correct
                Assert(all(isinstance(i, impl) for i in s))     # Of the correct type
            if 1:   # Test corner cases
                with raises(TypeError):     # First argument needs to be an integer
                    list(fDistribute(1.0, 1, 2))
                with raises(ValueError):    # Must have n > 1
                    list(fDistribute(1, 1, 2))
                with raises(TypeError):     # a must be int or impl
                    list(fDistribute(2, "1", 2))
                with raises(TypeError):     # b must be int or impl
                    list(fDistribute(2, 1, "2"))
                # Must have a < b
                with raises(ValueError):
                    list(fDistribute(2, 2, 1))
        def Test_GetClosest():
            low, high = -3, 6
            seq = (4, low, high, 1)  # Unsorted sequence
            sseq = (low, 1, 4, high)  # Sorted sequence
            if 1:
                # Test for each type of is_sorted.  This makes sure they each get the same results,
                # except when the unresolved keyword is different.
                for k in (None, False, True):
                    F = partial(GetClosest, is_sorted=k)
                    seq = sseq if k else seq
                    if k is None:
                        raises(ValueError, F, -1e99, seq, unresolved=None)
                        raises(ValueError, F, 1e99, seq, unresolved=None)
                        Assert(F(-1e99, seq) == seq[0])
                        Assert(F(1e99, seq) == seq[0])
                    else:
                        Assert(F(-1e99, seq) == low)
                        Assert(F(1e99, seq) == high)
                    Assert(F(-40, seq) == low)
                    Assert(F(-4, seq) == low)
                    # Note x can be a float also
                    Assert(F(-4.0, seq) == low)
                    Assert(F(-3, seq) == low)
                    Assert(F(-2, seq) == low)
                    Assert(F(-1, seq) == low)
                    Assert(F(0, seq) == 1)
                    Assert(F(1, seq) == 1)
                    Assert(F(2, seq) == 1)
                    Assert(F(3, seq) == 4)
                    Assert(F(4, seq) == 4)
                    Assert(F(5, seq) == 4)
                    Assert(F(6, seq) == high)
                    Assert(F(7, seq) == high)
                    Assert(F(20, seq) == high)
                    Assert(F(100, seq) == high)
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
                        return f.flt((x + y)**0.5)
                seq = (Pt(0, 0), Pt(-3, 6), Pt(4, 8), Pt(2, 0))
                F = partial(GetClosest, is_sorted=None)
                def metric(a, b):
                    return a.dist(b)
                Assert(F(Pt(0.1, 0.1), seq, distance=metric) == Pt(0, 0))
                Assert(F(Pt(-0.1, -0.1), seq, distance=metric) == Pt(0, 0))
                Assert(F(Pt(-100, 0.1), seq, distance=metric) == Pt(-3, 6))
                Assert(F(Pt(0, 1000), seq, distance=metric) == Pt(4, 8))
                Assert(F(Pt(1, 0), seq, distance=metric) == Pt(0, 0))
                Assert(F(Pt(1.0001, 0), seq, distance=metric) == Pt(2, 0))
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
            Assert(GetNum(s, typ=f.flt) == [1.0, 2.0, 3.0, 4.0])
            Assert(GetNum(s, typ=D) == [D(1), D(2), D(3), D(4)])
            Assert(GetNum(["1.0093753795"], typ=f.flt) == [1.0093753795])
        def Test_Clamp():
            rgb = (0.03, 1.223, 0.855)
            RGB = tuple(Clamp(rgb))     # Default behavior
            Assert(RGB == (0.03, 1.0, 0.855))
            # Typical use case:  scaling (r, g, b) when elements on [0, 1] to int on [0, 255]
            RGB = tuple(Clamp((int(i*256) for i in rgb), low=0, high=255))
            Assert(RGB == (7, 255, 218))
            # Check it works with the Decimal type
            seq = [D(int(i*256)) for i in rgb]
            RGB = tuple(Clamp(seq, low=0, high=255))
            Assert(RGB == (D(7), D(255), D(218)))
        def Test_Batch():
            s = "0123456789"
            r = ("012", "345", "678", "9")
            for i, b in enumerate(Batch(s, 3)):
                Assert(r[i] == "".join(list(b)))
    if 1:  # Testing frange etc. stuff
        if 1:  # Global variables
            n, N = 10, 100000  # "Large" numbers
            s = "9.6001 9.6002 9.6003 9.6004 9.6005 9.6006 9.6007 9.6008 9.6009"
            eps = 1.0/10**sys.float_info.dig
        def Test_frange_Normal_one_parameter():
            got = list(frange(str(n)))
            expected = [float(i) for i in range(n)]
            Assert(got == expected)
        def Test_frange_Normal_one_parameter_Decimals():
            got = list(frange(str(n), return_type=decimal.Decimal))
            expected = [decimal.Decimal(i) for i in range(n)]
            Assert(got == expected)
        def Test_frange_Normal_two_parameters():
            got = list(frange(str(n//2), str(n)))
            expected = [float(i) for i in range(n//2, n)]
            Assert(got == expected)
        def Test_frange_Normal_two_parameters_Decimals():
            got = list(frange(str(n//2), str(n), return_type=decimal.Decimal))
            expected = [decimal.Decimal(i) for i in range(n//2, n)]
            Assert(got == expected)
        def Test_frange_Normal_three_parameters():
            got = list(frange("9.6001", "9.601", "0.0001"))
            expected = [float(i) for i in s.split()]
            Assert(got == expected)
        def Test_frange_Normal_three_parameters_Decimals():
            got = list(frange("9.6001", "9.601", "0.0001", return_type=decimal.Decimal))
            expected = [decimal.Decimal(i) for i in s.split()]
            Assert(got == expected)
        def Test_frange_Counting_down():
            got = list(frange(str(n), "0", "-1"))
            expected = [float(i) for i in range(n, 0, -1)]
            Assert(got == expected)
        def Test_frange_Numbers_outside_float_range():
            s = "e-28000"
            got = list(frange("1" + s, "4" + s, "1" + s, return_type=decimal.Decimal))
            expected = [decimal.Decimal("1E-28000"), decimal.Decimal("2E-28000"), decimal.Decimal("3E-28000")]
            Assert(got == expected)
            s = "e28000"
            got = list(frange("1" + s, "4" + s, "1" + s, return_type=decimal.Decimal))
            expected = [decimal.Decimal("1E28000"), decimal.Decimal("2E28000"), decimal.Decimal("3E28000")]
            Assert(got == expected)
        def Test_frange_Sequence_of_complex_numbers():
            got = list(complex(0, i) for i in frange(str(n)))
            expected = [complex(0, i) for i in range(n)]
            Assert(got == expected)
        def Test_frange_mpmath():
            if not _have_mpmath:
                return
            # Plain floating point
            got = list(frange(str(n), return_type=lambda x: mpmath.mpf(str(x))))
            expected = [mpmath.mpf(i) for i in range(n)]
            Assert(got == expected)
            # Use mpf for implementation and return type
            got = list(frange(str(n), return_type=mpmath.mpf, impl=mpmath.mpf))
            expected = [mpmath.mpf(i) for i in range(n)]
            Assert(got == expected)
            # mpmath's complex numbers
            got = list(frange(str(n), return_type=lambda x: mpmath.mpc(0, str(x))))
            expected = [mpmath.mpc(0, i) for i in range(n)]
            Assert(got == expected)
            # One would expect mpmath to work as well as Decimal in the following call:
            #   frange("9.6001", "9.601", "0.0001", return_type=mpmath.mpf, impl=mpmath.mpf)
            # I found that it doesn't work for the default 15 decimals places (it generates 10
            # numbers instead of 9, just like using impl=float).  However, changing to >= 16
            # decimal places lets the code work the same as Decimal.  Note:  I'm using an older
            # version (0.12) of mpmath (0.16 is the current version as this is written), so
            # this might work with a newer version.
            mpmath.mp.dps = 16
            got = list(
                frange("9.6001", "9.601", "0.0001", return_type=mpmath.mpf,
                impl=mpmath.mpf)
            )
            expected = [mpmath.mpf(i) for i in s.split()]
            Assert(got == expected)
        def Test_frange_numpy():
            if not _have_numpy:
                return
            # Things work OK for the following case
            got = numpy.array(list(frange(str(n))))
            expected = numpy.arange(0, n, float(1))
            Assert(list(got) == list(expected))
            # However, the following test case won't work with the default frange implementation
            # using Decimal numbers; the Decimal implementation will return 9 numbers, but both
            # numpy and frange(impl=float) will return 10 numbers.  This is the "hazard" of
            # computing with floats and their roundoff problems.  But we get things to "work"
            # (i.e., frange duplicates the output of numpy's arange) by using impl=float.
            start, stop, step = 9.6001, 9.601, 0.0001
            got = frange(start, stop, step, impl=float)
            expected = numpy.arange(start, stop, step)
            Assert(list(got) == list(expected))
        def Test_frange_fractions():
            # The following test case shows that frange can be used with a python Fraction to
            # return a sequence of Fractions.
            got = list(frange("1/3", "5", "1/3", return_type=fractions.Fraction, impl=fractions.Fraction))
            # Note that because we're using floats, we have to avoid using 5 to ensure that we get
            # the same number of elements as in got.  Again, this kind of thing is problematic with
            # the quantization errors of binary floating point arithmetic.
            start, stop, inc = 1/float(3), 5 - eps, 1/float(3)
            expected = list(frange(start, stop, inc, return_type=float, impl=float))
            Assert(len(got) == len(expected))
            # There are small differences between the numbers; we use eps to detect failures.
            for i, j in zip(got, expected, strict=True):
                Assert(abs(i - j) <= eps)
        def Test_frange_include_end():
            # Test with integers
            res = list(frange("1", "3", return_type=int))
            Assert(res == [1, 2])
            res = list(frange("1", "3", return_type=int, include_end=True))
            Assert(res == [1, 2, 3])
            # Test with floats
            res = list(frange("1", "3", "0.9"))
            Assert(res == [1.0, 1.9, 2.8])
            res = list(frange("1", "3", "0.9", include_end=True))
            Assert(res == [1.0, 1.9, 2.8, 3.7])
        def Test_frange_doctest_examples():
            # Basic frange tests
            got = list(frange("0", "1", "0.1"))
            expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            Assert(got == expected)
            #
            got = list(frange("0.125", "1", ".125"))
            expected = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
            Assert(got == expected)
            #
            R = Rational
            got = list(frange("1/8", "1", "1/8", impl=R, return_type=R))
            expected = [fractions.Fraction(i) for i in "1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            Assert(got == expected)
            # Note integers can be coerced to fractions
            got = list(frange(0, 1, "1/8", impl=R, return_type=R))
            expected = [fractions.Fraction(i) for i in "0 1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            Assert(got == expected)
            # lrange tests
            got = lrange(0, 1)
            expected = [1, 2, 3, 4, 5, 6, 7, 8, 9]
            Assert(got == expected)
            #
            got = list(lrange(0, 2))
            expected = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 20, 30, 40, 50, 60, 70, 80, 90]
            Assert(got == expected)
            #
            got = list(lrange(0, 3, mantissas=[1, 2, 5]))
            expected = [1, 2, 5, 10, 20, 50, 100, 200, 500]
            Assert(got == expected)
            #
            got = lrange(0, 2, dx=2)
            expected = [1, 3, 5, 7, 9, 10, 30, 50, 70, 90]
            Assert(got == expected)
        def Test_frange_Rational():
            R = Rational
            got = [i for i in frange("1", "4", ".6", impl=R, return_type=R)]
            expected = [R(1, 1), R(8, 5), R(11, 5), R(14, 5), R(17, 5)]
            Assert(got == expected)
        def Test_frange_flt():
            o = f.flt(1)
            # Should get floats back by default
            got = list(frange(1, o(5.7), o(0.51)))
            expected = [1.0, 1.51, 2.02, 2.53, 3.04, 3.55, 4.06, 4.57, 5.08, 5.59]
            Assert(str(got) == str(expected))
            Assert(all([isinstance(i, float) for i in got]))
            # Use flt for type
            got = list(frange(1, o(5.7), o(0.51), return_type=f.flt))
            Assert(all([isinstance(i, f.flt) for i in got]))
        def Test_frange_ifrange():
            # Basic tests
            got = list(ifrange(0, 1, 0.1))
            expected = [0.0, 0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9]
            Assert(got == expected)
            #
            got = list(ifrange(0.125, 1, 0.125))
            expected = [0.125, 0.25, 0.375, 0.5, 0.625, 0.75, 0.875]
            Assert(got == expected)
            #
            R = Rational
            got = list(ifrange(R(1, 8), 1, R(1, 8)))
            expected = [fractions.Fraction(i) for i in "1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            Assert(got == expected)
            # Note integers can be coerced to fractions
            got = list(ifrange(0, 1, R(1, 8)))
            expected = [fractions.Fraction(i) for i in "0 1/8 1/4 3/8 1/2 5/8 3/4 7/8".split()]
            Assert(got == expected)
    if 1:  # Testing for old util stuff
        def Test_GroupByN():
            n, m = 5, 3
            s = range(n)
            t = ((0, 1, 2),)
            Assert(t == tuple(GroupByN(s, m, fill=False)))
            t = ((0, 1, 2), (3, 4, None))
            Assert(t == tuple(GroupByN(s, m, fill=True)))
        def Test_GetSize():
            # Run a few simple cases from pysize's tests (I ran the full set of tests before
            # utilizing the code.  From https://github.com/bosswissam/pysize
            #
            # Empty sequences
            for i in ([], (), deque(), set()):
                Assert(sys.getsizeof(i) == GetSize(i))
            # list of collections
            collection_list = [[], {}, ()]
            pointer_byte_size = 8*len(collection_list)
            empty_list_size = sys.getsizeof([])
            empty_tuple_size = sys.getsizeof(())
            empty_dict_size = sys.getsizeof({})
            expected_size = empty_list_size*2 + empty_tuple_size + empty_dict_size + pointer_byte_size
            assert_equal(expected_size, GetSize(collection_list))
            # no double counting
            rep = ["test1"]
            obj = [rep, rep]
            obj2 = [rep]
            assert_equal(GetSize(obj), GetSize(obj2) + 8)
            # gracefully handles self referential objects
            class Test:
                pass
            obj = Test()
            obj.prop = obj
            obj2 = Test()
            assert_equal(GetSize(obj), GetSize(obj.prop))
            # strings_pv3_compat
            test_string = "abc"
            assert_equal(sys.getsizeof(test_string), GetSize(test_string))
            # custom_class
            class Point:
                def __init__(self, x, y):
                    self.x = x
                    self.y = y
            point = Point(3, 4)
            assert_equal(GetSize(point),
                        sys.getsizeof(point) +
                        sys.getsizeof(point.__dict__) +
                        sys.getsizeof('x') +
                        sys.getsizeof(3) +
                        sys.getsizeof('y') +
                        sys.getsizeof(4))
            # namedtuple
            Point = collections.namedtuple('Point', ['x', 'y'])
            point = Point(3, 4)
            assert_equal(GetSize(point),
                            sys.getsizeof(point) +
                            sys.getsizeof(3) +
                            sys.getsizeof(4))
            # st_subclass_of_namedtuple
            class Point(collections.namedtuple('Point', ['x', 'y'])):
                pass
            point = Point(3, 4)
            assert_equal(GetSize(point),
                            sys.getsizeof(point) +
                            sys.getsizeof(point.__dict__) +
                            sys.getsizeof(3) +
                            sys.getsizeof(4))
            # subclass_of_namedtuple_with_slots
            class Point(collections.namedtuple('Point', ['x', 'y'])):
                __slots__ = ()
            point = Point(3, 4)
            assert_equal(GetSize(point),
                            sys.getsizeof(point) +
                            sys.getsizeof(3) +
                            sys.getsizeof(4))
            # slots
            class slots1:
                __slots__ = ["number1"]
                def __init__(self, number1):
                    self.number1 = number1
            class slots2:
                __slots__ = ["number1", "number2"]
                def __init__(self, number1,number2):
                    self.number1 = number1
                    self.number2 = number2
            class slots3:
                __slots__ = ["number1", "number2", "number3"]
                def __init__(self, number1, number2, number3):
                    self.number1 = number1
                    self.number2 = number2
                    self.number3 = number3
            s1 = slots1(7)
            s2 = slots2(3, 4)
            s3 = slots3(4, 5, 6)
            version_addition = 0
            if hasattr(sys.version_info, 'major') and sys.version_info.major == 3:
                version_addition = 4
            # base 40 for the class, 28 per integer, +8 per element
            assert_equal(GetSize(s2), GetSize(s1) + 28 + 4 + version_addition)
            assert_equal(GetSize(s3), GetSize(s2) + 28 + 4 + version_addition)
            assert_equal(GetSize(s3), GetSize(s1) + 56 + 8 + version_addition*2) # *2 for the num of variables in difference
        def Test_flatten():
            # This is the modern type annotated version of flatten, elegantly simple and
            # high performance because it's a generator
            o = (1, [2.5, 3.5], ["alpha", ["beta", "gamma"]], 42)
            expected = [1, 2.5, 3.5, "alpha", "beta", "gamma", 42]
            Assert(list(flatten(o)) == expected)
            # Flattening a string 
            Assert(list(flatten("abc")) == ["abc"])
        def Test_Flatten():
            t.print(f"{t.orn}{__file__}:Test_Flatten needs implementation")
            #raise Exception("Needs implementation")
        def Test_grouper():
            def even_odd(elem):  # sample mapper
                if 10 <= elem <= 20:  # skip elems outside the range
                    key = elem % 2  # group into evens and odds
                    return key, elem
            got = grouper(range(30), even_odd)
            expected = {0: [10, 12, 14, 16, 18, 20], 1: [11, 13, 15, 17, 19]}
            Assert(got == expected)
            got = grouper(range(30), even_odd, sum)
            expected = {0: 90, 1: 75}
            Assert(got == expected)
        def Test_IsHomogeneous():
            a = [1, 2, 3]
            Assert(IsHomogeneous(a))
            a[1] = 2.0
            Assert(not IsHomogeneous(a))
        def Test_IsIterable():
            Assert(IsIterable("", ignore_strings=False))
            Assert(not IsIterable("", ignore_strings=True))
            Assert(IsIterable([]) and IsIterable(()))
            Assert(IsIterable({}) and IsIterable(set()))
            Assert(not IsIterable(3))
            Assert(not IsIterable("a"))
            Assert(IsIterable([]))
            Assert(IsIterable((0,)))
            Assert(IsIterable(iter((0,))))
            Assert(not IsIterable(0))
        def Test_ItemCount():
            f, F = ItemCount, fractions.Fraction
            raises(Exception, f, 1)
            raises(Exception, f, 1.0)
            raises(Exception, f, F(1, 1))
            raises(Exception, f, object())
            # Empty sequence returns empty string
            Assert(f([]) == [])
            # Elementary counting
            Assert(f([1]) == [(1, 1)])
            Assert(f([1.0]) == [(1.0, 1)])
            Assert(f([1, 1]) == [(1, 2)])
            Assert(f([1, 1, 1]) == [(1, 3)])
            # Two element types
            Assert(f([1, 2]) == [(1, 1), (2, 1)])
            Assert(f([1, 1, 2]) == [(1, 2), (2, 1)])
            Assert(f([1, 2.0]) == [(1, 1), (2.0, 1)])
            Assert(f([1.0, 2.0]) == [(1.0, 1), (2.0, 1)])
            Assert(f([1.0, 2.0, 2]) == [(2.0, 2), (1.0, 1)])
            Assert(f([1.0, 2, 2.0]) == [(2, 2), (1.0, 1)])
            Assert(f([1.0, 2, 2.0, F(2, 1)]) == [(2, 3), (1.0, 1)])
            # Show order can matter.  Thus, the results can be syntactically
            # different but semantically the same.
            Assert(f([1, 2, 1, 2]) == [(1, 2), (2, 2)])
            Assert(f([2, 1, 1, 2]) == [(2, 2), (1, 2)])
            Assert(f([2, 1, F(1, 1), 2]) == [(2, 2), (1, 2)])
            # Item type also matters
            Assert(f([1, F(1, 1)]) == [(1, 2)])
            Assert(f([1.0, F(1, 1)]) == [(1.0, 2)])
            Assert(f([F(1, 1), 1.0]) == [(F(1, 1), 2)])
            Assert(f([F(1, 1), 1]) == [(F(1, 1), 2)])
            # Fractions
            Assert(f([F(1, 2), 1]) == [(F(1, 2), 1), (1, 1)])
            Assert(f([F(1, 2), F(1, 2)]) == [(F(1, 2), 2)])
            # Show that it works with strings
            Assert(f(["a", "b", "a"]) == [("a", 2), ("b", 1)])
            # Any hashable object can be counted
            a, b = object(), object()
            Assert(f([a, b]) == [(a, 1), (b, 1)])
            # Show the n keyword returns the n largest counts
            a = [1, 2, 2, 3, 3, 3]
            Assert(f(a, n=1) == [(3, 3)])
            Assert(f(a, n=2) == [(3, 3), (2, 2)])
            Assert(f(a, n=3) == [(3, 3), (2, 2), (1, 1)])
            Assert(f(a, n=4) == [(3, 3), (2, 2), (1, 1)])
        def Test_Paste():
            a = ["a", "b", 1]
            b = ["d", "e"]
            c = ["f"]
            s = Paste(a, b, c)  # noqa  ∞∞1 Remove when Paste fixed
            t.print(f"{t.orn}{__file__}:Test_Paste needs fixing Paste() bug")
            #Assert(s == ["a\td\tf", "b\te\t", "1\t\t"])
        def Test_PPSeq():
            pp = PPSeq()
            x = (44, 128, 250)
            Assert(pp(tuple(x)) == "( 44, 128, 250)")
            Assert(pp(tuple(x), exp=True) == "( 44, 128, 250)⁸")
            Assert(pp(list(x)) == "[ 44, 128, 250]")
            Assert(pp(set(x)) == "{128, 250,  44}")
            Assert(pp(deque(x)) == "< 44, 128, 250>")
            Assert(pp(bytes(x)) == "« 44, 128, 250»")
        def Test_Ranges():
            # Empty sequence
            assert Ranges([], validate=False) == []
            assert Ranges([], validate=True) == []
            # Simple unsorted sequence
            seq = [2, 1, -3, 7]
            r = Ranges(seq)
            assert r == seq
            # Algorithm author's example
            seq = [1, 2, 3, 4, 6, 7, 8, 9, 12, 13, 19, 20, 22, 23, 40, 44]
            r = Ranges(seq)
            assert r == [(1, 5), (6, 10), (12, 14), (19, 21), (22, 24), 40, 44]
            # Equal elements
            seq = [2, 2, 2, 2]
            r = Ranges(seq)
            assert r == seq
            # Exception cases
            raises(TypeError, Ranges, [fractions.Fraction(1, 2)])
            raises(TypeError, Ranges, [1.0])
            raises(TypeError, Ranges, ["1"])
        def Test_transpose():
            def TestTransposeEmptySequence():
                a = []
                Assert(transpose(a) == a)
            def TestTransposeExceptions():
                raises(TypeError, transpose, lambda x: x, check=True)  # Can't be function
                raises(TypeError, transpose, "a", check=True)  # Can't be string
                raises(TypeError, transpose, dict(), check=True)  # Can't be dict
                raises(TypeError, transpose, set(), check=True)  # Can't be set
                raises(TypeError, transpose, 1, check=True)  # seq must be an iterable
                raises(TypeError, transpose, [1, [2, 3]], check=True)  # seq[0] has no len
                a = [[1, 2], [3]]
                raises(TypeError, transpose, a, check=True)  # Unequal row lengths
                # Can't be a 3D matrix
                a = [[[1, 2], [3, 4]], [[5, 6], [7, 8]], [[9, 10], [11, 12]]]
                raises(TypeError, transpose, a, check=True)  # Not a 2D matrix
            def TestCommonVectorsAndMatrixes():
                # Row vector
                a = [[1, 2, 3]]
                Assert(transpose(a) == [[1], [2], [3]])
                Assert(transpose(transpose(a)) == a)
                # Column vector
                a = [[1], [2], [3]]
                Assert(transpose(a) == [[1, 2, 3]])
                Assert(transpose(transpose(a)) == a)
                # 2x3 to 3x2 to 2x3
                a = [list("abc"), list("def")]
                Assert(transpose(a) == [list("ad"), list("be"), list("cf")])
                Assert(transpose(transpose(a)) == a)
                # 2x2 to 2x2 to 2x2
                a = [list("ab"), list("cd")]
                Assert(transpose(a) == [list("ac"), list("bd")])
                Assert(transpose(transpose(a)) == a)
            def TestGetDesiredType():
                a = ((1, 2), (3, 4))
                b = transpose(a)
                # List of list by default
                Assert(isinstance(b, list))
                Assert(isinstance(b[0], list))
                Assert(isinstance(b[1], list))
                Assert(isinstance(b, list))
                # Tuple if you ask for it
                b = transpose(a, typ=tuple)
                Assert(isinstance(b[0], tuple))
                Assert(isinstance(b[1], tuple))
                Assert(isinstance(b, tuple))
            def TestTransposeOfTransposeIsOriginal():
                # With tuple
                a = ((1, 2), (3, 4))
                b = transpose(a)
                c = transpose(b, typ=tuple)
                Assert(a == c)
                # With list
                a = [[1, 2], [3, 4]]
                b = transpose(a)
                c = transpose(b)
                Assert(a == c)
            TestTransposeEmptySequence()
            TestTransposeExceptions()
            TestCommonVectorsAndMatrixes()
            TestGetDesiredType()
            TestTransposeOfTransposeIsOriginal()
        def Test_Unique():
            def f(x):
                return list(Unique(x))
            Assert(f([]) == [])
            Assert(f([1, 1, 1]) == [1])
            Assert(f([1, 2, 1]) == [1, 2])
            Assert(tuple(Unique([1, 2, 1])) == (1, 2))
            Assert(f(["Mon", "Tue", 1, "Tue"]) == ["Mon", "Tue", 1])
            Assert(f(["Mon", "Tue", 1, "Tue"]) != ["Mon", 1, "Tue"])
        def Test_unrange_real():
            sep, f = "┅", unrange_real
            s = f([], sort_first=False)
            Assert(s == "")
            s = f([1], sort_first=False)
            Assert(s == "1")
            s = f([1, 2], sort_first=False)
            Assert(s == f"1{sep}2")
            s = f([1, 2, 4], sort_first=False)
            Assert(s == f"1{sep}4")
            s = f([1, 3, 4, 5, 6, 7, 8, 10, 11, 12], sort_first=False)
            Assert(s == f"1{sep}12")
            n = 10000
            s = f(range(1, n), sort_first=False)
            Assert(s == f"1{sep}{n - 1}")
            s = f([float(i) for i in range(1, n)], sort_first=False)
            Assert(s == f"1.0{sep}{float(n - 1)}")
            s = f([1.0], sort_first=False)
            Assert(s == "1.0")
            s = f([float(i) for i in range(1, n)], sort_first=False)
            Assert(s == f"1.0{sep}{float(n - 1)}")
            s = f([1.0, 2.2, 3.1, 2.7, 8.1], sort_first=False)
            Assert(s == f"1.0{sep}3.1 2.7{sep}8.1")
            s = f([1.0, 2.2, 3.1, 2.7, 8.1], sort_first=True)
            Assert(s == f"1.0{sep}8.1")
        def Test_unrange():
            sep, f = "┅", unrange
            s = f([], sort_first=False, sep=sep)
            Assert(s == "")
            s = f([1], sort_first=False, sep=sep)
            Assert(s == "1")
            s = f([1, 2], sort_first=False, sep=sep)
            Assert(s == f"1{sep}2")
            s = f([1, 2, 4], sort_first=False, sep=sep)
            Assert(s == f"1{sep}2 4")
            s = f([1, 3, 4, 5, 6, 7, 8, 10, 11, 12], sort_first=False, sep=sep)
            Assert(s == f"1 3{sep}8 10{sep}12")
            n = 10000
            s = f(range(1, n), sort_first=False, sep=sep)
            Assert(s == f"1{sep}{n - 1}")
            seq = [-i for i in (1, 3, 4, 5, 6, 7, 8, 10, 11, 12)]
            s = f(seq, sort_first=False, sep=sep)
            Assert(s == "-1 -3 -4 -5 -6 -7 -8 -10 -11 -12")
            s = f(seq, sort_first=True, sep=sep)
            Assert(s == f"-12{sep}-10 -8{sep}-3 -1")
        def Test_hyphen_range():
            for s, expected in (
                    ("", []),
                    ("1", [1]),
                    ("2 3 4", [2, 3, 4]),
                    ("2-4", [2, 3, 4]),
                    ("4 3 2", [4, 3, 2]),
                    ("4-2", [4, 3, 2]),
                    ("1--2", [1, 0, -1, -2]),
                    ("-1--3", [-1, -2, -3]),
                    ("-3--1", [-3, -2, -1]),
                    ("1-3 5 10-8", [1, 2, 3, 5, 10, 9, 8])):
                Assert(hyphen_range(s) == expected)
            
            # Things that give exceptions
            raises(TypeError, hyphen_range, 0)
            raises(TypeError, hyphen_range, 1.0)
            raises(ValueError, hyphen_range, "1.0")
            raises(ValueError, hyphen_range, "2-1.0")
            raises(ValueError, hyphen_range, "1/2")
            raises(ValueError, hyphen_range, "2-1/2")
            raises(ValueError, hyphen_range, "-1---2")
        def Test_VisualCount():
            s = (1, 1, 1, 2, "a", "a", (1, 2))
            got = "\n".join(VisualCount(s, width=20))
            expected = wrap.dedent('''
            1      *************
            a      ********
            2      ****
            (1, 2) ****''')
            Assert(got == expected)
    GetColors()
    exit(run(globals(), regexp=r"^[Tt]est_", halt=1, verbose=0)[0])
