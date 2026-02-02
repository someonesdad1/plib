'''
Homogeneous list
'''
if 1:  # Header
    _pgminfo = '''
        <oo gist ∞ Homogeneous list oo>
        <oo desc ∞ oo>
        <oo copy ∞ Copyright © 2021 Don Peterson oo>
        <oo lic ∞ MIT License
            Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
            The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
            THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.  IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
        oo>
        <oo ind ∞ 8 indent oo>
        <oo cat ∞ utility oo>
        <oo test ∞ run oo>
        <oo todo ∞ oo>
    '''
    if 1:  # Standard imports
        pass
    if 1:  # Custom imports
        pass
    if 1:  # Global variables
        pass
if 1:  # Classes
    class HomogenousList(list):
        '''A homogenous list which allows items only of a single type.  The
        first element of the sequence provided to the constructor determines
        the type of objects allowed to be stored in the container.
        '''
        def __init__(self, seq=None):
            self.super = super(HomogenousList, self)
            self.type = None
            if seq is not None and seq:
                self.type = type(seq[0])
                for item in seq:
                    self._check_type(item)
                    self.append(item)
        def _check_type(self, item):
            if not isinstance(item, self.type):
                raise ValueError("item must be of type {}".format(self.type))
        def append(self, item):
            if self.type is None:
                self.type = type(item)
            self._check_type(item)
            self.super.append(item)
        def extend(self, seq):
            for item in seq:
                self.append(item)
        def insert(self, i, item):
            self._check_type(item)
            self.super.insert(i, item)
        def __add__(self, seq):
            try:
                for item in seq:
                    self.append(item)
            except TypeError:
                raise TypeError("Item being added must be a sequence")

if __name__ == "__main__":
    from lwtest import run, assert_equal, raises
    def Test():
        # Construct empty list
        h = HomogenousList()
        h.append(0)
        h.append(1)
        raises(ValueError, h.append, "2")
        h1 = HomogenousList(range(2))  # Construct list with sequence
        raises(ValueError, h1.append, "2")
        assert_equal(h, list(range(2)))
        assert_equal(h1, list(range(2)))
        h.extend([2, 3])
        assert_equal(h, list(range(4)))
        raises(ValueError, h.extend, ["2"])
        h.insert(0, -1)
        assert_equal(h, [-1] + list(range(4)))
        # Show two lists with different types can't be concatenated
        g = HomogenousList(["0"])
        with raises(ValueError):
            h + g
    exit(run(globals(), halt=1)[0])
    
