'''
Generate the transpose of a nested list (matrix or vector) of objects
'''
if 1:   # Header
    # Copyright, license
        # These "trigger strings" can be managed with trigger.py
        #∞copyright∞# Copyright (C) 2022 Don Peterson #∞copyright∞#
        #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
        #∞license∞#
        #   Licensed under the Open Software License version 3.0.
        #   See http://opensource.org/licenses/OSL-3.0.
        #∞license∞#
        #∞what∞#
        # Transpose a rectangular matrix of objects
        #∞what∞#
        #∞test∞# run #∞test∞#
    # Standard imports
        from pprint import pprint as pp
    # Custom imports
        from util import IsIterable
        if 1:
            import debug
            debug.SetDebugger()
    # Global variables
        ii = isinstance
        __all__ = ["Transpose"]
if 1:   # Core functionality
    def Transpose(seq, homogeneous=False):
        '''seq must be a nested list or tuple of objects.  The transpose of
        the sequence seq is returned as a nested list.  If homogeneous is
        True, then each element must be of the same type.
        '''
        def IsHomogeneous(x):
            if not homogeneous:
                return
            if type(x) != Transpose.type:
                raise TypeError(f"{x!r} is not of type {Transpose.type}")
        if not ii(seq, (list, tuple)):
            raise TypeError("seq must be a list or tuple")
        nrows, ncols = Size(seq)
        trows, tcols = ncols, nrows
        if not nrows or not ncols:
            return []
        if nrows == 1 and ncols == 1:
            return list(seq)
        # Get the required type for testing homogeneity
        if homogeneous:
            item0 = seq[0]
            if ii(item0, (list, tuple)):
                item0 = item0[0]
            Transpose.type = type(item0)
        # Set up the return matrix
        out, row_vector, col_vector = [], 0, 0
        if nrows == 1 and ncols != 1:       # seq was row vector
            # Result is column vector
            col_vector = ncols
            for i in range(trows):
                out.append([0])
        elif nrows != 1 and ncols == 1:     # seq was column vector
            # Result is row vector
            row_vector = nrows
            out = [0]*tcols
        else:
            for i in range(trows):
                out.append([0])
            for i in range(trows):
                out[i] = [0]*tcols
        # Replace the elements
        if col_vector:
            for i in range(col_vector):
                j = seq[i][0] if IsIterable(seq[i]) else seq[i]
                IsHomogeneous(j)
                out[i][0] = j
        elif row_vector:
            for i in range(row_vector):
                j = seq[i][0] if IsIterable(seq[i]) else seq[i]
                IsHomogeneous(j)
                out[i] = j
        else:
            for i in range(nrows):
                for j in range(ncols):
                    IsHomogeneous(seq[i][j])
                    out[j][i] = seq[i][j]
        if 0:
            # Show the details
            print(f"{msg}")
            print(f"  seq = {seq}")
            print(f"  Size = ({nrows}, {ncols}])")
            print("  out sequence:")
            pp(out)
        return out
    def IsHomogeneous(m):
        ''' Return True if each row has the same number of columns as
        determined by Len().
        '''
        rows = Len(m)
        columns = Len(m[0])
        return all(Len(row) == columns for row in m)
    def Size(item):
        'Return (rows, columns) for item'
        rows = Len(item)
        if not rows:
            return (0, 0)
        columns = Len(item[0])
        if IsHomogeneous(item):
            if columns:
                return (rows, Len(item[0]))
            else:
                return (1, rows)    # It's a row vector
        else:
            return (rows, 1)        # It's a column vector
    def Len(item):
        '''Return the length of the item.  If it's an iterable that's not a
        string, the normal len() is returned; otherwise, 0 is returned.
        '''
        return len(item) if IsIterable(item, ignore_strings=True) else 0

if __name__ == "__main__":
    from lwtest import run, raises, assert_equal, Assert
    '''
    Identity:  Transpose(Transpose(x)) = x
    Test cases:
        ["a", "b", "c"] --> [["a"], ["b"], ["c"]
        [["a"], ["b"], ["c"] --> ["a", "b", "c"]
    '''
    def TestEmpty():
        for i in ([], ()):
            Assert(Transpose(i) == [])
    def TestRowVector():
        v = ["abc", 1]
        expected = [["abc"], [1]]
        Assert(Transpose(v) == expected)
        # One element
        for v in (["abc"], ("abc",), [44], [44.]):
            Assert(Transpose(v) == list(v))
    def TestColumnVector():
        v = [["abc"], [1]]
        expected = ["abc", 1]
        Assert(Transpose(v) == expected)
        v = (("abc",), (1,))
        Assert(Transpose(v) == expected)
    def TestMatrix():
        m = [["abc", 1], [4.8, "Another string"]]
        expected = [["abc", 4.8], [1, "Another string"]]
        Assert(Transpose(m) == expected)
    def TestHomogeneity():
        v = [1, 2]
        expected = [[1], [2]]
        Assert(Transpose(v, homogeneous=True) == expected)
        v = [1, "2"]
        with raises(TypeError):
            Transpose(v, homogeneous=True)
            
    exit(run(globals(), halt=True)[0])
