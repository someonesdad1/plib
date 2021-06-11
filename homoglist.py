'''
Homogeneous list
'''
if 1:  # Copyright, license
    # These "trigger strings" can be managed with trigger.py
    #∞copyright∞# Copyright (C) 2021 Don Peterson #∞copyright∞#
    #∞contact∞# gmail.com@someonesdad1 #∞contact∞#
    #∞license∞#
    #   Licensed under the Open Software License version 3.0.
    #   See http://opensource.org/licenses/OSL-3.0.
    #∞license∞#
    #∞what∞#
    # <programming> Homogeneous list
    #∞what∞#
    #∞test∞# run #∞test∞#
    pass
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
        h1 = HomogenousList(range(2))    # Construct list with sequence
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
