'''
Intervals
    Wed 03 Sep 2014 02:23:05 PM
        I've stopped work on this because it's more likely I'll get what I
        want by modifying an interval library found on pypi because it
        will be less work.
    ----------------------------------------------------------------------

    Provides a class Interval that encapsulates a set of intervals.  The
    interval is defined by objects that have ordering semantics like
    numbers.

    You can create an Interval object and then test if a particular object
    is in the interval:

        # Sequence of intervals must be sorted in increasing order.
        # The sequence can be of any objects that have the proper
        # comparison semantics (numbers are an obvious use case).
        I = Interval([(48, 57), (65, 90), 95])  # Sequence must be sorted
        x = 48
        95 in I         --> True
        96 in I         --> False
        x in I          --> True
        float(x) in I   --> True
        x - 1 in I      --> False
        
    An example would be the set of Unicode codepoints that are allowed in
    identifier names in a particular python distribution (see 'Identifiers
    and keywords' under 'Lexical analysis' in the 'Python Language
    Reference' documentation that comes with python.

    The bisect module is used to perform a binary search, so time for a
    membership check will be O(log(len(intervals))) where intervals is the
    sequence passed to the constructor.

'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Intervals (obsolete) oo>
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
        from bisect import bisect_right
    if 1:  # Custom imports
        if 0:
            import debug
            debug.SetDebugger()
    if 1:  # Global variables
        __all__ = ["Interval"]
if 1:  # Classes
    class Interval(object):
        '''Encapsulate an object or 2-sequence of objects so that they can
        be ordered.  The objects must have ordering semantics.
        Multiplication of two Interval objects returns False if the two
        intervals do not overlap and True if there's any overlap.
        '''
        def __init__(self, item):
            if Interval.is_2(item):
                self.item = tuple(item)
            else:
                self.item = (item, item)
        @classmethod
        def is_2(self, x):
            '''Return True if x is a 2-sequence.'''
            if isinstance(x, str):
                return False
            try:
                return True if len(x) == 2 else False
            except TypeError:
                return False
        def __lt__(self, other):
            if not isinstance(other, Interval):
                raise ValueError("other must be an Interval object")
            return self.item < other.item
        def __eq__(self, other):
            if not isinstance(other, Interval):
                raise ValueError("other must be an Interval object")
            return self.item == other.item
        def __contains__(self, other):
            '''other is an object that is orderable with respect to the
            interval's endpoints.
            '''
            return self.item[0] <= other and other <= self.item[1]
        def __mul__(self, other):
            if not isinstance(other, Interval):
                raise ValueError("other must be an Interval object")
            if other.items[0] in self or other.items[1] in self:
                return True
            elif self.items[0] in other or self.items[1] in other:
                return True
            return False
    class IntervalContainer(object):
        def __init__(self, intervals, check=False):
            '''intervals must be a sequence of Interval objects (it can
            also be empty).  If check is True, the intervals sequence is
            checked to ensure that it is in sorted order and no intervals
            overlap.
            '''
            self.intervals = intervals
            if check:
                self.check()
        def __contains__(self, thing):
            '''Implements the 'in' functionality.  Uses binary search to
            locate the nearest element.
            '''
            if not self.intervals:
                return False
            raise ValueError
        def check(self):
            '''Check that self.intervals is in sorted order and elements
            can be compared.  Raise ValueError if not.
            '''
            for i, curr in enumerate(self.intervals):
                is_2 = self.is_2(curr)
                if is_2 and curr[0] >= curr[1]:
                    msg = "Item %d ('%s') not properly ordered sequence"
                    raise ValueError(msg % (i, curr))
                if not i:
                    continue  # Need predecessor for comparison
                prev = self.intervals[i - 1]
                a = prev[1] if self.is_2(prev) else prev
                b = curr[0] if is_2 else curr
                if a >= b:
                    msg = "Not sorted:  item %d ('%s') >= item %d ('%s')"
                    raise ValueError(msg % (i - 1, prev, i, curr))
if 1:  # Core functionality
    def LeastRightmost(x, seq):
        '''Return the index of the rightmost value in sequence seq that is
        less than or equal to x; return None if it can't be found.
        Adapted from find_le() in the section 'Searching Sorted Lists' in
        the bisect module's documentation.
        '''
        index = bisect_right(seq, x)
        return index - 1 if index else None

if __name__ == "__main__":
    II = Interval([(48, 57), (65, 90), 95])
    II = Interval(["a", "d", "c"])
